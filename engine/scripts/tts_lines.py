# -*- coding: utf-8 -*-
"""TTS text for every spoken line (respellings for the recording only; screens and captions use the approved text)."""
import json, sys
sys.path.insert(0, "/home/ubuntu/kslo_grammar/scripts")
import single_script as SS

BASE = "high pitch, bubbly, playful and energetic"          # approved Voice 2 sample style
TEACH = BASE + "; clear and unhurried"

RESPELL = [("K S Lo", "K S Low"), ("Tsing Yi", "Ching Yee"), ("in 2013", "in twenty thirteen"),
           ("in 2008", "in two thousand and eight"), ("plus -ing", "plus ing"), ("with -ing", "with ing"),
           ("take -ing", "take ing"), ("so no -ing", "so no ing"), ("add -ed", "add ed"),
           ("Look! Is, read, was,", "Look! Is, red, was,"), ("gives, saves and live:", "gives, saves and liv:"), ("Read and was: finished", "Red and was: finished")]


def tts(text):
    for a, b in RESPELL:
        text = text.replace(a, b)
    return text


def lines():
    out = []
    W = {w[0]: w for w in SS.WRAP}
    out.append(dict(id="L1_intro", text=tts(W["L1"][2]), approved=W["L1"][2], style=BASE))
    out.append(dict(id="L2_transition", text=tts("Nice one! Now, let's move on to the next part!"),
                    approved="Nice one! Now, let's move on to the next part!", style=BASE))
    out.append(dict(id="L3_outro", text=tts(W["L3"][2]), approved=W["L3"][2], style=BASE))
    for s in SS.S:
        if s[0] == "T":
            continue
        sid = s[0].replace(".", "_")
        teach = not (s[0].endswith(".0") or s[0].startswith("Q"))
        out.append(dict(id=f"S{sid}", text=tts(s[3]), approved=s[3], style=TEACH if teach else BASE))
    return out


if __name__ == "__main__":
    L = lines()
    json.dump(L, open("/home/ubuntu/kslo_grammar/audio/tts_lines.json", "w"), indent=1, ensure_ascii=False)
    for l in L:
        flag = "" if l["text"] == l["approved"] else "  [respelt]"
        print(f'{l["id"]:16s} {l["style"][-22:]:>22s} | {l["text"]}{flag}')
    print(len(L), "lines")
