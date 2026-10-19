# -*- coding: utf-8 -*-
"""Core graphics for Kayla's Grammar Lab renderer (Style A · Neon Stream). 1920x1080, PIL RGBA."""
import math, functools
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# ----------------------------------------------------------------------------- anti-aliased shapes (round 4)
# Pillow draws ellipses, rounded rectangles, polygons and lines with hard, stair-stepped edges. Every such call on an
# RGB/RGBA image is routed through _aa(): the shape is drawn into a 4x supersampled coverage mask, box-reduced, and
# applied with EXACTLY Pillow's own semantics at full coverage (RGBA = replace, RGB = opaque paint), blended in
# premultiplied space at the edges (no dark fringes). Masks on L/1 images keep the original behaviour.
_AA_K = 4
_ORIG = {n: getattr(ImageDraw.ImageDraw, n) for n in ("ellipse", "rounded_rectangle", "polygon", "line", "arc")}
def _pts(xy):
    if len(xy) and isinstance(xy[0], (tuple, list)):
        return [(float(a), float(b)) for a, b in xy]
    return [(float(xy[i]), float(xy[i + 1])) for i in range(0, len(xy), 2)]
def _ink(c, mode):
    from PIL import ImageColor
    if isinstance(c, str):
        c = ImageColor.getrgb(c)
    c = tuple(int(v) for v in c)
    return c + (255,) if len(c) == 3 else c
def _apply(im, box, cov, ink):
    x0, y0, x1, y1 = box
    reg = np.asarray(im.crop(box)).astype(np.float32)
    m = cov[..., None]
    if im.mode == "RGBA":
        a = reg[..., 3:4] / 255.0
        dp = np.concatenate([reg[..., :3] * a, a], -1)
        sa = ink[3] / 255.0
        sp = np.array([ink[0] * sa, ink[1] * sa, ink[2] * sa, sa], np.float32)
        op = dp * (1 - m) + sp * m
        oa = op[..., 3:4]
        rgb = np.where(oa > 1e-6, op[..., :3] / np.maximum(oa, 1e-6), 0)
        out = np.concatenate([rgb, oa * 255.0], -1)
    else:
        out = reg * (1 - m) + np.array(ink[:3], np.float32) * m
    im.paste(Image.fromarray(np.clip(out + 0.5, 0, 255).astype(np.uint8), im.mode), (x0, y0))
def _aa(self, kind, xy, fill=None, outline=None, width=1, **kw):
    im = getattr(self, "_image", None)
    if im is None or im.mode not in ("RGBA", "RGB") or (fill is None and outline is None) or isinstance(fill, int) \
            or isinstance(outline, int):
        return _ORIG[kind](self, xy, fill=fill, outline=outline, width=width, **kw) if kind not in ("line", "arc") \
            else _ORIG[kind](self, xy, fill=fill, width=width, **kw)
    P = _pts(xy)
    if not P:
        return
    K = _AA_K
    xs, ys = [p[0] for p in P], [p[1] for p in P]
    pad = 3 + (width if kind == "line" else 0)
    bx0, by0 = max(0, int(math.floor(min(xs))) - pad), max(0, int(math.floor(min(ys))) - pad)
    bx1, by1 = min(im.width, int(math.ceil(max(xs))) + pad + 2), min(im.height, int(math.ceil(max(ys))) + pad + 2)
    if bx1 <= bx0 or by1 <= by0:
        return
    W_, H_ = bx1 - bx0, by1 - by0
    if kind in ("ellipse", "rounded_rectangle", "arc"):     # inclusive pixel box -> continuous box at K x
        (ax, ay), (bx, by) = P[0], P[1]
        sxy = [((ax - bx0) * K, (ay - by0) * K), ((bx + 1 - bx0) * K - 1, (by + 1 - by0) * K - 1)]
    else:                                                    # vertices sit on pixel centres
        sxy = [((x - bx0 + 0.5) * K - 0.5, (y - by0 + 0.5) * K - 0.5) for x, y in P]
    extra = dict(kw)
    if "radius" in extra:
        extra["radius"] = extra["radius"] * K
    def cov(**args):
        m = Image.new("L", (W_ * K, H_ * K), 0)
        _ORIG[kind](ImageDraw.Draw(m), sxy, **args, **extra)
        return np.asarray(m.reduce(K)).astype(np.float32) / 255.0
    box = (bx0, by0, bx1, by1)
    if kind in ("line", "arc"):
        if fill is not None:
            _apply(im, box, cov(fill=255, width=max(1, int(round(width * K)))), _ink(fill, im.mode))
        return
    if fill is not None:
        _apply(im, box, cov(fill=255), _ink(fill, im.mode))
    if outline is not None and width:
        _apply(im, box, cov(outline=255, width=max(1, int(round(width * K)))), _ink(outline, im.mode))
def _mk(kind):
    if kind == "arc":
        def f(self, xy, start, end, fill=None, width=1):
            return _aa(self, "arc", xy, fill=fill, width=width, start=start, end=end)
    elif kind == "line":
        def f(self, xy, fill=None, width=0, joint=None):
            kw = {"joint": joint} if joint else {}
            return _aa(self, "line", xy, fill=fill, width=width or 1, **kw)
    elif kind == "rounded_rectangle":
        def f(self, xy, radius=0, fill=None, outline=None, width=1, *, corners=None):
            kw = {"radius": radius}
            if corners is not None:
                kw["corners"] = corners
            return _aa(self, kind, xy, fill=fill, outline=outline, width=width, **kw)
    else:
        def f(self, xy, fill=None, outline=None, width=1):
            return _aa(self, kind, xy, fill=fill, outline=outline, width=width)
    return f
for _k in _ORIG:
    setattr(ImageDraw.ImageDraw, _k, _mk(_k))

ROOT = "/home/ubuntu/kslo_grammar"
W, H, FPS = 1920, 1080, 30
FRED, NUN = f"{ROOT}/fonts/Fredoka.ttf", f"{ROOT}/fonts/Nunito.ttf"
LOGO = "/home/ubuntu/kslo-vocab-video/brand/logo_white.png"
VIOLET_TOP, VIOLET_BOT = (21, 15, 51), (43, 20, 92)
CYAN, PINK, YELLOW, MINT = (46, 230, 255), (255, 79, 168), (255, 217, 61), (92, 242, 176)
WHITE, INK, RED, ORANGE = (255, 255, 255), (40, 20, 80), (255, 84, 104), (255, 164, 72)
NAVY = (30, 70, 110)
DIM = (205, 195, 240)
LILAC = (192, 166, 255)            # step titles: distinct from the pink/yellow/cyan used for highlighted words
SERIES, UNIT = "Kayla's Grammar Lab", "The present and the past"


# ----------------------------------------------------------------------------- fonts & glyphs
@functools.lru_cache(None)
def F(kind, size, weight="Bold"):
    f = ImageFont.truetype(FRED if kind == "fred" else NUN, size)
    f.set_variation_by_name(weight)
    return f


_CM = {}


def check_glyphs(text, f):
    from fontTools.ttLib import TTFont
    if f.path not in _CM:
        _CM[f.path] = set(TTFont(f.path).getBestCmap())
    miss = sorted({c for c in text if ord(c) not in _CM[f.path] and not c.isspace() and c not in "→✓✗"})
    if miss:
        raise ValueError(f"Font {f.path} cannot draw {miss} in {text!r}")


# ----------------------------------------------------------------------------- easing
def clamp(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x


def e_out(p):
    p = clamp(p); return 1 - (1 - p) ** 3


def e_inout(p):
    p = clamp(p); return 3 * p * p - 2 * p * p * p


def e_back(p, s=1.7):
    p = clamp(p); q = p - 1
    return 1 + (s + 1) * q ** 3 + s * q ** 2


# ----------------------------------------------------------------------------- compositing
def place(dst, img, x, y, anchor="lt", alpha=1.0, scale=1.0):
    """Alpha-composite img onto dst with anchor (lt, mm, lm, mt, rt, rm, mb, lb), alpha and scale; clips safely."""
    if img is None or alpha <= 0.003 or scale <= 0.01:
        return
    if abs(scale - 1) > 0.004:
        img = img.resize((max(1, round(img.width * scale)), max(1, round(img.height * scale))), Image.BILINEAR)
    w, h = img.size
    ax = {"l": 0, "m": 0.5, "r": 1}[anchor[0]]
    ay = {"t": 0, "m": 0.5, "b": 1}[anchor[1]]
    gp = img.info.get("gpad", 0) * scale          # text images: x/y refer to the INK box, not the glow margin
    x0, y0 = round(x - ax * (w - 2 * gp) - gp), round(y - ay * (h - 2 * gp) - gp)
    if alpha < 0.997:
        a = img.getchannel("A").point(lambda v: int(v * alpha))
        img = img.copy(); img.putalpha(a)
    cx0, cy0 = max(0, -x0), max(0, -y0)
    cx1, cy1 = min(w, dst.width - x0), min(h, dst.height - y0)
    if cx1 <= cx0 or cy1 <= cy0:
        return
    if (cx0, cy0, cx1, cy1) != (0, 0, w, h):
        img = img.crop((cx0, cy0, cx1, cy1))
    dst.alpha_composite(img, (x0 + cx0, y0 + cy0))


def glow(img, radius=14, color=None, strength=1.0, pad=None):
    """Return img with a soft neon halo underneath (colour of the art if color is None)."""
    pad = pad if pad is not None else radius * 2
    big = Image.new("RGBA", (img.width + 2 * pad, img.height + 2 * pad), (0, 0, 0, 0))
    big.alpha_composite(img, (pad, pad))
    a = big.getchannel("A").filter(ImageFilter.GaussianBlur(radius))
    a = a.point(lambda v: min(255, int(v * 1.6 * strength)))
    if color is None:
        col = big.filter(ImageFilter.GaussianBlur(radius)).convert("RGB")
        halo = col.copy().convert("RGBA")
    else:
        halo = Image.new("RGBA", big.size, color + (255,))
    halo.putalpha(a)
    halo.alpha_composite(big)
    return halo


# ----------------------------------------------------------------------------- background & header
@functools.lru_cache(None)
def background():
    y = np.linspace(0, 1, H)[:, None, None]
    base = (np.array(VIOLET_TOP) * (1 - y) + np.array(VIOLET_BOT) * y) * np.ones((H, W, 3))
    img = Image.fromarray(base.astype(np.uint8)).convert("RGBA")
    blobs = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(blobs)
    d.ellipse((-200, 650, 600, 1350), fill=PINK + (70,))
    d.ellipse((1250, -300, 2150, 500), fill=CYAN + (55,))
    img = Image.alpha_composite(img, blobs.filter(ImageFilter.GaussianBlur(160)))
    dots = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dd = ImageDraw.Draw(dots)
    for yy in range(30, H, 48):
        for xx in range(30, W, 48):
            dd.ellipse((xx - 2, yy - 2, xx + 2, yy + 2), fill=(255, 255, 255, 22))
    return Image.alpha_composite(img, dots)


@functools.lru_cache(None)
def logo(height):
    lg = Image.open(LOGO).convert("RGBA")
    return lg.resize((round(lg.width * height / lg.height), height), Image.LANCZOS)


def kf(text):
    """Fredoka kerns 'space + V' to 0.085 em (looks like no space: 'NON-ACTIONVERBS'); switch kerning off there."""
    return ["-kern"] if " V" in text else None


@functools.lru_cache(8192)
def ink_cols(text, f):
    """(first, last) column of VISIBLE ink (alpha > 100) relative to the pen x, measured by rendering - Pillow's
    textbbox() starts at the pen and ignores the glyph's left side bearing ('R', 'I', 'L' start ~4 px in at 60 px)."""
    if not text.strip():
        return 0, 0
    sz = getattr(f, "size", 60)
    w = int(ImageDraw.Draw(Image.new("L", (1, 1))).textlength(text, font=f, features=kf(text))) + 4 * sz
    im = Image.new("L", (w, 3 * sz), 0)
    ImageDraw.Draw(im).text((sz, 2 * sz), text, font=f, fill=255, anchor="ls", features=kf(text))
    cols = np.nonzero((np.asarray(im) > 100).any(0))[0]
    return (int(cols.min()) - sz, int(cols.max()) - sz) if len(cols) else (0, 0)
def centred_text(d, box, text, f, fill):
    """Text whose visible ink is optically centred in box (x1, y1, x2, y2)."""
    check_glyphs(text, f)
    l, t, r, b = d.textbbox((0, 0), text, font=f, anchor="ls", features=kf(text))
    cx, cy = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2
    c0, c1 = ink_cols(text, f)
    l, r = c0, c1 + 1
    letters = [c for c in text if c.isalpha() or c.isdigit()]
    if letters:
        lower_only = all(c.islower() for c in letters)
        band = -f.getbbox("x" if lower_only else "H", anchor="ls")[1]     # x-height or cap height above baseline
        d.text((cx - (l + r) / 2, cy + band / 2), text, font=f, fill=fill, anchor="ls", features=kf(text))
    else:
        d.text((cx - (l + r) / 2, cy - (t + b) / 2), text, font=f, fill=fill, anchor="ls", features=kf(text))


@functools.lru_cache(None)
def header_img(level_idx, label):
    """Transparent full-width header: logo (same height as divider), series + unit title, level chip, 4 dots."""
    img = Image.new("RGBA", (W, 110), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    LT, LB = 30, 88
    lg = logo(LB - LT)
    img.alpha_composite(lg, (44, LT))
    x = 44 + lg.width + 26
    d.line((x - 13, LT, x - 13, LB), fill=(255, 255, 255, 90), width=2)
    d.text((x, 22), SERIES, font=F("fred", 34, "Bold"), fill=WHITE)
    d.text((x, 62), UNIT, font=F("nun", 24, "Bold"), fill=CYAN)
    rx = W - 44
    dots_w = 4 * 26
    for i in range(4):
        cx = rx - dots_w + 13 + i * 26
        d.ellipse((cx - 8, 49, cx + 8, 65), fill=YELLOW if i < level_idx else (255, 255, 255, 70))
    if label:
        f = F("fred", 26, "SemiBold")
        tw = d.textlength(label, font=f)
        px1 = rx - dots_w - 20 - tw - 44
        d.rounded_rectangle((px1, 30, rx - dots_w - 20, 84), radius=27, fill=YELLOW + (255,))
        centred_text(d, (px1, 30, rx - dots_w - 20, 84), label, f, INK)
    return img


# ----------------------------------------------------------------------------- shapes
def arrow_img(length=60, color=WHITE, th=8, head=22):
    img = Image.new("RGBA", (length + 4, head + 4), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cy = (head + 4) / 2
    d.rounded_rectangle((2, cy - th / 2, length - head + 6, cy + th / 2), radius=th // 2, fill=color)
    d.polygon([(length - head, 2), (length + 2, cy), (length - head, head + 2)], fill=color)
    return img


def tick_img(size=86, bg=MINT, fg=(20, 60, 40)):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse((0, 0, size - 1, size - 1), fill=bg)
    s = size / 86
    d.line((22 * s, 44 * s, 39 * s, 63 * s, 68 * s, 24 * s), fill=fg, width=max(4, int(10 * s)), joint="curve")
    return img


def cross_img(size=86, bg=RED, fg=WHITE):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse((0, 0, size - 1, size - 1), fill=bg)
    m, w = size * 0.3, max(4, int(size * 0.11))
    d.line((m, m, size - m, size - m), fill=fg, width=w)
    d.line((m, size - m, size - m, m), fill=fg, width=w)
    return img


def circle_num(n, d=90, bg=PINK, fg=WHITE, fsize=None):
    img = Image.new("RGBA", (d, d), (0, 0, 0, 0))
    dr = ImageDraw.Draw(img)
    dr.ellipse((0, 0, d - 1, d - 1), fill=bg)
    f = F("fred", fsize or int(d * 0.62), "Bold")
    t = str(n); check_glyphs(t, f)
    m = Image.new("L", (d * 3, d * 3), 0)
    ImageDraw.Draw(m).text((d, 2 * d), t, font=f, fill=255, anchor="ls")
    a = np.asarray(m).astype(np.float64)
    ys, xs = np.nonzero(a > 0)
    cx = (a.sum(0) * np.arange(a.shape[1])).sum() / a.sum()
    cy = (ys.min() + ys.max() + 1) / 2
    layer = Image.new("RGBA", (d * 3, d * 3), fg + (0,) if len(fg) == 3 else fg)
    layer.putalpha(m)
    img.alpha_composite(layer, (int(round(d / 2 - cx)), int(round(d / 2 - cy))))
    return img


def panel_img(w, h, outline=CYAN, fill_a=20, radius=40, width=3, fill=None):
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((1, 1, w - 2, h - 2), radius=radius, fill=(fill or (255, 255, 255)) + (fill_a,),
                        outline=(outline + (130,)) if outline else None, width=width)
    return img


# ----------------------------------------------------------------------------- text
def text_img(text, size, kind="fred", weight="Bold", fill=WHITE, glow_r=0, glow_col=None, stroke=0, stroke_col=INK):
    f = F(kind, size, weight)
    check_glyphs(text, f)
    d0 = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    l, t, r, b = d0.textbbox((0, 0), text, font=f, anchor="ls", stroke_width=stroke, features=kf(text))
    pad = 4 + stroke
    img = Image.new("RGBA", (r - l + 2 * pad, b - t + 2 * pad), (0, 0, 0, 0))
    ImageDraw.Draw(img).text((pad - l, pad - t), text, font=f, fill=fill, anchor="ls", stroke_width=stroke,
                             stroke_fill=stroke_col, features=kf(text))
    cols = np.nonzero((np.asarray(img)[..., 3] > 100).any(0))[0]
    if len(cols) and (cols.min() != pad or cols.max() != img.width - 1 - pad):
        img = img.crop((int(cols.min()) - pad, 0, int(cols.max()) + 1 + pad, img.height))
    out = glow(img, glow_r, glow_col) if glow_r else img
    out.info["gpad"] = pad + (2 * glow_r if glow_r else 0)
    return out


def pill_img(text, size, bg, fg, kind="fred", weight="Bold", padx=None, h=None, glow_r=0, outline=None):
    f = F(kind, size, weight)
    check_glyphs(text, f)
    d0 = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    l, t, r, b = d0.textbbox((0, 0), text, font=f, anchor="ls", features=kf(text))
    hh = h or int(size * 1.5)
    padx = padx if padx is not None else int(size * 0.62)
    w = (r - l) + 2 * padx
    img = Image.new("RGBA", (w, hh), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, w - 1, hh - 1), radius=hh // 2, fill=bg if len(bg) == 4 else bg + (255,),
                        outline=outline, width=3 if outline else 0)
    centred_text(d, (0, 0, w, hh), text, f, fg)
    return glow(img, glow_r, bg[:3]) if glow_r else img


def para(text, size, width, kind="nun", weight="ExtraBold", fill=WHITE, colors=None, line_gap=1.28, align="l",
         underline=True):
    """Wrap text into width. Words written {like this} (or {like this|key}) are TRACKED: each gets an id (key or
    running index) and is drawn in colors[key] (default fill) with an underline. '→' draws as an arrow shape.
    Returns (img, boxes) where boxes[key] = (x0, y0, x1, y1) of the tracked phrase inside img."""
    f = F(kind, size, weight)
    colors = colors or {}
    toks, i, n = [], 0, 0
    glue = set()                              # indices of tokens drawn with no space before them
    while i < len(text):                      # tokenize into (word, key or None)
        if i > 0 and text[i] not in " \n" and text[i - 1] not in " \n" and toks:
            glue.add(len(toks))
        if text[i] == "\n":                    # manual line break
            toks.append(("\n", None, True, True)); i += 1
        elif text[i] == "{":
            j = text.index("}", i)
            body = text[i + 1:j]
            key = body.split("|")[1] if "|" in body else str(n)
            words = body.split("|")[0].split(" ")
            for k, wd in enumerate(words):
                toks.append((wd, key, k == 0, k == len(words) - 1))
            n += 1; i = j + 1
        elif text[i] == " ":
            i += 1
        else:
            j = i
            while j < len(text) and text[j] not in " {\n":
                j += 1
            toks.append((text[i:j], None, True, True)); i = j
    check_glyphs("".join(t[0] for t in toks if t[0] != "\n"), f)
    d0 = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    sp = d0.textlength(" ", font=f)
    aw = int(size * 1.1)

    def wlen(wd):
        return sum(aw if c == "→" else d0.textlength(c, font=f) for c in wd) if "→" in wd else d0.textlength(wd, font=f)
    lines, cur, cw = [], [], 0
    for ti, t in enumerate(toks):
        if t[0] == "\n":
            lines.append((cur, cw)); cur, cw = [], 0
            continue
        wl = wlen(t[0])
        g = ti in glue
        if cur and not g and cw + sp + wl > width:
            lines.append((cur, cw)); cur, cw = [], 0
        cw = cw + (sp if cur and not g else 0) + wl
        cur.append((t + (g,), wl))
    if cur:
        lines.append((cur, cw))
    lh = int(size * line_gap)
    asc = f.getmetrics()[0]
    img = Image.new("RGBA", (int(max(c for _, c in lines)) + 8 if align == "l" else width + 8,
                             lh * len(lines) + int(size * 0.35)), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    boxes = {"_lines": {}}
    for li, (ln, cw) in enumerate(lines):
        if align == "l":
            w0 = ln[0][0][0] if ln else ""
            x = -ink_cols(w0, f)[0] if w0 and "→" not in w0[:1] else 0
        else:
            x = 4 + (width - cw) / 2
        y = li * lh
        runs, prev_key = [], None            # underline runs: ONE bar per phrase per line (no seams between words)
        for k, (t, wl) in enumerate(ln):
            wd, key, first, last, g = t
            if g and k:
                x -= sp
            col = colors.get(key, fill) if key is not None else fill
            if "→" in wd:
                xx = x
                for c in wd:
                    if c == "→":
                        a = arrow_img(int(aw * 0.8), col, max(4, size // 9), max(12, size // 3))
                        img.alpha_composite(a, (int(xx + aw * 0.08), int(y + asc * 0.62 - a.height / 2)))
                        xx += aw
                    else:
                        d.text((xx, y), c, font=f, fill=col); xx += d0.textlength(c, font=f)
            else:
                d.text((x, y), wd, font=f, fill=col)
            if key is not None:
                bx = boxes.get(key)
                x1 = x + wl + (0 if last else sp)
                boxes[key] = (min(bx[0], x) if bx else x, y, max(bx[2], x + wl) if bx else x + wl, y + lh)
                lb = boxes["_lines"].setdefault(key, [])
                if lb and lb[-1][1] == y:
                    lb[-1] = (lb[-1][0], y, x + wl, y + lh)
                else:
                    lb.append((x, y, x + wl, y + lh))
                if underline and key in colors:
                    uy = y + asc + max(4, size // 9)
                    if runs and prev_key == key:
                        runs[-1][2] = x + wl
                    else:
                        runs.append([key, x, x + wl, uy, col])
            prev_key = key
            x += wl + sp
        for _k, rx0, rx1, uy, ucol in runs:
            d.rounded_rectangle((rx0, uy, rx1, uy + max(4, size // 10)), radius=3, fill=ucol)
    return img, boxes


def bubble_img(w, h, tail="left", color=WHITE, fill_a=26, outline=CYAN, edge=4):
    """Speech bubble drawn as ONE merged shape (box + tail), so the outline runs round the tail with no seam."""
    import cv2
    K = 3
    m = Image.new("L", ((w + 40) * K, (h + 40) * K), 0)
    d = ImageDraw.Draw(m)
    d.rounded_rectangle((20 * K, 4 * K, (w + 20) * K, h * K), radius=36 * K, fill=255)
    if tail == "left":
        d.polygon([(74 * K, (h - 30) * K), (48 * K, (h + 34) * K), (132 * K, (h - 30) * K)], fill=255)
    else:
        d.polygon([((w - 92) * K, (h - 30) * K), ((w - 8) * K, (h + 34) * K), ((w - 34) * K, (h - 30) * K)], fill=255)
    a = (np.array(m) > 127).astype(np.uint8)
    dist = cv2.distanceTransform(a, cv2.DIST_L2, 5) / K
    ring = np.clip(dist, 0, 1) * np.clip(edge + 0.5 - dist, 0, 1)        # outline band, anti-aliased
    body = np.clip(dist - edge, 0, 1)
    al_ring, al_body = ring * 170, body * fill_a
    tot = np.maximum(al_ring + al_body, 1e-6)
    rgba = np.zeros(a.shape + (4,), np.float32)
    for c in range(3):
        rgba[..., c] = (outline[c] * al_ring + color[c] * al_body) / tot
    rgba[..., 3] = np.clip(al_ring + al_body, 0, 255)
    return Image.fromarray(rgba.astype(np.uint8), "RGBA").resize((w + 40, h + 40), Image.LANCZOS)
# ----------------------------------------------------------------------------- icons (neon sheet)
@functools.lru_cache(None)
def icon(name, size=120):
    im = Image.open(f"{ROOT}/design/icons/{name}.png").convert("RGBA")
    s = size / max(im.size)
    return im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS)
