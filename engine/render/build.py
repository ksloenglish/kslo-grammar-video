# -*- coding: utf-8 -*-
"""Build: python3 build.py timeline | stills SID t ... | sheet [SID ...] | render [SID ...] | audio | mux"""
import sys, os, json, subprocess, time
from multiprocessing import Pool
import numpy as np, soundfile as sf
sys.path.insert(0, os.path.dirname(__file__))
from PIL import Image, ImageDraw
import gl
from engine import ClipReader

ROOT = gl.ROOT
sys.path.insert(0, f"{ROOT}/proto")
import layer as LY
OUT = f"{ROOT}/build"
SR = 48000
os.makedirs(f"{OUT}/seg", exist_ok=True); os.makedirs(f"{OUT}/stills", exist_ok=True)
_SC = None


def scenes():
    global _SC
    if _SC is None:
        import scenes as S
        _SC = S.all_scenes()
        for s in _SC:                       # proto/holds/<sid>.txt overrides the hold after the voice
            h = LY.hold_override(s.sid)
            if h is not None and s.voice_id and not s.clip:
                s.dur = s.lead + s.vlen + h
        t = 0.0
        for s in _SC:
            s.t0 = t
            s.nf = int(round(s.dur * gl.FPS))
            t += s.nf / gl.FPS
        for s in _SC:                       # design-led scenes: browser layer replaces the PIL lesson graphics
            s.html = LY.is_html(s.sid)
            if s.html:
                s.cues = LY.cues_for(s)
                s.els, s.panel = [], False
    return _SC
_LAYER = [None, None]
def html_frame(s, t):
    if _LAYER[0] is None:
        _LAYER[0] = LY.Layer()
    if _LAYER[1] != s.sid:
        _LAYER[0].open(s.sid, s.cues); _LAYER[1] = s.sid
    return _LAYER[0].frame(t)
def compose(s, t, cr=None, L=None):
    fr = s.render(t, s.t0 + t, cr)
    if not getattr(s, "html", False):
        return fr
    g = L.frame(t) if L is not None else html_frame(s, t)
    fr = fr.convert("RGBA"); fr.alpha_composite(g)
    return fr.convert("RGB")


def find(sid):
    return next(i for i, s in enumerate(scenes()) if s.sid == sid)


def timeline():
    sc = scenes()
    for s in sc:
        print(f"{s.sid:4s} start {s.t0:7.2f}  dur {s.dur:6.2f}  layout {s.layouts[-1][1]}")
    tot = sc[-1].t0 + sc[-1].nf / gl.FPS
    print(f"TOTAL {tot:.2f} s = {int(tot // 60)}:{tot % 60:05.2f}")
    return tot


def render_still(sid, t):
    s = scenes()[find(sid)]
    cr = None
    if s.clip:
        cr = ClipReader(s.clip)
        for _ in range(int(t * gl.FPS)):
            cr.next()
    return compose(s, t, cr)


def stills(sid, ts):
    for t in ts:
        im = render_still(sid, float(t))
        p = f"{OUT}/stills/{sid}_{float(t):05.2f}.jpg"
        im.save(p, quality=88); print(p)


def sheet(sids=None):
    sc = scenes()
    sel = [s for s in sc if not sids or s.sid in sids]
    for s in sel:
        ts = [min(s.dur - 0.3, x) for x in (s.dur * 0.35, s.dur * 0.7, s.dur - 0.3)]
        tiles = [render_still(s.sid, t).resize((640, 360)) for t in ts]
        im = Image.new("RGB", (1920, 360))
        for i, t in enumerate(tiles):
            ImageDraw.Draw(t).text((8, 8), f"{s.sid} {ts[i]:.1f}s", fill=(255, 0, 0)); im.paste(t, (i * 640, 0))
        p = f"{OUT}/stills/sheet_{s.sid}.jpg"; im.save(p, quality=85); print(p)


def render_scene(i):
    s = scenes()[i]
    p = f"{OUT}/seg/{i:02d}_{s.sid}.mp4"
    t0 = time.time()
    ff = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{gl.W}x{gl.H}",
                           "-r", str(gl.FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                           "-pix_fmt", "yuv420p", "-r", str(gl.FPS), p], stdin=subprocess.PIPE)
    cr = ClipReader(s.clip) if s.clip else None
    L = None
    if s.html:
        L = LY.Layer(); L.open(s.sid, s.cues)
    for f in range(s.nf):
        t = f / gl.FPS
        ff.stdin.write(compose(s, t, cr, L).tobytes())
    ff.stdin.close(); ff.wait()
    if L is not None:
        L.close()
    return s.sid, s.nf, round(time.time() - t0, 1)


def render(sids=None):
    sc = scenes()
    idx = [i for i, s in enumerate(sc) if not sids or s.sid in sids]
    idx.sort(key=lambda i: -sc[i].nf)
    with Pool(6) as pool:
        for r in pool.imap_unordered(render_scene, idx):
            print("done", r, flush=True)
    if not sids:
        with open(f"{OUT}/concat.txt", "w") as f:
            for i, s in enumerate(sc):
                f.write(f"file '{OUT}/seg/{i:02d}_{s.sid}.mp4'\n")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", f"{OUT}/concat.txt", "-c", "copy",
                        f"{OUT}/video.mp4"], check=True)
        print("video", f"{OUT}/video.mp4")


# ----------------------------------------------------------------------------- audio
def load(p):
    from scipy.signal import resample_poly
    x, sr = sf.read(p, always_2d=True)
    x = x.mean(1) if x.shape[1] == 1 else x
    if sr != SR:
        x = resample_poly(x, SR, sr, axis=0)
    if x.ndim == 1:
        x = np.stack([x, x], 1)
    return x


def lufs_norm(x, target):
    import pyloudnorm as pyln
    lu = pyln.Meter(SR).integrated_loudness(x)
    return x * 10 ** ((target - lu) / 20)


def add(buf, x, t, g=1.0):
    i = int(round(t * SR))
    if i >= len(buf):
        return
    n = min(len(x), len(buf) - i)
    buf[i:i + n] += x[:n] * g


def audio():
    sc = scenes()
    tot = sc[-1].t0 + sc[-1].nf / gl.FPS
    N = int(tot * SR) + SR
    voice = np.zeros((N, 2)); sfx = np.zeros((N, 2)); music = np.zeros((N, 2))
    HS = LY.html_sfx(sc)                    # design-led scenes define their own SFX (keyed to their visuals)
    json.dump(HS, open(f"{OUT}/html_sfx.json", "w"))
    for s in sc:
        if s.voice_id:
            add(voice, load(f"{ROOT}/audio/vo_prep/{s.voice_id}.wav"), s.t0 + s.lead)
        if s.clip_audio:
            add(voice, lufs_norm(load(s.clip_audio), -15.0), s.t0)  # = -18 mono, like vo_prep
        for t, name, g in (HS.get(s.sid, s.sfx) if HS else s.sfx):
            add(sfx, load(f"{ROOT}/audio/sfx/{name}.wav"), s.t0 + t, g * 0.55)
    # music
    theme = lufs_norm(load(f"{ROOT}/audio/music/theme.wav"), -16.0)
    bed = lufs_norm(load(f"{ROOT}/audio/music/study_bed.wav"), -16.0)
    iH, iL3 = find("H"), find("L3")
    t_body0, t_body1 = sc[iH].t0, sc[iL3].t0
    # theme intro: L0 + L1, fading out over the last 1.5 s of L1
    a_end = t_body0 + 0.3
    seg = theme[:int(a_end * SR)].copy()
    fo = int(1.8 * SR); seg[-fo:] *= np.linspace(1, 0, fo)[:, None]
    add(music, seg, 0.0, 1.0)
    # bed: looped with 2 s crossfades, from body start to outro start (+0.8 s overlap)
    L = int((t_body1 - t_body0 + 1.5) * SR)
    loop, xf = np.zeros((0, 2)), int(2 * SR)
    while len(loop) < L:
        b = bed.copy()
        if len(loop):
            b[:xf] *= np.linspace(0, 1, xf)[:, None]
            loop[-xf:] *= np.linspace(1, 0, xf)[:, None]
            loop[-xf:] += b[:xf]; loop = np.concatenate([loop, b[xf:]])
        else:
            loop = b
    loop = loop[:L]
    fi = int(0.6 * SR); loop[:fi] *= np.linspace(0, 1, fi)[:, None]
    fo = int(1.2 * SR); loop[-fo:] *= np.linspace(1, 0, fo)[:, None]
    add(music, loop, t_body0 - 0.2, 0.62)
    # theme ending under outro + end card, aligned so the theme ends with the video
    t_out = sc[iL3].t0
    dur_out = tot - t_out
    st = max(0, len(theme) / SR - dur_out - 0.2)
    seg = theme[int(st * SR):].copy()
    fi = int(1.0 * SR); seg[:fi] *= np.linspace(0, 1, fi)[:, None]
    add(music, seg, t_out - 0.2, 1.0)
    # music gain curve: full under logo/end card, lower under speech, ducked further while voice is active
    g = np.full(N, 0.38)
    g[:int(4.0 * SR)] = 0.9
    for s in sc:                                   # thinking time: let the bed come up
        if s.sid in ("Q1", "Q2", "Q3", "Q4"):
            g[int((s.t0 + 0.5) * SR):int((s.t0 + 3.85) * SR)] = 0.8
        if s.sid == "C":
            g[int((s.t0 + s.vend + 0.3) * SR):int((s.t0 + s.dur) * SR)] = 0.75
    iL4 = find("L4")
    g[int(sc[iL4].t0 * SR):] = 0.85
    from scipy.ndimage import maximum_filter1d, uniform_filter1d
    env = np.abs(voice[:, 0])
    env = maximum_filter1d(env, int(0.25 * SR))
    act = np.clip(env / 0.05, 0, 1)
    act = uniform_filter1d(act, int(0.3 * SR))
    g = g * (1 - 0.4 * act)
    rampN = int(0.8 * SR)
    g = uniform_filter1d(g, rampN)
    mix = voice + sfx + music * g[:, None]
    mix = mix[:int(tot * SR)]
    import pyloudnorm as pyln
    k = 10 ** ((-16.0 - pyln.Meter(SR).integrated_loudness(mix)) / 20)
    mix = mix * k
    if os.environ.get("STEMS"):
        for nm, st in (("voice", voice), ("sfx", sfx), ("music", music * g[:, None])):
            sf.write(f"{OUT}/stem_{nm}.wav", (st[:len(mix)] * k).astype(np.float32), SR)
    # end: fade to silence together with the picture (black from L4 + 5.4 s), silence held to the end
    f0 = int((sc[iL4].t0 + 4.5) * SR); f1 = int((sc[iL4].t0 + 5.4) * SR)
    fenv = np.ones(len(mix)); fenv[f0:f1] = 0.5 * (1 + np.cos(np.linspace(0, np.pi, f1 - f0))); fenv[f1:] = 0
    mix = mix * fenv[:, None]
    # simple look-ahead peak limiter at -1 dBFS
    lim = 0.89
    pk = maximum_filter1d(np.abs(mix).max(1), int(0.005 * SR))
    gain = np.minimum(1, lim / np.maximum(pk, 1e-9))
    gain = -maximum_filter1d(-gain, int(0.01 * SR))
    gain = uniform_filter1d(gain, int(0.004 * SR))
    mix = mix * gain[:, None]
    mix = np.clip(mix, -0.99, 0.99)
    sf.write(f"{OUT}/mix.wav", mix.astype(np.float32), SR)
    import pyloudnorm as pyln
    print("mix", f"{OUT}/mix.wav", round(len(mix) / SR, 2), "s  LUFS", round(pyln.Meter(SR).integrated_loudness(mix), 1),
          "peak", round(float(np.abs(mix).max()), 3))
    json.dump([dict(sid=s.sid, t0=round(s.t0, 3), dur=round(s.nf / gl.FPS, 3), lead=s.lead, voice=s.voice_id)
               for s in sc], open(f"{OUT}/timeline.json", "w"), indent=1)


def mux(out=None):
    out = out or f"{ROOT}/output/Kayla_Grammar_Lab_The_present_and_the_past.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", f"{OUT}/video.mp4", "-i", f"{OUT}/mix.wav", "-map", "0:v",
                    "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart",
                    out], check=True)
    print("final", out)


if __name__ == "__main__":
    cmd, args = sys.argv[1], sys.argv[2:]
    if cmd == "timeline":
        timeline()
    elif cmd == "stills":
        stills(args[0], args[1:])
    elif cmd == "sheet":
        sheet(args)
    elif cmd == "render":
        render(args)
    elif cmd == "audio":
        audio()
    elif cmd == "mux":
        mux()
