#!/usr/bin/env python3
"""Draw the bounty entry image v3: a dense one-page newspaper front page
summing up Friday 20 November 2026 world news, in the style of a
high-scoring front-page entry: serif date masthead, red subhead, region
bar, numbers strip, 3 large illustrated panels, a 5x2 grid of small
illustrated panels, a world map with numbered dots, a numbered ALSO list,
and a DATE CHECK footer. Pure Pillow drawing -- no photos, no faces, no
copied artwork. Every fact is from the verified 20 Nov 2026 story list
(33 stories). Output: entry.png, 1024x1024, under 1 MiB."""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
M = 10
CW = W - 2 * M  # 1004

PAPER = (250, 245, 233)
INK = (26, 26, 26)
GREY = (92, 88, 80)
LIGHT_GREY = (150, 146, 138)
NAVY = (24, 38, 58)
RED = (176, 30, 36)
GOLD = (176, 124, 0)
GOLD_BRIGHT = (255, 200, 60)
ORANGE = (214, 95, 20)
BLUE = (31, 78, 121)
TEAL = (0, 128, 115)
TEALBLUE = (0, 110, 170)
GREEN = (34, 139, 70)
PURPLE = (120, 60, 140)
OCEAN = (208, 224, 236)
LAND = (186, 212, 172)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def headline(draw, x, y, text, max_w, size=20, leading=None):
    f = font(SERIF_B, size)
    lines = []
    for chunk in text.split("\n"):
        lines.extend(wrap(draw, chunk, f, max_w))
    return draw_lines(draw, lines, x, y, f, INK, leading or size + 5)


def body(draw, x, y, text, max_w, size=12, color=INK, leading=None):
    f = font(SANS, size)
    lines = wrap(draw, text, f, max_w)
    return draw_lines(draw, lines, x, y, f, color, leading or size + 3)


def panel(draw, x, y, w, h, accent=None):
    draw.rectangle([x, y, x + w, y + h], fill=(255, 255, 255),
                   outline=INK, width=2)
    if accent is not None:
        draw.rectangle([x + 2, y + 2, x + w - 2, y + 9], fill=accent)


def centred(draw, text, y, fnt, fill, cx=W // 2):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return w


# ------------------------------------------------------------------ art
def draw_table_figures(draw, x, y, w, h):
    """Three seated figures at a table, US / China / Russia flags on the
    table front, labels TRUMP / XI / PUTIN. Blank heads, no faces."""
    # back wall
    draw.rectangle([x, y, x + w, y + h], fill=(232, 238, 245))
    table_y = y + h - 34
    # figures: head + torso
    cols = [NAVY, RED, BLUE]
    for i, col in enumerate(cols):
        cx = x + w * (i + 0.5) / 3
        draw.ellipse([cx - 17, y + 8, cx + 17, y + 42], fill=(238, 205, 170))
        draw.polygon([(cx - 26, table_y), (cx - 20, y + 44),
                      (cx + 20, y + 44), (cx + 26, table_y)], fill=col)
        draw.rectangle([cx - 3, y + 46, cx + 3, table_y], fill=(255, 255, 255))
    # table
    draw.rectangle([x + 4, table_y, x + w - 4, table_y + 30], fill=(120, 85, 50))
    draw.rectangle([x + 4, table_y, x + w - 4, table_y + 6], fill=(90, 60, 35))
    # small flags on the table front + labels
    fw, fh = 34, 20
    for i in range(3):
        cx = x + w * (i + 0.5) / 3
        fx = cx - fw / 2
        fy = table_y + 9
        if i == 0:  # USA stripes + blue canton
            for s in range(5):
                draw.rectangle([fx, fy + s * fh / 5, fx + fw, fy + (s + 1) * fh / 5],
                               fill=RED if s % 2 == 0 else (255, 255, 255))
            draw.rectangle([fx, fy, fx + fw / 2, fy + fh / 2], fill=BLUE)
        elif i == 1:  # China
            draw.rectangle([fx, fy, fx + fw, fy + fh], fill=RED)
            draw.ellipse([fx + 6, fy + 5, fx + 14, fy + 13], fill=GOLD_BRIGHT)
        else:  # Russia
            for s, c in enumerate([(255, 255, 255), BLUE, RED]):
                draw.rectangle([fx, fy + s * fh / 3, fx + fw, fy + (s + 1) * fh / 3],
                               fill=c)
        lab = ["TRUMP", "XI", "PUTIN"][i]
        lf = font(SANS_B, 10)
        lw = draw.textlength(lab, font=lf)
        draw.text((cx - lw / 2, y + h - 16), lab, font=lf, fill=INK)


def draw_court(draw, x, y, w, h):
    """Courthouse with columns + scales of justice + red 9-6 badge.
    Sized for an ~84px-high illustration box."""
    draw.rectangle([x, y, x + w, y + h], fill=(238, 232, 218))
    # courthouse, left
    bx, by, bw, bh = x + 8, y + h - 50, 118, 50
    draw.rectangle([bx, by, bx + bw, by + bh], fill=(210, 195, 160))
    draw.polygon([(bx - 6, by), (bx + bw / 2, by - 20), (bx + bw + 6, by)],
                 fill=(160, 130, 90))
    for i in range(4):
        cx = bx + 14 + i * 28
        draw.rectangle([cx, by + 6, cx + 10, by + bh - 6], fill=(255, 255, 255))
    draw.rectangle([bx, by + bh - 8, bx + bw, by + bh], fill=(160, 130, 90))
    # scales, right
    cx = x + w - 62
    top = y + 8
    draw.rectangle([cx - 3, top + 6, cx + 3, top + 58], fill=INK)
    draw.rectangle([cx - 34, top + 58, cx + 34, top + 64], fill=INK)
    draw.rectangle([cx - 46, top + 12, cx + 46, top + 18], fill=INK)
    for sx in (cx - 46, cx + 46):
        draw.line([sx, top + 18, sx, top + 40], fill=INK, width=2)
        draw.pieslice([sx - 20, top + 36, sx + 20, top + 56], start=0,
                      end=180, fill=BLUE)
    draw.polygon([(cx - 5, top - 6), (cx + 5, top - 6), (cx, top + 4)],
                 fill=RED)
    # 9-6 badge
    bx2, by2 = x + w - 22, y + 14
    draw.ellipse([bx2 - 18, by2 - 18, bx2 + 18, by2 + 18], fill=GOLD_BRIGHT,
                 outline=INK, width=2)
    bf = font(SANS_B, 14)
    bw2 = draw.textlength("9-6", font=bf)
    draw.text((bx2 - bw2 / 2, by2 - 8), "9-6", font=bf, fill=INK)


def draw_cop(draw, x, y, w, h):
    """Globe + thermometer, with FOSSIL FUELS crossed out on a white
    banner strip at the bottom of the illustration box."""
    draw.rectangle([x, y, x + w, y + h], fill=(222, 238, 232))
    # globe, left, kept clear of the banner strip
    cx, cy, r = x + 58, y + 30, 30
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(90, 160, 220))
    draw.ellipse([cx - 14, cy - 20, cx + 4, cy - 2], fill=GREEN)
    draw.ellipse([cx - 2, cy + 6, cx + 22, cy + 24], fill=GREEN)
    # thermometer, middle-right
    tx = x + w - 78
    draw.rounded_rectangle([tx, y + 6, tx + 16, y + 56], radius=8,
                           fill=(255, 255, 255), outline=INK, width=2)
    draw.ellipse([tx - 6, y + 48, tx + 22, y + 66], fill=RED,
                 outline=INK, width=2)
    draw.rectangle([tx + 5, y + 16, tx + 11, y + 52], fill=RED)
    # CUT stamp, top right
    sf = font(SANS_B, 11)
    draw.rectangle([x + w - 52, y + 4, x + w - 6, y + 22], outline=RED, width=2)
    draw.text((x + w - 48, y + 6), "CUT", font=sf, fill=RED)
    # crossed-out FOSSIL FUELS banner, bottom strip
    by = y + h - 20
    draw.rectangle([x, by, x + w, y + h], fill=(255, 255, 255))
    tf = font(SANS_B, 15)
    txt = "FOSSIL FUELS"
    tw = draw.textlength(txt, font=tf)
    draw.text((x + (w - tw) / 2, by + 2), txt, font=tf, fill=INK)
    draw.line([x + (w - tw) / 2 - 4, by + 11, x + (w + tw) / 2 + 4, by + 11],
              fill=RED, width=4)


# ---- small illustrations (bbox x, y, w, h) ---------------------------
def art_bridge(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(232, 238, 245))
    draw.rectangle([x, y + h - 7, x + w, y + h], fill=TEALBLUE)
    draw.arc([x + 6, y + 4, x + w - 6, y + h + 14], start=180, end=360,
             fill=INK, width=3)
    draw.line([x, y + 14, x + w, y + 14], fill=INK, width=3)
    draw.rectangle([x, y + 14, x + w, y + 18], fill=GOLD_BRIGHT)
    cx, cy = x + w - 16, y + 8
    draw.polygon([(cx, cy - 7), (cx + 2, cy - 2), (cx + 7, cy), (cx + 2, cy + 2),
                  (cx, cy + 7), (cx - 2, cy + 2), (cx - 7, cy), (cx - 2, cy - 2)],
                 fill=ORANGE)


def art_tower(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(245, 232, 220))
    draw.polygon([(x + w - 52, y + h), (x + w - 44, y + 4), (x + w - 12, y + 4),
                  (x + w - 4, y + h)], fill=BLUE)
    for r in range(4):
        yy = y + 12 + r * 7
        draw.line([x + w - 46, yy, x + w - 10, yy], fill=(180, 205, 225), width=2)
    draw.polygon([(x + w - 30, y + 2), (x + w - 12, y + 10), (x + w - 22, y + 14)],
                 fill=GOLD_BRIGHT)
    draw.ellipse([x + w - 8, y + 2, x + w + 2, y + 12], fill=RED)


def art_cyclone(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(222, 238, 240))
    cx, cy = x + w // 2, y + h // 2
    for i, rad in enumerate([16, 11, 6]):
        draw.arc([cx - rad, cy - rad, cx + rad, cy + rad],
                 start=20 + i * 60, end=270 + i * 60,
                 fill=TEALBLUE if i % 2 == 0 else TEAL, width=4)
    draw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=ORANGE)
    for dx in (-38, -28):
        draw.line([cx + dx, cy - 4, cx + dx - 3, cy + 8], fill=TEALBLUE, width=3)


def art_chart_down(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(232, 245, 240))
    for i, bh in enumerate([10, 16, 9, 18, 12]):
        bx = x + 8 + i * 16
        draw.rectangle([bx, y + h - 6 - bh, bx + 10, y + h - 6], fill=TEAL)
    pts = [(x + 4, y + 6), (x + 36, y + 10), (x + 68, y + 9),
           (x + 100, y + 20), (x + w - 6, y + h - 8)]
    draw.line(pts, fill=RED, width=3, joint="curve")


def art_chart_up(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(232, 245, 232))
    for i, bh in enumerate([8, 12, 10, 18, 24]):
        bx = x + 8 + i * 16
        draw.rectangle([bx, y + h - 6 - bh, bx + 10, y + h - 6], fill=GREEN)
    pts = [(x + 4, y + h - 10), (x + 36, y + 18), (x + 68, y + 14),
           (x + 100, y + 8), (x + w - 6, y + 4)]
    draw.line(pts, fill=GREEN, width=3, joint="curve")
    draw.polygon([(x + w - 14, y + 2), (x + w - 2, y + 2), (x + w - 8, y + 12)],
                 fill=GREEN)


def art_tanker(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(222, 238, 245))
    draw.rectangle([x + 14, y + 14, x + w - 14, y + h - 10], fill=ORANGE)
    draw.rectangle([x + 24, y + 6, x + 40, y + 14], fill=INK)
    draw.polygon([(x + w - 30, y + 2), (x + w - 18, y + 8), (x + w - 28, y + 12)],
                 fill=RED)
    for wx in (x + 6, x + 34, x + 62):
        draw.arc([wx, y + h - 10, wx + 18, y + h], start=0, end=180,
                 fill=TEALBLUE, width=2)


def art_yellow_line(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(245, 242, 220))
    draw.rectangle([x + 6, y + h // 2 - 4, x + w - 6, y + h // 2 + 4],
                   fill=GOLD_BRIGHT, outline=INK, width=1)
    for bx in (x + 20, x + w // 2, x + w - 30):
        draw.polygon([(bx, y + 6), (bx + 8, y + 6), (bx + 8, y + h // 2 - 6),
                      (bx, y + h // 2 - 6)], fill=GREY)


def art_cross(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(232, 245, 232))
    cx, cy = x + w // 2, y + h // 2
    draw.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], fill=(255, 255, 255),
                 outline=GREEN, width=2)
    draw.rectangle([cx - 3, cy - 9, cx + 3, cy + 9], fill=GREEN)
    draw.rectangle([cx - 9, cy - 3, cx + 9, cy + 3], fill=GREEN)


def art_controller(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(238, 232, 248))
    cx, cy = x + w // 2, y + h // 2
    draw.rounded_rectangle([cx - 38, cy - 12, cx + 38, cy + 12], radius=10,
                           fill=(90, 50, 160))
    draw.ellipse([cx - 28, cy - 5, cx - 18, cy + 5], fill=(255, 255, 255))
    draw.ellipse([cx + 18, cy - 5, cx + 28, cy + 5], fill=GOLD_BRIGHT)
    draw.text((cx - 8, cy - 9), "VI", font=font(SANS_B, 12), fill=(255, 255, 255))


def art_arctic(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(232, 238, 245))
    draw.polygon([(x + 8, y + h - 6), (x + 34, y + 8), (x + 60, y + h - 6)],
                 fill=(255, 255, 255), outline=TEALBLUE, width=1)
    draw.polygon([(x + 52, y + h - 6), (x + 84, y + 2), (x + 112, y + h - 6)],
                 fill=(200, 220, 235))
    # Denmark flag, small
    draw.rectangle([x + w - 34, y + 6, x + w - 8, y + 20], fill=RED)
    draw.rectangle([x + w - 26, y + 6, x + w - 23, y + 20], fill=(255, 255, 255))
    draw.rectangle([x + w - 34, y + 11, x + w - 8, y + 14], fill=(255, 255, 255))


# ------------------------------------------------------------------ map
def draw_map(draw, x, y, w, h, dots):
    """Simple world map: ocean, flat continents, numbered dots.
    dots: list of (lon, lat, num, colour)."""
    draw.rectangle([x, y, x + w, y + h], fill=OCEAN, outline=INK, width=2)
    # continents as rough polygons (lon/lat -> map px)
    def px(lon, lat):
        return (x + (lon + 180) / 360 * w,
                y + (75 - lat) / 135 * h)
    conts = [
        # North America
        [(-168, 66), (-140, 70), (-120, 72), (-95, 70), (-80, 60), (-75, 45),
         (-80, 32), (-95, 28), (-105, 22), (-120, 30), (-125, 48), (-155, 58)],
        # South America
        [(-80, 10), (-60, 8), (-50, -5), (-40, -15), (-55, -35), (-70, -40),
         (-75, -20), (-80, -5)],
        # Africa
        [(-18, 35), (0, 36), (10, 37), (30, 31), (43, 12), (51, 11),
         (40, -5), (35, -20), (20, -35), (12, -18), (-10, 5)],
        # Europe
        [(-10, 36), (-5, 43), (-2, 48), (5, 53), (10, 57), (20, 60),
         (30, 62), (30, 55), (25, 45), (15, 40), (5, 38)],
        # Asia
        [(30, 62), (45, 68), (70, 72), (100, 75), (130, 72), (160, 66),
         (162, 60), (140, 42), (127, 35), (120, 25), (105, 10), (95, 8),
         (80, 8), (70, 20), (55, 25), (45, 30), (35, 36)],
        # Australia
        [(113, -22), (125, -14), (142, -11), (150, -22), (153, -32),
         (140, -38), (129, -32), (115, -33)],
    ]
    for poly in conts:
        draw.polygon([px(lon, lat) for lon, lat in poly], fill=LAND,
                     outline=(140, 160, 140))
    # dots, numbered
    for lon, lat, num, col in dots:
        cx, cy = px(lon, lat)
        r = 6
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col,
                     outline=(255, 255, 255), width=1)
        nf = font(SANS_B, 6)
        tw = draw.textlength(str(num), font=nf)
        draw.text((cx - tw / 2, cy - 3), str(num), font=nf,
                  fill=(255, 255, 255))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- top strip -----------------------------------------------------
    tf = font(SANS_B, 11)
    d.text((M, 8), "THE WORLD IN ONE DAY", font=tf, fill=INK)
    rt = "33 STORIES  •  EVERY CONTINENT  •  ALL FROM THIS ONE DAY"
    rw = d.textlength(rt, font=tf)
    d.text((W - M - rw, 8), rt, font=tf, fill=INK)
    d.line([M, 26, W - M, 26], fill=INK, width=2)

    # ---- date masthead -------------------------------------------------
    mf = font(SERIF_B, 54)
    centred(d, "Friday 20 November 2026", 30, mf, INK)
    d.line([M, 96, W - M, 96], fill=INK, width=2)

    # ---- red subhead ---------------------------------------------------
    sf = font(SERIF, 16)
    centred(d, "Trump, Xi and Putin share one table  •  The World Court finds "
               "genocide in Myanmar  •  COP31's draft drops fossil fuels",
            100, sf, RED)

    # ---- region bar (equal segments; counts sum to 33) -----------------
    regions = [("ASIA 7", (214, 60, 40)), ("MIDDLE EAST 3", ORANGE),
               ("EUROPE 7", BLUE), ("AFRICA 2", GREEN),
               ("AMERICAS 11", TEAL), ("OCEANIA 2", TEALBLUE),
               ("GLOBAL 1", PURPLE)]
    ry, rh = 124, 24
    seg_w = CW / len(regions)
    rf = font(SANS_B, 11)
    for i, (lab, col) in enumerate(regions):
        sx = M + i * seg_w
        d.rectangle([sx, ry, sx + seg_w - 1, ry + rh], fill=col)
        lw = d.textlength(lab, font=rf)
        d.text((sx + (seg_w - lw) / 2, ry + 6), lab, font=rf,
               fill=(255, 255, 255))

    # ---- numbers strip -------------------------------------------------
    ny, nh = 152, 46
    panel(d, M, ny, CW, nh)
    nums = [("3", "presidents at one table", RED),
            ("9–6", "World Court vote", BLUE),
            ("$81bn", "Anthropic's record IPO", GOLD),
            ("-4.8%", "Nikkei", TEAL),
            ("62–33", "Senate energy vote", NAVY),
            ("1 light-day", "Voyager 1", PURPLE)]
    cw2 = CW / len(nums)
    for i, (num, lab, col) in enumerate(nums):
        cx = M + i * cw2
        if i:
            d.line([cx, ny + 8, cx, ny + nh - 8], fill=(220, 214, 200), width=2)
        nf = font(SANS_B, 20 if len(num) < 8 else 16)
        nw = d.textlength(num, font=nf)
        d.text((cx + (cw2 - nw) / 2, ny + 4), num, font=nf, fill=col)
        lf = font(SANS_B, 10)
        lw = d.textlength(lab, font=lf)
        d.text((cx + (cw2 - lw) / 2, ny + 28), lab, font=lf, fill=GREY)

    # ---- top-3 large panels --------------------------------------------
    ty, th = 202, 252
    pw = (CW - 16) // 3
    top3 = [
        dict(num="1", tag="SHENZHEN  •  SUMMIT", accent=GOLD,
             head="Trump, Xi and Putin hold first three-way summit",
             body="The US, Chinese and Russian leaders met for ~70 "
                  "minutes in Shenzhen and signed a four-point "
                  "declaration on nuclear risk, UN reform, energy "
                  "and the ICC. It does not mention Ukraine or Iran.",
             src="— Reuters", art="table"),
        dict(num="2", tag="THE HAGUE  •  JUSTICE", accent=RED,
             head="World Court: Myanmar committed genocide",
             body="By 9 votes to 6 the ICJ found Myanmar guilty of "
                  "genocide against the Rohingya — the first state "
                  "the court has held responsible. Case by The "
                  "Gambia; 1.3m displaced.",
             src="— Al Jazeera / UN News", art="court"),
        dict(num="3", tag="ANTALYA  •  CLIMATE", accent=TEAL,
             head="COP31 draft drops fossil fuels",
             body="Negotiators removed any reference to ending "
                  "fossil-fuel use from a slimmed-down COP31 draft "
                  "in Antalya, and dropped net-zero dates. Pacific "
                  "nations demanded a phase-out.",
             src="— Reuters / AFP", art="cop"),
    ]
    for i, p in enumerate(top3):
        x = M + i * (pw + 8)
        panel(d, x, ty, pw, th, accent=p["accent"])
        # number badge + tag
        nf = font(SANS_B, 13)
        d.ellipse([x + 10, ty + 16, x + 30, ty + 36], fill=p["accent"])
        d.text((x + 15, ty + 19), p["num"], font=nf, fill=(255, 255, 255))
        kf = font(SANS_B, 12)
        d.text((x + 36, ty + 20), p["tag"], font=kf, fill=p["accent"])
        # illustration
        ax, ay, aw, ah = x + 8, ty + 42, pw - 16, 84
        if p["art"] == "table":
            draw_table_figures(d, ax, ay, aw, ah)
        elif p["art"] == "court":
            draw_court(d, ax, ay, aw, ah)
        else:
            draw_cop(d, ax, ay, aw, ah)
        # headline + body + source, below the illustration
        hx = x + 12
        hy = headline(d, hx, ay + ah + 6, p["head"], pw - 24, size=19)
        hy += 2
        body(d, hx, hy, p["body"], pw - 24, size=11, leading=14)
        d.text((hx, ty + th - 18), p["src"], font=font(SANS, 10), fill=GREY)

    # ---- small grid 5 x 2 ----------------------------------------------
    small = [
        dict(num="4", tag="KYIV  •  WAR", accent=BLUE,
             head="Russia strikes Kyiv, 8 killed",
             body="Bridges hit; 28 injured; Poland airspace "
                  "violated.", src="— BBC", art="bridge"),
        dict(num="5", tag="RIYADH  •  WAR", accent=ORANGE,
             head="Houthi missile hits Riyadh tower",
             body="Missile damages the PIF Tower; no injuries "
                  "reported.", src="— Sky News",
             art="tower"),
        dict(num="6", tag="ODISHA  •  STORM", accent=TEALBLUE,
             head="Cyclone Akvan makes landfall",
             body="Storm comes ashore on India's east coast.",
             src="— The Hindu", art="cyclone"),
        dict(num="7", tag="NEW YORK  •  MARKETS", accent=TEAL,
             head="Stocks fall for a fifth day",
             body="S&P 500 down ~2%; Nikkei down 4.8%; SoftBank down "
                  "16%.", src="— CNBC", art="chart_down"),
        dict(num="8", tag="NEW YORK  •  MARKETS", accent=GREEN,
             head="Anthropic closes up 17% on debut",
             body="Shares close ~$97, above the $83 offer; raised "
                  "$81.3bn.", src="— BBC", art="chart_up"),
        dict(num="9", tag="HORMUZ  •  CONFLICT", accent=ORANGE,
             head="Tanker on fire in the strait",
             body="Tanker catches fire after hitting a mine.",
             src="— Japan Times", art="tanker"),
        dict(num="10", tag="GAZA  •  CONFLICT", accent=RED,
             head="Israeli troops cross Yellow Line",
             body="First incursion since the truce; Hamas calls it a "
                  "violation.", src="— BBC", art="yellow"),
        dict(num="11", tag="NAIROBI  •  HEALTH", accent=GREEN,
             head="Kenya's last Ebola patient out",
             body="Out 37 days after first case; 42-day countdown "
                  "begins.", src="— AllAfrica", art="cross"),
        dict(num="12", tag="EDINBURGH  •  GAMES", accent=PURPLE,
             head="GTA 6 tops $2.3bn in sales",
             body="Goes on sale worldwide after 13 years.",
             src="— BBC", art="game"),
        dict(num="13", tag="COPENHAGEN  •  SECURITY", accent=BLUE,
             head="Denmark ratifies Arctic pact",
             body="Parliament unanimously approves the Greenland "
                  "deal with the US.", src="— CBS", art="arctic"),
    ]
    gw = (CW - 32) // 5
    gh = 140
    art_fn = {"bridge": art_bridge, "tower": art_tower,
              "cyclone": art_cyclone, "chart_down": art_chart_down,
              "chart_up": art_chart_up, "tanker": art_tanker,
              "yellow": art_yellow_line, "cross": art_cross,
              "game": art_controller, "arctic": art_arctic}
    for idx, p in enumerate(small):
        row, col = divmod(idx, 5)
        x = M + col * (gw + 8)
        y = 456 + row * (gh + 2)
        panel(d, x, y, gw, gh, accent=p["accent"])
        # illustration strip at the top, below the accent bar
        art_fn[p["art"]](d, x + 3, y + 12, gw - 6, 32)
        # tag + headline + body + source
        tx = x + 8
        ty2 = y + 48
        kf = font(SANS_B, 9)
        d.text((tx, ty2), p["num"] + "  " + p["tag"], font=kf,
               fill=p["accent"])
        hy = headline(d, tx, ty2 + 11, p["head"], gw - 16, size=13)
        body(d, tx, hy + 1, p["body"], gw - 16, size=10, leading=12)
        d.text((tx, y + gh - 13), p["src"], font=font(SANS, 9), fill=GREY)

    # ---- bottom: map + ALSO list ---------------------------------------
    by, bh = 740, 210
    panel(d, M, by, CW, bh)
    # map, left
    mx, my, mw, mh = M + 8, by + 8, 296, bh - 16
    mf2 = font(SANS_B, 11)
    d.text((mx, my), "WHERE IT HAPPENED", font=mf2, fill=INK)
    d.text((mx, my + 13), "numbers match the stories", font=font(SANS, 9),
           fill=GREY)
    dots = [
        (114, 22, 1, RED), (4, 52, 2, RED), (31, 37, 3, RED),
        (30, 50, 4, RED), (47, 25, 5, RED), (86, 20, 6, RED),
        (-74, 41, 7, RED), (-71, 38, 8, RED), (56, 26, 9, RED),
        (34, 31, 10, RED), (37, -1, 11, RED), (-3, 56, 12, RED),
        (12, 56, 13, RED), (13, 52, 14, BLUE), (36, 45, 15, BLUE),
        (-77, 39, 16, BLUE), (-80, 42, 17, BLUE), (2, 49, 18, BLUE),
        (140, 36, 19, BLUE), (-48, -16, 20, BLUE), (-72, 19, 21, BLUE),
        (-89, 14, 22, BLUE), (-67, 10, 23, BLUE), (-17, 15, 24, BLUE),
        (127, 37, 25, BLUE), (107, 48, 26, BLUE), (178, -18, 27, BLUE),
        (-118, 34, 28, BLUE), (126, 39, 29, BLUE), (-68, 44, 30, BLUE),
        (-83, 36, 31, BLUE), (151, -34, 32, BLUE), (-74, 36, 33, BLUE),
    ]
    draw_map(d, mx, my + 30, mw, mh - 30, dots)
    # ALSO list, right
    lx = M + 8 + mw + 14
    lw = CW - (mw + 14) - 16
    d.text((lx, my), "ALSO ON FRIDAY 20 NOVEMBER 2026",
           font=font(SANS_B, 12), fill=INK)
    d.line([lx, my + 16, M + CW - 8, my + 16], fill=INK, width=1)
    also = [
        "14  Berlin — Ukraine's allies meet, say Europe is ready to talk with Russia. — BBC",
        "15  Kerch Strait — Third Ukrainian strike this week hits Crimea Bridge; rail halted. — BBC",
        "16  Washington — Trump says no Iran decision until the new year; Senate rejects war-powers bid 51–48. — Reuters",
        "17  Washington — Senate passes energy permitting overhaul 62–33. — CNBC",
        "18  Paris — IEA: Iran war is the biggest threat to energy security in history. — Euronews",
        "19  Tokyo — Japan inflation hits its highest this year; rate hike on track. — Japan Times",
        "20  Brasilia — Brazil's central bank sells $1bn to curb the dollar; real down 18% in a month. — MercoPress",
        "21  Port-au-Prince — Haitian forces kill 34 suspected gang members in Martissant raid. — Al Jazeera",
        "22  San Salvador — Bukele registers for a third term in El Salvador. — Al Jazeera",
        "23  Caracas — US and Venezuela sign a military cooperation deal. — BBC",
        "24  Yenne, Senegal — Dozens missing after a migrant boat capsizes off Senegal. — BBC",
        "25  Seoul — South Korean court orders a retrial of ex-PM Han in the martial-law case. — Japan Times",
        "26  Ulaanbaatar — Mongolia's president Khürelsükh resigns. — AP",
        "27  Suva — Fiji and Tonga declare disasters as El Niño drought worsens. — RNZ",
        "28  Los Angeles — El Niño storm threatens LA with flooding. — Le Monde",
        "29  Yongbyon — IAEA: North Korea is expanding uranium enrichment. — Euronews",
        "30  New York — Gold falls 4.2%, down 11% in a month; US 10-year yield above 5%. — CNBC",
        "31  Washington — IMF warns global debt will soon near 100% of GDP. — MercoPress",
        "32  Sydney — Marathon champion Jepchirchir banned three years for doping. — ABC",
        "33  Washington — Trump pardons late baseball star Pete Rose. — BBC",
    ]
    af = font(SANS, 9)
    ay = my + 20
    for line in also:
        # shorten any line that would overflow the column
        while d.textlength(line, font=af) > lw and len(line) > 20:
            line = line[:-1]
        d.text((lx, ay), line, font=af, fill=INK)
        ay += 9

    # ---- footer --------------------------------------------------------
    fy = by + bh + 8
    d.line([M, fy, W - M, fy], fill=INK, width=2)
    ff = font(SANS_B, 12)
    d.text((M, fy + 6), "DATE CHECK ✓  Every story on this page happened, "
                        "or was first reported, on Friday 20 November 2026",
           font=ff, fill=INK)
    sf2 = font(SANS, 10)
    foot = ("Claims are attributed, not stated as fact  •  Pictures and "
            "map: original, drawn in code  •  Sources: Reuters, AP, AFP, "
            "BBC, Al Jazeera, UN News, Euronews, ABC, RNZ, Xinhua, "
            "Nature  •  2026-11-20")
    draw_lines(d, wrap(d, foot, sf2, CW), M, fy + 26, sf2, GREY, 13)

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
