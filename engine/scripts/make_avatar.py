# -*- coding: utf-8 -*-
"""Build Kayla's PNGtuber sprites from the keyframe and the nano-banana expression edits.
Face variants: align to base (SIFT + RANSAC similarity on body/hair, face masked out), then paste ONLY the changed
face area (feathered) onto the base, so the hair/body are pixel-identical across sprites (no jumps when swapping).
Pose variants (thinking): aligned whole image. All sprites share one crop box. Output: sprites/kayla_<name>.png"""
import sys, json
import numpy as np, cv2
from PIL import Image, ImageDraw
sys.path.insert(0, "/home/ubuntu/skills/kslo-vocab-video/scripts")
from keying import key

ROOT = "/home/ubuntu/kslo_grammar"
W, H = 2560, 1440
FACE = ["mouth_half", "mouth_open", "blink", "wink", "surprised"]
POSE = ["thinking"]


def load(p):
    return np.array(Image.open(p).convert("RGB").resize((W, H), Image.LANCZOS))


def align(base, var, mask_box=None):
    g1, g2 = cv2.cvtColor(base, cv2.COLOR_RGB2GRAY), cv2.cvtColor(var, cv2.COLOR_RGB2GRAY)
    m = np.full((H, W), 255, np.uint8)
    # ignore flat green background
    m[(base[..., 1] > 200) & (base[..., 0] < 90) & (base[..., 2] < 90)] = 0
    if mask_box:
        x0, y0, x1, y1 = mask_box
        m[y0:y1, x0:x1] = 0
    sift = cv2.SIFT_create(8000)
    k1, d1 = sift.detectAndCompute(g1, m)
    k2, d2 = sift.detectAndCompute(g2, None)
    bf = cv2.BFMatcher()
    good = [a for a, b in bf.knnMatch(d2, d1, k=2) if a.distance < 0.7 * b.distance]
    src = np.float32([k2[g.queryIdx].pt for g in good])
    dst = np.float32([k1[g.trainIdx].pt for g in good])
    M, inl = cv2.estimateAffinePartial2D(src, dst, method=cv2.RANSAC, ransacReprojThreshold=2.0)
    s = np.sqrt(M[0, 0] ** 2 + M[0, 1] ** 2)
    warped = cv2.warpAffine(var, M, (W, H), flags=cv2.INTER_LANCZOS4, borderValue=(0, 255, 0))
    return warped, dict(matches=len(good), inliers=int(inl.sum()), scale=round(float(s), 4),
                        tx=round(float(M[0, 2]), 1), ty=round(float(M[1, 2]), 1))


MOUTH = (1262, 394, 50, 34)                         # ellipse cx, cy, rx, ry (keyframe px)
EYE_L, EYE_R = (1180, 303, 68, 64), (1332, 299, 70, 64)
PATCHES = {  # name: (source variant, ellipses)
    "mouth_half": ("mouth_half", [MOUTH]), "mouth_open": ("mouth_open", [MOUTH]),
    "mouth_o": ("surprised", [MOUTH]), "eyes_blink": ("blink", [EYE_L, EYE_R]),
    "eyes_wink": ("wink", [EYE_R]), "eyes_surprised": ("surprised", [EYE_L, EYE_R]),
}


def ellipse_mask(ells, feather=7):
    m = np.zeros((H, W), np.float32)
    for cx, cy, rx, ry in ells:
        cv2.ellipse(m, (cx, cy), (rx - feather, ry - feather), 0, 0, 360, 1.0, -1)
    return cv2.GaussianBlur(m, (0, 0), feather)


def main():
    import os
    os.makedirs(f"{ROOT}/sprites", exist_ok=True)
    base = load(f"{ROOT}/design/kayla_keyframe_green.png")
    FB = (1120, 200, 1460, 520)
    aligned, info = {}, {}
    for n in FACE:
        aligned[n], info[n] = align(base, load(f"{ROOT}/design/expr/kayla_{n}.png"), FB)
    think, info["thinking"] = align(base, load(f"{ROOT}/design/expr/kayla_thinking.png"), (FB[0], FB[1], FB[2], FB[3] + 400))
    kb, kt = key(base), key(think)
    ys0 = xs0 = 10 ** 9; ys1 = xs1 = 0
    for k in (kb, kt):
        yy, xx = np.where(k[..., 3] > 8)
        ys0, ys1, xs0, xs1 = min(ys0, yy.min()), max(ys1, yy.max()), min(xs0, xx.min()), max(xs1, xx.max())
    box = (int(max(0, xs0 - 12)), int(max(0, ys0 - 12)), int(min(W, xs1 + 13)), H)
    info["crop"] = list(box)
    Image.fromarray(kb).crop(box).save(f"{ROOT}/sprites/kayla_base.png")
    Image.fromarray(kt).crop(box).save(f"{ROOT}/sprites/kayla_thinking.png")
    info["patches"] = {}
    for pn, (src, ells) in PATCHES.items():
        m = ellipse_mask(ells)
        yy, xx = np.where(m > 0.002)
        x0, y0, x1, y1 = int(xx.min()), int(yy.min()), int(xx.max()) + 1, int(yy.max()) + 1
        rgba = np.dstack([aligned[src][y0:y1, x0:x1], (m[y0:y1, x0:x1] * 255).astype(np.uint8)])
        Image.fromarray(rgba).save(f"{ROOT}/sprites/patch_{pn}.png")
        info["patches"][pn] = [x0 - box[0], y0 - box[1]]       # offset inside the cropped sprite
    json.dump(info, open(f"{ROOT}/sprites/sprites.json", "w"), indent=1)
    # QA: combinations
    combos = [("base", None, None), ("half", None, "mouth_half"), ("open", None, "mouth_open"),
              ("blink", "eyes_blink", None), ("wink+open", "eyes_wink", "mouth_open"),
              ("surprised", "eyes_surprised", "mouth_o"), ("blink+half", "eyes_blink", "mouth_half"), ("thinking", "T", None)]
    sb = Image.open(f"{ROOT}/sprites/kayla_base.png")
    tiles = []
    for lab, e, mth in combos:
        im = Image.open(f"{ROOT}/sprites/kayla_thinking.png") if e == "T" else sb.copy()
        for pn in (e, mth):
            if pn and pn != "T":
                im.alpha_composite(Image.open(f"{ROOT}/sprites/patch_{pn}.png"), tuple(info["patches"][pn]))
        bg = Image.new("RGBA", im.size, (30, 18, 70, 255)); bg.alpha_composite(im)
        fx, fy = 1060 - box[0], 170 - box[1]
        c = bg.crop((fx, fy, fx + 420, fy + 320)).convert("RGB")
        ImageDraw.Draw(c).text((8, 8), lab, fill=(255, 255, 0)); tiles.append(c)
    sheet = Image.new("RGB", (420 * 4, 320 * 2))
    for i, t in enumerate(tiles):
        sheet.paste(t, ((i % 4) * 420, (i // 4) * 320))
    sheet.save(f"{ROOT}/work/sprite_combos.jpg", quality=90)
    print(json.dumps(info["patches"]), box)


if __name__ == "__main__":
    main()
