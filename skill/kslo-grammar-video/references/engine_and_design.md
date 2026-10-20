# Engine and design system

Use this reference after `scripts/fetch_assets.sh` and `scripts/init_project.sh`. Let `$P` mean the new project directory and `$A` the cloned public asset repository (`~/kslo-grammar-video` by default). Read **`$A/engine/proto/DESIGN.md`** in full before designing or delegating any lesson scene; it is the detailed scene-builder brief copied to `$P/proto/DESIGN.md`.

## What renders a video

The production is a 1920×1080, 30 fps local render. It has two composited graphic layers.

1. **Python base layer** (`render/engine.py`, `render/gl.py`, `render/scenes.py`) renders the violet background, header/logo, lesson panel, Kayla, base-library scenes and sound/timeline metadata.
2. **Design-led HTML layer** (`proto/shell.html?s=<SID>`, `proto/lib.js`, `proto/scenes/<SID>.js`) renders transparent lesson graphics in headless Chromium/Playwright. `build.py` alpha-composites this layer over the base frame.

For design-led scenes, the engine still owns timing, Kayla, background and header, but disables its old PIL lesson graphics/panel. `NO_HTML=sid1,sid2` or `NO_HTML=all` deliberately forces the old PIL body look for a comparison only; it is not a production style choice.

### Kayla without per-scene video generation

Kayla is a layered PNGtuber:

- `sprites/kayla_base.png` or `kayla_thinking.png` is the base.
- Eye and mouth face patches listed in `sprites/sprites.json` create blink, wink, surprise and RMS-driven lip flap without generated video.
- The engine switches mouth from closed/half/open from 30 fps voice RMS, applies deterministic blinks and can cue expressions/pose/shake/bounce.
- Library scenes use keyed, retimed Seedance clips; their clean WAVs are mixed separately.

Use these layouts (Kayla centre x, top y, height; panel right edge):

| Layout | Kayla | Panel / safe lesson region |
|---|---|---|
| `std` | (1660, 330, 1000) | panel ends x=1170; keep lesson graphics left of about x=1130 |
| `small` | (1730, 700, 560) | panel ends x=1400; avoid Kayla's lower-right area |
| `large` | (1460, 110, 1350) | no panel; keep teaching content x=90–760 |
| `off` | no visible avatar | opening/end-card use |

The engine eases layout changes over 0.5 s. Treat per-frame `kaylaAt(t)` and `panelAt(t)` as authoritative, rather than assuming a static safe area.

## Project map

```text
$P/
├── render/              # Python engine: build.py, engine.py, gl.py, scenes.py, hand.py
├── proto/               # HTML scene layer: DESIGN.md, shell.html, lib.js, layer.py
│   ├── scenes/          # <SID>.js; _level.js for 1.0–4.0, _quiz.js for Q1–Q4
│   ├── holds/           # <SID>.txt: seconds after voice ends
│   ├── assets/          # scene-specific exported assets, if truly needed
│   └── cues/            # optional inspection JSON written by layer.py
├── scripts/             # source-topic, TTS, captions and QA helpers
├── audio/               # vo/, vo_prep/, refs/, music/, sfx/, tts_lines.json, takes.json
├── clips/{raw,retimed}/ # library source and retimed keyed clips
├── sprites/, design/, fonts/, brand/
├── build/               # stills, segment MP4s, video.mp4, mix.wav, timeline.json, QA files
├── output/              # final MP4, both SRTs and YouTube text
└── reference/           # copied rebuildable reference-topic source material
```

`init_project.sh` copies the engine/assets and rewrites the original absolute paths. Run its smoke test before changing a topic:

```bash
bash /home/ubuntu/skills/kslo-grammar-video/scripts/fetch_assets.sh
bash /home/ubuntu/skills/kslo-grammar-video/scripts/init_project.sh "$P"
cd "$P/render"
python3 build.py timeline
python3 build.py stills 2.2 27.5
```

## Timing model and build commands

For a voice scene, nominal duration is:

> **lead + prepared voice duration + hold**

The normal lead is 0.3 s. A file `proto/holds/<SID>.txt` overrides the hold **after the voice**. For a focus-dimmed sequential scene, use `3.9` (review restoration + 2.5 s full-brightness review). For a level card use `1.2`; give other text a deliberately chosen reading hold.

Run commands from `$P/render`:

```bash
python3 build.py timeline                         # scene starts, durations, total
python3 build.py stills 2.2 3 15 27.5            # full-resolution key stills
python3 build.py sheet                            # three 640×360 review moments per scene
python3 build.py sheet H 1.2 Q1                  # selected contact sheets
python3 build.py render 2.2                      # changed segment only
python3 build.py render H 1.2 Q1                 # selected segments only
python3 build.py render                           # all segments + concat build/video.mp4
STEMS=1 python3 build.py audio                    # mix + voice/SFX/music stems + timeline
python3 build.py mux                              # AAC MP4 in output/
```

A full reference-sized render took about **10 minutes** using the six-worker render pool (design-led segments about 0.26 s per frame). Re-render only changed SIDs while reviewing; before final delivery run a full build and all QA. If a timing/graphics change affects the final programme, rebuild `audio` and `mux` after the required segment render; do not reuse stale captions/timeline.

## HTML scene contract

Each scene is one deterministic file, `$P/proto/scenes/<SID>.js`:

```js
(() => {
  // scene-local CSS may be injected here
  window.init = function (cues) {
    // build DOM, measure after fonts, register fx(t, name, gain)
    return { /* optional diagnostic info */ };
  };
  window.seek = function (t) {
    // set every style solely from scene-local t
    return true;
  };
})();
```

- `shell.html?s=<SID>` loads `lib.js` then the scene. It accepts `?f=_level` or `?f=_quiz` for shared templates.
- `init(cues)` builds once; `seek(t)` must be a **pure function of time**. No CSS transitions/animations, Date, requestAnimationFrame state, unseeded randomness or frame-order dependency: frames render in parallel/out of order.
- Wait for `window.ready` before measuring text. A fallback-font measurement previously made formula tokens overlap.
- `layer.py` opens Chromium at 1920×1080, checks page/console errors, calls `boot(cues)`, calls `seek(t)`, and takes transparent screenshots. It writes HTML scene SFX into `build/html_sfx.json`; these replace the old scene SFX.
- Generate inspection cues with `python3 ../proto/layer.py cues 2.2`; `CUES` provides `sid`, `dur`, `t0`, `fps`, `lead`, `voice_end`, word timings, per-frame panel/Kayla values, level/label and expression cues.

Useful `lib.js` API: `cue(phrase, n, end)`, `fx(t,name,gain)`, `panel()`, `followPanel()`, `panelAt()`, `kaylaAt()`, `masked()/reveal()`, `sentence()/riseWords()/sweep()`, `icon()/drawIcon()`, `badge()/popBadge()` (solid rounded icon badges), `inkGlyph()` (ink-centred + optically corrected single glyph on a canvas: countdown digits), `qToken()/animQToken()` (bold yellow '?' disc), `hrule()`, easing functions and `exitLift()`. Do not edit shared `lib.js`, `shell.html`, `layer.py`, `build.py`, `engine.py` or `gl.py` for a normal scene task.

## Add or change a scene safely

1. Read the approved body script, the old/reference scene and its current cue words. Render the reference with `NO_HTML=all python3 build.py stills <SID> ...` only to identify content/timing that must survive.
2. Decide whether existing `<SID>.js`, `_level.js` or `_quiz.js` covers it. Add only scene-specific `<SID>.js`, `holds/<SID>.txt` and `assets/<SID>/` files unless an approved engine change is essential.
3. Build all DOM in `init()`. Use `cue()` to time narration-related events. Register SFX in `init()` and make the final `seek()` exit cleanly with `exitLift()`.
4. Measure actual text and icon bounds. Never let content invade Kayla, the header, panel padding or another element. Keep all text/grammar words from the approved script.
5. Run full-resolution still review at entrances, busiest state, review hold and 0.2 s before exit; then render that SID and inspect its motion sheet. Resolve page errors immediately.
6. After approval of a batched complete still gallery, render changed segments, then audio/mux and the full QA checklist.

## Concise design-system summary

- **Grid:** standard glass panel x=60, y=130, height=900; content left x=116; numbered rows at x=116/196; header zone ends around y=140. Keep at least 40 px interior padding.
- **Type:** Fredoka 600 titles (about 58 px); Nunito 800 lesson copy (38–46 px examples; 20–24 px secondary); min 20 px. Use lilac uppercase step labels and the hairline under titles.
- **Colour semantics:** yellow simple tense verbs; pink continuous verb phrases; cyan time/signal expressions; lilac structure; mint/orange PRESENT/PAST; red wrong. Do not use accent colour as decoration or over-highlight a sentence.
- **Motion:** cue on spoken words; title/label masked rises, word-by-word sentences, 0.3–0.42 s highlighter sweeps, draw-on icons, token docking. Use small glows only on the focal item. No spin, wobble or flash.
- **Sequential pedagogy:** numbered rows, a progress rail and focus dimming; restore everything to full brightness for the review hold.
- **Exit:** fade/lift lesson content before segment end; leave the final lesson frame clean enough to chain scenes.

The complete non-negotiable dimensions, palette, safe zones, timing values and scene-builder QA live in **`proto/DESIGN.md`**. Read it rather than duplicating/reinterpreting the system.

## Icons and illustration sources (all MIT, free for colleagues)

`proto/icons.js` is generated by `scripts/build_icons.py` from `design/phosphor/` (Phosphor Icons core v2.1.1
duotone), `design/phosphor_bold/` (bold) and `design/fluent_shark.svg` (Microsoft Fluent Emoji Flat); notices are in
`design/ICON_LICENCES.md`. `publish_assets.sh` and `init_project.sh` carry all of these; a project without `icons.js`
cannot load any scene. Scenes call `icon(name,…)` for line icons and `badge(name,…)` for prominent filled badges;
`ART.shark` is a full illustration. Pick the most literal icon (lightbulb = think/opinion, brain = using your brain,
key = have/own, fork-knife = eating, film-slate = inside a film, globe-hemisphere-west = real world,
book-open-text = story, crown/heart = story details). Never hand-draw icons in SVG paths or use thin outline icons for
an element the viewer must notice: use `badge()`. For a new icon, add the Phosphor SVGs to `design/phosphor*/`, rerun
`build_icons.py`, then check the icon at full resolution.
