# Sharing, access and publishing

## Where things live

| What | Where |
|---|---|
| Skill (instructions, references, scripts) | `/home/ubuntu/skills/kslo-grammar-video/`, mirrored in the repo at `skill/kslo-grammar-video/` |
| Assets, engine, reference records | **PUBLIC** repo `https://github.com/ksloenglish/kslo-grammar-video` (branch `main`) |
| Final videos | GitHub **release assets**, one release per video (tag pattern `<topic-slug>-vN`, e.g. `present-and-past-v1`), with the EN and zh-HK SRT files |
| Live production folder (owner's sandbox) | one folder per video, e.g. `/home/ubuntu/kslo_grammar` (first video) |

The repo was created **PUBLIC on 20 October 2026 at the owner's request**, and anonymous access was verified: raw
README 200, release MP4 200, and a credential-free `git clone`. Public availability does not grant a new blanket copyright
licence. Retain existing rights and notices.

## Colleague setup

1. Install the **whole** skill folder (SKILL.md + references/ + scripts/), either from the shared Manus skill card
   (**Add to My Skills**) or by zipping `skill/kslo-grammar-video/` from the repo. SKILL.md alone is not enough.
2. No GitHub account or integration is needed to read the assets. `scripts/fetch_assets.sh` clones over public
   HTTPS to `~/kslo-grammar-video`. If cloning fails, check the network and the repo's live visibility
   (`gh repo view ksloenglish/kslo-grammar-video --json visibility`) and whether the folder already exists, before asking
   for authentication. Fallback: the ZIP at `https://github.com/ksloenglish/kslo-grammar-video/archive/refs/heads/main.zip`.
3. Writing to the repo (publishing a new video's record) needs `gh` logged in as an account with push rights to
   `ksloenglish`. Colleagues without push rights deliver their files to the owner instead.

## Publishing a finished video (owner)

1. Finish every QA gate (`qa_checklist.md`) and get the teacher's acceptance of the final MP4.
2. Stage: `bash <project>/scripts/publish_assets.sh <project> ~/kslo-grammar-video <topic_slug>`. It refreshes
   reusable assets and engine code and writes `reference/<topic_slug>/` (NOTES.md, docs, captions, mockups, prepared
   voice, chosen raw takes, timeline). It never copies `build/`, frames or `work/`. Edit its hard-coded source-page
   filenames for the new topic's uploads.
3. Review `git status`/`git diff --stat`. Keep every file under 50 MB (GitHub rejects files over 100 MB). Commit, then
   `git push`.
4. Attach the MP4 and both SRTs to a new release:
   `gh release create <slug>-v1 -R ksloenglish/kslo-grammar-video --title "..." --notes "..." <mp4> <en.srt> <zh-HK.srt> < /dev/null | cat`
5. Verify anonymously, e.g. `env -u GH_TOKEN -u GITHUB_TOKEN curl -sIL -o /dev/null -w "%{http_code}" <release URL>`.
6. If the skill changed, copy the validated skill into `skill/kslo-grammar-video/` (exclude `__pycache__`), commit and
   push, and deliver the SKILL.md attachment so the owner can choose **Add to My Skills**. A local edit alone does not
   update the account's stored skill.

## Terminal gotcha

`gh` can emit terminal colour queries that corrupt the interactive shell (stray `;1R`/`rgb:` text, then
`syntax error near unexpected token`). Run `gh` with `< /dev/null | cat` and `NO_COLOR=1`. If a session is already
corrupted, switch to a new session name rather than retrying in it.

## Size rules

Keep the skill package small (scripts and text only, well under 11 MB). Large media (clips, music, sprites, final MP4s)
live only in the repo or its releases, never inside the skill.
