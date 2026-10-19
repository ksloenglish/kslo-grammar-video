# Kayla's Grammar Lab — design-led motion system (read fully before building a scene)

Video: "Kayla's Grammar Lab — The present and the past", 1920x1080, 30 fps, for Hong Kong secondary students
(K S Lo English). Kayla is a VTuber-style study buddy drawn by the engine (NOT by you). Teacher: British English,
British spelling, British single quotes (‘ ’). The teacher APPROVED two design-led scenes and asked for ALL other
lesson scenes to be converted to the same system, so they no longer look like PowerPoint. The approved references:
`proto/scenes/1.2.js` (Simple present, three uses) and `proto/scenes/2.2.js` (Past continuous, three uses).
Look at both, and at their stills: `python3 build.py stills 2.2 3 15 27.5` and `python3 build.py stills 1.2 7.6 12.6 15`
(run inside `/home/ubuntu/kslo_grammar/render`; JPGs appear in `/home/ubuntu/kslo_grammar/build/stills/`).

## 1. How a design-led scene works
- The engine (`render/engine.py`, `render/scenes.py`) still owns timing, Kayla, the background, the header (logo top-left,
  level chip top-right) and the voice. For a design-led scene it draws NO lesson graphics and NO glass panel; your
  transparent browser layer is composited on top of every frame.
- Your scene = ONE file `proto/scenes/<SID>.js`, loaded by `proto/shell.html?s=<SID>` after `proto/lib.js`.
  Templates: `proto/scenes/_level.js` serves 1.0/2.0/3.0/4.0 and `proto/scenes/_quiz.js` serves Q1–Q4 (read `CUES.sid`).
- Wrap the file in an IIFE `(() => { ... })();` and define `window.init = function (cues) {...}` (build DOM, measure,
  register SFX, optionally return an info object) and `window.seek = function (t) {...}` (set every style for time t).
- `seek(t)` MUST be a pure function of t (scene-local seconds): no CSS transitions/animations, no Date, no unseeded
  random. Frames are rendered in any order, in parallel.
- Scene-specific CSS: `document.head.insertAdjacentHTML("beforeend", "<style>...</style>")` at the top of your file.
  Do NOT add global `svg path {fill:none}` rules (they override SVG fill attributes used by lib icons).
- Extra icons: add to the shared object inside your file, e.g. `ICONS.lock = [["path", "M..", 0], ...]` (64x64 viewBox,
  role 0 outline, 1 accent stroke, 2 filled accent).

### `CUES` (also passed to init) — all times scene-local seconds
`sid, dur, t0, fps (30), lead, voice_end` (time the voice ends; null if no voice), `words` = [[word, start, end], ...]
(ASR of Kayla's line, already offset by lead), `panel` = per-frame [right, alpha], `kayla` = per-frame [cx, top, h],
`level, label, kc` (Kayla's expression cues, drawn by the engine). Print a scene's words with
`cd /home/ubuntu/kslo_grammar/proto && python3 layer.py cues <SID>` (writes `proto/cues/<SID>.json`).

### lib.js API (do not edit lib.js; copy/extend inside your own file if you need a variant)
- `cue(phrase, n=1, end=false)` → start time of the n-th occurrence of a phrase in the voice (end=true → its end).
  Throws if missing (then check the word list: ASR spellings can differ, e.g. "Tsing" may be "Ching").
- `fx(t, name, gain)` → register a sound effect (names: buzz click correct glitch levelup pop sparkle sting tick whoosh).
  Register them in init(). Your scene's SFX REPLACE the old scene's SFX, so recreate the old ones that still fit.
- Layout: `panel(x, y, w, h)` glass card; `followPanel(pn, t)` sets its width/opacity from the engine layout every
  frame (alpha 0 in the 'large' layout = no panel); `panelAt(t)`, `kaylaAt(t)`; `hrule(x, y, w, alpha)`.
- Text: `masked(text, style)` + `reveal(m, p)` (text rises through a mask); `sentence(markup, x, y, size)` with markup
  `{phrase|k}` highlight groups (k: v/y yellow, p pink, t cyan) and `\n` line breaks; `riseWords(sn, t, t0, stagger)`;
  `sweep(group, t, ts, d)` highlighter sweep (text turns ink as the marker passes).
- Icons: `icon(name, x, y, size, outline, accent, parent, strokeWidth)` + `drawIcon(ic, p)` draw-on. Built in:
  thermometer pin alarm clock bolt tick cross arrow question book star.
- Motion: `ease.outExpo/outCubic/inCubic/inOutCubic/outBack`, `spring(s, w, z)`, `prog(t, t0, d)`, `clamp`, `lerp`,
  `mix(c1, c2, p)`; `exitLift(node, t)` standard exit (lift 16 px + fade over 0.42 s from dur − 0.45).
- Palette `C`: yellow #FFD93D, cyan #2EE6FF, pink #FF4FA8, lilac #C0A6FF, dim #CDC3F0, ink #281450, white.
  Also used in the old design with meaning: mint #5CF2B0 (PRESENT tag, correct), orange #FFA448 (PAST tag),
  red #FF5468 (wrong). Glows: `GLOW.yellow/cyan/pink` (use sparingly).

## 2. The visual language (match 1.2 and 2.2)
- Grid: glass panel at x 60, y 130, height 900 (bottom 1030); its right edge comes from the layout (std 1170,
  small 1400). Content left edge L = 116; number column L, text column 196 when rows are numbered; right content edge
  = panel right − 56. Keep ≥ 40 px inside the panel edges. Nothing above y 140 (header zone).
- Kayla must never be covered: std layout → keep content left of x 1130; small layout → x < 1360 and avoid the bottom-
  right (Kayla's head starts at y ≈ 700 from x ≈ 1450); large layout (no panel, Kayla big from x ≈ 800) → keep content
  in x 90–760. If a scene changes layout, use per-frame `kaylaAt(t)`/`panelAt(t)`.
- Type: titles Fredoka 600, 58 px, white, top 176 with a hairline rule (alpha 0.18) at y 266 spanning the content
  width. Step labels: Nunito 800, 20 px, UPPERCASE, letter-spacing 0.14em, lilac. Numbers: Fredoka 600 30 px "01".
  Example sentences: Nunito 800, 38–46 px, white, highlighted words via `sentence()`. Secondary text Nunito 700
  22–24 px, colour dim. Minimum text size 20 px. One type scale per scene; align left edges on the grid.
- Colour meaning (keep consistent across the video): yellow = simple tense verbs (simple present / simple past);
  pink = continuous verb phrases; cyan = time expressions / signal words (every day, yesterday, when, while...);
  lilac = structural labels; mint/orange tags = PRESENT/PAST (as in the old hook); red = wrong.
- Restraint: flat glass cards with hairline borders, generous spacing, at most ~3 accent colours on screen, small
  glows only on the focal element. No clip-art, no emoji, no drop-shadowed WordArt, no rainbow gradients, no bouncy
  cartoon pops on body text. Never use Unicode arrows/ticks/crosses (→ ✓ ✗) — draw them as SVG (ICONS.arrow/tick/cross).
- Diagrams beat bullet points: timelines, bars, token formulas (e.g. `was / were` + `verb` + `-ing` docking), grids,
  sorting bins — like 2.2's timelines and formula tokens.

## 3. Motion language
- Everything is cued to Kayla's voice with `cue()`: an element appears when she says it (structure such as a card
  or a rule may lead by 0.1–0.3 s). Never show content long before it is spoken, never late.
- Entrances: masked rise for titles/labels (outExpo 0.7–0.8 s); sentences rise word by word (stagger 0.05 s, 0.6 s,
  start ≈ 0.12 s before the first spoken word); highlighter sweeps 0.3–0.42 s when the word is spoken (or once the word
  has landed); rules draw with scaleX (outExpo 1.0 s); icons draw on (0.6 s); tokens slide 18 px + fade (outExpo 0.6).
  Springs only for docking/counters. No spins, no wobbles, no flashing.
- Sequential rows (3+ items): numbered rows with a progress rail + "01 / 03" counter, and FOCUS DIMMING: when row k+1
  starts, earlier rows fade to 0.4 opacity over 0.5 s; at the review (voice_end + 0.35) all rows return to full
  brightness over 0.6 s. TEACHER RULE: every dimmed scene then holds 2.5 s at full brightness before the exit, i.e.
  dur = voice_end + 3.9 → request it by writing `3.9` into `proto/holds/<SID>.txt` (plain number = seconds after the
  voice ends). Other scenes: request a hold only if the teacher rules below need it (reading time after the last item
  ≥ 1.5 s for anything with text to read).
- Exit: `exitLift(contentRoot, t)` at the end of every scene (the last frame must be empty of lesson graphics so
  scenes chain cleanly). Keep the panel itself visible until the exit (fade it with the content).

## 4. Content fidelity (most important)
- Read the OLD scene code in `render/scenes.py` (function names: s_H, s_M, s_level, s_11, s_12, s_13, s_21, s_22, s_31,
  s_32, s_33, s_41, s_42, s_43, s_44, s_Q0, s_Q, s_C) and render the old design with
  `NO_HTML=all python3 build.py stills <SID> t1 t2 ...` to see exactly what is on screen now.
- Keep ALL teaching content and on-screen wording of the old scene (sentences, labels, tags, tips, chips, captions)
  and its timing to the voice. You may restructure layout and motion; you must not drop, add or reword teaching
  content (tiny formatting changes such as capitalisation of labels are fine; list any wording change in your report).
- Grammar terms must stay accurate; examples must stay exactly as spoken.
- Global teacher rules already approved in feedback: viewers have NOT seen the grammar book, so each screen must be
  self-explanatory (context labels); nothing rushed (video may exceed 5 min); breathing space around icons/labels;
  lines that belong together must align exactly; vertical centring of text in pills/containers; quiz blank lines
  are solid lines (never underscores); highlight only the words meant (e.g. ‘was preparing’, not the whole line);
  give viewers time to read tips and chip rows.

## 5. QA you must do before reporting
1. `cd /home/ubuntu/kslo_grammar/render && python3 build.py stills <SID> t1 t2 ...` at key moments (each entrance, the
   busiest moment, the review/hold, 0.2 s before the end) and LOOK at them (read the JPGs). Check: no overflow/clipping,
   left edges aligned, ≥ 16 px between elements, text not touching card edges, nothing over Kayla or the header,
   minimum sizes, highlight colours per §2, last frame clean. Also compare with the old design stills.
2. Render your full segment once (`python3 build.py render <SID>` → `build/seg/NN_<SID>.mp4`) and extract a frame
   sheet (e.g. ffmpeg fps=2 tile) to check motion is smooth and cued; fix and re-check.
3. Page errors raise immediately; there must be none.
Do NOT edit: lib.js, shell.html, layer.py, build.py, scenes.py, engine.py, gl.py, NOTES.md, other builders' scene
files. You own only your scene files, `proto/holds/<your SIDs>.txt` and `proto/assets/<your SID>/` (for exported
images, e.g. PNGs made from render/hand.py). Do not run `build.py audio`, `mux` or a full `render` without SIDs.

## 6. Report (final answer)
Per scene: one-paragraph design summary; cue words used; SFX list; hold requested; any wording deviations; paths of
3 representative full-frame stills; known issues. Keep it concise.
