# -*- coding: utf-8 -*-
"""Scene engine: Kayla avatar (layered PNGtuber), timed elements, library-clip playback, frame rendering."""
import json, math, functools, subprocess, random
import numpy as np, soundfile as sf
from PIL import Image
import gl
from gl import place, clamp, e_out, e_inout, e_back, W, H, FPS, ROOT

# (kayla centre x, top, height, panel right edge, panel alpha)
LAYOUTS = {"std": (1660, 330, 1000, 1170, 1.0), "small": (1730, 700, 560, 1400, 1.0),
           "large": (1460, 110, 1350, 1170, 0.0), "off": (1730, 1180, 560, 1400, 1.0)}


@functools.lru_cache(maxsize=64)
def panel_cached(w):
    return gl.panel_img(w, 900)
SPR_W, SPR_H, CLIP_X0 = 1414, 1440, 525          # sprite crop box x0 inside the 2560-wide keyframe
WORDS = json.load(open(f"{ROOT}/audio/vo_prep/words.json"))


# ----------------------------------------------------------------------------- avatar
class Avatar:
    def __init__(self):
        sp = f"{ROOT}/sprites"
        self.base = Image.open(f"{sp}/kayla_base.png").convert("RGBA")
        self.think = Image.open(f"{sp}/kayla_thinking.png").convert("RGBA")
        info = json.load(open(f"{sp}/sprites.json"))
        self.patches = {k: (Image.open(f"{sp}/patch_{k}.png").convert("RGBA"), tuple(v)) for k, v in info["patches"].items()}
        self.cache = {}

    def full(self, eyes, mouth, pose):
        key = (eyes, mouth, pose)
        if key not in self.cache:
            im = (self.think if pose == "thinking" else self.base).copy()
            if pose != "thinking":
                for p in (f"eyes_{eyes}" if eyes != "open" else None, f"mouth_{mouth}" if mouth != "closed" else None):
                    if p:
                        pim, off = self.patches[p]
                        im.alpha_composite(pim, off)
            self.cache[key] = im
        return self.cache[key]

    @functools.lru_cache(maxsize=256)
    def scaled(self, eyes, mouth, pose, h):
        im = self.full(eyes, mouth, pose)
        s = h / SPR_H
        return im.resize((max(1, round(SPR_W * s)), max(1, round(SPR_H * s))), Image.LANCZOS if h in (1000, 560, 1350)
                         else Image.BILINEAR)


AV = None


def avatar():
    global AV
    if AV is None:
        AV = Avatar()
    return AV


# blink schedule (global time)
_rng = random.Random(7)
BLINKS, _t = [], 1.4
while _t < 900:
    BLINKS.append(_t); _t += _rng.uniform(2.6, 4.8)


def blinking(tg):
    import bisect
    i = bisect.bisect_right(BLINKS, tg) - 1
    return i >= 0 and tg - BLINKS[i] < 0.13


def key_green(fr):
    f = fr.astype(np.float32)
    r, g, b = f[..., 0], f[..., 1], f[..., 2]
    mx = np.maximum(r, b)
    d = g - mx
    a = np.clip((150 - d) / (150 - 45), 0, 1)
    a = np.clip((a - 0.12) / 0.88, 0, 1)
    a[a < 0.03] = 0
    out = np.empty(fr.shape[:2] + (4,), np.uint8)
    out[..., 0] = fr[..., 0]; out[..., 1] = np.minimum(g, mx).astype(np.uint8); out[..., 2] = fr[..., 2]
    out[..., 3] = (a * 255).astype(np.uint8)
    return out


class ClipReader:
    """Sequential 30 fps reader of a retimed Seedance clip (1280x720)."""
    def __init__(self, path):
        self.p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", path, "-vf", "fps=30", "-f", "rawvideo", "-pix_fmt",
                                   "rgb24", "-"], stdout=subprocess.PIPE)
        self.last = None

    def next(self):
        b = self.p.stdout.read(1280 * 720 * 3)
        if len(b) == 1280 * 720 * 3:
            self.last = np.frombuffer(b, np.uint8).reshape(720, 1280, 3)
        return self.last


# ----------------------------------------------------------------------------- elements
class E:
    """Image element with entrance/exit animation. anim: pop, fade, up, down, left, right, drop, wipe, none, zoom."""
    def __init__(self, img, x, y, anchor="lt", t=0.0, anim="pop", dur=0.35, out=None, out_dur=0.25, pulse=0.0,
                 alpha=1.0):
        self.img, self.x, self.y, self.anchor, self.t, self.anim, self.dur = img, x, y, anchor, t, anim, dur
        self.out, self.out_dur, self.pulse, self.alpha = out, out_dur, pulse, alpha

    def state(self, t):
        if t < self.t:
            return None
        p = clamp((t - self.t) / self.dur)
        a, s, dx, dy = 1.0, 1.0, 0, 0
        an = self.anim
        if an == "pop":
            a, s = clamp(p * 2.5), 0.55 + 0.45 * e_back(p)
        elif an == "zoom":
            a, s = clamp(p * 2), 1.6 - 0.6 * e_out(p)
        elif an == "fade":
            a = e_out(p)
        elif an in ("up", "down", "left", "right", "drop"):
            a = clamp(p * 2)
            k = 1 - (e_back(p, 1.2) if an == "drop" else e_out(p))
            dist = {"up": (0, 50), "down": (0, -50), "left": (-70, 0), "right": (70, 0), "drop": (0, -90)}[an]
            dx, dy = dist[0] * k, dist[1] * k
        if self.out is not None and t > self.out:
            q = clamp((t - self.out) / self.out_dur)
            a *= 1 - q
            if q >= 1:
                return None
        if self.pulse and p >= 1:
            s *= 1 + self.pulse * 0.5 * (1 + math.sin((t - self.t) * 5.0))
        return a * self.alpha, s, dx, dy, p

    def draw(self, fr, t):
        st = self.state(t)
        if not st:
            return
        a, s, dx, dy, p = st
        img = self.img
        if self.anim == "wipe":
            w = max(1, int(img.width * e_inout(p)))
            img = img.crop((0, 0, w, img.height)); a = 1.0 if self.out is None or t <= self.out else a
        place(fr, img, self.x + dx, self.y + dy, self.anchor, a, s)


class Fn:
    """Custom drawing: func(frame, t_local, p) with p = progress over dur; drawn while t0 <= t < t1."""
    def __init__(self, func, t0=0.0, dur=0.4, t1=1e9):
        self.func, self.t0, self.dur, self.t1 = func, t0, dur, t1

    def draw(self, fr, t):
        if self.t0 <= t < self.t1:
            self.func(fr, t, clamp((t - self.t0) / self.dur))


class Fly:
    """Image moving from (x0, y0) to (x1, y1) starting at t (anchor mm)."""
    def __init__(self, img, p0, p1, t, dur=0.6, scale1=1.0, out=None):
        self.img, self.p0, self.p1, self.t, self.dur, self.s1, self.out = img, p0, p1, t, dur, scale1, out

    def draw(self, fr, t):
        if t < self.t or (self.out and t > self.out):
            return
        p = e_inout((t - self.t) / self.dur)
        x = self.p0[0] + (self.p1[0] - self.p0[0]) * p
        y = self.p0[1] + (self.p1[1] - self.p0[1]) * p - 60 * math.sin(math.pi * p)
        place(fr, self.img, x, y, "mm", 1.0, 1 + (self.s1 - 1) * p)


# ----------------------------------------------------------------------------- scene
class Scene:
    def __init__(self, sid, voice=None, lead=0.3, hold=0.7, dur=None, layout="std", level=0, label=None,
                 clip=None, clip_audio=None, music="bed", header=True):
        self.sid, self.voice_id, self.lead = sid, voice, lead
        self.vlen = 0.0
        if voice:
            x, sr = sf.read(f"{ROOT}/audio/vo_prep/{voice}.wav")
            self.vx, self.vsr = x, sr
            self.vlen = len(x) / sr
            self.words = [(w, a + lead, b + lead) for w, a, b in WORDS[voice]]
        self.clip, self.clip_audio = clip, clip_audio
        if clip:
            d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                      clip], capture_output=True, text=True).stdout)
            dur = dur or d
        self.dur = dur or (lead + self.vlen + hold)
        self.layouts = [(0.0, layout)]
        self.level, self.label, self.music, self.header = level, label, music, header
        self.els, self.kc, self.sfx = [], [], []
        self.prev_layout = None
        self.exit = 0.22
        self.panel, self.panel_in, self.panel_out = True, False, False

    # --- cues
    def w(self, phrase, n=1, end=False):
        """Time (scene-local) of the n-th occurrence of phrase in the ASR words of this scene's voice."""
        norm = lambda s: "".join(c for c in s.lower() if c.isalnum())
        ws = [norm(w[0]) for w in self.words]
        ph = [norm(p) for p in phrase.split()]
        k = 0
        for i in range(len(ws)):
            if ws[i:i + len(ph)] == ph:
                k += 1
                if k == n:
                    return self.words[i + len(ph) - 1][2] if end else self.words[i][1]
        raise KeyError(f"{self.sid}: '{phrase}' not in: {' '.join(w[0] for w in self.words)}")

    @property
    def vend(self):
        return self.lead + self.vlen

    def add(self, *els):
        self.els.extend(els); return els[0] if len(els) == 1 else els

    def kay(self, t0, t1, kind, val=None):
        self.kc.append((t0, t1, kind, val))

    def lay(self, t, name):
        self.layouts.append((t, name))

    def fx(self, t, name, gain=1.0):
        self.sfx.append((t, name, gain))

    # --- kayla state
    def layout_at(self, t):
        cur = LAYOUTS[self.prev_layout or self.layouts[0][1]]
        for (tt, name) in self.layouts:
            tgt = LAYOUTS[name]
            if t < tt:
                break
            p = e_inout((t - tt) / 0.5)
            cur = tuple(c + (g - c) * p for c, g in zip(cur, tgt))
        return cur

    def mouth_at(self, t):
        if not self.voice_id:
            return "closed"
        i = int((t - self.lead) * self.vsr)
        n = int(self.vsr / FPS)
        if i < 0 or i >= len(self.vx):
            return "closed"
        seg = self.vx[max(0, i - n // 2): i + n // 2]
        if not hasattr(self, "_ref"):
            hop = int(self.vsr / 100)
            e = np.array([np.sqrt((self.vx[j:j + hop] ** 2).mean()) for j in range(0, len(self.vx) - hop, hop)])
            self._ref = np.percentile(e[e > e.max() * 0.05], 90) if (e > e.max() * 0.05).any() else 1
        r = np.sqrt((seg ** 2).mean()) / self._ref if len(seg) else 0
        return "closed" if r < 0.16 else "half" if r < 0.5 else "open"

    def kayla_state(self, t, tg):
        eyes, mouth, pose, dx, sc = "open", self.mouth_at(t), "base", 0.0, 1.0
        for t0, t1, kind, val in self.kc:
            if t0 <= t < t1:
                if kind == "eyes":
                    eyes = val
                elif kind == "pose":
                    pose = val
                elif kind == "mouth":
                    mouth = val
                elif kind == "shake":
                    p = (t - t0) / (t1 - t0); dx = 14 * math.sin(2 * math.pi * 3 * p) * (1 - p)
                elif kind == "bounce":
                    p = (t - t0) / (t1 - t0); sc = 1 + 0.04 * math.sin(math.pi * p)
        if eyes == "open" and pose == "base" and blinking(tg):
            eyes = "blink"
        if eyes == "surprised" and mouth == "closed":
            mouth = "o"
        return eyes, mouth, pose, dx, sc

    # --- render
    def render(self, t, tg, clipreader=None):
        fr = gl.background().copy()
        if self.header:
            place(fr, gl.header_img(self.level, self.label), 0, 0)
        cx, top, h, right, pa = self.layout_at(t)
        if self.panel_in:
            pa *= clamp(t / 0.4)
        if self.panel_out:
            pa *= clamp((self.dur - t) / 0.35)
        if self.panel and pa > 0.01:
            place(fr, panel_cached(int(round(right - 60))), 60, 130, "lt", pa)
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        for e in self.els:
            e.draw(layer, t)
        if t > self.dur - self.exit:                      # glitch-out of the lesson layer
            q = clamp((t - (self.dur - self.exit)) / self.exit)
            arr = np.array(layer)
            rng = np.random.default_rng(int(tg * 1000))
            for _ in range(6):
                y0 = int(rng.integers(0, H - 40)); hh = int(rng.integers(8, 40))
                arr[y0:y0 + hh] = np.roll(arr[y0:y0 + hh], int(rng.integers(-60, 60) * q), axis=1)
            arr[..., 3] = (arr[..., 3] * (1 - q)).astype(np.uint8)
            layer = Image.fromarray(arr)
        fr.alpha_composite(layer)
        if self.clip is not None and clipreader is not None:
            raw = clipreader.next()
            if raw is not None:
                s = h / SPR_H
                k = Image.fromarray(key_green(raw)).resize((round(1280 * 2 * s), round(720 * 2 * s)), Image.BILINEAR)
                a = clamp(t / 0.3) if self.sid == "L1" else 1.0
                place(fr, k, cx - SPR_W * s / 2 - CLIP_X0 * s, top + 4 * math.sin(2 * math.pi * tg / 3.4) * 0, "lt", a)
        elif h < 1150 or self.layouts[-1][1] != "off":
            eyes, mouth, pose, dx, sc = self.kayla_state(t, tg)
            hh = int(round(h * sc / 2) * 2)
            img = avatar().scaled(eyes, mouth, pose, hh)
            bob = 5 * math.sin(2 * math.pi * tg / 3.4)
            place(fr, img, cx + dx, top + bob - (hh - h), "mt")
        return fr.convert("RGB")
