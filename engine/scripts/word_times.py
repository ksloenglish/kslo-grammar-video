# -*- coding: utf-8 -*-
"""Word timestamps for prepared body lines -> audio/vo_prep/words.json  {id: [[word, start, end], ...]}"""
import json, glob, os
from faster_whisper import WhisperModel
import soundfile as sf, numpy as np
from scipy.signal import resample_poly

ROOT = "/home/ubuntu/kslo_grammar"
m = WhisperModel("small.en", device="cpu", compute_type="int8")
out = {}
for f in sorted(glob.glob(f"{ROOT}/audio/vo_prep/*.wav")):
    k = os.path.basename(f)[:-4]
    x, sr = sf.read(f); x = x if x.ndim == 1 else x.mean(1)
    x = resample_poly(x, 16000, sr).astype(np.float32)
    segs, _ = m.transcribe(x, word_timestamps=True, beam_size=5, language="en")
    ws = []
    for s in segs:
        for w in s.words:
            ws.append([w.word.strip(), round(w.start, 3), round(w.end, 3)])
    out[k] = ws
    print(k, " ".join(w[0] for w in ws))
json.dump(out, open(f"{ROOT}/audio/vo_prep/words.json", "w"), indent=0)
print("saved")
