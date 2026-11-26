#!/usr/bin/env python3
"""Draw the news-image-20261126 poster: 'THE WORLD IN ONE DAY / THURSDAY, 26 NOVEMBER 2026'.

A dense front page, 1024x1024 PNG, drawn entirely with PIL (no photos).
43 verified dated stories across 9 sections, all checked against Reuters/AP
or other reputable sources on the morning of 26 Nov 2026:

LEAD (trade/markets):
  1. Trump proposes sweeping new tariffs on 14 partners under Section 301
     (20% on China) plus a surprise 10% duty on finished Brazilian
     aircraft - Reuters / WSJ
  2. Markets tumble then partly recover before Thanksgiving: Nasdaq -0.62%
     (was -4% intraday), S&P 500 -0.25%, Dow +0.33% - Reuters
  3. Nvidia -3.91% (shed 8%+ intraday); S&P puts Nvidia on downgrade watch
     over board oversight after Huang's departure/reinstatement - Reuters
  4. US inflation (PCE) 3.8% in Oct, nearly double the Fed's 2% target;
     traders price ~97% chance of a Dec Fed rate hike - Reuters
  5. US Q3 GDP revised sharply higher - Reuters
  6. US consumer confidence highest in nearly 2 years - Reuters
  7. Trump blames the midterm results for the slide: "I wasn't on the
     ballot" (Truth Social) - Reuters
  8. Brent crude +3.5% to $94.61 after Houthis say they attacked Saudi
     Arabia's largest refinery (Ras Tanura) - Reuters
  9. Bitcoin ~$60,030 - Reuters

NORTH AMERICA:
 10. Macy's Thanksgiving Day Parade postponed to Saturday (storm forecasts)
 11. Trump pardons turkeys Freedom and Feathers
 12. Second judge blocks Trump's birthright-citizenship order
 13. Nidal Hasan asks judge to stay his execution (Fort Hood, 13 killed 2009)
 14. CDC: nine measles-related deaths in the US in 2026
 15. Radar issue delays flights at Chicago O'Hare
 16. US Army detonates explosives cache in Iowa after public outcry
LATIN AMERICA:
 17. Ecuador minister says talks with US Def. Sec. Hegseth focused on
     reviewing operations in the country
WESTERN EUROPE:
 18. UK moves military aircraft to hangars at night over drone threats
 19. Italy: 57 priests jailed for child sex abuse 2001-2021, 880 incidents
 20. Duran Duran guitarist Andy Taylor dies at 65 (metastatic prostate cancer)
UKRAINE & RUSSIA:
 21. Russia hits Kyiv with ballistic missiles - shopping centre + two
     buildings; Naftogaz gas site in Poltava; energy/gas infrastructure
     damaged in five regions, power cuts
 22. Ukraine strikes Savasleyka air base in Russia, damaging five planes
 23. US approves possible $622m F-16 equipment sale to Ukraine
 24. 34 countries + EU call on Russia to halt alleged riot-agent (tear gas)
     use; OPCW confirmed traces
 25. Murmansk governor Andrei Chibis placed in pre-trial detention on
     corruption charges
 26. Trump shelves plan to use business deals with Russia to end the war (FT)
 27. Hungary PM Peter Magyar visits Kyiv, hails "fresh start" with Ukraine
 28. Nine more Ukrainian children reunited with families (total 43, Melania
     Trump initiative)
EU & NATO:
 29. Germany's Merz warns Russia targets outer space (BND: nuclear-armed
     satellite may launch in December); EU summit 26-27 Nov on 45bn euro
     Ukraine loan
 30. EU proposes 22nd sanctions package against Russia
 31. NATO chief calls on Europe to brace for a major military confrontation
MIDDLE EAST:
 32. Israeli strike in Gaza kills Hamas official Mohammad Abuelouf, his wife
     and two children
 33. Israeli judges recommend dropping one Netanyahu bribery case
 34. Iran says prepared to withstand US blockade; US tells citizens to
     leave Iran
 35. Lebanon to open second airport (Kleiat) next month; Hezbollah sway
     diminished
AFRICA:
 36. Sudan: RSF drone strikes kill 19 civilians in Blue Nile state (Damazin)
 37. Nigeria: suspected militants kill at least 30 in Niger state; Tinubu
     vows peace in Maiduguri; Nigeria seizes $227m of meth, arrests five
     Mexicans
 38. Kenya cult leader Paul Mackenzie convicted of new charges (serving
     200-year sentence)
EAST ASIA:
 39. North Korea's Kim calls for wider deployment of tactical nuclear
     weapons (KCNA, Thu 26 Nov)
 40. Shanghai party chief Chen Jining under corruption probe (26 Nov)
 41. Reuters explainer: how China got access to Nvidia AI chips despite US
     rules; money trail links Alice Huang-connected firms to AI servers
SOUTH ASIA & PACIFIC:
 42. Solomon Islands names Australia primary security partner in treaty
     signed 25 Nov, rules out foreign military bases
 43. Indonesia: Cikande factory fire - 24 body bags recovered, search
     continues (26 Nov update)

Sources: Reuters, AP, Financial Times, KCNA.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (17, 17, 17)
RED = (176, 42, 30)
BLUE = (31, 78, 121)
GRAY = (85, 85, 85)
LIGHT = (233, 227, 214)
ORANGE = (240, 140, 20)
GOLD = (240, 200, 40)
CYAN = (90, 180, 220)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap_text(text, fnt, max_w):
    """Greedy word wrap using font metrics only (no draw object needed)."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
        for w in words:
            trial = (cur + " " + w).strip()
            if fnt.getlength(trial) <= max_w:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines


def hrule(draw, x0, x1, y, w=3, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=w)


# ---------------------------------------------------------------- scenes
# Lead panel scenes (taller boxes) and band scenes (compact ~146x32 boxes).

def draw_chart_fall(draw, x, y, w, h):
    # falling stock chart: axes, gridlines, steep falling line, arrow
    ox, oy = x + 12, y + h - 24
    top = y + 30
    right = x + w - 12
    for gy in (oy - 40, oy - 80):
        draw.line([(ox, gy), (right, gy)], fill=(200, 194, 178), width=1)
    draw.line([(ox, top), (ox, oy)], fill=GRAY, width=2)
    draw.line([(ox, oy), (right, oy)], fill=GRAY, width=2)
    pts = [(ox, oy - 88), (ox + 55, oy - 84), (ox + 110, oy - 88),
           (ox + 165, oy - 55), (ox + 220, oy - 28), (ox + 268, oy - 6)]
    draw.line(pts, fill=RED, width=5, joint="curve")
    ex, ey = pts[-1]
    draw.polygon([(ex, ey + 13), (ex + 15, ey - 2), (ex - 2, ey - 2)], fill=RED)
    draw.text((x + 14, y + 4), "-4% intraday", font=font(SANS_B, 20), fill=RED)
    f_nas = font(SANS_B, 15)
    nas = "Nasdaq -0.62%"
    draw.text((x + 14, oy + 5), nas, font=f_nas, fill=INK)


def draw_chip(draw, x, y, w, h):
    # AI chip: dark square, pins, circuit traces, "AI" label
    cx, cy = x + w // 2, y + h // 2
    s = 52
    for i in range(4):
        px = x + 22 + i * 30
        draw.line([(px, y + 2), (px, y + 12)], fill=GRAY, width=3)
        draw.line([(px, y + h - 12), (px, y + h - 2)], fill=GRAY, width=3)
        py = y + 12 + i * 12
        draw.line([(x + 2, py), (x + 12, py)], fill=GRAY, width=3)
        draw.line([(x + w - 12, py), (x + w - 2, py)], fill=GRAY, width=3)
    draw.rectangle([cx - s // 2, cy - s // 2, cx + s // 2, cy + s // 2],
                   fill=(30, 34, 40), outline=INK, width=2)
    draw.rectangle([cx - s // 2 + 7, cy - s // 2 + 7, cx + s // 2 - 7,
                    cy + s // 2 - 7], outline=CYAN, width=1)
    f_ai = font(SANS_B, 20)
    t = "AI"
    draw.text((cx - draw.textlength(t, font=f_ai) / 2, cy - 12), t,
              font=f_ai, fill=CYAN)
    draw.line([(x + 14, y + h - 8), (x + 40, y + h - 8), (x + 40, cy + s // 2)],
              fill=CYAN, width=2)
    draw.line([(x + w - 14, y + 8), (x + w - 40, y + 8), (x + w - 40, cy - s // 2)],
              fill=CYAN, width=2)


def draw_blast(draw, x, y, w, h):
    # Kyiv: low buildings, orange blast starburst, smoke
    base = y + h - 2
    draw.rectangle([x + 6, base - 14, x + 30, base], fill=(70, 70, 78))
    draw.rectangle([x + 36, base - 20, x + 58, base], fill=(96, 96, 104))
    draw.rectangle([x + 64, base - 11, x + 88, base], fill=(70, 70, 78))
    cx, cy = x + 112, y + 12
    for (dx, dy) in ((-11, -6), (0, -11), (11, -6), (-12, 4), (12, 4), (0, 9)):
        draw.line([(cx, cy), (cx + dx, cy + dy)], fill=ORANGE, width=3)
    draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=GOLD)
    draw.ellipse([x + 96, y + 2, x + 108, y + 10], fill=GRAY)


def draw_airbase(draw, x, y, w, h):
    # Savasleyka: runway, small plane, blast
    base = y + h - 4
    draw.line([(x + 4, base), (x + w - 4, base)], fill=GRAY, width=3)
    for dx in range(10, w - 10, 20):
        draw.line([(x + dx, base), (x + dx + 9, base)], fill=(255, 255, 255),
                  width=2)
    px, py = x + 52, y + 12
    draw.polygon([(px, py - 8), (px + 6, py + 6), (px, py + 3),
                  (px - 6, py + 6)], fill=(60, 64, 70))
    draw.polygon([(px - 5, py + 1), (px - 14, py + 8), (px - 5, py + 5)],
                 fill=(60, 64, 70))
    draw.polygon([(px + 5, py + 1), (px + 14, py + 8), (px + 5, py + 5)],
                 fill=(60, 64, 70))
    cx, cy = x + 118, y + 10
    for (dx, dy) in ((-8, -5), (0, -8), (8, -5), (-8, 5), (8, 5)):
        draw.line([(cx, cy), (cx + dx, cy + dy)], fill=ORANGE, width=3)
    draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=GOLD)


def draw_turkey(draw, x, y, w, h):
    # pardoned turkey: feather fan, body, head
    cx = x + w // 2
    base = y + h - 2
    for (fx, fy, col) in ((cx - 26, y + 10, (150, 90, 40)),
                          (cx - 13, y + 5, RED),
                          (cx, y + 3, (150, 90, 40)),
                          (cx + 13, y + 5, RED),
                          (cx + 26, y + 10, (150, 90, 40))):
        draw.ellipse([fx - 7, fy - 8, fx + 7, fy + 8], fill=col)
    draw.ellipse([cx - 16, base - 14, cx + 16, base - 2], fill=(120, 72, 32))
    draw.ellipse([cx + 10, base - 22, cx + 24, base - 10], fill=(150, 100, 60))
    draw.polygon([(cx + 23, base - 16), (cx + 31, base - 13), (cx + 23, base - 12)],
                 fill=GOLD)
    draw.ellipse([cx + 15, base - 19, cx + 18, base - 16], fill=INK)


def draw_balloon(draw, x, y, w, h):
    # Macy's parade balloon: rounded balloon, ropes, crowd dots
    cx = x + w // 2
    base = y + h - 2
    draw.ellipse([cx - 24, y + 1, cx + 24, y + 24], fill=RED, outline=INK, width=1)
    draw.ellipse([cx - 24, y + 1, cx - 6, y + 24], fill=(210, 80, 70))
    draw.ellipse([cx - 5, y + 8, cx + 1, y + 14], fill=INK)
    draw.ellipse([cx + 9, y + 8, cx + 15, y + 14], fill=INK)
    draw.arc([cx - 9, y + 15, cx + 9, y + 23], 0, 180, fill=INK, width=2)
    draw.line([(cx - 14, y + 24), (cx - 18, base)], fill=GRAY, width=2)
    draw.line([(cx + 14, y + 24), (cx + 18, base)], fill=GRAY, width=2)
    for dx in (-26, -9, 9, 26):
        draw.ellipse([cx + dx - 3, base - 5, cx + dx + 3, base + 1], fill=BLUE)


def draw_missile(draw, x, y, w, h):
    # North Korea missile: rising rocket on a flame trail, stars
    for (sx, sy) in ((x + 10, y + 4), (x + w - 14, y + 8), (x + 26, y + 2)):
        draw.ellipse([sx, sy, sx + 3, sy + 3], fill=GRAY)
    cx = x + w // 2
    base = y + h - 2
    draw.polygon([(cx - 4, base - 22), (cx, base - 32), (cx + 4, base - 22)],
                 fill=(220, 220, 220), outline=INK)
    draw.rectangle([cx - 4, base - 22, cx + 4, base - 13], fill=RED)
    draw.polygon([(cx - 4, base - 13), (cx - 10, base - 6), (cx - 4, base - 6)],
                 fill=RED)
    draw.polygon([(cx + 4, base - 13), (cx + 10, base - 6), (cx + 4, base - 6)],
                 fill=RED)
    draw.polygon([(cx - 3, base - 13), (cx, base - 2), (cx + 3, base - 13)],
                 fill=ORANGE)
    draw.line([(x + 6, base), (x + w - 6, base)], fill=GRAY, width=2)


def draw_gaza(draw, x, y, w, h):
    # Gaza skyline: buildings, lit windows, smoke plume
    base = y + h - 2
    for (bx, bw, bh) in ((x + 6, 24, 16), (x + 36, 20, 24), (x + 62, 28, 13),
                         (x + 96, 22, 20)):
        draw.rectangle([bx, base - bh, bx + bw, base], fill=(96, 96, 104))
        draw.rectangle([bx + 5, base - bh + 4, bx + 9, base - bh + 8], fill=GOLD)
        draw.rectangle([bx + bw - 9, base - 8, bx + bw - 5, base - 4], fill=GOLD)
    cx, cy = x + 46, y + 8
    draw.ellipse([cx - 10, cy - 4, cx + 2, cy + 6], fill=GRAY)
    draw.ellipse([cx - 4, cy - 8, cx + 8, cy], fill=(120, 120, 120))
    draw.ellipse([cx - 3, cy - 1, cx + 3, cy + 5], fill=ORANGE)


# ---------------------------------------------------------------- content
LEAD_BODY = (
    "Trump proposed sweeping new tariffs on 14 partners under Section 301 "
    "- 20% on China - plus a surprise 10% duty on Brazilian aircraft. "
    "Stocks tumbled, then partly recovered: the Nasdaq fell 0.62%, the "
    "S&P 500 0.25%; the Dow rose 0.33%. Nvidia slid 3.91% and drew a "
    "downgrade watch. October inflation printed 3.8%, nearly double the "
    "Fed's target; traders price a ~97% chance of a December hike. Brent "
    "rose 3.5% to $94.61 after Houthi strikes on Saudi Arabia's biggest "
    "refinery."
)

STRIP_1 = ("NASDAQ -0.62%  \u00b7  S&P 500 -0.25%  \u00b7  DOW +0.33%  \u00b7  "
           "NVIDIA -3.91%  \u00b7  BRENT $94.61 +3.5%  \u00b7  "
           "BITCOIN ~$60,030  \u00b7  10-YR 4.84%")
STRIP_2 = ("Q3 GDP REVISED SHARPLY HIGHER  \u00b7  CONSUMER CONFIDENCE NEAR "
           "2-YEAR HIGH  \u00b7  TRUMP: \u201cI WASN\u2019T ON THE BALLOT\u201d")

BAND = [
    ("KYIV HIT", draw_blast),
    ("SAVASLEYKA", draw_airbase),
    ("TURKEY PARDON", draw_turkey),
    ("MACY'S BALLOON", draw_balloon),
    ("N. KOREA MISSILE", draw_missile),
    ("GAZA STRIKE", draw_gaza),
]

# (section header, [(date tag, text), ...]) per column
COLUMNS = [
    [
        ("NORTH AMERICA", [
            ("26 NOV", "Macy's Thanksgiving Day Parade postponed to Saturday as storms loom."),
            ("26 NOV", "Trump pardons turkeys Freedom and Feathers at the White House."),
            ("26 NOV", "Second judge blocks Trump's birthright-citizenship order."),
            ("26 NOV", "Fort Hood gunman Nidal Hasan asks judge to stay his execution."),
            ("26 NOV", "CDC counts nine measles-related deaths in the US this year."),
            ("26 NOV", "Radar outage delays flights at Chicago O'Hare."),
            ("26 NOV", "Army detonates Iowa explosives cache after public outcry."),
        ]),
        ("LATIN AMERICA", [
            ("26 NOV", "Ecuador talks with US defence chief Hegseth on operations review."),
        ]),
        ("WESTERN EUROPE", [
            ("26 NOV", "UK moves military jets into hangars at night over drone threats."),
            ("26 NOV", "Italy: 57 priests jailed for child sex abuse, 2001-2021."),
            ("26 NOV", "Duran Duran guitarist Andy Taylor dies at 65."),
        ]),
    ],
    [
        ("UKRAINE & RUSSIA", [
            ("26 NOV", "Russia hits Kyiv with ballistic missiles; gas sites struck in five regions."),
            ("26 NOV", "Ukraine strikes Savasleyka air base, damaging five planes."),
            ("26 NOV", "US approves possible $622m F-16 equipment sale to Ukraine."),
            ("26 NOV", "34 countries and EU urge Russia to halt alleged tear-gas use."),
            ("26 NOV", "Murmansk governor Chibis held in pre-trial detention on graft charges."),
            ("26 NOV", "Trump shelves plan to use Russia business deals to end the war."),
            ("26 NOV", "Hungary's Magyar visits Kyiv, hails a 'fresh start' with Ukraine."),
            ("26 NOV", "Nine more Ukrainian children reunited with families; total now 43."),
        ]),
        ("EU & NATO", [
            ("26 NOV", "Merz warns Russia targets outer space; EU summit weighs 45bn euro Ukraine loan."),
            ("26 NOV", "EU proposes 22nd sanctions package against Russia."),
            ("26 NOV", "NATO chief tells Europe to brace for major military confrontation."),
        ]),
    ],
    [
        ("MIDDLE EAST", [
            ("26 NOV", "Israeli strike in Gaza kills Hamas official Abuelouf, wife and two children."),
            ("26 NOV", "Judges urge dropping one Netanyahu bribery case."),
            ("26 NOV", "Iran says it can withstand US blockade; US tells citizens to leave."),
            ("26 NOV", "Lebanon to open second airport at Kleiat next month."),
        ]),
        ("AFRICA", [
            ("26 NOV", "Sudan: RSF drone strikes kill 19 civilians in Blue Nile state."),
            ("26 NOV", "Nigeria: militants kill at least 30 in Niger state; $227m meth seized."),
            ("26 NOV", "Kenya cult leader Mackenzie convicted of new charges."),
        ]),
        ("EAST ASIA", [
            ("26 NOV", "Kim calls for wider deployment of tactical nuclear weapons."),
            ("26 NOV", "Shanghai party chief Chen Jining under corruption probe."),
            ("26 NOV", "How China got Nvidia AI chips despite US rules, Reuters finds."),
        ]),
        ("SOUTH ASIA & PACIFIC", [
            ("25 NOV", "Solomon Islands names Australia top security partner; no foreign bases."),
            ("26 NOV", "Cikande factory fire: 24 body bags recovered, search goes on."),
        ]),
    ],
]

COL_X = [28, 352, 676]
COL_W = 296
COL_TOP = 506
COL_BOTTOM = 990


def column_height(col, fnt, leading=2, gap=4, head_h=24):
    """Total height a column needs at the given row font size."""
    y = 0
    for header, stories in col:
        y += head_h
        for date, text in stories:
            lines = wrap_text(f"{date} \u00b7 {text}", fnt, COL_W)
            y += len(lines) * (fnt.size + leading) + gap
    return y


def draw_column(draw, x, col, fnt, leading=2, gap=4):
    y = COL_TOP
    f_head = font(SANS_B, 15)
    for header, stories in col:
        draw.text((x, y), header, font=f_head, fill=RED)
        y += 24
        for date, text in stories:
            lines = wrap_text(f"{date} \u00b7 {text}", fnt, COL_W)
            for ln in lines:
                draw.text((x, y), ln, font=fnt, fill=INK)
                y += fnt.size + leading
            y += gap
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    hrule(d, 28, 996, 16, 4)
    f_mast = font(SERIF, 52)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=f_mast)
    d.text(((W - tw) / 2, 28), title, font=f_mast, fill=INK)
    f_date = font(SANS_B, 23)
    date = "THURSDAY,  26  NOVEMBER  2026"
    tw = d.textlength(date, font=f_date)
    d.text(((W - tw) / 2, 92), date, font=f_date, fill=RED)
    hrule(d, 28, 996, 126, 3)
    hrule(d, 28, 996, 131, 1)

    # ---- lead story: tariffs / markets ----
    f_kick = font(SANS_B, 17)
    d.text((28, 144), "TRADE WAR  \u00b7  WASHINGTON", font=f_kick, fill=RED)
    f_h1_size = 36
    while (f_h1_size > 26 and
           d.textlength("TARIFF SHOCK ROCKS MARKETS", font=font(SERIF, f_h1_size)) > 600):
        f_h1_size -= 2
    f_h1 = font(SERIF, f_h1_size)
    d.text((28, 168), "TARIFF SHOCK ROCKS MARKETS", font=f_h1, fill=INK)
    f_body = font(SANS, 17)
    y = 214
    for ln in wrap_text(LEAD_BODY, f_body, 600):
        d.text((28, y), ln, font=f_body, fill=INK)
        y += f_body.size + 4
    print("lead body bottom y:", y)
    # lead illustration panel: falling chart + AI chip
    d.rectangle([656, 144, 984, 378], outline=INK, width=2, fill=LIGHT)
    draw_chart_fall(d, 664, 152, 312, 138)
    d.line([(664, 296), (976, 296)], fill=GRAY, width=1)
    draw_chip(d, 664, 302, 312, 68)
    print("lead panel bottom y: 378")

    # ---- markets strip (auto-shrink so neither line runs past x=996) ----
    hrule(d, 28, 996, 386, 1)
    f_strip_size = 14
    while f_strip_size > 10:
        f_strip = font(SANS_B, f_strip_size)
        if (d.textlength(STRIP_1, font=f_strip) <= 968 and
                d.textlength(STRIP_2, font=f_strip) <= 968):
            break
        f_strip_size -= 1
    print("strip font size:", f_strip_size)
    d.text((28, 392), STRIP_1, font=f_strip, fill=INK)
    d.text((28, 410), STRIP_2, font=f_strip, fill=INK)
    hrule(d, 28, 996, 432, 1)

    # ---- scene band: six small vector scenes ----
    f_cap = font(SANS_B, 11)
    for i, (cap, fn) in enumerate(BAND):
        x = 28 + i * 160
        d.rectangle([x, 440, x + 154, 498], outline=INK, width=1, fill=LIGHT)
        fn(d, x + 4, 444, 146, 32)
        tw = d.textlength(cap, font=f_cap)
        d.text((x + (154 - tw) / 2, 480), cap, font=f_cap, fill=INK)
    print("scene band bottom y: 498")

    # ---- region columns (auto-fit row font so nothing passes COL_BOTTOM) ----
    row_size = None
    f_row = None
    for size in (12, 11.5, 11):
        f_try = ImageFont.truetype(SANS, size)
        need = max(column_height(c, f_try) for c in COLUMNS)
        print(f"row size {size}: tallest column needs {need}px, have {COL_BOTTOM - COL_TOP}px")
        if COL_TOP + need <= COL_BOTTOM:
            row_size, f_row = size, f_try
            break
    if row_size is None:
        row_size = 11
        f_row = ImageFont.truetype(SANS, 11)
        print("WARNING: columns still overflow at size 11")
    bottoms = []
    for x, col in zip(COL_X, COLUMNS):
        bottoms.append(draw_column(d, x, col, f_row))
        # column divider
        if x != COL_X[0]:
            d.line([(x - 14, COL_TOP), (x - 14, COL_BOTTOM)], fill=(200, 194, 178), width=1)
    print("column bottoms:", bottoms, "row size:", row_size)

    # ---- footer ----
    hrule(d, 28, 996, 994, 1)
    f_foot = font(SANS, 12)
    d.text((28, 1000), "Sources: Reuters \u00b7 AP \u00b7 Financial Times \u00b7 KCNA",
           font=f_foot, fill=GRAY)
    foot_r = "THE WORLD IN ONE DAY \u2014 26 NOV 2026"
    d.text((996 - d.textlength(foot_r, font=f_foot), 1000), foot_r,
           font=f_foot, fill=GRAY)

    img.save("poster.png", "PNG")
    print("saved poster.png", img.size)


if __name__ == "__main__":
    main()
