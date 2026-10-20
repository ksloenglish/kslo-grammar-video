# Kayla's Grammar Lab: standing requirements

Treat these as **acceptance criteria** for every new video unless Mr Kum explicitly changes a rule. The finished reference video is *Kayla's Grammar Lab — The present and the past* (5:19.6). Use British English, British spelling and British single-quotation-mark punctuation throughout.

## Audience, series and title

| ID | Requirement / pass condition |
|---|---|
| A1 | Make 1920×1080, 16:9, 30 fps videos for Hong Kong secondary students of HKMA K S Lo College. Address them on screen and in speech as **'K S Lo students'**. |
| A2 | Present Kayla as an upbeat, friendly **grammar study buddy**, not a formal teacher. Make the work polished, teenage-appropriate and self-contained. |
| A3 | Use **'Kayla's Grammar Lab'** plus the teacher's **unit title only** (for example, *The present and the past*). Never show a unit, episode or form number; do not infer one. This keeps the series future-proof. |
| A4 | Make one concise video per grammar unit. Aim for roughly **4–5 minutes**, but do not rush teaching to force a five-minute limit. A video may exceed five minutes where reading/review time requires it; the reference video is 5:19.6. |
| A5 | Base grammar content on the teacher's supplied pages and an approved body script. Retain correct textbook terms and examples unless the teacher approves a change. Do not try to include every example. |

## Kayla, voice and branding

| ID | Requirement / pass condition |
|---|---|
| K1 | Use approved **Design A, 'Neon Pop'**: the original trendy VTuber-style study buddy. Use the supplied cut-out avatar/sprites; never substitute another character or regenerate her casually. |
| K2 | Keep Kayla as a cut-out, with **no box or facecam frame**. Use the standard, small or large layout as the scene needs; resize/reposition her so she never covers lesson text, labels, icons or quiz content. |
| K3 | Use **Laomedeia**, `en-GB`, at the approved natural pitch (no pitch lift). Use the exact styles and pronunciation/verification procedure in `voice_and_audio.md`. |
| B1 | Show the white K S Lo English logo at the opening, in the body header and on the end card. Preserve the transparent logo: **never add a glow, plate, fill, backing or box behind it**. Put it against the dark/vivid series background. |
| B2 | In the body header, set the logo to the **same height as the divider** (reference: y=30–88, 58 px high). Do not make a smaller arbitrary logo. |
| B3 | Use the title lock-up without a unit-number pill. Use a Kayla name tag in the opening: 'KAYLA' / 'your grammar study buddy'. |

## Mandatory running order

Use this order, adapting the number of levels and the point of the one reusable transition to the approved script:

1. **L0 logo opening** — logo, series title and unit title; music sting.
2. **L1 reusable intro clip** — Kayla greeting K S Lo students, with the on-screen title/overview.
3. **Hook** — a contextualised question or source example that is answered later.
4. **Overview map** — show the unit's system/map before its levels where suitable.
5. **Levels** — level card then the approved form/use/explanation scenes for each real grammar point.
6. **T reusable transition clip** — normally between the two broad halves of the lesson.
7. **Quiz** — question, three-second 3–2–1 countdown, then answer/explanation.
8. **Cheat sheet** — concise 'Pause & screenshot!' recap.
9. **L3 reusable outro clip** — card lists only the unit's actual grammar points.
10. **L4 end card** — fade fully to black and to silence; hold black/silence before EOF.

Use only reusable generic library clips for a normal topic. Their spoken lines never name a unit or number; show the topic only in on-screen text.

## Visual and motion system

| ID | Requirement / pass condition |
|---|---|
| V1 | Keep the approved **Style A, 'Neon Stream'** identity: midnight-violet field; Fredoka display type and Nunito body type; yellow = simple tense verbs, pink = continuous verb phrases, cyan = time/signal words, lilac = structural labels, mint/orange = PRESENT/PAST tags, mint tick/red cross = correct/wrong. |
| V2 | Use the **design-led HTML/SVG/CSS layer** for lesson graphics. The first PIL/PowerPoint-like lesson treatment is **superseded**; use it only through `NO_HTML` for comparison/debugging, not for a new production scene. Keep L0, L1, T, L3 and L4 as the library/base scenes unless a replacement is approved. |
| V3 | Make motion serve an explanation: cue visual events to the narration; use diagrams, timelines, formula tokens, comparison pairs and maps rather than decorative bullets. Use masked rises, word reveals, highlighter sweeps and restrained draw-on icons. No spins, wobbles, flashing, clip-art, emoji, rainbow gradients or WordArt. |
| V4 | Draw arrows, ticks, crosses and numbered circles as SVG/shapes, not unsupported Unicode glyphs. Run glyph coverage checks for all visible strings. |
| V5 | Use anti-aliased shapes. Keep the approved signed-distance-field 'Give me five' hand; do not replace it with separately stamped/blurred fingers. |
| V6 | Make every focal signal **solid and prominent**: the hook/recap question mark is the yellow `qToken()` disc (bold navy '?', glow, gentle wobble) that hands over to the mint tick disc in the same spot; never a thin outline icon. Use literal, decent icons from the MIT catalogue as filled `badge()`s (Phosphor v2.1.1, Fluent Emoji shark); never hand-drawn SVG paths for a featured object (the clapperboard and shark were rejected). |

## Layout, clarity and reading time

| ID | Requirement / pass condition |
|---|---|
| L1 | Follow the design grid. Standard panel: x=60 to 1170, y=130 to 1030; small: right edge 1400; large: teaching content x=90–760 because Kayla occupies the right. Keep content below the header zone and at least 40 px inside panel edges. |
| L2 | Use one left alignment system. Align **visible ink**, not nominal Pillow/CSS boxes. Lines that belong together must align exactly; audit near-misses. |
| L3 | Give text, labels and icons breathing space. Do not crowd panel edges, icon/card edges, the bottom of a panel, each other, or Kayla. Use at least 20 px type and no clipped/overflowing text. |
| L4 | Vertically and optically centre text in every pill, chip, badge, circle and answer container, including narrow digits such as '1'. Centre single glyphs by **ink box** with `inkGlyph()` (60 % optical mass correction); verify in the rendered PNG. |
| L5 | Assume viewers have **not read the grammar book**. Add short context labels for unexplained source material, signal-word chip rows and diagrams. Explain `when`/`while`, LONG/SHORT, or similarly non-obvious visual coding on screen. |
| L6 | Highlight **only the intended grammar words**. Preserve word-level colour meaning; do not put a glow/highlight around an entire sentence where only a verb phrase is meant. |
| L7 | Use a solid drawn blank line in every quiz; never underscores, dashes or a broken underline. Keep the answer on the measured baseline above the line and keep the countdown clear of multi-line question text. |
| L8 | For a sequential 3+ row scene, use numbered rows/progress rail and focus dimming. When the next row begins, fade earlier rows; after the voice ends, restore all rows (review begins at `voice_end + 0.35 s`, restore for 0.6 s), then hold full brightness for 2.5 s. Request this as a **3.9 s post-voice hold**. |
| L9 | Give any final readable item at least **1.5 s** after it appears. Give level cards a **1.2 s** hold. Do not cut a scene until the student has had time to read tips, labels, chips and recap content. |
| L10 | **Use the free space.** A lone short example in a mostly empty panel is scaled up to fill the band (e.g. 'She plays.' at 132 px). Quiz: 168 px countdown timer disc with running yellow arc; answer pills 86 px with 54 px text; tags 54 px. |
| L11 | Compound formula chips (`verb`+`-ing`, `was/were`+`verb-ing`) **dock with no gap**, placed by measured width minus the shared border, never by fixed x. Related icons, labels and chips in a column share one centred axis; card text has ≥ 30 px visible-ink padding. |

## Lesson integrity, recap and end

- Keep the approved sequence, wording and timing relationship between speech and teaching content. A layout/motion redesign must not silently add, remove or rewrite teaching content.
- Use **real grammar points** from the source pages in level names, header chips, quiz grammar tags, cheat-sheet headings, outro chips and YouTube chapters. 'Tense Map', 'Give me five', 'No -ing Zone', 'Plot twist' and 'Boss quiz' are **teaching devices**, not recap subjects.
- Make an outro card list only the unit's genuine grammar points. Never list devices as though they were grammar points.
- End with a full fade to black **and silence**. In the reference engine, the end fade runs from L4+4.5 to L4+5.4 s, then holds black/silent to the end; preserve an equivalent verified ending.

## Captions and YouTube text

| Deliverable | Acceptance criterion |
|---|---|
| Captions | Deliver two separate SRTs: English and `zh-HK`. Chinese must be **Traditional, Hong Kong standard written Chinese (書面語)**, not Cantonese. Retain English example sentences in English within the Chinese track. English captions match the approved spoken script and both tracks have identical cue timings. Do not burn captions into the picture. |
| YouTube text | Deliver a title, description, chapters and tags automatically with the video. Title format: `<unit title> \| Kayla's Grammar Lab \| K S Lo English`. In the description, greet K S Lo students; list the real grammar points, quiz and cheat sheet; use final timeline chapter times; state English and Traditional Chinese captions; include suitable hashtags/tags. Never mention AI, Manus or 'generated'. Regenerate after a title, content or timing change. |
| Upload labels | Use **English (United Kingdom)** and **Chinese (Hong Kong)** (or Chinese Traditional, if YouTube requires it). Do not upload/publish without a separate instruction. |

## Superseded decisions (do not revive)

- **Four short episodes / a hard under-five-minute cap**: superseded by one video per grammar unit; clarity outranks a strict duration cap.
- **Old PIL/PowerPoint-like body graphics**: superseded by the approved design-led HTML motion system.
- **A generic outro recap of lesson devices**: superseded by real grammar-point-only recaps.
- **Any unit/S2/episode number in titles or speech**: superseded by title-only future-proofing.
- **A framed/minimised facecam Kayla**: superseded by the adaptive cut-out avatar.
