#!/usr/bin/env python3
"""Draw the 25 November 2026 world-news broadsheet (1024x1024 PNG).

One image that sums up Wednesday 25 November 2026: a serif broadsheet
with a masthead, one big hero story, a numbers strip, and 28 more
stories in two columns, tagged by region. All 29 stories were first
reported on 25 November 2026 (any time zone) and verified against a
real source; the full source list is in STORIES.md.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 241, 227)
INK = (26, 26, 26)
RED = (179, 32, 44)
NAVY = (31, 58, 95)
GOLD = (176, 124, 18)
GREY = (90, 86, 78)
LINE = (26, 26, 26)
WHITE = (255, 255, 255)

SERIF_B = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf"
SERIF_I = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"
SANS_B = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"

REGION_COLORS = {
    "US": (179, 32, 44), "EU": (31, 58, 95), "AP": (0, 110, 84),
    "ME": (122, 74, 12), "AF": (106, 44, 112), "LA": (0, 96, 128),
    "TE": (70, 70, 70),
}

# (region, headline) — 28 stories; the hero (CIA breach) makes 29.
STORIES = [
    ("US", "Abrego Garcia leaves US for Spain"),
    ("US", "Radar outage delays O'Hare flights"),
    ("US", "Huawei guilty on 10 of 12 counts"),
    ("EU", "EU hosts Balkans summit in Brussels"),
    ("EU", "EU unveils new Russia sanctions"),
    ("EU", "EU nature-law talks collapse"),
    ("EU", "Zelenskyy: Kyiv needs \u20ac115bn in 2027"),
    ("AP", "China's Shenzhou-24 lifts off"),
    ("AP", "Shanghai party chief under probe"),
    ("AP", "Russian jets enter Seoul's air zone"),
    ("AP", "Seoul Metro strike called off"),
    ("AP", "China extends chip-mineral pause"),
    ("ME", "Houthi drone wounds 11 in Riyadh"),
    ("ME", "Eisenkot clinches coalition deal"),
    ("ME", "Houthis 60 km from Aden; city holds"),
    ("ME", "Iraq seizes Kurdistan border posts"),
    ("AF", "Court hands Senegal back AFCON title"),
    ("AF", "WHO flees Ebola hospital in Congo"),
    ("AF", "Amnesty: 37 killed in Sudan strikes"),
    ("AF", "Ethiopia, Eritrea mass troops"),
    ("LA", "US pauses drills with Ecuador"),
    ("LA", "Lula backs new spending curbs"),
    ("LA", "Lula snubs Milei for inauguration"),
    ("LA", "Maduro's first birthday behind bars"),
    ("TE", "DeepSeek maths AI checks own proofs"),
    ("TE", "Google launches Deep Research agent"),
    ("TE", "Microsoft declares 'Code Red' outage"),
    ("TE", "SoftBank falls 11% as AI stocks slide"),
]


def font(path, size):
    return ImageFont.truetype(path, size)


def fit(text, path, start, minimum, max_width, draw):
    """Largest font size (down to `minimum`) that fits `text` in max_width."""
    size = start
    while size > minimum:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_width:
            return f
        size -= 1
    return font(path, minimum)


def draw_shield_crack(draw, x, y, s):
    """Flat shield with a red crack, server rack and warning triangle."""
    # server rack
    draw.rectangle([x, y + 8, x + 64, y + s], fill=NAVY)
    for i in range(4):
        yy = y + 18 + i * 34
        draw.rectangle([x + 8, yy, x + 56, yy + 18], fill=(58, 90, 140))
        draw.ellipse([x + 12, yy + 5, x + 20, yy + 13], fill=(120, 220, 120))
        draw.rectangle([x + 28, yy + 7, x + 50, yy + 11], fill=(200, 210, 225))
    # shield
    cx = x + 150
    shield = [(cx - 62, y + 10), (cx + 62, y + 10), (cx + 62, y + 62),
              (cx, y + 128), (cx - 62, y + 62)]
    draw.polygon(shield, fill=(232, 222, 200), outline=NAVY, width=4)
    # crack
    crack = [(cx - 8, y + 16), (cx + 10, y + 44), (cx - 6, y + 66),
             (cx + 12, y + 92), (cx - 2, y + 118)]
    draw.line(crack, fill=RED, width=7, joint="curve")
    # warning triangle
    tx, ty = x + 196, y + 96
    draw.polygon([(tx, ty), (tx + 44, ty + 40), (tx - 44, ty + 40)],
                 fill=GOLD, outline=INK, width=3)
    draw.rectangle([tx - 3, ty + 12, tx + 3, ty + 28], fill=INK)
    draw.ellipse([tx - 3, ty + 31, tx + 3, ty + 37], fill=INK)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 6], fill=RED)
    title = "THE WORLD IN ONE DAY"
    tf = font(SERIF_B, 58)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 14), title, font=tf, fill=INK)
    d.line([(24, 88), (W - 24, 88)], fill=INK, width=3)
    d.line([(24, 93), (W - 24, 93)], fill=INK, width=1)
    dateline = "WEDNESDAY 25 NOVEMBER 2026  \u00b7  29 STORIES  \u00b7  7 REGIONS"
    df = font(SANS_B, 21)
    dw = d.textlength(dateline, font=df)
    d.text(((W - dw) / 2, 102), dateline, font=df, fill=INK)
    check = "Yesterday's news, not today's \u2014 COP31 climate talks end without a deal."
    cf = font(SERIF_I, 19)
    cw = d.textlength(check, font=cf)
    d.text(((W - cw) / 2, 128), check, font=cf, fill=GREY)

    # ---- hero ----
    hy = 152
    d.line([(24, hy - 6), (W - 24, hy - 6)], fill=INK, width=2)
    d.text((24, hy + 6), "THE BIG STORY \u2014 UNITED STATES", font=font(SANS_B, 20), fill=RED)
    hero_head = "AMERICA'S SPIES HACKED"
    hf = fit(hero_head, SERIF_B, 62, 44, 700, d)
    d.text((24, hy + 32), hero_head, font=hf, fill=INK)
    d.text((24, hy + 100), "CIA and the intelligence chief's office hit", font=font(SERIF, 26), fill=INK)
    d.text((24, hy + 130), "by a cyber breach, sources say.", font=font(SERIF, 26), fill=INK)
    d.text((24, hy + 160), "Officials insist no classified data was hit.", font=font(SERIF_I, 22), fill=GREY)
    draw_shield_crack(d, 748, hy + 8, 150)
    d.line([(24, hy + 188), (W - 24, hy + 188)], fill=INK, width=2)

    # ---- numbers strip ----
    ny = hy + 194
    d.rectangle([0, ny, W, ny + 46], fill=NAVY)
    nums = "11 hurt in Riyadh  \u00b7  37 killed in Sudan  \u00b7  \u20ac115bn for Kyiv  \u00b7  \u20ac1.78tn EU budget"
    nf = font(SANS_B, 22)
    nw = d.textlength(nums, font=nf)
    d.text(((W - nw) / 2, ny + 10), nums, font=nf, fill=WHITE)

    # ---- story grid: 2 columns x 14 rows ----
    gy = ny + 46 + 10
    col_x = [24, 524]
    col_w = 476
    rows = 14
    row_h = 41
    half = len(STORIES) // 2
    columns = [STORIES[:half], STORIES[half:]]
    for ci, col in enumerate(columns):
        for ri, (region, headline) in enumerate(col):
            y = gy + ri * row_h
            color = REGION_COLORS[region]
            d.rectangle([col_x[ci], y + 2, col_x[ci] + 46, y + 30], fill=color)
            tagf = font(SANS_B, 16)
            tag = region
            tgw = d.textlength(tag, font=tagf)
            d.text((col_x[ci] + (46 - tgw) / 2, y + 6), tag, font=tagf, fill=WHITE)
            hf2 = fit(headline, SERIF_B, 23, 18, col_w - 58, d)
            d.text((col_x[ci] + 58, y + 3), headline, font=hf2, fill=INK)
            if ri < rows - 1:
                d.line([(col_x[ci], y + 36), (col_x[ci] + col_w, y + 36)], fill=(210, 203, 188), width=1)

    # ---- footer ----
    fy = H - 34
    d.line([(24, fy), (W - 24, fy)], fill=INK, width=2)
    foot = "Sources: Reuters, CNN, AP, BBC, Al Jazeera, ABC, Korea Times \u00b7 All events first reported 25 Nov 2026"
    ff = font(SANS, 16)
    d.text((24, fy + 8), foot, font=ff, fill=GREY)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")
    img.save(path, "PNG", optimize=True)
    size = os.path.getsize(path)
    print(f"wrote {path}: {img.size[0]}x{img.size[1]}, {size} bytes, {len(STORIES) + 1} stories")


if __name__ == "__main__":
    main()
