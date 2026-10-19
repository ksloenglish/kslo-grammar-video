# -*- coding: utf-8 -*-
"""Quick look-and-layout mockups for Kayla's Grammar Lab (not final art)."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np, math

ROOT = "/home/ubuntu/kslo_grammar"
W, H = 1920, 1080
FRED = f"{ROOT}/fonts/Fredoka.ttf"
NUN = f"{ROOT}/fonts/Nunito.ttf"
LOGO = "/home/ubuntu/kslo-vocab-video/brand/logo_white.png"
KAYLA = f"{ROOT}/work/kayla_keyed_mock.png"

VIOLET_TOP, VIOLET_BOT = (21, 15, 51), (43, 20, 92)
CYAN, PINK, YELLOW, MINT = (46, 230, 255), (255, 79, 168), (255, 217, 61), (92, 242, 176)
WHITE = (255, 255, 255)


def font(path, size, var):
    f = ImageFont.truetype(path, size)
    f.set_variation_by_name(var)
    return f


def background():
    y = np.linspace(0, 1, H)[:, None, None]
    top, bot = np.array(VIOLET_TOP), np.array(VIOLET_BOT)
    base = (top * (1 - y) + bot * y) * np.ones((H, W, 3))
    img = Image.fromarray(base.astype(np.uint8)).convert("RGBA")
    blobs = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(blobs)
    d.ellipse((-200, 650, 600, 1350), fill=PINK + (70,))
    d.ellipse((1250, -300, 2150, 500), fill=CYAN + (55,))
    blobs = blobs.filter(ImageFilter.GaussianBlur(160))
    img = Image.alpha_composite(img, blobs)
    dots = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dd = ImageDraw.Draw(dots)
    for yy in range(30, H, 48):
        for xx in range(30, W, 48):
            dd.ellipse((xx - 2, yy - 2, xx + 2, yy + 2), fill=(255, 255, 255, 22))
    return Image.alpha_composite(img, dots)


def header(img, level_idx, level_name):
    d = ImageDraw.Draw(img)
    logo = Image.open(LOGO).convert("RGBA")
    LINE_TOP, LINE_BOT = 30, 88          # divider line; the logo matches its height exactly
    lh = LINE_BOT - LINE_TOP
    logo = logo.resize((round(logo.width * lh / logo.height), lh), Image.LANCZOS)
    img.alpha_composite(logo, (44, LINE_TOP))
    x = 44 + logo.width + 26
    d.line((x - 13, LINE_TOP, x - 13, LINE_BOT), fill=(255, 255, 255, 90), width=2)
    d.text((x, 22), "Kayla's Grammar Lab", font=font(FRED, 34, "Bold"), fill=WHITE)
    d.text((x, 62), "The present and the past", font=font(NUN, 24, "Bold"), fill=CYAN)
    # level progress
    f = font(FRED, 26, "SemiBold")
    label = level_name if level_name.startswith(("BOSS", "THE TENSE", "WELL DONE")) else f"LEVEL {level_idx} · {level_name}"
    tw = d.textlength(label, font=f)
    rx = W - 44
    dots_w = 4 * 26
    px1 = rx - dots_w - 20 - tw - 44
    d.rounded_rectangle((px1, 30, rx - dots_w - 20, 84), radius=27, fill=YELLOW + (255,))
    centred_text(d, (px1, 30, rx - dots_w - 20, 84), label, f, (40, 20, 80))
    for i in range(4):
        cx = rx - dots_w + 13 + i * 26
        col = YELLOW if i < level_idx else (255, 255, 255, 70)
        d.ellipse((cx - 8, 49, cx + 8, 65), fill=col)


def kayla(img, top_y, height_px, centre_x):
    k = Image.open(KAYLA).convert("RGBA")
    s = height_px / k.height
    k = k.resize((int(k.width * s), int(k.height * s)), Image.LANCZOS)
    img.alpha_composite(k, (int(centre_x - k.width / 2), int(top_y)))


_CMAPS = {}


def check_glyphs(text, f):
    """Fail loudly if the font cannot draw a character (Fredoka/Nunito lack arrows, ticks, crosses and circled
    numbers: draw those as shapes instead)."""
    from fontTools.ttLib import TTFont
    if f.path not in _CMAPS:
        _CMAPS[f.path] = set(TTFont(f.path).getBestCmap())
    missing = sorted({c for c in text if ord(c) not in _CMAPS[f.path] and not c.isspace()})
    if missing:
        raise ValueError(f"Font {f.path} cannot draw {missing} in {text!r}")


def centred_text(d, box, text, f, fill):
    """Draw text so its visible ink is centred in box (x1, y1, x2, y2), horizontally and vertically.
    Uses the real glyph bounding box, so capitals, ascenders and descenders all sit optically centred."""
    check_glyphs(text, f)
    l, t, r, b = d.textbbox((0, 0), text, font=f, anchor="ls")
    cx, cy = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2
    d.text((cx - (l + r) / 2, cy - (t + b) / 2), text, font=f, fill=fill, anchor="ls")


def pill(d, xy, text, f, bg, fg, padx=24):
    x, y = xy
    l, t, r, b = d.textbbox((0, 0), text, font=f, anchor="ls")
    hgt = f.size + 22
    w = (r - l) + 2 * padx
    d.rounded_rectangle((x, y, x + w, y + hgt), radius=hgt // 2, fill=bg)
    centred_text(d, (x, y, x + w, y + hgt), text, f, fg)
    return x + w


def snowflake(d, cx, cy, r, col):
    for k in range(3):
        a = math.pi * k / 3
        dx, dy = r * math.cos(a), r * math.sin(a)
        d.line((cx - dx, cy - dy, cx + dx, cy + dy), fill=col, width=4)


def teaching_frame():
    img = background()
    header(img, 1, "THE PRESENT")
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    d.rounded_rectangle((60, 130, 1170, 1030), radius=40, fill=(255, 255, 255, 20), outline=CYAN + (110,), width=3)
    img = Image.alpha_composite(img, ov)
    d = ImageDraw.Draw(img)
    pill(d, (110, 175), "PRESENT CONTINUOUS", font(FRED, 30, "Bold"), PINK, WHITE)
    # use badge
    d.ellipse((110, 270, 210, 370), fill=PINK)
    centred_text(d, (110, 270, 210, 370), "1", font(FRED, 64, "Bold"), WHITE)
    d.text((240, 283), "RIGHT NOW", font=font(FRED, 74, "Bold"), fill=WHITE)
    # sentence with highlight
    f = font(NUN, 80, "ExtraBold")
    x, y = 115, 450
    for part, col in (("Look! Snow ", WHITE), ("is falling", PINK), (".", WHITE)):
        d.text((x, y), part, font=f, fill=col)
        w = d.textlength(part, font=f)
        if col == PINK:
            d.rounded_rectangle((x, y + 104, x + w, y + 114), radius=5, fill=PINK)
        x += w
    # snow
    for cx, cy, r in ((900, 300, 22), (1010, 380, 16), (1060, 250, 26), (820, 400, 14)):
        snowflake(d, cx, cy, r, (255, 255, 255, 230))
    # timeline
    ty = 820
    d.line((140, ty, 1060, ty), fill=WHITE, width=6)
    d.polygon([(1060, ty - 16), (1090, ty), (1060, ty + 16)], fill=WHITE)
    lf = font(FRED, 30, "SemiBold")
    d.text((140, ty + 34), "PAST", font=lf, fill=(255, 255, 255, 200))
    d.text((940, ty + 34), "FUTURE", font=lf, fill=(255, 255, 255, 200))
    nx = 600
    d.rounded_rectangle((nx - 70, ty - 18, nx + 70, ty + 18), radius=18, fill=PINK)
    d.line((nx, ty - 70, nx, ty - 24), fill=CYAN, width=5)
    d.text((nx, ty - 96), "NOW", font=font(FRED, 34, "Bold"), fill=CYAN, anchor="mm")
    d.text((nx, ty + 70), "in progress right now", font=font(NUN, 30, "Bold"), fill=PINK, anchor="mm")
    # Kayla cut-out, bottom-right, about two thirds of the screen height, cut off by the bottom edge
    kayla(img, top_y=330, height_px=1000, centre_x=1660)
    return img.convert("RGB")


def popup_frame():
    img = background()
    header(img, 4, "BOSS QUIZ")
    d = ImageDraw.Draw(img)
    pill(d, (110, 190), "QUESTION 1 of 4", font(FRED, 32, "Bold"), YELLOW, (40, 20, 80))
    f = font(NUN, 72, "ExtraBold")
    d.text((110, 330), "Look! The baby", font=f, fill=WHITE)
    # answer blank: one solid line (never underscores, which render as a dotted line)
    bx, by, blen = 115, 430 + 82, 300
    d.rounded_rectangle((bx, by, bx + blen, by + 8), radius=4, fill=WHITE)
    d.text((bx + blen + 22, 430), "(sleep).", font=f, fill=WHITE)
    x2 = pill(d, (110, 590), "is sleeping", font(NUN, 64, "ExtraBold"), PINK, WHITE)
    d.ellipse((x2 + 24, 596, x2 + 110, 682), fill=MINT)
    d.line((x2 + 46, 640, x2 + 63, 659, x2 + 92, 616), fill=(20, 60, 40), width=10)
    pill(d, (110, 740), "Look! = right now", font(FRED, 36, "SemiBold"), (30, 70, 110), CYAN)
    # Kayla pops up large on the right
    kayla(img, top_y=110, height_px=1350, centre_x=1460)
    return img.convert("RGB")


def wide_frame():
    """A scene that needs more width: Kayla shrinks into the corner (head and shoulders)."""
    img = background()
    header(img, 0, "THE TENSE MAP")
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    d.rounded_rectangle((60, 130, 1400, 1030), radius=40, fill=(255, 255, 255, 20), outline=CYAN + (110,), width=3)
    img = Image.alpha_composite(img, ov)
    d = ImageDraw.Draw(img)
    hf, cf, ef = font(FRED, 40, "Bold"), font(FRED, 38, "SemiBold"), font(NUN, 46, "ExtraBold")
    x0, y0, cw, ch, rw = 310, 300, 520, 300, 230
    # column heads
    for i, (t, col) in enumerate((("SIMPLE", YELLOW), ("CONTINUOUS", PINK))):
        cx = x0 + i * (cw + 30) + cw // 2
        d.text((cx, 215), t, font=hf, fill=col, anchor="mm")
        if i == 0:
            for k in range(3):
                d.ellipse((cx - 70 + k * 60, 245, cx - 46 + k * 60, 269), fill=YELLOW)
        else:
            d.rounded_rectangle((cx - 90, 248, cx + 90, 266), radius=9, fill=PINK)
    cells = [[("simple present", "I play"), ("present continuous", "I am playing")],
             [("simple past", "I played"), ("past continuous", "I was playing")]]
    for r, row in enumerate(("PRESENT", "PAST")):
        cy = y0 + r * (ch + 30)
        d.text((x0 - 40, cy + ch // 2), row, font=hf, fill=WHITE, anchor="rm")
        for c in range(2):
            col = YELLOW if c == 0 else PINK
            xx = x0 + c * (cw + 30)
            d.rounded_rectangle((xx, cy, xx + cw, cy + ch), radius=30, fill=col + (255,))
            name, ex = cells[r][c]
            d.text((xx + cw // 2, cy + 95), name, font=cf, fill=(40, 20, 80), anchor="mm")
            d.text((xx + cw // 2, cy + 185), ex, font=ef, fill=(40, 20, 80), anchor="mm")
    kayla(img, top_y=700, height_px=560, centre_x=1730)
    return img.convert("RGB")


if __name__ == "__main__":
    a, w, b = teaching_frame(), wide_frame(), popup_frame()
    a.save(f"{ROOT}/work/mock_teaching.jpg", quality=92)
    w.save(f"{ROOT}/work/mock_wide.jpg", quality=92)
    b.save(f"{ROOT}/work/mock_popup.jpg", quality=92)
    tw, th = 1280, 720
    pad, lab = 30, 80
    # header close-up: before and after (both crops 760 x 120, shown at 1.6x)
    before = Image.open(f"{ROOT}/work/hdr_before.png").convert("RGB")
    after = a.crop((0, 0, 760, 120))
    z = 1.6
    hb = [im.resize((int(760 * z), int(120 * z)), Image.LANCZOS) for im in (before, after)]
    strip_h = lab + hb[0].height + 50 + hb[1].height + pad
    sheet = Image.new("RGB", (tw + 2 * pad, strip_h + 3 * (th + lab) + 4 * pad), (16, 10, 36))
    d = ImageDraw.Draw(sheet)
    y = pad
    d.text((pad, y + 18), "Header close-up: logo now the same height as the divider line", font=font(NUN, 34, "Bold"), fill=YELLOW)
    y += lab
    for im, tag in zip(hb, ("Before", "After")):
        sheet.paste(im, (pad + 130, y))
        d.text((pad, y + im.height // 2), tag, font=font(NUN, 32, "Bold"), fill=WHITE, anchor="lm")
        y += im.height + 25
    y += pad
    for im, cap in ((a, "1. Explaining (most of the video): cut-out Kayla, bottom-right, talking and reacting"),
                    (w, "2. Scenes that need more space: Kayla shrinks into the corner"),
                    (b, "3. Pop-up moments (hook, level-ups, quiz answers): she slides in larger")):
        d.text((pad, y + 18), cap, font=font(NUN, 34, "Bold"), fill=YELLOW)
        sheet.paste(im.resize((tw, th), Image.LANCZOS), (pad, y + lab))
        y += th + lab + pad
    sheet.save(f"{ROOT}/output/Kayla_onscreen_mockup_v2.jpg", quality=90)
    print("ok", sheet.size)
