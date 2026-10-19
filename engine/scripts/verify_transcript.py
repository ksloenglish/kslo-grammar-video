"""Verify the final-audio transcription and the bilingual captions against the approved script.
1  Transcript vs script, per scene: word-sequence similarity of the ASR text inside each scene window against the
   scene's approved English caption text; lists missing / extra words (flags < 0.85).
2  Pause windows: no ASR words inside inserted pauses (e.g. after 'yesterday' in 2.2).
3  SRT integrity: EN and ZH cue counts equal the script, identical timings, monotonic, no overlaps, every cue inside
   its own scene window, EN cue text == script text.
4  Cue timing: ASR words heard inside each EN cue window match that cue's text (flags < 0.6).
Two INDEPENDENT transcriptions: A = manus-speech-to-text (segments; used for the clip captions), B = faster-whisper
small.en with true word timestamps (build/qa/final_audio_fw_words.json, made on first run). Check 1 uses A with a
timing-free global alignment; checks 2 and 4 use B's word times; check 5 compares A with B.
usage: python3 verify_transcript.py"""
import json, glob, re, difflib, sys
sys.path.insert(0, "/home/ubuntu/kslo_grammar/scripts")
from captions import CAP
ROOT = "/home/ubuntu/kslo_grammar"
NUM = {"0": "zero", "1": "one", "2": "two", "3": "three", "4": "four", "5": "five", "6": "six", "7": "seven",
       "8": "eight", "9": "nine", "10": "ten"}
def norm(s):
    s = s.lower().replace("’", "'").replace("‘", "'").replace("k s lo", "kslo").replace("k.s. lo", "kslo")
    s = s.replace("ks lo", "kslo").replace("a.m.", "am").replace("-", " ")
    w = re.findall(r"[a-z0-9']+", s)
    return [NUM.get(x, x) for x in w]
def sim(a, b):
    return difflib.SequenceMatcher(None, a, b, autojunk=False).ratio()
def diff(a, b):
    out = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if op != "equal":
            out.append(f"{op}: script[{' '.join(a[i1:i2])}] heard[{' '.join(b[j1:j2])}]")
    return out
def srt(p):
    cues = []
    for blk in open(p, encoding="utf-8").read().strip().split("\n\n"):
        L = blk.split("\n")
        a, b = [sum(float(x) * m for x, m in zip(t.replace(",", ".").split(":"), (3600, 60, 1))) for t in L[1].split(" --> ")]
        cues.append((a, b, " ".join(L[2:])))
    return cues
def fw_words():
    import os
    out = f"{ROOT}/build/qa/final_audio_fw_words.json"
    if not os.path.exists(out) or os.path.getmtime(out) < os.path.getmtime(f"{ROOT}/build/qa/final_audio.wav"):
        import soundfile as sf, numpy as np
        from scipy.signal import resample_poly
        from faster_whisper import WhisperModel
        x, sr = sf.read(f"{ROOT}/build/qa/final_audio.wav"); x = x.mean(1) if x.ndim > 1 else x
        x = resample_poly(x, 16000, sr).astype("float32")
        m = WhisperModel("small.en", device="cpu", compute_type="int8")
        segs, _ = m.transcribe(x, word_timestamps=True, beam_size=5, language="en")
        json.dump([(w.word.strip(), round(w.start, 3), round(w.end, 3)) for sg in segs for w in sg.words],
                  open(out, "w"))
    return [tuple(w) for w in json.load(open(out))]
def main():
    tl = json.load(open(f"{ROOT}/build/timeline.json"))
    f = sorted(glob.glob(f"{ROOT}/build/qa/final_audio_transcription_*.json"))[-1]
    segs = json.load(open(f))["segments"]
    words = []                                   # ASR words with times interpolated inside each segment
    for sg in segs:
        ws = sg["text"].split(); n = sum(len(w) + 1 for w in ws) or 1; c = 0
        for w in ws:
            words.append((w, sg["start"] + (sg["end"] - sg["start"]) * c / n,
                          sg["start"] + (sg["end"] - sg["start"]) * (c + len(w)) / n)); c += len(w) + 1
    print(f"transcript: {f.split('/')[-1]}  {len(segs)} segments, {len(words)} words, last end {segs[-1]['end']:.1f} s")
    bad = 0
    print("\n1) transcript A vs approved script, per scene (global alignment, timing-free)")
    sw, tag = [], []
    for d in tl:
        for en, _ in CAP.get(d["sid"], []):
            for w in norm(en):
                sw.append(w); tag.append(d["sid"])
    hw = norm(" ".join(sg["text"] for sg in segs))
    sm = difflib.SequenceMatcher(None, sw, hw, autojunk=False)
    hit = [False] * len(sw); extra = {}
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            for i in range(i1, i2): hit[i] = True
        elif j2 > j1:
            extra.setdefault(tag[min(i1, len(sw) - 1)], []).append(" ".join(hw[j1:j2]) + (f" (for: {' '.join(sw[i1:i2])})" if i2 > i1 else ""))
    print(f"   whole video: {sum(hit)}/{len(sw)} script words heard ({sum(hit) / len(sw):.1%})")
    order = []
    for t in tag:
        if t not in order: order.append(t)
    for sid in order:
        idx = [i for i, t in enumerate(tag) if t == sid]
        r = sum(hit[i] for i in idx) / len(idx)
        flag = "  <-- CHECK" if r < 0.85 else ""
        bad += r < 0.85
        miss = [sw[i] for i in idx if not hit[i]]
        print(f"   {sid:4s} {r:5.0%} of {len(idx):2d} words{flag}" + (f"   not heard: {' '.join(miss)}" if miss else "")
              + (f"   | heard instead/extra: {'; '.join(extra[sid])}" if sid in extra else ""))
    B = fw_words()
    print(f"\n   transcript B (faster-whisper, word timestamps): {len(B)} words")
    print("\n2) inserted pause windows (no speech expected; transcript B)")
    W = json.load(open(f"{ROOT}/audio/vo_prep/words.json"))
    d22 = [d for d in tl if d["sid"] == "2.2"][0]; base = d22["t0"] + d22["lead"]
    vw = W[d22["voice"]]
    for i in range(len(vw) - 1):
        gap = vw[i + 1][1] - vw[i][2]
        if gap > 0.5:
            a, b = base + vw[i][2] + 0.15, base + vw[i + 1][1] - 0.15
            inside = [w for w, x, y in B if a < (x + y) / 2 < b]
            print(f"   after '{vw[i][0]}' {a:7.2f}-{b:7.2f} s: {'clean' if not inside else 'WORDS: ' + ' '.join(inside)}")
            bad += bool(inside)
    print("\n3) SRT integrity")
    en = srt(f"{ROOT}/output/Kayla_Grammar_Lab_The_present_and_the_past.en.srt")
    zh = srt(f"{ROOT}/output/Kayla_Grammar_Lab_The_present_and_the_past.zh-HK.srt")
    n_exp = sum(len(v) for v in CAP.values())
    ok_count = len(en) == len(zh) == n_exp
    ok_time = all(abs(a[0] - b[0]) < 1e-3 and abs(a[1] - b[1]) < 1e-3 for a, b in zip(en, zh))
    ok_order = all(en[i][1] <= en[i + 1][0] and en[i][0] < en[i][1] for i in range(len(en) - 1))
    exp_texts = [t for d in tl if d["sid"] in CAP for t, _ in CAP[d["sid"]]]
    ok_text = [re.sub(r"\s+", " ", c[2]) for c in en] == [re.sub(r"\s+", " ", t) for t in exp_texts]
    win = {}
    for d in tl:
        for t, _ in CAP.get(d["sid"], []):
            win.setdefault(t, []).append((d["t0"] - 0.1, d["t0"] + d["dur"] + 0.1))
    ok_win = all(any(a <= c[0] and c[1] <= b for a, b in win.get(e, [])) for c, e in zip(en, exp_texts))
    for k, v in (("cue count EN = ZH = script (%d)" % n_exp, ok_count), ("EN/ZH timings identical", ok_time),
                 ("monotonic, no overlaps", ok_order), ("EN text == approved script", ok_text),
                 ("every cue inside its scene", ok_win)):
        print(f"   {'PASS' if v else 'FAIL'}  {k}")
        bad += not v
    print("\n4) cue timing vs words heard in each cue window (transcript B; flag < 0.60)")
    low = []
    for a, b, t in en:
        got = norm(" ".join(w for w, x, y in B if a - 0.15 <= (x + y) / 2 <= b + 0.15))
        r = sim(norm(t), got)
        if r < 0.6:
            low.append((a, r, t[:50], " ".join(got)[:50]))
    print(f"   {len(en) - len(low)}/{len(en)} cues match the words heard in their window")
    for a, r, t, g in low:
        print(f"   {a:7.2f} {r:.2f}  cue[{t}]  heard[{g}]")
    bad += len(low)
    print("\n5) agreement of the two independent transcriptions")
    ra = sim(norm(" ".join(sg["text"] for sg in segs)), norm(" ".join(w for w, _, _ in B)))
    rb = sim(sw, norm(" ".join(w for w, _, _ in B)))
    print(f"   A vs B {ra:.1%}   |   B vs script {rb:.1%}" + ("" if ra >= 0.9 and rb >= 0.9 else "  <-- CHECK"))
    bad += ra < 0.9 or rb < 0.9
    print(f"\nRESULT: {'ALL CHECKS PASSED' if not bad else str(bad) + ' item(s) to review'}")
if __name__ == "__main__":
    main()
