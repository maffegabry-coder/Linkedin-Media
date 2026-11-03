import asyncio, math
from pathlib import Path
from playwright.async_api import async_playwright
from r2lib import page, hbars, art_rings, art_facades, BLUE, CYAN, LIME, HTML
OUT = Path(__file__).parent / "out_ai"; OUT.mkdir(exist_ok=True)

def art_people():
    # four silhouettes, the last one an empty dashed outline (1 in 4)
    s = '<svg width="912" height="400" viewBox="0 0 912 400"><defs><filter id="gp" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="8" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>'
    for i in range(4):
        cx = 114 + i*228
        head = f'<circle cx="{cx}" cy="110" r="58"/>'
        body = f'<path d="M{cx-98} 380 C{cx-98} 250 {cx-60} 196 {cx} 196 C{cx+60} 196 {cx+98} 250 {cx+98} 380 Z"/>'
        if i < 3:
            s += f'<g fill="{CYAN}" filter="url(#gp)">{head}{body}</g>'
        else:
            s += f'<g fill="none" stroke="{LIME}" stroke-width="3" stroke-dasharray="10 8">{head}{body}</g>'
    return s + '</svg>'

def art_dc():
    # data centre hall: racks with power lines
    s = '<svg width="912" height="420" viewBox="0 0 912 420"><defs><filter id="gd"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>'
    s += f'<rect x="20" y="40" width="872" height="340" fill="none" stroke="{BLUE}" stroke-width="3"/>'
    for i in range(8):
        x = 60 + i*104
        s += f'<rect x="{x}" y="90" width="60" height="230" fill="#FFFFFF" stroke="#0A1230" stroke-width="2.5"/>'
        for j in range(9):
            s += f'<rect x="{x+10}" y="{104+j*24}" width="40" height="10" fill="{BLUE if (i+j)%3 else CYAN}"/>'
    s += f'<path d="M20 20 H892" stroke="{BLUE}" stroke-width="3" stroke-dasharray="12 8"/>'
    s += f'<text x="20" y="408" font-family="JB" font-size="18" fill="#56618A" letter-spacing="2">POWER FIRST, THEN SPACE</text>'
    return s + '</svg>'

SRC_MS = "Source: CBS News, 26 Oct 2026. Microsoft headcount 223,000 (June 2026)"
SRC_AMZ = "Sources: Puget Sound Business Journal via KIRO 7, Mar 2026; Challenger, Gray &amp; Christmas via Outlook Business, Aug 2026"
SRC_CW = "Source: Cushman &amp; Wakefield, European Office Update, Mar 2026"
SRC_CBD = "Source: European office market research, Q1 2026 (13 CBD markets)"
SRC_MSCI = "Source: MSCI Real Capital Analytics, Aug 2026 (CBD deals above EUR 5m)"
SRC_DC = "Source: Cushman &amp; Wakefield, EMEA Data Centre update, H1 2026"

C = [
  page("d", "AI x Workplace", "1/6",
    '<h1 style="margin-top:40px">Microsoft just offered<br><em>60,000 people</em> a way out.</h1>'
    '<div class="sub">About 1 in 4 employees, while it plans <b>$175bn</b> of AI infrastructure spend in 2026.</div>'
    f'<div class="art">{art_people()}</div>'
    '<h1 style="font-size:58px;margin-bottom:28px">What does it mean for <em>Grade A offices?</em></h1>', SRC_MS),
  page("l", "Not only Microsoft", "2/6",
    '<h1>Fewer people, fewer desks.<br><em>Better buildings.</em></h1>'
    '<div class="sub">Big tech is funding AI by trimming headcount, yet the best offices keep filling up.</div><div class="grow"></div>'
    '<div class="stats" style="grid-template-columns:1fr 1fr;gap:16px;margin-bottom:32px">'
    '<div class="st"><div class="v">49,000</div><div class="k">desks Amazon plans to cut in 2026</div></div>'
    '<div class="st"><div class="v">~88,000</div><div class="k">US job losses in 2026 linked to AI</div></div>'
    '<div class="st"><div class="v">52%</div><div class="k">of 2025 European leasing was Grade A, a record</div></div>'
    '<div class="st"><div class="v">3.5%</div><div class="k">vacancy left in Grade A buildings</div></div></div>',
    "Sources: Puget Sound Business Journal via KIRO 7; Challenger, Gray &amp; Christmas; Cushman &amp; Wakefield, European Office Update, Mar 2026"),
  page("l", "Principle 1 - Smaller and central", "3/6",
    '<h1>The centre fills up.<br><em>The edge empties.</em></h1>'
    f'<div class="art">{art_rings()}</div>', SRC_CBD),
  page("d", "Principle 2 - Mixed use and conversion", "4/6",
    '<h1>Offices are becoming <em>hotels and homes.</em></h1>'
    f'<div class="art">{art_facades()}</div>'
    '<div class="stats" style="margin-bottom:28px"><div class="st"><div class="v">17%</div><div class="k">of CBD office purchases in H1 2026 were for conversion</div></div>'
    '<div class="st"><div class="v">14 yrs</div><div class="k">highest share since 2012; 12% in 2022</div></div>'
    '<div class="st"><div class="v">70%+</div><div class="k">of known conversions go to homes and hotels</div></div></div>', SRC_MSCI),
  page("l", "Principle 3 - The building AI needs", "5/6",
    '<h1>The AI boom is <em>a power boom.</em></h1>'
    f'<div class="art">{art_dc()}</div>'
    '<div class="stats" style="margin-bottom:28px"><div class="st"><div class="v">12.1 GW</div><div class="k">data centre capacity live in EMEA, H1 2026</div></div>'
    '<div class="st"><div class="v">18.3 GW</div><div class="k">in construction or planning</div></div>'
    '<div class="st"><div class="v">+34%</div><div class="k">pipeline growth, year on year</div></div></div>', SRC_DC),
  page("d", "What it means for Grade A", "6/6",
    '<h1 style="font-size:64px">Fewer desks. <em>Higher stakes per square metre.</em></h1>'
    '<div class="stats" style="grid-template-columns:repeat(4,1fr);gap:12px;margin-top:40px">'
    '<div class="st" style="padding:20px 16px"><div class="v" style="font-size:28px">Smaller</div><div class="k" style="font-size:17px">sized to real attendance</div></div>'
    '<div class="st" style="padding:20px 16px"><div class="v" style="font-size:28px">Central</div><div class="k" style="font-size:17px">close to transport and clients</div></div>'
    '<div class="st" style="padding:20px 16px"><div class="v" style="font-size:28px">Mixed use</div><div class="k" style="font-size:17px">office, hotel, homes together</div></div>'
    '<div class="st" style="padding:20px 16px"><div class="v" style="font-size:28px">Convertible</div><div class="k" style="font-size:17px">ready for a second life</div></div></div>'
    '<div class="grow"></div><h1 style="font-size:84px;margin-bottom:20px">Will AI shrink Grade A offices, or make them <em>more valuable?</em></h1>'
    '<div class="sub" style="margin-top:0;margin-bottom:32px">Tell me what you see in your market.</div>'),
]

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg = await b.new_page(viewport={"width": 1080, "height": 1350})
        shots = []
        for i, h in enumerate(C, 1):
            f = HTML / f"ai_slide{i}.html"; f.write_text(h, encoding="utf-8")
            await pg.goto(f.as_uri(), wait_until="networkidle"); await pg.evaluate("document.fonts.ready")
            o = OUT / f"ai_slide{i}.png"; await pg.screenshot(path=str(o)); shots.append(o)
        await b.close()
    from PIL import Image
    ims = [Image.open(s).convert("RGB") for s in shots]
    ims[0].save(OUT / "post01_ai-and-offices.pdf", save_all=True, append_images=ims[1:], resolution=150, quality=85)
    sheet = Image.new("RGB", (432*3, 540*2), "white")
    for i, im in enumerate(ims): sheet.paste(im.resize((432,540)), ((i%3)*432, (i//3)*540))
    sheet.save("/tmp/claude-0/-home-claude/3116edaa-2b55-58f6-9d21-13d8e709f5e9/scratchpad/ai_sheet.png")

asyncio.run(main())
