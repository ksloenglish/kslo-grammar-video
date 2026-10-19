# -*- coding: utf-8 -*-
"""Same teaching screen in three motion-graphics styles, for the teacher to choose (look only, not final art)."""
import sys, math
sys.path.insert(0, "/home/ubuntu/kslo_grammar/scripts")
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
import mockup_layout as M

W, H = M.W, M.H
ROOT = M.ROOT
PIX = f"{ROOT}/fonts/PressStart2P.ttf"
INK = (43, 20, 88)            # dark outline colour for the sticker style
PINK, CYAN, YELLOW, WHITE, MINT = M.PINK, M.CYAN, M.YELLOW, M.WHITE, M.MINT
from PIL import ImageFont


def pix(size):
    return ImageFont.truetype(PIX, size)


def logo_block(img, title_font, title_fill, sub_font, sub_fill, title_text="Kayla's Grammar Lab",
               stroke=0, stroke_fill=None, line_fill=(255, 255, 255, 110)):
    """Logo at the same height as the divider line (approved rule), drawn as-is with nothing behind it."""
    d = ImageDraw.Draw(img)
    top, bot = 30, 88
    logo = Image.open(M.LOGO).convert("RGBA")
    lh = bot - top
    logo = logo.resize((round(logo.width * lh / logo.height), lh), Image.LANCZOS)
    img.alpha_composite(logo, (44, top))
    x = 44 + logo.width + 26
    d.line((x - 13, top, x - 13, bot), fill=line_fill, width=2)
    d.text((x, 24), title_text, font=title_font, fill=title_fill, stroke_width=stroke, stroke_fill=stroke_fill)
    d.text((x, 63), "The present and the past", font=sub_font, fill=sub_fill, stroke_width=stroke and 2,
           stroke_fill=stroke_fill)


def paste_kayla(img, top_y, height_px, centre_x, outline=0, shadow=False):
    k = Image.open(M.KAYLA).convert("RGBA")
    s = height_px / k.height
    k = k.resize((int(k.width * s), int(k.height * s)), Image.LANCZOS)
    pad = outline + 20
    canvas = Image.new("RGBA", (k.width + 2 * pad, k.height + 2 * pad), (0, 0, 0, 0))
    canvas.alpha_composite(k, (pad, pad))
    x, y = int(centre_x - canvas.width / 2), int(top_y - pad)
    a = canvas.split()[-1]
    if shadow:
        sh = Image.new("RGBA", canvas.size, INK + (0,))
        sh.putalpha(a.filter(ImageFilter.MaxFilter(2 * outline + 1)).point(lambda v: 150 if v > 40 else 0))
        img.alpha_composite(sh, (x + 12, y + 12))
    if outline:
        die = Image.new("RGBA", canvas.size, WHITE + (0,))
        die.putalpha(a.filter(ImageFilter.MaxFilter(2 * outline + 1)).point(lambda v: 255 if v > 40 else 0))
        img.alpha_composite(die, (x, y))
    img.alpha_composite(canvas, (x, y))


# ---------------------------------------------------------------- A: Neon Stream (current look)
def style_a():
    return M.teaching_frame()


# ---------------------------------------------------------------- B: Candy Sticker Pop
def style_b():
    yy, xx = np.mgrid[0:H, 0:W]
    t = ((xx / W) * 0.65 + (yy / H) * 0.35)[..., None]
    c1, c2 = np.array((124, 77, 255)), np.array((255, 95, 162))
    img = Image.fromarray((c1 * (1 - t) + c2 * t).astype(np.uint8)).convert("RGBA")
    dots = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dd = ImageDraw.Draw(dots)
    for j, y in enumerate(range(20, H, 70)):
        for x in range(20 + (35 if j % 2 else 0), W, 70):
            dd.ellipse((x - 5, y - 5, x + 5, y + 5), fill=(255, 255, 255, 38))
    img = Image.alpha_composite(img, dots)
    d = ImageDraw.Draw(img)
    logo_block(img, M.font(M.FRED, 34, "Bold"), WHITE, M.font(M.NUN, 24, "ExtraBold"), (255, 240, 150),
               stroke=3, stroke_fill=INK, line_fill=(255, 255, 255, 200))
    # level chip as a sticker
    f = M.font(M.FRED, 26, "Bold")
    label = "LEVEL 1 · THE PRESENT"
    tw = d.textlength(label, font=f)
    x2 = W - 44 - 4 * 26 - 20
    x1 = x2 - tw - 44
    d.rounded_rectangle((x1 + 6, 36, x2 + 6, 90), radius=27, fill=INK)
    d.rounded_rectangle((x1, 30, x2, 84), radius=27, fill=YELLOW, outline=INK, width=4)
    d.text((x1 + 22, 42), label, font=f, fill=INK)
    for i in range(4):
        cx = W - 44 - 4 * 26 + 13 + i * 26
        d.ellipse((cx - 9, 48, cx + 9, 66), fill=YELLOW if i < 1 else (255, 255, 255, 120), outline=INK, width=3)
    # main sticker card with hard shadow
    d.rounded_rectangle((74, 144, 1184, 1044), radius=40, fill=INK)
    d.rounded_rectangle((60, 130, 1170, 1030), radius=40, fill=WHITE, outline=INK, width=6)
    # chip
    cf = M.font(M.FRED, 30, "Bold")
    cw = d.textlength("PRESENT CONTINUOUS", font=cf)
    d.rounded_rectangle((110, 175, 110 + cw + 44, 227), radius=26, fill=PINK, outline=INK, width=4)
    d.text((132, 182), "PRESENT CONTINUOUS", font=cf, fill=WHITE)
    d.ellipse((110, 270, 210, 370), fill=PINK, outline=INK, width=5)
    d.text((160, 320), "1", font=M.font(M.FRED, 64, "Bold"), fill=WHITE, anchor="mm", stroke_width=3, stroke_fill=INK)
    d.text((240, 283), "RIGHT NOW", font=M.font(M.FRED, 74, "Bold"), fill=INK)
    # sentence; continuous verb in pink with a marker squiggle
    f = M.font(M.NUN, 80, "ExtraBold")
    x, y = 115, 450
    for part, col in (("Look! Snow ", INK), ("is falling", PINK), (".", INK)):
        d.text((x, y), part, font=f, fill=col)
        w = d.textlength(part, font=f)
        if col == PINK:
            pts = [(x + i, y + 112 + 7 * math.sin(i / 14)) for i in range(0, int(w), 4)]
            d.line(pts, fill=PINK, width=8, joint="curve")
        x += w
    for cx, cy, r in ((900, 300, 24), (1010, 380, 18), (1060, 250, 28), (820, 400, 15)):
        for k in range(3):
            a = math.pi * k / 3
            d.line((cx - r * math.cos(a), cy - r * math.sin(a), cx + r * math.cos(a), cy + r * math.sin(a)),
                   fill=(120, 200, 255), width=7)
    ty = 820
    d.line((140, ty, 1060, ty), fill=INK, width=7)
    d.polygon([(1058, ty - 18), (1092, ty), (1058, ty + 18)], fill=INK)
    lf = M.font(M.FRED, 30, "Bold")
    d.text((140, ty + 34), "PAST", font=lf, fill=INK)
    d.text((940, ty + 34), "FUTURE", font=lf, fill=INK)
    nx = 600
    d.rounded_rectangle((nx - 72, ty - 20, nx + 72, ty + 20), radius=20, fill=PINK, outline=INK, width=4)
    d.line((nx, ty - 70, nx, ty - 26), fill=(124, 77, 255), width=6)
    d.text((nx, ty - 96), "NOW", font=M.font(M.FRED, 34, "Bold"), fill=(124, 77, 255), anchor="mm")
    d.text((nx, ty + 72), "in progress right now", font=M.font(M.NUN, 30, "ExtraBold"), fill=PINK, anchor="mm")
    paste_kayla(img, top_y=330, height_px=1000, centre_x=1660, outline=10, shadow=True)
    return img.convert("RGB")


# ---------------------------------------------------------------- C: Arcade Level-Up (pixel game HUD)
def style_c():
    img = Image.new("RGBA", (W, H), (11, 14, 36, 255))
    d = ImageDraw.Draw(img)
    for x in range(0, W, 40):
        d.line((x, 0, x, H), fill=(60, 80, 160, 40), width=1)
    for y in range(0, H, 40):
        d.line((0, y, W, y), fill=(60, 80, 160, 40), width=1)
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse((1150, 200, 2150, 1300), fill=(120, 60, 255, 70))
    img = Image.alpha_composite(img, glow.filter(ImageFilter.GaussianBlur(140)))
    d = ImageDraw.Draw(img)
    logo_block(img, pix(22), WHITE, M.font(M.NUN, 24, "ExtraBold"), CYAN, title_text="KAYLA'S GRAMMAR LAB")
    # HUD: level and segmented XP bar
    d.text((1290, 34), "LV 1", font=pix(22), fill=YELLOW)
    d.text((1290, 66), "THE PRESENT", font=pix(14), fill=WHITE)
    for i in range(10):
        x = 1500 + i * 38
        d.rectangle((x, 40, x + 30, 74), fill=YELLOW if i < 3 else (40, 50, 100), outline=(255, 255, 255, 90))
    d.text((1500, 82), "XP", font=pix(12), fill=(180, 190, 255))

    def pixel_frame(x1, y1, x2, y2, col, step=12, width=6):
        d.rectangle((x1 + step, y1 + step, x2 - step, y2 - step), fill=(18, 22, 60, 235))
        d.rectangle((x1 + step, y1, x2 - step, y1 + width), fill=col)
        d.rectangle((x1 + step, y2 - width, x2 - step, y2), fill=col)
        d.rectangle((x1, y1 + step, x1 + width, y2 - step), fill=col)
        d.rectangle((x2 - width, y1 + step, x2, y2 - step), fill=col)
        for (cx, cy) in ((x1 + width, y1 + width), (x2 - step, y1 + width), (x1 + width, y2 - step), (x2 - step, y2 - step)):
            d.rectangle((cx, cy, cx + step - width, cy + step - width), fill=col)
        d.rectangle((x1 + width, y1 + step, x2 - width, y2 - step), fill=(18, 22, 60, 235))
        d.rectangle((x1 + step, y1 + width, x2 - step, y2 - width), fill=(18, 22, 60, 235))

    pixel_frame(60, 130, 1170, 1030, CYAN)
    # chip
    d.rectangle((110, 178, 110 + 470, 226), fill=PINK)
    d.text((126, 190), "PRESENT CONTINUOUS", font=pix(22), fill=WHITE)
    d.rectangle((110, 275, 200, 365), fill=PINK)
    d.text((155, 322), "1", font=pix(48), fill=WHITE, anchor="mm")
    d.text((235, 296), "RIGHT NOW", font=pix(50), fill=YELLOW)
    f = M.font(M.NUN, 80, "ExtraBold")
    x, y = 115, 450
    for part, col in (("Look! Snow ", WHITE), ("is falling", PINK), (".", WHITE)):
        d.text((x, y), part, font=f, fill=col)
        w = d.textlength(part, font=f)
        if col == PINK:
            d.rectangle((x, y + 106, x + w, y + 116), fill=PINK)          # solid, never dashed
        x += w
    d.rectangle((x + 10, y + 18, x + 46, y + 100), fill=(255, 255, 255, 200))  # blinking cursor block
    for cx, cy, r in ((900, 300, 6), (1010, 380, 5), (1060, 250, 7), (820, 400, 4)):
        for dx, dy in ((0, 0), (-1, 0), (1, 0), (0, -1), (0, 1), (-2, -2), (2, 2), (2, -2), (-2, 2)):
            d.rectangle((cx + dx * r * 2, cy + dy * r * 2, cx + dx * r * 2 + r * 2, cy + dy * r * 2 + r * 2),
                        fill=(200, 230, 255))
    ty = 820
    d.rectangle((140, ty - 4, 1060, ty + 4), fill=WHITE)              # solid timeline
    d.polygon([(1058, ty - 18), (1090, ty), (1058, ty + 18)], fill=WHITE)
    d.text((140, ty + 36), "PAST", font=pix(20), fill=(200, 205, 255))
    d.text((960, ty + 36), "FUTURE", font=pix(20), fill=(200, 205, 255))
    nx = 600
    d.rectangle((nx - 72, ty - 18, nx + 72, ty + 18), fill=PINK)
    d.rectangle((nx - 3, ty - 70, nx + 3, ty - 24), fill=CYAN)
    d.text((nx, ty - 96), "NOW", font=pix(26), fill=CYAN, anchor="mm")
    d.text((nx, ty + 72), "in progress right now", font=M.font(M.NUN, 30, "ExtraBold"), fill=PINK, anchor="mm")
    paste_kayla(img, top_y=330, height_px=1000, centre_x=1660)
    d = ImageDraw.Draw(img)
    d.rectangle((1560, 1000, 1760, 1040), fill=(11, 14, 36, 220), outline=CYAN, width=3)
    d.text((1660, 1021), "P1 KAYLA", font=pix(16), fill=CYAN, anchor="mm")
    # CRT scanlines
    sl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sl)
    for y in range(0, H, 4):
        sd.line((0, y, W, y), fill=(0, 0, 0, 34), width=1)
    img = Image.alpha_composite(img, sl)
    return img.convert("RGB")


if __name__ == "__main__":
    frames = [
        (style_a(), "Style A · Neon Stream",
         "Dark violet, glassy panels, neon glow. Motion: smooth glides, soft glow pulses, glitch-wipe transitions."),
        (style_b(), "Style B · Candy Sticker Pop",
         "Bright candy gradient, white sticker cards with bold outlines. Motion: bouncy slap-on stickers, wiggles, doodles drawing on."),
        (style_c(), "Style C · Arcade Level-Up",
         "Retro game screen, pixel headings, XP bar. Motion: blocks snap in, typewriter text with blips, 8-bit LEVEL UP flashes."),
    ]
    tw, th, pad, lab = 1280, 720, 30, 135
    sheet = Image.new("RGB", (tw + 2 * pad, len(frames) * (th + lab + pad) + pad), (16, 10, 36))
    d = ImageDraw.Draw(sheet)
    y = pad
    for i, (im, title, desc) in enumerate(frames):
        im.save(f"{ROOT}/work/style_{'abc'[i]}.jpg", quality=92)
        d.text((pad, y + 10), title, font=M.font(M.FRED, 42, "Bold"), fill=YELLOW)
        df = M.font(M.NUN, 25, "Bold")
        words, line, lines = desc.split(), "", []
        for wd in words:                      # wrap to the sheet width
            trial = (line + " " + wd).strip()
            if d.textlength(trial, font=df) > tw:
                lines.append(line); line = wd
            else:
                line = trial
        lines.append(line)
        assert len(lines) <= 2, desc
        for k, ln in enumerate(lines):
            d.text((pad, y + 60 + k * 30), ln, font=df, fill=WHITE)
        sheet.paste(im.resize((tw, th), Image.LANCZOS), (pad, y + lab))
        y += th + lab + pad
    sheet.save(f"{ROOT}/output/Motion_graphics_style_options.jpg", quality=90)
    print("ok", sheet.size)
