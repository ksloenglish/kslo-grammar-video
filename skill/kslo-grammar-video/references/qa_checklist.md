# QA checklist: Kayla's Grammar Lab

Run all applicable gates from the project root (`$P`) or the stated directory. **PASS means the actual final encoded MP4 and its current source assets meet the criterion**; a previous version, a code inspection or an unverified model claim is not PASS. Fix, rebuild downstream assets and re-run affected gates after every change.

## 1. Pre-render content and asset gate

- [ ] **Approved source and title:** teacher has approved the body script, source-page changes, title-only naming, sentence wording and quiz key.
- [ ] **Real grammar recaps:** level labels, header chips, quiz grammar tags, cheat sheet, outro chips and chapters name source grammar points, never teaching devices.
- [ ] **Avatar/library integrity:** use supplied Kayla sprites and generic retimed intro/transition/outro. Check the library clip's pronunciation, gesture timing, neutral endpoints and no slow/stretched tail if it changed.
- [ ] **TTS take audit:** every take has a falling statement tone, clear phrase/function words, natural delivery, no extra sound and measured/risk-listened pronunciation. Do not use ASR as proof of accent/stress/final consonants.
- [ ] **Glyph coverage:** no unsupported Unicode arrow/tick/cross/circled-number glyph is left in lesson text. The renderer's `gl.check_glyphs()` must run on every string; use SVG/drawn primitives instead.

## 2. Scene/build gate

```bash
cd "$P/render"
python3 build.py timeline
python3 build.py stills H 0.2 3 8
python3 build.py stills 2.2 3 15 27.5
python3 build.py stills Q4 0.3 3.0 5.2
python3 build.py sheet H 1.2 2.2 Q1 Q4 C
```

- [ ] **Full-resolution still review:** for every changed scene, inspect 1920×1080 stills at its entrance, busiest state, review hold and 0.2 s before exit. Do not rely only on 640×360 sheets.
- [ ] **Layout PASS:** no crop/overflow; visible-ink left edges line up; at least 16 px between neighbouring elements; text clears panel edges, header and Kayla; text is at least 20 px; no unexpected empty state; final lesson graphic exits cleanly.
- [ ] **Pedagogy PASS:** every book excerpt/diagram/chip group has enough context; intended words only are highlighted; label and colour meanings agree; final readable material receives its required hold.
- [ ] **Quiz PASS:** blank is one continuous solid line; answer baseline/pill are optically centred; countdown digits are ink-centred and clear of question text; tags neither duplicate nor wrap/crop.
- [ ] **Design-led page PASS:** no browser page or console errors. `layer.py` must fail on an `init/seek`/font readiness error; do not ignore warnings.

### Alignment audit

```bash
cd "$P"
python3 scripts/align_audit.py
# Investigate every 1–14 px near-miss reported; rerun selected scenes if needed.
```

- [ ] **Alignment PASS:** every flagged near-miss is either corrected or visibly intentional; do not dismiss text-vs-shape offsets without full-resolution review.

### Segment smoothness/contact sheets

```bash
cd "$P/render"
python3 build.py render 2.2 Q4
SEG=$(find build/seg -maxdepth 1 -name '*_2.2.mp4' -print -quit)
ffmpeg -y -v error -i "$SEG" \
  -vf "fps=2,scale=480:-1,tile=5x5:padding=8" -frames:v 1 build/stills/2.2_motion_sheet.jpg
```

- [ ] **Motion PASS:** entrances/reveals occur on the intended cue; no CSS-frame flicker, fallback font, motion jump, surprise overlap or unreadable rapid exit.
- [ ] **Focus-dimming PASS:** earlier rows dim only after the next begins; all return to full brightness at review; dimmed scenes have `voice_end + 3.9 s` duration (2.5 s clear review after restore).

## 3. Retimed-library clip gate (only if clip/assets changed)

```bash
cd "$P"
python3 scripts/clip_qa.py intro 12
python3 scripts/clip_qa.py transition 12
python3 scripts/clip_qa.py outro 12
# Make a dense manual motion sheet around any gesture or suspected repeat/freeze.
ffmpeg -y -v error -i clips/retimed/intro_v2.mp4 \
  -vf "fps=8,scale=320:-1,tile=8x6:padding=4" -frames:v 1 build/stills/intro_motion.jpg
# Check for duplicate/frozen frames; compare decoded and mpdecimate counts.
ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames -of default=nw=1 clips/retimed/intro_v2.mp4
ffmpeg -v warning -i clips/retimed/intro_v2.mp4 -vf mpdecimate -an -f null -
```

- [ ] **Clip PASS:** green keys cleanly; framing is stable; no arm snap/size jump; gesture occurs only on its words; clean voice is uncut and lip timing plausible; no slow-motion tail or unintentional repeated/frozen frames. Check intro/outro phrase positions with a gesture contact sheet.

## 4. Full render, encode and frame-spot gate

```bash
cd "$P/render"
python3 build.py render
STEMS=1 python3 build.py audio
python3 build.py mux

# Pull encoded-video frames, including beginning/body/quiz/outro/end.
mkdir -p "$P/build/qa/encoded_frames"
ffmpeg -y -v error -ss 00:00:00 -i "$P/output/Kayla_Grammar_Lab_The_present_and_the_past.mp4" \
  -vf "fps=1/5,scale=960:-1" "$P/build/qa/encoded_frames/frame_%03d.jpg"
```

- [ ] **Encode PASS:** final is 1920×1080, 30 fps and has the intended AAC soundtrack; segment joins have no visual/aural discontinuity.
- [ ] **Encoded-frame PASS:** inspect frames from the actual MP4 at opening, every scene type, all text-heavy holds, every quiz countdown/answer, outro and fade. No clipping, wrong font, chroma edge, logo backing/glow, avatar/text overlap or missing/cropped label is visible.

## 5. Audio, transcript and captions gate

```bash
cd "$P"
# Extract current final audio, make an independent final-audio transcription, then captions.
mkdir -p build/qa
ffmpeg -y -v error -i output/Kayla_Grammar_Lab_The_present_and_the_past.mp4 \
  -vn -ac 1 -ar 16000 build/qa/final_audio.wav
rm -f build/qa/final_audio_fw_words.json      # CACHED transcript B: delete after EVERY render or B is stale
manus-speech-to-text build/qa/final_audio.wav
# Outro clip captions need their own ASR crop starting at L3 t0 + 6.13 s (captions.py reads bye_transcription_*.json)
OFF=$(python3 -c "import json;print([d for d in json.load(open('build/timeline.json')) if d['sid']=='L3'][0]['t0']+6.13)")
ffmpeg -y -v error -ss $OFF -i build/qa/final_audio.wav -t 3.6 build/qa/bye.wav && manus-speech-to-text build/qa/bye.wav
python3 scripts/captions.py
python3 scripts/verify_transcript.py

# Final programme loudness/peak inspection (the build log must also report −16 LUFS).
ffmpeg -v info -i build/mix.wav -af ebur128=peak=true -f null - 2>&1 | tail -45
```

- [ ] **Two-transcription PASS:** `verify_transcript.py` reports **ALL CHECKS PASSED**: final ASR A vs approved script, independent local `faster-whisper small.en` B for word windows/pauses, A/B agreement and B/script agreement. Investigate every low scene/cue rather than normalising a spoken error away.
- [ ] **Pause PASS:** no transcript word appears within each inserted-pause window; listen to the actual mixed audio for tail/noise.
- [ ] **Caption PASS:** English and `zh-HK` cue counts equal the approved caption data; timings are identical, increasing and non-overlapping; English cue text equals approved script; every cue lies within its scene. Chinese is Traditional standard written Hong Kong Chinese and retains English example sentences in English.
- [ ] **Audio PASS:** final mix is **−16 LUFS**; limiter peak is no more than 0.89 (about −1 dBFS); voice is intelligible over bed/SFX. Check selected final consonants over the *mixed* bed, using freshly created `build/stem_*.wav` from `STEMS=1`, where relevant.

## 6. Final black-and-silent end gate

```bash
cd "$P"
ffmpeg -y -v error -sseof -0.5 -i output/Kayla_Grammar_Lab_The_present_and_the_past.mp4 \
  -frames:v 1 build/qa/end_frame.png
ffmpeg -v info -sseof -0.7 -i output/Kayla_Grammar_Lab_The_present_and_the_past.mp4 \
  -vn -af astats=metadata=1:reset=0 -f null - 2>&1 | tail -35
```

- [ ] **End PASS:** visually inspect `end_frame.png`: every pixel is black. `astats` reports silence/no non-zero programme tail over the final black hold. Confirm by listening through EOF. The music must not resume or leave a fade tail.

## 7. Delivery gate

- [ ] Final MP4, `.en.srt`, `.zh-HK.srt` and `YouTube_text.md` are current and correspond to the final timeline.
- [ ] YouTube title/description use the actual title, final chapter times, real grammar-point list, caption notice and appropriate tags. They do not mention AI, Manus or generation.
- [ ] Record the exact render/version, changed SIDs, QA evidence and unresolved caveats in `NOTES.md` before context is compacted or the project is handed over.

## Known benign log lines and revision evidence (added round 13)
- Three `Broken pipe` / `Error muxing a packet` lines after the clip scenes are the library-clip decoder being closed
  once enough frames are read; they appear in every accepted render. Any other error or Traceback fails the build.
- After a revision render, compare SRTs with `_vN`: only the ASR-timed clip cues may move (≤ 50 ms). Check the
  changed animation in the **encoded** MP4 (e.g. a 0.1 s crop strip of a token hand-over), not only stills.
- Give the teacher one labelled overview image (one encoded frame per requested change, numbered as in the request)
  with the MP4 and SRT links.

## Glyph-centring and focal-signal checks (added round 13)
- Countdown digits and any single glyph in a disc: measure ink box and centre of mass in the rendered PNG; box/mass
  within ±4 px horizontally of the disc centre, vertical ≤ 1 px.
- A key signal (question mark, tick, warning) must be a solid badge/token readable at a glance in a 960 px thumbnail.
- Adjoining formula chips: zero visible gap at full resolution.
- Every icon checked at full resolution for broken paths; prefer MIT catalogue badges.
