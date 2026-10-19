# -*- coding: utf-8 -*-
"""QA for Kayla Seedance clips: contact sheet of N frames per variant, green-background check, clip transcript.
usage: python3 clip_qa.py NAME [N]   (uses clips/raw/NAME_v1.mp4, NAME_v2.mp4 ...)"""
import subprocess, sys, glob, json, os
import numpy as np
from PIL import Image, ImageDraw

ROOT = "/home/ubuntu/kslo_grammar/clips"
name = sys.argv[1]
N = int(sys.argv[2]) if len(sys.argv) > 2 else 8
files = sorted(glob.glob(f"{ROOT}/raw/{name}_v*.mp4"))
rows = []
for f in files:
    v = os.path.basename(f)[:-4]
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f],
                             capture_output=True, text=True).stdout)
    tiles, corners = [], []
    for k in range(N):
        t = min(d - 0.2, d * k / (N - 1))
        r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.2f}", "-i", f, "-frames:v", "1", "-f", "rawvideo",
                            "-pix_fmt", "rgb24", "-s", "1280x720", "-"], capture_output=True)
        a = np.frombuffer(r.stdout, np.uint8).reshape(720, 1280, 3)
        corners.append(a[:60, :60].reshape(-1, 3).mean(0).astype(int).tolist())
        im = Image.fromarray(a).resize((320, 180))
        ImageDraw.Draw(im).text((5, 5), f"{v} {t:.1f}s", fill=(255, 0, 0))
        tiles.append(im)
    row = Image.new("RGB", (320 * N, 180))
    for i, x in enumerate(tiles):
        row.paste(x, (i * 320, 0))
    rows.append(row)
    subprocess.run(["manus-speech-to-text", f], capture_output=True)
    tx = sorted(glob.glob(f"{ROOT}/raw/{v}_transcription_*.json"))
    txt = json.load(open(tx[-1]))["full_text"] if tx else "?"
    for p in glob.glob(f"{ROOT}/raw/{v}_transcription_*"):
        os.makedirs(f"{ROOT}/qa/asr", exist_ok=True); os.replace(p, f"{ROOT}/qa/asr/{os.path.basename(p)}")
    print(f"{v}: {d:.2f}s | bg corners min G-max(R,B) = {min(c[1] - max(c[0], c[2]) for c in corners)} | {txt}")
s = Image.new("RGB", (320 * N, 180 * len(rows)))
for i, r in enumerate(rows):
    s.paste(r, (0, i * 180))
s.save(f"{ROOT}/qa/{name}_sheet.jpg", quality=85)
print("sheet", f"{ROOT}/qa/{name}_sheet.jpg")
