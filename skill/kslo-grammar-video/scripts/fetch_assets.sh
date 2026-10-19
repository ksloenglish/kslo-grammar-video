#!/usr/bin/env bash
# Clone or update the PUBLIC asset repo ksloenglish/kslo-grammar-video (no GitHub login needed).
# KSLO_GRAMMAR_ASSETS overrides the destination (default ~/kslo-grammar-video).
set -euo pipefail
D=${KSLO_GRAMMAR_ASSETS:-$HOME/kslo-grammar-video}
URL=https://github.com/ksloenglish/kslo-grammar-video.git
if [ -d "$D/.git" ]; then
  git -C "$D" pull --ff-only || echo "WARN: pull failed; using existing copy in $D"
elif [ -e "$D" ] && [ -n "$(ls -A "$D" 2>/dev/null)" ]; then
  echo "Using existing non-git asset folder $D"
else
  git clone --depth 1 "$URL" "$D" || {
    echo "Clone failed. Check network and that $URL is still PUBLIC (gh repo view ksloenglish/kslo-grammar-video --json visibility)."
    echo "Fallback: download https://github.com/ksloenglish/kslo-grammar-video/archive/refs/heads/main.zip and unzip to $D"
    exit 1; }
fi
for f in engine/render/build.py engine/proto/lib.js library/clips/intro_v2.mp4 sprites/kayla_base.png audio/music/theme.wav brand/logo_white.png; do
  [ -f "$D/$f" ] || { echo "MISSING $D/$f"; exit 1; }
done
echo "assets OK: $D"
