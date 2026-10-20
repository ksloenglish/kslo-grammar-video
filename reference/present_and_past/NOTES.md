# K S Lo grammar video series with Kayla: production record

## Status (19 Oct 2026, 22:25 HKT)
Stage 0: proposals delivered; awaiting teacher choices/approvals (design, voice, library scripts, episode split,
series title, body scripts, textbook changes, music, captions). NOTHING built or generated as video yet.

## Brief (teacher, 19 Oct 2026 22:11)
- New grammar series modelled on /kslo-vocab-video workflow; audience = vocab-series audience (S2), addressed as
  "K S Lo students". Design must differ from vocab series. Virtual study buddy 'Kayla', typical trendy VTuber look;
  3 designs to choose. Young-girl VTuber voice; 3 voices to choose.
- Reusable intro/transition/outro clips; K S Lo English logo at beginning, body and end. Show scripts first.
- Body from teacher-supplied grammar book pages (Unit 8 The present and the past, pp. 52-54); may simplify/elaborate;
  effective strategy for tables/lists; graphics allowed. Body script approval before building.
- Suggest length (short). Minimise cost: motion graphics mostly. 16:9. Video model seedance-2-5 (4-30 s, 720p).

## Sources
- upload/pasted_file_yusG78_image.webp (p.52), pasted_file_xddcW5_image.webp (p.53), pasted_file_afHCwG_image.webp (p.54)
- Brand logo: ~/kslo-vocab-video/brand/logo_white.png (white on transparent; never glow/plate)

## Generated so far
- design/kayla_A_neon_pop.png (sha f1f1bb163bafd4aa), kayla_B_cyber_scholar.png (6d54a6d42d5bca90),
  kayla_C_cosy_bookworm.png (bf2c4a65302480cb); gpt-image-2.5, 2560x1440, sheet = thigh-up neutral clasped pose + 3
  expressions (wink, surprised, thinking). Prompts: see scripts/ (copied in this file's history) and job record.
- output/Kayla_design_options.jpg: labelled comparison sheet.
- Voice samples (en-GB, style "high pitch, bubbly, playful and energetic", same text with "K. S. Low"):
  - Voice1 Zephyr = voice/kayla_voice1_Zephyr_v2.wav (ASR "KSLO students"; F0 median 276 Hz; 15.7 s)
  - Voice2 Laomedeia = voice/kayla_voice2_Laomedeia.wav (first take, text "K S Low"; ASR "KSLO students"; F0 220 Hz)
    REJECTED take: kayla_voice2_Laomedeia_v2.wav (ASR "K Law" -> "law" fault, V2 rule)
  - Voice3 Achernar = voice/kayla_voice3_Achernar_v2.wav (ASR "KSLO students"; F0 294 Hz; 14.5 s)
  - Rejected first takes: Zephyr v1 (ASR "ESL students"), Achernar v1 (ASR "Chaos Slow students").
  - Leda excluded on purpose (Miss K's voice). ASR spelling cannot prove "Lo"="low"; recheck by listening in library lines.
- Scripts: scripts/scripts_data.py (structured, timed at 2.6 words/s + holds) -> scripts/build_proposal.py ->
  output/Kayla_Grammar_Series_Proposal.md

## Proposed decisions (pending approval)
- 4 episodes for Unit 8: Ep1 simple present vs present continuous (~3:24), Ep2 simple past vs past continuous (~2:52),
  Ep3 state verbs (~2:16), Ep4 tenses in stories (~2:51). Target 3-4 min, max 5.
- Kayla body presence = code-animated still-image avatar ("PNGtuber": mouth closed/half/open, blink, wink, surprised,
  thinking); Seedance only for 3 generic library clips (intro, transition, outro), 2 variants each.
- Colour code: yellow simple, pink continuous, cyan time/signal words, green tick / red cross.
- Textbook changes proposed: born 2011->2013; grandpa passed away -> family moved to Tsing Yi; form reminders;
  house-husband gloss; when/while tip; state-verb grouping + extras; optional Snow White synopsis; own quizzes.

## Teacher decisions (19 Oct 2026, 22:43 HKT)
- Design A (Neon Pop). Voice 2 Laomedeia, natural pitch (no lift). Library scripts L0-L4 APPROVED as written.
- ONE video per grammar unit, 4-5 min, not every textbook example. (4-episode plan superseded.)
- Series name "Kayla's Grammar Lab"; NO unit numbers anywhere (future-proof); show unit title only, e.g.
  "The present and the past". Proposed: also omit "S2" (pending confirmation).
- New signature music track. Captions: English + Hong Kong Chinese SRT (proposed: Traditional, standard written
  Chinese, HK school grammar terms, English examples kept in English; pending confirmation of written vs Cantonese).
- Asked: is Kayla a cut-out or minimised? Answered: cut-out, no box, bottom-right waist-up ~2/3 screen height,
  teaching panel on the left never covered; larger at pop-up moments. Mockup: output/Kayla_onscreen_mockup.jpg.

## New assets (19 Oct 2026)
- design/kayla_keyframe_green.png: Seedance keyframe (gpt-image-2.5 high, 2560x1440, thigh-up, hands clasped,
  flat #00FF00). Keyed copy for mockups: work/kayla_keyed_mock.png (simple G-max(R,B) key, 40-120 ramp).
- design/kayla_avatar_base.png: transparent waist-up avatar base (1632x2176). NOTE hair tips touch left/right
  edges (alpha 233/249 at x=0/x=max): regenerate avatar stills with more side margin before final use.
- fonts/Fredoka.ttf (display, variable: Bold/SemiBold), fonts/Nunito.ttf (sentences, ExtraBold).
- scripts/mockup_layout.py -> work/mock_teaching.jpg, work/mock_popup.jpg, output/Kayla_onscreen_mockup.jpg.
  Layout rule: teaching panel x 60-1170 (1920 canvas); Kayla centre x~1660, top y~330, height 1000 (keyed keyframe).
- output/Kayla_Single_Video_Plan.md: single-video plan v2 (Tense Map + 4 levels, est. 4:42). Awaiting approval;
  then write full body script for approval (v2 structure) before building.

## Teacher decisions (19 Oct 2026, 23:00 HKT)
- Single-video plan v2 APPROVED (Tense Map + 4 levels). Next: word-for-word body script for approval.
- Header logo: SAME HEIGHT AS THE DIVIDER LINE to its right (1080p: line y 30-88 -> logo 58 px tall, top 30).
  Mockup: output/Kayla_onscreen_mockup_v2.jpg (before/after close-up + 3 Kayla sizes). Awaiting OK.
- Kayla size adapts per scene: standard (centre x 1660, top 330, h 1000 keyed keyframe), small corner for wide
  scenes (centre 1730, top 700, h 560; panel to x 1400), large pop-up (centre 1460, top 110, h 1350).
- Quiz blanks = ONE SOLID LINE (drawn), never underscores or dashes. Also keep other lines solid (Style C fixed).
- "S2" omitted everywhere (video + YouTube title). Chinese captions = standard written Chinese (書面語), Traditional.
- Asked for motion-graphics style options -> output/Motion_graphics_style_options.jpg (scripts/style_mockups.py):
  A Neon Stream (dark violet glass/neon), B Candy Sticker Pop (violet-pink gradient, white outlined sticker cards,
  white die-cut outline on Kayla), C Arcade Level-Up (pixel HUD, PressStart2P headings, XP bar, scanlines).
  Logo is white-only (both brand PNGs pure white) -> every style needs a dark/vivid background behind the white logo.

## Teacher decisions (19 Oct 2026, 23:12 HKT)
- Logo size OK (same height as divider). STYLE A (Neon Stream) CHOSEN.
- Pills/chips/badges: text must be OPTICALLY CENTRED by ink bbox (mockup_layout.centred_text); the old fixed y-offset
  made 'is sleeping' sink (gaps 26/2 px -> now 13/15). Close-up: output/Quiz_pill_centring_closeup.jpg.
- Body script v1 written: scripts/single_script.py (data, single source of truth) -> scripts/build_body_doc.py ->
  output/Kayla_Body_Script_v1.md. Est. 4:57 (body 4:18) at 2.4 wps. Awaiting approval.
  Quiz Q3 'Right now, I ___ (want) a new phone.' and Q4 '... (fly) to the moon and saves the planet.' were given
  context so only one answer fits. TTS respell: read(past)->'red', '-ing'->'ing', Tsing Yi -> check by ear.

## Error record (19 Oct 2026, 23:26 HKT) - outro chips listed teaching devices
- Problem: outro card chips were "Tense Map · Give me five · No -ing Zone · Tenses in stories". Teacher: 'Give me
  five' is not a main focus of the unit.
- Root cause: chip labels were copied from my own section/device names instead of the source pages' grammar headings;
  no rule separated GRAMMAR POINTS from TEACHING DEVICES.
- RULE (all future videos): recap surfaces (outro chips, cheat sheet headings, level names/header chips, quiz answer
  tags, YouTube chapters) use the unit's grammar points as named in the source pages. Devices (Tense Map, Give me
  five, No -ing Zone, Plot twist, Boss quiz) may appear only inside the lesson, and only alongside the real term.
- Applied: outro chips = Simple present · Present continuous · Simple past · Past continuous · Non-action verbs ·
  Tenses in stories (output/Outro_card_mockup.jpg). Level 3 = "NON-ACTION VERBS" (No -ing Zone sign kept inside);
  Q3 tag "non-action verb"; cheat-sheet strip "NON-ACTION VERBS". Script re-timed 4:56.
- Also found: Fredoka and Nunito have NO glyphs for → ↔ ✓ ✗ ①②③ (rendered as boxes). RULE: draw arrows, ticks,
  crosses and numbered circles as shapes; mockup_layout.check_glyphs() now raises on any missing glyph (called by
  centred_text/pill); reuse it in the final renderer for every on-screen string.

## BUILD STARTED (19 Oct 2026, 23:30 HKT) - teacher approved body script v1 ("Approved. Start building.")
Build plan / file map:
- Voice: Laomedeia, en-GB, style "high pitch, bubbly, playful and energetic" (+ "; clear and unhurried" for teaching
  scenes). Lines + respellings: scripts/tts_lines.py -> audio/tts_lines.json; takes -> audio/vo/<id>.wav.
  Respell only for TTS: K S Low, red (past read), ing, ed, Ching Yee, twenty thirteen, two thousand and eight, liv.
- Seedance library clips (intro/transition/outro): keyframe design/kayla_keyframe_green.png first=last, refs from
  audio/vo via 0.5 s lead padded to whole s (vocab make_refs logic), 2 variants each, retime with vocab
  retime_clip.py, QA (green bg, transcript, gesture contact sheet).
- PNGtuber avatar: nano-banana edits of keyframe (mouth half/open, blink, wink, surprised, thinking pose) ->
  ECC-align to base -> face-region feathered composite -> key. Lip-sync from voice RMS.
- Music: theme (logo/intro/outro/end) + study bed (body), same key/BPM, instrumental. SFX synthesised (numpy).
- Renderer: Python PIL frames 1920x1080 30 fps -> ffmpeg; captions EN + zh-HK written Chinese SRT; YouTube text.
- VOICE TAKES CHOSEN (blind IPA check via manus-analyze-video on cropped phrase; ASR alone unreliable):
  L1_intro_C [kʰeɪ ɛs loʊ] OK (L1 v1 merged 'KS', L1_B 'lɑ' LAW rejected); L3_outro_D [kʰeɪ ɛs loʊ] OK (orig 'K S L',
  B/E spelt 'K S L O', C 'K S O L' rejected); SQ3_B (orig spelt 'I-N-G' + question tone). Others = first take.
  S1_2 Tsing Yi [tʃʰɪŋ.jiː], live [lɪv] OK; SH/S4_4 'red' OK, S4_4 'liv' /lɪv/ OK. audio/takes.json maps ids.
  RULE: leading questions bias the model; always ask for blind narrow IPA of a cropped phrase.
- Music: audio/music/theme.wav (60 s, 112 BPM F major) + study_bed.wav (150 s loop bed).
- Expression edits (nano-banana-pro, 2752x1536): design/expr/kayla_{mouth_half,mouth_open,blink,wink,surprised,thinking}.png
- SPRITES DONE (scripts/make_avatar.py): sprites/kayla_base.png + kayla_thinking.png (keyed, crop box 525,0,1939,1440 of
  2560x1440 keyframe => 1414x1440), patches/ sprites/patch_{mouth_half,mouth_open,mouth_o,eyes_blink,eyes_wink,
  eyes_surprised}.png with offsets in sprites/sprites.json ("patches"). Layered: base + eye patch + mouth patch.
  Whole-face swaps rejected (variant eyes differ -> flicker). QA: work/sprite_combos.jpg.
- Seedance refs: audio/refs/{intro 17 s, transition 4 s, outro 10 s}.wav (0.5 s lead + chosen take), refs.json.
  Clips requested 23:48 (seedance-2-5, 720p, keyframe first=last, generate_audio): clips/raw/{intro,transition,outro}_v{1,2}.mp4
  Gesture prompts: intro wave on "Hello, hello, K S Lo students" + fist pump on "Let's level up!"; outro wave only on
  "See you next time! Bye-bye!"; transition nod only.
- Next: SFX synth, renderer (scripts/render.py), keyed clip prep, captions EN/zh, YouTube text.
- CLIPS CHOSEN: intro_v2 (wave on 'Hello, hello, K S Lo students', fist pump on 'Let's level up'; v1 waved late),
  transition_v2, outro_v1 (wave only on final words). Retimed (vocab retime_clip.py) -> clips/retimed/*.mp4, audio =
  refs. QA sheets: clips/qa/*_sheet.jpg, *_gesture.jpg. scripts/clip_qa.py NAME N = reusable QA.
- Voice prep: scripts/prep_voice.py -> audio/vo_prep/<id>.wav (pauses >0.42 s cut to 0.34 s, -18 LUFS, peak cap 0.93, no
  clipping). Body voice 227.0 -> 210.9 s. Word times: scripts/word_times.py (faster-whisper small.en, numpy input; PyAV
  path input breaks) -> audio/vo_prep/words.json. SFX: scripts/make_sfx.py -> audio/sfx/*.wav.
- RENDERER BUILT (render/gl.py, engine.py, scenes.py, build.py; plan render/SCENE_PLAN.md). Timeline 4:56.9.
  build.py: timeline | stills SID t.. | sheet [SID..] (build/stills/sheet_*.jpg) | render [SID..] (6 procs ->
  build/seg, build/video.mp4) | audio (build/mix.wav) | mux (output/Kayla_Grammar_Lab_The_present_and_the_past.mp4).
- QA round 1 fixes needed: para() must glue punctuation after {tracked} words (no 'falling .'); 1.1 'She plays' s
  highlight drawn manually; 1.2 card text 40 px width 780, icons 110; 2.1 irregular cards own row (y 560, sequential x),
  examples lower; level stings XP bar w 600 + label not under Kayla; H bubble font larger (42).

## QA round 2 (20 Oct 2026, 00:13-00:37 HKT) - first full render v1 -> fixes -> v2 render
- gl.para(): tokens with no space before them are GLUED (no 'falling .', 'She play s'); glued tokens never wrap alone.
- Snow White bubbles: 38 px, width 980, bubble_img 1060 -> 2 + 3 lines, no orphans (tested numerically first).
- Quiz blank placeholder = 'm' + answer (spaces -> 'm') + 'm' as ONE token; a multi-word placeholder wrapped across
  lines and the answer overlapped '(sleep)'.
- AUDIO RULE: build.load() duplicates mono to stereo (+3 LU). vo_prep files are -18 mono = -15 stereo, so clip refs
  must be normalised to -15 in the mixer (they were -18 -> 3 dB quieter). Verify with STEMS=1 python3 build.py audio
  (writes build/stem_{voice,sfx,music}.wav). Final: voice -15.7 LUFS everywhere; bed ~18 dB under; bed lifted to 0.8
  during quiz countdowns (t0+0.5..3.85) and 0.75 for the cheat-sheet hold.
- Independent VLM review (manus-analyze-video on the full cut) -> VERIFY EVERY CLAIM with full-res frames: 6 of 10
  were false (no cut-offs, no misspelling, lip-sync fine). Real: 1.2 frequency chips small (30 -> 34 px), 4.1 panel
  empty ~4 s (book frame now enters at 0.6 s), shark flew in from x 1500 outside the comic (now rises at 1130, 'up').
- 'mum' was pronounced American 'mom' [mɑm] in S2_2 (blind IPA). Re-recorded the last sentence only: take A with
  style '; British English pronunciation' -> [mɐm]; 'mumm'/'muhm' respellings gave [mɒm] (rejected). Spliced at the
  pause before 'And' (audio/vo/S2_2_spliced.wav, takes.json S2_2 -> S2_2_spliced), loudness matched (-15.3/-15.4).
  RULE: for British-only words (mum, etc.) add '; British English pronunciation' to the style and IPA-check them.
  ASR (whisper / manus-speech-to-text) always writes 'mom' - never trust ASR for vowel quality.
- Captions: scripts/captions.py (bilingual data CAP per scene; body cues aligned to words.json with difflib; clip
  cues from final-audio ASR segments, filtered by overlap). Re-run manus-speech-to-text on the FINAL audio after any
  timing change, then python3 scripts/captions.py. Outputs output/*.en.srt + *.zh-HK.srt (77 cues).
- YouTube text: scripts/youtube_text.py reads build/timeline.json -> output/YouTube_text.md.

## Teacher feedback round 3 (20 Oct 2026, 01:13 HKT) - TO DO / status
1 Intro: name tag for Kayla 'grammar study buddy', skilfully placed -> above-head game-style nameplate (cat-ear corners), pops on "It's me, Kayla" (~2.8 s into L1).
2 Bubble tails had a horizontal line at the base -> gl.bubble_img = ONE merged mask, distance-transform outline. DONE.
3 Glowing yellow '?' (H + 4.4) too close to panel bottom -> y 945 -> 895.
4 Chips 'every day/often/usually/always' (1.2) and 'yesterday/last week...' (2.1) unexplained -> add label line above chips.
5 2.2: pink bars in situations 1-2 must be vertically centred on the timeline; 'when + short action'/'while + long action' unexplained -> TIP lines under examples 2 and 3.
6 3.2: breathing space right of 'NO -ing ZONE' sign; flying -ing pill must not sit on the sign.
7 3.3: PLOT TWIST! and the next line misaligned -> ROOT CAUSE glow margin; gl.place() now anchors text images by INK (img.info['gpad']). Rule: lines must align.
8 Cheat sheet: align CHEAT SHEET with other items; tile contents messy -> bullet lists, hanging indents, column headings aligned to tile text, equal strip label widths.
9 After 00:18 slow motion -> ROOT CAUSE retime tail stretched (intro x0.27, transition x0.60, outro x0.52). Fix: tail at natural speed and clip trimmed (scripts/retime_clip.py).
10 01:11 'give me five' hand weird -> render/hand.py (tapered fingers, blur-threshold webbing, distance-transform outline). Teacher said v2 'choppy' -> v3 smooth approved by me; show teacher.
11 1.3: remove 'house husband = ...' remark.
12 Video must fade to COMPLETE black before ending (video + audio).
13 (also) Fredoka space is only 0.08 em -> 'NON-ACTION VERBS' reads 'NON-ACTIONVERBS' in pills; widen spaces in Fredoka pills.
### Round 3 implementation (20 Oct 2026, ~01:37 HKT)
- gl.place(): text images carry img.info['gpad'] (text pad + glow pad) -> x/y now = INK box for every anchor. Titles: LEVEL n x104,
  Tense Map x105, PLOT TWIST/line x110, CHEAT SHEET x100 (= PRESENT/PAST labels = strips).
- gl.kf(): Fredoka kerns 'space+V' to 0.085 em -> kerning off for strings containing ' V' (NON-ACTION VERBS).
- gl.bubble_img(): merged mask + distance-transform outline; tails on the straight edge (no seam line).
- render/hand.py: natural smooth hand (tapered fingers, blur-threshold webbing, distance-transform outline, badges inside tips).
- scenes: name_tag() above Kayla (1660, 318 'mb', pops 2.8 s, out dur-0.45); tip_img() TIP lines in 2.2; chip labels
  'Habit words that go with the simple present:' / 'Time words that go with the simple past:'; 2.2 bars centred on line
  (y+123; row 3 pair y+102/y+144), LONG/SHORT labels stacked at x150; '?' y895; NO -ing ZONE sign right ink edge 1114,
  -ing pills shrink (scale 0.3) into it + ring; house-husband remark removed; cheat sheet = bullet_tile() grid
  (TX 280/845, TY 280/498, 540x205, strips X0..1385, equal pill widths, 13 px gaps); L4 dur 6.1, black from 5.4 s.
- build.py: audio cosine fade to silence L4+4.5..5.4 s, silence after.
- Clips retimed with scripts/retime_clip.py (tail natural speed, max_tail 1.2): intro 15.79 s, transition 3.60, outro 9.68.
  Old retimed clips kept in clips/retimed_r1/. TOTAL now 4:55.9.

## Teacher feedback round 4 (20 Oct 2026, 02:01-02:11 HKT) - TO DO / status
Rule: assume viewers have NOT seen the grammar book; on-screen context must be self-explanatory. Video may exceed 5 min;
nothing rushed.
1 H (Snow White hook) + 4.4 (back to Snow White): add labels saying what each bubble is (book p.52 gives no caption;
  bubble 1 = someone talking about a favourite story, bubble 2 = summary of what happens in the story).
2 1.2 simple present: breathing space ABOVE 'Habit words...' label; hold ~1 s+ after the chips (hold 0.8 -> 2.0).
  Also: icons on the right of each card need breathing space from the card's right edge (alarm touches edge).
3 2.1 simple past: more time after the time-word chips (hold -> 2.2).
4 Give-me-five hand: still broken near the thumb -> rewritten as ONE signed-distance field with smooth-min joins
  (render/hand.py; old blur version kept in hand_v3_blur.py). Explain why it was hard.
5 2.2 past continuous: glow highlight on 'was preparing' only (per-line boxes: para boxes['_lines'] DONE in gl.py;
  ParaStates must draw per line); separate the three cases more (cards); more time to read the when/while TIPs
  (voice S2_2p = S2_2 + 0.7 s after 'yesterday' + 1.8 s after 'rained', scripts/insert_pauses.py DONE; end hold 2.4).
  Manual line breaks '\n' now supported in para (DONE): break before the time clause in each example.
6 Countdown '1' (and all circle numbers): optical centring by ink centroid DONE in gl.circle_num.
7 Boss quiz: make the answer words larger (in-blank answer and the answer pill).
8 4.4: breathing space below the tick icon (tick at 1050,945 too close to the panel bottom).
9 2.1 timeline: the cyan line under NOW touched the word -> NOW ink bottom at y 306, line 320-382 (14 px gap).
### Round 4 implementation (02:15 HKT)
- hand.py rewritten as one SDF (palm round-cone + finger round-cones + thumb, polynomial smin); outline smooth.
- scenes.py: ParaStates glow per line; bubbles() context_label() captions + recomputed positions (label 158, bubble1 205,
  label2 below tail, bubble2 +44); 1.2 cards 185 high every 205, label 852, chips 896, icons on a common centre line
  48 px clear of the card edge, hold 2.0; 2.1 hold 2.2; 2.2 voice S2_2p, cards tops [222,460,735] h [218,255,255],
  '\n' before the time clause, hold 2.4; Q answer text/pill 68 px (wrong pill 58), tags below the pill; 4.4 tick 140 at
  (1050, 902). Backups: /tmp/scenes_before_r4.py, /tmp/gl_before_r4.py, render/hand_v3_blur.py.
10 (02:19) Step titles next to number circles used the same pink/yellow as highlighted verbs -> gl.LILAC (192,166,255)
   for use-titles in 1.2, 1.3, 2.1 (FINISHED ACTIONS), 2.2. 3.1 category cards keep their colour coding.
- Quiz: answer text 68 px seated on a common BASELINE 18 px above the blank line (baseline from ink top; text_img's
  soft shadow distorts getbbox bottoms). Strike through the x-height middle (measured: centred).
- Full render 4 started (log /tmp/render4.log). Then: captions.py, youtube_text.py, spot checks.
11 (02:22-02:25) Number circles had rough edges -> teacher: "do this to ALL shapes". gl.py now monkeypatches
   ImageDraw.ellipse/rounded_rectangle/polygon/line/arc on RGB/RGBA images: 4x supersampled coverage, exact Pillow
   semantics at full coverage (RGBA = replace, RGB = paint), premultiplied blend at edges. L/1 masks unchanged.
- ROUND 4 DONE (02:35 HKT): render 5 complete, 302.53 s, -16 LUFS, peak 0.84; ends on full black (max px 0) + silence.
  Captions re-timed from a fresh final-audio ASR (77 cues EN + zh-HK, no overlaps); YouTube chapters regenerated.
  Spot-checked final MP4: hook/4.4 labels, 1.2 + 2.1 holds, 2.2 cards + per-line glow, countdown, quiz baseline,
  big and small hand, AA edges.

## Teacher feedback round 5 (20 Oct 2026, 02:44-02:49 HKT) - status
1 ~02:02 noise after 'yesterday' = tail of '-day' played after the inserted pause (ASR word end 10.32 s, real end
  10.42 s; old cut at the ASR end). scripts/insert_pauses.py now cuts at the quietest frame of the first quiet run
  (< -55 dBFS, >= 40 ms) after the word, 8 ms fades, shifts words whose END is after the cut. S2_2p rebuilt:
  cut 10.47 s; speech ends 10.40, next onset 11.45, gap max -47 dB. DONE
2 ~03:42 'in 2008' underline looked broken = per-word rounded bars meeting (notch, worse with AA). gl.para now draws
  ONE bar per phrase per line (runs). DONE
3 'Richard' looked indented / check ALL scenes: Pillow textbbox() ignores the left side bearing, so text started
  1-4 px in (R/I/L/K 4 px, W 2, A 1), and paras also had a 4 px pad. gl.ink_cols() renders and measures visible ink
  (alpha > 100); para lines start ink-exact at x; text_img crops to ink columns (ink-exact lt/mm); pill text centred
  on ink horizontally, vertically on FONT METRICS (lowercase-only = x-height band, else cap band) so chip rows share
  one baseline ('often' sat low). Audit tool: scripts/align_audit.py (flags 1-14 px near-misses per scene).
4 1.2: more space above 'Habit words...' (cards 178 high every 196 from 228; label 864; chips 906; icons y+92; para y+98).
5 2.2 LONG/SHORT labels at x 149 (bar's visible edge); quiz blank at a line start begins at the text edge.
Backups: /tmp/gl_before_r5.py, /tmp/gl_before_r5b.py, /tmp/scenes_before_r5.py, /tmp/insert_pauses_before_r5.py
TODO: visual check of glow titles (level cards 1.0-4.0, 3.3 PLOT TWIST, C), stills, full render, audio, mux,
  transcription WITH verification (knowledge rule: verify transcription vs script), captions, YouTube text.
- VERIFY (knowledge rule: every transcription must be verified): scripts/verify_transcript.py. Two independent
  transcripts: A manus-speech-to-text (final_audio_transcription_*.json, drives clip captions), B faster-whisper small.en
  word timestamps (build/qa/final_audio_fw_words.json). Checks: 1 A vs script per scene by GLOBAL alignment (segment
  times are too coarse for windows), 2 no words in inserted pauses (B), 3 SRT integrity, 4 cue window words (B),
  5 A vs B agreement. Run after captions.py on every rebuild.
- ROUND 5 DONE (03:04 HKT): render 6, 302.53 s, -16 LUFS, peak 0.843, ends black (mean 0.0). verify_transcript.py:
  ALL CHECKS PASSED (573/580 script words; misses = ASR spellings red/read, ching/Tsing, e d/-ed, 00/o'clock, mom/mum,
  practicing/practising; pauses clean; SRT 77 cues EN=ZH; 77/77 cue windows match; A vs B 98.3%).
  Final voice stem: 'yesterday' ends 121.73 s, next word 122.80 s, gap max -46 dB (was ~-25 dB '-ay' tail).
  NOTE: build/stem_*.wav are only written with STEMS=1 (they were stale from an old build) - regenerate before measuring.

## Teacher feedback round 6 (20 Oct 2026, 03:11 HKT): '-ed' of 'allowed' at 00:28 sounds weird (hook SH)
- SH raw (audio/vo/SH.wav, 24 kHz): ASR hears 'Is that loud?'; envelope: vowel, dip (-29..-44 dB), then a burst back
  to -10 dB (over-released /d/, 'allow-duh'). Blind check: [laʊdᵊ], 2/5.
- New takes (Laomedeia en-GB, context 'Present, past, then present again! Is that allowed? Let's find out!'):
  audio/vo/SH_allowed_A/B/C.wav (B style '; say allowed smoothly with a soft, natural final d'). ASR hears 'allowed'
  in all. Silent cut points (/tmp/sh_cuts.json): SH 8.015/9.035, A 2.675/3.645, B 2.975/4.140, C 2.975/4.105.
  Blind check (leading prompt) rated A 1, B 2, C 1 'over-released' - unverified; RMS shows no second burst.
- Plan: verify with spectral (HF transient) measurement + neutral A/B prompt; splice the chosen sentence into SH
  raw at the cuts, re-run prep_voice + word_times for SH, rebuild timeline/render/audio/mux, captions, verify.
- HF check (4 kHz high-pass, 5 ms): only SH raw has a release transient (+7 dB over vowel HF); A/B/C none. RMS: SH
  release burst -10 dB after a -44 dB closure; A/B/C soft release ~30 dB under the vowel.
- Paired listening test: the analyser answered 'SECOND' 4/4 (position bias) -> re-ran reversed. Only take A beat SH
  in BOTH orders (B, C and A-vs-B split 1-1). RULE: paired AI listening tests must be run in both orders.
- CHOSEN: take A. audio/vo/SH_spliced.wav = SH[0:8.015] + A[2.675:3.645] (-0.3 dB, 5 ms fades) + SH[9.035:];
  takes.json SH -> SH_spliced; vo_prep/SH.wav prepped like prep_voice.main (-18 LUFS), words.json SH updated (ASR now
  'Is that allowed?'), then insert_pauses.py SH SH allowed=0.15 to restore the approved 0.5 s pause before 'Let's'.
  Hook cues use s.w('is', 2) and s.w('lets') only - unaffected. Timeline 302.47 s.
- Splice QA: analyser 'edit heard' claims are unreliable - control on the UNEDITED line also 'heard an edit' (0:07);
  control did flag original 'allowed' as 'allowed-uh' (matches teacher). Same-words spectral tilt: orig -19.5 dB vs
  take A -20.7 dB; 'present...again' -12.9 vs -13.1 -> timbre matched, no EQ needed.
- ROUND 6 DONE (03:27 HKT): render 7, 302.47 s, -16 LUFS, peak 0.845. Final voice stem: 'allowed' at 28.12 s,
  vowel peak -12 dB, loudest point after the vowel -41 dB (old -10 dB burst). verify_transcript.py ALL CHECKS PASSED
  (H 100%; A vs B 98.8%; B vs script 99.0%; 77/77 cues). Captions + YouTube text rebuilt (OFF 292.83).

## Teacher feedback round 7 (20 Oct 2026, 03:30 HKT): '-ed of allowed is now inaudible; I want it audible'
- VERIFIED: take A release -44 dB = 33 dB under the vowel and 14 dB UNDER the music bed (-30 dB) -> masked. Round-6
  QA only tested for 'too strong'; RULE: final consonants must also be checked for audibility over the bed.
- scripts/dcheck.py measure(x, sr, t0, t1): vowel peak/end, release level (full, 2-8 kHz), tail ms (vocalic 'uh').
  Reference (approved voice): S4_4 'finished.' release -12.4 dB vs vowel, HF +8.3, tail 0 (short 5 ms bursts).
- Takes (audio/vo/SH_allowed_*.wav, /tmp/sh_dcheck.json, cuts /tmp/sh_cuts.json):
  orig SH -4.3 dB/HF +10.7/tail 10 (single 10 ms burst at +65 ms, too loud); A -35 (inaudible); D -35; F -40;
  E -8.5/HF +8.6 but 25 ms voiced 'uh' after release (=allow-duh); G -14.4 but a 70 ms breathy noise, not a d.
- BEST: 'tamed original' = approved SH raw with release region (vowel end 8.885 + 57..135 ms = 8.942-9.020 s)
  attenuated, 3 ms ramps: audio/vo/SH_tamed8.wav (-12.3 dB vs vowel, HF +2.7, tail 5 = matches reference) and
  SH_tamed5.wav (-9.3, HF +5.7). No splice; restores approved timing (prepped SH 9.84 s, total ~302.53 s).
- NEXT: masking check in mix context (release vs bed, 2-8 kHz), calibrated blind check (controls: A=inaudible,
  orig=exaggerated), then takes.json SH -> chosen, prep SH only, word timings SH only (NO insert_pauses: original
  pause), rebuild, captions, verify_transcript, STEMS=1 audibility measurement on the final voice/bed stems.
- Mix-context masking (voice gain prep->mix -0.7 dB): release over bed (full band): A -13.7, orig +14.4, tamed5 +9.4,
  tamed8 +6.4. 2-8 kHz bed is near-silent there (A +35 dB) -> HF margin not informative; full band decides.
- Calibrated blind AI check FAILED: analyser said EXAGGERATED for all 8 clips incl. control A (inaudible) -> discarded.
  RULE: AI listener cannot judge consonant audibility; use measurements anchored to an approved reference.
- Reference over-bed: S4_4 'finished.' release +10.7 dB over the bed (full band) at -12.4 dB vs vowel.
- CHOSEN (03:38): SH_tamed5 (original approved take, release region -5 dB): -9.2 dB vs vowel, +9.4 over bed, tail 5 ms.
  tamed8 (-12.2 / +6.4) kept as the softer fallback. takes.json SH -> SH_tamed5; vo_prep/SH.wav 9.84 s; words.json SH
  updated (faster-whisper hears 'loud?' as it did for the approved original - captions use script text). No pause
  insertion. Timeline 302.53 s (= approved timing).
- ROUND 7 DONE (03:45 HKT): render 8, 302.53 s, -16 LUFS, peak 0.843. Final stems: 'allowed' 28.18 s, d release
  28.73 s: -9.3 dB vs vowel, +10.1 dB over music+sfx (reference 'finished.' +10.7), tail 5 ms. verify_transcript ALL
  PASSED (H 100% in A; A vs B 98.2%; B vs script 98.4%; 77/77 cues). Captions + YouTube text rebuilt (OFF 292.897).
  Fallback if teacher finds it too strong: SH_tamed8 (-12.2 / +6.4 over bed).

## Teacher request round 8 (20 Oct 2026, 04:02 HKT): 'give me some choices of the allowed audio'
- scripts/allowed_options.py -> output/allowed_options/Option_1..6.wav (hook context 'then present again? Is that
  allowed? Let's find out.' + real bed, matched to final video loudness) + allowed_options_compare.mp4 (34.1 s, cards).
  1 orig untouched (-4.2 vs vowel/+15.0 over music); 2 orig d -3 dB (-7.2/+12.0); 3 orig d -5 dB = current video
  (-9.2/+10.0); 4 orig d -8 dB (-12.2/+7.0); 5 take E spliced (-7.7/+18.1, voiced 'uh' 10-13 dB under vowel);
  6 take E with 'uh' -10 dB (+43..66 ms after vowel; uh now 16-23 dB under vowel).
- Transcription check: manus STT heard 'Is that allowed? Let's find out' in all 6 + 6x in compare video; faster-whisper
  hears 'loud' for 1-4 (weak initial 'a-' in the original recording since round 1) and 'allowed' for 5-6.
- Fredoka variable axes order = [weight, width] (set_variation_by_axes([wt, 100])).
- To apply a choice: options 1-4 -> raw atten of audio/vo/SH.wav release region 8.942-9.020 (0/3/5/8 dB) as SH_tamedN;
  5-6 -> work/allowed_options/raw_5|6.wav as the SH take. Then prep SH, words SH, timeline, rebuild, captions, verify.

## Teacher decision + request round 9 (20 Oct 2026, 04:12 HKT)
- ACCEPTED current 'allowed' (Option 3 = SH_tamed5). Video final as render 8.
- NEW: explore 'design-led' motion graphics (current looks like PowerPoint). Research: Claude Code videos are web pages
  (HTML/SVG/canvas, GSAP/Remotion/HyperFrames) stepped frame-by-frame in a headless browser + ffmpeg (webflow.com/blog/
  animating-with-claude-and-gsap); Remotion free for individuals + non-profits (remotion.dev/license). Skill rule:
  plain JS/p5.js, no framework, local fonts/assets, time-driven deterministic.
- PROTOTYPE PLAN: redesign scene 1.2 (Simple present uses; t0 51.967, dur 13.567, lead 0.3, voice S1_2) in
  ~/kslo_grammar/proto/: base layer = engine render with els=[] and no panel (bg+header+Kayla identical);
  graphics layer = proto/scene12.html (plain JS seek(t)), Playwright screenshots with alpha; composite; audio = final
  video's audio for that window. Same content/text and same cue words (facts/water/things/live/habits/richard/every).
  Deliver before/after comparison video + still.
- PROTOTYPE DONE (04:29 HKT): proto/scene12.html (plain JS seek(t), grid L116/COL196/R1114, rows 286/470/654 h184,
  title 'Simple present' + 01/03 counter, hairlines, word-mask reveals, highlighter sweeps (ink text), SVG draw-on icons,
  progress rail with spring, focus dim 0.6 of earlier rows until voice_end+0.35, 'every day' shared-element travel to
  tag 1 at every+0.36 (0.45 s), tags 2-4 at every+0.68+k*0.12, exit at dur-0.45). render_gfx.py (Playwright,
  /usr/bin/chromium, omit_background PNGs, 407 frames ~1 min); base_layer.py (engine els=[] panel=False);
  assemble.py (stems voice+music, SFX re-timed: whooshes at rows, soft whoosh 0.22 at travel, pops at 11.74/11.86/11.98;
  gain fitted to final mix k=0.998, residual 2%). Outputs: output/Design-led_prototype_comparison.mp4 (31.17 s),
  output/Design-led_prototype_simple_present.mp4 (13.57 s), output/Design-led_prototype_side_by_side.jpg.
  Verified: frame sheet 0-13.53 s, full-res review frame, ffprobe, transcript (both narrations in order).
  Same scene length kept for fair comparison -> review hold only ~1 s; lengthen in a full rebuild.

## Teacher reply round 10 (20 Oct 2026, 05:53 HKT) to the 3 prototype questions
1 Yes (direction approved: convert more scenes design-led). 2 "What does this mean?" -> asked what FOCUS DIMMING means:
  explain + show side by side (with vs without) and let the teacher choose. 3 Yes (prototype the past continuous scene 2.2 next).
### Built (06:08 HKT)
- proto/lib.js: shared design-led library (palette, easing, spring, masks, line icons incl. clock + bolt, sentence markup with
  {phrase|k} k=v/y yellow, t cyan, p pink, "\n" line break; riseWords, sweep). FONT RULE: window.ready explicitly
  document.fonts.load()s every face BEFORE init() measures text - otherwise widths are measured in the fallback font
  (bug seen: '+' overlapped 'was / were', title-formula gap too small). render_gfx.py asserts window.ready is true.
- proto/base_layer.py SID (generic; exports cues_<sid>.json incl. per-frame panel_right - panel widens 1170->1400 in the
  first 0.5 s of 2.2 as Kayla moves std->small). proto/render_gfx.py SID [--nodim] [times]; comp_stills.py SID suffix times.
- proto/scene22.html: 'Past continuous' title + formula tokens (was / were + verb, -ing docks onto verb at 'plus'),
  3 rows (226/244/236 px, tops 280/506/750) with label, timeline (axis 196-600, bars 226-560 centred on axis), text column
  x 660..1340 (38 px, fits), tips 24 px. Row1 clock + dashed 4:00 marker; row2 bolt + yellow strike dot + ring, legend
  LONG = past continuous / SHORT = simple past; row3 two bars centred on the axis, FRED / HIS MUM labels at 'fred'/'his'.
  Marker colours tie to diagram: pink = past continuous verbs, cyan = time phrase/when/while, yellow = simple past 'rained'.
  All visual events keep the old SFX times -> audio = the final video's own audio for the window (unchanged sound).
- scene12.html honours cues.dim (false = no dimming). Re-rendered 1.2 (dim + nodim) with the font fix.
- proto/assemble_r10.py -> output/Design-led_prototype_past_continuous(_comparison|_no_dimming).mp4,
  output/Focus_dimming_explained.mp4/.jpg (1.2 side by side, still at 10.0 s during row 3).
- ROUND 10 DONE (06:11 HKT): outputs verified (28.23 s x2, comparison 60.5 s, explainer 13.55 s; 1920x1080 30 fps, AAC 48 kHz).
  Comparison transcript = narration twice in order, complete. Explainer panes 896x504 at x 48 / 976, y 380 (gap 32 px).
  assemble_r10.py --dim-only rebuilds only the explainer. ASKED: keep focus dimming or not; approve the 2.2 design;
  then convert the remaining teaching scenes to the shared lib.js system.

## Teacher decisions round 11 (20 Oct 2026, 06:20 HKT)
1 KEEP focus dimming, but add ~1.5 s more after everything returns to full brightness for the review. CHOSEN RULE:
  every dimmed scene holds 2.5 s at FULL brightness after the restore (review starts voice_end+0.35, restore 0.6 s,
  then 2.5 s, then exit 0.45 s) => dur = voice_end + 3.9. (Was: 2.2 ~1.0 s -> +1.5; 1.2 only 0.6 s -> +1.9.)
2 2.2 design APPROVED -> convert ALL remaining graphics scenes to the design-led lib.js system:
  H, M, 1.0/2.0/3.0/4.0 (one level-card template), 1.1, 1.3, 2.1, 3.1, 3.2, 3.3, 4.1, 4.2, 4.3, 4.4, Q0, Q1-Q4 (one
  template), C. Keep as-is: L0 logo opening, L1 intro clip (+name tag), T transition clip, L3 outro clip, L4 end card.
### Conversion plan
- proto/shell.html?s=<name> = shared CSS + lib.js + scenes/<name>.js (init(cues)->{sfx:[[t,name,gain]..]}, seek(t)).
- Generic cues per scene (proto/cues/<sid>.json): all words [w,t0,t1] scene-local, w(phrase,n) in lib.js mirrors
  engine Scene.w normalisation, per-frame panel [right, alpha], Kayla layout per frame, dur/lead/voice_end/fps.
- build integration: for HTML scenes, segment = engine base (els=[], panel False: bg+header+Kayla) + Playwright
  frame (bytes, alpha) composited in memory; sfx from init() -> build/html_sfx/<sid>.json overrides sc.sfx in the mix.
- Keep EVERY approved per-scene fix listed in rounds 3-7 above (content, labels, holds, tips, alignments, no glyph
  arrows/ticks: draw shapes, solid quiz blank lines, lilac step titles, grammar-term recap rule, British spelling).
### Round 11 build (06:23-06:37 HKT)
- INFRA DONE: proto/layer.py (cues_for(scene) live from build; Layer = Chromium page, open(sid,cues)->boot, frame(t)->RGBA;
  html_sfx(); TEMPLATE _level (1.0-4.0) + _quiz (Q1-Q4); NO_HTML=sid,..|all forces old PIL design; hold_override from
  proto/holds/<sid>.txt = seconds after voice). proto/shell.html?s=SID&f=FILE (shared CSS, lib.js, scenes/FILE.js).
  lib.js: cue(), fx(), panelAt(), kaylaAt(), followPanel(), exitLift(), boot(); icons tick/cross/arrow/question/book/star.
  build.py: scenes() applies holds, sets s.html/s.cues and clears els/panel; compose() = engine base + layer;
  render_scene uses one Layer per worker; audio() uses html_sfx (dumped to build/html_sfx.json). Backup /tmp/build_before_r11.py.
- scenes/1.2.js + 2.2.js = ported prototypes (IIFE; cue mapping + SFX recreated). Holds 1.2 & 2.2 -> 3.9 in scenes.py.
  TOTAL 5:05.9 before other conversions.
- proto/DESIGN.md = brief for builders. Builders (background agents, 06:36): A H/4.4/M/1.1 job_vWbNsT4P; B 1.3/2.1
  job_0zJHKXmS; C _level/3.1/3.2/3.3 job_9nDODIjb; D 4.1/4.2/4.3 job_zpE4uPwD; E Q0/_quiz/C job_a09H0xkH.
- NEXT: review each builder's stills; consistency pass; full render; audio (html sfx); mux; captions (re-time: scene
  durations change!), youtube_text, verify_transcript; spot checks.
- BUILDERS DONE (06:55-07:02): all scenes design-led except L0/L1/T/L3/L4 (kept). Holds files: 1.0-4.0 2.0, 1.1 0.9,
  1.3 3.9, 2.1 2.2, 3.1 3.9, 3.2 2.0, 3.3 2.0, 4.1-4.3 1.7, Q0 0.5, Q1-Q4 1.2, C 4.2. TOTAL 5:22.8. Segment render
  0.26 s/frame (30 fps). Review stills: build/qa11/page_*.jpg (/tmp/qa11.py = parallel full-res stills for all html scenes).
- MY REVIEW FINDINGS (07:03-07:08) -> fix list:
  H/4.4 DONE: text overflowed bubble 1 (manual 63-char line) + highlight boxes 74 px tall (inline-block .hl inherited
    box line-height 1.95) + tags over the line above. Fix: lines() helper = one standard sentence per line, 34 px, step 75,
    balanced breaks 2+3 (after 'favourite' / after 'gives' / after 'kiss'), bubbles sized from measured lines
    (top-42, h+64), init THROWS if a line > BW-48 (38 px measured 1060 > 980). Labels y160/448; '?' y842; 4.4 dot 838,
    tick 869, sparkle 901. Backups /tmp/H_before_fix.js /tmp/44_before_fix.js.
  TODO 3.1 + 3.2: sign text 'NO -ING ZONE' -> 'NO -ing ZONE'; 3.1 sign nearly touches '04 / 04' counter (gap ~8 px).
  TODO 2.1: 'REGULAR (-ED)' via CSS uppercase -> keep '-ed' lowercase; 'break→ broke' arrow touches 'break'.
  TODO quiz: Q4 uneven line gaps (blank line taller), 'and saves the planet.' crowds the blank, countdown circle touches
    text -> uniform line rhythm + countdown placed below measured text; Q3 duplicate tags (additive 'Non-action verbs' +
    legacy 'non-action verb'); Q4 4 tags wrap -> drop additive 'Simple present'.
  TODO 4.1 two empty book pages ~3 s before content; 4.3 empty card frame before its content.
  TODO level-card holds 2.0 -> 1.2 (title card, voice ~2 s). Consider larger hand in 1.3 (shown ~90 px).
- FIXES DONE (07:16): 3.1/3.2 sign 'NO -ing ZONE' (3.1 sign placed 40 px left of counter by measurement);
  2.1 'REGULAR (<span text-transform:none>-ed</span>)', pairCard measured (16 px gaps round arrow), pair2 x = pair1 + w + 24;
  quiz: font 52/1.5, .quiz-blank height 48 (was 70 -> taller line), countdown top = max(458, q.bottom+44);
  Q3 tags ['no -ing'] + grammar 'Non-action verbs'; Q4 grammar ['Tenses in stories'] only;
  4.1 book + spine enter at c.once-.62/-.47 (was 0.16 -> empty 4 s); holds 1.0-4.0 -> 1.2. Timeline 5:19.6.
  Backups /tmp/<file>_before_fix. QA stills build/qa12. 3.2 pink ring over sign = intended pulse.
- RENDER 11 started 07:17 (/tmp/render11.log). After: captions.py, youtube_text.py, transcript A+B, verify_transcript.py,
  spot-check frames, black/silent ending check.
- ROUND 11 DONE (07:30 HKT): render 11 = full design-led video, 319.6 s (5:19.6), 1920x1080 30 fps, -16 LUFS, peak 0.835,
  black + silent end. Captions 77 cues EN = ZH, YouTube text rebuilt from timeline. verify_transcript: ALL CHECKS PASSED
  (A vs B 98.1%, B vs script 98.4%; only recogniser spellings mum/mom, practising/practicing, o'clock/00, -ed/e d).
  Bye crop offset = L3 t0 + 6.13 (L3 t0 now 303.833).

## Round 12 (20 Oct 2026, 07:32-07:48 HKT): skill + public asset repo
- Teacher request: record all instructions/requirements/issues/fixes in a skill; save assets PUBLIC on ksloenglish GitHub
  like kslo-vocab-video; include cost-saving instructions without lowering quality.
- Skill: /home/ubuntu/skills/kslo-grammar-video (SKILL.md + references: requirements, corrections_log, voice_and_audio,
  engine_and_design, script_writing, qa_checklist, cost_saving, sharing_and_access; scripts: fetch_assets.sh,
  init_project.sh). Validated. Mirrored in repo at skill/kslo-grammar-video/.
- Repo: https://github.com/ksloenglish/kslo-grammar-video (PUBLIC, plain git, ~154 MB). Release present-and-past-v1 =
  final MP4 (55,475,249 B) + EN/zh-HK SRTs. Anonymous README/release/clone verified.
- Reproducibility test: init_project.sh -> /tmp/gtest from the repo alone: timeline 319.60 s identical; 6 stills
  pixel-identical except sub-pixel anti-aliasing on the C title (visually identical).
- proto/layer.py: Chromium path now _chromium() (CHROMIUM env, /usr/bin/chromium, else Playwright's own).
- scripts/publish_assets.sh stages the repo (cp only; this sandbox has no rsync). gh in an interactive shell can corrupt
  it with colour queries: run gh with '< /dev/null | cat'.

## Teacher feedback round 13 (20 Oct 2026, 13:06 HKT) - TO DO / status
Timeline map (t0): H 19.8, 1.1 45.5, 1.3 68.23, 3.3 183.87, 4.1 203.4, 4.2 215.27, 4.3 232.6, 4.4 244.87, Q1 261.93..Q4 287.73.
1 H (~00:28) + 4.4 (~04:08): '?' too thin/unimpressive -> make prominent. Code: H.js:45 / 4.4.js:46
  icon("question",986,842,118,...). 4.4 later shows mint dot + navy tick (4.4.js:48) -> plan: solid yellow badge with
  bold navy Fredoka '?' (matches the tick badge), glow + gentle bob.
2 1.1 (~00:51): enlarge 'She plays.' to use the empty space.
3 1.3 (~01:11): title formula: 'verb' box + '-ing' box must be ONE compound with no gap (as in past continuous 2.2).
4 3.3 Plot Twist (~03:17): decent, relevant icons for 'using your brain' (was gears) and 'eating' (was sushi line icon);
  keep all 4 card icons one consistent style (bulb, family->own?).
5 4.1 Stories in the past (~03:32): right column icons (book, heart) + PAST TENSES label + was/had chips not prominent,
  misaligned (book x1000, heart x1024, chips off-centre) -> decent icons, one centred axis, bigger chips.
6 4.2 (~03:51): shark line icon messed up -> better, prominent graphics for the beach/shark comic panel.
7 4.3 Careful (~04:00): clapper line icon broken -> decent icon (consider matching icon on OUTSIDE card).
8 Quiz (_quiz.js): countdown numbers more prominent/decent; '1' optically centred; answer text + boxes slightly larger.
Icon sources: Phosphor Icons core v2.1.1 (MIT) duotone SVGs from
  https://cdn.jsdelivr.net/npm/@phosphor-icons/core@2/assets/duotone/<name>-duotone.svg -> design/phosphor/*.svg
  (brain, fork-knife, bowl-food, bowl-steam, lightbulb, key, hand-coins, book-open, book-open-text, heart, film-slate,
  globe-hemisphere-west, fish, sun, umbrella, waves, question, warning, house, hand-heart, chat-circle-dots...). No shark.
  Shark option: Microsoft Fluent Emoji Flat (MIT) https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/Shark/Flat/shark_flat.svg
  -> design/fluent_shark.svg. Tabler outline fish (MIT) -> design/tabler_fish.svg. Noto/Tabler have no shark at those URLs.
Before stills: build/qa13/before/*.png (scripts/qa_stills.py OUTDIR SID:t,t ...).
- R13 progress (13:17): scripts/build_icons.py -> proto/icons.js (PH = Phosphor duotone tint at 0.3 + BOLD outline from
  design/phosphor_bold/<name>.svg [https://cdn.jsdelivr.net/npm/@phosphor-icons/core@2/assets/bold/<name>-bold.svg];
  ART = Fluent flat SVGs, width/height stripped). shell.html loads icons.js before lib.js. lib.js: rgba(hex,a),
  badge(name,x,y,size,col,parent,round) = tinted tile + icon at 0.64*size, popBadge(b,t,t0,d).
  3.3 DONE: lightbulb/brain/key/fork-knife badges 84px at (x+26,y+32), text x+128 (backup /tmp/3.3_before_r13.js).
  4.1 PATCHED: right page axis CX 1034: book-open-text badge 112 @ y404, 'PAST TENSES' centred 28px @ y544,
  rows crown+was (y612) / heart+had (y716): badge 80 + chip 140x66 38px (backup /tmp/4.1_before_r13.js).
  4.2 PLAN: illustrated comic (dusk sky, sun + rays, filled moving wave layers, sand + striped umbrella + towels,
  Fluent shark leaping out between back/front waves with splash at 'spot', comic '!' burst at 'shark'). Fluent shark
  faces left, head top-left, tail bottom (leaping pose).
- R13 progress (13:25): 4.2 DONE comic rewrite (backup /tmp/4.2_before_r13.js): sky gradient CSS, svg layers back(sun+rays rot t*12,
  waves w1/w2) > shark div (ART.shark 276px @792,164; leaps on spot-.14 outBack from +250px, rotate 16->-4, bob) > front (w3, sand,
  towels, umbrella, splash drops+foam at spot+.02) > burst star '!' at 1034,98 on 'shark'. Waves scroll seamlessly (PER 120).
  4.3 DONE (backup /tmp/4.3_before_r13.js): badges film-slate (MINT) @146,344 and globe-hemisphere-west (ORANGE) @746,344, 72px;
  kicker/sub/pills at card+126 (242 / 842); 'came out' left = 842 + was.offsetWidth + 16.
  lib.js: inkGlyph(cv,ch,font,fill,optical,glow) = ink-box centring + optical mass correction; qToken(cx,cy,d) yellow '?' disc;
  animQToken(q,t,t0,out). H and 4.4 use qToken(1045,901,126) (backups /tmp/H_before_r13.js, /tmp/4.4_before_r13.js).
  QUIZ (backup /tmp/_quiz_before_r13.js): ROOT CAUSE of off-centre '1': old drawCountdownDigit used cx-(left+right)/2 (sign error,
  ~5 px right). Now inkGlyph 0.6 optical. Countdown = 168 px navy disc + track + yellow arc running down (dashoffset over t0+.08..+.84),
  centre x 434. Pills 86 px / 54 px font, tick 72, tags 54 px / 24 px, tags top answerY+108, strike baseline 43.
  REMAINING: 1.1 'She plays.' enlarge; 1.3 verb+-ing compound; render QA stills; full render; captions/verify; push repo + skill update.
- R13 completed edits (13:33): 1.1 'She plays.' 68 -> 132 px at L,694 (only 's' highlighted; centred in free band under formulas).
  1.3 '-ing' left = 830 + verb width - 2 (docked like 2.2, shared border, no gap; inner radii already dock to 3). Hand art untouched.
  4.1 left story text 46 -> 44 px at 170,527: ink x 171-678 in page 138-713 (33/35 px padding), vertical centre 604.5 = page centre.
  QA stills build/qa14: H/4.4 '?' token, 3.3 badges, 4.1 right axis, 4.2 shark comic, 4.3 film-slate/globe, quiz discs all OK.
  Measured countdown ink vs disc centre (433.5,541.5): '3' box -1.5 / '2' +0.5 / '1' box -3.5 & mass +2.3 (optical balance);
  vertical all <=0.5 px. align_audit 1.1 4.1 4.3 Q1 Q3: no suspects. Timeline unchanged 319.60 s.
  BASELINE PRESERVED: output/..._past_v1.mp4 + .en_v1.srt + .zh-HK_v1.srt (never overwrite baselines again).
  Full render 13 launched 13:34 -> /tmp/render13.log (render + STEMS=1 audio + mux).
- R13 RENDER 13 FINAL QA (13:50): output/Kayla_Grammar_Lab_The_present_and_the_past.mp4 = v2 (v1 kept as _v1.mp4).
  1920x1080 / 30 fps / 48 kHz stereo / 319.600 s; −16.0 LUFS, peak 0.835, LRA 6.0; end frame max pixel 0; last 0.7 s
  peak −106.5 dB. ASR A 20261020_054716 + bye 054719 (crop L3 t0+6.13 = 309.963); fw cache regenerated.
  verify_transcript: ALL CHECKS PASSED (77 EN = zh-HK cues, timings identical, pauses after 'yesterday'/'rained' clean,
  77/77 cue windows, A/B 98.1 %, B/script 98.4 %; only 'practicing' recogniser spelling). SRT change vs v1 = two
  ASR-timed outro cue ends (≤ 20 ms). YouTube text unchanged. Encoded-frame review build/qa15 (20 frames) all OK;
  4.4 '?'->tick handover at 4.4+10.8 s clean. Benign 'Broken pipe' clip-decoder log lines as in every render.
  NEXT: teacher acceptance -> release present-and-past-v2 (MP4 + SRTs), publish_assets.sh, sync skill copy, push.
