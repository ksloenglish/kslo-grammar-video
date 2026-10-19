"""Natural cartoon hand (open palm, five numbered fingertips), round 4.
The silhouette is ONE signed-distance field: palm + tapered fingers + thumb blended with a smooth minimum
(polynomial smin). Every join (finger valleys, the thumb web) is a mathematically smooth fillet, so there are no
kinks or notches where pieces meet (the problem with the earlier stamp-and-blur approach, kept in hand_v3_blur.py).
Edges are anti-aliased analytically from the distance value."""
import sys
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, "/home/ubuntu/kslo_grammar/render")
import gl
from gl import PINK, YELLOW, WHITE, INK, F, glow

S = 460                                   # design canvas (px)
PALM = ((238, 268), (240, 326), 80, 74)    # ONE convex tapered palm: top centre, bottom centre, radii
# (base point inside the palm, tip-circle centre, base radius, tip radius); thumb first
FINGERS = [((206, 352), (80, 222), 37, 24),       # thumb (wide base = thumb muscle)
           ((178, 270), (140, 96), 27.5, 24),     # index
           ((222, 262), (213, 58), 28, 24.5),     # middle
           ((265, 266), (285, 78), 27, 23.5),     # ring
           ((286, 300), (342, 138), 24, 21)]      # little
K_FINGER, K_THUMB, K_PALM = 13.0, 20.0, 34.0      # smooth-min radii (fillet sizes)


def _rcone(px, py, a, b, r1, r2):
    """Exact SDF of a 2-D 'round cone' (capsule whose radius goes r1 -> r2), after Inigo Quilez."""
    bax, bay = b[0] - a[0], b[1] - a[1]
    l2 = bax * bax + bay * bay
    rr = r1 - r2
    a2 = l2 - rr * rr
    il2 = 1.0 / l2
    pax, pay = px - a[0], py - a[1]
    y = pax * bax + pay * bay
    z = y - l2
    qx, qy = pax * l2 - bax * y, pay * l2 - bay * y
    x2 = qx * qx + qy * qy
    y2, z2 = y * y * l2, z * z * l2
    k = np.sign(rr) * rr * rr * x2
    d_b = np.sqrt(x2 + z2) * il2 - r2
    d_a = np.sqrt(x2 + y2) * il2 - r1
    d_m = (np.sqrt(np.maximum(x2 * a2 * il2, 0)) + y * rr) * il2 - r1
    return np.where(np.sign(z) * a2 * z2 > k, d_b, np.where(np.sign(y) * a2 * y2 < k, d_a, d_m))


def _rbox(px, py, c, h, r):
    qx = np.abs(px - c[0]) - (h[0] - r)
    qy = np.abs(py - c[1]) - (h[1] - r)
    return np.hypot(np.maximum(qx, 0), np.maximum(qy, 0)) + np.minimum(np.maximum(qx, qy), 0) - r


def _smin(a, b, k):
    h = np.clip(0.5 + 0.5 * (b - a) / k, 0, 1)
    return b * (1 - h) + a * h - k * h * (1 - h)


def hand_sdf(scale=1.0):
    n = int(S * scale)
    ys, xs = np.mgrid[0:n, 0:n].astype(np.float64)
    px, py = (xs + 0.5) / scale, (ys + 0.5) / scale
    palm = _rcone(px, py, *PALM)
    fingers = None
    for a, b, r1, r2 in FINGERS[1:]:
        f = _rcone(px, py, a, b, r1, r2)
        fingers = f if fingers is None else np.minimum(fingers, f)
    d = _smin(palm, fingers, K_FINGER)
    a, b, r1, r2 = FINGERS[0]
    d = _smin(d, _rcone(px, py, a, b, r1, r2), K_THUMB)
    return d * scale                       # distance in output pixels


def hand_img(lit=0, size=300, fill=(255, 122, 192), line=(255, 222, 238), edge=5):
    sc = 2.0                               # render at 2x the design canvas, then resize
    d = hand_sdf(sc)
    e = edge * sc
    alpha = np.clip(0.5 - d, 0, 1)
    linemix = np.clip(d + e + 0.5, 0, 1)   # 1 within `edge` of the outline, 0 deeper inside
    rgba = np.zeros(d.shape + (4,), np.float32)
    for c in range(3):
        rgba[..., c] = fill[c] * (1 - linemix) + line[c] * linemix
    rgba[..., 3] = alpha * 255
    img = Image.fromarray(rgba.astype(np.uint8), "RGBA")
    dr = ImageDraw.Draw(img)
    f = F("fred", int(25 * sc), "Bold")
    for i, (a, b, r1, r2) in enumerate(FINGERS):
        ux, uy = b[0] - a[0], b[1] - a[1]
        L = (ux * ux + uy * uy) ** 0.5
        x, y = (b[0] - ux / L * 3) * sc, (b[1] - uy / L * 3) * sc   # badge centred in the rounded fingertip
        r = (r2 - 5) * sc
        dr.ellipse((x - r, y - r, x + r, y + r), fill=YELLOW if i < lit else WHITE)
        gl.centred_text(dr, (x - r, y - r, x + r, y + r), str(i + 1), f, INK)
    img = img.crop(img.getbbox())          # visual centre = image centre
    img = glow(img, 24, PINK, 0.8)         # (2x canvas: same glow as the 12 px used before)
    s = size / img.height
    return img.resize((round(img.width * s), size), Image.LANCZOS)


if __name__ == "__main__":
    row = Image.new("RGBA", (1560, 560), (40, 30, 80, 255))
    for k, lit in enumerate((0, 3, 5)):
        row.alpha_composite(hand_img(lit, 460), (20 + k * 480, 40))
    row.alpha_composite(hand_img(2, 150), (1420, 40))
    row.convert("RGB").save("/tmp/hand_v4.jpg", quality=92)
