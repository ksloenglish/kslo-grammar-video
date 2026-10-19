"""Design-led graphics layer: cues per scene + headless-Chromium frame renderer.

A scene is design-led when proto/scenes/<SID>.js exists (e.g. scenes/2.2.js). The page proto/shell.html?s=<SID>
loads lib.js + the scene script. boot(cues) -> {"info": ..., "sfx": [[t, name, gain], ...]}; seek(t) per frame.

CLI:  python3 layer.py cues SID [SID ...]     -> proto/cues/<SID>.json (for reading words/times; tools compute live)
"""
import io, json, os, sys
ROOT = "/home/ubuntu/kslo_grammar"
PROTO = f"{ROOT}/proto"
sys.path.insert(0, f"{ROOT}/render")


# one script can serve several scenes: scenes/_level.js -> 1.0-4.0, scenes/_quiz.js -> Q1-Q4 (read CUES.sid)
TEMPLATE = {"1.0": "_level", "2.0": "_level", "3.0": "_level", "4.0": "_level",
            "Q1": "_quiz", "Q2": "_quiz", "Q3": "_quiz", "Q4": "_quiz"}


def _chromium():
    """System Chromium if present (Manus sandbox: /usr/bin/chromium); else Playwright's own (playwright install chromium)."""
    for p in (os.environ.get("CHROMIUM", ""), "/usr/bin/chromium", "/usr/bin/chromium-browser"):
        if p and os.path.exists(p):
            return p
    return None
def script_of(sid):
    return TEMPLATE.get(sid, sid)


def is_html(sid):
    """Design-led if its script exists. NO_HTML=sid1,sid2 (or 'all') forces the old PIL design (for comparisons)."""
    off = os.environ.get("NO_HTML", "").split(",")
    return os.path.exists(f"{PROTO}/scenes/{script_of(sid)}.js") and sid not in off and "all" not in off


def hold_override(sid):
    """proto/holds/<sid>.txt = seconds after the voice ends (dur = lead + voice + hold). None if absent."""
    p = f"{PROTO}/holds/{sid}.txt"
    return float(open(p).read().strip()) if os.path.exists(p) else None


def cues_for(s, dim=True):
    """Everything a scene page needs, all times scene-local (seconds from the scene start)."""
    from engine import clamp
    import gl
    n = int(round(s.dur * gl.FPS))
    panel, kay = [], []
    for i in range(n):
        t = i / gl.FPS
        cx, top, h, right, pa = s.layout_at(t)
        if s.panel_in:
            pa *= clamp(t / 0.4)
        if s.panel_out:
            pa *= clamp((s.dur - t) / 0.35)
        panel.append([round(right, 2), round(pa, 4)])
        kay.append([round(cx, 1), round(top, 1), round(h, 1)])
    vend = round(s.lead + s.vlen, 3) if s.voice_id else None
    return {"sid": s.sid, "dur": s.dur, "t0": round(getattr(s, "t0", 0.0), 3), "fps": gl.FPS, "lead": s.lead,
            "voice_end": vend, "words": [[w[0], round(w[1], 3), round(w[2], 3)] for w in (s.words or [])],
            "panel": panel, "kayla": kay, "level": s.level, "label": s.label, "dim": dim,
            "kc": [[round(a, 3), round(b, 3), k, v] for a, b, k, v in s.kc]}


class Layer:
    """One Chromium page; open(sid, cues) boots a scene; frame(t) -> PIL RGBA 1920x1080."""
    def __init__(self):
        from playwright.sync_api import sync_playwright
        self._pw = sync_playwright().start()
        self.b = self._pw.chromium.launch(executable_path=_chromium(),
                                          args=["--force-color-profile=srgb", "--font-render-hinting=none"])
        self.pg = None
        self.errs = []

    def open(self, sid, cues):
        if self.pg:
            self.pg.close()
        self.pg = self.b.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=1)
        self.pg.on("pageerror", lambda e: self.errs.append(f"{sid}: {e}"))
        self.pg.on("console", lambda m: self.errs.append(f"{sid}: {m.text}") if m.type in ("error", "warning") else None)
        self.pg.goto(f"file://{PROTO}/shell.html?s={sid}&f={script_of(sid)}")
        ok = self.pg.evaluate("window.loaded")
        if ok is not True:
            raise RuntimeError(f"{sid}: page not ready ({ok}); errors: {self.errs}")
        res = self.pg.evaluate("c => boot(c)", cues)
        if self.errs:
            raise RuntimeError("PAGE ERRORS: " + " | ".join(self.errs[:6]))
        return res

    def frame(self, t):
        from PIL import Image
        self.pg.evaluate(f"seek({t:.6f})")
        png = self.pg.screenshot(omit_background=True)
        if self.errs:
            raise RuntimeError("PAGE ERRORS: " + " | ".join(self.errs[:6]))
        return Image.open(io.BytesIO(png)).convert("RGBA")

    def close(self):
        try:
            self.b.close()
        finally:
            self._pw.stop()


def html_sfx(scenes):
    """Boot every design-led scene once (no frames) and return {sid: [[t, name, gain], ...]}."""
    out = {}
    todo = [s for s in scenes if is_html(s.sid)]
    if not todo:
        return out
    L = Layer()
    try:
        for s in todo:
            out[s.sid] = L.open(s.sid, s.cues)["sfx"]
    finally:
        L.close()
    return out


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "cues":
        import build
        os.makedirs(f"{PROTO}/cues", exist_ok=True)
        for s in build.scenes():
            if s.sid in sys.argv[2:]:
                c = cues_for(s)
                json.dump(c, open(f"{PROTO}/cues/{s.sid}.json", "w"))
                print(s.sid, f"dur {c['dur']:.2f} voice_end {c['voice_end']} words {len(c['words'])}:",
                      " ".join(w[0] for w in c["words"])[:300])
