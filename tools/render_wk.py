import asyncio, math
from playwright.async_api import async_playwright
from next_lib import *
from r2lib import art_street, art_facades

def art_portfolio():
    s = f'<svg width="912" height="300" viewBox="0 0 912 300">{glow("gp2")}'
    s += f'<rect x="0" y="60" width="640" height="130" fill="{CYAN}" fill-opacity=".85"/>'
    s += f'<rect x="652" y="60" width="260" height="130" fill="{LIME}" filter="url(#gp2)"/>'
    s += f'<text x="24" y="140" font-family="SG" font-weight="700" font-size="46" fill="#070B1A">CORE</text>'
    s += f'<text x="676" y="140" font-family="SG" font-weight="700" font-size="46" fill="#070B1A">FLEX</text>'
    s += f'<text x="0" y="240" font-family="JB" font-size="18" fill="#8C97B8" letter-spacing="2">LONG-TERM HQ</text>'
    s += f'<text x="652" y="240" font-family="JB" font-size="18" fill="#8C97B8" letter-spacing="2">CAPACITY THAT ADAPTS</text>'
    s += f'<text x="0" y="290" font-family="JB" font-size="15" fill="#56618A" letter-spacing="2">ILLUSTRATIVE SPLIT</text>'
    return s + '</svg>'

def art_courtyard():
    s = f'<svg width="760" height="384" viewBox="0 0 912 460">{glow("gc")}'
    s += f'<rect x="80" y="20" width="752" height="420" fill="none" stroke="{CYAN}" stroke-width="3"/>'
    s += f'<rect x="250" y="130" width="412" height="200" fill="{LIME}" filter="url(#gc)"/>'
    s += f'<text x="456" y="238" text-anchor="middle" font-family="SG" font-weight="700" font-size="40" fill="#070B1A">PUBLIC COURTYARD</text>'
    for x in (120, 700):
        for i in range(5):
            s += f'<rect x="{x}" y="{50+i*76}" width="92" height="44" fill="{CYAN}" fill-opacity=".25"/>'
    s += f'<rect x="420" y="410" width="72" height="30" fill="#070B1A" stroke="{LIME}" stroke-width="3"/>'
    s += f'<text x="456" y="400" text-anchor="middle" font-family="JB" font-size="16" fill="{LIME}" letter-spacing="2">OPEN BY DAY</text>'
    return s + '</svg>'

def art_citymap():
    s = f'<svg width="912" height="420" viewBox="0 0 912 420">{glow("gq")}'
    for r in range(4):
        for c in range(7):
            x, y = 10 + c*130, 10 + r*102
            s += f'<rect x="{x}" y="{y}" width="110" height="82" fill="{CYAN}" fill-opacity=".10" stroke="{CYAN}" stroke-opacity=".35" stroke-width="1.5"/>'
    s += f'<rect x="400" y="112" width="110" height="184" fill="{BLUE}"/>'
    s += f'<text x="455" y="212" text-anchor="middle" font-family="JB" font-size="16" fill="#FFFFFF" letter-spacing="2">OFFICE</text>'
    for (x, y, lab) in [(205, 60, "CAFE"), (720, 60, "GYM"), (180, 340, "PARK"), (720, 340, "HOTEL"), (590, 210, "THEATRE")]:
        s += f'<line x1="455" y1="204" x2="{x}" y2="{y}" stroke="{LIME}" stroke-width="2" stroke-dasharray="6 6"/>'
        s += f'<circle cx="{x}" cy="{y}" r="12" fill="{LIME}" filter="url(#gq)"/>'
        s += f'<text x="{x}" y="{y+36}" text-anchor="middle" font-family="JB" font-size="15" fill="{LIME}" letter-spacing="2">{lab}</text>'
    return s + '</svg>'

def art_meeting():
    s = '<svg width="912" height="420" viewBox="0 0 912 420">'
    s += f'<rect x="156" y="10" width="600" height="400" fill="none" stroke="{CYAN}" stroke-width="3"/>'
    s += f'<rect x="156" y="10" width="600" height="100" fill="{LIME}"/>'
    s += f'<text x="456" y="70" text-anchor="middle" font-family="SG" font-weight="700" font-size="34" fill="#070B1A">25%+ MEETING SPACE</text>'
    for r in range(3):
        for c in range(8):
            s += f'<rect x="{186+c*70}" y="{140+r*86}" width="44" height="40" fill="{CYAN}" fill-opacity=".3"/>'
    return s + '</svg>'

def art_skyline():
    s = f'<svg width="912" height="400" viewBox="0 0 912 400">{glow("gk")}'
    towers = [(10,120,140),(170,60,120),(310,170,150),(480,30,130),(630,140,110),(760,90,150)]
    lit = {(1,2),(3,1),(3,4),(5,3),(0,5),(2,2),(4,6),(1,7)}
    for i,(x,top,w) in enumerate(towers):
        s += f'<rect x="{x}" y="{top}" width="{w}" height="{390-top}" fill="none" stroke="{CYAN}" stroke-width="2.5"/>'
        for r in range(int((390-top-20)/34)):
            for c in range(int((w-20)/30)):
                on = (i*3+r+c) % 5 == 0
                s += f'<rect x="{x+12+c*30}" y="{top+14+r*34}" width="18" height="18" fill="{LIME if on else CYAN}" fill-opacity="{1 if on else .18}"/>'
    return s + '</svg>'

def art_shrink():
    s = '<svg width="912" height="360" viewBox="0 0 912 360">'
    for i in range(6):
        x = 10 + i*150
        gone = i in (1, 4)
        if gone:
            s += f'<rect x="{x}" y="60" width="120" height="280" fill="none" stroke="{CYAN}" stroke-opacity=".5" stroke-width="2" stroke-dasharray="8 7"/>'
            s += f'<text x="{x+60}" y="210" text-anchor="middle" font-family="JB" font-size="16" fill="{CYAN}" letter-spacing="2">OUT</text>'
        else:
            s += f'<rect x="{x}" y="{40+i%3*30}" width="120" height="{300-i%3*30}" fill="{CYAN}" fill-opacity=".85"/>'
    return s + '</svg>'

def art_convert():
    s = '<svg width="912" height="420" viewBox="0 0 912 420">'
    s += f'<rect x="40" y="20" width="300" height="390" fill="#FFFFFF" stroke="{INK}" stroke-width="3"/>'
    for i in range(8):
        s += f'<rect x="60" y="{40+i*46}" width="260" height="24" fill="{INK}" fill-opacity=".15"/>'
    s += f'<text x="190" y="12" text-anchor="middle" font-family="JB" font-size="16" fill="{MUT}" letter-spacing="2">OFFICE</text>'
    s += f'<path d="M380 215 H520" stroke="{BLUE}" stroke-width="5"/><path d="M500 195 L524 215 L500 235" fill="none" stroke="{BLUE}" stroke-width="5"/>'
    s += f'<rect x="572" y="20" width="300" height="390" fill="#FFFFFF" stroke="{BLUE}" stroke-width="3"/>'
    for r in range(8):
        for c in range(4):
            s += f'<rect x="{592+c*70}" y="{40+r*46}" width="46" height="28" fill="{BLUE if (r+c)%3 else CYAN}" fill-opacity=".7"/>'
    s += f'<text x="722" y="12" text-anchor="middle" font-family="JB" font-size="16" fill="{BLUE}" letter-spacing="2">HOMES</text>'
    return s + '</svg>'

# --- flex v3: only slides 1 and 6 change ---
B3 = list(B)
B3[0] = page("d", "Workplace strategy - Nov 2026", "1/6",
    '<h1 style="margin-top:40px">Not lease <em>or</em> flex. <em>How much of each.</em></h1>'
    '<div class="sub">Flex operators signed a record 728 new locations in H1 2026, 95% of them in partnership with landlords. Flex is becoming part of the building.</div>'
    f'<div class="art">{art_portfolio()}</div>'
    '<h1 style="font-size:58px;margin-bottom:28px">Where does your company <em>draw the line?</em></h1>', "Source: IWG via Allwork.Space, Oct 2026")
B3[5] = page("l", "What it means for occupiers", "6/6",
    '<h1 style="font-size:64px">Commit where you are sure. <em>Flex where you are not.</em></h1>'
    + '<div style="margin-top:36px">' + tiles([("Core", "a long-term HQ that carries the brand"), ("Flex", "capacity that follows the business"), ("Adapt", "fit-outs ready to change")], cols=3, big=38, mb=0) + '</div>'
    '<div class="grow"></div><h1 style="font-size:84px;margin-bottom:20px">How much of your portfolio <em>should be flexible?</em></h1>'
    '<div class="sub" style="margin-top:0;margin-bottom:32px">Tell me how your company is deciding.</div>')

SRC_ORS = "Source: ANSA and Italpress, 4 Nov 2026"
SRC_FO = "Source: Cushman &amp; Wakefield, Office Fit Out Cost Guide EMEA 2026"
M = [
  page("d", "Milan - 4 Nov 2026", "1/6",
    '<h1 style="margin-top:40px">Milan just opened an office <em>with a public courtyard.</em></h1>'
    '<div class="sub">Orsole 4 in the Cinque Vie: eight floors rebuilt in almost three years, next to the Roman theatre, courtyard open to the public by day.</div>'
    f'<div class="art">{art_courtyard()}</div>'
    '<h1 style="font-size:58px;margin-bottom:28px">What deserves a <em>prime square metre?</em></h1>', SRC_ORS),
  page("l", "Same week, two signals", "2/6",
    '<h1>The best offices <em>open onto the city.</em></h1>'
    '<div class="sub">A landmark office opened its doors, while the cost of prime space kept rising.</div><div class="grow"></div>'
    + tiles([("8 floors", "rebuilt at Orsole 4 in almost three years"), ("+4.7%", "prime office occupier costs in a year, across 47 cities"),
             ("26%", "of the working week spent neither in the office nor at home"), ("EUR 1,250", "per sq m, a medium-spec fit-out in Milan")]),
    "Sources: ANSA, 4 Nov 2026; office occupier cost research via Allwork.Space, 6 Nov 2026; Gensler Global Workplace Survey 2026; Cushman &amp; Wakefield Fit Out Cost Guide 2026"),
  page("d", "Principle 1 - Borrow the city", "3/6",
    '<h1>The café, the gym, the hotel lobby: <em>already next door.</em></h1>'
    f'<div class="art">{art_citymap()}</div>'
    + tiles([("26%", "of the working week is spent in third places, neither office nor home")], cols=1), "Source: Gensler Global Workplace Survey 2026"),
  page("l", "Principle 2 - Invest where it counts", "4/6",
    '<h1>Every square metre <em>has to earn its place.</em></h1>'
    f'<div class="art">{art_street()}</div>'
    + tiles([("EUR 1,250", "per sq m for a medium-spec fit-out in Milan"), ("+4.7%", "prime occupier costs in a year")]),
    "Sources: Cushman &amp; Wakefield Fit Out Cost Guide 2026; office occupier cost research, Q3 2026"),
  page("d", "Principle 3 - Rooms for people", "5/6",
    '<h1>What only the office can do: <em>bring people together.</em></h1>'
    f'<div class="art">{art_meeting()}</div>'
    '<div class="sub" style="margin-bottom:28px">High-spec fit-outs now give more than a quarter of the floor to meeting and collaboration space.</div>', SRC_FO),
  page("l", "What it means for the office", "6/6",
    '<h1 style="font-size:64px">Don\'t build the city inside. <em>Open the door to it.</em></h1>'
    + '<div style="margin-top:36px">' + tiles([("Open", "connected to its street"), ("Invest", "where only the office delivers"), ("Gather", "space for people, not desks")], cols=3, big=38, mb=0) + '</div>'
    '<div class="grow"></div><h1 style="font-size:80px;margin-bottom:20px">What would you keep inside, and <em>what would you leave to the city?</em></h1>'
    '<div class="sub" style="margin-top:0;margin-bottom:32px">Tell me how your office does it.</div>'),
]

SRC_NY = "Source: Manhattan leasing data via Commercial Observer, 2 Nov 2026"
SRC_TRD = "Source: The Real Deal, 8 Nov 2026"
SRC_US = "Source: Cushman &amp; Wakefield, U.S. Office MarketBeat Q3 2026"
U = [
  page("d", "Manhattan - October 2026", "1/6",
    '<h1 style="margin-top:40px">Manhattan office leasing <em>jumped 54%</em> in a month.</h1>'
    '<div class="sub">Availability fell to 12.3%, the tightest since August 2020. 2026 is on pace for the busiest year since 2000.</div>'
    f'<div class="art">{art_skyline()}</div>'
    '<h1 style="font-size:58px;margin-bottom:28px">Recovering, or <em>being sorted?</em></h1>', SRC_NY),
  page("l", "The other half of the story", "2/6",
    '<h1>Fewer offices. <em>Fuller offices.</em></h1>'
    '<div class="sub">Demand is coming back to a smaller, better stock.</div><div class="grow"></div>'
    + tiles([("+54%", "Manhattan leasing in October vs September"), ("12.3%", "Manhattan availability, lowest since 2020"),
             ("-42.5m sq ft", "US office inventory in six quarters"), ("~1/5", "of the usual new supply delivered in 2026")]),
    "Sources: Commercial Observer, 2 Nov 2026; Cushman &amp; Wakefield, U.S. Office MarketBeat Q3 2026"),
  page("d", "Principle 1 - Fewer buildings", "3/6",
    '<h1>Obsolete stock <em>is leaving the market.</em></h1>'
    f'<div class="art">{art_shrink()}</div>'
    + tiles([("42.5m sq ft", "removed from US office inventory in six quarters")], cols=1), SRC_US),
  page("l", "Principle 2 - Second lives", "4/6",
    '<h1>Yesterday\'s offices, <em>tomorrow\'s homes.</em></h1>'
    f'<div class="art">{art_convert()}</div>'
    + tiles([("13", "Manhattan conversion projects"), ("11,000+", "apartments from 7m sq ft of offices")]), SRC_TRD),
  page("d", "Principle 3 - The race moves inside", "5/6",
    '<h1>Almost nothing new. <em>Everything gets fitted out.</em></h1>'
    f'<div class="art">{hbars([("Delivered, Jan-Sep 2026", 20, "~1/5", True), ("Historical average", 100, "100%", False)], 100, True)}</div>'
    + tiles([("7.1m sq ft", "new US office space in nine months"), ("$90+", "per sq ft fit-out allowances in Manhattan, a record")], mb=28),
    "Sources: Cushman &amp; Wakefield, U.S. Office MarketBeat Q3 2026; The Real Deal, 8 Nov 2026"),
  page("l", "What it means for project teams", "6/6",
    '<h1 style="font-size:64px">The market is not full. <em>It is selective.</em></h1>'
    + '<div style="margin-top:36px">' + tiles([("Fewer", "obsolete stock leaves"), ("Converted", "second lives as homes"), ("Fitted out", "the race for quality")], cols=3, big=38, mb=0) + '</div>'
    '<div class="grow"></div><h1 style="font-size:84px;margin-bottom:20px">Is your city <em>sorting its offices</em> the same way?</h1>'
    '<div class="sub" style="margin-top:0;margin-bottom:32px">Tell me what you see.</div>'),
]

WK = {"post03_flex-core-plus-flex": B3, "post04_italy-luxury-hotels_v2": C, "post05_milan-open-office": M, "post06_us-offices-sorted": U}

async def run():
    from PIL import Image
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg = await b.new_page(viewport={"width": 1080, "height": 1350})
        for name, slides in WK.items():
            shots = []
            for i, h in enumerate(slides, 1):
                f = HTML / f"{name}_{i}.html"; f.write_text(h, encoding="utf-8")
                await pg.goto(f.as_uri(), wait_until="networkidle"); await pg.evaluate("document.fonts.ready")
                o = OUT / f"{name}_{i}.png"; await pg.screenshot(path=str(o)); shots.append(o)
            ims = [Image.open(s).convert("RGB") for s in shots]
            ims[0].save(OUT / f"{name}.pdf", save_all=True, append_images=ims[1:], resolution=150, quality=85)
            sh = Image.new("RGB", (432*3, 540*2), "white")
            for i, im in enumerate(ims): sh.paste(im.resize((432, 540)), ((i % 3)*432, (i//3)*540))
            sh.save(SCR + f"sheet_{name}.png")
        await b.close()

asyncio.run(run())
