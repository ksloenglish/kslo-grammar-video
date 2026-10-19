# Renderer scene plan (Style A Neon Stream) - implementation spec

Files: render/gl.py (core graphics: F fonts, place, glow, background, header_img(level,label), pill_img, para (tracked
{words|key}, '→' drawn as arrow), bubble_img, tick/cross/circle_num/arrow_img, icon(name,size)), render/engine.py
(Avatar layered sprite; LAYOUTS std (1660,330,1000) small (1730,700,560) large (1460,110,1350); Scene with
w(phrase,n,end) word cues from audio/vo_prep/words.json (+lead), kay(t0,t1,'eyes'|'pose'|'mouth'|'shake'|'bounce',val),
lay(t,layout) 0.5 s eased, fx(t,sfx,gain); elements E(img,x,y,anchor,t,anim,dur,out,pulse) anims pop/zoom/fade/up/
down/left/right/drop/wipe; Fn(func,t0,dur,t1); Fly(img,p0,p1,t,dur)); exit glitch on lesson layer last 0.22 s;
clips keyed via key_green and placed at sprite position (clip scale 2*h/1440, left = sprite_left - 525*s).
Icons: design/icons/{thermometer,pin,alarm,snowflake,goggles,chart,camera,grumpy,bulb,gears,family,sushi,book,shark,
clapper,lightning,heart,eye,gift,clock}.png (clock shows 4:00). Panel std x 60-1170 y 130-1030; small to x 1400;
large: text x 90-880.
Header chips (recap rule): H none; M "FOUR TENSES"; levels "LEVEL n · <grammar point>"; quiz "QUIZ TIME"; C "SUMMARY";
outro "WELL DONE". Colour: yellow simple, pink continuous, cyan time/signal words, mint tick, red cross; PRESENT tag
mint, PAST tag orange.

Scenes (voice id = vo_prep):
- L0 logo 4.0 s: logo large centre + neon ring + sparkles; series title 1.5 s; unit title 2.0 s. Theme from 0.
- L1 intro clip (clips/retimed/intro_v2.mp4, audio refs/intro.wav), std layout; left title card: series, big unit
  title, level chips appear on 'step by step' (THE PRESENT · THE PAST · NON-ACTION VERBS · TENSES IN STORIES), QUIZ
  chip on 'quiz'. Kayla fades in 0.3 s.
- H hook (SH) std: two speech bubbles (p.52 text); tracked verbs light yellow + PRESENT/PAST tags as named; big '?'
  at 'allowed'; Kayla surprised on 'Is that allowed'.
- M tense map (SM) small: 2x2 tiles rows PRESENT/PAST, cols SIMPLE (yellow, 3 dots) / CONTINUOUS (pink, bar);
  tiles 'simple present · I play' etc.; yellow tiles at 'Yellow', pink at 'Pink'; sparkle 'unlock'.
- n.0 level stings (S1_0..S4_0) large: big 'LEVEL n' neon + name + XP bar; levelup sfx; wink at end; bounce.
- 1.1 (S1_1) std: pill SIMPLE PRESENT; blocks [I / you / we / they]+[play]; [he / she / it]+[play]+'+s' sticker;
  'She plays.' example.
- 1.2 (S1_2) std: 3 cards (thermometer, pin, alarm) + chips every day · often · usually · always.
- 1.3 (S1_3) std: pill PRESENT CONTINUOUS; [am / is / are]+[verb]+'-ing' tag; 'GIVE ME FIVE!' burst with 5 circles;
  5 rows (snowflake, goggles, chart, camera, grumpy) + house-husband gloss.
- 2.1 (S2_1) std: pill SIMPLE PAST; timeline FINISHED ACTIONS dots+ticks; walk +ed walked; break→broke, is→was;
  examples with cyan time words; chips yesterday · last week · two years ago · in 2013.
- 2.2 (S2_2) small: pill PAST CONTINUOUS + [was / were]+[verb]+-ing; 3 timeline rows (clock pin 4:00; long bar +
  lightning short; two parallel bars); when/while cyan; tip chips.
- T transition clip std: 'NICE ONE!' + 'LEVELS 1-2 COMPLETE' XP 50%.
- 3.1 (S3_1) std: title NON-ACTION VERBS + neon sign NO -ING ZONE flicker; 4 bubbles FEELINGS like,want (heart) ·
  THINKING think,know (bulb) · SENSES see,smell (eye) · OWNING have (gift), cued per verb.
- 3.2 (S3_2) std: right sentence + tick; wrong sentence slides, -ing bounce + buzz, red strike + cross; x2; Kayla shake on 'not'.
- 3.3 (S3_3) large->std at 1.2 s: PLOT TWIST banner (glitch); cards THINK = opinion → THINKING = using your brain
  (+example); HAVE = own → HAVING = eating (+example). Kayla surprised 0-1.2 s.
- 4.1 (S4_1) small: storybook panel text; was/had yellow at cues; chip STORY → PAST TENSES.
- 4.2 (S4_2) small: card synopsis = a short summary of a film, play or book; SYNOPSIS / RETELLING → PRESENT TENSES;
  tags lively · dramatic; comic beach panel + shark fin flies in; are resting pink, spot yellow; surprised on 'shark'.
- 4.3 (S4_3) small: screen zone INSIDE THE STORY → PRESENT; outside zone REAL-WORLD FACTS → PAST; sentence; was /
  came out fly outside; saves flies onto screen.
- 4.4 (S4_4) std: bubbles return; tags TRUE NOW / FINISHED / SYNOPSIS (present); '?' -> green tick; wink at end.
- Q0 (SQ0) large: BOSS QUIZ burst + 4 dots + 'Say your answers out loud!'.
- Q1-4 (SQ1-4, voice starts after 0.8 s question + 3 s countdown) large: pill QUESTION n of 4; question with SOLID
  blank line; 3-2-1 ticks; answer pill + mint tick; tags. Q3 'am wanting' struck; Q4 'fly → flies'. Kayla thinking
  pose during countdown, wink on answer.
- C (SC) small, hold 4 s: completed map with uses; strips NON-ACTION VERBS / STORIES; sticker 'Pause & screenshot!'.
- L3 outro clip std: outro card (WELL DONE; six grammar-point chips as output/Outro_card_mockup.jpg).
- L4 end card ~5.5 s: logo large + series + unit + 'See you next time!'; theme ending.
Audio: theme for L0+L1 (ducked under voice), bed for body (looped, ducked), theme 24 s section under outro, theme
ending under end card; SFX per cue; master -16 LUFS.
