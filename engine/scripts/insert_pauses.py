"""Insert silent pauses into a prepared voice line and shift its word timings.
usage: insert_pauses.py BASE OUT word[:n]=seconds ...   (pause goes in the middle of the gap after the n-th 'word')
Writes audio/vo_prep/OUT.wav and words.json[OUT]; BASE is left untouched (idempotent)."""
import sys, json, numpy as np, soundfile as sf
ROOT = "/home/ubuntu/kslo_grammar/audio/vo_prep"
base, out, specs = sys.argv[1], sys.argv[2], sys.argv[3:]
x, sr = sf.read(f"{ROOT}/{base}.wav")
W = json.load(open(f"{ROOT}/words.json"))
words = [list(w) for w in W[base]]
norm = lambda s: "".join(c for c in s.lower() if c.isalnum())
cuts = []
for sp in specs:
    key, sec = sp.split("="); n = 1
    if ":" in key:
        key, n = key.split(":"); n = int(n)
    idx = [i for i, w in enumerate(words) if norm(w[0]) == norm(key)][n - 1]
    # ASR word ends are often early (e.g. 'yesterday' ended 0.1 s after its timestamp), so never cut at the timestamp:
    # search 0-0.6 s after it for the first quiet run (< -55 dBFS for >= 40 ms) and cut at its quietest 10 ms frame.
    mono = x if x.ndim == 1 else x.mean(1)
    fr = int(0.01 * sr); t0 = words[idx][2]
    db = []
    for j in range(60):
        seg = mono[int((t0 + j * 0.01) * sr):int((t0 + j * 0.01) * sr) + fr]
        db.append(20 * np.log10(np.sqrt((seg ** 2).mean()) + 1e-9) if len(seg) else -200)
    t, run = None, []
    for j, v in enumerate(db):
        if v < -55:
            run.append(j)
            if len(run) >= 4:
                jj = min(run, key=lambda q: db[q]); t = t0 + jj * 0.01 + 0.005; break
        else:
            run = []
    if t is None:
        jj = int(np.argmin(db)); t = t0 + jj * 0.01 + 0.005
        print(f"WARNING: no clean silence after '{words[idx][0]}', cutting at the quietest point ({db[jj]:.0f} dB)")
    cuts.append((t, float(sec), idx))
cuts.sort()
parts, last, shift = [], 0, 0.0
for t, sec, idx in cuts:
    k = int(t * sr)
    seg = x[last:k].copy(); nf = min(int(0.008 * sr), len(seg))          # 8 ms fades either side of the cut
    if nf:
        seg[-nf:] *= np.linspace(1, 0, nf).reshape((-1,) + (1,) * (x.ndim - 1))
    x[k:k + nf] *= np.linspace(0, 1, len(x[k:k + nf])).reshape((-1,) + (1,) * (x.ndim - 1))
    parts += [seg, np.zeros((int(sec * sr),) + x.shape[1:])]
    last = k
    print(f"pause {sec:.2f}s after '{words[idx][0]}' at {t:.2f}s")
parts.append(x[last:])
y = np.concatenate(parts)
new = []
for w, a, b in words:
    s = sum(sec for t, sec, _ in cuts if b > t)        # shift every word not finished before the cut
    new.append([w, round(a + s, 3), round(b + s, 3)])
sf.write(f"{ROOT}/{out}.wav", y, sr, subtype="PCM_16")
W[out] = new
json.dump(W, open(f"{ROOT}/words.json", "w"))
print(f"{out}: {len(x)/sr:.2f}s -> {len(y)/sr:.2f}s")
