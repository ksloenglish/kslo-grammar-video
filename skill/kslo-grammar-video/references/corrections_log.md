# Corrections log: *The present and the past*

This is the chronological failsafe record. Apply the prevention rule to future topics; do not reintroduce an old defect because a source file still contains a pre-fix prototype or comparison branch.

## Before build — 19 Oct 2026, 22:11–23:30 HKT

| Issue / finding | Root cause | Fix and prevention rule |
|---|---|---|
| Early voice auditions misheard 'K S Lo' as 'ESL students', 'Chaos Slow students' or 'K Law'. | Phonetic spelling and ASR were treated as sufficient. | Choose Laomedeia (Voice 2) at natural pitch; write `K S Low` only in TTS text and use blind IPA listening for every library line. ASR spelling cannot prove 'low'. |
| Kayla's initial transparent avatar base had hair touching the left/right edges. | The original crop had insufficient side margin. | Use the supplied keyed/cropped sprite set and inspect cut-out bounds before a new avatar asset; regenerate with margin before substituting base art. |
| A facecam/minimised avatar risked making Kayla too small or covering teaching. | Layout was not designed around a cut-out. | Use adaptive `std`/`small`/`large` cut-out layouts and keep text out of her safe area. |
| Header logo size was arbitrary. | The header had no measurable relationship between logo and divider. | Make the white logo exactly divider height (reference 58 px, y=30–88); never add a logo glow/plate/backing. |
| Earlier proposal had four episodes, unit/S2/episode labels and a strict five-minute expectation. | Planning followed a generic short-video template. | Supersede with one title-only, future-proof video per grammar unit; aim 4–5 minutes but do not rush. |
| Outro chips read 'Tense Map · Give me five · No -ing Zone · Tenses in stories'. | Teaching-device labels were copied as if they were source grammar headings. | Use real grammar points on all recap surfaces (outro, summary, level/header chips, quiz tags, chapters). Devices remain inside the lesson only. |
| Fredoka/Nunito rendered `→`, `↔`, `✓`, `✗`, `①②③` as boxes. | Unsupported glyphs were inserted as text. | Add `check_glyphs()` and draw arrows, ticks, crosses and number circles as shapes/SVG. |

## Build QA round 1 — 19 Oct, 23:30 HKT

| Issue / finding | Root cause | Fix and prevention rule |
|---|---|---|
| A tracked word separated from punctuation ('falling .') or suffix ('She play s'). | `para()` token spacing/gluing was incomplete. | Glue no-space tokens and prevent a glued suffix/punctuation mark wrapping alone. |
| 1.2 cards/icons, 2.1 irregular forms/examples, level XP area and hook bubbles were hard to read/balanced poorly. | First implementation used unreviewed nominal placements. | Enlarge 1.2 text/icons; give irregular cards their own measured row; lower examples; widen XP bar and move its label clear of Kayla; increase hook-bubble font. Review full-resolution stills, not only code. |

## QA round 2 — 20 Oct, 00:13–00:37 HKT

| Issue / finding | Root cause | Fix and prevention rule |
|---|---|---|
| Snow White bubble lines produced orphans; a multi-word quiz placeholder wrapped and overlapped '(sleep)'. | Text was laid out token by token without a protected placeholder. | Test bubble width/line count numerically; make each quiz blank one protected token (placeholder length derived from the answer). |
| Library voice was 3 dB quieter than body voice. | Mono prepared voice becomes +3 LU when duplicated to stereo, while clip refs were mixed at their mono loudness. | Normalise placed clip refs to −15 LUFS stereo; use `STEMS=1` before judging stems. |
| Automated VLM claimed six non-existent defects. Real defects were small frequency chips, a four-second empty book panel and a shark entering from outside its comic. | A broad model review was trusted instead of verified frames. | Verify every automated claim against full-resolution frames. Enlarge chips; introduce book content at 0.6 s; raise shark from the comic/waves. |
| Kayla pronounced *mum* as American *mom*. `mumm`/`muhm` made it worse; ASR still wrote *mom*. | Setting `en-GB` and ASR spelling were mistaken for vowel verification. | Re-record only the affected sentence with `; British English pronunciation`, IPA-listen it, splice at the quiet pre-'And' boundary and match loudness. Do not trust ASR for vowel quality. |
| Captions/timing could drift after fixes. | Caption source was an earlier audio render. | Re-transcribe final audio after **every** timing/audio change, then rebuild both SRTs. |

## Teacher feedback round 3 — 20 Oct, 01:13 HKT; implementation about 01:37

| Issue / finding | Root cause | Fix and prevention rule |
|---|---|---|
| Intro did not identify Kayla's role. | The generic visual lacked a character introduction. | Add a measured game-style nameplate ('KAYLA' / 'your grammar study buddy') at her entrance. |
| Speech-bubble tail showed a horizontal base seam. | Box and tail had separately outlined masks. | Build one merged mask and distance-transform outline; never overlay an independently outlined tail on an outlined box. |
| Glowing `?` sat too near panel bottom. | Placement ignored glow/ink clearance. | Move from y=945 to y=895 and review glow bounds, not just object coordinates. |
| Signal-word chips were unexplained. | Textbook context was assumed. | Add labels: 'Habit words that go with the simple present:' and 'Time words that go with the simple past:'. |
| Past-continuous bars were not centred; `when`/`while` tips were unexplained. | Timelines and labels were placed independently. | Centre bars on timeline axes; add tip lines below examples 2/3. |
| `NO -ing ZONE` and flying `-ing` pill crowded each other. | Sign/right safe edge was not measured. | Leave right breathing space; shrink/route flying pill to sign with measured bounds. |
| 'PLOT TWIST!' and its next line misaligned. | Glow padding changed nominal text bounds. | Anchor text to visible ink (`gpad`), not image bounds. Align related lines by ink edge. |
| Cheat sheet was messy and 'CHEAT SHEET' failed to align. | Free-form tiles and unequal strip labels. | Use bullet tiles, hanging indents, aligned headings/text and equal strip widths. |
| After 00:18 Kayla clip was slow motion. | Retimer stretched the final idle/tail (intro 0.27×, transition 0.60×, outro 0.52×). | Keep tail at natural speed, trim it and cap tail handling (`max_tail 1.2`); never stretch clean audio to fit lips. |
| 'Give me five' hand was choppy/weird. | Tapered finger/blur approach produced webbing/thumb defects. | First improve taper/outline, then retain only the later SDF hand (round 4) after review. |
| 'house husband' remark was unnecessary. | Script carried an unapproved extra gloss into this condensed scene. | Remove it. Keep only teacher-approved explanatory wording. |
| End did not reach full black/silence. | End-card music/picture were not held through a true black ending. | Fade audio/picture together; hold black and silence to EOF. |
| 'NON-ACTION VERBS' appeared run together. | Fredoka kerned space+V too tightly. | Disable that kerning case / inspect visible spacing in pills. |

## Teacher feedback round 4 — 20 Oct, 02:01–02:25 HKT; implementation 02:15–02:35

| Issue / finding | Root cause | Fix and prevention rule |
|---|---|---|
| Snow White hook/return bubbles were unexplained. | Viewers were assumed to know page 52. | Add contextual labels above/between bubbles; every source excerpt must stand alone. |
| 1.2 label/icons were cramped; chips and 2.1 time words vanished too quickly. | Reading time and icon-edge clearance were not budgeted. | Re-space cards/label/chips, keep icons 48 px from edge, extend holds (1.2=2.0 s; 2.1=2.2 s). Never rush a text/chip row. |
| Hand remained broken near thumb. | Discrete shapes and blur cannot guarantee smooth joins. | Rewrite as one SDF: round-cone palm/fingers + polynomial smooth-min joins, analytic AA. Do not revert to `hand_v3_blur.py`. |
| `was preparing` highlight/glow covered too much; three past-continuous cases blurred together; tips flashed past. | Paragraph highlight used whole-line boxes; cards/voice pauses had insufficient separation. | Glow tracked **per-line phrase** boxes; make separate case cards; insert quiet-safe pauses (+0.7/+1.8 s) and 2.4 s hold. Highlight only intended words. |
| Countdown '1' was visibly off-centre. | Advance/font box centring ignored ink shape. | Centre circle digits on ink centroid. Apply optical centring to all pills/badges. |
| Quiz answers were too small; tick crowded panel bottom; NOW line touched 'NOW'. | Text/icon positions used box, not ink/baseline clearance. | Set 68 px answers on a measured baseline, move tick to y=902, and leave a measured 14 px NOW-to-line gap. |
| Use titles looked like highlighted verbs. | Pink/yellow were reused decoratively. | Use lilac for structural step titles; reserve semantic colours. |
| Edges of circles/other shapes were rough. | Native Pillow primitives were hard edged. | Apply 4× supersampled, premultiplied anti-aliasing to all RGB/RGBA primitive shapes. |
| First final check | — | Render 5: 302.53 s, −16 LUFS, 0.84 peak; black/silent end and 77 matched EN/zh-HK cues passed spot review. |

## Teacher feedback round 5 — 20 Oct, 02:44–03:04 HKT

| Issue / finding | Root cause | Fix and prevention rule |
|---|---|---|
| Noise/tail from *yesterday* appeared after an inserted pause. | The pause cutter cut at the ASR word end (10.32 s), while speech actually ended about 10.40–10.42 s. | Search 0–0.6 s after a word for the first ≥40 ms quiet run below −55 dBFS; cut at its quietest frame, use 8 ms fades, shift later words. Rebuilt cut at 10.47 s; final gap max −46/−47 dB. |
| Underline below 'in 2008' had a notch/broken run. | Separate rounded bars met at word boundaries; AA revealed the join. | Draw one underline run per tracked phrase per line. |
| 'Richard' and other left edges looked indented; chip baselines differed. | `textbbox()` ignores left side bearings and a paragraph pad was retained. | Measure visible alpha ink (`ink_cols`); crop/anchor text to visible ink. Centre pills horizontally by ink and vertically by cap/x-height metrics. Run `align_audit.py`. |
| Risk of accepting a transcription blindly. | One ASR and segment time windows are insufficient. | Require `verify_transcript.py`: final ASR vs script by global alignment; faster-whisper word timings for pause/cue windows; SRT integrity; A/B agreement. Round 5 passed 77/77 cue windows and 98.3% A/B (recogniser variants documented). |
| Stem measurements were stale. | `build/stem_*.wav` exist only when `STEMS=1`. | Regenerate stems immediately before audio measurements. |

## Teacher feedback rounds 6–8: *allowed* / final `-ed` saga — 20 Oct, 03:11–04:12 HKT

| Round / issue | Root cause and evidence | Fix / prevention |
|---|---|---|
| R6, 03:11: *allowed* sounded like 'allow-duh'. | Original SH had a −44 dB closure then −10 dB burst; blind listening heard `[laʊdᵊ]`. | Record A/B/C in sentence context; compare spectral high-frequency transient and neutral/reversed A/B tests. A alone beat original in both orders. Splice A with 5 ms fades and restore pause. |
| R6 test-control discovery | A leading paired prompt answered 'SECOND' 4/4; even unedited-line control claimed an edit. | Reverse all paired tests and include controls. Do not accept analyser 'edit heard' assertions. |
| R6 audible result | Spliced A removed burst (final post-vowel max −41 dB) but not audibility. | It passed general transcript QA but was only an intermediate fix. |
| R7, 03:30: `-ed` became inaudible under bed. | A's release was −44 dB, 33 dB below vowel and 14 dB below music. R6 had tested only 'not too strong'. | Add mandatory over-bed final-consonant check using `dcheck.py` and stems. |
| R7 choices | Original: −4.3 dB vs vowel / +14.4 over bed, 10 ms burst (too strong). A/D/F: about −35 to −40 dB (inaudible). E: −8.5 dB but 25 ms voiced tail; G: −14.4 dB but breathy noise. Approved *finished* was −12.4 dB vs vowel / +10.7 over bed, tail 0. | Tame the approved original release (8.942–9.020 s) rather than splice a bad new voice. `SH_tamed5`: −9.2 dB vs vowel, +9.4 over bed, 5 ms tail; `tamed8` softer fallback. |
| R7 analyser failure | Calibrated blind AI marked all eight candidates, including inaudible control A, 'exaggerated'. | Discard that listener result. Anchor judgement to acoustic measure + approved reference and final human listening. |
| R7 final, 03:38–03:45 | `SH_tamed5` final release −9.3 dB vs vowel and +10.1 dB over music/SFX (reference +10.7); no pause insertion; timeline restored 302.53 s. | Keep `SH_tamed5` as chosen reference; retain `tamed8` fallback only if teacher requests softer sound. Rebuild captions/YouTube/verification after any choice. |
| R8 options, 04:02 | Teacher needed a real-mix comparison rather than abstract claims. | Produce six labelled context clips over the real bed: untouched, −3/−5/−8 dB original releases, E splice, E with tail attenuated. Teacher accepted Option 3 (original release −5 dB / `SH_tamed5`) at 04:12. |

## Round 9–10 design-led correction — 20 Oct, 04:12–06:11 HKT

| Issue / finding | Root cause | Fix and prevention rule |
|---|---|---|
| Teacher said the completed PIL body looked like PowerPoint. | The initial renderer could be technically neat but not design-led enough. | Convert lesson graphics to deterministic HTML/SVG/CSS rendered frame-by-frame in Chromium; retain engine timing/Kayla/audio. Build and approve representative 1.2 and 2.2 prototypes before bulk conversion. |
| Focus dimming was unclear as a pedagogic treatment. | The prototype did not explain the choice. | Show with/without side-by-side explainer; teacher chose dimming plus 2.5 s full-brightness review after restore. |
| Formula tokens overlapped in 2.2. | DOM was measured in fallback fonts before async font load. | Explicitly load/check all Fredoka/Nunito faces before `init()` measures; make renderer fail if `window.ready` is false. |

## Round 11 design-led conversion — 20 Oct, 06:20–07:30 HKT

| Issue / finding | Root cause | Fix / prevention rule |
|---|---|---|
| Need to retain every approved visual/audio correction during conversion. | Rebuilding all scenes risks losing small prior fixes. | Make `DESIGN.md` and this log mandatory for scene builders; preserve labels, holds, solid blanks, real grammar recap, lilac structural labels, British spelling and no-glyph-shapes rule. |
| H/4.4 bubble text overflowed; highlight blocks were 74 px tall; tags overlaid prior line. | Manual 63-character line and `.hl` inherited 1.95 line-height. | Use measured/balanced 2+3 breaks, standard 34 px sentence lines, measured bubble size, and throw if line width exceeds bubble inner width. Reposition labels/question/tick by measured bounds. |
| 3.1/3.2 sign casing/counter gap wrong. | Unchecked CSS text-transform and fixed placement. | Use 'NO -ing ZONE'; measure 40 px sign-to-counter clearance. |
| 2.1 displayed `REGULAR (-ED)` and arrow crowded 'break'. | CSS uppercased the suffix and pair card used unmeasured spacing. | Force lowercase `-ed`; measure pair cards with 16 px around arrow and 24 px between pairs. |
| Quiz Q4 had uneven rhythm/crowding/countdown collision; Q3 duplicate tags; Q4 four tags wrapped. | Fixed coordinate template did not react to measured multi-line question/tag content. | Use 52 px/1.5 rhythm, 48 px blank container, countdown below measured question, one grammar tag plus useful tags only. Q3: 'no -ing' + Non-action verbs; Q4: Tenses in stories only. |
| 4.1 book and 4.3 card stood empty for about three seconds; level cards held too long. | Decorative frame appeared before voice-cued content; inherited 2.0 s level holds. | Bring book/spine in just before cue; cue cards at content; set all level holds to 1.2 s. |
| Final acceptance | — | Full design-led render 11: 319.6 s/5:19.6, 1920×1080/30 fps, −16 LUFS, 0.835 peak, black/silent end; 77 EN=zh-HK cues; transcript checks passed (A/B 98.1%, B/script 98.4%; only documented recogniser spellings). |
