# -*- coding: utf-8 -*-
"""Outro 'WELL DONE!' card mockup (Style A). The chips list the unit's GRAMMAR POINTS as named in the source
pages, never teaching devices (Tense Map, Give me five, No -ing Zone, level names)."""
import sys
sys.path.insert(0, "/home/ubuntu/kslo_grammar/scripts")
from PIL import Image, ImageDraw
import mockup_layout as M

INK = (40, 20, 80)
# (title, sub-line, background, text colour) - row by row, mirroring the Tense Map
CHIPS = [
    ("Simple present", "I play", M.YELLOW, INK),
    ("Present continuous", "I am playing", M.PINK, M.WHITE),
    ("Simple past", "I played", M.YELLOW, INK),
    ("Past continuous", "I was playing", M.PINK, M.WHITE),
    ("Non-action verbs", "like · want · know · have …", M.CYAN, INK),
    ("Tenses in stories", "story: past · synopsis: present", M.CYAN, INK),
]


def outro_frame():
    img = M.background()
    M.header(img, 4, "WELL DONE!")
    ov = Image.new("RGBA", (M.W, M.H), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    od.rounded_rectangle((60, 130, 1170, 1030), radius=40, fill=(255, 255, 255, 20), outline=M.CYAN + (110,), width=3)
    img = Image.alpha_composite(img, ov)
    d = ImageDraw.Draw(img)
    M.centred_text(d, (60, 165, 1170, 285), "WELL DONE!", M.font(M.FRED, 104, "Bold"), M.YELLOW)
    M.centred_text(d, (60, 290, 1170, 345), "Today's key points", M.font(M.NUN, 38, "Bold"), M.WHITE)
    cw, ch, gx, gy, x0, y0 = 480, 170, 30, 26, 120, 385
    tf, sf = M.font(M.FRED, 44, "Bold"), M.font(M.NUN, 30, "ExtraBold")
    for i, (t, sub, bg, fg) in enumerate(CHIPS):
        r, c = divmod(i, 2)
        x, y = x0 + c * (cw + gx), y0 + r * (ch + gy)
        d.rounded_rectangle((x, y, x + cw, y + ch), radius=34, fill=bg)
        M.centred_text(d, (x, y + 22, x + cw, y + 92), t, tf, fg)
        M.centred_text(d, (x, y + 98, x + cw, y + 148), sub, sf, fg)
    M.kayla(img, top_y=330, height_px=1000, centre_x=1660)
    return img.convert("RGB")


if __name__ == "__main__":
    im = outro_frame()
    im.save(f"{M.ROOT}/output/Outro_card_mockup.jpg", quality=92)
    print("ok", im.size)
