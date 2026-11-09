"""Carousels for 5, 10 and 12 November 2026, same formula as the AI post."""
import asyncio, math
from pathlib import Path
from playwright.async_api import async_playwright
from r2lib import page, hbars, art_rooms, art_squares, BLUE, CYAN, LIME, HTML

OUT = Path(__file__).parent / "out_next"
OUT.mkdir(exist_ok=True)
SCR = "/tmp/claude-0/-home-claude/3116edaa-2b55-58f6-9d21-13d8e709f5e9/scratchpad/"
INK, MUT = "#0A1230", "#56618A"


def glow(fid):
    return (f'<defs><filter id="{fid}" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="8" result="b"/>'
            f'<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>')


def tiles(items, cols=2, big=None, mb=28):
    st = f'grid-template-columns:repeat({cols},1fr);gap:14px;margin-bottom:{mb}px'
    out = f'<div class="stats" style="{st}">'
    for v, k in items:
        vs = f' style="font-size:{big}px"' if big else ""
        out += f'<div class="st"><div class="v"{vs}>{v}</div><div class="k">{k}</div></div>'
    return out + "</div>"


# ---------- art ----------
def art_week():
    s = f'<svg width="912" height="330" viewBox="0 0 912 330">{glow("gw")}'
    for i, d in enumerate(["MON", "TUE", "WED", "THU", "FRI"]):
        x = 10 + i * 182
        on = d in ("TUE", "THU")
        if on:
            s += f'<rect x="{x}" y="20" width="158" height="230" fill="{LIME}" filter="url(#gw)"/>'
        else:
            s += f'<rect x="{x}" y="20" width="158" height="230" fill="none" stroke="{CYAN}" stroke-opacity=".45" stroke-width="2" stroke-dasharray="8 7"/>'
        s += f'<text x="{x+79}" y="296" text-anchor="middle" font-family="JB" font-size="22" fill="{LIME if on else "#8C97B8"}" letter-spacing="3">{d}</text>'
    return s + "</svg>"


def art_floor():
    s = '<svg width="912" height="560" viewBox="0 0 912 560">'
    s += f'<rect x="10" y="10" width="892" height="540" fill="#FFFFFF" stroke="{INK}" stroke-width="3"/>'
    zones = [(40, 40, 260, 200, "TEAM A"), (40, 310, 260, 210, "TEAM B"), (612, 40, 260, 200, "TEAM C"), (612, 310, 260, 210, "FOCUS")]
    for x, y, w, h, lab in zones:
        s += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{BLUE}" fill-opacity=".10" stroke="{BLUE}" stroke-width="2"/>'
        for r in range(2):
            for c in range(4):
                s += f'<rect x="{x+22+c*58}" y="{y+50+r*64}" width="40" height="30" fill="{BLUE}" fill-opacity=".55"/>'
        s += f'<text x="{x+14}" y="{y+30}" font-family="JB" font-size="17" fill="{BLUE}" letter-spacing="2">{lab}</text>'
    s += f'<circle cx="456" cy="280" r="150" fill="{CYAN}" fill-opacity=".35" stroke="{BLUE}" stroke-width="3"/>'
    s += f'<text x="456" y="272" text-anchor="middle" font-family="SG" font-weight="700" font-size="34" fill="{INK}">HOSPITALITY</text>'
    s += f'<text x="456" y="306" text-anchor="middle" font-family="JB" font-size="17" fill="{INK}" letter-spacing="2">CAFE - WELCOME - EVENTS</text>'
    return s + "</svg>"


def art_hub():
    s = '<svg width="912" height="560" viewBox="0 0 912 560">'
    cx, cy = 456, 280
    sats = [(130, 110), (780, 100), (110, 450), (800, 460), (456, 500)]
    for x, y in sats:
        s += f'<line x1="{cx}" y1="{cy}" x2="{x}" y2="{y}" stroke="{BLUE}" stroke-width="3" stroke-dasharray="10 8"/>'
    for x, y in sats:
        s += f'<rect x="{x-45}" y="{y-45}" width="90" height="90" fill="#FFFFFF" stroke="{BLUE}" stroke-width="3"/>'
        s += f'<text x="{x}" y="{y+7}" text-anchor="middle" font-family="JB" font-size="18" fill="{BLUE}" letter-spacing="2">FLEX</text>'
    s += f'<rect x="{cx-110}" y="{cy-110}" width="220" height="220" fill="{BLUE}"/>'
    s += f'<text x="{cx}" y="{cy+4}" text-anchor="middle" font-family="SG" font-weight="700" font-size="44" fill="#FFFFFF">CORE</text>'
    s += f'<text x="{cx}" y="{cy+40}" text-anchor="middle" font-family="JB" font-size="17" fill="{CYAN}" letter-spacing="2">HQ, OWN BRAND</text>'
    return s + "</svg>"


def art_modules():
    s = f'<svg width="912" height="460" viewBox="0 0 912 460">{glow("gm")}'
    s += f'<rect x="10" y="10" width="892" height="440" fill="none" stroke="{CYAN}" stroke-width="3"/>'
    for r in range(3):
        for c in range(5):
            x, y = 34 + c * 174, 34 + r * 138
            hi = (r, c) == (1, 2)
            if hi:
                s += f'<rect x="{x}" y="{y}" width="152" height="116" fill="{LIME}" filter="url(#gm)"/>'
                s += f'<text x="{x+76}" y="{y+66}" text-anchor="middle" font-family="JB" font-size="18" fill="#070B1A" letter-spacing="2">RE-LET</text>'
            else:
                s += f'<rect x="{x}" y="{y}" width="152" height="116" fill="{CYAN}" fill-opacity=".12" stroke="{CYAN}" stroke-opacity=".6" stroke-width="2"/>'
    return s + "</svg>"


def star(cx, cy, R, r=None):
    r = r or R * 0.45
    pts = []
    for i in range(10):
        a = math.radians(-90 + i * 36)
        rad = R if i % 2 == 0 else r
        pts.append(f"{cx+rad*math.cos(a):.1f},{cy+rad*math.sin(a):.1f}")
    return " ".join(pts)


def art_stars():
    s = f'<svg width="912" height="260" viewBox="0 0 912 260">{glow("gs")}'
    for i in range(5):
        cx = 96 + i * 180
        if i < 4:
            s += f'<polygon points="{star(cx,120,80)}" fill="{CYAN}" fill-opacity=".85"/>'
        else:
            s += f'<polygon points="{star(cx,120,80)}" fill="{LIME}" filter="url(#gs)"/>'
    s += f'<text x="456" y="245" text-anchor="middle" font-family="JB" font-size="20" fill="#8C97B8" letter-spacing="3">FROM 4 STARS TO 5, IN THE SAME WALLS</text>'
    return s + "</svg>"


def art_arches():
    s = '<svg width="912" height="500" viewBox="0 0 912 500">'
    s += f'<rect x="40" y="60" width="832" height="420" fill="#FFFFFF" stroke="{INK}" stroke-width="3"/>'
    s += f'<path d="M20 60 L456 6 L892 60 Z" fill="none" stroke="{INK}" stroke-width="3"/>'
    for r in range(2):
        for c in range(6):
            x, y = 84 + c * 132, 110 + r * 180
            col = BLUE if (r + c) % 3 == 0 else CYAN
            s += f'<path d="M{x} {y+140} V{y+50} A42 42 0 0 1 {x+84} {y+50} V{y+140} Z" fill="{col}" fill-opacity=".55" stroke="{BLUE}" stroke-width="2.5"/>'
    return s + "</svg>"


def art_gantt():
    s = '<svg width="912" height="400" viewBox="0 0 912 400">'
    rows = [("FLOORS 1-2", 0, 3), ("FLOORS 3-4", 2, 5), ("LOBBY + F&amp;B", 4, 7), ("FLOORS 5-6", 6, 9)]
    for i, (lab, a, b) in enumerate(rows):
        y = 30 + i * 80
        s += f'<text x="0" y="{y+32}" font-family="JB" font-size="18" fill="#8C97B8" letter-spacing="2">{lab}</text>'
        s += f'<rect x="{230+a*68}" y="{y+8}" width="{(b-a)*68}" height="36" fill="{CYAN if i%2==0 else BLUE}"/>'
    s += f'<rect x="230" y="350" width="612" height="10" fill="{LIME}"/>'
    s += f'<text x="230" y="392" font-family="JB" font-size="18" fill="{LIME}" letter-spacing="2">HOTEL OPEN THROUGHOUT</text>'
    return s + "</svg>"



def art_peak():
    s = '<svg width="912" height="360" viewBox="0 0 912 360">'
    hs = [120, 260, 170, 260, 90]
    for i, (d, h) in enumerate(zip(["MON", "TUE", "WED", "THU", "FRI"], hs)):
        x = 30 + i * 176
        peak = d in ("TUE", "THU")
        s += f'<rect x="{x}" y="{300-h}" width="130" height="{h}" fill="{LIME if peak else CYAN}" fill-opacity="{1 if peak else .35}"/>'
        s += f'<text x="{x+65}" y="340" text-anchor="middle" font-family="JB" font-size="20" fill="#8C97B8" letter-spacing="3">{d}</text>'
    s += f'<line x1="0" y1="{300-260}" x2="912" y2="{300-260}" stroke="{LIME}" stroke-width="2" stroke-dasharray="8 6"/>'
    s += f'<text x="912" y="{300-272}" text-anchor="end" font-family="JB" font-size="17" fill="{LIME}" letter-spacing="2">SIZE FOR THIS LINE</text>'
    return s + '</svg>'


def art_lease():
    s = f'<svg width="912" height="420" viewBox="0 0 912 420">{glow("gl")}'
    s += f'<rect x="250" y="10" width="412" height="400" fill="none" stroke="{CYAN}" stroke-width="3"/>'
    for i in range(7):
        s += f'<rect x="290" y="{60+i*34}" width="{332 if i%3 else 240}" height="10" fill="{CYAN}" fill-opacity=".35"/>'
    s += f'<text x="456" y="340" text-anchor="middle" font-family="SG" font-weight="700" font-size="64" fill="#8C97B8">10 YEARS</text>'
    s += f'<rect x="280" y="316" width="352" height="10" fill="{LIME}"/>'
    return s + '</svg>'

# ---------- carousels ----------
SRC_BK = "Source: Allwork.Space, 28 Oct 2026 (Amsterdam court ruling)"
SRC_CW25 = "Sources: Allwork.Space, Oct 2026; Cushman &amp; Wakefield occupier survey, 2025"
SRC_CWEU = "Source: Cushman &amp; Wakefield, European office market update, Sep 2026"

A = [
    page("d", "Netherlands - 28 Oct 2026", "1/6",
         '<h1 style="margin-top:40px">A court just sent staff <em>back to the office.</em></h1>'
         '<div class="sub">An Amsterdam court backed Booking.com: at least <b>40%</b> of working time on site. Today only <b>27%</b> of staff meet it.</div>'
         f'<div class="art">{art_week()}</div>'
         '<h1 style="font-size:58px;margin-bottom:28px">A rule fills desks. <em>What fills the office?</em></h1>', SRC_BK),
    page("l", "Same week, two answers", "2/6",
         '<h1>The office is not dying. <em>It is being tested.</em></h1>'
         '<div class="sub">Amsterdam pushed people back in. San Francisco\'s AI firms went looking for more space. ORGATEC named the question: "From rooms to relationships".</div><div class="grow"></div>'
         + tiles([("40%", "of working time on site, the new Booking.com rule"),
                  ("27%", "of its staff meet that bar today"),
                  ("90", "AI companies looking for office space in San Francisco"),
                  ("5.3m sq ft", "their combined requirement, 29% of US AI office demand")]),
         "Sources: Allwork.Space, 28 Oct 2026; The Real Deal, 3 Nov 2026 (VTS Q3 2026 data)"),
    page("d", "Principle 1 - Design for the peak", "3/6",
         '<h1>Tuesday and Thursday <em>decide the floor plan.</em></h1>'
         '<div class="sub">The court also ruled that every employee who comes in must find a place to sit. Average occupancy is no longer the design brief.</div>'
         f'<div class="art">{art_peak()}</div>', "Illustrative weekly attendance profile"),
    page("l", "Principle 2 - Hospitality, not just desks", "4/6",
         '<h1>From rooms to <em>relationships.</em></h1>'
         f'<div class="art">{art_floor()}</div>'
         + tiles([("85%", "of tenants want more from their landlord: services, amenities, events"),
                  ("46%", "would pay a premium for it")]),
         "Source: Cushman &amp; Wakefield occupier survey, 2025"),
    page("d", "Principle 3 - Plan earlier", "5/6",
         '<h1>The space you need in 2028 <em>is being decided now.</em></h1><div class="grow"></div>'
         + tiles([("3.3%", "Grade A vacancy in Europe"),
                  ("2014", "development pipeline at its lowest since then"),
                  ("-19%", "pipeline, year on year, to 8.4m sq m"),
                  ("+10.4%", "prime rent growth in Milan in a year")], mb=40), SRC_CWEU),
    page("l", "What it means for the office", "6/6",
         '<h1 style="font-size:64px">Mandates bring people in. <em>Places make them stay.</em></h1>'
         + '<div style="margin-top:36px">' + tiles([("Peak", "sized for the busiest day"), ("Host", "hospitality at the core"), ("Early", "secure quality space ahead")], cols=3, big=38, mb=0) + '</div>'
         '<div class="grow"></div><h1 style="font-size:84px;margin-bottom:20px">Will mandates bring people back, or will <em>better offices?</em></h1>'
         '<div class="sub" style="margin-top:0;margin-bottom:32px">Tell me what your company does.</div>'),
]

SRC_IWG = "Source: IWG CEO and CFO survey, reported by Urban Living News, Jul 2026"
SRC_IWG2 = "Sources: IWG via Allwork.Space, Oct 2026; India flex office market research, Oct 2026"
SRC_LDN = "Source: London managed office market research, via Allwork.Space, Aug 2026. Squares to scale."

B = [
    page("d", "Flex - after the AI layoffs", "1/6",
         '<h1 style="margin-top:40px"><em>99.8%</em> of CEOs and CFOs want their real estate costs flexible.</h1>'
         '<div class="sub">And 60% say AI has made it harder to predict how much office they will need in two years.</div>'
         f'<div class="art">{art_lease()}</div>'
         '<h1 style="font-size:58px;margin-bottom:28px">Is the <em>10-year lease</em> over?</h1>', SRC_IWG),
    page("l", "Flex is not for start-ups anymore", "2/6",
         '<h1>Enterprises are <em>the new flex tenants.</em></h1>'
         '<div class="sub">The world\'s largest flex operator is growing through partnerships with landlords, and big companies drive demand.</div><div class="grow"></div>'
         + tiles([("728", "new IWG locations signed in H1 2026, a record"),
                  ("95%", "of them through managed partnership agreements"),
                  ("x2", "India's flex stock by 2030, to about 180m sq ft"),
                  ("75-85%", "of that demand comes from enterprise clients")]), SRC_IWG2),
    page("d", "Principle 1 - Coworking grew up", "3/6",
         '<h1>From hot desks <em>to branded floors.</em></h1>'
         '<div class="sub">In London, managed offices grew about 7x in five years. 3 in 4 new users came from serviced offices.</div>'
         f'<div class="art">{art_squares()}</div>', SRC_LDN),
    page("l", "Principle 2 - Core plus flex", "4/6",
         '<h1>One core HQ. <em>Flexible space around it.</em></h1>'
         f'<div class="art">{art_hub()}</div>'
         + tiles([("57%", "are investing in hybrid arrangements"),
                  ("55%", "are opening locations closer to where staff live")]), SRC_IWG),
    page("d", "Principle 3 - Built to be re-let", "5/6",
         '<h1>The fit-out <em>outlives the tenant.</em></h1>'
         '<div class="sub">When landlords and operators commission the fit-out, it has to be fast, branded for one client and easy to reconfigure for the next.</div>'
         f'<div class="art">{art_modules()}</div>', "Illustrative layout"),
    page("l", "What it means for projects", "6/6",
         '<h1 style="font-size:64px">Less commitment. <em>More fit-outs.</em></h1>'
         + '<div style="margin-top:36px">' + tiles([("Fast", "weeks, not months"), ("Branded", "the client's identity"), ("Modular", "ready for the next tenant")], cols=3, big=38, mb=0) + '</div>'
         '<div class="grow"></div><h1 style="font-size:84px;margin-bottom:20px">Would you sign a <em>10-year lease</em> today?</h1>'
         '<div class="sub" style="margin-top:0;margin-bottom:32px">Tell me how your company is deciding.</div>'),
]

SRC_DEL = "Source: Hospitality &amp; Real Estate Observatory, presented at AURA Florence, Oct 2026"
SRC_CWH = "Source: Cushman &amp; Wakefield, Hospitality MarketBeat Italy H1 2026"

C = [
    page("d", "AURA Florence - 27-29 Oct 2026", "1/6",
         '<h1 style="margin-top:40px">Over <em>80%</em> of luxury hotel operators want to invest in Italy next.</h1>'
         '<div class="sub">Share of operators\' preferences for luxury hotel investment over the next three years.</div>'
         f'<div class="art">{hbars([("Italy", 80, "80%+", True), ("Spain", 10, "10%", False), ("Greece", 4, "4%", False)], 85, True)}</div>'
         '<h1 style="font-size:58px;margin-bottom:28px">What does it take to <em>deliver them?</em></h1>', SRC_DEL),
    page("l", "The numbers behind it", "2/6",
         '<h1>Italy is <em>outrunning Europe.</em></h1>'
         '<div class="sub">Performance, capital and new five-star supply all point the same way.</div><div class="grow"></div>'
         + tiles([("+11.3%", "hotel RevPAR in Italy in H1 2026, vs +3.0% in Europe"),
                  ("EUR 1.3bn", "invested in Italian hotels in H1 2026, 53% above the 10-year average"),
                  ("+4.9%", "five-star hotels in 2025, the fastest growth in Europe"),
                  ("~1,000", "five-star hotels Italy could reach by 2030")]),
         "Sources: Cushman &amp; Wakefield, Hospitality MarketBeat Italy H1 2026; industry observatory presented at AURA, Oct 2026"),
    page("d", "Principle 1 - Reposition, don't build", "3/6",
         '<h1>More openings. <em>Almost no new rooms.</em></h1>'
         '<div class="sub">Over 80 hotels opened in Italy in H1 2026, yet supply grew only 0.2%. Growth comes from upgrading what exists.</div>'
         f'<div class="art">{art_stars()}</div>'
         + tiles([("35%", "of H1 2026 investment went to upscale hotels"), ("+127%", "upscale volume, year on year")], mb=28), SRC_CWH),
    page("l", "Principle 2 - Heritage is the product", "4/6",
         '<h1>The building <em>is the brand.</em></h1>'
         f'<div class="art">{art_arches()}</div>'
         '<div class="sub" style="margin-bottom:28px">Palazzi, monasteries and former offices become hotels. Every survey, permit and structural check shapes the programme.</div>',
         "Illustrative facade"),
    page("d", "Principle 3 - Deliver while open", "5/6",
         '<h1>In a hotel that never closes, <em>the programme is the design.</em></h1>'
         f'<div class="art">{art_gantt()}</div>'
         + tiles([("68% to 73%", "expected luxury occupancy, 2027 to 2029"), ("~EUR 1,186", "expected luxury average daily rate in 2029")], mb=28), SRC_DEL),
    page("l", "What it means for project teams", "6/6",
         '<h1 style="font-size:64px">Hospitality is no longer a niche. <em>It is core business.</em></h1>'
         + '<div style="margin-top:36px">' + tiles([("Upgrade", "4 stars to 5"), ("Heritage", "the building is the brand"), ("Phasing", "work while it stays open")], cols=3, big=38, mb=0) + '</div>'
         '<div class="grow"></div><h1 style="font-size:80px;margin-bottom:20px">What is the hardest part of a <em>luxury repositioning?</em></h1>'
         '<div class="sub" style="margin-top:0;margin-bottom:32px">Tell me from your projects.</div>'),
]

SETS = {"post02_office-mandates_v2": A, "post03_flex-after-ai": B, "post04_italy-luxury-hotels": C}


async def main():
    from PIL import Image
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg = await b.new_page(viewport={"width": 1080, "height": 1350})
        for name, slides in SETS.items():
            shots = []
            for i, h in enumerate(slides, 1):
                f = HTML / f"{name}_{i}.html"
                f.write_text(h, encoding="utf-8")
                await pg.goto(f.as_uri(), wait_until="networkidle")
                await pg.evaluate("document.fonts.ready")
                o = OUT / f"{name}_{i}.png"
                await pg.screenshot(path=str(o))
                shots.append(o)
            ims = [Image.open(s).convert("RGB") for s in shots]
            ims[0].save(OUT / f"{name}.pdf", save_all=True, append_images=ims[1:], resolution=150, quality=85)
            sheet = Image.new("RGB", (432 * 3, 540 * 2), "white")
            for i, im in enumerate(ims):
                sheet.paste(im.resize((432, 540)), ((i % 3) * 432, (i // 3) * 540))
            sheet.save(SCR + f"sheet_{name}.png")
        await b.close()


