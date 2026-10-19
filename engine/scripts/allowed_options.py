"""Build listening options for the final 'd' of 'allowed' in the hook line (scene H).

Each option is the hook line as it would appear in the video (prepared exactly like the build),
mixed with the real music/SFX bed at that moment, then measured and packaged:
  output/allowed_options/Option_N.wav  +  output/allowed_options/allowed_options_compare.mp4
"""
import json, os, subprocess, sys
import numpy as np, soundfile as sf, pyloudnorm as pyln
from scipy.signal import resample_poly
from PIL import Image, ImageDraw, ImageFont

ROOT = "/home/ubuntu/kslo_grammar"
sys.path.insert(0, f"{ROOT}/scripts")
import prep_voice as pv
from dcheck import measure

OUT = f"{ROOT}/output/allowed_options"; WORK = f"{ROOT}/work/allowed_options"
os.makedirs(OUT, exist_ok=True); os.makedirs(WORK, exist_ok=True)
SR_RAW = 24000
CUTS = json.load(open("/tmp/sh_cuts.json")); DCH = json.load(open("/tmp/sh_dcheck.json"))


def raw(name):
    x, sr = sf.read(f"{ROOT}/audio/vo/{name}.wav"); assert sr == SR_RAW
    return x.mean(1) if x.ndim > 1 else x


def atten(x, a, b, db, ramp=0.003):
    """Lower x between a and b seconds by db, with short raised-cosine ramps."""
    g = np.ones(len(x)); ia, ib, r = int(a * SR_RAW), int(b * SR_RAW), int(ramp * SR_RAW)
    lo = 10 ** (-db / 20); w = 0.5 - 0.5 * np.cos(np.linspace(0, np.pi, r))
    g[ia:ib] = lo; g[ia - r:ia] = 1 - (1 - lo) * w; g[ib:ib + r] = lo + (1 - lo) * w
    return x * g


def splice(base, ins, cb, ci, xf=0.010):
    """Replace base[cb0:cb1] with ins[ci0:ci1] (cut points are in silence), RMS-matched, 10 ms crossfades."""
    b0, b1 = int(cb[0] * SR_RAW), int(cb[1] * SR_RAW); i0, i1 = int(ci[0] * SR_RAW), int(ci[1] * SR_RAW)
    seg = ins[i0:i1].copy(); ref = base[b0:b1]
    act = lambda y: np.sqrt(np.mean(y[np.abs(y) > 0.02 * np.abs(y).max()] ** 2))
    seg *= act(ref) / act(seg)
    n = int(xf * SR_RAW); f = np.linspace(0, 1, n)
    left, right = base[:b0].copy(), base[b1:].copy()
    seg[:n] = seg[:n] * f + left[-n:] * (1 - f); left = left[:-n]
    seg[-n:] = seg[-n:] * (1 - f) + right[:n] * f; right = right[n:]
    return np.concatenate([left, seg, right])


# ---- the options -------------------------------------------------------------------------------
SH = raw("SH"); ve = DCH["SH"]["vowel_end"]; A, B = ve + 0.057, ve + 0.135      # release region of the original 'd'
E = raw("SH_allowed_E"); veE = DCH["SH_allowed_E"]["vowel_end"]                  # take E: burst +35..42 ms, voiced 'uh' +42..60 ms
E_line = splice(SH, E, CUTS["SH"], CUTS["SH_allowed_E"])
E_soft = splice(SH, atten(E, veE + 0.043, veE + 0.066, 10), CUTS["SH"], CUTS["SH_allowed_E"])
OPTIONS = [
    ("1", "Original recording, untouched", "Strongest ‘d’ (the very first version)", SH),
    ("2", "Original recording, ‘d’ 3 dB softer", "Strong, clear ‘d’", atten(SH, A, B, 3)),
    ("3", "Original recording, ‘d’ 5 dB softer", "Clear ‘d’ – in the current video", atten(SH, A, B, 5)),
    ("4", "Original recording, ‘d’ 8 dB softer", "Gentle ‘d’", atten(SH, A, B, 8)),
    ("5", "Different recording (take E)", "Firm ‘d’ with a slight ‘uh’ after it", E_line),
    ("6", "Different recording (take E), ‘uh’ softened", "Firm ‘d’, ‘uh’ turned down", E_soft),
]

# ---- prepare exactly like the build, then mix with the real bed --------------------------------
from faster_whisper import WhisperModel
asr = WhisperModel("small.en", device="cpu", compute_type="int8")
tl = {d["sid"]: d for d in json.load(open(f"{ROOT}/build/timeline.json"))}; base = tl["H"]["t0"] + tl["H"]["lead"]
SR = 48000
mono = lambda y: y.mean(1) if y.ndim > 1 else y
bed = sum(mono(sf.read(f"{ROOT}/build/stem_{k}.wav")[0]) for k in ("music", "sfx"))
final = mono(sf.read(f"{ROOT}/build/qa/final_audio.wav")[0])
K = 10 ** (-0.7 / 20)                     # voice gain prepared line -> mix (measured)
lvl = lambda y, t, w=0.005: 20 * np.log10(np.sqrt(np.mean(y[int(t * SR):int((t + w) * SR)] ** 2)) + 1e-9)


def words(y, sr):
    segs, _ = asr.transcribe(resample_poly(y, 16000, sr).astype(np.float32), word_timestamps=True, beam_size=5, language="en")
    return [(w.word.strip(), w.start, w.end) for s in segs for w in s.words]


res = []
for num, title, desc, x in OPTIONS:
    sf.write(f"{WORK}/raw_{num}.wav", x.astype(np.float32), SR_RAW)
    y, _ = pv.prep(pv.load(f"{WORK}/raw_{num}.wav"))
    y = y * 10 ** ((-18.0 - pyln.Meter(pv.SR).integrated_loudness(y)) / 20); pk = np.abs(y).max(); y = y * 0.93 / pk if pk > 0.93 else y
    if pv.SR != SR: y = resample_poly(y, SR, pv.SR)
    ws = words(y, SR)
    al = [w for w in ws if w[0].lower().startswith(("allowed", "loud", "aloud"))][-1]
    nx = [w for w in ws if w[0].lower().startswith("let")][-1][1]
    th = [w for w in ws if w[0].lower().startswith("then")][-1][1]
    r = measure(y, SR, al[1], nx - 0.02)
    a, b = th - 0.25, len(y) / SR + 0.35                          # clip: '... then present again? Is that allowed? Let's find out.'
    v = np.zeros(int((b - a) * SR)); seg = y[int(a * SR):] * K; v[:len(seg)] = seg[:len(v)]
    bd = bed[int((base + a) * SR):int((base + a) * SR) + len(v)]
    mix = v + bd
    t_rel = r["rel_t"] - a
    over = max(lvl(v, t_rel + o) for o in (-0.005, 0, 0.005)) - np.median([lvl(bd, t_rel + o, 0.01) for o in np.arange(-0.05, 0.05, 0.01)])
    res.append(dict(num=num, title=title, desc=desc, mix=mix, a=a, d_vs_vowel=round(r["rel_full_vs_vowel"], 1),
                    over_music=round(float(over), 1), tail_ms=r["tail_ms"], allowed_at=round(al[1] - a, 2)))

# one common gain so the clips match the finished video's loudness (option 3 = the current video)
cur = res[2]; seg_f = final[int((base + cur["a"]) * SR):int((base + cur["a"]) * SR) + len(cur["mix"])]
G = np.sqrt(np.mean(seg_f ** 2)) / np.sqrt(np.mean(cur["mix"] ** 2))
for o in res:
    o["mix"] = np.clip(o["mix"] * G, -0.99, 0.99)
    sf.write(f"{OUT}/Option_{o['num']}.wav", o["mix"].astype(np.float32), SR, subtype="PCM_16")

# ---- labelled comparison video -----------------------------------------------------------------
W_, H_ = 1280, 720
FRED, NUN = f"{ROOT}/fonts/Fredoka.ttf", f"{ROOT}/fonts/Nunito.ttf"
def font(p, s, wt):
    f = ImageFont.truetype(p, s)
    try: f.set_variation_by_axes([wt] if p == NUN else [wt, 100])   # Fredoka axes: weight, width
    except Exception: pass
    return f
def card(o):
    im = Image.new("RGB", (W_, H_)); px = np.zeros((H_, W_, 3), np.uint8)
    g = np.linspace(0, 1, H_)[:, None]
    for c, (t, bt) in enumerate(((24, 70), (18, 28), (52, 92))): px[..., c] = (t + (bt - t) * g).astype(np.uint8)
    im = Image.fromarray(px); d = ImageDraw.Draw(im)
    d.rounded_rectangle((90, 110, W_ - 90, H_ - 110), 36, outline=(0, 220, 255), width=4, fill=(36, 28, 78))
    f1, f2, f3, f4 = font(FRED, 104, 700), font(NUN, 44, 800), font(NUN, 36, 600), font(NUN, 30, 600)
    def ctext(y, s, f, fill):
        bb = d.textbbox((0, 0), s, font=f); d.text(((W_ - (bb[2] - bb[0])) / 2 - bb[0], y), s, font=f, fill=fill)
    ctext(160, f"Option {o['num']}", f1, (255, 214, 0))
    ctext(320, o["title"], f2, (255, 255, 255))
    ctext(390, o["desc"], f3, (205, 195, 240))
    ctext(500, "\u2018Is that allowed? Let\u2019s find out.\u2019", f4, (0, 220, 255))
    return im
parts = []
for o in res:
    card(o).save(f"{WORK}/card_{o['num']}.png")
    pad0, pad1 = np.zeros(int(0.9 * SR)), np.zeros(int(0.9 * SR))
    sf.write(f"{WORK}/aud_{o['num']}.wav", np.concatenate([pad0, o["mix"], pad1]).astype(np.float32), SR)
    seg = f"{WORK}/seg_{o['num']}.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-framerate", "30", "-i", f"{WORK}/card_{o['num']}.png",
                    "-i", f"{WORK}/aud_{o['num']}.wav", "-shortest", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-tune", "stillimage",
                    "-c:a", "aac", "-b:a", "256k", "-ar", "48000", seg], check=True)
    parts.append(seg)
open(f"{WORK}/list.txt", "w").write("".join(f"file '{p}'\n" for p in parts))
subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", f"{WORK}/list.txt", "-c", "copy",
                f"{OUT}/allowed_options_compare.mp4"], check=True)

json.dump([{k: v for k, v in o.items() if k != "mix"} for o in res], open(f"{WORK}/options.json", "w"), indent=1)
for o in res:
    print(f"Option {o['num']}: {o['title']:45s} d {o['d_vs_vowel']:6.1f} dB vs vowel | {o['over_music']:+5.1f} dB over music | tail {o['tail_ms']:2d} ms | 'allowed' at {o['allowed_at']:.2f} s in clip")
print(f"common gain {20 * np.log10(G):+.1f} dB; files in {OUT}")
