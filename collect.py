#!/usr/bin/env python3
"""Hourly collector for the "اتاق پایش ریسک منطقه" dashboard.

Gathers raw signals with plain HTTP (no AI), keeps a rolling state,
computes baselines/anomalies and writes a compact data/digest.json that the
Claude monitoring runs read first. Every source is independent: a failing
source is recorded in sources_status and never stops the others.
"""
import csv, hashlib, html, io, json, math, os, re, statistics, sys, time
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
import xml.etree.ElementTree as ET

import requests

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data")
STATE_F = os.path.join(DATA, "state.json")
DIGEST_F = os.path.join(DATA, "digest.json")
NOW = datetime.now(timezone.utc)
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"}
NEWS_WINDOW_H = 12
MIL_WINDOW_H = 24
STATUS = {}


def iso(dt):
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_iso(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def get(url, timeout=25, **kw):
    r = requests.get(url, headers=UA, timeout=timeout, **kw)
    r.raise_for_status()
    return r


def guard(name):
    def deco(fn):
        def run(*a, **k):
            try:
                out = fn(*a, **k)
                STATUS.setdefault(name, "ok")
                return out
            except Exception as e:  # noqa
                STATUS[name] = f"error: {type(e).__name__}: {str(e)[:160]}"
                return None
        return run
    return deco


# ---------------------------------------------------------------- ADS-B
ADSB_POINTS = [
    ("Gulf", 27, 52), ("Israel", 31.5, 35), ("Saudi/Qatar", 24.5, 47),
    ("Iraq/Kuwait", 30, 44), ("Cyprus", 34.5, 32), ("Ramstein", 49.44, 7.6),
    ("UK", 52, 0), ("Crete", 36, 24), ("Incirlik", 38, 35), ("Tehran", 34, 50),
]
GROUPS = {
    "tanker": {"K35R", "K35E", "KC10", "K46", "A332", "B762", "A310", "B703", "MRTT", "KC2"},
    "transport": {"C17", "C5M", "C5", "C130", "C30J", "A400", "C2", "KC39", "IL76", "C135", "C27J"},
    "bomber": {"B52", "B1", "B2", "B21"},
    "isr": {"R135", "E3TF", "E3CF", "E6", "P8", "U2", "RQ4", "Q4", "E7", "MQ9", "HRON", "E2", "GLF5", "E8", "C12", "EP3"},
}


def group_of(t):
    for g, s in GROUPS.items():
        if t in s:
            return g
    return "other"


@guard("adsb")
def collect_adsb(state):
    points, seen = [], {}
    errs = 0
    for name, lat, lon in ADSB_POINTS:
        try:
            ac = get(f"https://api.adsb.lol/v2/point/{lat}/{lon}/250").json().get("ac") or []
        except Exception as e:
            errs += 1
            points.append({"area": name, "total": None, "mil": None, "err": str(e)[:80]})
            continue
        mil = [a for a in ac if (a.get("dbFlags") or 0) & 1]
        points.append({"area": name, "total": len(ac), "mil": len(mil)})
        for a in mil:
            hx = a.get("hex")
            t = (a.get("t") or "").upper()
            seen[hx] = {"hex": hx, "cs": (a.get("flight") or "").strip(), "type": t, "reg": a.get("r"),
                        "group": group_of(t), "area": name, "lat": a.get("lat"), "lon": a.get("lon"),
                        "alt": a.get("alt_baro"), "track": a.get("track")}
    if errs == len(ADSB_POINTS):
        raise RuntimeError("all ADS-B points failed")
    if errs:
        STATUS["adsb"] = f"partial: {errs} point(s) failed"
    # rolling 24h sightings by hex
    sight = state.setdefault("mil_sightings", {})
    for hx, a in seen.items():
        prev = sight.get(hx)
        a["first"] = prev["first"] if prev else iso(NOW)
        a["last"] = iso(NOW)
        a["areas"] = sorted(set((prev or {}).get("areas", [])) | {a["area"]})
        sight[hx] = a
    cutoff = NOW - timedelta(hours=MIL_WINDOW_H)
    for hx in [h for h, a in sight.items() if parse_iso(a["last"]) < cutoff]:
        del sight[hx]
    # hourly counts for baseline (14 days)
    cnt = {g: sum(1 for a in seen.values() if a["group"] == g) for g in GROUPS}
    cnt["mil"] = len(seen)
    hist = state.setdefault("adsb_hist", [])
    hist.append({"t": iso(NOW), **cnt})
    state["adsb_hist"] = [h for h in hist if parse_iso(h["t"]) > NOW - timedelta(days=14)]
    base = {}
    for k in cnt:
        vals = [h.get(k, 0) for h in state["adsb_hist"][:-1]]
        med = statistics.median(vals) if vals else None
        p90 = sorted(vals)[int(0.9 * (len(vals) - 1))] if vals else None
        base[k] = {"now": cnt[k], "median_14d": med, "p90_14d": p90, "samples": len(vals)}
    return {"asof": iso(NOW), "points": points, "now": list(seen.values()),
            "seen_24h": sorted(sight.values(), key=lambda a: (a["group"], a["first"])), "baseline": base}


# ---------------------------------------------------------------- FIRMS
SITES = {"Natanz": (33.72, 51.73), "Fordow": (34.88, 51.0), "Isfahan": (32.6, 51.68), "Parchin": (35.52, 51.77),
         "Bandar Abbas": (27.18, 56.27), "Kharg": (29.24, 50.31), "Bushehr": (28.83, 50.89), "Arak": (34.37, 49.24),
         "Tehran": (35.69, 51.39), "Tabriz": (38.08, 46.29), "Kermanshah": (34.35, 47.1), "Khorramabad": (33.49, 48.35),
         "Shiraz": (29.6, 52.5), "Jask": (25.64, 57.77), "Chabahar": (25.3, 60.6)}
OIL_BOXES = [(30.0, 32.6, 47.5, 50.5), (27.3, 27.95, 51.8, 52.8), (29.9, 30.6, 50.4, 51.2), (29.8, 31.3, 46.9, 48.2),
             (28.7, 29.4, 47.5, 48.3), (23.0, 27.2, 48.8, 50.6), (26.3, 28.6, 48.3, 50.6), (35.0, 36.6, 43.5, 45.0),
             (24.0, 25.5, 51.2, 52.7), (24.0, 25.2, 53.0, 54.8)]


def km(a, b):
    R = 6371
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))


@guard("firms")
def collect_firms(state):
    key = os.environ.get("FIRMS_KEY")
    if not key:
        raise RuntimeError("FIRMS_KEY secret missing")
    out = {"asof": iso(NOW)}
    allpts = []
    for prod in ("MODIS_NRT", "VIIRS_NOAA20_NRT", "VIIRS_SNPP_NRT"):
        try:
            txt = get(f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/{key}/{prod}/44,25,63.5,40/1", timeout=60).text
            rows = list(csv.DictReader(io.StringIO(txt)))
        except Exception as e:
            out[prod] = {"error": str(e)[:100]}
            continue
        out[prod] = {"n": len(rows)}
        for r in rows:
            try:
                p = (float(r["latitude"]), float(r["longitude"]))
            except Exception:
                continue
            frp = float(r.get("frp") or 0)
            in_oil = any(a <= p[0] <= b and c <= p[1] <= d for a, b, c, d in OIL_BOXES)
            near = [(n, round(km(p, s))) for n, s in SITES.items() if km(p, s) <= 25]
            allpts.append({"prod": prod, "lat": p[0], "lon": p[1], "frp": frp, "date": r.get("acq_date"),
                           "time": r.get("acq_time"), "conf": r.get("confidence"), "oilgas": in_oil,
                           "near": near})
    if all("error" in out.get(p, {}) for p in ("MODIS_NRT", "VIIRS_NOAA20_NRT", "VIIRS_SNPP_NRT")):
        raise RuntimeError("all FIRMS products failed")
    out["n_total"] = len(allpts)
    out["n_not_oilgas"] = sum(1 for p in allpts if not p["oilgas"])
    out["near_sites"] = [p for p in allpts if p["near"]]
    out["top_not_oilgas"] = sorted([p for p in allpts if not p["oilgas"]], key=lambda p: -p["frp"])[:12]
    hist = state.setdefault("firms_hist", [])
    hist.append({"t": iso(NOW), "n": len(allpts), "nn": out["n_not_oilgas"]})
    state["firms_hist"] = hist[-24 * 14:]
    vals = [h["nn"] for h in state["firms_hist"][:-1]]
    out["not_oilgas_median_14d"] = statistics.median(vals) if vals else None
    return out


# ---------------------------------------------------------------- markets
YAHOO = {"brent": "BZ=F", "wti": "CL=F", "gold": "GC=F", "vix": "^VIX", "sp500": "^GSPC",
         "usd_ils": "ILS=X", "ta35": "TA35.TA", "ta125": "^TA125.TA", "dxy": "DX-Y.NYB"}


STOOQ = {"brent": "cb.f", "wti": "cl.f", "gold": "gc.f", "vix": "^vix", "sp500": "^spx",
         "usd_ils": "usdils", "ta35": "^ta35", "ta125": "^ta125", "dxy": "dx.f"}


def stooq(sym):
    t = get(f"https://stooq.com/q/d/l/?s={requests.utils.quote(sym)}&i=d").text
    rows = [r for r in csv.DictReader(io.StringIO(t)) if r.get("Close") not in (None, "", "N/D")]
    if len(rows) < 2:
        raise RuntimeError("no stooq data")
    v, p = float(rows[-1]["Close"]), float(rows[-2]["Close"])
    return {"v": v, "prev": p, "chg_pct": round((v - p) / p * 100, 2), "t": rows[-1]["Date"], "src": "stooq"}


@guard("markets")
def collect_markets():
    out = {}
    fails = 0
    for k, sym in YAHOO.items():
        try:
            out[k] = stooq(STOOQ[k])
            continue
        except Exception:
            pass
        try:
            j = get(f"https://query1.finance.yahoo.com/v8/finance/chart/{requests.utils.quote(sym)}?range=5d&interval=1d").json()
            m = j["chart"]["result"][0]["meta"]
            v, p = m.get("regularMarketPrice"), m.get("chartPreviousClose") or m.get("previousClose")
            out[k] = {"v": v, "prev": p, "chg_pct": round((v - p) / p * 100, 2) if v and p else None,
                      "t": iso(datetime.fromtimestamp(m.get("regularMarketTime", 0), timezone.utc))}
        except Exception as e:
            fails += 1
            out[k] = {"error": str(e)[:80]}
    if fails == len(YAHOO):
        raise RuntimeError("all market symbols failed")
    return out


@guard("iran_fx")
def collect_iran_fx():
    t = get("https://www.tgju.org/", timeout=30).text
    out = {}
    for key, row in (("usd_rial", "price_dollar_rl"), ("emami_coin_rial", "sekee"), ("gold18_rial", "geram18")):
        m = re.search(r'data-market-row="%s"[\s\S]{0,600}?<td[^>]*class="nf"[^>]*>([\d,]+)</td>' % row, t)
        if not m:
            m = re.search(r'data-market-nameslug="%s"[\s\S]{0,600}?([\d]{1,3}(?:,\d{3})+)' % row, t)
        if m:
            rial = int(m.group(1).replace(",", ""))
            out[key] = rial
            out[key.replace("_rial", "_toman")] = rial // 10
    if not out:
        raise RuntimeError("tgju values not found")
    return out


# ---------------------------------------------------------------- news (RSS)
FEEDS = {
    "Times of Israel": "https://www.timesofisrael.com/feed/",
    "Times of Israel liveblog": "https://www.timesofisrael.com/liveblog/feed/",
    "Jerusalem Post": "https://www.jpost.com/rss/rssfeedsheadlines.aspx",
    "Al Jazeera": "https://www.aljazeera.com/xml/rss/all.xml",
    "BBC Middle East": "https://feeds.bbci.co.uk/news/world/middle_east/rss.xml",
    "BBC Persian": "https://feeds.bbci.co.uk/persian/rss.xml",
    "Iran International": "https://www.iranintl.com/en/feed",
    "gCaptain": "https://gcaptain.com/feed/",
    "The War Zone": "https://www.twz.com/feed",
    "USNI News": "https://news.usni.org/feed",
    "Defense News": "https://www.defensenews.com/arc/outboundfeeds/rss/",
    "Gulf News": "https://gulfnews.com/feeds/rss/world/gulf",
    "Arab News": "https://www.arabnews.com/rss.xml",
    "Radio Farda": "https://www.radiofarda.com/api/zrqiteuuir",
    "Euronews Persian": "https://parsi.euronews.com/rss",
}
GNEWS_Q = [
    "Iran attack", "Iran strike US", "Israel Iran", "Strait of Hormuz", "UKMTO", "CENTCOM Iran",
    "embassy ordered departure Middle East", "Iran airspace NOTAM", "Home Front Command", "Houthi missile",
    "Iran Qatar talks", "IAEA Iran", "USNI fleet tracker", "Iran tanker attack", "Iran nuclear site",
]
STRONG = re.compile(
    r"\b(iran|iranian|tehran|irgc|hormuz|khamenei|araghchi|pezeshkian|natanz|fordow|isfahan|bushehr|kharg|"
    r"houthi|hezbollah|centcom|ukmto|jmic|idf|netanyahu|hegseth|pentagon|b-?52|b-?2|kc-?135|kc-?46|"
    r"notam|airspace|evacuat|ordered departure|embassy|iaea|tanker|warship|carrier|uss |missile|drone|"
    r"home front|pikud|shelter|brent|oil price|qatar|doha|ceasefire)\b|"
    r"ایران|تهران|سپاه|هرمز|حمله|موشک|پهپاد|پدافند|انفجار|تخلیه|سفارت|حریم هوایی|اسرائیل|آمریکا|"
    r"איראן|אזעקה|פיקוד העורף|טיל|שיגור|מקלט", re.I)
PRECURSORS = [
    ("embassy_evacuation", r"(ordered departure|evacuat\w* (?:the )?(?:us |american |israeli )?(?:embassy|embassies|diplomats)|embassy[^.]{0,40}evacuat|تخلیه سفارت)"),
    ("leave_now", r"(leave (?:the country )?(?:immediately|now|today)|depart immediately|همین (?:امروز|حالا) .{0,15}(?:خارج|ترک))"),
    ("airspace_closure", r"(airspace (?:is )?clos|closes? (?:its )?airspace|bans? (?:all )?flights|بسته شدن حریم|حریم هوایی .{0,20}بسته)"),
    ("home_front", r"(shelters? (?:open|reopen)|schools? (?:closed|shut)|home front command (?:issues|orders|changes)|reservists? call)"),
    ("iaea_resolution", r"(iaea (?:board )?(?:resolution|censure)|board of governors (?:votes|adopts|resolution))"),
    ("bombers_tankers", r"(b-?52s?|b-?2s?|b-?1s?) (?:deploy|arriv|land|flown|sent)|tankers? (?:surge|deploy|arriv)"),
    ("strike_reported", r"(explosions? (?:heard |reported )?(?:in|near|across) (?:tehran|isfahan|natanz|fordow|shiraz|tabriz|bandar abbas)|(?:launch(?:ed|es)|carr(?:ied|ies) out|beg[ia]n) (?:air ?)?strikes? (?:on|against) iran|(?:us|israel|israeli|american) (?:jets|aircraft|forces) (?:struck|hit|attacked) iran)"),
]


def norm_title(t):
    t = re.sub(r"<[^>]+>", " ", html.unescape(t or ""))
    t = re.sub(r"\s+", " ", t).strip()
    return t


def toks(t):
    return {w for w in re.findall(r"[\w؀-ۿ֐-׿]{4,}", t.lower())}


def parse_feed(xml_text):
    out = []
    root = ET.fromstring(xml_text.encode("utf-8") if isinstance(xml_text, str) else xml_text)
    ns = {"a": "http://www.w3.org/2005/Atom"}
    for it in root.iter("item"):
        title = norm_title(it.findtext("title"))
        link = (it.findtext("link") or "").strip()
        d = it.findtext("pubDate") or it.findtext("{http://purl.org/dc/elements/1.1/}date")
        src = it.findtext("source")
        out.append((title, link, d, src))
    for it in root.findall("a:entry", ns):
        title = norm_title(it.findtext("a:title", namespaces=ns))
        le = it.find("a:link", ns)
        link = le.get("href") if le is not None else ""
        d = it.findtext("a:updated", namespaces=ns) or it.findtext("a:published", namespaces=ns)
        out.append((title, link, d, None))
    return out


def to_dt(d):
    if not d:
        return None
    try:
        return parsedate_to_datetime(d).astimezone(timezone.utc)
    except Exception:
        try:
            return parse_iso(d)
        except Exception:
            return None


@guard("news")
def collect_news(state):
    items, ok, bad = [], [], []
    srcs = list(FEEDS.items()) + [(f"Google News: {q}", "https://news.google.com/rss/search?q=" +
                                    requests.utils.quote(q + " when:1d") + "&hl=en-US&gl=US&ceid=US:en") for q in GNEWS_Q]
    for name, url in srcs:
        try:
            entries = parse_feed(get(url).text)
            ok.append(name)
        except Exception:
            bad.append(name)
            continue
        for title, link, d, src in entries:
            dt = to_dt(d)
            if dt and dt < NOW - timedelta(hours=NEWS_WINDOW_H):
                continue
            if not title or not STRONG.search(title):
                continue
            outlet = src if (src and name.startswith("Google")) else name
            if name.startswith("Google") and " - " in title:
                title = title.rsplit(" - ", 1)[0]
            items.append({"title": title, "link": link, "outlet": outlet, "pub": iso(dt) if dt else None})
    if not ok:
        raise RuntimeError("all feeds failed")
    if bad:
        STATUS["news"] = f"partial: {len(bad)} feed(s) failed: " + ", ".join(bad[:6])
    # cluster into stories (token Jaccard) and merge with rolling state
    stories = state.setdefault("stories", [])
    for it in items:
        tk = toks(it["title"])
        best, bs = None, 0
        for s in stories:
            j = len(tk & set(s["tok"])) / max(1, len(tk | set(s["tok"])))
            if j > bs:
                best, bs = s, j
        if best and bs >= 0.45:
            if it["outlet"] not in best["outlets"]:
                best["outlets"].append(it["outlet"])
                best["links"].append(it["link"])
            best["last"] = iso(NOW)
        else:
            stories.append({"id": hashlib.md5(it["title"].encode()).hexdigest()[:10], "title": it["title"],
                            "tok": sorted(tk), "outlets": [it["outlet"]], "links": [it["link"]],
                            "pub": it["pub"], "first": iso(NOW), "last": iso(NOW)})
    cutoff = NOW - timedelta(hours=NEWS_WINDOW_H)
    state["stories"] = [s for s in stories if parse_iso(s["last"]) >= cutoff][-600:]
    return {"feeds_ok": len(ok), "feeds_failed": bad}


# ---------------------------------------------------------------- Telegram public previews
TG = ["idfofficial", "PikudHaoref_all", "presstv", "amitsegal", "clashreport", "AuroraIntel", "bbcpersian",
      "iranintltv", "farsna", "abualiexpress", "warmonitors", "shin_persian", "alibk3", "manniefabian",
      "VahidOnline", "ynetalerts", "akhbarefori", "mehrnews", "isna94", "N12chat", "lieldaphna", "irna_1313",
      "indypersian", "euronewspe", "manototv", "idf_telegram"]
EMOJI = set("⏳⌛⏰🚀💥🔥✈🛩🚁🎯☢🚨⚠🔴‼⚡💣🧨☄📡🛰🚢🛳⚓🔊👀⚔🪖🛑⛔")


@guard("telegram")
def collect_telegram(state):
    last = state.setdefault("tg_last", {})
    posts, ok, bad = [], 0, []
    for ch in TG:
        try:
            t = get(f"https://t.me/s/{ch}").text
            ok += 1
        except Exception:
            bad.append(ch)
            continue
        for blk in t.split('class="tgme_widget_message_wrap')[1:]:
            m = re.search(r'data-post="([^"/]+)/(\d+)"', blk)
            if not m:
                continue
            pid = int(m.group(2))
            if pid <= last.get(ch, 0):
                continue
            tm = re.search(r'<time datetime="([^"]+)"', blk)
            tx = re.search(r'tgme_widget_message_text[^>]*>([\s\S]*?)</div>', blk)
            text = norm_title(re.sub(r"<br\s*/?>", " ", tx.group(1))) if tx else ""
            dt = to_dt(tm.group(1)) if tm else None
            if dt and dt < NOW - timedelta(hours=NEWS_WINDOW_H):
                continue
            if not text:
                continue
            emo = sorted({c for c in text if c in EMOJI})
            posts.append({"ch": ch, "id": pid, "t": iso(dt) if dt else None, "text": text[:280],
                          "emoji": "".join(emo), "link": f"https://t.me/{ch}/{pid}", "relevant": bool(STRONG.search(text))})
        ids = [int(x) for x in re.findall(r'data-post="%s/(\d+)"' % re.escape(ch), t)]
        if ids:
            last[ch] = max(ids + [last.get(ch, 0)])
    if not ok:
        raise RuntimeError("all channels failed")
    if bad:
        STATUS["telegram"] = f"partial: {len(bad)} channel(s) failed"
    keep = state.setdefault("tg_posts", [])
    have = {p["link"] for p in keep}
    keep.extend(p for p in posts if p["link"] not in have)
    cutoff = NOW - timedelta(hours=NEWS_WINDOW_H)
    state["tg_posts"] = [p for p in keep if not p["t"] or parse_iso(p["t"]) >= cutoff][-500:]
    return {"channels_ok": ok, "channels_failed": bad}


# ---------------------------------------------------------------- Safe Airspace
COUNTRIES = ["Iran", "Iraq", "Israel", "Lebanon", "Syria", "Jordan", "Saudi Arabia", "Yemen", "Kuwait", "Bahrain",
             "Qatar", "United Arab Emirates", "Oman", "Egypt", "Turkey", "Pakistan", "Afghanistan", "Cyprus"]


@guard("safeairspace")
def collect_safeairspace(state):
    t = get("https://safeairspace.net/", timeout=30).text
    text = norm_title(re.sub(r"<(script|style)[\s\S]*?</\1>", " ", t))
    found = []
    for m in re.finditer(r"(\d{1,2} (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* 20\d\d)", text):
        ctx = text[max(0, m.start() - 160): m.end() + 200]
        cs = [c for c in COUNTRIES if c in ctx]
        if cs:
            found.append({"date": m.group(1), "countries": cs, "text": ctx.strip()[:360]})
    h = hashlib.md5(text.encode()).hexdigest()
    changed = state.get("sa_hash") not in (None, h)
    state["sa_hash"] = h
    if changed:
        state["sa_changed_at"] = iso(NOW)
    recent = []
    for f in found:
        try:
            d = datetime.strptime(f["date"].replace("Sept", "Sep"), "%d %b %Y")
        except ValueError:
            try:
                d = datetime.strptime(f["date"], "%d %B %Y")
            except ValueError:
                continue
        if d.replace(tzinfo=timezone.utc) >= NOW - timedelta(days=3):
            recent.append(f)
    return {"page_changed_since_last_check": changed, "last_change": state.get("sa_changed_at"),
            "entries_last_3d": recent[:25]}


# ---------------------------------------------------------------- Polymarket
@guard("polymarket")
def collect_polymarket():
    j = get("https://gamma-api.polymarket.com/markets?closed=false&active=true&limit=500&order=volume24hr&ascending=false").json()
    out = []
    for m in j:
        q = m.get("question") or ""
        if re.search(r"\b(iran|israel|hormuz|khamenei|tehran|houthi)\b", q, re.I):
            try:
                prices = json.loads(m.get("outcomePrices") or "[]")
                outs = json.loads(m.get("outcomes") or "[]")
            except Exception:
                prices, outs = [], []
            out.append({"q": q, "end": m.get("endDate"), "outcomes": dict(zip(outs, prices)),
                        "vol24h": round(float(m.get("volume24hr") or 0)), "slug": m.get("slug")})
    return out[:25]


# ---------------------------------------------------------------- main
def detect_precursors(state, adsb, markets):
    alerts = []
    texts = [(s["title"], s["outlets"], s["links"][0]) for s in state.get("stories", [])]
    texts += [(p["text"], [p["ch"]], p["link"]) for p in state.get("tg_posts", [])]
    for key, rx in PRECURSORS:
        hits = [(t, o, l) for t, o, l in texts if re.search(rx, t, re.I)]
        if hits:
            outlets = sorted({x for _, o, _ in hits for x in o})
            alerts.append({"type": key, "n_items": len(hits), "n_outlets": len(outlets), "outlets": outlets[:10],
                           "examples": [{"text": t[:200], "link": l} for t, _, l in hits[:4]],
                           "note": "keyword match — verify before acting"})
    if adsb:
        b = adsb["baseline"]
        for g in ("tanker", "bomber", "transport", "isr"):
            now, med, p90 = b[g]["now"], b[g]["median_14d"], b[g]["p90_14d"]
            if b[g]["samples"] >= 24 and now >= max(3, 2 * (med or 0)) and now > (p90 or 0):
                alerts.append({"type": f"adsb_{g}_above_baseline", "now": now, "median_14d": med, "p90_14d": p90})
            if g == "bomber" and now > 0:
                alerts.append({"type": "adsb_bomber_seen", "now": now})
    if markets and isinstance(markets.get("usd_ils"), dict) and isinstance(markets.get("ta35"), dict):
        ils, ta = markets["usd_ils"].get("chg_pct"), markets["ta35"].get("chg_pct")
        if ils is not None and ta is not None and ils >= 1 and ta <= -1.5:
            alerts.append({"type": "shekel_ta35_stress", "usd_ils_chg": ils, "ta35_chg": ta})
    return alerts


def main():
    os.makedirs(DATA, exist_ok=True)
    state = json.load(open(STATE_F, encoding="utf-8")) if os.path.exists(STATE_F) else {}
    adsb = collect_adsb(state)
    firms = collect_firms(state)
    markets = collect_markets()
    fx = collect_iran_fx()
    news_meta = collect_news(state)
    tg_meta = collect_telegram(state)
    sa = collect_safeairspace(state)
    pm = collect_polymarket()
    alerts = detect_precursors(state, adsb, markets)

    stories = sorted(state.get("stories", []), key=lambda s: (-len(s["outlets"]), s["first"]), reverse=False)
    digest = {
        "generated": iso(NOW),
        "window_hours": {"news": NEWS_WINDOW_H, "military_air": MIL_WINDOW_H},
        "sources_status": STATUS,
        "alerts": alerts,
        "adsb": adsb,
        "firms": firms,
        "markets": markets,
        "iran_fx": fx,
        "safeairspace": sa,
        "polymarket": pm,
        "news_meta": news_meta,
        "news": [{k: s[k] for k in ("title", "outlets", "links", "pub", "first", "last")} for s in stories],
        "telegram_meta": tg_meta,
        "telegram": sorted({p["link"]: p for p in state.get("tg_posts", [])
                            if p.get("relevant") or p.get("emoji") or p["ch"] == "PikudHaoref_all"}.values(),
                           key=lambda p: p.get("t") or "", reverse=True),
    }
    json.dump(state, open(STATE_F, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    json.dump(digest, open(DIGEST_F, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    day = NOW.strftime("%Y-%m-%d")
    os.makedirs(os.path.join(DATA, "archive"), exist_ok=True)
    with open(os.path.join(DATA, "archive", f"{day}.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps({"t": iso(NOW), "status": STATUS, "alerts": alerts,
                            "adsb_now": (adsb or {}).get("now"), "firms_n": (firms or {}).get("n_total"),
                            "markets": markets, "iran_fx": fx}, ensure_ascii=False) + "\n")
    print(json.dumps({"status": STATUS, "alerts": len(alerts), "stories": len(digest["news"]),
                      "telegram": len(digest["telegram"])}, ensure_ascii=False))


if __name__ == "__main__":
    sys.exit(main())
