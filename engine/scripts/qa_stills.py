"""Render full-resolution stills: python3 qa_stills.py OUTDIR SID:t[,t...] ...  -> OUTDIR/<SID>_<t>.png"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "render"))
import build
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
for spec in sys.argv[2:]:
    sid, ts = spec.split(":")
    for t in ts.split(","):
        p = f"{out}/{sid}_{float(t):05.2f}.png"
        build.render_still(sid, float(t)).convert("RGB").save(p); print(p)
