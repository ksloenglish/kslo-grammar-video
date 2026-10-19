"""Left-edge alignment audit: for every scene, find left-anchored elements (text, paragraphs, pills, cards) whose
VISIBLE ink starts within 1-14 px of another element nearby (likely meant to line up but don't).
usage: python3 align_audit.py [sid ...]   -> prints suspects per scene"""
import sys
import numpy as np
sys.path.insert(0, "/home/ubuntu/kslo_grammar/render")
import build
from engine import E
import scenes as S

def ink_left(img):
    a = np.asarray(img)[..., 3]
    cols = np.nonzero((a > 100).any(0))[0]
    rows = np.nonzero((a > 100).any(1))[0]
    if not len(cols):
        return None
    return cols.min(), rows.min(), rows.max()

def items(sc):
    out = []
    for el in sc.els:
        if isinstance(el, E) and el.img is not None and el.anchor[0] == "l" and isinstance(el.x, (int, float)):
            gp = el.img.info.get("gpad", 0)
            ay = {"t": 0, "m": 0.5, "b": 1}[el.anchor[1]]
            r = ink_left(el.img)
            if r is None:
                continue
            x0 = round(el.x - gp); y0 = round(el.y - ay * (el.img.height - 2 * gp) - gp)
            kind = "text" if "gpad" in el.img.info else "shape"
            out.append((x0 + r[0], y0 + r[1], y0 + r[2], kind, el.img.size))
        elif isinstance(el, S.ParaStates):
            r = ink_left(el.base)
            if r is not None:
                out.append((round(el.x + r[0]), round(el.y + r[1]), round(el.y + r[2]), "para", el.base.size))
    return out

def audit(sids=None):
    for sc in build.scenes():
        if sids and sc.sid not in sids:
            continue
        it = items(sc)
        sus = []
        for i in range(len(it)):
            for j in range(i + 1, len(it)):
                a, b = it[i], it[j]
                dx = abs(a[0] - b[0])
                gap = max(a[1], b[1]) - min(a[2], b[2])          # vertical distance between the two ink boxes
                if 1 <= dx <= 14 and gap < 260 and "shape" not in (a[3], b[3]):
                    sus.append((dx, a, b))
                elif 1 <= dx <= 6 and gap < 260:                 # text vs shape: only tiny near-misses
                    sus.append((dx, a, b))
        if sus:
            print(f"== {sc.sid}")
            for dx, a, b in sorted(sus, key=lambda q: (q[1][1], q[0]))[:14]:
                print(f"   dx {dx:2d}: {a[3]:5s} x{a[0]} y{a[1]}-{a[2]}  vs  {b[3]:5s} x{b[0]} y{b[1]}-{b[2]}")

if __name__ == "__main__":
    audit(set(sys.argv[1:]) or None)
