"""LinkedIn visuals v2: dark/light alternation, electric blue + cyan + fluo lime, architectural line graphics."""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).parent
OUT = ROOT / "out2"
HTML = ROOT / "html2"
OUT.mkdir(exist_ok=True)
HTML.mkdir(exist_ok=True)
FS = (ROOT / "node_modules/@fontsource").as_uri()

BLUE, CYAN, LIME = "#2B5BFF", "#4FE3FF", "#D4FF3A"

CSS = f"""
@font-face {{ font-family:SG; font-weight:500; src:url('{FS}/space-grotesk/files/space-grotesk-latin-500-normal.woff2'); }}
@font-face {{ font-family:SG; font-weight:700; src:url('{FS}/space-grotesk/files/space-grotesk-latin-700-normal.woff2'); }}
@font-face {{ font-family:MR; font-weight:400; src:url('{FS}/manrope/files/manrope-latin-400-normal.woff2'); }}
@font-face {{ font-family:MR; font-weight:600; src:url('{FS}/manrope/files/manrope-latin-600-normal.woff2'); }}
@font-face {{ font-family:MR; font-weight:700; src:url('{FS}/manrope/files/manrope-latin-700-normal.woff2'); }}
@font-face {{ font-family:JB; font-weight:500; src:url('{FS}/jetbrains-mono/files/jetbrains-mono-latin-500-normal.woff2'); }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html,body {{ width:1080px; height:1350px; }}
body {{ font-family:MR; position:relative; overflow:hidden; display:flex; flex-direction:column; padding:88px 84px 64px; }}
body.d {{ background:#070B1A; color:#F4F7FF; --mut:#8C97B8; --ln:rgba(79,227,255,.08); --acc:{CYAN}; --hl:{LIME}; --card:rgba(255,255,255,.04); --bd:rgba(79,227,255,.22); }}
body.l {{ background:#EEF3FB; color:#0A1230; --mut:#56618A; --ln:rgba(10,18,48,.06); --acc:{BLUE}; --hl:{BLUE}; --card:#FFFFFF; --bd:rgba(43,91,255,.25); }}
body::before {{ content:''; position:absolute; inset:0; z-index:0;
  background-image:linear-gradient(var(--ln) 1px,transparent 1px),linear-gradient(90deg,var(--ln) 1px,transparent 1px);
  background-size:54px 54px; }}
body.d::after {{ content:''; position:absolute; width:1100px; height:1100px; right:-420px; top:-460px; z-index:0;
  background:radial-gradient(circle, rgba(43,91,255,.55) 0%, rgba(43,91,255,.12) 38%, transparent 68%); }}
body.l::after {{ content:''; position:absolute; width:900px; height:900px; left:-380px; bottom:-420px; z-index:0;
  background:radial-gradient(circle, rgba(79,227,255,.45) 0%, rgba(79,227,255,.08) 45%, transparent 70%); }}
body > * {{ position:relative; z-index:1; }}
.top {{ display:flex; justify-content:space-between; align-items:center; font-family:JB; font-size:21px; letter-spacing:.12em; text-transform:uppercase; color:var(--mut); }}
.tag {{ color:var(--acc); display:flex; align-items:center; gap:14px; }}
.tag::before {{ content:''; width:14px; height:14px; background:var(--hl); display:inline-block; }}
body.l .tag::before {{ background:{BLUE}; }}
h1 {{ font-family:SG; font-weight:700; font-size:82px; line-height:1.0; letter-spacing:-.035em; margin-top:52px; }}
h1.xl {{ font-size:112px; }}
h1 em {{ font-style:normal; color:var(--acc); }}
.sub {{ font-size:31px; line-height:1.42; color:var(--mut); margin-top:30px; max-width:880px; }}
.sub b {{ color:inherit; font-weight:700; }}
body.d .sub b {{ color:#F4F7FF; }} body.l .sub b {{ color:#0A1230; }}
.grow {{ flex:1; }}
.art {{ flex:1; display:flex; align-items:center; justify-content:center; margin:28px 0 24px; }}
.foot {{ display:flex; justify-content:space-between; align-items:center; gap:36px; border-top:1px solid var(--bd); padding-top:24px; }}
.who {{ display:flex; align-items:center; gap:18px; white-space:nowrap; }}
.av {{ width:78px; height:78px; border-radius:50%; overflow:hidden; border:2px solid var(--acc); flex:none;
  background:radial-gradient(circle at 50% 40%, rgba(79,227,255,.35), rgba(43,91,255,.18) 60%, transparent 75%); }}
.av img {{ width:100%; height:100%; display:block; object-fit:cover; }}
.nm {{ font-family:SG; font-weight:700; font-size:23px; line-height:1.15; }}
.rl {{ font-size:18px; color:var(--mut); }}
.src {{ font-family:JB; font-size:15px; line-height:1.45; color:var(--mut); text-align:right; max-width:560px; }}
.big {{ font-family:SG; font-weight:700; font-size:300px; line-height:.86; letter-spacing:-.06em; color:var(--acc); }}
body.d .big {{ color:{LIME}; text-shadow:0 0 60px rgba(212,255,58,.35); }}
.stats {{ display:grid; grid-template-columns:repeat(3,1fr); gap:18px; }}
.st {{ background:var(--card); border:1px solid var(--bd); padding:26px 24px; }}
.st .v {{ font-family:SG; font-weight:700; font-size:54px; letter-spacing:-.03em; color:var(--acc); }}
.st .k {{ font-size:20px; color:var(--mut); margin-top:6px; line-height:1.3; }}
"""


def foot(src=""):
    return (f'<div class="foot"><div class="who"><div class="av"><img src="{(ROOT / "photo/avatar.png").as_uri()}"></div><div><div class="nm">Gabriele Maffezzini</div>'
            f'<div class="rl">Project &amp; Development, EMEA</div></div></div><div class="src">{src}</div></div>')


def page(theme, tag, num, body, src=""):
    top = f'<div class="top"><span class="tag">{tag}</span><span>{num}</span></div>'
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head>'
            f'<body class="{theme}">{top}{body}{foot(src)}</body></html>')


def hbars(rows, maxv, dark, w=912):
    """rows: (label, value, text, highlight)"""
    acc = LIME if dark else BLUE
    base = "rgba(255,255,255,.14)" if dark else "rgba(10,18,48,.12)"
    txt = "#F4F7FF" if dark else "#0A1230"
    mut = "#8C97B8" if dark else "#56618A"
    h = len(rows) * 150
    s = f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
    if dark:
        s += '<defs><filter id="gl" x="-20%" y="-200%" width="140%" height="500%"><feGaussianBlur stdDeviation="10" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>'
    for i, (lab, v, t, hi) in enumerate(rows):
        y = i * 150
        bw = max(v / maxv * w, 10)
        col = acc if hi else base
        f = ' filter="url(#gl)"' if (hi and dark) else ""
        s += (f'<text x="0" y="{y+38}" font-family="MR" font-weight="600" font-size="28" fill="{mut}">{lab}</text>'
              f'<text x="{w}" y="{y+44}" text-anchor="end" font-family="SG" font-weight="700" font-size="52" fill="{txt}">{t}</text>'
              f'<rect x="0" y="{y+66}" width="{w}" height="2" fill="{base}"/>'
              f'<rect x="0" y="{y+62}" width="{bw:.0f}" height="34" fill="{col}"{f}/>')
    return s + "</svg>"


# ---------- art pieces ----------
def art_map_shifts():
    # four tiles with line icons
    c, l = CYAN, LIME
    tiles = [
        ("01", "Less space,<br>better space",
         f'<rect x="10" y="10" width="120" height="120" fill="none" stroke="{c}" stroke-opacity=".35" stroke-width="2" stroke-dasharray="6 6"/>'
         f'<rect x="40" y="40" width="70" height="70" fill="{l}" fill-opacity=".9"/>'),
        ("02", "From the edge<br>to the centre",
         f'<circle cx="70" cy="70" r="60" fill="none" stroke="{c}" stroke-opacity=".3" stroke-width="2"/>'
         f'<circle cx="70" cy="70" r="36" fill="none" stroke="{c}" stroke-opacity=".6" stroke-width="2"/>'
         f'<circle cx="70" cy="70" r="12" fill="{l}"/><path d="M128 18 L84 58" stroke="{c}" stroke-width="3"/>'
         f'<path d="M84 58 l3 -16 M84 58 l16 -3" stroke="{c}" stroke-width="3" fill="none"/>'),
        ("03", "From coworking<br>to branded space",
         f'<rect x="20" y="14" width="100" height="116" fill="none" stroke="{c}" stroke-width="3"/>'
         f'<rect x="38" y="34" width="64" height="22" fill="{l}"/><circle cx="102" cy="80" r="5" fill="{c}"/>'),
        ("04", "From offices<br>to hotels",
         f'<rect x="12" y="20" width="52" height="110" fill="none" stroke="{c}" stroke-width="3"/>'
         + "".join(f'<rect x="20" y="{30+i*20}" width="36" height="8" fill="{c}" fill-opacity=".5"/>' for i in range(5))
         + f'<rect x="80" y="20" width="52" height="110" fill="none" stroke="{l}" stroke-width="3"/>'
         + "".join(f'<rect x="{88+j*20}" y="{30+i*20}" width="14" height="12" fill="{l}"/>' for i in range(5) for j in range(2))),
    ]
    out = '<div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;width:100%">'
    for n, t, svg in tiles:
        out += (f'<div style="border:1px solid rgba(79,227,255,.22);background:rgba(255,255,255,.035);padding:30px 30px 28px;display:flex;gap:26px;align-items:center">'
                f'<svg width="140" height="140" viewBox="0 0 140 140">{svg}</svg>'
                f'<div><div style="font-family:JB;font-size:20px;color:{CYAN};letter-spacing:.1em">{n}</div>'
                f'<div style="font-family:SG;font-weight:700;font-size:34px;line-height:1.08;margin-top:10px;letter-spacing:-.02em">{t}</div></div></div>')
    return out + "</div>"


def art_rooms():
    # rooms (squares) connected by relationship lines, light theme
    nodes = [(150, 120, 130), (520, 70, 170), (820, 190, 120), (290, 400, 160), (690, 430, 150), (110, 650, 110), (520, 700, 120), (860, 640, 100)]
    links = [(0, 1), (1, 2), (0, 3), (1, 3), (1, 4), (2, 4), (3, 4), (3, 5), (3, 6), (4, 6), (4, 7), (5, 6)]
    s = '<svg width="820" height="690" viewBox="0 0 980 820">'
    for a, b in links:
        x1, y1, s1 = nodes[a]; x2, y2, s2 = nodes[b]
        s += f'<line x1="{x1+s1/2}" y1="{y1+s1/2}" x2="{x2+s2/2}" y2="{y2+s2/2}" stroke="{BLUE}" stroke-width="3" stroke-opacity=".55"/>'
    for i, (x, y, z) in enumerate(nodes):
        fill = BLUE if i in (1, 3, 4) else "#FFFFFF"
        s += f'<rect x="{x}" y="{y}" width="{z}" height="{z}" fill="{fill}" stroke="{BLUE}" stroke-width="3"/>'
        s += f'<circle cx="{x+z/2}" cy="{y+z/2}" r="9" fill="{CYAN if fill==BLUE else BLUE}"/>'
    return s + "</svg>"


def art_rings():
    # city map: CBD centre vs edge, light theme
    cx, cy = 456, 400
    s = '<svg width="912" height="800" viewBox="0 0 912 800">'
    s += f'<circle cx="{cx}" cy="{cy}" r="380" fill="rgba(10,18,48,.04)" stroke="#0A1230" stroke-opacity=".25" stroke-width="2" stroke-dasharray="8 8"/>'
    s += f'<circle cx="{cx}" cy="{cy}" r="230" fill="rgba(43,91,255,.10)" stroke="{BLUE}" stroke-opacity=".5" stroke-width="2"/>'
    s += f'<circle cx="{cx}" cy="{cy}" r="100" fill="{BLUE}"/>'
    # roads
    for ang in (20, 80, 140, 200, 260, 320):
        import math
        a = math.radians(ang)
        s += f'<line x1="{cx+100*math.cos(a):.0f}" y1="{cy+100*math.sin(a):.0f}" x2="{cx+400*math.cos(a):.0f}" y2="{cy+400*math.sin(a):.0f}" stroke="#0A1230" stroke-opacity=".12" stroke-width="3"/>'
    s += (f'<text x="{cx}" y="{cy-6}" text-anchor="middle" font-family="SG" font-weight="700" font-size="62" fill="#FFFFFF">~2%</text>'
          f'<text x="{cx}" y="{cy+34}" text-anchor="middle" font-family="JB" font-size="18" fill="{CYAN}" letter-spacing="2">PRIME CBD</text>'
          f'<text x="{cx}" y="{cy-150}" text-anchor="middle" font-family="SG" font-weight="700" font-size="56" fill="{BLUE}">5.6%</text>'
          f'<text x="{cx}" y="{cy-118}" text-anchor="middle" font-family="JB" font-size="18" fill="#56618A" letter-spacing="2">CBD AVERAGE</text>'
          f'<text x="{cx}" y="{cy+300}" text-anchor="middle" font-family="SG" font-weight="700" font-size="56" fill="#0A1230">11.2%</text>'
          f'<text x="{cx}" y="{cy+332}" text-anchor="middle" font-family="JB" font-size="18" fill="#56618A" letter-spacing="2">OUTSIDE THE CBD</text>')
    return s + "</svg>"


def art_squares():
    # area-true squares: 49k vs 334k sqm, dark theme
    big, small = 520, 520 / (334000 / 49050) ** 0.5
    s = '<svg width="912" height="600" viewBox="0 0 912 600"><defs><filter id="g2" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="18"/></filter></defs>'
    s += f'<rect x="40" y="{560-small:.0f}" width="{small:.0f}" height="{small:.0f}" fill="none" stroke="{CYAN}" stroke-width="3"/>'
    s += f'<text x="40" y="{540-small:.0f}" font-family="SG" font-weight="700" font-size="40" fill="#F4F7FF">49k</text>'
    s += f'<text x="40" y="590" font-family="JB" font-size="18" fill="#8C97B8">2020</text>'
    x = 352
    s += f'<rect x="{x}" y="{560-big}" width="{big}" height="{big}" fill="{LIME}" opacity=".35" filter="url(#g2)"/>'
    s += f'<rect x="{x}" y="{560-big}" width="{big}" height="{big}" fill="{LIME}"/>'
    s += f'<text x="{x+36}" y="{560-big+86}" font-family="SG" font-weight="700" font-size="84" fill="#070B1A">334k</text>'
    s += f'<text x="{x+38}" y="{560-big+128}" font-family="JB" font-size="20" fill="#070B1A">SQ M - 2025</text>'
    s += f'<text x="{x+38}" y="{560-36}" font-family="SG" font-weight="700" font-size="44" fill="#070B1A">~7x</text>'
    return s + "</svg>"


def art_street():
    # street section: office + city services, light theme
    s = '<svg width="912" height="620" viewBox="0 0 912 620">'
    g = 520
    s += f'<line x1="0" y1="{g}" x2="912" y2="{g}" stroke="#0A1230" stroke-width="3"/>'
    # office tower
    s += f'<rect x="345" y="80" width="230" height="{g-80}" fill="{BLUE}"/>'
    for i in range(9):
        s += f'<rect x="365" y="{104+i*44}" width="190" height="18" fill="{CYAN}" fill-opacity=".55"/>'
    s += f'<text x="455" y="{g+52}" text-anchor="middle" font-family="JB" font-size="18" fill="{BLUE}" letter-spacing="2">THE OFFICE</text>'
    items = [(10, 300, 190, "HOTEL LOBBY"), (214, 400, 110, "CAFE"), (600, 360, 140, "GYM"), (785, 260, 110, "PARK")]
    for x, y, w, lab in items:
        if lab == "PARK":
            s += f'<circle cx="{x+55}" cy="{g-90}" r="62" fill="none" stroke="#0A1230" stroke-width="3"/><line x1="{x+55}" y1="{g-28}" x2="{x+55}" y2="{g}" stroke="#0A1230" stroke-width="3"/>'
        else:
            s += f'<rect x="{x}" y="{y}" width="{w}" height="{g-y}" fill="#FFFFFF" stroke="#0A1230" stroke-width="3"/>'
            s += f'<rect x="{x+18}" y="{g-70}" width="{w-36}" height="52" fill="none" stroke="{BLUE}" stroke-width="3"/>'
        s += f'<text x="{x+w/2 if lab!="PARK" else x+55}" y="{g+52}" text-anchor="middle" font-family="JB" font-size="16" fill="#56618A" letter-spacing="1">{lab}</text>'
    # connections
    for x in (105, 269, 670, 840):
        s += f'<path d="M455 {g-12} Q {(455+x)/2} {g-150} {x} {g-12}" fill="none" stroke="{BLUE}" stroke-width="2.5" stroke-dasharray="7 7"/>'
    return s + "</svg>"


def art_facades():
    # office grid -> hotel windows, dark theme
    s = '<svg width="912" height="560" viewBox="0 0 912 560"><defs><filter id="g3"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>'
    s += f'<rect x="20" y="40" width="330" height="500" fill="none" stroke="#8C97B8" stroke-width="3"/>'
    for i in range(8):
        s += f'<rect x="40" y="{62+i*58}" width="290" height="30" fill="#8C97B8" fill-opacity=".28"/>'
    s += f'<text x="20" y="24" font-family="JB" font-size="18" fill="#8C97B8" letter-spacing="2">OFFICE</text>'
    s += f'<path d="M392 290 H 520" stroke="{CYAN}" stroke-width="4"/><path d="M500 272 L 522 290 L 500 308" fill="none" stroke="{CYAN}" stroke-width="4"/>'
    s += f'<rect x="562" y="40" width="330" height="500" fill="none" stroke="{LIME}" stroke-width="3" filter="url(#g3)"/>'
    lit = {(0, 1), (1, 3), (2, 0), (3, 2), (4, 3), (5, 1), (6, 0), (2, 3), (6, 2)}
    for i in range(7):
        for j in range(4):
            on = (i, j) in lit
            s += f'<rect x="{586+j*76}" y="{62+i*62}" width="52" height="38" fill="{LIME if on else CYAN}" fill-opacity="{1 if on else .22}"/>'
    s += f'<text x="562" y="24" font-family="JB" font-size="18" fill="{LIME}" letter-spacing="2">HOTEL</text>'
    return s + "</svg>"


# ---------- pages ----------
P = {}
P["post01_presentazione"] = page("d", "A new series", "01",
    '<h1>The real estate map is <em>being redrawn.</em></h1>'
    '<div class="sub">What it means for the people who design, build and pay for buildings.</div>'
    f'<div class="art">{art_map_shifts()}</div>', "Europe - Americas - Asia")
P["post02_orgatec"] = page("l", "ORGATEC 2026 - Cologne", "02",
    '<h1>From rooms<br>to <em>relationships.</em></h1>'
    '<div class="sub">The first central theme in the fair\'s history. Not "how many fit?" but <b>"why would they come?"</b></div>'
    f'<div class="art">{art_rooms()}</div>', "Source: ORGATEC 2026, orgatec.com")
P["post04_centro"] = page("l", "Europe - office vacancy", "04",
    '<h1>The centre fills up.<br><em>The edge empties.</em></h1>'
    f'<div class="art">{art_rings()}</div>',
    "Sources: European office market research, Q1 and Q2 2026 (13 CBD markets)")
P["post05_managed"] = page("d", "London - managed office stock", "05",
    '<h1>Coworking <em>grew up.</em></h1>'
    '<div class="sub">Private floors, the client\'s brand, run by an operator. The fastest-growing part of flex.</div>'
    f'<div class="art">{art_squares()}</div>', "Source: London managed office research, via Allwork.Space, Aug 2026. Squares to scale.")
P["post06_citta"] = page("l", "Workplace", "06",
    '<h1>The best office amenity might be <em>the street outside.</em></h1>'
    f'<div class="art">{art_street()}</div>', "")
P["post07_conversioni"] = page("d", "Europe - adaptive reuse", "07",
    '<h1>Offices are <em>checking out.</em></h1>'
    f'<div class="art">{art_facades()}</div>'
    '<div class="stats" style="margin-bottom:28px"><div class="st"><div class="v">12%</div><div class="k">CBD office deals for conversion, 2022</div></div>'
    '<div class="st"><div class="v">17%</div><div class="k">H1 2026, highest in 14 years</div></div>'
    '<div class="st"><div class="v">70%+</div><div class="k">of conversions go to homes and hotels</div></div></div>',
    "Source: MSCI Real Capital Analytics, Aug 2026 (deals above EUR 5m)")
P["post08_italia"] = page("l", "Hotels - RevPAR growth H1 2026", "08",
    '<h1>Italy is <em>outrunning</em> Europe.</h1>'
    f'<div class="art">{hbars([("Italy", 11.3, "+11.3%", True), ("European average", 3.0, "+3.0%", False)], 12, False)}</div>'
    '<div class="stats" style="margin-bottom:28px"><div class="st"><div class="v">EUR 1.3bn</div><div class="k">hotel investment in six months</div></div>'
    '<div class="st"><div class="v">+53%</div><div class="k">vs the 10-year average</div></div>'
    '<div class="st"><div class="v">+143%</div><div class="k">Milan volumes, year on year</div></div></div>',
    "Source: Cushman &amp; Wakefield, Hospitality MarketBeat Italy H1 2026")

S3 = "Sources: Cushman &amp; Wakefield, European Office Update, Mar 2026; European office leasing research, Q2 2026"
C = [
    page("d", "Office market 2026", "1/8",
         '<div class="grow"></div><h1 class="xl">Less space.<br><em>Better space.</em></h1>'
         '<div class="sub">What the market is telling occupiers, in 7 slides.</div><div class="grow"></div>'
         f'<div style="margin-bottom:40px"><svg width="912" height="220" viewBox="0 0 912 220">'
         f'<rect x="0" y="10" width="560" height="200" fill="none" stroke="{CYAN}" stroke-opacity=".4" stroke-width="2" stroke-dasharray="10 8"/>'
         f'<rect x="600" y="60" width="150" height="150" fill="{LIME}"/><path d="M570 110 H 590" stroke="{CYAN}" stroke-width="3"/></svg></div>'),
    page("l", "Quality wins", "2/8",
         '<div class="grow"></div><div class="big">52%</div>'
         '<h1 style="font-size:64px;margin-top:40px">of office space leased in Europe in 2025 was <em>Grade A.</em></h1>'
         '<div class="sub">The highest share on record.</div><div class="grow"></div>', S3),
    page("d", "The best space is almost gone", "3/8",
         '<h1>Vacancy in Europe</h1><div class="sub">The better the space, the less of it is left.</div>'
         f'<div class="art">{hbars([("Prime CBD", 2, "~2%", True), ("Grade A", 3.5, "3.5%", True), ("All offices", 9.4, "9.4%", False)], 10, True)}</div>', S3),
    page("l", "Prime pulls away", "4/8",
         '<h1>Rent growth<br>since 2019</h1><div class="sub">Prime rents grew three times faster than secondary.</div>'
         f'<div class="art">{hbars([("Prime", 27, "+27%", True), ("Secondary", 9, "+9%", False)], 30, False)}</div>', S3),
    page("d", "Nothing new is coming soon", "5/8",
         '<div class="grow"></div><div class="big">2016</div>'
         '<h1 style="font-size:66px;margin-top:40px">Office construction in Europe is at its <em>lowest since then.</em></h1>'
         '<div class="sub">Demand for quality rises while the pipeline shrinks.</div><div class="grow"></div>', S3),
    page("l", "Refurbishment is the route to prime", "6/8",
         '<h1>Payback of upgrading<br>secondary to prime</h1><div class="sub">Half the time it took before.</div>'
         f'<div class="art">{hbars([("Before", 10, "~10 yrs", False), ("Now", 5, "~5 yrs", True)], 10, False)}</div>', S3),
    page("d", "What it means for projects", "7/8",
         '<div class="grow"></div><h1 style="font-size:92px">Fewer square metres.<br><em>Higher spec per square metre.</em></h1>'
         '<div class="sub">The fit-out budget moves from quantity to quality: acoustics, light, services, flexibility.</div><div class="grow"></div>'),
    page("l", "Your turn", "8/8",
         '<div class="grow"></div><h1 class="xl">Shrinking, upgrading, <em>or both?</em></h1>'
         '<div class="sub">Tell me what your company is doing in the comments.</div><div class="grow"></div>'),
]


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg = await b.new_page(viewport={"width": 1080, "height": 1350})

        async def shot(name, html):
            f = HTML / f"{name}.html"
            f.write_text(html, encoding="utf-8")
            await pg.goto(f.as_uri(), wait_until="networkidle")
            await pg.evaluate("document.fonts.ready")
            await pg.screenshot(path=str(OUT / f"{name}.png"))
            return OUT / f"{name}.png"

        for n, h in P.items():
            await shot(n, h)
        slides = [await shot(f"post03_slide{i}", h) for i, h in enumerate(C, 1)]
        await b.close()
    from PIL import Image
    ims = [Image.open(s).convert("RGB") for s in slides]
    ims[0].save(OUT / "post03_carosello_less-space-better-space.pdf", save_all=True, append_images=ims[1:], resolution=150)
    # cover image of carousel also as single image for the post preview
    ims[0].save(OUT / "post03_copertina.png")


