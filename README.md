# K S Lo English: Kayla's Grammar Lab video assets

This repo holds the shared assets and the build engine for the **"Kayla's Grammar Lab"** grammar videos made with the
Manus skill `kslo-grammar-video`. The videos feature **Kayla**, a VTuber-style virtual study buddy, and are for
HKMA K S Lo College students. Clone it in any Manus account to make a new grammar video with the same character,
voice, branding, music, reusable clips and design system.

**Public from 20 October 2026.** Colleagues can browse, download the ZIP or clone without a GitHub account or
owner-specific permission. Public availability does not assign a new blanket copyright licence to these assets;
existing rights and notices are retained.

## Quick start (new grammar topic, in Manus)

1. Add the skill from `skill/kslo-grammar-video/` if the account doesn't have it yet (install the **whole folder**, not
   only SKILL.md). A shared Manus skill attachment can be added directly to **My Skills**.
2. Ask Manus, for example: *"Use the kslo-grammar-video skill to make a Kayla's Grammar Lab video on the passive voice.
   Here are the grammar book pages."* and attach the pages.
3. The skill runs `scripts/fetch_assets.sh` (clones this repo to `~/kslo-grammar-video`), then `scripts/init_project.sh`
   to create a project folder, and follows its approval workflow: body script approval, a stills gallery of every
   scene, then the full render, captions and YouTube text.

A new topic needs **no video generation**: Kayla's intro, transition and outro clips are reused from `library/`.
Only the body script, Kayla's voice lines for the body and the motion-graphics scenes are new.

## Reference video

*Kayla's Grammar Lab - The present and the past* (5:19.6, 1920x1080, 30 fps). The MP4 is attached to the
[latest release](https://github.com/ksloenglish/kslo-grammar-video/releases). Its full production record (decisions,
every defect and fix, scripts, captions, YouTube text and mockups) is in `reference/present_and_past/`.

## Contents

| Folder | What |
|---|---|
| `skill/kslo-grammar-video/` | The Manus skill (instructions, references, scripts). |
| `engine/render/` | Python base layer and build script (`build.py timeline / stills / render / audio / mux`). |
| `engine/proto/` | Design-led motion graphics: `shell.html`, `lib.js`, `layer.py`, one script per scene in `scenes/`, templates `_level.js` and `_quiz.js`, per-scene holds, `DESIGN.md` (design system). |
| `engine/scripts/` | Voice preparation, word timings, pause insertion, captions, YouTube text, transcript verification, alignment audit, publishing. |
| `library/` | **Reusable Kayla clips** (Seedance 2.5): `clips/` lip-retimed `intro_v2`, `transition_v2`, `outro_v1` (used by the engine); `source_clips/` raw outputs; `refs/` the clean voice for each clip. |
| `character/` | Kayla design A ('Neon Pop') master, green-screen keyframe, transparent avatar base, expression variants, the A/B/C design options sheet. |
| `sprites/` | Avatar sprites and face patches (blink, wink, mouth shapes) used for lip-flap without video generation. |
| `design/` | 20 neon icons and the source icon sheet. |
| `audio/` | `music/theme.wav` (signature track), `music/study_bed.wav`, `sfx/` UI sounds. |
| `voice/` | The three auditioned voices (`samples/`) and the chosen library-clip takes. Kayla's voice: Laomedeia. |
| `brand/` | K S Lo English logo (original transparent PNG and `logo_white.png`). Never add a glow or backing behind it. |
| `fonts/` | Fredoka, Nunito and Press Start 2P (open-licence Google Fonts). |
| `reference/present_and_past/` | Complete record of the first video: `NOTES.md`, approved documents, source pages, prepared voice lines, captions, mockups, timeline. |
