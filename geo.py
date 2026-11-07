"""Auto-locate kinetic reports (explosions, air defence, missiles, drones, UXO...) in Telegram posts and news titles.

Output is UNVERIFIED: a keyword + place-name match, not a confirmed event. The dashboard runs
must check date/source and record these as conf "u" (or "r"/"v" only with confirmation).
"""
import re
from datetime import timedelta

# name variants (fa / en / ar / he) -> (canonical Persian name, lat, lon)
PLACES = [
    (["تهران", "Tehran", "طهران", "טהרן"], "تهران", 35.69, 51.39),
    (["اصفهان", "Isfahan", "Esfahan", "أصفهان", "איספהאן"], "اصفهان", 32.65, 51.67),
    (["نطنز", "Natanz", "נתנז"], "نطنز", 33.72, 51.73),
    (["فردو", "Fordow", "Fordo", "פורדו"], "فردو", 34.88, 51.0),
    (["پارچین", "Parchin"], "پارچین", 35.52, 51.77),
    (["قم", "Qom"], "قم", 34.64, 50.88),
    (["کرج", "Karaj"], "کرج", 35.83, 50.97),
    (["شاهرود", "Shahroud", "Shahrud"], "شاهرود", 36.42, 54.98),
    (["سمنان", "Semnan"], "سمنان", 35.58, 53.39),
    (["تبریز", "Tabriz"], "تبریز", 38.08, 46.29),
    (["کرمانشاه", "Kermanshah"], "کرمانشاه", 34.31, 47.07),
    (["همدان", "Hamadan"], "همدان", 34.8, 48.52),
    (["اراک", "Arak"], "اراک", 34.09, 49.69),
    (["خنداب", "Khondab"], "خنداب", 34.37, 49.18),
    (["شیراز", "Shiraz"], "شیراز", 29.59, 52.58),
    (["مشهد", "Mashhad"], "مشهد", 36.3, 59.6),
    (["اهواز", "Ahvaz", "Ahwaz"], "اهواز", 31.32, 48.67),
    (["آبادان", "Abadan"], "آبادان", 30.34, 48.3),
    (["دزفول", "Dezful"], "دزفول", 32.38, 48.4),
    (["بوشهر", "Bushehr"], "بوشهر", 28.97, 50.84),
    (["خارک", "Kharg"], "جزیره خارک", 29.25, 50.32),
    (["عسلویه", "Asaluyeh"], "عسلویه", 27.48, 52.61),
    (["بندرعباس", "بندر عباس", "Bandar Abbas"], "بندرعباس", 27.18, 56.27),
    (["قشم", "Qeshm"], "قشم", 26.95, 56.27),
    (["بندرخمیر", "بندر خمیر", "Khamir"], "بندرخمیر", 26.95, 55.59),
    (["لارک", "Larak"], "جزیره لارک", 26.86, 56.36),
    (["هرمز", "Hormuz"], "تنگه هرمز", 26.57, 56.25),
    (["ابوموسی", "Abu Musa"], "ابوموسی", 25.88, 55.03),
    (["تنب", "Tunb"], "تنب", 26.26, 55.31),
    (["بندر لنگه", "بندرلنگه", "Lengeh"], "بندر لنگه", 26.56, 54.88),
    (["بندر کنگ", "Kong"], "بندر کنگ", 26.6, 54.94),
    (["سیریک", "Sirik"], "سیریک", 26.52, 57.1),
    (["جاسک", "Jask"], "جاسک", 25.64, 57.77),
    (["چابهار", "Chabahar"], "چابهار", 25.29, 60.64),
    (["کنارک", "Konarak"], "کنارک", 25.36, 60.4),
    (["کرمان", "Kerman"], "کرمان", 30.28, 57.08),
    (["یزد", "Yazd"], "یزد", 31.9, 54.37),
    (["زاهدان", "Zahedan"], "زاهدان", 29.5, 60.86),
    (["دهرود", "Dehrud"], "دهرود", 36.05, 59.0),
    (["خرم‌آباد", "خرم آباد", "Khorramabad"], "خرم‌آباد", 33.49, 48.36),
    (["ارومیه", "Urmia"], "ارومیه", 37.55, 45.08),
    (["بغداد", "Baghdad"], "بغداد", 33.31, 44.36),
    (["اربیل", "Erbil", "Irbil"], "اربیل", 36.19, 44.01),
    (["عین الاسد", "عین‌الاسد", "Ain al-Asad", "Ain al Asad"], "عین‌الاسد", 33.8, 42.44),
    (["بصره", "Basra"], "بصره", 30.51, 47.81),
    (["دمشق", "Damascus"], "دمشق", 33.51, 36.29),
    (["بیروت", "Beirut"], "بیروت", 33.89, 35.5),
    (["تل‌آویو", "تل آویو", "Tel Aviv", "תל אביב"], "تل‌آویو", 32.08, 34.78),
    (["حیفا", "Haifa", "חיפה"], "حیفا", 32.79, 34.99),
    (["اورشلیم", "Jerusalem", "ירושלים"], "اورشلیم", 31.78, 35.22),
    (["دیمونا", "Dimona", "דימונה"], "دیمونا", 31.07, 35.03),
    (["نواتیم", "Nevatim", "נבטים"], "نواتیم", 31.21, 35.01),
    (["بئرشبع", "Beersheba", "Be'er Sheva", "באר שבע"], "بئرشبع", 31.25, 34.79),
    (["ایلات", "Eilat", "אילת"], "ایلات", 29.56, 34.95),
    (["امان", "Amman"], "امان", 31.95, 35.93),
    (["ریاض", "Riyadh", "الرياض"], "ریاض", 24.71, 46.68),
    (["جده", "Jeddah"], "جده", 21.49, 39.19),
    (["مدینه", "Medina", "Madinah", "المدينة"], "مدینه", 24.47, 39.61),
    (["مکه", "Mecca", "Makkah"], "مکه", 21.42, 39.83),
    (["نجران", "Najran"], "نجران", 17.49, 44.13),
    (["جیزان", "Jizan", "Jazan"], "جیزان", 16.89, 42.55),
    (["دمام", "Dammam"], "دمام", 26.43, 50.1),
    (["العدید", "Al Udeid"], "العدید", 25.12, 51.31),
    (["دوحه", "Doha"], "دوحه", 25.29, 51.53),
    (["منامه", "Manama"], "منامه", 26.23, 50.59),
    (["کویت", "Kuwait"], "کویت", 29.37, 47.98),
    (["ابوظبی", "Abu Dhabi"], "ابوظبی", 24.45, 54.38),
    (["دبی", "Dubai"], "دبی", 25.2, 55.27),
    (["فجیره", "Fujairah"], "فجیره", 25.12, 56.33),
    (["خصب", "Khasab"], "خصب", 26.18, 56.25),
    (["مسقط", "Muscat"], "مسقط", 23.59, 58.41),
    (["صنعا", "Sanaa", "Sana'a"], "صنعا", 15.37, 44.19),
    (["حدیده", "Hodeidah"], "حدیده", 14.8, 42.95),
    (["عدن", "Aden"], "عدن", 12.79, 45.03),
]

KINDS = [
    ("uxo", r"مهمات عمل\s?نکرده|انهدام کنترل|خنثی‌سازی|UXO|unexploded|ordnance disposal"),
    ("air_defense", r"پدافند|ضدهوایی|رهگیر|air defen[cs]e|interceptor|intercepted|SAM\b|surface-to-air|יירוט|כיפת ברזל|Iron Dome|David's Sling|Arrow|THAAD|Patriot"),
    ("missile", r"موشک|پرتابه|missile|projectile|ballistic|cruise|טיל"),
    ("drone", r"پهپاد|drone|UAV|MQ-?9|כטב\"?ם"),
    ("strike", r"حمله هوایی|بمباران|airstrike|air strike|strikes? (?:on|hit)|תקיפה"),
    ("explosion", r"انفجار|صدای مهیب|explosion|blast|פיצוץ"),
    ("fighter", r"جنگنده|fighter jet|sonic boom|מטוסי קרב"),
    ("sirens", r"آژیر|siren|אזעקה|צבע אדום"),
    ("fire", r"آتش‌سوزی|حریق|fire broke|blaze"),
]
KIND_RE = [(k, re.compile(p, re.I)) for k, p in KINDS]
# names that are easily part of other words or of unrelated stories: require word boundaries
_compiled = []
for names, canon, lat, lon in PLACES:
    pats = []
    for n in names:
        if re.search(r"[A-Za-z]", n):
            pats.append(r"\b" + re.escape(n) + r"\b")
        else:
            pats.append(r"(?<![؀-ۿ])" + re.escape(n) + r"(?![؀-ۿ])")
    _compiled.append((re.compile("|".join(pats), re.I), canon, lat, lon))

NOISE = re.compile(r"Kyiv|Kiev|Kharkiv|Ukraine|اوکراین|کی‌یف|Gaza City|Rafah", re.I)


def _match(text):
    if not text or NOISE.search(text):
        return None
    kinds = [k for k, r in KIND_RE if r.search(text)]
    if not kinds:
        return None
    for r, canon, lat, lon in _compiled:
        if r.search(text):
            return kinds, canon, lat, lon
    return None


def geotag(tg_posts, stories, now, hours=24):
    """Return newest-first list of auto-located kinetic reports from the last `hours`."""
    from datetime import datetime
    cutoff = now - timedelta(hours=hours)
    out = []

    def ts(s):
        try:
            return datetime.fromisoformat(str(s).replace("Z", "+00:00"))
        except Exception:
            return None

    for p in tg_posts or []:
        t = ts(p.get("t"))
        if not t or t < cutoff:
            continue
        m = _match(p.get("text", ""))
        if m:
            out.append({"t": p["t"], "src": "tg:" + p.get("ch", ""), "link": p.get("link"), "place": m[1],
                        "lat": m[2], "lon": m[3], "kinds": m[0], "text": p.get("text", "")[:220]})
    for s in stories or []:
        t = ts(s.get("first") or s.get("pub"))
        if not t or t < cutoff:
            continue
        m = _match(s.get("title", ""))
        if m:
            out.append({"t": s.get("first") or s.get("pub"), "src": "news:" + ", ".join(s.get("outlets", [])[:3]),
                        "link": (s.get("links") or [None])[0], "place": m[1], "lat": m[2], "lon": m[3],
                        "kinds": m[0], "text": s.get("title", "")[:220], "n_outlets": len(s.get("outlets", []))})
    out.sort(key=lambda x: x["t"] or "", reverse=True)
    # cluster: same place + same main kind within 3h -> one item with a source count
    clusters = []
    for e in out:
        for c in clusters:
            if c["place"] == e["place"] and c["kinds"][0] == e["kinds"][0] and abs((ts(c["t"]) - ts(e["t"])).total_seconds()) <= 3 * 3600:
                c["n_sources"] += 1
                if len(c["more"]) < 4 and e["link"] not in c["more"] and e["link"] != c["link"]:
                    c["more"].append(e["link"])
                break
        else:
            clusters.append({**e, "n_sources": 1, "more": []})
    return clusters[:40]


def main(data_dir="data"):
    """Standalone step (run after collect.py): adds geo_events to digest.json and a ## geo section to brief.md."""
    import json
    import os
    from datetime import datetime, timezone
    dig_f, st_f, br_f = (os.path.join(data_dir, n) for n in ("digest.json", "state.json", "brief.md"))
    try:
        d = json.load(open(dig_f, encoding="utf-8"))
        st = json.load(open(st_f, encoding="utf-8")) if os.path.exists(st_f) else {}
        try:
            now = datetime.fromisoformat(d["generated"].replace("Z", "+00:00"))
        except Exception:
            now = datetime.now(timezone.utc)
        ev = geotag(st.get("tg_posts", []), st.get("stories", []), now)
        d["geo_events"] = ev
        d.setdefault("sources_status", {})["geo"] = "ok"
    except Exception as e:  # never break the collector
        print("geo step failed:", type(e).__name__, str(e)[:200])
        return 0
    json.dump(d, open(dig_f, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    head = "## geo (auto-located kinetic reports, UNVERIFIED keyword+place match; check date/source; conf u unless confirmed)"
    lines = [head] + ([f"- {g['t']} {g['place']} ({g['lat']},{g['lon']}) {'/'.join(g['kinds'])} x{g['n_sources']} "
                       f"{g['src'][:40]}: {g['text'][:160]} {g['link']}" for g in ev[:30]] or ["- none"])
    if os.path.exists(br_f):
        b = open(br_f, encoding="utf-8").read()
        b = re.sub(r"(?ms)^## geo \(.*?(?=^## |\Z)", "", b)
        k = b.find("## telegram")
        b = (b[:k] + "\n".join(lines) + "\n\n" + b[k:]) if k >= 0 else (b.rstrip() + "\n\n" + "\n".join(lines) + "\n")
        open(br_f, "w", encoding="utf-8").write(b)
    print(f"geo: {len(ev)} located reports")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
