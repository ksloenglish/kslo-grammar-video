# -*- coding: utf-8 -*-
"""Kayla's Grammar Lab - The present and the past: word-for-word body script v1 (for approval).

Scene tuple: (id, part, on_screen, kayla_says, kayla_cue, extra_hold_s)
kayla_cue: size (standard / small / large) and expression, used later by the renderer.
Estimated duration = words / WPS + extra hold. WPS measured from the chosen voice (Laomedeia sample: 2.41 w/s).
"""
import os

WPS = 2.4
ROOT = "/home/ubuntu/kslo_grammar"

WRAP = [  # approved library parts (fixed)
    ("L0", "Logo opening", "(music sting)", 4.0),
    ("L1", "Intro", "Hello, hello, K S Lo students! It's me, Kayla, your grammar study buddy! Grammar can be tricky, "
     "but don't worry. We'll break it down together, step by step. Watch carefully, because there's a quick quiz "
     "at the end. Ready? Let's level up!", 0.8),
    ("L3", "Outro", "Great work today, K S Lo students! Keep practising, and try using this grammar in your own "
     "writing and speaking. See you next time! Bye-bye!", 0.8),
    ("L4", "End card", "(music only)", 6.0),
]

S = []  # body scenes
A = S.append

# ------------------------------------------------------------------ HOOK + TENSE MAP
A(("H", "Hook",
   "The two Snow White speech bubbles from page 52 pop in: “‘Snow White and the Seven Dwarfs’ is one of my favourite "
   "stories. I first read it when I was only three.” and “The story reaches its climax when the evil queen gives Snow "
   "White a poisoned apple. Luckily the prince’s kiss saves her and they live happily ever after.” As Kayla names "
   "them, the verbs light up with small PRESENT or PAST tags. A big “?” bounces in.",
   "Look! Is, read, was, reaches, gives... Present, past, then present again! Is that allowed? Let's find out!",
   "large · curious", 1.5))
A(("M", "The Tense Map",
   "The 2 x 2 Tense Map builds tile by tile. Rows: PRESENT and PAST. Columns: SIMPLE (yellow, three dots) and "
   "CONTINUOUS (pink, a bar). Tiles: simple present · I play | present continuous · I am playing | simple past · "
   "I played | past continuous · I was playing.",
   "Here's our Tense Map. Yellow is simple: facts, habits and finished actions. Pink is continuous: actions in "
   "progress. Let's unlock them!",
   "small · smile", 1.5))

# ------------------------------------------------------------------ LEVEL 1
A(("1.0", "Level 1 title", "Sting: “LEVEL 1 · THE PRESENT” with an XP chime; the header progress bar fills its first dot.",
   "Level one: the present!", "large · cheer", 0.8))
A(("1.1", "Simple present: form",
   "The ‘simple present’ tile zooms into the panel. Word blocks snap together: [I / you / we / they] + [play] · "
   "[he / she / it] + [play] and a yellow “+s” sticker flies on → plays.",
   "The simple present uses the basic verb. With he, she or it, add an s. She plays!",
   "standard · talk", 1.0))
A(("1.2", "Simple present: three uses",
   "Three use cards stack up, each with an icon: ① FACTS & GENERAL TRUTHS – “Water freezes at 0°C.” (thermometer) · "
   "② TRUE NOW – “I live in Tsing Yi.” (map pin) · ③ HABITS – “Richard wakes up at 7 a.m. every day.” (alarm clock). "
   "Signal-word chips float up under card 3: every day · often · usually · always.",
   "Use it for facts. Water freezes at zero degrees Celsius. Things that are true now. I live in Tsing Yi. "
   "And habits. Richard wakes up at seven a.m. every day.",
   "standard · talk", 1.5))
A(("1.3", "Present continuous: form and “Give me five!”",
   "The ‘present continuous’ tile zooms in: [am / is / are] + [verb] and a pink “-ing” tag clicks on. Then a cartoon hand with five numbered fingers pops up. As each finger lights, a row is added to a five-row list on "
   "the panel, so the whole list is visible at the end: 1 RIGHT NOW – “Look! Snow is falling.” (snow) · 2 TEMPORARY – "
   "“I am learning to swim at present.” (goggles) · 3 CHANGING TRENDS – “House husbands are becoming more popular.” "
   "(rising arrow; gloss strip: house husband = a man who stays at home to look after the home and family) · "
   "4 PHOTOS & PICTURES – “Everyone is smiling happily in the photo.” (camera flash) · 5 ANNOYING HABITS + always – "
   "“He is always complaining about his job.” (grumbling bubbles). The verbs are pink throughout.",
   "The present continuous: am, is or are, plus -ing. It has five uses. Give me five! One: right now. Look! Snow is falling. Two: temporary situations. I am "
   "learning to swim at present. Three: changing trends. House husbands are becoming more popular. Four: photos. Everyone "
   "is smiling happily in the photo. Five: annoying habits, with always. He is always complaining about his job!",
   "standard · talk; eye-roll on ‘always complaining’", 2.0))

# ------------------------------------------------------------------ LEVEL 2
A(("2.0", "Level 2 title", "Sting: “LEVEL 2 UNLOCKED · THE PAST”; the second progress dot fills.",
   "Level two: the past!", "large · cheer", 0.8))
A(("2.1", "Simple past: form and use",
   "The ‘simple past’ tile zooms in. A yellow “+ed” sticker: walk → walked. Irregular verbs flip like cards: "
   "break → broke · is → was. Then the use card FINISHED ACTIONS: a timeline with yellow dots in the past, each "
   "stamped ✓. Sentences with time words in cyan: “I was born in 2013.” · “A fire broke out in my building "
   "yesterday.” Chips: yesterday · last week · two years ago · in 2013.",
   "The simple past is for finished actions. Most verbs add -ed, but some are irregular. I was born in 2013. "
   "A fire broke out in my building yesterday.",
   "standard · talk", 1.5))
A(("2.2", "Past continuous: form and three timeline pictures",
   "The ‘past continuous’ tile zooms in: [was / were] + [verb-ing]. Then three timelines build one under another (Kayla shrinks to give them full width): ① a long pink bar across "
   "yesterday afternoon with a clock pin dropping at 4:00 – “We were having a barbecue at four o’clock yesterday.” · "
   "② a long pink bar hit by a short yellow lightning dot – “She was waiting for the bus when it suddenly rained.” "
   "with labels LONG = past continuous, SHORT = simple past · ③ two parallel pink bars – “Fred was watching TV "
   "while his mum was preparing dinner.” The words ‘when’ and ‘while’ glow cyan, and two tip chips stay on "
   "screen: “when + short action” · “while + long action”.",
   "The past continuous: was or were, plus -ing. Use it for an action in progress at a past time. We were having a barbecue at four o'clock yesterday. For a "
   "long action interrupted by a short one. She was waiting for the bus when it suddenly rained. And for two "
   "actions at the same time. Fred was watching TV while his mum was preparing dinner.",
   "small · talk", 1.5))
A(("T", "Transition clip (approved library clip)", "Kayla's reusable transition, at the halfway point.",
   "Nice one! Now, let's move on to the next part!", "library clip", 0.6))

# ------------------------------------------------------------------ LEVEL 3
A(("3.0", "Level 3 title", "Sting: “LEVEL 3 UNLOCKED · NON-ACTION VERBS”; the third progress dot fills.",
   "Level three: non-action verbs!", "large · cheer", 0.8))
A(("3.1", "Non-action verbs",
   "A title card “NON-ACTION VERBS” appears, then a neon sign “NO -ING ZONE” flickers on beneath it. The verbs drop into four colour bubbles: FEELINGS like, want · "
   "THINKING think, know · SENSES see, smell · OWNING have.",
   "Non-action verbs describe feelings, opinions or states. We don't usually use them with -ing. Like, want, "
   "think, know, see, smell and have.",
   "standard · talk", 1.5))
A(("3.2", "Right and wrong",
   "Each correct sentence slides in with a green ✓; then its wrong version arrives, the pink “-ing” tag bounces "
   "off the sign with a buzzer, and the wrong sentence is struck through with a red ✗: “I think game shows are "
   "exciting.” ✓ / “I am thinking game shows are exciting.” ✗ · “Mike has one brother and one sister.” ✓ / "
   "“Mike is having one brother and one sister.” ✗",
   "I think game shows are exciting. Not I am thinking! Mike has one brother and one sister. Not Mike is having!",
   "standard · shake head on each ‘Not’", 1.5))
A(("3.3", "Plot twist",
   "“PLOT TWIST!” banner. Two cards flip: THINK = opinion (lightbulb) ↔ THINKING = using your brain (turning "
   "gears) – “What is she thinking now?” · HAVE = own (family icon) ↔ HAVING = eating (sushi icon) – “We were "
   "having dinner at a Japanese restaurant.”",
   "Plot twist! Some of these verbs can take -ing when they're actions. What is she thinking now? That's the "
   "action of thinking. We were having dinner at a Japanese restaurant. Here, having means eating!",
   "large · surprised, then standard · talk", 1.5))

# ------------------------------------------------------------------ LEVEL 4
A(("4.0", "Level 4 title", "Sting: “LEVEL 4 UNLOCKED · TENSES IN STORIES”; the fourth progress dot fills.",
   "Level four: tenses in stories!", "large · cheer", 0.8))
A(("4.1", "Stories: past tenses",
   "A storybook opens on the panel: “Once upon a time, there was a beautiful princess who had a kind heart …” – "
   "‘was’ and ‘had’ light up yellow.",
   "Stories that happened in the past usually use past tenses. Once upon a time, there was a beautiful princess "
   "who had a kind heart...",
   "small · storytelling", 0.8))
A(("4.2", "Synopses and retellings: present tenses",
   "Word card: “synopsis = a short summary of a film, play or book”. Then a comic panel: a beach, a shark fin "
   "speeding in, dramatic zoom – “Dora and Sam are resting on the beach when suddenly, they spot a shark …” "
   "‘are resting’ flashes pink and ‘spot’ yellow; tags: lively · dramatic.",
   "But in a synopsis, a short summary of a film, play or book, or when we retell a story, we often use present tenses. "
   "It's more dramatic! Dora and Sam are resting on the beach when suddenly, they spot a shark!",
   "small · excited, surprised on ‘shark’", 0.8))
A(("4.3", "Real-world facts: past tenses",
   "A cinema screen with two zones: INSIDE THE STORY (present) and OUTSIDE THE STORY: REAL-WORLD FACTS (past). "
   "“The film was a big hit when it came out in 2008. In the film, Harry the superhero saves thousands of lives.” – "
   "‘was’ and ‘came out’ fly to the outside zone; ‘saves’ flies onto the screen.",
   "Careful! Real-world facts stay in the past. The film was a big hit when it came out in 2008. In the film, Harry "
   "the superhero saves thousands of lives.",
   "small · talk", 1.0))
A(("4.4", "Back to the hook",
   "The Snow White bubbles return with tags: ‘is’ → TRUE NOW · ‘read’, ‘was’ → FINISHED · ‘reaches’, ‘gives’, "
   "‘saves’, ‘live’ → SYNOPSIS (present). The “?” turns into a green ✓.",
   "Back to Snow White! Is: true now. Read and was: finished. Reaches, gives, saves and live: the story, told in "
   "the present. Every tense has a reason!",
   "large · proud wink", 1.0))

# ------------------------------------------------------------------ BOSS QUIZ + CHEAT SHEET
A(("Q0", "Boss quiz intro", "“BOSS QUIZ” burst; four question dots; the header chip reads BOSS QUIZ.",
   "Boss quiz! Say your answers out loud!", "large · cheer", 0.6))
A(("Q1", "Question 1",
   "“Look! The baby ________ (sleep).” (the blank is one solid line) → 3-2-1 countdown → answer pill “is sleeping” "
   "+ tag “Look! = right now”.",
   "Is sleeping! It's happening right now.", "large · thinking during countdown, wink on answer", 4.0))
A(("Q2", "Question 2",
   "“I ________ (do) my homework when the lights went out.” → countdown → “was doing” + tag “long action, "
   "interrupted”.",
   "Was doing! A long action, interrupted.", "large · thinking, wink", 4.0))
A(("Q3", "Question 3",
   "“Right now, I ________ (want) a new phone.” → countdown → “want” + tag “non-action verb” (‘am wanting’ "
   "appears briefly and is struck through).",
   "Want! It's a non-action verb, so no -ing.", "large · thinking, wink", 4.0))
A(("Q4", "Question 4",
   "“In the film, the hero ________ (fly) to the moon and saves the planet.” → countdown → “flies” + tags "
   "“synopsis = present” and the spelling chip “fly → flies”.",
   "Flies! In a synopsis, we use the present.", "large · thinking, wink", 4.0))
A(("C", "Cheat sheet",
   "The completed Tense Map with the uses written inside each tile, plus two strips underneath: NON-ACTION VERBS "
   "(like · want · think · know · see · smell · have) and STORIES (story → past · synopsis/retelling → present · "
   "real-world facts → past). Sticker: “Pause & screenshot!”",
   "Here's your cheat sheet. Pause the video and take a screenshot!", "small · smile", 4.0))


def est(text, hold):
    return hold if text.startswith("(") else len(text.split()) / WPS + hold


def mmss(s):
    s = int(round(s)); return f"{s // 60}:{s % 60:02d}"


if __name__ == "__main__":
    body = sum(est(s[3], s[5]) for s in S)
    wrap = sum(est(t, h) for _, _, t, h in WRAP)
    total = body + wrap
    words = sum(len(s[3].split()) for s in S if not s[3].startswith("("))
    print(f"body {mmss(body)}  wrap {mmss(wrap)}  total {mmss(total)}  body words {words}")
    # running clock
    t = est(WRAP[0][2], WRAP[0][3]) + est(WRAP[1][2], WRAP[1][3])
    clock = []
    for s in S:
        clock.append((s[0], mmss(t), est(s[3], s[5])))
        t += est(s[3], s[5])
    for c in clock:
        print(c[0], c[1], round(c[2], 1))
    print("outro at", mmss(t))
