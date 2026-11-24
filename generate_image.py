#!/usr/bin/env python3
"""Draws 'The World Today - Tuesday 24 November 2026' front page.

Deterministic: fixed coordinates, fixed palette, no timestamps, no
randomness, no network. Writes entry.png (1024x1024) next to this file.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")

PAPER = (247, 243, 232)
INK = (26, 26, 26)
RED = (176, 42, 32)
BLUE = (31, 78, 121)
SKY = (178, 214, 235)
SEA = (64, 120, 158)
GREEN = (74, 124, 66)
GREY = (110, 110, 105)
LIGHT = (233, 227, 210)
PANEL_BG = (255, 253, 246)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def fit_lines(draw, text, fnt, max_w, max_lines):
    """Wrap text; shrink font until it fits max_lines (min size 10)."""
    size = fnt.size
    while size > 10:
        f = font(fnt.path, size)
        lines = wrap(draw, text, f, max_w)
        if len(lines) <= max_lines:
            return lines, f
        size -= 1
    f = font(fnt.path, 10)
    return wrap(draw, text, f, max_w)[:max_lines], f


# ---------------------------------------------------------------- hero art
def draw_hero(d):
    """Jet over Ulleung island: sky, sea, green island, jet + contrail."""
    x0, y0, x1, y1 = 28, 168, 500, 536
    d.rectangle([x0, y0, x1, y1], fill=SKY, outline=INK, width=2)
    # sun
    d.ellipse([x1 - 90, y0 + 18, x1 - 34, y0 + 74], fill=(250, 204, 72),
              outline=(230, 170, 40), width=2)
    # clouds
    for cx, cy, s in [(90, 210, 1.0), (300, 196, 0.8), (180, 250, 0.7)]:
        d.ellipse([cx, cy, cx + 70 * s, cy + 22 * s], fill=(255, 255, 255))
        d.ellipse([cx + 14 * s, cy - 10 * s, cx + 56 * s, cy + 12 * s],
                  fill=(255, 255, 255))
    # sea
    d.rectangle([x0, 420, x1, y1], fill=SEA)
    for wy in (448, 478, 508):
        for wx in range(x0 + 12, x1 - 30, 44):
            d.arc([wx, wy, wx + 34, wy + 14], 0, 180, fill=(255, 255, 255),
                  width=3)
    # island: green hill + cliffs
    d.polygon([(120, 420), (180, 330), (260, 300), (330, 340), (400, 420)],
              fill=GREEN)
    d.polygon([(180, 330), (260, 300), (300, 360), (240, 400), (200, 380)],
              fill=(58, 100, 52))
    d.polygon([(120, 420), (400, 420), (400, 396), (120, 396)],
              fill=(120, 96, 64))
    # houses on the island
    for hx in (210, 250, 292):
        d.rectangle([hx, 372, hx + 26, 396], fill=(240, 235, 220),
                    outline=INK, width=1)
        d.polygon([(hx - 2, 372), (hx + 13, 356), (hx + 28, 372)],
                  fill=RED)
    # jet: fuselage, wings, tail, contrail
    d.line([(60, 300), (300, 262)], fill=(255, 255, 255), width=5)
    d.polygon([(300, 252), (392, 244), (398, 252), (392, 262), (300, 270)],
              fill=(70, 70, 74))
    d.polygon([(330, 252), (352, 216), (366, 218), (352, 252)],
              fill=(90, 90, 96))
    d.polygon([(330, 262), (352, 296), (366, 294), (352, 262)],
              fill=(90, 90, 96))
    d.polygon([(388, 244), (404, 224), (410, 226), (400, 250)],
              fill=(70, 70, 74))
    d.ellipse([386, 246, 396, 256], fill=(250, 204, 72))
    # warning triangle
    cx, cy = 442, 320
    d.polygon([(cx, cy - 34), (cx + 34, cy + 24), (cx - 34, cy + 24)],
              fill=(250, 204, 72), outline=INK, width=2)
    d.text((cx - 5, cy - 18), "!", font=font(SANS_B, 30), fill=RED)
    # caption strip
    d.rectangle([x0, y1 - 26, x1, y1], fill=INK)
    d.text((x0 + 10, y1 - 22), "ULLEUNG ISLAND, SOUTH KOREA",
           font=font(SANS_B, 14), fill=(255, 255, 255))


# ------------------------------------------------------------- panel art
def panel_art(d, kind, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=SKY, outline=INK, width=1)
    if kind == "iran":  # tanker on the Strait of Hormuz
        d.rectangle([x0, y0 + 62, x1, y1], fill=SEA)
        d.rectangle([x0 + 22, y0 + 34, x1 - 22, y0 + 66], fill=(40, 40, 44))
        d.rectangle([x0 + 30, y0 + 18, x0 + 52, y0 + 36], fill=(40, 40, 44))
        d.rectangle([x0 + 60, y0 + 22, x0 + 96, y0 + 36], fill=(40, 40, 44))
        for wx in range(x0 + 8, x1 - 20, 30):
            d.arc([wx, y0 + 74, wx + 24, y0 + 86], 0, 180,
                  fill=(255, 255, 255), width=2)
        d.ellipse([x1 - 44, y0 + 8, x1 - 16, y0 + 36], fill=(250, 204, 72))
    elif kind == "awacs":  # plane with radar dome
        d.ellipse([x0 + 30, y0 + 12, x0 + 62, y0 + 26], fill=(255, 255, 255))
        d.ellipse([x0 + 190, y0 + 22, x0 + 226, y0 + 36],
                  fill=(255, 255, 255))
        d.polygon([(x0 + 60, y0 + 52), (x0 + 236, y0 + 48),
                   (x0 + 242, y0 + 56), (x0 + 236, y0 + 64),
                   (x0 + 60, y0 + 68)], fill=(235, 235, 238))
        d.ellipse([x0 + 128, y0 + 30, x0 + 168, y0 + 52], fill=(200, 205, 210),
                  outline=INK, width=2)
        d.polygon([(x0 + 138, y0 + 52), (x0 + 152, y0 + 26),
                   (x0 + 162, y0 + 28), (x0 + 152, y0 + 52)],
                  fill=(150, 158, 165))
        d.polygon([(x0 + 138, y0 + 64), (x0 + 152, y0 + 90),
                   (x0 + 162, y0 + 88), (x0 + 152, y0 + 64)],
                  fill=(150, 158, 165))
        d.polygon([(x0 + 232, y0 + 48), (x0 + 246, y0 + 32),
                   (x0 + 250, y0 + 34), (x0 + 240, y0 + 56)],
                  fill=(235, 235, 238))
    elif kind == "sanctions":  # bank building, red stamp
        d.rectangle([x0, y0, x1, y1], fill=LIGHT)
        d.rectangle([x0 + 40, y0 + 58, x1 - 40, y0 + 66], fill=INK)
        for cx in range(x0 + 52, x1 - 52, 44):
            d.rectangle([cx, y0 + 30, cx + 12, y0 + 58], fill=(255, 255, 255),
                        outline=INK, width=1)
        d.polygon([(x0 + 34, y0 + 30), ((x0 + x1) // 2, y0 + 8),
                   (x1 - 34, y0 + 30)], fill=RED)
        d.ellipse([x1 - 52, y0 + 66, x1 - 22, y0 + 96], fill=(250, 204, 72),
                  outline=RED, width=2)
        d.text((x1 - 46, y0 + 70), "$", font=font(SANS_B, 20), fill=INK)
    elif kind == "gaza":  # UN flag over a stone water well
        d.rectangle([x0, y0, x1, y1], fill=(214, 196, 160))
        # well: stone rim with dark water inside
        d.rectangle([x0 + 92, y0 + 58, x1 - 92, y0 + 96], fill=(150, 150, 148),
                    outline=INK, width=2)
        d.ellipse([x0 + 96, y0 + 54, x1 - 96, y0 + 72], fill=(64, 120, 158),
                  outline=INK, width=2)
        # posts + little roof over the well
        d.rectangle([x0 + 96, y0 + 22, x0 + 104, y0 + 58], fill=(120, 96, 64))
        d.rectangle([x1 - 104, y0 + 22, x1 - 96, y0 + 58], fill=(120, 96, 64))
        d.polygon([(x0 + 86, y0 + 24), ((x0 + x1) // 2, y0 + 6),
                   (x1 - 86, y0 + 24)], fill=(120, 96, 64))
        d.line([(x0 + 28, y0 + 6), (x0 + 28, y0 + 62)], fill=INK, width=3)
        d.rectangle([x0 + 28, y0 + 6, x0 + 80, y0 + 38], fill=(0, 122, 184))
        d.text((x0 + 36, y0 + 10), "UN", font=font(SANS_B, 20),
               fill=(255, 255, 255))
    elif kind == "factory":  # factory with flames and smoke
        d.rectangle([x0, y0, x1, y1], fill=(250, 220, 180))
        d.rectangle([x0 + 30, y0 + 46, x1 - 30, y0 + 98], fill=(150, 150, 150),
                    outline=INK, width=1)
        d.rectangle([x0 + 44, y0 + 16, x0 + 58, y0 + 46], fill=(120, 120, 120),
                    outline=INK, width=1)
        d.rectangle([x0 + 70, y0 + 22, x0 + 82, y0 + 46], fill=(120, 120, 120),
                    outline=INK, width=1)
        for sx, sy in [(x0 + 50, y0 + 4), (x0 + 78, y0 + 10), (x0 + 108, y0 + 2)]:
            d.ellipse([sx, sy, sx + 26, sy + 14], fill=(120, 120, 120))
        # flames
        for fx, fh in [(x0 + 60, 34), (x0 + 130, 46), (x0 + 200, 30)]:
            d.polygon([(fx, y0 + 46), (fx + 14, y0 + 46 - fh),
                       (fx + 28, y0 + 46)], fill=(240, 120, 30))
            d.polygon([(fx + 6, y0 + 46), (fx + 14, y0 + 46 - fh + 12),
                       (fx + 22, y0 + 46)], fill=(250, 204, 72))
        d.rectangle([x0 + 52, y0 + 62, x0 + 84, y0 + 98], fill=(60, 60, 64))
    elif kind == "cop":  # cracked globe, sun
        d.ellipse([x0 + 88, y0 + 8, x0 + 208, y0 + 96], fill=(64, 120, 158),
                  outline=INK, width=2)
        d.ellipse([x0 + 108, y0 + 22, x0 + 148, y0 + 52], fill=GREEN)
        d.ellipse([x0 + 150, y0 + 58, x0 + 188, y0 + 84], fill=GREEN)
        d.line([(x0 + 148, y0 + 8), (x0 + 138, y0 + 40), (x0 + 158, y0 + 62),
                (x0 + 148, y0 + 96)], fill=INK, width=2)
        d.ellipse([x0 + 20, y0 + 12, x0 + 52, y0 + 44], fill=(250, 120, 40))
        for a in range(0, 360, 45):
            import math
            r1, r2 = 22, 30
            cx, cy = x0 + 36, y0 + 28
            x_a = cx + r1 * math.cos(math.radians(a))
            y_a = cy + r1 * math.sin(math.radians(a))
            x_b = cx + r2 * math.cos(math.radians(a))
            y_b = cy + r2 * math.sin(math.radians(a))
            d.line([(x_a, y_a), (x_b, y_b)], fill=(250, 120, 40), width=2)


# ------------------------------------------------------------------- page
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead
    d.rectangle([0, 0, W, 8], fill=RED)
    d.text((W // 2, 26), "THE WORLD TODAY", font=font(SERIF_B, 62),
           fill=INK, anchor="ma")
    d.line([(28, 104), (W - 28, 104)], fill=INK, width=2)
    d.text((28, 112), "TUESDAY 24 NOVEMBER 2026", font=font(SANS_B, 26),
           fill=RED)
    d.text((W - 28, 112), "ONE DAY  •  SEVEN STORIES",
           font=font(SANS_B, 17), fill=GREY, anchor="ra")
    d.line([(28, 150), (W - 28, 150)], fill=INK, width=3)

    # ---- hero
    draw_hero(d)
    hx, hw = 524, 1024 - 28 - 524
    y = 176
    d.text((hx, y), "KOREA  •  AIRSPACE SCARE", font=font(SANS_B, 17),
           fill=RED)
    y += 30
    hero_head = "JET SCARE SPARKS\nKOREA ALERT"
    for ln in hero_head.split("\n"):
        d.text((hx, y), ln, font=font(SERIF_B, 44), fill=INK)
        y += 52
    y += 8
    hero_sum = ("Seoul briefly orders Ulleung islanders to take shelter "
                "after an aircraft enters its airspace. The alert is lifted "
                "in minutes; the aircraft is first said to be Russian, "
                "later possibly North Korean.")
    lines, f = fit_lines(d, hero_sum, font(SANS, 21), hw, 6)
    y = text_block(d, hx, y, lines, f, INK, 28)
    y += 14
    d.line([(hx, y), (W - 28, y)], fill=GREY, width=1)
    y += 10
    d.text((hx, y), "Warning at 7:52 a.m. local time",
           font=font(SANS_B, 16), fill=BLUE)

    # ---- panels: 3 columns x 2 rows
    panels = [
        ("iran", "IRAN", "IRAN VOWS TO FIGHT\nUS BLOCKADE",
         "Tehran says it will use \u201call its tools\u201d against the US "
         "naval blockade. The Hormuz standoff goes on."),
        ("awacs", "NATO  •  POLAND", "NATO SENDS AWACS\nTO POLAND",
         "An early-warning jet goes to Poland after three Russian "
         "missiles landed there on Friday."),
        ("sanctions", "USA  •  IRAN", "US HITS IRAN\u2019S\nSHADOW BANKS",
         "Treasury sanctions dozens of exchange houses and front "
         "firms; $14.7bn in suspect flows found."),
        ("gaza", "GAZA", "THREE KILLED IN\nGAZA STRIKES",
         "Israeli strikes kill three, including an UNRWA worker at a "
         "well in Jabalia camp."),
        ("factory", "INDONESIA", "24 DEAD IN FACTORY\nFIRE IN INDONESIA",
         "A blaze at a candy factory in Banten; about 30 workers "
         "still missing as rescuers search."),
        ("cop", "CLIMATE  •  COP31", "COP31 ENDS WITH\nNO DEAL",
         "Climate talks collapse in Antalya; backlash in Australia, "
         "despair among Pacific nations."),
    ]
    px0, py0 = 28, 556
    pw, ph = 317, 216
    gap = 12
    for i, (kind, kicker, head, summ) in enumerate(panels):
        col, row = i % 3, i // 3
        x0 = px0 + col * (pw + gap)
        y0 = py0 + row * (ph + gap)
        x1, y1 = x0 + pw, y0 + ph
        d.rectangle([x0, y0, x1, y1], fill=PANEL_BG, outline=INK, width=1)
        panel_art(d, kind, x0 + 6, y0 + 6, x1 - 6, y0 + 104)
        ty = y0 + 110
        d.text((x0 + 10, ty), kicker, font=font(SANS_B, 13), fill=RED)
        ty += 18
        for ln in head.split("\n"):
            d.text((x0 + 10, ty), ln, font=font(SERIF_B, 21), fill=INK)
            ty += 25
        lines, f = fit_lines(d, summ, font(SANS, 14), pw - 20, 2)
        text_block(d, x0 + 10, ty + 2, lines, f, (60, 60, 60), 18)

    # ---- footer
    d.line([(28, 1000), (W - 28, 1000)], fill=INK, width=1)
    d.text((W // 2, 1006),
           "Sources: Reuters, AP, UNRWA, US Treasury  •  Events of 24 November 2026",
           font=font(SANS, 13), fill=GREY, anchor="ma")

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
