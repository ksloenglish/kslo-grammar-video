# -*- coding: utf-8 -*-
"""Build output/Kayla_Body_Script_v1.md from scripts/single_script.py (single source of truth)."""
import sys
sys.path.insert(0, "/home/ubuntu/kslo_grammar/scripts")
import single_script as SS

est, mmss = SS.est, SS.mmss
W = {w[0]: w for w in SS.WRAP}

GROUPS = [
    ("Hook and the Tense Map", lambda i: i in ("H", "M")),
    ("Level 1: The present", lambda i: i.startswith("1.")),
    ("Level 2: The past", lambda i: i.startswith("2.")),
    ("Halfway: transition clip", lambda i: i == "T"),
    ("Level 3: Non-action verbs", lambda i: i.startswith("3.")),
    ("Level 4: Tenses in stories", lambda i: i.startswith("4.")),
    ("Boss quiz and cheat sheet", lambda i: i.startswith("Q") or i == "C"),
]


def cell(t):
    return t.replace("|", "/").replace("\n", " ")


def main():
    t = 0.0
    start = {}
    for k in ("L0", "L1"):
        start[k] = t; t += est(W[k][2], W[k][3])
    for s in SS.S:
        start[s[0]] = t; t += est(s[3], s[5])
    start["L3"] = t; t += est(W["L3"][2], W["L3"][3])
    start["L4"] = t; t += est(W["L4"][2], W["L4"][3])
    total = t
    body = sum(est(s[3], s[5]) for s in SS.S)

    out = []
    A = out.append
    A("# Kayla's Grammar Lab: *The present and the past*")
    A("")
    A("## Body script v1, for approval")
    A("")
    A(f"*K S Lo English · Style A (Neon Stream) · Kayla's voice: Voice 2 (Laomedeia), natural pitch. "
      f"Estimated length **{mmss(total)}**, of which the body is {mmss(body)}. Timings are estimates at Kayla's measured "
      f"speaking rate (2.4 words per second) plus animation holds; final timings come from the recorded voice.*")
    A("")
    A("Colour code throughout: **yellow** = simple tenses, **pink** = continuous tenses, **cyan** = time and signal "
      "words. Every example sentence Kayla reads appears on screen with the same wording, and every quiz blank is one "
      "solid line.")
    A("")
    A("## At a glance")
    A("")
    A("| Starts | Part | Length |")
    A("|---|---|---|")
    A(f"| {mmss(start['L0'])} | Logo opening (reusable) | {est(W['L0'][2], W['L0'][3]):.0f} s |")
    A(f"| {mmss(start['L1'])} | Intro clip (reusable, approved) | {est(W['L1'][2], W['L1'][3]):.0f} s |")
    for g, f in GROUPS:
        ids = [s for s in SS.S if f(s[0])]
        dur = sum(est(s[3], s[5]) for s in ids)
        A(f"| {mmss(start[ids[0][0]])} | {g} | {dur:.0f} s |")
    A(f"| {mmss(start['L3'])} | Outro clip (reusable, approved) | {est(W['L3'][2], W['L3'][3]):.0f} s |")
    A(f"| {mmss(start['L4'])} | End card (reusable) | {est(W['L4'][2], W['L4'][3]):.0f} s |")
    A(f"| **{mmss(total)}** | **Total** | |")
    A("")
    A("## The script")
    A("")
    A("Kayla's position and expression are given in the last column: **standard** means the waist-up cut-out at the "
      "bottom right, **small** means she shrinks into the corner to free up width, and **large** means she slides "
      "in big for a pop-up moment.")
    A("")
    for g, f in GROUPS:
        A(f"### {g}")
        A("")
        A("| Clock | Scene | On screen | Kayla says | Kayla |")
        A("|---|---|---|---|---|")
        for s in SS.S:
            if f(s[0]):
                A(f"| {mmss(start[s[0]])} | **{s[0]}** {cell(s[1])} | {cell(s[2])} | {cell(s[3])} | {cell(s[4])} |")
        A("")
    A("## Quiz answer key")
    A("")
    A("| # | Question (on screen) | Answer | Why (tag on screen) |")
    A("|---|---|---|---|")
    A("| 1 | Look! The baby ________ (sleep). | is sleeping | Look! = right now (present continuous) |")
    A("| 2 | I ________ (do) my homework when the lights went out. | was doing | long action, interrupted (past continuous) |")
    A("| 3 | Right now, I ________ (want) a new phone. | want | non-action verb; *am wanting* is struck through |")
    A("| 4 | In the film, the hero ________ (fly) to the moon and saves the planet. | flies | synopsis = present; spelling chip *fly → flies* |")
    A("")
    A("I added context to questions 3 and 4 so that only one answer fits. Without *Right now*, *wanted* would also "
      "be correct. Without *and saves the planet*, *flew* would also be acceptable in a past-tense retelling.")
    A("")
    A("## Changes from the textbook pages")
    A("")
    A("| Change | Reason |")
    A("|---|---|")
    A("| *I was born in 2011* → *I was born in 2013* | Matches current students' birth years (as in the approved plan) |")
    A("| Left out: *We often walk our dog in the morning.*, *My grandpa passed away two years ago.*, *The cake smelt great.* | "
      "Time; one example per idea. The bereavement example also sits awkwardly with a cheerful host |")
    A("| Fairy-tale passage cut after *…who had a kind heart* | Time; *was* and *had* are enough to show past tenses in a story |")
    A("| Shark passage cut after *…they spot a shark* | Time; keeps one continuous and one simple present verb |")
    A("| *Harry the superhero saves the lives of hundreds of thousands of people using magic* → *Harry the superhero saves thousands of lives* | "
      "Shorter to read and say; the tense point is unchanged |")
    A("| Added: form reminders (+s, +ed, am/is/are + -ing, was/were + -ing) | The pages assume the forms; a 3-second reminder helps weaker students |")
    A("| Added: gloss *house husband = a man who stays at home to look after the home and family* | Likely unfamiliar to students |")
    A("| Added: *when + short action · while + long action* tip chips | A memorable rule drawn from the textbook's two examples |")
    A("| Added: verb groups in the No -ing Zone (feelings, thinking, senses, owning) | Easier to remember than a flat list |")
    A("| Snow White speech bubbles used as the hook and answered in Level 4 | Gives students a reason to watch to the end |")
    A("")
    A("## Pronunciation notes for recording")
    A("")
    A("| Text | Kayla should say |")
    A("|---|---|")
    A("| *read* (past, in the hook and in 4.4) | /red/; the recording text uses the respelling “red” |")
    A("| *-ing* (No -ing Zone, plus -ing) | “ing”, as one syllable |")
    A("| *0°C* | “zero degrees Celsius” |")
    A("| *7 a.m.* | “seven a.m.” |")
    A("| *2013* / *2008* | “twenty thirteen” / “two thousand and eight” |")
    A("| *Tsing Yi* | “Ching Yee”, as Hong Kong speakers say it (checked by ear after recording) |")
    A("")
    A("## Reusable parts: small updates to match your decisions")
    A("")
    A("The approved lines for the intro, transition and outro are unchanged. Only their on-screen details need small "
      "updates. The **logo opening** lockup shows only *Kayla's Grammar Lab* and *The present and the past*; the "
      "earlier \"S2 · UNIT 8 · EP 1\" pill is gone. The **outro** \"WELL DONE!\" card lists only the unit's grammar "
      "points, not the teaching devices: *Simple present · Present continuous · Simple past · Past continuous · "
      "Non-action verbs · Tenses in stories*. The **transition clip** is used once, at "
      "the halfway point, and the \"LEVEL UNLOCKED\" motion-graphics stings mark the other level changes.")
    A("")
    open(f"{SS.ROOT}/output/Kayla_Body_Script_v1.md", "w").write("\n".join(out))
    print("written", mmss(total))


if __name__ == "__main__":
    main()
