# Voice and audio: Kayla's Grammar Lab

## Fixed voice and recording settings

Read the `tts-prompter` skill before a live `generate_speech` call. Use **one call per approved line**; do not record a list in one call.

| Setting | Approved value |
|---|---|
| Voice | `Laomedeia` (Voice 2) |
| Language | `en-GB` |
| Pitch | Natural; **no pitch lift** |
| Base style | `high pitch, bubbly, playful and energetic` |
| Teaching-scene style | `high pitch, bubbly, playful and energetic; clear and unhurried` |
| Long library lines | Base style |
| Audience name in TTS text | Write `K S Low` so 'Lo' is pronounced **low**, never 'law'. Keep `K S Lo` in approved script, captions and screen text. |

The British language setting does **not** prove a British accent. Kayla was selected for the approved character sound, not because the studio voice is guaranteed native-British. Keep Laomedeia unless Mr Kum explicitly approves a change. Do not apply pitch/timbre processing merely to force an accent.

## Before recording

1. Obtain approval of the final spoken body script. Keep approved display/caption wording separate from TTS-only pronunciation text.
2. Run `python3 scripts/tts_lines.py` to create/review `audio/tts_lines.json`. For a new topic, preserve the same `id`, `text`, `approved` and `style` structure.
3. Apply only the known TTS respellings below **before** the first take. Never let a respelling appear on screen or in captions.
4. Generate one full line per call. Save each candidate with a clear take suffix in `audio/vo/`; record the selected take in `audio/takes.json`.

### Recorded respelling map

| Approved text | TTS-only text / treatment |
|---|---|
| K S Lo | `K S Low` |
| Tsing Yi | `Ching Yee`; listen for /tʃɪŋ jiː/ |
| in 2013 | `in twenty thirteen` |
| in 2008 | `in two thousand and eight` |
| plus/with/take/so no `-ing` | `plus ing`, `with ing`, `take ing`, `so no ing` |
| add `-ed` | `add ed` |
| past *read* | `red` |
| *gives, saves and live* | `gives, saves and liv` |
| *Read and was: finished* | `Red and was: finished` |
| *mum* | Do **not** use `mumm` or `muhm`: add `; British English pronunciation` to the style, then listen. |

Use the approved visible spellings (*Tsing Yi*, *read*, *live*, *mum*, `-ing`, `-ed`) in the script, picture and captions. Treat new risky proper names, homographs, final stops and UK/US-sensitive vowels as candidates for an isolated listening test.

## Choose takes by listening, not ASR

ASR can verify approximate words/order, but not a British vowel, lexical stress, naturalness or an unvoiced final consonant. It repeatedly wrote *mum* as *mom*, and may normalise `K S Low` or `red` misleadingly.

1. Check every take for a falling statement ending, clear short function words, even loudness, no extra sounds and no hurried syllables.
2. For a disputed word, crop an isolated phrase with neutral context and request **blind narrow IPA** through `manus-analyze-video`; do not say which result is supposed to be better. Ask a concrete phonetic question.
3. Counter analyser bias: randomise/reverse A/B order, include an unedited control and do not accept a judgement contradicted by the control. The first 'allowed' test said 'SECOND' four times because of position bias; reversing order exposed it.
4. Keep actual recording-waveform boundaries. Do not copy offsets from a different take. Allow head/tail guards when extracting a carrier phrase; reject a cut initial consonant, final syllable or carrier residue.
5. Document uncertainty honestly. Never claim that `en-GB` or an ASR spelling proves British pronunciation.

Useful remedies:

- If an item rises like a question, record a carrier (for example, 'The next phrase is: based on.'), then extract the final phrase with guards; retain only a falling, natural result.
- If one word is wrong in an otherwise approved line, splice a short re-recorded phrase at a quiet boundary with short fades; preserve the approved rest. The reference used this for *mum* before 'And'.
- If a word remains unnatural after a reliable respelling attempt, retain the more natural Laomedeia take and flag the unresolved accent issue rather than replacing her voice.

## Prepare voices and timings

```bash
# From the project root; prepare selected body takes, then regenerate all word cues.
python3 scripts/prep_voice.py
python3 scripts/word_times.py

# Insert a needed reading pause only at quiet audio, without damaging a word tail.
# Usage: BASE OUT word[:occurrence]=seconds ...
python3 scripts/insert_pauses.py S2_2 S2_2p yesterday=0.7 rained=1.8
```

`prep_voice.py` trims edges, shortens only internal gaps longer than 0.42 s to 0.34 s, normalises prepared mono takes to **−18 LUFS** and caps peaks at 0.93 without clipping. It produces 48 kHz `audio/vo_prep/*.wav`; `word_times.py` uses local `faster-whisper small.en` word timestamps to cue motion.

For inserted pauses, let `insert_pauses.py` find the first quiet run below −55 dBFS for at least 40 ms after the recognised word, use 8 ms fades, and shift later word timings. Never cut directly at an ASR word end: in the reference, it left a tail from *yesterday* after the new pause.

## Final-consonant audibility: required for risky endings

A smooth ending can be **too soft over music**, while a strong release can sound like an added vowel. Check both. The reference *allowed* repair chose a tamed original rather than a new take:

| Candidate / reference | Release vs vowel | Over bed | Tail | Decision |
|---|---:|---:|---:|---|
| Original *allowed* | −4.3 dB | +14.4 dB | 10 ms | reject: over-released / 'allow-duh' |
| Take A | −35 dB | −13.7 dB | — | reject: inaudible under bed |
| Approved *finished* reference | −12.4 dB | +10.7 dB | 0 ms | target character |
| `SH_tamed5` | about −9.2 dB | +9.4 dB (+10.1 dB final mix) | 5 ms | **chosen** |
| `SH_tamed8` | −12.2 dB | +6.4 dB | 5 ms | softer fallback |

Measure a candidate before and after the mix. `dcheck.py` is an importable measurement module:

```bash
cd "$P/scripts"
python3 - <<'PY'
import soundfile as sf
from dcheck import measure
x, sr = sf.read('../audio/vo/SH.wav')
print(measure(x, sr, 8.0, 9.2))  # replace bounds with the actual word window
PY
```

It reports vowel peak/end, closure, 2–8 kHz release, full-band release and vocalic-tail length. Compare the final voice/music stems made with `STEMS=1 python3 render/build.py audio`; full-band release **over the actual bed** is decisive where high-frequency bed energy is low. AI listening cannot reliably judge consonant audibility; use measurement anchored to an approved reference, then listen to the assembled mix.

## Reusable Seedance clips and lip timing

The public library already supplies clean reference WAVs and retimed `intro_v2`, `transition_v2` and `outro_v1`. **Do not re-record or regenerate them for a normal unit.** Library speech is generic and must never acquire a title, unit number or new topic wording.

If a clip is explicitly authorised for replacement or fails QA:

1. Record its approved generic line with the fixed settings. Create a reference WAV with 0.5 s lead and padding to a whole second.
2. Generate **two** Seedance variants (`seedance-2-5`, landscape, 720p, generated audio; supplied green keyframe as both first and last frame). Keep the better one only.
3. Require a neutral start/end pose. Gesture only on the matching spoken words; hands stay clasped otherwise. The intro wave is on 'Hello'; the outro wave is only on 'See you next time!'; transition has a small nod only.
4. Retime the **video**, not Kayla's clean voice:

```bash
python3 scripts/retime_clip.py clips/raw/intro_v2.mp4 audio/refs/intro.wav clips/retimed/intro_v2.mp4
# Use --gap 0.12 for a short line when needed; default --max_tail is 1.2.
```

Do not stretch/cut clean audio to make lips fit. The old slow-motion fault came from an over-stretched tail (intro 0.27×; transition 0.60×; outro 0.52×). Preserve a natural-speed tail, trim it, and inspect contact sheets/frame smoothness. Update the public library only after complete clip QA.

## Mix and finish

| Element | Required handling |
|---|---|
| Theme | Use `audio/music/theme.wav` for L0/L1 and outro/end. It is the signature track; do not generate topic-specific replacement music. |
| Study bed | Loop `audio/music/study_bed.wav` under the body with crossfades. Duck under speech; raise only during quiz thinking and cheat-sheet reading holds. |
| SFX | Use the locally supplied logo sting, whooshes, pops, clicks, level-up, tick/countdown, correct chime, buzz, glitch and sparkle only where an explanatory visual cue needs one. |
| Voice balance | The mixer duplicates mono to stereo, so normalise clean clip refs to **−15 LUFS stereo** on placement; otherwise they are 3 dB too quiet. Keep the body bed roughly 18 dB under speech before ducking. |
| Final master | `build.py audio` targets **−16 LUFS** and applies a −1 dBFS-class look-ahead peak limiter (0.89 linear peak). Run with `STEMS=1` when measuring stems. |
| End | Fade picture and sound together to full black/silence; no theme, tail, SFX or encoder residue may remain in the held black. |

After **any** voice/timing change, re-run word timing, timeline/render/audio/mux, fresh final-audio transcription, captions, transcript verification and final listening. Regenerate captions only from the final audio, never from an earlier cue map.
