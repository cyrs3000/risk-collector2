"""Official / sensor sources for the risk collector. Every function is best-effort:
it returns data or raises; collect.py wraps each call and records the status."""
import csv, hashlib, io, json, re, statistics
from datetime import datetime, timedelta, timezone
import xml.etree.ElementTree as ET

import requests

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"}
REGION = ["Iran", "Israel", "Iraq", "Lebanon", "Syria", "Jordan", "Saudi Arabia", "Yemen", "Kuwait", "Bahrain",
          "Qatar", "United Arab Emirates", "Oman", "Egypt", "Turkey", "Cyprus", "Pakistan", "Afghanistan"]


def _get(url, timeout=30, **kw):
    r = requests.get(url, headers=UA, timeout=timeout, **kw)
    r.raise_for_status()
    return r


def _iso(dt):
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _rss(url):
    root = ET.fromstring(_get(url).content)
    out = []
    for it in root.iter("item"):
        out.append({"title": re.sub(r"\s+", " ", (it.findtext("title") or "")).strip(),
                    "link": (it.findtext("link") or "").strip(),
                    "date": it.findtext("pubDate") or it.findtext("{http://purl.org/dc/elements/1.1/}date"),
                    "desc": re.sub(r"<[^>]+>|\s+", " ", it.findtext("description") or "").strip()[:300]})
    return out


def _changes(state, key, items, idf):
    """Mark items not seen before (by id) and remember seen ids."""
    seen = set(state.setdefault("seen_" + key, []))
    for it in items:
        it["new"] = idf(it) not in seen
    state["seen_" + key] = list((seen | {idf(i) for i in items}))[-800:]
    return items


# ---- 1. US State Department travel advisories (official RSS)
def state_dept(state, now):
    items = [i for i in _rss("https://travel.state.gov/_res/rss/TAsTWs.xml")
             if any(c.lower() in i["title"].lower() for c in REGION)]
    for i in items:
        m = re.search(r"Level (\d)", i["title"])
        i["level"] = int(m.group(1)) if m else None
        i["ordered_departure"] = bool(re.search(r"ordered departure", i["title"] + " " + i["desc"], re.I))
    return _changes(state, "statedept", items, lambda i: i["title"] + "|" + (i["date"] or ""))


# ---- 2. US embassy security alerts (official WordPress feeds)
EMBASSIES = {"Israel": "il", "Iraq": "iq", "Jordan": "jo", "Lebanon": "lb", "Qatar": "qa", "Bahrain": "bh",
             "Kuwait": "kw", "UAE": "ae", "Saudi Arabia": "sa", "Oman": "om", "Turkey": "tr", "Cyprus": "cy",
             "Egypt": "eg", "Azerbaijan": "az", "Pakistan": "pk"}


def embassy_alerts(state, now):
    out, ok = [], 0
    for country, cc in EMBASSIES.items():
        try:
            items = _rss(f"https://{cc}.usembassy.gov/category/alert/feed/")
            ok += 1
        except Exception:
            continue
        for i in items[:5]:
            i["country"] = country
            i["ordered_departure"] = bool(re.search(r"ordered departure|authorized departure|depart immediately|leave (?:the country|now|immediately)", i["title"] + " " + i["desc"], re.I))
            out.append(i)
    if not ok:
        raise RuntimeError("no embassy feed reachable")
    return {"feeds_ok": ok, "items": _changes(state, "embassy", out, lambda i: i["link"])}


# ---- 3. UK FCDO travel advice (official gov.uk content API)
FCDO = {"Iran": "iran", "Israel": "israel", "Iraq": "iraq", "Lebanon": "lebanon", "Jordan": "jordan",
        "Saudi Arabia": "saudi-arabia", "Qatar": "qatar", "Bahrain": "bahrain", "Kuwait": "kuwait",
        "UAE": "united-arab-emirates", "Oman": "oman", "Yemen": "yemen", "Syria": "syria", "Cyprus": "cyprus",
        "Turkey": "turkey", "Egypt": "egypt"}


def fcdo(state, now):
    out = []
    for country, slug in FCDO.items():
        try:
            j = _get(f"https://www.gov.uk/api/content/foreign-travel-advice/{slug}").json()
        except Exception:
            continue
        d = j.get("details") or {}
        upd = j.get("public_updated_at")
        alert = " ".join(d.get("alert_status") or [])
        out.append({"country": country, "updated": upd, "change": (d.get("change_description") or "")[:300],
                    "alert_status": alert, "link": f"https://www.gov.uk/foreign-travel-advice/{slug}",
                    "updated_last_24h": bool(upd and datetime.fromisoformat(upd.replace("Z", "+00:00")) > now - timedelta(hours=24))})
    if not out:
        raise RuntimeError("FCDO unreachable")
    return out


# ---- 4. Aviation: EASA CZIB + FAA restrictions (page watch)
def page_watch(state, key, url, pattern, limit=20):
    t = _get(url).text
    txt = re.sub(r"<(script|style)[\s\S]*?</\1>|<[^>]+>", " ", t)
    txt = re.sub(r"\s+", " ", txt)
    hits = []
    for m in re.finditer(pattern, txt, re.I):
        hits.append(txt[max(0, m.start() - 120): m.end() + 180].strip())
    h = hashlib.md5("".join(hits).encode()).hexdigest()
    changed = state.get("hash_" + key) not in (None, h)
    state["hash_" + key] = h
    if changed:
        state["changed_" + key] = _iso(datetime.now(timezone.utc))
    return {"changed_since_last_check": changed, "last_change": state.get("changed_" + key),
            "snippets": list(dict.fromkeys(hits))[:limit], "url": url}


def easa(state, now):
    return page_watch(state, "easa", "https://www.easa.europa.eu/en/domains/air-operations/czibs",
                      r"CZIB[- ]?\d{4}-\d+[^.]{0,80}(Iran|Iraq|Israel|Lebanon|Syria|Jordan|Gulf|Saudi|Yemen|Middle East|Persian)")


def faa(state, now):
    return page_watch(state, "faa", "https://www.faa.gov/air_traffic/publications/us_restrictions",
                      r"(Iran|Iraq|Israel|Lebanon|Syria|Jordan|Persian Gulf|Gulf of Oman|Saudi|Yemen|Kuwait|Qatar|Bahrain|UAE|Oman)[^.]{0,120}(SFAR|NOTAM|KICZ|prohibit|caution)", limit=15)


# ---- 5. Maritime: IMF PortWatch (Hormuz transits) + MARAD advisories
def portwatch(state, now):
    url = ("https://services9.arcgis.com/weJ1QsnbMYJlCHdG/arcgis/rest/services/Daily_Chokepoints_Data/FeatureServer/0/query"
           "?where=portname%3D%27Strait%20of%20Hormuz%27&outFields=date,n_total,n_tanker,n_cargo,capacity"
           "&orderByFields=date%20DESC&resultRecordCount=30&f=json")
    feats = _get(url).json().get("features") or []
    rows = []
    for f in feats:
        a = f["attributes"]
        d = a.get("date")
        if isinstance(d, (int, float)):
            d = datetime.fromtimestamp(d / 1000, timezone.utc).strftime("%Y-%m-%d")
        rows.append({"date": d, "total": a.get("n_total"), "tanker": a.get("n_tanker"), "cargo": a.get("n_cargo")})
    if not rows:
        raise RuntimeError("no PortWatch rows")
    vals = [r["total"] for r in rows[1:] if r["total"] is not None]
    return {"latest": rows[0], "median_prev_29d": statistics.median(vals) if vals else None, "last_7d": rows[:7]}


def marad(state, now):
    return page_watch(state, "marad", "https://www.maritime.dot.gov/msci-advisories",
                      r"20\d\d-\d{3}[^.]{0,40}(Persian Gulf|Strait of Hormuz|Gulf of Oman|Red Sea|Arabian Sea|Iran|Bab|Gulf of Aden)[^.]{0,200}")


# ---- 6. Official statements: CENTCOM, DoD, IAEA, OFAC, UN
def statements(state, now):
    feeds = {
        "CENTCOM": "https://www.centcom.mil/DesktopModules/ArticleCS/RSS.ashx?ContentType=1&Site=808&max=15",
        "DoD releases": "https://www.defense.gov/DesktopModules/ArticleCS/RSS.ashx?ContentType=9&Site=945&max=15",
        "DoD news": "https://www.defense.gov/DesktopModules/ArticleCS/RSS.ashx?ContentType=1&Site=945&max=15",
        "IAEA": "https://www.iaea.org/feeds/topnews",
        "UN News ME": "https://news.un.org/feed/subscribe/en/news/region/middle-east/feed/rss.xml",
        "US Treasury": "https://home.treasury.gov/system/files/126/ofac.xml",
        "White House": "https://www.whitehouse.gov/news/feed/",
    }
    out, status = [], {}
    rx = re.compile(r"iran|tehran|irgc|hormuz|houthi|israel|gulf|centcom|nuclear|safeguards|sanction|middle east|red sea|yemen|iraq|syria|lebanon", re.I)
    for name, url in feeds.items():
        try:
            items = _rss(url)
            status[name] = "ok"
        except Exception as e:
            status[name] = f"error: {str(e)[:60]}"
            continue
        for i in items[:15]:
            if rx.search(i["title"] + " " + i["desc"]):
                i["source"] = name
                out.append(i)
    if not any(v == "ok" for v in status.values()):
        raise RuntimeError("no official feed reachable")
    return {"status": status, "items": _changes(state, "official", out, lambda i: i["link"] or i["title"])}


def ofac_page(state, now):
    return page_watch(state, "ofac", "https://ofac.treasury.gov/recent-actions",
                      r"(\d{2}/\d{2}/20\d\d)[^|]{0,30}[^.]{0,160}(Iran|Counter Terrorism|Houthi|IRGC|Hizballah)", limit=10)


# ---- 7. Sensors: USGS seismic + IODA internet
SITES = {"Natanz": (33.72, 51.73), "Fordow": (34.88, 51.0), "Isfahan": (32.6, 51.68), "Parchin": (35.52, 51.77),
         "Tehran": (35.69, 51.39), "Bushehr": (28.83, 50.89), "Arak": (34.37, 49.24), "Bandar Abbas": (27.18, 56.27),
         "Shiraz": (29.6, 52.5), "Tabriz": (38.08, 46.29), "Kermanshah": (34.35, 47.1)}


def usgs(state, now, km):
    st = (now - timedelta(hours=48)).strftime("%Y-%m-%dT%H:%M:%S")
    j = _get("https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=" + st +
             "&minlatitude=24&maxlatitude=40&minlongitude=44&maxlongitude=64&minmagnitude=2.5").json()
    out = []
    for f in j.get("features", []):
        lon, lat, depth = f["geometry"]["coordinates"]
        p = f["properties"]
        near = [(n, round(km((lat, lon), s))) for n, s in SITES.items() if km((lat, lon), s) <= 60]
        out.append({"t": _iso(datetime.fromtimestamp(p["time"] / 1000, timezone.utc)), "mag": p.get("mag"),
                    "depth_km": depth, "place": p.get("place"), "type": p.get("type"), "lat": lat, "lon": lon,
                    "near_sites": near, "shallow_near_site": bool(near and depth is not None and depth <= 5),
                    "url": p.get("url")})
    return sorted(out, key=lambda e: e["t"], reverse=True)


def ioda(state, now):
    frm, until = int((now - timedelta(hours=48)).timestamp()), int(now.timestamp())
    ev = _get(f"https://api.ioda.inetintel.cc.gatech.edu/v2/outages/events?entityType=country&entityCode=IR&from={frm}&until={until}&limit=20").json()
    events = ev.get("data") or []
    out = {"events_48h": [{"start": _iso(datetime.fromtimestamp(e.get("start", 0), timezone.utc)),
                           "duration_min": round((e.get("duration") or 0) / 60), "datasource": e.get("datasource"),
                           "score": e.get("score")} for e in events][:10]}
    try:
        sig = _get(f"https://api.ioda.inetintel.cc.gatech.edu/v2/signals/raw/country/IR?from={frm}&until={until}&datasource=bgp").json()
        series = (sig.get("data") or [[]])[0]
        vals = series[0].get("values") if series else []
        vals = [v for v in vals if v is not None]
        if vals:
            med = statistics.median(vals)
            out["bgp_latest"], out["bgp_median_48h"] = vals[-1], med
            out["bgp_drop_pct"] = round((med - vals[-1]) / med * 100, 1) if med else None
    except Exception as e:
        out["bgp_error"] = str(e)[:80]
    return out


# ---- 8. Media volume spike detection (GDELT, statistical, multi-language global coverage)
def gdelt(state, now):
    q = requests.utils.quote('(Iran OR Tehran OR IRGC OR Hormuz) (attack OR strike OR missile OR explosion OR evacuation)')
    j = _get(f"https://api.gdeltproject.org/api/v2/doc/doc?query={q}&mode=timelinevolraw&timespan=7d&format=json", timeout=40).json()
    pts = (j.get("timeline") or [{}])[0].get("data") or []
    vals = [p.get("value", 0) for p in pts]
    if len(vals) < 12:
        raise RuntimeError("short GDELT series")
    last = sum(vals[-4:])
    windows = [sum(vals[i:i + 4]) for i in range(0, len(vals) - 8, 4)]
    med = statistics.median(windows) if windows else None
    return {"last_window_articles": last, "median_window_7d": med,
            "ratio": round(last / med, 2) if med else None, "bins": len(vals)}
