# -*- coding: utf-8 -*-
"""Build output/Kayla_Grammar_Series_Proposal.md from scripts_data.py plus fixed prose."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from scripts_data import LIBRARY, EPISODES, est

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "output", "Kayla_Grammar_Series_Proposal.md")


def mmss(s):
    s = int(round(s))
    return f"{s//60}:{s%60:02d}"


lib = {k: est(t, h) for k, _, _, t, h in LIBRARY}
wrap = lib["L0"] + lib["L1"] + lib["L3"] + lib["L4"]
ep_body = {n: sum(est(t, h) for _, _, _, t, h in ep["scenes"]) for n, ep in EPISODES.items()}

md = []
A = md.append

A("# Kayla's Grammar Lab: series proposal and scripts for approval")
A("")
A("*K S Lo English · draft v1 · 19 October 2026 · prepared for Mr Kum*")
A("")
A("This document sets out the design concept, recommended length, production approach and every script "
  "that needs your approval before anything is built. Nothing below has been generated as video yet. The "
  "only media made so far are the three Kayla design sheets and three voice samples, so that you can choose.")
A("")

A("## 1. Series concept: how it differs from the vocab series")
A("")
A("The vocab series is a calm, navy-and-gold quiz show hosted by a tutor, Miss K. The grammar series should feel "
  "like dropping into a friendly VTuber's study stream. Kayla is a study buddy rather than a teacher, so she "
  "speaks like a slightly older schoolmate: upbeat, encouraging and occasionally dramatic (\"Plot twist!\").")
A("")
A("| Element | Vocab series (Miss K) | Proposed grammar series (Kayla) |")
A("|---|---|---|")
A("| Feel | Polished quiz show | Upbeat VTuber study stream, the \"Grammar Lab\" |")
A("| Palette | Navy, gold, coral | Midnight violet background with neon cyan, hot pink and sunshine yellow |")
A("| Type | Bebas Neue and Poppins | A rounded, bubbly display font for titles and a clean sans for sentences (confirmed in mockups) |")
A("| Host on screen | Badge with voice rings | Kayla's animated \"facecam\" in the bottom-right corner: she talks, blinks, bobs and reacts throughout the explanation |")
A("| Motion style | Smooth slides, film-leader countdown | Snappy pop-and-bounce stickers, word blocks that snap together, animated timelines and glitch-wipe transitions |")
A("| Branding | Logo at start and end | K S Lo English logo at the **start** (logo sting), in the **body** (small header logo on every screen) and at the **end** (end card). The logo is always drawn as-is, with no glow, plate or box |")
A("")
A("**Fixed colour code for the whole series.** Students will learn to read colours as grammar: "
  "**yellow = simple tenses**, **pink = continuous tenses**, **cyan = time and signal words** (every day, "
  "now, yesterday, when, while), **green tick = correct** and **red cross = wrong**. Every example sentence "
  "highlights its verb in its tense colour. You can reuse the same code in worksheets and slides.")
A("")

A("## 2. Recommended length")
A("")
A("I recommend **3 to 4 minutes per video, never more than 5**. That means one grammar idea per video: about "
  "20 seconds of opening, 2 to 3 minutes of explanation, a 30-second quiz, a 10-second cheat sheet and a "
  "15-second outro. Each new idea on screen lasts no more than 10 to 20 seconds.")
A("")
A("The three textbook pages for Unit 8 contain four separate ideas, which would make one video of roughly "
  "10 minutes. I therefore suggest **four short episodes**. The timings below are estimates from the scripts "
  "in Section 6 and will be confirmed against the recorded voice.")
A("")
A("| Episode | Topic | Textbook source | Body | Total with intro and outro |")
A("|---|---|---|---|---|")
for n, ep in EPISODES.items():
    A(f"| Ep {n} | {ep['title']} | {ep['source']} | about {mmss(ep_body[n])} | **about {mmss(ep_body[n] + wrap)}** |")
A("")
A("If you would rather have a single Unit 8 video, the same four parts can be joined with one intro and one "
  "outro, giving about 9 minutes. I would not recommend that for S2 attention spans.")
A("")

A("## 3. Production approach and cost")
A("")
A("Your concept is correct: **motion graphics should carry almost everything**. They are rendered from code "
  "here, so they cost almost nothing per video, every word is spelt exactly as written, and a correction means "
  "re-rendering one scene rather than regenerating footage. I would refine the plan in one important way.")
A("")
A("**Kayla in the body should be an animated still-image avatar, not generated video.** Many real VTubers "
  "stream with a simple avatar whose mouth moves with their voice. I would create a set of about 8 still "
  "images of Kayla once (mouth closed, half-open and open; eyes blinking; happy wink; surprised; thinking). "
  "The renderer then animates them in time with her recorded voice, adds blinking and a gentle bob, and "
  "switches expressions on cue: a wink for correct answers, surprise for \"Plot twist!\" and thinking during "
  "quiz countdowns. She is therefore present and talking for the whole video at no extra cost per episode. "
  "Lip-synced video for 3 minutes of narration would be the most expensive item in the project, and it is "
  "unnecessary.")
A("")
A("| Item | Made | Method | Cost profile |")
A("|---|---|---|---|")
A("| Kayla master design, keyframe on green screen and about 8 avatar stills | Once | Image generation and editing from your chosen design | Small, one-off |")
A("| Intro, transition and outro clips (Section 5) | Once, reused in every video | Video generation with lip-sync, two variants each, keeping the better one (as for Miss K) | The main one-off cost, about 30 seconds of footage in total |")
A("| Logo sting, end card, layouts, timelines, word blocks, quizzes and cheat sheets | Reusable templates; content changes per video | Code-rendered motion graphics | Almost free |")
A("| Kayla's narration | Per video | Text-to-speech in the chosen voice, checked line by line | Small |")
A("| Pictures | Per video, only where they genuinely help | Mostly icons drawn in code; at most a few generated sticker illustrations (for example, the shark scene) | Small or none |")
A("| Music | Once | A new signature background track so the series does not sound like the vocab videos; existing sound effects reused | Small, one-off |")
A("")
A("After the one-off library is made, **a normal episode needs no video generation at all**, exactly like the "
  "vocab series format v2.")
A("")
A("**Other improvements I suggest:**")
A("")
A("1. **A hook question that is answered at the end** of each episode (for example, \"What's the difference "
  "between *I play football* and *I'm playing football*?\"). It gives students a reason to keep watching.")
A("2. **Three-question quick quiz** with a 3-2-1 countdown and \"Say your answers out loud!\", which links "
  "the series to the familiar vocab-video routine.")
A("3. **\"Pause and screenshot\" cheat sheet**: one screen that condenses the textbook section into a "
  "revision card.")
A("4. **YouTube captions file (SRT)** for every video. This supports weaker readers and listeners without "
  "cluttering the screen.")
A("5. **YouTube title, description and chapters** with every video, in the same style as the vocab series, "
  "never mentioning AI.")
A("6. *(Later, optional)* a 30 to 45-second vertical Short cut from each cheat sheet and quiz, for "
  "Instagram or YouTube Shorts.")
A("")

A("## 4. Kayla: three designs and three voices")
A("")
A("**Designs** (main pose plus three expressions: wink, surprised and thinking). All three are original "
  "characters with modest, school-appropriate clothing, and none of them looks like Miss K.")
A("")
A("| Option | Look | Mood |")
A("|---|---|---|")
A("| **A · Neon Pop** | Lavender twin-tails fading to cyan, gold star clips, cat-ear headphones with glowing cyan rings, oversized lilac hoodie with a pencil zip charm | The most classic VTuber look: cute, playful, energetic |")
A("| **B · Cyber Scholar** | Silver bob with electric-blue streaks, quotation-mark hair clips, headset microphone, white-and-purple techwear jacket with a speech-bubble pin | Cool, smart and futuristic, with grammar details built in |")
A("| **C · Cosy Bookworm Gamer** | Strawberry-pink side ponytail, round gold glasses, bear-ear headband, cream cardigan and sailor collar, pencil in her hair | Warm, friendly and studious |")
A("")
A("Any design can be adjusted, for example with different colours, shorter hair or a K S Lo-coloured accessory.")
A("")
A("**Voices** (all three read the same sample line). Miss K's voice, Leda, has been left out deliberately so "
  "that the two characters sound different.")
A("")
A("| Option | Voice | Character |")
A("|---|---|---|")
A("| **Voice 1** | Zephyr | Bright and clear; the most \"presenter-like\" |")
A("| **Voice 2** | Laomedeia | Upbeat and bouncy; the most \"hyper streamer\" |")
A("| **Voice 3** | Achernar | Soft, sweet and the highest-pitched; the most \"anime girl\" |")
A("")
A("All three are studio voices with a General American base, as Leda is. The British setting is applied, but "
  "it cannot guarantee a fully British accent, and I will check particular words as we did for Miss K. "
  "\"K S Lo\" is written phonetically as \"K. S. Low\" for the voice, and it will be checked in every recorded "
  "line. Real VTubers often sound slightly higher than these samples. If you wish, I can add a gentle pitch "
  "lift of 1 to 2 semitones to the chosen voice; Miss K, by contrast, was kept natural.")
A("")

A("## 5. Reusable library scripts: logo opening, intro, transition, outro and end card")
A("")
A("These clips are generic and never mention a unit, topic or number, so they fit every video. The unit and "
  "topic appear only as on-screen text. Gestures happen **only** on the words shown, and Kayla's hands are "
  "clasped at all other times. That is the rule which fixed Miss K's early-wave problem.")
A("")
A("| # | Clip | What you see | Kayla says | Approx. length |")
A("|---|---|---|---|---|")
for k, label, screen, says, hold in LIBRARY:
    shown = says.replace("K S Lo", "K S Lo")
    A(f"| {k} | {label.split(' (')[0]} | {screen} | {shown} | {lib[k]:.0f} s |")
A("")
A("Kayla's name tag in the opening reads **\"Kayla · Your Grammar Study Buddy\"**. Every episode follows "
  "this order: **L0 logo opening → L1 intro → body (with L2 between the two big sections where relevant) → "
  "quiz and cheat sheet → L3 outro → L4 end card.**")
A("")

A("## 6. Body scripts for approval")
A("")
A("I have kept the textbook's terms (*simple present*, *present continuous*, *simple past*, *past "
  "continuous*), its explanations and most of its example sentences, simplified for S2 and with some added "
  "material. My changes to the textbook are marked in Section 7 for you to accept or reject. During the "
  "body, Kayla speaks from her avatar corner. Her lines are shown exactly as she will say them; on-screen "
  "sentences use the textbook spelling and punctuation.")
A("")
for n, ep in EPISODES.items():
    A(f"### Episode {n}: {ep['title']}")
    A("")
    A(f"*Source: textbook {ep['source']}. Estimated body length: about {mmss(ep_body[n])}; total video: "
      f"about {mmss(ep_body[n] + wrap)}.*")
    A("")
    A("| Scene | Purpose | On screen (motion graphics) | Kayla says | Approx. |")
    A("|---|---|---|---|---|")
    t = 0.0
    for sid, label, screen, says, hold in ep["scenes"]:
        d = est(says, hold)
        A(f"| {sid} | {label} | {screen} | {says} | {d:.0f} s |")
        t += d
    A("")
    A("Quiz scenes: the question appears, the 3-2-1 countdown runs with Kayla's \"thinking\" face, then the "
      "answer pops in and Kayla says the line shown.")
    A("")

A("## 7. Changes from the textbook, for your decision")
A("")
A("| Where | Textbook | Draft | Reason |")
A("|---|---|---|---|")
A("| Ep 2, scene 2.03 | *I was born in 2011.* | *I was born in 2013.* | Current S2 students were born around 2013, so the example matches their own lives. |")
A("| Ep 2, scene 2.03 | *My grandpa passed away two years ago.* | *My family moved to Tsing Yi two years ago.* | A cheerful avatar reading a bereavement example can sound insensitive; this example also continues Ep 1's \"I live in Tsing Yi\". |")
A("| Ep 1, scenes 1.02 and 1.08; Ep 2, scenes 2.02 and 2.05 | Uses only | Short form reminders (+s/-es, am/is/are + -ing, -ed and irregular verbs, was/were + -ing) | Students need the form before the uses; each reminder takes about 10 seconds. |")
A("| Ep 1, scene 1.12 | *House husbands …* | Same sentence plus a one-line gloss | S2 students may not know \"house husband\". |")
A("| Ep 2, scene 2.09 | Not in the book | Tip: *when* + short action, *while* + long action | A common and memorable pattern, worded as \"often\" because *when* can also introduce a long action. |")
A("| Ep 3, scene 3.03 | have, know, like, see, smell, think, want | The same verbs grouped by meaning, plus small extra chips (love, need, understand, hear) | Grouping by meaning makes a list memorable; the extras are common state verbs. |")
A("| Ep 4, scene 4.04 | The Snow White synopsis speech bubble | Optional scene | Can be cut to save about 15 seconds. |")
A("| All quizzes | Not in the book | Three questions per episode, written by me | For retrieval practice. Please check that the level suits S2. |")
A("")

A("## 8. What happens after approval")
A("")
A("1. **Kayla is finalised** from your chosen design: a master image, a green-screen keyframe and the avatar stills. You see them before anything else is built.")
A("2. **Library lines are recorded** in the chosen voice and checked for \"K S Lo\", pronunciation and falling endings. The three library clips are then generated, two variants each, and checked for lip-sync and gestures that match the words.")
A("3. **Mockup stills** of the new layout are shown to you for approval: the opening lockup, a teaching screen with Kayla's facecam, a timeline, a quiz screen, the cheat sheet and the end card.")
A("4. **Episode 1 is built in full**: narration, rendering, a speech check against the script and a visual check of every scene. It is delivered with its YouTube text and captions file. Episodes 2 to 4 then follow the same pipeline at much lower cost.")
A("5. A **reusable skill for the grammar series** is written as a complete record and failsafe, in the same way as the vocab-video skill.")
A("")

os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "w", encoding="utf-8").write("\n".join(md) + "\n")
print("wrote", OUT, sum(len(x) for x in md), "chars")
for n in EPISODES:
    print(n, mmss(ep_body[n]), mmss(ep_body[n] + wrap))
