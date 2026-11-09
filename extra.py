"""Extra sources: NOTAMs, foreign travel advisories for Iran/region, more military-air points,
military AIS at chokepoints, and civil-traffic drop detection (airspace-closure sensor)."""
import asyncio, json, os, re, statistics
from datetime import datetime, timedelta, timezone

import requests

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"}


def _iso(dt):
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ------------------------------------------------------------ NOTAMs (FIRs of the region)
FIRS = {"OIIX": "Tehran", "ORBB": "Baghdad", "LLLL": "Tel Aviv", "OJAC": "Amman", "OSTT": "Damascus",
        "OLBB": "Beirut", "OEJD": "Jeddah", "OKAC": "Kuwait", "OBBB": "Bahrain", "OTDF": "Doha",
        "OMAE": "Emirates", "OOMM": "Muscat", "OYSC": "Sanaa", "LCCC": "Nicosia", "OPKR": "Karachi",
        "OPLR": "Lahore", "OAKX": "Kabul", "LTAA": "Ankara", "HECC": "Cairo"}
NOTAM_KEY = re.compile(r"CLSD|CLOSED|PROHIBITED|PROHIBIT|DANGER AREA|RESTRICTED AREA|MISSILE|ROCKET|FIRING|"
                       r"UNMANNED|UAS|GNSS|GPS|JAMMING|SPOOF|MIL(?:ITARY)? (?:ACT|EXER)|AIR DEFEN[CS]E|"
                       r"NOT AVBL|NO FLIGHTS|EXCEPT STATE|HUMANITARIAN|EVACUATION|DRONE", re.I)


def _notam_public(fir):
    r = requests.post("https://notams.aim.faa.gov/notamSearch/search", headers=UA, timeout=40,
                      data={"searchType": 0, "designatorsForLocation": fir, "notamsOnly": "false",
                            "offset": 0, "notamsPerPage": 200})
    r.raise_for_status()
    out = []
    for n in (r.json().get("notamList") or []):
        out.append({"id": n.get("notamNumber"), "text": n.get("icaoMessage") or n.get("traditionalMessage") or "",
                    "start": n.get("startDate"), "end": n.get("endDate"), "issued": n.get("issueDate")})
    return out


def _notam_api(fir):
    cid, sec = os.environ.get("FAA_CLIENT_ID"), os.environ.get("FAA_CLIENT_SECRET")
    if not (cid and sec):
        raise RuntimeError("no FAA key")
    r = requests.get("https://external-api.faa.gov/notamapi/v1/notams", timeout=40,
                     headers={"client_id": cid, "client_secret": sec},
                     params={"icaoLocation": fir, "pageSize": 1000})
    r.raise_for_status()
    out = []
    for it in r.json().get("items", []):
        p = it.get("properties", {}).get("coreNOTAMData", {}).get("notam", {})
        out.append({"id": p.get("number") or p.get("id"), "text": p.get("text") or "",
                    "start": p.get("effectiveStart"), "end": p.get("effectiveEnd"), "issued": p.get("issued")})
    return out


def notams(state, now):
    seen = set(state.setdefault("seen_notam", []))
    res, ok, method = {}, 0, None
    for fir, name in FIRS.items():
        items = None
        for fn, m in ((_notam_public, "faa-search"), (_notam_api, "faa-api")):
            try:
                items, method = fn(fir), m
                break
            except Exception:
                continue
        if items is None:
            continue
        ok += 1
        rel = []
        for n in items:
            txt = re.sub(r"\s+", " ", n["text"])
            if not NOTAM_KEY.search(txt):
                continue
            key = f"{fir}:{n['id']}"
            rel.append({**n, "text": txt[:400], "new": key not in seen})
            seen.add(key)
        res[fir] = {"fir": name, "total": len(items), "relevant": len(rel),
                    "new_relevant": [r for r in rel if r["new"]][:15]}
    if not ok:
        raise RuntimeError("no NOTAM source reachable")
    state["seen_notam"] = list(seen)[-6000:]
    return {"method": method, "firs_ok": ok, "by_fir": res}


# ------------------------------------------------------------ foreign travel advisories
DE = {"Iran": "Iran", "Israel": "Israel", "Irak": "Iraq", "Libanon": "Lebanon", "Jordanien": "Jordan",
      "Katar": "Qatar", "Bahrain": "Bahrain", "Kuwait": "Kuwait", "Vereinigte Arabische Emirate": "UAE",
      "Oman": "Oman", "Saudi-Arabien": "Saudi Arabia", "Jemen": "Yemen", "Syrien": "Syria", "Zypern": "Cyprus"}
CA = {"IR": "Iran", "IL": "Israel", "IQ": "Iraq", "LB": "Lebanon", "JO": "Jordan", "QA": "Qatar", "BH": "Bahrain",
      "KW": "Kuwait", "AE": "UAE", "OM": "Oman", "SA": "Saudi Arabia", "YE": "Yemen", "SY": "Syria", "CY": "Cyprus"}


def advisories(state, now):
    out, status = [], {}
    prev = state.setdefault("adv_prev", {})
    try:
        j = requests.get("https://www.auswaertiges-amt.de/opendata/travelwarning", headers=UA, timeout=30).json()
        for k, v in (j.get("response") or {}).items():
            if not isinstance(v, dict):
                continue
            c = DE.get(v.get("countryName"))
            if not c:
                continue
            lvl = "warning" if v.get("warning") else "partial" if v.get("partialWarning") else "situation" if v.get("situationWarning") else "none"
            mod = v.get("lastModified")
            mod_iso = _iso(datetime.fromtimestamp(mod, timezone.utc)) if isinstance(mod, (int, float)) else mod
            out.append({"src": "Germany", "country": c, "level": lvl, "modified": mod_iso})
        status["Germany"] = "ok"
    except Exception as e:
        status["Germany"] = f"error: {str(e)[:60]}"
    try:
        j = requests.get("https://data.international.gc.ca/travel-voyage/index-updated.json", headers=UA, timeout=30).json()
        data = j.get("data") or {}
        for cc, c in CA.items():
            v = data.get(cc) or {}
            eng = v.get("eng") or {}
            out.append({"src": "Canada", "country": c, "level": v.get("advisory-state"),
                        "text": (eng.get("advisory-text") or "")[:160], "modified": v.get("date-published", {}).get("date") if isinstance(v.get("date-published"), dict) else v.get("date-published")})
        status["Canada"] = "ok"
    except Exception as e:
        status["Canada"] = f"error: {str(e)[:60]}"
    pages = {"France Iran": "https://www.diplomatie.gouv.fr/fr/conseils-aux-voyageurs/conseils-par-pays-destination/iran/",
             "France Israel": "https://www.diplomatie.gouv.fr/fr/conseils-aux-voyageurs/conseils-par-pays-destination/israel-territoires-palestiniens/",
             "Australia Iran": "https://www.smartraveller.gov.au/destinations/middle-east/iran",
             "Australia Israel": "https://www.smartraveller.gov.au/destinations/middle-east/israel-and-palestinian-territories",
             "Switzerland Iran": "https://www.eda.admin.ch/eda/en/fdfa/representations-and-travel-advice/iran/travel-advice-iran.html",
             "Netherlands Iran": "https://www.nederlandwereldwijd.nl/reisadvies/iran",
             "Italy Iran": "https://www.viaggiaresicuri.it/find-country/country/IRN"}
    import hashlib
    for name, url in pages.items():
        try:
            t = requests.get(url, headers=UA, timeout=30).text
            txt = re.sub(r"\s+", " ", re.sub(r"<(script|style)[\s\S]*?</\1>|<[^>]+>", " ", t))
            m = re.search(r"(Derni[eè]re minute[^.]{0,300}|Latest update[^.]{0,300}|Do not travel[^.]{0,200}|"
                          r"Reconsider your need to travel[^.]{0,200}|quitter (?:le pays|l'Iran)[^.]{0,200}|"
                          r"leave (?:Iran|the country)[^.]{0,200}|Bijgewerkt[^.]{0,200})", txt, re.I)
            core = m.group(1) if m else txt[:2000]
            h = hashlib.md5(core.encode()).hexdigest()
            changed = prev.get(name) not in (None, h)
            prev[name] = h
            out.append({"src": name, "changed_since_last_check": changed, "snippet": core[:300], "url": url})
            status[name] = "ok"
        except Exception as e:
            status[name] = f"error: {str(e)[:60]}"
    # change detection for structured ones
    for o in out:
        if "level" in o:
            k = f"{o['src']}:{o['country']}"
            sig = f"{o.get('level')}|{o.get('modified')}"
            o["changed_since_last_check"] = prev.get(k) not in (None, sig)
            prev[k] = sig
    if not any(v == "ok" for v in status.values()):
        raise RuntimeError("no advisory source reachable")
    return {"status": status, "items": out}


# ------------------------------------------------------------ more military air + second source
EXTRA_POINTS = [("Al Udeid", 25.12, 51.32), ("Prince Sultan AB", 24.06, 47.58), ("Muwaffaq Salti", 31.83, 36.78),
                ("Diego Garcia", -7.31, 72.41), ("Akrotiri", 34.59, 32.99), ("Souda", 35.53, 24.15),
                ("Moron", 37.17, -5.62), ("Lajes", 38.76, -27.09), ("Mildenhall", 52.36, 0.49),
                ("Red Sea", 20.0, 38.6), ("Arabian Sea", 18.0, 61.0)]
# Iran periphery: community ADS-B has almost no receivers inside Iran, so aircraft flying into/out of
# Iran are only visible near its borders. These points watch the entry corridors of an airbridge to Tehran.
IRAN_RIM_POINTS = [("Caspian/Baku", 40.4, 49.9), ("Ashgabat", 37.9, 58.4), ("Yerevan/Nakhchivan", 39.9, 45.0),
                   ("Van/Tabriz rim", 38.5, 44.3), ("Iraq-Iran border", 33.4, 45.6), ("Basra/Khuzestan rim", 30.5, 47.8),
                   ("UAE/Bandar Abbas rim", 25.4, 55.8), ("Muscat/Oman", 23.6, 58.3), ("Herat/Mashhad rim", 34.4, 61.0)]
REGION_BOX = (10.0, 45.0, 25.0, 65.0)  # lat_min, lat_max, lon_min, lon_max  (Levant-Gulf-Iran-Caucasus)

# --- state / VIP / airbridge classification (beyond the dbFlags "military" bit)
HEX_RANGES = {"IR": (0x730000, 0x737FFF), "RU": (0x100000, 0x1FFFFF), "CN": (0x780000, 0x7BFFFF),
              "BY": (0x510000, 0x5103FF), "SY": (0x778000, 0x77FFFF), "KP": (0x720000, 0x727FFF)}
GOV_CS = ("GAF", "SUI", "CTM", "RRR", "SAM", "SPAR", "VENUS", "EXEC", "IAM", "NAF", "BAF", "PLF", "HUAF", "CEF",
          "ORF", "QAF", "BAH", "KAF", "RSF", "RJZ", "JYR", "UAF", "PAF", "TUAF", "TRKAF", "SSG", "AME", "SVF",
          "RFF", "RSD", "IRI", "IRIAF", "SHAHED", "IAF", "EGY", "LYAF", "ASY", "CFC", "AUS", "KIWI", "NOW", "DAF", "HAF")
GOV_REG = ("A4O-", "A7-H", "A7-M", "HZ-HM", "HZ-MF", "HZ-SK", "A6-PF", "A6-AL", "A6-HR", "A6-DLM", "A9C-", "9K-AK",
           "9K-GA", "JY-RY", "JY-ONE", "TC-ANK", "TC-CBK", "TC-TRK", "EP-IGA", "EP-AJA", "EP-PAK", "RA-96", "RA-64",
           "RA-86", "RF-", "YK-A", "YI-AS", "SU-GG", "4K-AI", "EK-RA", "EZ-A0")
BRIDGE_CS = ("QFZ", "PYA", "IRZ", "FPI", "IRA", "IRM", "IRC", "RDS", "IRU", "SHI", "VDA", "AZS", "RSD", "RFF",
             "MSI", "KGT", "CKK", "CAO", "SYR", "MHS", "TBZ")
BRIDGE_TYPES = {"IL76", "IL78", "IL62", "IL96", "A124", "A225", "AN12", "AN22", "AN26", "AN30", "AN32", "AN72", "AN74",
                "Y20", "Y8", "Y9", "T204", "T214", "TU54", "TU95", "TU16", "TU22", "TU60", "B742", "B744", "B748"}
INTERESTING_TYPES = {"C17", "C5M", "C130", "C30J", "A400", "KC39", "C2", "K35R", "KC46", "A332", "MRTT", "E3TF",
                     "E3CF", "E7", "R135", "RC135", "P8", "RQ4", "Q4", "MQ9", "B52", "B1", "B2", "F35", "F22", "F15", "F16"}


def hex_country(hx):
    try:
        v = int(hx, 16)
    except Exception:
        return None
    for c, (a, b) in HEX_RANGES.items():
        if a <= v <= b:
            return c
    return None


def in_region(a):
    la, lo = a.get("lat"), a.get("lon")
    if la is None or lo is None:
        return False
    return REGION_BOX[0] <= la <= REGION_BOX[1] and REGION_BOX[2] <= lo <= REGION_BOX[3]


def classify_extra(a):
    """Return (group, why) for state/VIP/airbridge aircraft that are not flagged military, else (None, None)."""
    cs = (a.get("flight") or "").strip().upper()
    reg = (a.get("r") or "").upper()
    t = (a.get("t") or "").upper()
    hc = hex_country(a.get("hex") or "")
    flags = a.get("dbFlags") or 0
    if hc == "IR" or reg.startswith("EP-"):
        return "bridge_ir", "Iranian-registered"
    if t in BRIDGE_TYPES and (in_region(a) or hc in ("RU", "CN", "BY", "SY", "KP")):
        return "bridge_ir", f"heavy cargo/state type {t}" + (f" ({hc})" if hc else "")
    if any(cs.startswith(p) for p in BRIDGE_CS) and in_region(a):
        return "bridge_ir", "sanctioned/IR-RU-CN cargo or state callsign"
    if hc in ("RU", "CN", "BY", "SY", "KP") and in_region(a):
        return "bridge_ir", f"{hc}-registered in region"
    if any(reg.startswith(p) for p in GOV_REG) or any(cs.startswith(p) for p in GOV_CS):
        return "gov", "government/VIP"
    if flags & 2:
        return "gov", "flagged interesting (state/VIP)"
    return None, None


def is_us_mil_hex(hx):
    try:
        return 0xAE0000 <= int(hx, 16) <= 0xAFFFFF
    except Exception:
        return False


SOURCES = ("https://api.adsb.lol", "https://api.airplanes.live")


def _get_ac(path, retries=2):
    """GET an ADS-B v2 path from adsb.lol, falling back to airplanes.live; backs off on 429/5xx.
    Both APIs rate-limit (~1 req/s); the old sequential loop got throttled after ~10 points, which is
    why every EXTRA point (Al Udeid, Prince Sultan, Diego Garcia...) failed in every run."""
    import time
    last = None
    for base in SOURCES:
        for i in range(retries):
            try:
                r = requests.get(base + path, headers=UA, timeout=15)
                if r.status_code in (429, 500, 502, 503, 504):
                    last = f"{base.split('/')[2]} {r.status_code}"
                    time.sleep(2.5 * (i + 1))
                    continue
                r.raise_for_status()
                return r.json().get("ac") or [], base.split("/")[2]
            except Exception as e:
                last = f"{base.split('/')[2]} {type(e).__name__}"
                time.sleep(1.5 * (i + 1))
    raise RuntimeError(f"ADS-B sources failed: {last}")


def fetch_point(lat, lon, radius=250):
    return _get_ac(f"/v2/point/{lat}/{lon}/{radius}")


def fetch_global(kind):
    """kind: 'mil' or 'type/IL76' etc. Global endpoints, filtered to the region by the caller."""
    return _get_ac(f"/v2/{kind}")


# ------------------------------------------------------------ military AIS at chokepoints (needs AISSTREAM_KEY)
BOXES = {"Hormuz": [[25.0, 54.5], [27.5, 58.5]], "Bab el-Mandeb": [[11.5, 42.0], [14.5, 45.0]],
         "Suez": [[29.5, 32.0], [31.5, 33.0]], "Gibraltar": [[35.6, -6.5], [36.3, -5.0]],
         "Gulf of Oman": [[22.5, 57.0], [25.5, 61.5]], "Eastern Med": [[32.0, 30.0], [36.0, 35.5]]}
NAVY_NAME = re.compile(r"^(USNS|USS|HMS|RFA|FS |FGS|ITS|HNLMS|HDMS|INS|IRIS|ROKS|JS |SPS|HMAS|HMCS|TCG|NATO)", re.I)


def ais_military(state, now, seconds=150):
    key = os.environ.get("AISSTREAM_KEY")
    if not key:
        raise RuntimeError("AISSTREAM_KEY secret missing (optional)")
    import websockets

    async def run():
        found, static = {}, {}
        sub = {"APIKey": key, "BoundingBoxes": list(BOXES.values()),
               "FilterMessageTypes": ["ShipStaticData", "PositionReport"]}
        async with websockets.connect("wss://stream.aisstream.io/v0/stream", open_timeout=20) as ws:
            await ws.send(json.dumps(sub))
            end = asyncio.get_event_loop().time() + seconds
            while asyncio.get_event_loop().time() < end:
                try:
                    msg = json.loads(await asyncio.wait_for(ws.recv(), timeout=end - asyncio.get_event_loop().time()))
                except asyncio.TimeoutError:
                    break
                md = msg.get("MetaData", {})
                mmsi, name = md.get("MMSI"), (md.get("ShipName") or "").strip()
                if msg.get("MessageType") == "ShipStaticData":
                    st = msg["Message"]["ShipStaticData"]
                    static[mmsi] = {"type": st.get("Type"), "dest": (st.get("Destination") or "").strip(), "name": name}
                s = static.get(mmsi, {})
                if s.get("type") == 35 or NAVY_NAME.match(name):
                    box = next((b for b, ((la1, lo1), (la2, lo2)) in BOXES.items()
                                if la1 <= md.get("latitude", 999) <= la2 and lo1 <= md.get("longitude", 999) <= lo2), None)
                    found[mmsi] = {"mmsi": mmsi, "name": name, "ais_type": s.get("type"), "dest": s.get("dest"),
                                   "lat": md.get("latitude"), "lon": md.get("longitude"), "area": box, "t": md.get("time_utc")}
        return list(found.values())

    ships = asyncio.run(run())
    log = state.setdefault("ais_seen", {})
    for s in ships:
        prev = log.get(str(s["mmsi"]))
        s["first"] = prev["first"] if prev else _iso(now)
        s["last"] = _iso(now)
        log[str(s["mmsi"])] = s
    cutoff = now - timedelta(hours=48)
    state["ais_seen"] = {k: v for k, v in log.items() if datetime.fromisoformat(v["last"].replace("Z", "+00:00")) > cutoff}
    return {"listened_seconds": seconds, "now": ships, "seen_48h": list(state["ais_seen"].values())}


# ------------------------------------------------------------ civil traffic drop (airspace closure sensor)
def traffic_drop(state, now, points):
    """Compare each area's total aircraft with the 14-day median for the same UTC hour."""
    hist = state.setdefault("traffic_hist", [])
    hour = now.hour
    row = {"t": _iso(now), "h": hour, **{p["area"]: p["total"] for p in points if p.get("total") is not None}}
    out = []
    for p in points:
        if p.get("total") is None:
            continue
        same = [r[p["area"]] for r in hist if r.get("h") == hour and p["area"] in r]
        if len(same) >= 4:
            med = statistics.median(same)
            drop = round((med - p["total"]) / med * 100, 1) if med else None
            out.append({"area": p["area"], "now": p["total"], "median_same_hour": med, "drop_pct": drop})
    hist.append(row)
    state["traffic_hist"] = [r for r in hist if datetime.fromisoformat(r["t"].replace("Z", "+00:00")) > now - timedelta(days=14)]
    return out
