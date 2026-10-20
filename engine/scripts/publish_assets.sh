#!/usr/bin/env bash
# Stage the public asset repo ksloenglish/kslo-grammar-video from a finished project.
# Usage: bash publish_assets.sh [PROJECT] [REPO_DIR] [TOPIC_SLUG]
#   PROJECT    default /home/ubuntu/kslo_grammar          (the production folder)
#   REPO_DIR   default /home/ubuntu/kslo-grammar-video    (git working copy)
#   TOPIC_SLUG default present_and_past                   (reference/<slug>/ = this video's full record)
# Copies only reusable assets + the engine + this topic's reference record. Never copies build/, frames or work/.
# The final MP4 is NOT committed: attach it to a GitHub release (see the skill's sharing_and_access.md).
set -euo pipefail
P=${1:-/home/ubuntu/kslo_grammar}
R=${2:-/home/ubuntu/kslo-grammar-video}
T=${3:-present_and_past}
VOCAB=${KSLO_VOCAB_ASSETS:-/home/ubuntu/kslo-vocab-video}
mkdir -p "$R"
cp_() { mkdir -p "$(dirname "$2")"; cp -a "$1" "$2"; }
rsync_() { rm -rf "$2"; mkdir -p "$2"; cp -a "$1". "$2"/; }   # mirror a folder (no rsync needed)

# --- branding (same logo as the vocab series; never add glow/backing behind it)
mkdir -p "$R/brand"; cp -a "$VOCAB"/brand/* "$R/brand/"

# --- Kayla character (Design A 'Neon Pop' chosen 19 Oct 2026)
mkdir -p "$R/character/expressions"
cp_ "$P/design/kayla_A_neon_pop.png"      "$R/character/kayla_master_design_A_neon_pop.png"
cp_ "$P/design/kayla_keyframe_green.png"  "$R/character/kayla_keyframe_green.png"
cp_ "$P/design/kayla_avatar_base.png"     "$R/character/kayla_avatar_base.png"
cp -a "$P"/design/expr/*.png "$R/character/expressions/"
[ -f "$P/output/Kayla_design_options.jpg" ] && cp_ "$P/output/Kayla_design_options.jpg" "$R/character/design_options_A_B_C.jpg"
rsync_ "$P/sprites/" "$R/sprites/"
mkdir -p "$R/design"; rsync_ "$P/design/icons/" "$R/design/icons/"; cp_ "$P/design/icons_sheet.png" "$R/design/icons_sheet.png"
# MIT icon catalogue sources for proto/icons.js (scripts/build_icons.py) + licence notice
rsync_ "$P/design/phosphor/" "$R/design/phosphor/"; rsync_ "$P/design/phosphor_bold/" "$R/design/phosphor_bold/"
cp -a "$P"/design/fluent_*.svg "$R/design/"; cp_ "$P/design/ICON_LICENCES.md" "$R/design/ICON_LICENCES.md"

# --- reusable Kayla library clips (Seedance 2.5, generated once; NEVER regenerate per topic)
mkdir -p "$R/library/clips" "$R/library/source_clips" "$R/library/refs"
for c in intro_v2 transition_v2 outro_v1; do
  cp_ "$P/clips/retimed/$c.mp4" "$R/library/clips/$c.mp4"         # lip-retimed to the clean voice (used by the engine)
  cp_ "$P/clips/raw/$c.mp4"     "$R/library/source_clips/$c.mp4"  # untouched Seedance output
done
cp -a "$P"/audio/refs/*.wav "$P"/audio/refs/refs.json "$R/library/refs/"

# --- audio: signature theme, study bed, SFX
rsync_ "$P/audio/music/" "$R/audio/music/"
rsync_ "$P/audio/sfx/"   "$R/audio/sfx/"

# --- voice: the three auditioned voices + chosen library takes
mkdir -p "$R/voice/samples" "$R/voice/library_takes"
cp -a "$P"/output/voice_samples/* "$R/voice/samples/" 2>/dev/null || true
for f in L1_intro_C L2_transition L3_outro_D; do cp_ "$P/audio/vo/$f.wav" "$R/voice/library_takes/$f.wav"; done

# --- fonts
rsync_ "$P/fonts/" "$R/fonts/"

# --- engine (code only)
rsync_ "$P/render/" "$R/engine/render/"; rm -f "$R/engine/render/hand_v3_blur.py"
mkdir -p "$R/engine/proto"
for f in lib.js icons.js shell.html layer.py DESIGN.md RESEARCH.md; do cp_ "$P/proto/$f" "$R/engine/proto/$f"; done
rsync_ "$P/proto/scenes/" "$R/engine/proto/scenes/"
rsync_ "$P/proto/holds/"  "$R/engine/proto/holds/"
rsync_ "$P/proto/assets/" "$R/engine/proto/assets/"
rsync_ "$P/scripts/" "$R/engine/scripts/"

# --- reference record for this topic (everything needed to rebuild or audit it)
D="$R/reference/$T"; mkdir -p "$D/docs" "$D/source_pages" "$D/audio" "$D/captions" "$D/mockups"
cp_ "$P/NOTES.md" "$D/NOTES.md"
for f in Kayla_Grammar_Series_Proposal.md Kayla_Single_Video_Plan.md Kayla_Body_Script_v1.md YouTube_text.md; do
  [ -f "$P/output/$f" ] && cp_ "$P/output/$f" "$D/docs/$f"; done
cp -a "$P"/output/*.srt "$D/captions/"
for f in "$P"/output/*.jpg; do cp_ "$f" "$D/mockups/$(basename "$f")"; done
for f in pasted_file_yusG78_image.webp pasted_file_xddcW5_image.webp pasted_file_afHCwG_image.webp; do
  [ -f "/home/ubuntu/upload/$f" ] && cp_ "/home/ubuntu/upload/$f" "$D/source_pages/$f"; done
cp_ "$P/audio/tts_lines.json" "$D/audio/tts_lines.json"
cp_ "$P/audio/takes.json"     "$D/audio/takes.json"
rsync_ "$P/audio/vo_prep/" "$D/audio/vo_prep/"
mkdir -p "$D/audio/vo_chosen_raw"
python3 - "$P" "$D" <<'PY'
import json, os, shutil, sys
P, D = sys.argv[1:]
lines = [l["id"] for l in json.load(open(f"{P}/audio/tts_lines.json"))]
takes = json.load(open(f"{P}/audio/takes.json"))
n = 0
for i in lines:
    src = f"{P}/audio/vo/{takes.get(i, i)}.wav"
    if os.path.exists(src):
        shutil.copy2(src, f"{D}/audio/vo_chosen_raw/{os.path.basename(src)}"); n += 1
print("chosen raw takes copied:", n)
PY
[ -f "$P/build/timeline.json" ] && cp_ "$P/build/timeline.json" "$D/timeline.json"
for f in Design-led_prototype_past_continuous_comparison.mp4 Focus_dimming_explained.mp4; do
  [ -f "$P/output/$f" ] && cp_ "$P/output/$f" "$D/mockups/$f"; done

find "$R" -name '__pycache__' -prune -exec rm -rf {} +
du -sh "$R" --exclude=.git
echo "STAGED -> $R (final MP4: attach as a release asset, not a commit)"
