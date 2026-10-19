# -*- coding: utf-8 -*-
"""Prepare body voice lines: trim edges, tighten long internal pauses, normalise loudness. -> audio/vo_prep/<id>.wav
Pauses longer than MAXGAP are shortened to KEEP (never removed), so phrasing stays natural."""
import json, glob, os
import numpy as np, soundfile as sf, pyloudnorm as pyln
from scipy.signal import resample_poly

ROOT = "/home/ubuntu/kslo_grammar"
SR = 48000
MAXGAP, KEEP = 0.42, 0.34
BODY = ["SH", "SM", "S1_0", "S1_1", "S1_2", "S1_3", "S2_0", "S2_1", "S2_2", "S3_0", "S3_1", "S3_2", "S3_3",
        "S4_0", "S4_1", "S4_2", "S4_3", "S4_4", "SQ0", "SQ1", "SQ2", "SQ3", "SQ4", "SC"]


def load(f):
    x, sr = sf.read(f)
    x = x if x.ndim == 1 else x.mean(1)
    return resample_poly(x, SR, sr) if sr != SR else x


def prep(x):
    h = SR // 100
    e = np.array([np.sqrt((x[i:i + h] ** 2).mean()) for i in range(0, len(x) - h, h)])
    thr = max(e.max() * 0.025, 1e-4)
    voiced = e > thr
    idx = np.where(voiced)[0]
    a, b = idx[0], idx[-1] + 1
    out, i, removed = [], a, 0.0
    while i < b:
        if voiced[i]:
            j = i
            while j < b and voiced[j]:
                j += 1
            out.append(x[i * h:j * h]); i = j
        else:
            j = i
            while j < b and not voiced[j]:
                j += 1
            g = (j - i) * h / SR
            if g > MAXGAP:
                keep = int(KEEP * SR); seg = x[i * h:j * h]
                fade = int(0.02 * SR)
                s1, s2 = seg[:keep // 2].copy(), seg[-keep // 2:].copy()
                s1[-fade:] *= np.linspace(1, 0, fade); s2[:fade] *= np.linspace(0, 1, fade)
                out.append(np.concatenate([s1, s2])); removed += g - KEEP
            else:
                out.append(x[i * h:j * h])
            i = j
    y = np.concatenate([np.zeros(int(0.03 * SR)), x[max(0, a * h - int(0.04 * SR)):a * h], *out,
                        x[b * h:b * h + int(0.12 * SR)]])
    return y, removed


def main():
    takes = json.load(open(f"{ROOT}/audio/takes.json"))
    os.makedirs(f"{ROOT}/audio/vo_prep", exist_ok=True)
    meter = pyln.Meter(SR)
    info, tot0, tot1 = {}, 0, 0
    for k in BODY:
        src = takes.get(k, k)
        x = load(f"{ROOT}/audio/vo/{src}.wav")
        y, rem = prep(x)
        lu = meter.integrated_loudness(y)
        y = y * 10 ** ((-18.0 - lu) / 20)
        pk = np.abs(y).max()
        if pk > 0.93:
            y = y * 0.93 / pk          # cap peaks by gain, never clip
        sf.write(f"{ROOT}/audio/vo_prep/{k}.wav", y.astype(np.float32), SR)
        info[k] = dict(src=src, before=round(len(x) / SR, 2), after=round(len(y) / SR, 2), removed=round(rem, 2))
        tot0 += len(x) / SR; tot1 += len(y) / SR
    json.dump(info, open(f"{ROOT}/audio/vo_prep/prep.json", "w"), indent=1)
    for k, v in info.items():
        print(k, v)
    print(f"total {tot0:.1f} -> {tot1:.1f} s")


if __name__ == "__main__":
    main()
