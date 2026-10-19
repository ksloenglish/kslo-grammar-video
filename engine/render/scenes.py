# -*- coding: utf-8 -*-
"""All scenes of 'Kayla's Grammar Lab - The present and the past' (approved body script v1)."""
import math, functools, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import gl
from gl import (place, clamp, e_out, e_inout, e_back, W, H, ROOT, F, CYAN, PINK, YELLOW, MINT, WHITE, INK, RED,
                ORANGE, NAVY, DIM, text_img, pill_img, para, icon, tick_img, cross_img, circle_num, arrow_img, glow)
from engine import Scene, E, Fn, Fly

CLIPS = f"{ROOT}/clips/retimed"
REFS = f"{ROOT}/audio/refs"
LVL = {1: "THE PRESENT", 2: "THE PAST", 3: "NON-ACTION VERBS", 4: "TENSES IN STORIES"}
LABEL = {n: f"LEVEL {n} · {v}" for n, v in LVL.items()}


# ============================================================================ helpers
def fit(text, maxw, size, kind="fred", weight="Bold", **kw):
    while True:
        im = text_img(text, size, kind, weight, **kw)
        if im.width <= maxw or size <= 20:
            return im
        size -= 2


def block(text, size=44, outline=CYAN, fill_a=34, padx=26, h=None, fg=WHITE, kind="nun", weight="ExtraBold"):
    f = F(kind, size, weight)
    gl.check_glyphs(text, f)
    d0 = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    l, t, r, b = d0.textbbox((0, 0), text, font=f, anchor="ls")
    hh = h or int(size * 1.7)
    img = Image.new("RGBA", (r - l + 2 * padx, hh), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((1, 1, img.width - 2, hh - 2), radius=18, fill=(255, 255, 255, fill_a), outline=outline + (230,),
                        width=4)
    gl.centred_text(d, (0, 0, img.width, hh), text, f, fg)
    return img


def card(w, h, col, fill_a=34, radius=30, width=4):
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(img).rounded_rectangle((2, 2, w - 3, h - 3), radius=radius, fill=col + (fill_a,),
                                          outline=col + (220,), width=width)
    return img


def chip(text, col=CYAN, bg=NAVY, size=30, **kw):
    return pill_img(text, size, bg, col, kind="nun", weight="ExtraBold", **kw)


def xp_img(frac, w=760):
    img = Image.new("RGBA", (w + 140, 60), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.text((0, 6), "XP", font=F("fred", 40, "Bold"), fill=YELLOW)
    d.rounded_rectangle((80, 10, 80 + w, 50), radius=20, fill=(255, 255, 255, 30), outline=(255, 255, 255, 120), width=3)
    if frac > 0.005:
        d.rounded_rectangle((86, 16, 86 + max(28, (w - 12) * frac), 44), radius=14, fill=YELLOW)
    return img


def strike(x0, y, x1, t, col=RED, th=8, dur=0.35):
    def f(fr, tt, p):
        d = ImageDraw.Draw(fr)
        d.rounded_rectangle((x0, y - th // 2, x0 + (x1 - x0) * e_out(p), y + th // 2), radius=th // 2, fill=col)
    return Fn(f, t, dur)


def ring(cx, cy, t, col=YELLOW, r0=10, r1=60, dur=0.5, width=5):
    def f(fr, tt, p):
        if p >= 1:
            return
        d = ImageDraw.Draw(fr)
        r = r0 + (r1 - r0) * e_out(p)
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=col + (int(255 * (1 - p)),), width=width)
    return Fn(f, t, dur, t + dur)


def sparkle_burst(cx, cy, t, n=10, rad=140, col=YELLOW, dur=0.7, seed=1):
    rng = random.Random(seed)
    pts = [(rng.uniform(0, 2 * math.pi), rng.uniform(0.6, 1.0), rng.choice([YELLOW, CYAN, PINK, WHITE])) for _ in range(n)]

    def f(fr, tt, p):
        if p >= 1:
            return
        d = ImageDraw.Draw(fr)
        for a, k, c in pts:
            r = rad * k * e_out(p); x, y = cx + r * math.cos(a), cy + r * math.sin(a)
            s = 10 * (1 - p) + 3
            al = int(255 * (1 - p))
            d.polygon([(x, y - 2 * s), (x + s * 0.5, y - s * 0.5), (x + 2 * s, y), (x + s * 0.5, y + s * 0.5), (x, y + 2 * s),
                       (x - s * 0.5, y + s * 0.5), (x - 2 * s, y), (x - s * 0.5, y - s * 0.5)], fill=c + (al,))
    return Fn(f, t, dur, t + dur)


class ParaStates:
    """A paragraph whose tracked words light up (colour + underline + glow) at given times, in order."""
    def __init__(self, text, size, width, x, y, colors, order, t_in=0.0, anim="up", kind="nun", weight="ExtraBold",
                 fill=WHITE, line_gap=1.28, glow_on=True):
        self.x, self.y, self.t_in, self.anim, self.order, self.colors = x, y, t_in, anim, order, colors
        self.kw = dict(kind=kind, weight=weight, fill=fill, line_gap=line_gap)
        self.text, self.size, self.width, self.glow_on = text, size, width, glow_on
        self.base, self.boxes = para(text, size, width, colors={}, **self.kw)
        self.cache = {}

    def img(self, n):
        if n not in self.cache:
            keys = {k for k, _ in self.order[:n]}
            self.cache[n] = para(self.text, self.size, self.width, colors={k: self.colors[k] for k in keys}, **self.kw)[0]
        return self.cache[n]

    def box(self, k):
        b = self.boxes[k]
        return (self.x + b[0], self.y + b[1], self.x + b[2], self.y + b[3])

    def centre(self, k):
        b = self.box(k); return ((b[0] + b[2]) / 2, (b[1] + b[3]) / 2)

    def draw(self, fr, t):
        if t < self.t_in:
            return
        p = clamp((t - self.t_in) / 0.35)
        n = sum(1 for _, tt in self.order if t >= tt)
        dy = 40 * (1 - e_out(p)) if self.anim == "up" else 0
        if self.glow_on:
            for k, tt in self.order:
                q = (t - tt) / 0.6
                if 0 <= q < 1:
                    c = self.colors[k]
                    d = ImageDraw.Draw(fr)
                    pad = 10 + 8 * q
                    for b0 in self.boxes.get("_lines", {}).get(k) or [self.boxes[k]]:
                        b = (self.x + b0[0], self.y + b0[1], self.x + b0[2], self.y + b0[3])
                        d.rounded_rectangle((b[0] - pad, b[1] - pad * 0.4 + dy, b[2] + pad,
                                             b[3] - self.size * 0.15 + pad * 0.4 + dy),
                                            radius=14, fill=c + (int(90 * (1 - q)),))
        place(fr, self.img(n), self.x, self.y + dy, "lt", e_out(p * 1.4))


def hand_img_old(lit=0, size=300):
    """Cartoon hand (pink) with five numbered fingertips; the first `lit` tips glow yellow."""
    S = 400
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    pc = (200, 270)
    fingers = [(-62, 105), (-20, 135), (-3, 148), (13, 135), (30, 108)]
    tips = []
    for ang, ln in fingers:
        a = math.radians(ang)
        bx, by = pc[0] + 52 * math.sin(a), pc[1] - 40
        if ang == -62:
            bx, by = pc[0] - 50, pc[1] + 10
        ex, ey = bx + ln * math.sin(a), by - ln * math.cos(a)
        d.line((bx, by, ex, ey), fill=PINK, width=46)
        d.ellipse((ex - 23, ey - 23, ex + 23, ey + 23), fill=PINK)
        tips.append((ex, ey))
    d.rounded_rectangle((pc[0] - 82, pc[1] - 70, pc[0] + 82, pc[1] + 90), radius=60, fill=PINK)
    for i, (x, y) in enumerate(tips):
        c = YELLOW if i < lit else WHITE
        d.ellipse((x - 21, y - 21, x + 21, y + 21), fill=c)
        gl.centred_text(d, (x - 21, y - 21, x + 21, y + 21), str(i + 1), F("fred", 28, "Bold"), INK)
    img = glow(img, 12, PINK, 0.8)
    s = size / img.height
    return img.resize((round(img.width * s), size), Image.LANCZOS)


def padlock(size=46, col=WHITE):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.arc((size * 0.22, size * 0.05, size * 0.78, size * 0.6), 180, 360, fill=col, width=max(3, size // 9))
    d.line((size * 0.22, size * 0.33, size * 0.22, size * 0.5), fill=col, width=max(3, size // 9))
    d.line((size * 0.78, size * 0.33, size * 0.78, size * 0.5), fill=col, width=max(3, size // 9))
    d.rounded_rectangle((size * 0.12, size * 0.45, size * 0.88, size * 0.95), radius=6, fill=col)
    return img


from hand import hand_img          # round 3: natural hand, smooth edges (render/hand.py)


def name_tag():
    """Game-style nameplate for Kayla: cat-ear corners (echo her headphones), star (echo her hair clip), pointer."""
    W_, H_, top = 440, 122, 26
    img = Image.new("RGBA", (W_ + 8, top + H_ + 30), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for x0 in (52, W_ - 52 - 50):                                   # cat ears behind the plate
        d.polygon([(x0, top + 14), (x0 + 22, 2), (x0 + 50, top + 10)], fill=PINK)
        d.polygon([(x0 + 12, top + 10), (x0 + 23, 12), (x0 + 38, top + 8)], fill=(255, 180, 220))
    d.rounded_rectangle((4, top, W_ + 3, top + H_), radius=36, fill=NAVY + (255,), outline=PINK, width=5)
    cx = (W_ + 8) // 2                                              # pointer towards her head
    d.polygon([(cx - 20, top + H_ - 6), (cx, top + H_ + 24), (cx + 20, top + H_ - 6)], fill=NAVY + (255,))
    d.line([(cx - 22, top + H_ - 1), (cx, top + H_ + 25), (cx + 22, top + H_ - 1)], fill=PINK, width=5, joint="curve")
    nm = text_img("KAYLA", 54, glow_r=6, glow_col=PINK)
    sub = text_img("your grammar study buddy", 25, "nun", "ExtraBold", fill=CYAN)
    star = Image.new("RGBA", (44, 44), (0, 0, 0, 0)); ds = ImageDraw.Draw(star)
    pts = [(22 + (20 if k % 2 == 0 else 8.5) * math.sin(k * math.pi / 5), 23 - (20 if k % 2 == 0 else 8.5) * math.cos(k * math.pi / 5)) for k in range(10)]
    ds.polygon(pts, fill=YELLOW)
    gw = star.width + 12 + nm.width - 2 * nm.info["gpad"]
    x = cx - gw // 2
    img.alpha_composite(star, (x, top + 20))
    img.alpha_composite(nm, (x + star.width + 12 - nm.info["gpad"], top + 14 - nm.info["gpad"] + 4))
    img.alpha_composite(sub, (cx - sub.width // 2, top + 76))
    return glow(img, 10, PINK, 0.55)


def tip_img(kw, rest, size=27):
    """'TIP' pill + 'Use <kw> <rest>' with the keyword in cyan, pill centred on the text line."""
    p, boxes = para("Use {" + kw + "|k} " + rest, size, 760, weight="ExtraBold", colors={"k": CYAN})
    pill = pill_img("TIP", 20, YELLOW, INK, h=34, padx=12)
    y0, y1 = boxes["k"][1], boxes["k"][3]
    line_c = y0 + (y1 - y0) * 0.45
    h = max(p.height, pill.height + 8)
    im = Image.new("RGBA", (pill.width + 14 + p.width, h), (0, 0, 0, 0))
    im.alpha_composite(pill, (0, max(0, int(line_c - pill.height / 2))))
    im.alpha_composite(p, (pill.width + 14, 0))
    return im


def ink_bounds(img, thr=110):
    a = np.array(img)[:, :, 3] > thr
    xs, ys = np.where(a.any(0))[0], np.where(a.any(1))[0]
    return xs[0], ys[0], xs[-1] + 1, ys[-1] + 1


def neon_sign(text, size=54, col=PINK):
    f = F("fred", size, "Bold")
    d0 = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    l, t, r, b = d0.textbbox((0, 0), text, font=f, anchor="ls")
    w, h = r - l + size * 1.2, int(size * 1.9)
    img = Image.new("RGBA", (int(w), h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((3, 3, w - 4, h - 4), radius=h // 3, outline=col, width=5)
    gl.centred_text(d, (0, 0, w, h), text, f, col)
    return glow(img, 10, col, 0.7)


def flicker(el, t0, dur=0.7, seed=3):
    """Neon flicker: element alpha jumps during [t0, t0+dur]."""
    rng = random.Random(seed)
    seq = [rng.random() < 0.55 for _ in range(40)]

    def f(fr, t, p):
        if t < t0:
            return
        on = True
        if t < t0 + dur:
            on = seq[int((t - t0) / dur * 39)]
        if on:
            place(fr, el[0], el[1], el[2], el[3], 1.0)
    return Fn(f, t0, dur)


def countdown(s, cx, cy, t0):
    for i, n in enumerate((3, 2, 1)):
        img = glow(circle_num(n, 150, NAVY, YELLOW, 100), 12, CYAN)
        s.add(E(img, cx, cy, "mm", t0 + i, "pop", 0.3, out=t0 + i + 0.85, out_dur=0.12))
        s.fx(t0 + i, "tick", 0.9)


def bubbles(s, t_in, b1_order, b2_order, size=38):
    """Snow White speech bubbles (std layout). Returns (ParaStates b1, ParaStates b2)."""
    b1 = "‘Snow White and the Seven Dwarfs’ {is|is} one of my favourite stories. I first {read|read} it when I {was|was} only three."
    b2 = ("The story {reaches|reaches} its climax when the evil queen {gives|gives} Snow White a poisoned apple. Luckily "
          "the prince’s kiss {saves|saves} her and they {live|live} happily ever after.")
    cols = {k: YELLOW for k in ("is", "read", "was", "reaches", "gives", "saves", "live")}
    y1 = 205
    p1 = ParaStates(b1, size, 980, 130, y1 + 35, cols, b1_order, t_in, "none", line_gap=1.9)
    h1 = p1.base.height + 40
    ly2 = y1 + h1 + 34 + 30                      # below the first bubble's tail tip
    y2 = ly2 + 44
    p2 = ParaStates(b2, size, 980, 130, y2 + 35, cols, b2_order, t_in + 0.25, "none", line_gap=1.9)
    h2 = p2.base.height + 40
    s.add(E(context_label("Someone talks about a favourite story"), 96, 158, "lt", t_in, "fade", 0.35))
    s.add(E(gl.bubble_img(1060, h1, "left"), 70, y1, "lt", t_in, "pop", 0.4))
    s.add(E(context_label("The same person then sums up what happens in the story"), 96, ly2, "lt", t_in + 0.25,
            "fade", 0.35))
    s.add(E(gl.bubble_img(1060, h2, "left"), 70, y2, "lt", t_in + 0.25, "pop", 0.4))
    s.add(p1, p2)
    return p1, p2
def context_label(text, size=27):
    """Small cyan speech icon + sentence-case caption saying what a speech bubble is."""
    t = text_img(text, size, "nun", "ExtraBold", fill=CYAN)
    ic = Image.new("RGBA", (34, 30), (0, 0, 0, 0)); d = ImageDraw.Draw(ic)
    d.rounded_rectangle((1, 1, 32, 21), radius=8, outline=CYAN + (255,), width=3)
    d.polygon([(7, 19), (6, 29), (16, 20)], fill=CYAN + (255,))
    im = Image.new("RGBA", (ic.width + 12 + t.width, max(ic.height, t.height)), (0, 0, 0, 0))
    im.alpha_composite(ic, (0, (im.height - ic.height) // 2))
    im.alpha_composite(t, (ic.width + 12, (im.height - t.height) // 2))
    return im


def tag_on(s, ps, key, text, col, t):
    cx, _ = ps.centre(key)
    b = ps.box(key)
    s.add(E(pill_img(text, 19, col, INK, h=30, padx=12), cx, b[1] + 6, "mb", t, "pop", 0.3))


# ============================================================================ wrap scenes
def s_L0():
    s = Scene("L0", dur=4.0, layout="off", header=False, music="theme")
    s.panel = False
    lg = gl.logo(300)
    rimg = Image.new("RGBA", (720, 720), (0, 0, 0, 0))
    d = ImageDraw.Draw(rimg)
    d.arc((40, 40, 680, 680), 200, 330, fill=CYAN, width=10)
    d.arc((40, 40, 680, 680), 20, 150, fill=PINK, width=10)
    d.arc((90, 90, 630, 630), 300, 60, fill=YELLOW, width=6)
    rimg = glow(rimg, 16, None, 1.3)

    def ringf(fr, t, p):
        im = rimg.rotate(-t * 60, resample=Image.BILINEAR)
        place(fr, im, 960, 420, "mm", e_out(p), 0.8 + 0.2 * e_back(p))
    s.add(Fn(ringf, 0.05, 0.6))
    s.add(E(lg, 960, 420, "mm", 0.15, "zoom", 0.5))
    s.add(sparkle_burst(960, 420, 0.5, 16, 420, seed=4, dur=1.0))
    s.add(E(text_img(gl.SERIES, 84, glow_r=14, glow_col=CYAN), 960, 790, "mm", 1.2, "up", 0.45))
    s.add(E(text_img(gl.UNIT, 50, "nun", "ExtraBold", fill=CYAN), 960, 880, "mm", 1.6, "up", 0.45))
    s.fx(0.12, "sting", 0.9); s.fx(1.2, "whoosh", 0.6); s.fx(1.6, "sparkle", 0.5)
    return s


def s_L1():
    s = Scene("L1", layout="std", clip=f"{CLIPS}/intro_v2.mp4", clip_audio=f"{REFS}/intro.wav", music="theme")
    s.panel_in = True
    s.add(E(text_img(gl.SERIES, 40, "fred", "SemiBold", fill=CYAN), 615, 205, "mm", 0.3, "fade", 0.4))
    s.add(E(text_img("The present", 92, glow_r=16, glow_col=PINK), 615, 305, "mm", 0.6, "zoom", 0.45))
    s.add(E(text_img("and the past", 92, glow_r=16, glow_col=PINK), 615, 415, "mm", 0.9, "zoom", 0.45))
    s.add(E(text_img("Today's levels", 34, "nun", "Bold", fill=DIM), 615, 520, "mm", 8.2, "fade", 0.3))
    cols = [YELLOW, YELLOW, CYAN, MINT]
    for i in range(4):
        t = 8.6 + i * 0.42
        s.add(E(pill_img(LABEL[i + 1], 34, cols[i], INK), 615, 595 + i * 82, "mm", t, "pop", 0.35))
        s.fx(t, "pop", 0.6)
    s.add(E(pill_img("+ QUIZ AT THE END", 34, PINK, WHITE), 615, 935, "mm", 12.3, "pop", 0.35))
    s.fx(12.3, "pop", 0.7)
    s.add(sparkle_burst(615, 700, 14.3, 16, 380, seed=9, dur=0.9)); s.fx(14.3, "sparkle", 0.6)
    s.add(E(name_tag(), 1660, 318, "mb", 2.8, "pop", 0.45, out=s.dur - 0.45, out_dur=0.3)); s.fx(2.8, "pop", 0.6)
    return s


def s_L3():
    s = Scene("L3", layout="std", clip=f"{CLIPS}/outro_v1.mp4", clip_audio=f"{REFS}/outro.wav", level=4,
              label="WELL DONE!", music="theme")
    s.panel_out = True
    s.exit = 0.35
    s.add(E(text_img("WELL DONE!", 104, glow_r=16, glow_col=ORANGE, fill=YELLOW), 615, 225, "mm", 0.2, "zoom", 0.45))
    s.add(E(text_img("Today's key points", 38, "nun", "Bold"), 615, 318, "mm", 0.6, "fade", 0.3))
    CH = [("Simple present", "I play", YELLOW, INK), ("Present continuous", "I am playing", PINK, WHITE),
          ("Simple past", "I played", YELLOW, INK), ("Past continuous", "I was playing", PINK, WHITE),
          ("Non-action verbs", "like · want · know · have …", CYAN, INK),
          ("Tenses in stories", "story: past · synopsis: present", CYAN, INK)]
    cw, chh, gx, gy, x0, y0 = 480, 170, 30, 26, 120, 385
    for i, (t, sub, bg, fg) in enumerate(CH):
        r, c = divmod(i, 2)
        im = Image.new("RGBA", (cw, chh), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle((0, 0, cw - 1, chh - 1), radius=34, fill=bg)
        gl.centred_text(d, (0, 22, cw, 92), t, F("fred", 44, "Bold"), fg)
        gl.centred_text(d, (0, 98, cw, 148), sub, F("nun", 30, "ExtraBold"), fg)
        tt = 0.9 + i * 0.3
        s.add(E(im, x0 + c * (cw + gx) + cw / 2, y0 + r * (chh + gy) + chh / 2, "mm", tt, "pop", 0.35))
        s.fx(tt, "pop", 0.5)
    return s


def s_L4():
    s = Scene("L4", dur=6.1, layout="off", header=False, music="theme")
    s.panel = False; s.exit = 0.01
    s.add(E(gl.logo(260), 960, 400, "mm", 0.1, "zoom", 0.5))
    s.add(sparkle_burst(960, 400, 0.4, 14, 380, seed=12, dur=1.0))
    s.add(E(text_img(gl.SERIES, 76, glow_r=14, glow_col=CYAN), 960, 660, "mm", 0.6, "up", 0.4))
    s.add(E(text_img(gl.UNIT, 46, "nun", "ExtraBold", fill=CYAN), 960, 745, "mm", 0.9, "up", 0.4))
    s.add(E(text_img("See you next time!", 40, "nun", "Bold", fill=DIM), 960, 840, "mm", 1.3, "fade", 0.4))

    def fade(fr, t, p):
        a = clamp((t - 4.5) / 0.9)                     # fully black from 5.4 s; held to the end (6.1 s)
        if a > 0:
            fr.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, int(255 * a))))
    s.add(Fn(fade, 4.5, 1.6))
    s.fx(0.1, "sparkle", 0.6)
    return s


# ============================================================================ body scenes
def s_H():
    s = Scene("H", "SH", hold=0.9, layout="std")
    order1 = [("is", s.w("is")), ("read", s.w("read")), ("was", s.w("was"))]
    order2 = [("reaches", s.w("reaches")), ("gives", s.w("gives"))]
    p1, p2 = bubbles(s, 0.05, order1, order2)
    for (k, t), tx in zip(order1 + order2, ["PRESENT", "PAST", "PAST", "PRESENT", "PRESENT"]):
        tag_on(s, p1 if k in ("is", "read", "was") else p2, k, tx, MINT if tx == "PRESENT" else ORANGE, t)
        s.fx(t, "pop", 0.6)
    tq = s.w("is", 2)
    s.add(E(text_img("?", 190, glow_r=18, glow_col=ORANGE, fill=YELLOW), 1050, 895, "mm", tq, "pop", 0.4, pulse=0.03))
    s.fx(tq, "whoosh", 0.5)
    s.kay(tq, s.w("lets") - 0.05, "eyes", "surprised")
    return s


def s_M():
    s = Scene("M", "SM", hold=0.8, layout="small", label="FOUR TENSES")
    s.add(E(text_img("THE TENSE MAP", 54, glow_r=12, glow_col=CYAN), 105, 160, "lt", 0.1, "left", 0.4))
    s.add(E(text_img("PRESENT", 44, fill=MINT), 105, 470, "lm", 0.4, "left"), E(text_img("PAST", 44, fill=ORANGE), 105, 740, "lm", 0.55, "left"))
    tY, tP = s.w("yellow"), s.w("pink")
    hdr_s = Image.new("RGBA", (500, 70), (0, 0, 0, 0)); d = ImageDraw.Draw(hdr_s)
    d.text((0, 8), "SIMPLE", font=F("fred", 46, "Bold"), fill=YELLOW)
    for i in range(3):
        d.ellipse((210 + i * 34, 26, 234 + i * 34, 50), fill=YELLOW)
    hdr_c = Image.new("RGBA", (520, 70), (0, 0, 0, 0)); d = ImageDraw.Draw(hdr_c)
    d.text((0, 8), "CONTINUOUS", font=F("fred", 46, "Bold"), fill=PINK)
    d.rounded_rectangle((330, 28, 470, 48), radius=10, fill=PINK)
    s.add(E(hdr_s, 345, 300, "lt", tY, "drop"), E(hdr_c, 875, 300, "lt", tP, "drop"))
    tiles = [("simple present", "I play", YELLOW, 345, 370, tY + 0.15), ("simple past", "I played", YELLOW, 345, 640, tY + 0.35),
             ("present continuous", "I am playing", PINK, 875, 370, tP + 0.15), ("past continuous", "I was playing", PINK, 875, 640, tP + 0.35)]
    tu = s.w("unlock")
    for name, ex, col, x, y, t in tiles:
        im = card(500, 240, col, 30)
        d = ImageDraw.Draw(im)
        gl.centred_text(d, (0, 30, 500, 100), name, F("fred", 40, "Bold"), col)
        gl.centred_text(d, (0, 115, 500, 200), ex, F("nun", 54, "ExtraBold"), WHITE)
        s.add(E(im, x, y, "lt", t, "pop", 0.4))
        s.add(E(padlock(44), x + 450, y + 40, "mm", t, "pop", 0.3, out=tu, out_dur=0.3))
        s.fx(t, "pop", 0.55)
    xx = 345
    for w, ph in (("facts", "facts"), ("habits", "habits"), ("finished actions", "finished")):
        im = chip(w, YELLOW, (70, 60, 20))
        s.add(E(im, xx, 905, "lt", s.w(ph), "pop", 0.3)); xx += im.width + 14
    s.add(E(chip("actions in progress", PINK, (80, 25, 70)), 875, 905, "lt", s.w("actions", 2), "pop", 0.3))
    s.add(sparkle_burst(870, 610, tu, 18, 520, seed=5, dur=0.9)); s.fx(tu, "sparkle", 0.8)
    s.kay(tu, tu + 0.4, "bounce")
    return s


def s_level(n, voice):
    s = Scene(f"{n}.0", voice, hold=0.5, layout="large", level=n, label=LABEL[n])
    s.add(E(text_img(f"LEVEL {n}", 170, glow_r=20, glow_col=ORANGE, fill=YELLOW), 104, 300, "lt", 0.05, "zoom", 0.4))
    s.add(E(fit(LVL[n], 800, 92, glow_r=14, glow_col=PINK), 104, 530, "lt", 0.3, "up", 0.4))
    xp0, xp1 = (n - 1) / 4, n / 4
    s.add(Fn(lambda fr, t, p: place(fr, xp_img(xp0 + (xp1 - xp0) * e_out(p), 540), 104, 700), 0.5, 0.8))
    s.add(E(text_img(f"{n} of 4 levels", 32, "nun", "ExtraBold", fill=DIM), 186, 785, "lt", 0.5, "fade"))
    dot_x = W - 44 - 104 + 13 + (n - 1) * 26
    s.add(ring(dot_x, 57, 0.4, YELLOW, 8, 40, 0.6))
    s.add(sparkle_burst(450, 420, 0.1, 14, 380, seed=n))
    s.fx(0.05, "levelup", 0.85)
    s.kay(0.05, 0.45, "bounce")
    s.kay(s.vend - 0.15, s.dur, "eyes", "wink")
    return s


def s_11():
    s = Scene("1.1", "S1_1", hold=0.8, layout="std", level=1, label=LABEL[1])
    s.add(E(pill_img("SIMPLE PRESENT", 34, YELLOW, INK), 110, 165, "lt", 0.05, "left"))
    tb, ta = s.w("basic"), s.w("add")
    b1 = block("I / you / we / they", 46); b2 = block("play", 46, YELLOW)
    s.add(E(b1, 110, 300, "lt", tb, "left"), E(text_img("+", 60), 110 + b1.width + 40, 340, "mm", tb + 0.15, "pop"),
          E(b2, 110 + b1.width + 80, 300, "lt", tb + 0.25, "pop"))
    th = s.w("he")
    b3 = block("he / she / it", 46)
    x3 = 110 + b3.width + 80
    s.add(E(b3, 110, 460, "lt", th, "left"), E(text_img("+", 60), 110 + b3.width + 40, 500, "mm", th + 0.15, "pop"),
          E(b2, x3, 460, "lt", th + 0.25, "pop"))
    st = glow(pill_img("+s", 48, YELLOW, INK, h=78, padx=22), 10, YELLOW)
    s.add(Fly(st, (900, 220), (x3 + b2.width + 60, 499), ta, 0.55))
    s.fx(ta + 0.5, "click", 0.8)
    tp = s.w("plays")
    ps = ParaStates("She {play|v}{s|s}.", 110, 900, 110, 640, {"v": WHITE, "s": YELLOW}, [("s", tp)], tp - 0.05, "up",
                    kind="fred", weight="Bold")
    s.add(ps)
    s.add(sparkle_burst(ps.centre("s")[0], ps.centre("s")[1], tp + 0.1, 10, 120, seed=2)); s.fx(tp, "sparkle", 0.6)
    return s


def s_12():
    s = Scene("1.2", "S1_2", hold=3.9, layout="std", level=1, label=LABEL[1])
    s.add(E(pill_img("SIMPLE PRESENT", 28, YELLOW, INK), 110, 160, "lt", 0.05, "left"))
    rows = [("FACTS & GENERAL TRUTHS", "Water {freezes} at 0°C.", "thermometer", "facts", "water"),
            ("TRUE NOW", "I {live} in Tsing Yi.", "pin", "things", "live"),
            ("HABITS", "Richard {wakes up} at 7 a.m. {every day|t}.", "alarm", "habits", "richard")]
    ics = [icon(r[2], 110) for r in rows]
    def ink(im):                                   # ink width and ink-centre offset from the image centre
        xs = np.nonzero((np.asarray(im)[..., 3] > 60).any(0))[0]
        return xs.max() - xs.min() + 1, (xs.max() + xs.min() + 1) / 2 - im.width / 2
    icx = 110 + 1010 - 48 - max(ink(im)[0] for im in ics) / 2     # common icon centre line, 48 px clear of the edge
    for i, (lab, ex, ic, c1, c2) in enumerate(rows):
        y = 228 + i * 196                              # cards 178 high: leaves a clear gap above the habit words
        t1, t2 = s.w(c1), s.w(c2)
        s.add(E(card(1010, 178, YELLOW, 18), 110, y, "lt", t1, "left", 0.4))
        s.add(E(circle_num(i + 1, 66, YELLOW, INK), 135, y + 22, "lt", t1 + 0.1, "pop"))
        s.add(E(text_img(lab, 38, fill=gl.LILAC), 225, y + 30, "lt", t1 + 0.1, "left"))
        cols = {"0": YELLOW, "t": CYAN}
        order = [("0", t2)] + ([("t", s.w("every"))] if "{every" in ex else [])
        s.add(ParaStates(ex, 40, 790, 225, y + 98, cols, order, t2 - 0.1, "up"))
        s.add(E(ics[i], icx - ink(ics[i])[1], y + 92, "mm", t1 + 0.15, "pop", 0.4))
        s.fx(t1, "whoosh", 0.4)
    te = s.w("every")
    x = 225
    s.add(E(text_img("Habit words that go with the simple present:", 28, "nun", "ExtraBold", fill=DIM), 225, 864, "lt",
            te + 0.05, "fade"))
    for i, w in enumerate(("every day", "often", "usually", "always")):
        im = chip(w, CYAN, NAVY, 34)
        s.add(E(im, x, 906, "lt", te + 0.15 + i * 0.18, "up", 0.3)); x += im.width + 18
        s.fx(te + 0.15 + i * 0.18, "pop", 0.4)
    return s


def s_13():
    s = Scene("1.3", "S1_3", hold=1.0, layout="std", level=1, label=LABEL[1])
    s.add(E(pill_img("PRESENT CONTINUOUS", 30, PINK, WHITE), 110, 158, "lt", 0.05, "left"))
    b1, b2 = block("am / is / are", 40, PINK), block("verb", 40)
    s.add(E(b1, 110, 230, "lt", 0.4, "left"), E(text_img("+", 52), 110 + b1.width + 34, 264, "mm", 0.55, "pop"),
          E(b2, 110 + b1.width + 68, 230, "lt", 0.65, "pop"))
    tp = s.w("plus")
    ing = glow(pill_img("-ing", 40, PINK, WHITE, h=68, padx=20), 10, PINK)
    s.add(Fly(ing, (900, 180), (110 + b1.width + 68 + b2.width + 18 + ing.width / 2, 264), tp, 0.5))
    s.fx(tp + 0.45, "click", 0.8)
    tg = s.w("give")
    hands = [hand_img(k, 380) for k in range(6)]
    small = [hand_img(k, 150) for k in range(6)]
    cues = [s.w("one"), s.w("two"), s.w("three"), s.w("four"), s.w("five", 3)]
    s.add(E(text_img("GIVE ME FIVE!", 84, glow_r=14, glow_col=ORANGE, fill=YELLOW), 615, 840, "mm", tg + 0.1, "zoom", 0.35,
            out=cues[0] - 0.2, out_dur=0.2))

    def handf(fr, t, p):
        k = sum(1 for c in cues if t >= c)
        if t < cues[0] - 0.2:
            place(fr, hands[0], 615, 580, "mm", e_out(p * 2), 0.6 + 0.4 * e_back(p))
        else:
            q = e_inout((t - (cues[0] - 0.2)) / 0.4)
            if q < 1:
                place(fr, hands[0], 615 + (1060 - 615) * q, 580 + (235 - 580) * q, "mm", 1.0, 1 - 0.6 * q)
            else:
                place(fr, small[k], 1060, 235, "mm")
    s.add(Fn(handf, tg, 0.4))
    s.fx(tg, "pop", 0.8)
    rows = [("RIGHT NOW", "Look! Snow {is falling}.", "snowflake", "look"),
            ("TEMPORARY SITUATIONS", "I {am learning} to swim at present.", "goggles", "i"),
            ("CHANGING TRENDS", "House husbands {are becoming} more popular.", "chart", "house"),
            ("PHOTOS & PICTURES", "Everyone {is smiling} happily in the photo.", "camera", "everyone"),
            ("ANNOYING HABITS + always", "He {is|a} {always|b} {complaining|c} about his job.", "grumpy", "he")]
    for i, (lab, ex, ic, ce) in enumerate(rows):
        y = 335 + i * 136
        t1, t2 = cues[i], s.w(ce)
        s.add(E(circle_num(i + 1, 60, PINK, WHITE), 112, y + 4, "lt", t1, "pop"))
        s.add(E(text_img(lab, 32, fill=gl.LILAC), 190, y + 6, "lt", t1 + 0.05, "left"))
        if i == 4:
            cols, order = {"a": PINK, "b": CYAN, "c": PINK}, [("a", t2), ("b", t2), ("c", t2)]
        else:
            cols, order = {"0": PINK}, [("0", t2 + 0.25)]
        s.add(ParaStates(ex, 34, 790, 190, y + 50, cols, order, t2 - 0.1, "up"))
        s.add(E(icon(ic, 92), 1080, y + 52, "mm", t1 + 0.1, "pop"))
        s.add(ring(130, y + 34, t1, YELLOW, 20, 60, 0.45))
        s.fx(t1, "pop", 0.6)
    ta = s.w("always", 2)
    s.kay(ta, ta + 0.35, "eyes", "blink")
    return s


def s_21():
    s = Scene("2.1", "S2_1", hold=2.2, layout="std", level=2, label=LABEL[2])
    s.add(E(pill_img("SIMPLE PAST", 30, YELLOW, INK), 110, 158, "lt", 0.05, "left"))
    tf = s.w("finished")
    s.add(E(card(1010, 200, YELLOW, 16), 110, 228, "lt", tf - 0.2, "left"))
    s.add(E(text_img("FINISHED ACTIONS", 36, fill=gl.LILAC), 140, 248, "lt", tf - 0.1, "left"))
    tl = Image.new("RGBA", (930, 60), (0, 0, 0, 0)); d = ImageDraw.Draw(tl)
    d.rounded_rectangle((0, 26, 900, 34), radius=4, fill=WHITE)
    d.polygon([(895, 12), (928, 30), (895, 48)], fill=WHITE)
    s.add(E(tl, 140, 320, "lt", tf, "wipe", 0.5))
    s.add(E(text_img("PAST", 24, "fred", "SemiBold", fill=DIM), 140, 390, "lt", tf + 0.2, "fade"))
    now = text_img("NOW", 28, fill=CYAN)
    ib = now.getbbox()                                       # ink box, so the gap is measured from the letters
    s.add(E(now, 860, 306 - ib[3] + now.height, "mb", tf + 0.4, "pop"))     # ink bottom at y 306
    s.add(E(Image.new("RGBA", (6, 62), CYAN + (255,)), 860, 320, "mt", tf + 0.4, "fade"))   # 14 px below the ink
    for i, x in enumerate((260, 460, 660)):
        tt = tf + 0.5 + i * 0.25
        dot = Image.new("RGBA", (40, 40), (0, 0, 0, 0)); ImageDraw.Draw(dot).ellipse((0, 0, 39, 39), fill=YELLOW)
        s.add(E(dot, x, 350, "mm", tt, "pop"), E(tick_img(36), x + 28, 318, "mm", tt + 0.15, "pop"))
    tm, ti = s.w("most"), s.w("irregular")
    bw = block("walk", 46, WHITE)
    st = glow(pill_img("+ed", 42, YELLOW, INK, h=72, padx=18), 8, YELLOW)
    s.add(E(bw, 110, 465, "lt", tm, "left"), E(st, 110 + bw.width + 20, 503, "lm", tm + 0.3, "drop"))
    ax = 110 + bw.width + 40 + st.width
    s.add(E(arrow_img(70, WHITE), ax, 503, "lm", tm + 0.5, "fade"),
          E(text_img("walked", 54, "nun", "ExtraBold", fill=YELLOW), ax + 95, 503, "lm", tm + 0.6, "pop"))
    lab = text_img("IRREGULAR:", 34, fill=ORANGE)
    s.add(E(lab, 110, 600, "lm", ti - 0.1, "fade"))
    xx = 110 + lab.width + 24
    for j, (a, b) in enumerate((("break", "broke"), ("is", "was"))):
        im, _ = para(f"{a} → {{{b}|x}}", 40, 400, colors={"x": YELLOW}, underline=False)
        c = card(im.width + 40, 74, ORANGE, 24, 20, 3); c.alpha_composite(im, (20, 8))
        s.add(E(c, xx, 600, "lm", ti + 0.15 + j * 0.25, "pop")); xx += c.width + 24
    t1, t2 = s.w("i"), s.w("fire")
    s.add(ParaStates("I {was} born {in 2013|t}.", 46, 1000, 110, 680, {"0": YELLOW, "t": CYAN}, [("0", t1 + 0.2), ("t", t1 + 0.7)], t1 - 0.1))
    s.add(ParaStates("A fire {broke out} in my building {yesterday|t}.", 46, 1000, 110, 775, {"0": YELLOW, "t": CYAN},
                     [("0", t2 + 0.3), ("t", s.w("yesterday"))], t2 - 0.1))
    ty = s.w("yesterday")
    x = 110
    s.add(E(text_img("Time words that go with the simple past:", 28, "nun", "ExtraBold", fill=DIM), 110, 870, "lt",
            ty + 0.15, "fade"))
    for i, w in enumerate(("yesterday", "last week", "two years ago", "in 2013")):
        im = chip(w, CYAN, NAVY, 30)
        s.add(E(im, x, 912, "lt", ty + 0.25 + i * 0.15, "up", 0.3)); x += im.width + 16
    return s


def s_22():
    s = Scene("2.2", "S2_2p", hold=3.9, layout="small", level=2, label=LABEL[2])
    s.add(E(pill_img("PAST CONTINUOUS", 30, PINK, WHITE), 100, 152, "lt", 0.05, "left"))
    b1, b2 = block("was / were", 34, PINK, h=58), block("verb", 34, h=58)
    x = 480
    s.add(E(b1, x, 150, "lt", 0.35, "left"), E(text_img("+", 44), x + b1.width + 28, 179, "mm", 0.45, "pop"),
          E(b2, x + b1.width + 56, 150, "lt", 0.55, "pop"))
    tp = s.w("plus")
    ing = glow(pill_img("-ing", 34, PINK, WHITE, h=58, padx=16), 8, PINK)
    s.add(Fly(ing, (1250, 120), (x + b1.width + 56 + b2.width + 14 + ing.width / 2, 179), tp, 0.45))
    s.fx(tp + 0.4, "click", 0.8)

    def tline(y, t):
        im = Image.new("RGBA", (520, 30), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle((0, 12, 495, 18), radius=3, fill=(255, 255, 255, 170))
        d.polygon([(492, 4), (518, 15), (492, 26)], fill=(255, 255, 255, 170))
        s.add(E(im, 100, y, "lt", t, "wipe", 0.4))

    def bar(x0, x1, y, t, col=PINK, h=24):
        im = Image.new("RGBA", (x1 - x0, h), (0, 0, 0, 0))
        ImageDraw.Draw(im).rounded_rectangle((0, 0, x1 - x0 - 1, h - 1), radius=h // 2, fill=col)
        s.add(E(glow(im, 8, col, 0.8), x0 - 16, y - 16, "lt", t, "wipe", 0.6))
    rows = [("IN PROGRESS AT A PAST TIME", "use", "we",
             "We {were having} a barbecue\n{at four o’clock yesterday|t}.", {"0": PINK, "t": CYAN}),
            ("LONG ACTION + SHORT ACTION", "long", "she",
             "She {was waiting} for the bus\n{when|w} it suddenly {rained|y}.", {"0": PINK, "w": CYAN, "y": YELLOW}),
            ("TWO ACTIONS AT THE SAME TIME", "two", "fred",
             "Fred {was watching|a} TV\n{while|w} his mum {was preparing|b} dinner.", {"a": PINK, "w": CYAN, "b": PINK})]
    tops, hs = [222, 460, 735], [218, 255, 255]           # one card per case, 20 px apart
    ys = [t + 16 for t in tops]
    for i, (lab, c1, c2, ex, cols) in enumerate(rows):
        y = ys[i]
        t1, t2 = s.w(c1), s.w(c2)
        s.add(E(card(1300, hs[i], PINK, 14, 26, 3), 80, tops[i], "lt", t1 - 0.05, "fade", 0.3))
        s.add(E(circle_num(i + 1, 54, PINK, WHITE), 100, y, "lt", t1, "pop"))
        s.add(E(text_img(lab, 30, fill=gl.LILAC), 170, y + 8, "lt", t1 + 0.05, "left"))
        tline(y + 120, t1 + 0.1)
        if i == 0:
            bar(150, 540, y + 123, t1 + 0.3)
            tc = s.w("four")
            s.add(E(icon("clock", 84), 345, y + 72, "mm", tc, "drop", 0.45), E(text_img("4:00", 26, fill=CYAN), 345, y + 158, "mt", tc + 0.2, "fade"))
            s.fx(tc + 0.3, "click", 0.7)
            order = [("0", t2 + 0.2), ("t", tc)]
        elif i == 1:
            bar(150, 540, y + 123, t1 + 0.3)
            ts = s.w("short")
            s.add(E(icon("lightning", 90), 430, y + 88, "mm", ts, "drop", 0.3), ring(430, y + 135, ts + 0.25, YELLOW, 10, 60))
            s.fx(ts + 0.2, "glitch", 0.6)
            s.add(E(text_img("LONG = past continuous", 24, "nun", "ExtraBold", fill=PINK), 149, y + 168, "lt", t1 + 0.5, "fade"))
            s.add(E(text_img("SHORT = simple past", 24, "nun", "ExtraBold", fill=YELLOW), 149, y + 196, "lt", ts + 0.3, "fade"))
            order = [("0", t2 + 0.2), ("w", s.w("when")), ("y", s.w("when") + 0.6)]
            s.add(E(tip_img("when", "before the short action."), 640, y + 178, "lt", s.w("when") + 1.0, "up", 0.35))
        else:
            bar(150, 540, y + 102, t1 + 0.3); bar(150, 540, y + 144, t1 + 0.45)    # pair centred on the line
            order = [("a", t2 + 0.25), ("w", s.w("while")), ("b", s.w("while") + 0.5)]
        s.add(ParaStates(ex, 36, 720, 640, y + 62, cols, order, t2 - 0.1, "up"))
        s.fx(t1, "whoosh", 0.4)
    td = s.w("dinner")
    s.add(E(tip_img("while", "before a long action."), 640, ys[2] + 178, "lt", td + 0.2, "up", 0.35))
    return s


def s_T():
    s = Scene("T", layout="std", clip=f"{CLIPS}/transition_v2.mp4", clip_audio=f"{REFS}/transition.wav", level=2)
    s.add(E(text_img("NICE ONE!", 130, glow_r=18, glow_col=ORANGE, fill=YELLOW), 615, 430, "mm", 0.45, "zoom", 0.4))
    s.add(E(text_img("2 of 4 levels complete", 44, "nun", "ExtraBold"), 615, 590, "mm", 0.9, "up"))
    s.add(E(xp_img(0.5, 600), 615, 700, "mm", 1.1, "fade"))
    s.add(sparkle_burst(615, 430, 0.5, 16, 420, seed=21)); s.fx(0.45, "sparkle", 0.6)
    return s


def s_31():
    s = Scene("3.1", "S3_1", hold=0.8, layout="std", level=3, label=LABEL[3])
    s.add(E(text_img("NON-ACTION VERBS", 66, glow_r=12, glow_col=CYAN), 615, 200, "mm", 0.05, "zoom", 0.4))
    s.add(E(text_img("feelings · opinions · states", 34, "nun", "Bold", fill=DIM), 615, 268, "mm", s.w("feelings"), "fade"))
    sign = neon_sign("NO -ING ZONE", 50)
    td = s.w("dont")
    s.add(flicker((sign, 615, 365, "mm"), td))
    s.fx(td, "glitch", 0.5)
    groups = [("FEELINGS", PINK, "heart", ["like", "want"]), ("THINKING", YELLOW, "bulb", ["think", "know"]),
              ("SENSES", CYAN, "eye", ["see", "smell"]), ("OWNING", MINT, "gift", ["have"])]
    for i, (lab, col, ic, verbs) in enumerate(groups):
        r, c = divmod(i, 2)
        x, y = 110 + c * 515, 460 + r * 280
        t0 = s.w(verbs[0])
        s.add(E(card(495, 255, col, 26, 40), x, y, "lt", t0, "pop", 0.4))
        s.add(E(icon(ic, 96), x + 75, y + 80, "mm", t0 + 0.1, "pop"))
        s.add(E(text_img(lab, 40, fill=col), x + 140, y + 55, "lt", t0 + 0.1, "left"))
        xx = x + 40
        for j, v in enumerate(verbs):
            tv = s.w(v) if j else t0
            im = pill_img(v, 42, WHITE, INK, kind="nun", weight="ExtraBold")
            s.add(E(im, xx, y + 150, "lt", tv, "drop", 0.4)); xx += im.width + 20
            s.fx(tv, "pop", 0.6)
    return s


def s_32():
    s = Scene("3.2", "S3_2", hold=0.8, layout="std", level=3, label=LABEL[3])
    s.add(E(pill_img("NON-ACTION VERBS", 28, CYAN, INK), 110, 160, "lt", 0.05, "left"))
    sign = neon_sign("NO -ING ZONE", 28)
    il, it, ir, ib = ink_bounds(sign)
    sx = 1170 - 56 - (ir - il) / 2; sy = 182
    s.add(E(sign, sx, sy, "mm", 0.2, "fade"))
    tn1, tm, tn2 = s.w("not"), s.w("mike"), s.w("not", 2)
    pairs = [("I {think} game shows are exciting.", "I {am thinking|x} game shows are exciting.", 0.25, tn1, s.w("thinking", end=True)),
             ("Mike {has} one brother and one sister.", "Mike {is having|x} one brother and one sister.", tm, tn2, s.w("having", end=True))]
    for i, (ok, bad, t_ok, t_bad, t_x) in enumerate(pairs):
        y = 270 + i * 360
        p_ok = ParaStates(ok, 42, 900, 110, y, {"0": YELLOW}, [("0", t_ok + 0.3)], t_ok, "up")
        s.add(p_ok)
        s.add(E(tick_img(70), 110 + p_ok.base.width + 50, y + 30, "mm", t_ok + 0.5, "pop")); s.fx(t_ok + 0.5, "correct", 0.6)
        p_bad = ParaStates(bad, 42, 900, 110, y + 120, {"x": PINK}, [("x", t_bad + 0.1)], t_bad, "up", fill=DIM)
        s.add(p_bad)
        bx = p_bad.box("x")
        ing = pill_img("-ing", 28, PINK, WHITE, h=46, padx=12)
        s.add(Fly(ing, (bx[2] - 20, bx[1] - 10), (sx, sy), t_x - 0.1, 0.5, scale1=0.3, out=t_x + 0.38))
        s.add(ring(sx, sy, t_x + 0.36, PINK, 20, 120, 0.4))
        s.add(strike(105, y + 120 + 30, 110 + p_bad.base.width + 6, t_x + 0.05, RED, 8))
        s.add(E(cross_img(70), 110 + p_bad.base.width + 50, y + 150, "mm", t_x + 0.3, "pop"))
        s.fx(t_x + 0.05, "buzz", 0.6)
        s.kay(t_bad, t_bad + 0.6, "shake")
    return s


def s_33():
    s = Scene("3.3", "S3_3", hold=0.9, layout="large", level=3, label=LABEL[3])
    big = text_img("PLOT TWIST!", 112, glow_r=18, glow_col=PINK, fill=YELLOW, stroke=4, stroke_col=PINK)
    s.add(E(big, 460, 520, "mm", 0.05, "zoom", 0.35, out=1.25, out_dur=0.2))
    s.fx(0.05, "glitch", 0.8); s.fx(0.1, "whoosh", 0.5)
    s.kay(0.0, 1.3, "eyes", "surprised")
    s.lay(1.2, "std")
    s.add(E(text_img("PLOT TWIST!", 46, glow_r=8, glow_col=PINK, fill=YELLOW), 110, 152, "lt", 1.4, "pop"))
    s.add(E(text_img("Some can take -ing when they are actions.", 30, "nun", "Bold", fill=DIM), 110, 222, "lt", s.w("some"), "fade"))
    rows = [("THINK", "= opinion", "bulb", YELLOW, "THINKING", "= using your brain", "gears", "what", "action",
             "What {is} she {thinking} now?"),
            ("HAVE", "= own", "family", YELLOW, "HAVING", "= eating", "sushi", "we", "means",
             "We {were having} dinner at a Japanese restaurant.")]
    for i, (w1, m1, i1, c1, w2, m2, i2, cl, cr, ex) in enumerate(rows):
        y = 290 + i * 355
        tl, tr = s.w(cl), s.w(cr)
        for j, (wd, mn, ic, col, tt) in enumerate(((w1, m1, i1, c1, tl), (w2, m2, i2, PINK, tr))):
            im = card(450, 160, col, 26)
            im.alpha_composite(icon(ic, 100), (24, 30))
            d = ImageDraw.Draw(im)
            d.text((145, 22), wd, font=F("fred", 46, "Bold"), fill=col)
            d.text((145, 88), mn, font=F("nun", 30, "ExtraBold"), fill=WHITE)
            s.add(E(im, 110 + j * 560, y, "lt", tt, "pop", 0.4)); s.fx(tt, "pop", 0.6)
        s.add(E(arrow_img(70, WHITE), 580, y + 80, "lm", tr - 0.1, "fade"))
        cols = {"0": PINK, "1": PINK} if i == 0 else {"0": PINK}
        order = [("0", tl + 0.4), ("1", tl + 0.8)] if i == 0 else [("0", tl + 0.5)]
        s.add(ParaStates(ex, 42, 1000, 110, y + 185, cols, order, tl + 0.1, "up"))
    return s


def s_41():
    s = Scene("4.1", "S4_1", hold=0.8, layout="small", level=4, label=LABEL[4])
    ts = s.w("stories")
    im, _ = para("Stories in the past → {past tenses|p}", 44, 1200, colors={"p": YELLOW})
    s.add(E(im, 100, 160, "lt", ts, "wipe", 0.6))
    bk = Image.new("RGBA", (1240, 680), (0, 0, 0, 0)); d = ImageDraw.Draw(bk)
    d.rounded_rectangle((0, 20, 615, 660), radius=30, fill=(40, 26, 88, 235), outline=YELLOW + (230,), width=5)
    d.rounded_rectangle((625, 20, 1238, 660), radius=30, fill=(40, 26, 88, 235), outline=YELLOW + (230,), width=5)
    d.line((620, 30, 620, 660), fill=YELLOW + (200,), width=4)
    bk = glow(bk, 12, YELLOW, 0.5)
    to = s.w("once")
    s.add(E(bk, 76, 236, "lt", 0.6, "pop", 0.5)); s.fx(0.6, "whoosh", 0.5)        # frame in early; text at "Once"
    tw, th = s.w("was"), s.w("had")
    ps = ParaStates("Once upon a time, there {was} a beautiful princess who {had} a kind heart …", 46, 520, 150, 330,
                    {"0": YELLOW, "1": YELLOW}, [("0", tw), ("1", th)], to - 0.1, "up", line_gap=1.45)
    s.add(ps)
    s.add(E(icon("book", 190), 1040, 420, "mm", to - 0.3, "pop", 0.4))
    s.add(E(icon("heart", 120), 1040, 620, "mm", th, "pop", 0.4))
    s.add(E(text_img("PAST TENSES", 32, fill=ORANGE), 1040, 730, "mm", tw, "fade"))
    s.add(E(pill_img("was", 40, YELLOW, INK, kind="nun", weight="ExtraBold"), 975, 800, "mm", tw + 0.2, "pop"))
    s.add(E(pill_img("had", 40, YELLOW, INK, kind="nun", weight="ExtraBold"), 1110, 800, "mm", th + 0.2, "pop"))
    s.fx(tw, "pop", 0.6); s.fx(th, "pop", 0.6)
    s.add(sparkle_burst(1040, 420, to, 10, 160, seed=31))
    return s


def s_42():
    s = Scene("4.2", "S4_2", hold=0.9, layout="small", level=4, label=LABEL[4])
    tsy = s.w("synopsis")
    c = card(1290, 100, CYAN, 22, 26, 3)
    im, _ = para("{synopsis|s} = a short summary of a film, play or book", 40, 1240, colors={"s": CYAN}, underline=False)
    c.alpha_composite(im, (24, 22))
    s.add(E(c, 100, 152, "lt", tsy, "left", 0.4)); s.fx(tsy, "whoosh", 0.4)
    tp = s.w("present")
    im, _ = para("SYNOPSIS / RETELLING → {PRESENT TENSES|p}", 44, 1200, kind="fred", weight="Bold", colors={"p": MINT})
    s.add(E(im, 100, 280, "lt", s.w("retell"), "wipe", 0.6))
    s.add(E(chip("lively", MINT, (20, 70, 60), 30), 100, 370, "lt", s.w("dramatic") - 0.2, "pop"))
    s.add(E(chip("dramatic", MINT, (20, 70, 60), 30), 260, 370, "lt", s.w("dramatic"), "pop"))
    s.fx(tp, "pop", 0.6)
    td, tsp, tsh = s.w("dora"), s.w("spot"), s.w("shark")
    comic = Image.new("RGBA", (1290, 530), (0, 0, 0, 0)); d = ImageDraw.Draw(comic)
    d.rounded_rectangle((0, 0, 1289, 529), radius=20, fill=(18, 40, 90, 255), outline=WHITE, width=8)
    d.ellipse((1080, 40, 1200, 160), fill=YELLOW + (230,))
    for k in range(3):
        yy = 420 + k * 34
        pts = [(x, yy + 10 * math.sin(x / 40 + k)) for x in range(20, 1270, 10)]
        d.line(pts, fill=CYAN + (200,), width=5)

    def comicf(fr, t, p):
        z = 1.0
        if t >= tsh:
            q = clamp((t - tsh) / 0.25); z = 1 + 0.045 * e_out(q)
        jx = 6 * math.sin((t - tsh) * 60) * clamp(1 - (t - tsh) / 0.4) if t >= tsh else 0
        place(fr, comic, 745 + jx, 470 + 265, "mm", e_out(p), z)
    s.add(Fn(comicf, td - 0.5, 0.4))
    s.add(ParaStates("Dora and Sam {are resting|a} on the beach when suddenly, they {spot|b} a shark …", 44, 760, 140, 520,
                     {"a": PINK, "b": YELLOW}, [("a", s.w("resting")), ("b", tsp)], td - 0.1, "up"))
    s.add(E(icon("shark", 230), 1130, 790, "mm", tsp - 0.2, "up", 0.5))            # rises out of the waves
    s.add(E(text_img("!", 150, glow_r=12, glow_col=ORANGE, fill=YELLOW), 990, 760, "mm", tsh, "pop", 0.25))
    s.fx(tsp, "whoosh", 0.6); s.fx(tsh, "glitch", 0.5)
    s.kay(tsh, s.dur, "eyes", "surprised")
    return s


def s_43():
    s = Scene("4.3", "S4_3", hold=0.9, layout="small", level=4, label=LABEL[4])
    s.add(ParaStates("{Careful!|c} Real-world facts stay in the past.", 44, 1250, 100, 152, {"c": ORANGE}, [("c", 0.3)], 0.2,
                     "up"))
    zA = card(600, 330, MINT, 22, 30, 5)
    zA.alpha_composite(icon("clapper", 90), (20, 20))
    d = ImageDraw.Draw(zA)
    d.text((125, 28), "INSIDE THE STORY", font=F("fred", 36, "Bold"), fill=MINT)
    d.text((125, 76), "present", font=F("nun", 30, "ExtraBold"), fill=WHITE)
    zB = card(620, 330, ORANGE, 22, 30, 5)
    d = ImageDraw.Draw(zB)
    d.text((28, 28), "OUTSIDE THE STORY", font=F("fred", 36, "Bold"), fill=ORANGE)
    d.text((28, 76), "real-world facts: past", font=F("nun", 30, "ExtraBold"), fill=WHITE)
    tt = s.w("the")
    s.add(E(zA, 100, 250, "lt", tt - 0.3, "pop", 0.4), E(zB, 760, 250, "lt", tt - 0.1, "pop", 0.4))
    ps = ParaStates("The film {was|was} a big hit when it {came out|came} {in 2008|t}. In the film, Harry the superhero "
                    "{saves|saves} thousands of lives.", 42, 1260, 100, 640, {"was": YELLOW, "came": YELLOW, "t": CYAN,
                                                                              "saves": YELLOW},
                    [("was", s.w("was")), ("came", s.w("came")), ("t", s.w("came") + 0.5), ("saves", s.w("saves"))], tt - 0.1, "up")
    s.add(ps)
    for k, txt, col, dst in (("was", "was", ORANGE, (900, 470)), ("came", "came out", ORANGE, (1130, 470)),
                             ("saves", "saves", MINT, (400, 470))):
        tk = dict(ps.order)[k] + 0.35
        s.add(Fly(pill_img(txt, 40, col, INK, kind="nun", weight="ExtraBold"), ps.centre(k), dst, tk, 0.6))
        s.fx(tk + 0.55, "pop", 0.6)
    return s


def s_44():
    s = Scene("4.4", "S4_4", hold=1.0, layout="std", level=4, label=LABEL[4])
    o1 = [("is", s.w("is")), ("read", s.w("read")), ("was", s.w("was"))]
    o2 = [("reaches", s.w("reaches")), ("gives", s.w("gives")), ("saves", s.w("saves")), ("live", s.w("live"))]
    p1, p2 = bubbles(s, 0.0, o1, o2)
    tag_on(s, p1, "is", "TRUE NOW", MINT, s.w("true"))
    tf = s.w("finished")
    tag_on(s, p1, "read", "FINISHED", ORANGE, tf); tag_on(s, p1, "was", "FINISHED", ORANGE, tf)
    for k, t in o2:
        tag_on(s, p2, k, "SYNOPSIS", CYAN, t + 0.1)
        s.fx(t, "pop", 0.5)
    s.fx(s.w("true"), "pop", 0.6); s.fx(tf, "pop", 0.6)
    te = s.w("every")
    s.add(E(text_img("?", 190, glow_r=18, glow_col=ORANGE, fill=YELLOW), 1050, 895, "mm", 0.0, "fade", 0.3, out=te, out_dur=0.15))
    s.add(E(glow(tick_img(140), 16, MINT), 1050, 902, "mm", te + 0.1, "pop", 0.4))
    s.fx(te + 0.1, "correct", 0.8)
    s.add(sparkle_burst(1050, 902, te + 0.2, 12, 200, seed=44))
    s.kay(s.w("reason") - 0.1, s.dur, "eyes", "wink")
    return s


def s_Q0():
    s = Scene("Q0", "SQ0", hold=0.5, layout="large", level=4, label="BOSS QUIZ")
    big = text_img("BOSS QUIZ", 150, glow_r=20, glow_col=PINK, fill=WHITE, stroke=5, stroke_col=PINK)
    s.add(E(big, 470, 430, "mm", 0.05, "zoom", 0.35)); s.fx(0.05, "sting", 0.7)
    for i in range(4):
        s.add(E(circle_num(i + 1, 80, NAVY, YELLOW), 230 + i * 120, 600, "mm", 0.4 + i * 0.12, "pop")); s.fx(0.4 + i * 0.12, "pop", 0.4)
    s.add(E(text_img("Say your answers out loud!", 46, "nun", "ExtraBold", fill=CYAN), 470, 720, "mm", s.w("say"), "up"))
    s.kay(0.05, 0.45, "bounce")
    s.kay(s.vend - 0.2, s.dur, "eyes", "wink")
    return s


def s_Q(n, voice, q, ph, ans, acol, tags, cue2):
    s = Scene(f"Q{n}", voice, lead=3.95, hold=1.2, layout="large", level=4, label="BOSS QUIZ")
    ph = "m" + ans.replace(" ", "m") + "m"
    s.add(E(pill_img(f"QUESTION {n} of 4", 34, YELLOW, INK), 100, 175, "lt", 0.05, "left"))
    ps = ParaStates(q.replace("___", "{" + ph + "|blank}"), 60, 780, 100, 280, {"blank": (0, 0, 0, 0)}, [], 0.1, "up",
                    line_gap=1.35)
    ps.base, _ = para(q.replace("___", "{" + ph + "|blank}"), 60, 780, colors={"blank": (0, 0, 0, 0)}, underline=False,
                      line_gap=1.35)
    ps.cache[0] = ps.base
    s.add(ps)
    bx = ps.box("blank")
    if bx[0] < ps.x + 8:                      # blank at the start of a line: begin exactly at the text's left edge
        bx = (ps.x,) + tuple(bx[1:])
    by = bx[1] + 74
    s.add(E(Image.new("RGBA", (int(bx[2] - bx[0]), 7), WHITE + (255,)), bx[0], by, "lt", 0.1, "wipe", 0.4))
    s.fx(0.1, "whoosh", 0.4)
    yb = 280 + ps.base.height + 40
    countdown(s, 300, yb + 110, 0.85)
    s.kay(0.6, 3.85, "pose", "thinking")
    ta = s.lead
    aim = text_img(ans, 68, "nun", "ExtraBold", fill=acol)
    # common BASELINE 18 px above the line (descenders may dip towards it); baseline found from the ink top,
    # which a soft drop shadow below the letters cannot distort
    fa = F("nun", 68, "ExtraBold")
    rows = np.nonzero((np.asarray(aim)[..., 3] > 128).any(1))[0]
    base_in = rows.min() - fa.getbbox(ans, anchor="ls")[1]
    s.add(E(aim, (bx[0] + bx[2]) / 2, by - 18 - base_in, "mt", ta, "pop", 0.3))
    x = 100
    if n == 3:
        wrong = pill_img("am wanting", 58, (90, 70, 120), DIM, kind="nun", weight="ExtraBold")
        s.add(E(wrong, x, yb + 60, "lt", ta, "pop"))
        fw = F("nun", 58, "ExtraBold")
        _, t0, _, b0 = fw.getbbox("am wanting", anchor="ls"); xh = -fw.getbbox("x", anchor="ls")[1]
        sy = yb + 60 + wrong.height / 2 + (-xh / 2 - (t0 + b0) / 2)      # through the middle of the x-height
        s.add(strike(x - 6, sy, x + wrong.width + 6, ta + 0.25, RED, 8))
        x += wrong.width + 30
    apill = pill_img(ans, 68, acol, INK if acol == YELLOW else WHITE, kind="nun", weight="ExtraBold")
    s.add(E(apill, x, yb + 50, "lt", ta + 0.05, "pop", 0.35))
    s.add(E(tick_img(86), x + apill.width + 24, yb + 50 + apill.height / 2, "lm", ta + 0.25, "pop"))
    s.fx(ta, "correct", 0.75)
    s.add(sparkle_burst(x + apill.width / 2, yb + 50 + apill.height / 2, ta + 0.1, 10, 220, seed=50 + n))
    tc = s.w(cue2)
    xx = 100
    for tg in tags:
        if "→" in tg:
            im, _ = para(tg, 34, 600, colors={}, fill=CYAN)
            c = Image.new("RGBA", (im.width + 40, 64), (0, 0, 0, 0))
            ImageDraw.Draw(c).rounded_rectangle((0, 0, c.width - 1, 63), radius=32, fill=NAVY + (255,))
            c.alpha_composite(im, (20, 6)); im = c
        else:
            im = chip(tg, CYAN, NAVY, 34)
        s.add(E(im, xx, yb + 50 + apill.height + 46, "lt", tc, "up", 0.35)); xx += im.width + 18
    s.kay(ta, ta + 0.7, "eyes", "wink")
    s.kay(ta, ta + 0.35, "bounce")
    return s


def bullet_tile(title, col, rows, w=540, h=205, px=24):
    """Cheat-sheet tile: title line + bullet rows. A row is a string (one bullet; '\n' = manual line break with a
    hanging indent) or a tuple of two strings (two bullets side by side). {word} = cyan signal word."""
    im = card(w, h, col, 22, 26, 3)
    d = ImageDraw.Draw(im)
    d.text((px, 16), title, font=F("fred", 29, "Bold"), fill=col)
    f = F("nun", 24, "Bold")
    LH, y, col2 = 31, 81, 252
    def seg_line(x, ym, line):
        for k, part in enumerate(line.replace("}", "{").split("{")):
            if part:
                gl.check_glyphs(part, f)
                d.text((x, ym), part, font=f, fill=CYAN if k % 2 else WHITE, anchor="lm")
                x += d.textlength(part, font=f)
    for row in rows:
        items = row if isinstance(row, tuple) else (row,)
        n_lines = 1
        for j, it in enumerate(items):
            x = px + j * col2
            d.ellipse((x + 2, y - 5, x + 12, y + 5), fill=col)
            for k, line in enumerate(it.split("\n")):
                seg_line(x + 24, y + k * LH, line)
            n_lines = max(n_lines, len(it.split("\n")))
        y += n_lines * LH
    return im
def s_C():
    s = Scene("C", "SC", hold=4.2, layout="small", level=4, label="SUMMARY")
    X0, TX, TY, TW, TH, PX = 100, (280, 845), (280, 498), 540, 205, 24
    s.add(E(text_img("CHEAT SHEET", 50, glow_r=10, glow_col=ORANGE, fill=YELLOW), X0, 150, "lt", 0.05, "left"))
    s.add(E(text_img("SIMPLE", 34, fill=YELLOW), TX[0] + PX, 232, "lt", 0.15, "fade"),
          E(text_img("CONTINUOUS", 34, fill=PINK), TX[1] + PX, 232, "lt", 0.15, "fade"))
    s.add(E(text_img("PRESENT", 32, fill=MINT), X0, TY[0] + TH / 2, "lm", 0.2, "fade"),
          E(text_img("PAST", 32, fill=ORANGE), X0, TY[1] + TH / 2, "lm", 0.2, "fade"))
    tiles = [("simple present · I play", YELLOW, 0, 0,
              ["facts", "true now", "habits: {every day}, {often},\n{usually}, {always}"]),
             ("present continuous · I am playing", PINK, 1, 0,
              [("right now", "temporary"), ("changing trends", "photos"), "annoying habits ({always})"]),
             ("simple past · I played", YELLOW, 0, 1,
              ["finished actions", "time words: {yesterday}, {last week},\n{two years ago}, {in 2013}"]),
             ("past continuous · I was playing", PINK, 1, 1,
              ["in progress at a past time", "long action + short action ({when})", "two actions at the same time ({while})"])]
    for i, (ttl, col, cx, cy, rows) in enumerate(tiles):
        s.add(E(bullet_tile(ttl, col, rows, TW, TH, PX), TX[cx], TY[cy], "lt", 0.3 + i * 0.15, "pop", 0.35))
        s.fx(0.3 + i * 0.15, "pop", 0.4)
    strips = [("NON-ACTION VERBS", "like · want · think · know · see · smell · have: no -ing", CYAN),
              ("TENSES IN STORIES", "story → past · synopsis / retelling → present · real-world facts → past", CYAN)]
    pw = max(pill_img(lab, 24, CYAN, INK, h=48, padx=16).width for lab, _, _ in strips)
    SW = TX[1] + TW - X0                                   # strips span exactly the label column + both tiles
    for i, (lab, txt, col) in enumerate(strips):
        y = TY[1] + TH + 13 + i * 95                       # same 13 px gap as between the tile rows
        im = Image.new("RGBA", (SW, 82), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle((0, 0, SW - 1, 81), radius=24, fill=NAVY + (220,), outline=col + (200,), width=3)
        lp0 = pill_img(lab, 24, col, INK, h=48, padx=16)
        lp = pill_img(lab, 24, col, INK, h=48, padx=16 + (pw - lp0.width) // 2)   # equal pill widths
        im.alpha_composite(lp, (17, 17))
        pi, _ = para(txt, 27, SW - pw - 70, weight="ExtraBold")
        im.alpha_composite(pi, (17 + pw + 24, (82 - pi.height) // 2 + 2))
        s.add(E(im, X0, y, "lt", 0.9 + i * 0.2, "left", 0.4))
    st = pill_img("Pause & screenshot!", 36, YELLOW, INK, kind="fred", weight="Bold").rotate(6, expand=True, resample=Image.BICUBIC)
    tp = s.w("pause")
    s.add(E(glow(st, 10, YELLOW, 0.7), 1150, 975, "mm", tp, "pop", 0.4, pulse=0.025)); s.fx(tp, "pop", 0.8)
    s.kay(s.w("screenshot"), s.w("screenshot") + 0.8, "eyes", "wink")
    return s
QUIZ = [
    (1, "SQ1", "Look! The baby ___ (sleep).", "is sleep", "is sleeping", PINK, ["Look! = right now"], "its"),
    (2, "SQ2", "I ___ (do) my homework when the lights went out.", "was doing", "was doing", PINK,
     ["long action, interrupted"], "long"),
    (3, "SQ3", "Right now, I ___ (want) a new phone.", "wanting", "want", YELLOW, ["non-action verb", "no -ing"], "its"),
    (4, "SQ4", "In the film, the hero ___ (fly) to the moon and saves the planet.", "flies", "flies", YELLOW,
     ["synopsis = present", "fly → flies"], "in"),
]


def all_scenes():
    sc = [s_L0(), s_L1(), s_H(), s_M(), s_level(1, "S1_0"), s_11(), s_12(), s_13(), s_level(2, "S2_0"), s_21(), s_22(),
          s_T(), s_level(3, "S3_0"), s_31(), s_32(), s_33(), s_level(4, "S4_0"), s_41(), s_42(), s_43(), s_44(), s_Q0()]
    sc += [s_Q(*q) for q in QUIZ]
    sc += [s_C(), s_L3(), s_L4()]
    prev = None
    for s in sc:
        s.prev_layout = prev
        prev = s.layouts[-1][1]
    return sc
