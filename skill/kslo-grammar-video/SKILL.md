---
name: kslo-grammar-video
description: Produce, revise and share "Kayla's Grammar Lab" grammar explainer videos for HKMA K S Lo College ("K S Lo students") from teacher-supplied grammar-book pages. One 16:9 video per unit title (never unit numbers), presented by VTuber study buddy Kayla (design A 'Neon Pop', Laomedeia voice), with reusable Seedance intro/transition/outro clips, design-led HTML/Chromium motion graphics, K S Lo English logo at start, body and end, English + written Chinese captions and YouTube text. Assets, engine and every past production record live in the PUBLIC repo ksloenglish/kslo-grammar-video. Use to make a new grammar topic, fix script/voice/pronunciation/layout/timing in an existing one, rebuild, cut production cost, publish assets or set up colleagues. Not for vocabulary videos (use kslo-vocab-video).
---

# Kayla's Grammar Lab (grammar video series)

A new topic needs **no video generation**. Reuse Kayla's library clips, sprites, music, SFX, fonts and engine
from the repo. Only the body script, the body voice lines and the scene scripts are new. Read before acting:

| Read | When |
|---|---|
| `references/requirements.md` | ALWAYS first. Every approved rule is an acceptance criterion |
| `references/cost_saving.md` | ALWAYS before planning. Money-saving rules and the quality gates they must keep |
| `references/script_writing.md` | turning grammar pages into the body script; tables/vocab strategies; timing; approval documents |
| `references/engine_and_design.md` | building scenes, timeline, holds, templates, build commands, project file map |
| `proto/DESIGN.md` (in the project) | before writing or changing any scene script. Design system and builder brief |
| `references/voice_and_audio.md` | recording, pronunciation checks, splicing/pauses, final-consonant audibility, mix |
| `references/qa_checklist.md` | before showing stills, after every render, before delivery |
| `references/corrections_log.md` | any reported defect (check whether it happened before) and after every production |
| `references/sharing_and_access.md` | repo, releases, colleague setup, publishing, `gh` terminal gotcha |

## Setup

```bash
sudo pip3 install -q soundfile scipy pyloudnorm praat-parselmouth opencv-python-headless faster-whisper playwright
ls /usr/bin/chromium || python3 -m playwright install chromium   # layer.py uses /usr/bin/chromium, else Playwright's
S=/home/ubuntu/skills/kslo-grammar-video/scripts
bash $S/fetch_assets.sh                     # public clone -> ~/kslo-grammar-video (no login needed)
P=/home/ubuntu/kslo_grammar_<topic>        # ONE folder per video
bash $S/init_project.sh $P                  # engine + assets + reference topic; old absolute paths rewritten
cd $P/render && python3 build.py timeline   # smoke test: reference topic = 319.60 s
```
`init_project.sh` copies the reference topic (`present_and_past`) so the project builds at once. Replace its topic
content as described below and keep `$P/reference/` for consulting. Never edit the asset-repo copy directly.

## Inputs: ask first (blocking)

1. The grammar-book pages (images/PDF). Use them freely: simplify, reorder, elaborate. Not every example is needed.
2. The exact **unit title** (e.g. "The present and the past"). On-screen title = "Kayla's Grammar Lab" + unit title.
   **Never show unit numbers.**
3. Anything unclear: target form level, preferred terms, length limits. Default length is about 4-5 min. Going longer
   is acceptable when nothing would otherwise be rushed.

## Workflow and approval gates

1. **Plan (no generation).** Draft the running order and the word-for-word body script in
   `scripts/single_script.py` (same data shape as the reference) per `script_writing.md`. Outro-card points = the unit's
   **real grammar points only**. Estimate timing with the measured speaking rate.
2. **GATE 1: script approval.** `python3 scripts/build_body_doc.py`. Show the body-script document (lines, timings,
   on-screen plan) in a blocking ask. Record no voice before approval.
3. **Voice.** `python3 scripts/tts_lines.py` (TTS respellings for recording only, e.g. `K S Low`, `Ching Yee`; add
   new ones to its `RESPELL` list before take 1) → one `generate_speech` call per line with the recorded Kayla
   settings → `prep_voice.py` → `word_times.py`. Blind-check only risky words
   (`voice_and_audio.md`). Fix a single word by splicing a short re-take. Never re-record the library lines.
4. **Scenes.** Edit `render/scenes.py` (scene list, voice ids, layouts, SFX). Write `proto/scenes/<SID>.js` per scene
   from DESIGN.md and the reference scenes. Level cards and quiz questions use `_level.js` / `_quiz.js`. Holds go in
   `proto/holds/<SID>.txt` (focus-dimmed review scenes `3.9`; level cards `1.2`). For 5+ new scenes, parallel
   subagent builders may be used with the DESIGN.md brief and strict per-file ownership.
5. **GATE 2: stills gallery.** Render key moments of EVERY scene (`build.py stills <SID> t ...`). Self-QA them
   (`qa_checklist.md`, incl. `align_audit.py`). Show one batched gallery for teacher review **before the full render**.
   Any new visual direction gets a mockup first.
6. **Render** as background work:
   `cd render && nohup sh -c 'python3 build.py render && python3 build.py audio && python3 build.py mux' &`
   (about 10-15 min, 6 workers). For revisions, re-render only the changed SIDs (`build.py render <SID> ...`), then
   `audio` + `mux`.
7. **QA and copy.** Run every gate in `qa_checklist.md`: encoded-frame spot checks, two transcriptions +
   `verify_transcript.py`, black and silent ending, −16 LUFS. Then `captions.py` (EN + written Chinese zh-HK, same
   timings) and `youtube_text.py` (chapters from the final timeline; never mention AI/Manus).
8. **Deliver** the MP4, both SRTs and `output/YouTube_text.md` as file links. Keep `NOTES.md` current throughout:
   decisions, chosen takes, defects/fixes, metrics, versions. It is the failsafe when context is compacted.
9. **Record and publish** after acceptance. Add this production's defects and fixes to
   `references/corrections_log.md`. Run `scripts/publish_assets.sh`, push, create the release and sync the skill
   copy in the repo (`sharing_and_access.md`).

## Revisions: what to re-run

| Feedback | Fix | Re-run |
|---|---|---|
| On-screen wording, layout, alignment | edit that scene's JS (or scenes.py) | stills → `render <SID>` → `audio` → `mux`; captions only if speech changed |
| More reading time | `proto/holds/<SID>.txt` | `timeline`, render that SID and every later SID (start times shift), `audio`, `mux`, captions, YouTube text |
| Mispronounced or inaudible word | short re-take + splice or tame (`voice_and_audio.md`), update `audio/takes.json` | prep + word times for that line, render that SID, `audio`, `mux`, verification |
| Noise in a pause | silence-seeking `insert_pauses.py` | as above |
| Library clip glitch | `scripts/retime_clip.py` (fixed version) + `clip_qa.py`; Seedance only if unfixable | that clip scene, `audio`, `mux`, republish the clip |
| YouTube copy only | `youtube_text.py` | no render |

Keep the previous MP4 as `_vN` before replacing it.

## Non-negotiables (most-repeated defects)

- Viewers have not read the book. Label every screen so they know what the bubbles, chips and lists are about.
- Highlight only the intended words. Align related lines by visible ink edge. Centre text vertically in pills.
  Leave breathing space round icons and labels. Use solid quiz blank lines, never underscores. Kayla and the header
  never cover content.
- Give at least 1.5 s of reading time after each list or tip. Rushed screens were the most frequent complaint.
- Fade to complete black with silence at the end. Show the logo at start, body (header logo height = divider) and end,
  never with glow or backing.
- Use no Unicode symbols missing from the fonts (glyph check). Use British spelling and single quotes.
- ASR and automated video analysis do not prove pronunciation or layout. Look at full-resolution frames and listen in
  context.

## Scripts

| Location | Purpose |
|---|---|
| skill `scripts/fetch_assets.sh`, `scripts/init_project.sh` | public clone; new project folder with path rewrite |
| `render/build.py` | `timeline`, `stills SID t…` (→ `build/stills/`), `sheet [SID…]` (3-frame contact sheets), `render [SID…]`, `audio` (`STEMS=1` for stems), `mux` |
| `proto/layer.py`, `lib.js`, `shell.html`, `scenes/`, `holds/` | design-led scene layer rendered in headless Chromium |
| `scripts/single_script.py`, `build_body_doc.py`, `build_proposal.py` | script data (single source of truth) and approval documents |
| `scripts/tts_lines.py`, `prep_voice.py`, `word_times.py`, `insert_pauses.py`, `dcheck.py` | voice lines, prep, word timings, pauses, final-consonant audibility |
| `scripts/captions.py`, `youtube_text.py`, `verify_transcript.py`, `align_audit.py` | captions, copy, transcript and alignment verification |
| `scripts/make_avatar.py`, `make_sfx.py`, `retime_clip.py`, `clip_qa.py` | sprites, SFX, library clip retime and QA (rarely needed) |
| `scripts/publish_assets.sh` | stage the public repo from a finished project |
