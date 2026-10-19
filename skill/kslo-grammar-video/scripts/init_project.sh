#!/usr/bin/env bash
# Create a new Kayla's Grammar Lab production folder from the asset repo.
# Usage: bash init_project.sh <PROJECT_DIR> [REFERENCE_TOPIC]
#   PROJECT_DIR      e.g. /home/ubuntu/kslo_grammar_passive (one folder per video)
#   REFERENCE_TOPIC  default present_and_past - its scenes, script data and prepared voice are copied in so the
#                    project is immediately rebuildable (smoke test) and serves as the template to adapt.
# Afterwards replace the topic content (see SKILL.md "New topic"). The reference copy stays in PROJECT/reference/.
set -euo pipefail
P=${1:?project dir}; T=${2:-present_and_past}
A=${KSLO_GRAMMAR_ASSETS:-$HOME/kslo-grammar-video}
[ -f "$A/engine/render/build.py" ] || { echo "Run fetch_assets.sh first ($A missing)"; exit 1; }
[ -e "$P/render" ] && { echo "$P already initialised - refusing to overwrite"; exit 1; }
mkdir -p "$P"/{build,output,clips,audio,design,proto,work}
cp -a "$A/engine/render" "$P/render"
cp -a "$A/engine/scripts" "$P/scripts"
cp -a "$A"/engine/proto/* "$P/proto/"                        # lib.js shell.html layer.py DESIGN.md scenes/ holds/ assets/
cp -a "$A/fonts" "$P/fonts"; cp -a "$A/sprites" "$P/sprites"; cp -a "$A/brand" "$P/brand"
cp -a "$A/design/icons" "$P/design/icons"; cp -a "$A/design/icons_sheet.png" "$P/design/"
cp -a "$A/character/kayla_keyframe_green.png" "$A/character/kayla_avatar_base.png" "$P/design/"
cp -a "$A/character/kayla_master_design_A_neon_pop.png" "$P/design/kayla_A_neon_pop.png"
cp -a "$A/character/expressions" "$P/design/expr"
cp -a "$A/audio/music" "$P/audio/music"; cp -a "$A/audio/sfx" "$P/audio/sfx"
cp -a "$A/library/refs" "$P/audio/refs"
mkdir -p "$P/clips/retimed" "$P/clips/raw"
cp -a "$A"/library/clips/*.mp4 "$P/clips/retimed/"; cp -a "$A"/library/source_clips/*.mp4 "$P/clips/raw/"
R="$A/reference/$T"
if [ -d "$R" ]; then
  cp -a "$R/audio/vo_prep" "$P/audio/vo_prep"
  cp -a "$R/audio/tts_lines.json" "$R/audio/takes.json" "$P/audio/"
  mkdir -p "$P/reference"; cp -a "$R" "$P/reference/$T"
fi
# rewrite the original production paths to this project
grep -rlZ -e "/home/ubuntu/kslo_grammar" -e "/home/ubuntu/kslo-vocab-video/brand" \
     "$P/render" "$P/scripts" "$P/proto" --include='*.py' --include='*.js' --include='*.html' --include='*.sh' 2>/dev/null |
  xargs -0 -r sed -i -e "s#/home/ubuntu/kslo-vocab-video/brand#$P/brand#g" -e "s#/home/ubuntu/kslo_grammar#$P#g"
left=$(grep -rl "/home/ubuntu/kslo_grammar\b" "$P/render" "$P/scripts" "$P/proto" --include='*.py' --include='*.js' 2>/dev/null | wc -l)
echo "initialised $P (reference: $T; leftover old paths: $left)"
echo "Smoke test: cd $P/render && python3 build.py timeline && python3 build.py stills 2.2 27.5"
