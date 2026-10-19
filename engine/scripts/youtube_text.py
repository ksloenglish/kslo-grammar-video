# -*- coding: utf-8 -*-
"""YouTube title, description (with chapters from build/timeline.json) and tags -> output/YouTube_text.md"""
import json
ROOT = "/home/ubuntu/kslo_grammar"
tl = {d["sid"]: d for d in json.load(open(f"{ROOT}/build/timeline.json"))}
total = tl["L4"]["t0"] + tl["L4"]["dur"]
mmss = lambda t: f"{int(t // 60)}:{int(t % 60):02d}"

# Chapter names = the unit's grammar points (rule: no teaching-device names on recap surfaces)
CH = [("L0", "Introduction", 0.0), ("H", "Review: the present and the past", None), ("1.0", "Simple present", None),
      ("1.3", "Present continuous", None), ("2.0", "Simple past", None), ("2.2", "Past continuous", None),
      ("3.0", "Non-action verbs", None), ("4.0", "Tenses in stories", None), ("Q0", "Quiz", None),
      ("C", "Summary", None)]
chapters = [f"{mmss(t if t is not None else tl[s]['t0'])} {name}" for s, name, t in CH]

TITLE = "The present and the past | Kayla’s Grammar Lab | K S Lo English"
DESC = f"""Hello, K S Lo students! Join Kayla, your grammar study buddy, for a quick and colourful review of the present and the past.

In under five minutes, you will learn:
• the simple present: facts, things that are true now and habits
• the present continuous: five uses, from actions happening right now to annoying habits with ‘always’
• the simple past: finished actions, with regular and irregular verbs
• the past continuous: actions in progress, long actions interrupted by short ones, and two actions at the same time
• non-action verbs such as like, want, think, know, see, smell and have, and when some of them can take -ing
• tenses in stories: why we can use present tenses in a synopsis or when retelling a story

Stay until the end for a four-question quiz and a cheat sheet you can screenshot.

Chapters
{chr(10).join(chapters)}

Captions are available in English and Traditional Chinese.

#Grammar #EnglishGrammar #Tenses #KSLoEnglish"""

TAGS = ["K S Lo English", "Kayla's Grammar Lab", "English grammar", "tenses", "simple present", "present continuous",
        "simple past", "past continuous", "non-action verbs", "state verbs", "tenses in stories", "synopsis",
        "present and past tenses", "grammar revision", "secondary school English", "Hong Kong"]

md = f"""# YouTube text: The present and the past

**Video length:** {mmss(total)}

## Title

{TITLE}

## Description

```
{DESC}
```

## Tags

{", ".join(TAGS)}

## Captions to upload

Upload both SRT files under Subtitles: `Kayla_Grammar_Lab_The_present_and_the_past.en.srt` as **English (United Kingdom)** and
`Kayla_Grammar_Lab_The_present_and_the_past.zh-HK.srt` as **Chinese (Hong Kong)** (or Chinese (Traditional)).
"""
open(f"{ROOT}/output/YouTube_text.md", "w", encoding="utf-8").write(md)
print(md)
