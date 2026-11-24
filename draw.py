#!/usr/bin/env python3
"""news-23 b148 heroes-scene: draw THE WORLD TODAY, Monday 23 November 2026 (31 stories)."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (17, 17, 17)
RED = (139, 26, 26)
DARKRED = (110, 18, 18)
GOLD = (166, 124, 0)
NAVY = (20, 33, 61)
GREEN = (18, 77, 48)
GREY = (90, 86, 78)
LIGHT = (232, 226, 214)
BLUE = (28, 68, 140)
ORANGE = (232, 120, 40)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit(d, text, path, size, max_w, start=None):
    """Largest font size <= size that fits max_w."""
    s = start or size
    while s > 6:
        f = font(path, s)
        if d.textlength(text, font=f) <= max_w:
            return f
        s -= 1
    return font(path, 6)


def wrap(d, text, f, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def chip(d, x, y, label, claim=False):
    bg = (178, 34, 34) if claim else (28, 68, 140)
    f = font(SANS_B, 9)
    w = d.textlength(label, font=f) + 10
    d.rounded_rectangle([x, y, x + w, y + 13], radius=2, fill=bg)
    d.text((x + 5, y + 2), label, font=f, fill=(255, 255, 255))
    return w


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---- top gold rule ----
d.rectangle([0, 0, W, 5], fill=GOLD)

# ---- masthead ----
f_mast = font(SERIF, 54)
d.text((10, 8), "THE WORLD TODAY", font=f_mast, fill=INK)
f_date = font(SANS_B, 15)
d.text((1024 - 10 - d.textlength("MONDAY 23 NOVEMBER 2026", font=f_date), 30),
       "MONDAY 23 NOVEMBER 2026", font=f_date, fill=GOLD)
d.rectangle([10, 64, 1014, 66], fill=INK)

# ---- kicker strip ----
d.rectangle([10, 70, 1014, 92], fill=RED)
f_kick = font(SANS_B, 12)
kick = "AI ROUT HITS ASIA   \u00b7   UN CHIEF URGES AI RULES   \u00b7   US LEAD OVER CHINA AT RECORD LOW   \u00b7   ANTHROPIC IPO $107.3B"
d.text((14, 76), kick, font=f_kick, fill=(255, 255, 255))

# ---- number strip: 5 cols x 2 rows ----
nums = [
    ("-3.3%", "KOSPI"), ("5.3", "US-CHINA POWER GAP"), ("11,762", "EBOLA CASES, DRC"),
    ("10T won", "SEOUL STABILISATION FUND"), ("2%", "BILLIONAIRE TAX IN PARIS"),
    ("$450M", "SKUBAL DEAL"), ("165", "RUSSIAN MISSILES/WEEK"), ("12,000", "CLEARED IN MANCHESTER"),
    ("264 kg", "EXPLOSIVES SEIZED"), ("$107.3B", "ANTHROPIC IPO"),
]
for i, (v, lab) in enumerate(nums):
    col, row = i % 5, i // 5
    x = 14 + col * 202
    y = 98 + row * 27
    d.text((x, y), v, font=font(SANS_B, 17), fill=INK)
    d.text((x, y + 17), lab, font=font(SANS, 8), fill=GREY)
d.rectangle([10, 152, 1014, 153], fill=(200, 192, 176))

# ---- region bar ----
regions = [("ASIA-PACIFIC 7", 7, (28, 68, 140)), ("AMERICAS 8", 8, (139, 26, 26)),
           ("MIDDLE EAST 6", 6, (18, 77, 48)), ("EUROPE 5", 5, (166, 124, 0)),
           ("AFRICA 3", 3, (90, 60, 140)), ("WORLD 2", 2, (90, 86, 78))]
x = 10
for name, n, col in regions:
    w = int(1004 * n / 31)
    d.rectangle([x, 157, x + w, 175], fill=col)
    f_r = fit(d, name, SANS_B, 11, w - 8)
    d.text((x + 4, 162), name, font=f_r, fill=(255, 255, 255))
    x += w

# ---- UTC strip ----
d.rectangle([10, 179, 1014, 195], fill=LIGHT)
f_utc = font(SANS, 10)
d.text((14, 183), "THE DAY IN UTC   —   ~00:00 Kospi dives   \u00b7   ~05:30 Guterres opens   \u00b7   ~09:00 Power Index   \u00b7   ~12:00 Paris 2% tax   \u00b7   ~15:00 Kyiv missiles",
       font=f_utc, fill=INK)
d.text((1014 - d.textlength("~ APPROX", font=f_utc) - 4, 183), "~ APPROX", font=f_utc, fill=GREY)

# ---- hero scenes ----
HX = [10, 352, 694]
HW = 330
HY, HH = 199, 120
heroes = [
    dict(kind="kospi", cap="KOSPI 4,708.54  \u00b7  -161 PTS  \u00b7  SAMSUNG -3.1%  \u00b7  HYNIX -2.5%",
         head="AI ROUT HITS ASIA",
         body="Kospi closes -3.3% to 4,708.54, sheds 161 pts; intraday -5.8%. Samsung -3.1%, SK Hynix -2.5%.",
         src="KOREA EXCHANGE"),
    dict(kind="guterres", cap="BRIDGETOWN SUMMIT, BARBADOS",
         head="GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
         body="UN chief urges global AI safety rules at the Bridgetown summit; 150 back a risk framework.",
         src="UNITED NATIONS"),
    dict(kind="power", cap="ASIA POWER INDEX 2026  \u00b7  LOWY INSTITUTE",
         head="US LEAD OVER CHINA AT RECORD LOW",
         body="Asia Power Index 2026: US 78.9, China 73.6 \u2014 gap 5.3, narrowest since 2018. India third at 40.5.",
         src="LOWY INSTITUTE"),
]
for hx, hero in zip(HX, heroes):
    # scene box
    if hero["kind"] == "kospi":
        d.rectangle([hx, HY, hx + HW, HY + HH], fill=NAVY)
        # buildings: only bottom 55% so the big number stays clear
        import random
        rnd = random.Random(7)
        bx = hx + 8
        while bx < hx + HW - 14:
            bw = rnd.randint(16, 30)
            bh = rnd.randint(18, 58)
            d.rectangle([bx, HY + HH - bh, bx + bw, HY + HH], fill=(32, 52, 96))
            for wy in range(HY + HH - bh + 5, HY + HH - 4, 9):
                for wx in range(bx + 3, bx + bw - 3, 7):
                    if rnd.random() < 0.55:
                        d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 214, 90))
            bx += bw + 4
        # chart line: starts right of the big number
        pts = [(hx + 118, HY + 26), (hx + 160, HY + 40), (hx + 205, HY + 34),
               (hx + 250, HY + 58), (hx + 295, HY + 52), (hx + 322, HY + 78)]
        d.line(pts, fill=ORANGE, width=3)
        for px, py in pts:
            d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 255, 255))
        d.text((hx + 10, HY + 6), "-3.3%", font=font(SANS_B, 34), fill=(255, 255, 255))
    elif hero["kind"] == "guterres":
        d.rectangle([hx, HY, hx + HW, HY + HH], fill=GREEN)
        # globe on the right, masked circle
        cx, cy, r = hx + HW - 62, HY + 58, 44
        mask = Image.new("L", (2 * r, 2 * r), 0)
        md = ImageDraw.Draw(mask)
        md.ellipse([0, 0, 2 * r, 2 * r], fill=255)
        globe = Image.new("RGB", (2 * r, 2 * r), (196, 228, 196))
        gd = ImageDraw.Draw(globe)
        gd.ellipse([0, 0, 2 * r, 2 * r], outline=(90, 140, 100), width=2)
        for k in range(-2, 3):
            gd.arc([k * 18, -10, k * 18 + 44, 2 * r + 10], 270, 90, fill=(90, 140, 100), width=1)
        gd.line([0, r, 2 * r, r], fill=(90, 140, 100), width=1)
        img.paste(globe, (cx - r, cy - r), mask)
        d = ImageDraw.Draw(img)
        d.text((hx + 10, HY + 8), "150", font=font(SANS_B, 40), fill=(255, 214, 90))
        d.text((hx + 10, HY + 52), "DELEGATES BACK A", font=font(SANS_B, 13), fill=(255, 255, 255))
        d.text((hx + 10, HY + 70), "RISK FRAMEWORK", font=font(SANS_B, 13), fill=(255, 255, 255))
    else:
        d.rectangle([hx, HY, hx + HW, HY + HH], fill=(24, 24, 32))
        d.text((hx + 10, HY + 6), "NARROWEST SINCE 2018", font=font(SANS_B, 12), fill=(255, 255, 255))
        d.text((hx + HW - 62, HY + 6), "GAP 5.3", font=font(SANS_B, 12), fill=(255, 214, 90))
        bars = [("78.9", "US", (28, 68, 140), 0.95), ("73.6", "CHINA", (178, 34, 34), 0.89),
                ("40.5", "INDIA", (166, 124, 0), 0.50)]
        by = HY + 30
        for val, lab, col, frac in bars:
            bw = int(300 * frac)
            d.rectangle([hx + 10, by, hx + 10 + bw, by + 22], fill=col)
            d.text((hx + 14, by + 4), val, font=font(SANS_B, 13), fill=(255, 255, 255))
            d.text((hx + 10 + bw - 52, by + 4), lab, font=font(SANS_B, 12), fill=(255, 255, 255))
            by += 27
    # caption band inside scene bottom
    d.rectangle([hx, HY + HH - 16, hx + HW, HY + HH], fill=(0, 0, 0))
    f_cap = fit(d, hero["cap"], SANS_B, 9, HW - 10)
    d.text((hx + 5, HY + HH - 13), hero["cap"], font=f_cap, fill=(255, 255, 255))
    # headline below scene (gap keeps it clear of the black band)
    f_h = fit(d, hero["head"], SERIF, 20, HW, start=20)
    lines = wrap(d, hero["head"], f_h, HW)
    hy = HY + HH + 8
    for ln in lines[:2]:
        d.text((hx, hy), ln, font=f_h, fill=INK)
        hy += 22
    f_b = font(SANS, 11)
    for ln in wrap(d, hero["body"], f_b, HW)[:2]:
        d.text((hx, hy), ln, font=f_b, fill=(40, 40, 40))
        hy += 14
    d.text((hx, hy + 2), hero["src"], font=font(SANS, 9), fill=GREY)
    chip(d, hx + HW - 62, hy, "REPORTED")

# ---- cards ----
d.rectangle([10, 400, 1014, 402], fill=INK)
d.text((10, 406), "MORE OF THE DAY  \u2014  10 STORIES", font=font(SANS_B, 13), fill=INK)
cards = [
    ("1", "AMERICAS", "BESSENT: NVIDIA ANSWERS", "Treasury wants answers.", "WSJ", False),
    ("2", "AMERICAS", "FBI PROBES NCIC HACK", "NCIC database hacked.", "AP", False),
    ("3", "WHITE HOUSE", "TRUMP: IRAN STRIKES MAY RESUME", "May resume in New Year.", "Reuters", False),
    ("4", "MARKETS", "US FUTURES JUMP 3%", "Holiday rally lifts 3%.", "Bloomberg", False),
    ("5", "SPORT", "SKUBAL'S $450M METS DEAL", "Nine-year, largest ever.", "AP", False),
    ("6", "SPORT", "TOM JACKSON DIES AT 75", "Broncos LB, ESPN voice.", "ESPN", False),
    ("7", "LEGAL", "STATES SUE SPACEX", "Ten states sue over AI.", "AP", False),
    ("8", "TECH", "ANTHROPIC IPO: $107.3B", "Raised $83, closes $97.17.", "WSJ", False),
    ("9", "EUROPE", "POLAND: 3 MISSILES CROSSED AIRSPACE", "Kyiv: 3 Kh-101s crossed.", "AP", True),
    ("10", "SPACE", "RUSSIAN NUCLEAR SATELLITE", "May carry a nuke.", "Reuters", True),
]
CW, CG = 196, 7
for i, (num, cat, head, body, src, claim) in enumerate(cards):
    cx = 10 + (i % 5) * (CW + CG)
    cy = 424 + (i // 5) * 60
    d.rectangle([cx, cy, cx + CW, cy + 56], outline=(200, 192, 176), width=1)
    d.text((cx + 5, cy + 3), num, font=font(SANS_B, 10), fill=RED)
    d.text((cx + 22, cy + 3), cat, font=font(SANS_B, 9), fill=GREY)
    f_ch = fit(d, head, SANS_B, 10, CW - 10)
    hl = wrap(d, head, f_ch, CW - 10)
    hy = cy + 15
    for ln in hl[:1]:
        d.text((cx + 5, hy), ln, font=f_ch, fill=INK)
        hy += 12
    d.text((cx + 5, hy), body, font=font(SANS, 9), fill=(40, 40, 40))
    d.text((cx + 5, cy + 42), src, font=font(SANS, 8), fill=GREY)
    chip(d, cx + CW - 62, cy + 41, "CLAIM" if claim else "REPORTED", claim)

# ---- map + ALSO ----
d.rectangle([10, 548, 1014, 550], fill=INK)
d.text((10, 554), "WHERE IT HAPPENED", font=font(SANS_B, 13), fill=INK)
d.text((414, 554), "ALSO ON MONDAY", font=font(SANS_B, 13), fill=INK)
MAP = (10, 574, 400, 800)
# blobs (absolute coords)
d.polygon([(30, 590), (150, 580), (178, 612), (160, 668), (118, 706), (78, 726), (44, 694), (24, 642)],
          fill=(196, 222, 180), outline=(140, 170, 120))
d.polygon([(96, 730), (142, 724), (152, 762), (122, 796), (94, 780), (84, 748)],
          fill=(196, 222, 180), outline=(140, 170, 120))
d.polygon([(205, 586), (388, 580), (396, 642), (362, 692), (300, 704), (238, 682), (204, 644)],
          fill=(196, 222, 180), outline=(140, 170, 120))
d.polygon([(232, 708), (300, 702), (312, 758), (282, 796), (240, 782), (224, 742)],
          fill=(196, 222, 180), outline=(140, 170, 120))
pins = {
    1: (352, 622), 2: (80, 700), 3: (372, 606), 4: (66, 640), 5: (96, 622),
    6: (300, 612), 7: (246, 640), 8: (236, 626), 9: (268, 606), 10: (222, 606),
    11: (306, 664), 12: (288, 682), 13: (262, 736),
}
for n, (px, py) in pins.items():
    d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=(178, 34, 34), outline=(255, 255, 255), width=1)
    f_p = font(SANS_B, 9)
    tw = d.textlength(str(n), font=f_p)
    d.text((px - tw / 2, py - 6), str(n), font=f_p, fill=(255, 255, 255))
f_leg = font(SANS, 8)
d.text((10, 801), "Pins 1\u201313:  1 Seoul \u00b7 2 Bridgetown \u00b7 3 Beijing \u00b7 4 Washington \u00b7 5 New York \u00b7 6 Kyiv", font=f_leg, fill=GREY)
d.text((10, 812), "7 Paris \u00b7 8 London \u00b7 9 Warsaw \u00b7 10 Manchester \u00b7 11 Beirut \u00b7 12 Gaza \u00b7 13 Khartoum", font=f_leg, fill=GREY)
# ALSO list
also = [
    "Paris: 100+ back 2% billionaire tax", "Manchester: 12,000 cleared",
    "Zelenskyy: 165 Russian missiles in a week", "COP31: the day after Antalya pact rejected",
    "Israel unity talks resume", "Gaza: two killed in Israeli strike",
    "West Bank settler attacks", "Iran war: no deal in sight",
    "Lebanon seizes 264 kg explosives", "Bahrain: strike hits plant, 2 hurt",
    "Benghazi: UN demands probe [CLAIM]", "Sudan: defences down drones [CLAIM]",
    "DRC: fighting traps Ebola teams", "Bangladesh: Hasina jailed if she returns",
    "Seoul minister quits over AI exam chaos", "SK Telecom -7.3% as hype cools",
    "China eases margin rules", "Seoul readies 10T-won fund",
]
f_a = font(SANS, 11)
ay = 574
for i, item in enumerate(also):
    d.text((414, ay), f"{14 + i}. {item}", font=f_a, fill=INK)
    ay += 13

# ---- DATE CHECK red box ----
d.rectangle([10, 830, 1014, 918], outline=RED, width=2)
d.text((18, 836), "DATE CHECK  \u2014  READ 23 NOV 2026, 23:59 UTC  \u00b7  STORIES DATED 23 NOV ONLY",
       font=font(SANS_B, 11), fill=RED)
d.text((18, 854), "LEFT OUT \u2014 NOT 23 NOV:  Dems reach 258 (22 Nov)  \u00b7  Sparta II fire (22 Nov)  \u00b7  El Chapo Isidro captured (22 Nov)",
       font=font(SANS, 11), fill=INK)
d.text((18, 870), "EU\u2013Indonesia pact (21 Nov)  \u00b7  Nigeria boat (21 Nov)  \u00b7  ICJ Myanmar ruling (19 Nov)",
       font=font(SANS, 11), fill=INK)
d.text((18, 890), "NOT YET \u2014  Dymer search continues (14 missing)  \u00b7  4 House races uncalled  \u00b7  COP32 venue not set  \u00b7  WHO evacuating trapped Ebola staff",
       font=font(SANS, 11), fill=INK)

# ---- footer ----
d.text((10, 926), "Sources: Reuters \u00b7 AP \u00b7 Bloomberg \u00b7 AFP \u00b7 Yonhap \u00b7 BBC \u00b7 WSJ \u00b7 ESPN \u00b7 Lowy Institute (Asia Power Index 2026).",
       font=font(SANS, 10), fill=GREY)
d.text((10, 942), "CHIPS: REPORTED = confirmed by wires.  CLAIM = one side's claim, independently unconfirmed.  ONGOING = still developing.",
       font=font(SANS, 10), fill=GREY)
d.text((10, 958), "All times UTC. Figures as reported 23 Nov 2026. Scenes are drawn illustrations, not photographs.",
       font=font(SANS, 10), fill=GREY)
d.rectangle([10, 978, 1014, 980], fill=GOLD)
f_f = font(SANS_B, 12)
ft = "THE WORLD TODAY  \u00b7  Monday 23 November 2026  \u00b7  31 stories  \u00b7  6 regions"
d.text(((W - d.textlength(ft, font=f_f)) / 2, 988), ft, font=f_f, fill=GOLD)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out)
print("saved", out, os.path.getsize(out))
