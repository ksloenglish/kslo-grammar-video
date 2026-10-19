# -*- coding: utf-8 -*-
"""Draft scripts for the K S Lo grammar series with Kayla (v1 draft for approval).

Each scene: (id, label, on_screen, kayla_says, extra_hold_seconds)
Duration estimate = spoken words / WPS + extra hold (animation or thinking time).
"""

WPS = 2.6  # bubbly but clear delivery, measured later from real TTS

LIBRARY = [
    ("L0", "Logo opening (motion graphics, reusable, about 4 s)",
     "The K S Lo English logo pops in at the centre of the neon 'Grammar Lab' background with a short "
     "musical sting, then rises to form one lockup with the series name, an episode pill (e.g. "
     "'S2 · UNIT 8 · EP 1') and the episode topic. No glow or box behind the logo.",
     "(music sting only)", 4.0),
    ("L1", "Intro clip (Seedance, reusable, about 14 s)",
     "The lockup slides to a left-aligned column with a smaller logo; Kayla enters large on the right "
     "with a 'Kayla / Your Grammar Study Buddy' name tag beside her. Wave ONLY on 'Hello, hello, K S Lo "
     "students'; a small fist pump ONLY on 'Let's level up!'; hands clasped at all other times.",
     "Hello, hello, K S Lo students! It's me, Kayla, your grammar study buddy! Grammar can be tricky, "
     "but don't worry. We'll break it down together, step by step. Watch carefully, because there's a "
     "quick quiz at the end. Ready? Let's level up!", 0.8),
    ("L2", "Transition clip (Seedance, reusable, about 4 s)",
     "Kayla slides in from the right between two big sections of an episode; small nod and a thumbs-up "
     "ONLY on 'Nice one!'; then the next section title card bursts in.",
     "Nice one! Now, let's move on to the next part!", 0.6),
    ("L3", "Outro clip (Seedance, reusable, about 11 s)",
     "Kayla slides in beside a 'WELL DONE!' card listing the episode's key points as chips. Hands clasped; "
     "wave ONLY on 'See you next time! Bye-bye!'.",
     "Great work today, K S Lo students! Keep practising, and try using this grammar in your own "
     "writing and speaking. See you next time! Bye-bye!", 0.8),
    ("L4", "End card (motion graphics, reusable, 6 s)",
     "Logo and 'Thanks for studying with Kayla!' only, vertically centred; 3 s hold, 2 s eased fade to "
     "black, 1 s black with the music silent.",
     "(music only)", 6.0),
]

EPISODES = {}

EPISODES[1] = dict(
    title="Simple Present vs Present Continuous",
    source="Page 52 (1.1, 1.2)",
    scenes=[
        ("1.01", "Hook",
         "Split screen. Left card: 'I play football.' with a mini calendar ticking every Saturday. Right card: "
         "'I'm playing football.' with a bouncing ball and a 'NOW' pin. A big '?' pops between them.",
         "Quick question! What's the difference between 'I play football' and 'I'm playing football'? "
         "Let's find out!", 1.0),
        ("1.02", "Simple present: the form",
         "Title card 'SIMPLE PRESENT' slams in (yellow = simple). Word blocks snap together: "
         "[I / you / we / they] + [play]. Then [he / she / it] + [play] and a yellow '+s' sticker flies on: "
         "plays. Mini examples flip in: watch → watches, study → studies.",
         "First up, the simple present. It uses the basic verb, but with he, she or it, don't forget the s! Play becomes plays. "
         "Watch becomes watches.", 2.0),
        ("1.03", "Use 1: facts and general truths",
         "Use card 1 'FACTS & GENERAL TRUTHS' (globe icon). Sentence builds: 'Water freezes at 0°C.' - "
         "'freeze' morphs into 'freezes' (verb highlighted). A thermometer drops to 0 °C and ice crystals form.",
         "We use the simple present for facts and general truths, things that are always true. "
         "Water freezes at zero degrees Celsius.", 1.5),
        ("1.04", "Use 2: things that are true now",
         "Use card 2 'TRUE NOW' (home icon). A simple map of Hong Kong; a pin drops on Tsing Yi. "
         "'I live in Tsing Yi.'",
         "We also use it for things that are true now, like where you live. I live in Tsing Yi.", 1.0),
        ("1.05", "Use 3: regular events and habits",
         "Use card 3 'HABITS & REGULAR EVENTS' (repeat icon). A Monday-to-Friday calendar; an alarm clock "
         "rings at 7:00 on each day (tick, tick, tick). 'Richard wakes up at 7 a.m. every day.' then 'We often "
         "walk our dog in the morning.' Signal-word chips float up: every day · often · usually · always · on Sundays.",
         "And we use it for habits, things that happen again and again. Richard wakes up at seven a.m. every "
         "day. We often walk our dog in the morning. Look out for words like every day, often and usually!", 1.5),
        ("1.06", "Simple present on a timeline",
         "Timeline arrow PAST - NOW - FUTURE. Yellow dots pop on along the whole line. Label: "
         "'always true / again and again'.",
         "On a timeline, the simple present looks like this: true all the time, or again and again.", 1.5),
        ("1.07", "Transition clip (library L2)", "Kayla's reusable transition.", "(library clip)", 4.0),
        ("1.08", "Present continuous: the form",
         "Title card 'PRESENT CONTINUOUS' (pink = continuous). Blocks: [I] + [am] · [he / she / it] + [is] · "
         "[you / we / they] + [are], then a pink '-ing' tag clicks onto the verb: fall → falling, learn → learning.",
         "Now, the present continuous. Here's the recipe: am, is or are, plus a verb ending in -ing. "
         "Like is falling, or am learning.", 2.0),
        ("1.09", "'Give me five!'",
         "A cartoon hand pops up with five numbered fingers; each finger will light up for one use.",
         "It has five main uses. Give me five!", 0.8),
        ("1.10", "Use 1: happening right now",
         "Finger 1 lights: 'RIGHT NOW'. A window with animated falling snow. 'Look! Snow is falling.' "
         "Timeline: a short pink bar right on NOW.",
         "One: actions happening right now, as we speak. Look! Snow is falling.", 1.2),
        ("1.11", "Use 2: temporary situations around now",
         "Finger 2: 'TEMPORARY, AROUND NOW'. Timeline: a longer pink bar stretching a few weeks either side of "
         "NOW. Swimming-goggles icon. 'I am learning to swim at present.' Chips: at present · these days · this term.",
         "Two: temporary situations around now. Maybe not this very second, but these days. "
         "I am learning to swim at present.", 1.2),
        ("1.12", "Use 3: changing situations and trends",
         "Finger 3: 'CHANGES & TRENDS'. A rising arrow chart. 'House husbands are becoming more popular.' "
         "Gloss strip: house husband = a man who stays at home to look after the home and family.",
         "Three: changing situations and trends. House husbands, men who look after the home, are becoming "
         "more popular.", 1.5),
        ("1.13", "Use 4: photos and pictures",
         "Finger 4: 'PHOTOS & PICTURES'. A photo frame drops in with a camera flash; a smiling group. "
         "'Everyone is smiling happily in the photo.' Sticker: 'Great for describing pictures!'",
         "Four: describing photos and pictures. Everyone is smiling happily in the photo. Super useful when "
         "you describe a picture!", 1.2),
        ("1.14", "Use 5: annoying repeated actions",
         "Finger 5: 'ANNOYING HABITS'. 'He is always complaining about his job.' The word 'always' bounces into "
         "place between 'is' and 'complaining'; pattern strip: is + always + verb-ing. Grumbling speech bubbles multiply.",
         "And five: repeated actions that are annoying. We often add always. He is always complaining about "
         "his job. So annoying!", 1.2),
        ("1.15", "Showdown: back to the hook",
         "VS screen. Left: 'I play football.' + timeline of repeated yellow dots = HABIT. Right: "
         "'I'm playing football.' + pink bar on NOW = RIGHT NOW.",
         "So, back to our question! I play football is a habit. I'm playing football means I'm doing it right "
         "now. See the difference?", 1.5),
        ("1.16", "Quiz intro",
         "'QUICK QUIZ' burst; three question dots at the top.",
         "Quiz time! Fill in the blanks, and say your answers out loud!", 0.8),
        ("1.17", "Quiz Q1",
         "'Look! The baby ________ (sleep).' 3-2-1 countdown, then the answer drops in: 'is sleeping' + clue "
         "tag 'Look! → right now'.",
         "Is sleeping! The word look tells us it's happening right now.", 5.0),
        ("1.18", "Quiz Q2",
         "'The sun ________ (rise) in the east.' Countdown, then 'rises' + tag 'fact'.",
         "Rises! It's a fact.", 5.0),
        ("1.19", "Quiz Q3",
         "'My brother ____ always ________ (lose) his keys. It's so annoying!' Countdown, then 'is … losing' + "
         "tag 'annoying habit'.",
         "Is always losing! An annoying habit.", 5.0),
        ("1.20", "Cheat sheet",
         "Two-column summary card. SIMPLE PRESENT (yellow): facts & truths · true now · habits. PRESENT "
         "CONTINUOUS (pink): right now · temporary · trends · photos · annoying 'always'. Sticker: 'Pause & screenshot!'",
         "Here's your cheat sheet. Pause the video and take a screenshot!", 4.0),
    ])

EPISODES[2] = dict(
    title="Simple Past vs Past Continuous",
    source="Page 53 (1.3, 1.4)",
    scenes=[
        ("2.01", "Hook",
         "A clock spins to 8:00 p.m. with a moon outside the window. 'What were you doing at 8 p.m. last night?'",
         "Hey, what were you doing at eight p.m. last night? Hold that thought!", 1.0),
        ("2.02", "Simple past: the form",
         "Title card 'SIMPLE PAST' (yellow = simple). Regular verbs: a yellow '+ed' sticker: walk → walked, "
         "move → moved. Irregular verbs flip like cards: break → broke · come → came · is → was.",
         "The simple past. Most verbs just add -ed. Walk becomes walked. But watch out for irregular verbs, "
         "like break and broke, or is and was!", 2.0),
        ("2.03", "Use: completed actions in the past",
         "Timeline: yellow dots in the PAST zone, each stamped 'DONE'. Three sentences slide in, time phrases in "
         "bold cyan: 'I was born in 2013.' · 'My family moved to Tsing Yi two years ago.' · 'A fire broke out in "
         "my building yesterday.' Chips: yesterday · last week · two years ago · in 2013.",
         "We use the simple past for completed actions in the past. They're finished! I was born in 2013. "
         "My family moved to Tsing Yi two years ago. A fire broke out in my building yesterday. Look for time "
         "words like yesterday, ago and last week.", 1.5),
        ("2.04", "Transition clip (library L2)", "Kayla's reusable transition.", "(library clip)", 4.0),
        ("2.05", "Past continuous: the form",
         "Title card 'PAST CONTINUOUS' (pink). Blocks: [I / he / she / it] + [was] · [you / we / they] + [were], "
         "then the pink '-ing' tag: have → having, wait → waiting.",
         "Next, the past continuous: was or were, plus a verb ending in -ing.", 1.5),
        ("2.06", "Use 1: happening at a time in the past",
         "Timeline: a long pink bar in yesterday's afternoon (barbecue icon sizzling); a clock pin drops at 4:00 "
         "inside the bar. 'We were having a barbecue at four o'clock yesterday.'",
         "Use it for what was happening at a time in the past. We were having a barbecue at four o'clock "
         "yesterday. At four o'clock, the barbecue was still going on.", 1.2),
        ("2.07", "Use 2: interrupted by another action",
         "A long pink bar 'was waiting for the bus' rolls along; a yellow lightning-bolt dot crashes into it: "
         "'it suddenly rained'. Labels: LONG action = past continuous · SHORT action = simple past. Keyword 'when' glows.",
         "Use it for what was happening when another action took place. She was waiting for the bus when it "
         "suddenly rained. The long action uses the past continuous. The short action that interrupts it uses "
         "the simple past.", 1.5),
        ("2.08", "Use 3: two actions over the same period",
         "Two parallel pink bars: 'Fred was watching TV' (TV icon) / 'his mum was preparing dinner' (pot icon). "
         "Keyword 'while' glows between them.",
         "And use it for two actions going on over the same period. Fred was watching TV while his mum was "
         "preparing dinner. Two long actions, side by side!", 1.2),
        ("2.09", "Top tip: when vs while",
         "Two chips: 'when + short action (simple past)' and 'while + long action (past continuous)'.",
         "Top tip! We often use when with the short action, and while with the long action.", 1.5),
        ("2.10", "Back to the hook",
         "The 8:00 p.m. clock returns; a pink bar: 'At 8 p.m. last night, I was watching a cartoon.'",
         "So, what were you doing at eight p.m. last night? Me? I was watching a cartoon!", 1.0),
        ("2.11", "Quiz intro", "'QUICK QUIZ' burst.", "Quiz time! Say your answers out loud!", 0.8),
        ("2.12", "Quiz Q1",
         "'I ________ (do) my homework when the lights went out.' Countdown, then 'was doing' + tag 'long action'.",
         "Was doing! The long action.", 5.0),
        ("2.13", "Quiz Q2",
         "'We ________ (visit) Japan last summer.' Countdown, then 'visited' + tag 'finished'.",
         "Visited! It's finished.", 5.0),
        ("2.14", "Quiz Q3",
         "'While Mum ________ (cook), Dad ________ (wash) the car.' Countdown, then 'was cooking' / 'was washing' "
         "+ tag 'two long actions'.",
         "Was cooking, and was washing! Two long actions.", 5.0),
        ("2.15", "Cheat sheet",
         "SIMPLE PAST (yellow): finished actions · time words: yesterday, ago, last week, in 2013. PAST "
         "CONTINUOUS (pink): in progress at a past time · interrupted (when) · two at once (while).",
         "Here's your cheat sheet. Pause and take a screenshot!", 4.0),
    ])

EPISODES[3] = dict(
    title="State Verbs: When Not to Use -ing",
    source="Page 53 (1.5)",
    scenes=[
        ("3.01", "Hook",
         "Two answer buttons: A 'I am knowing the answer.' / B 'I know the answer.' A timer ring spins.",
         "Which one is correct? I am knowing the answer, or I know the answer?", 2.0),
        ("3.02", "Action verbs vs state verbs",
         "Left: 'ACTION VERBS - things you DO' (run, eat, play) with a running figure. Right: 'STATE VERBS - "
         "feelings, opinions and states' (like, know, have) with a heart and a lightbulb.",
         "Most verbs are action verbs. They're things you do, like run or eat. But state verbs describe "
         "feelings, opinions or states. We don't usually use them in the continuous form.", 1.5),
        ("3.03", "The 'No -ing Zone'",
         "A neon 'NO -ING ZONE' sign lights up. The textbook verbs drop into four colour bubbles: "
         "FEELINGS: like, want · THINKING: think, know · SENSES: see, smell · HAVING: have. Smaller extra chips: "
         "love, need, understand, hear.",
         "Welcome to the No -ing Zone! Like and want are feelings. Think and know are about thinking. See and "
         "smell are senses. And have means owning something.", 1.5),
        ("3.04", "Right and wrong examples",
         "Each correct sentence slides in with a green tick; then its wrong version arrives, the pink '-ing' tag "
         "bounces off the No -ing sign (buzzer), and the wrong sentence is struck through with a red cross: "
         "'I think game shows are exciting.' ✓ / 'I am thinking game shows are exciting.' ✗ · 'Mike has one brother "
         "and one sister.' ✓ / 'Mike is having one brother and one sister.' ✗ · 'The cake smelt great.' ✓ / "
         "'The cake was smelling great.' ✗",
         "I think game shows are exciting. Not I am thinking! Mike has one brother and one sister. Not Mike is "
         "having! The cake smelt great. Not was smelling!", 3.0),
        ("3.05", "Plot twist: -ing changes the meaning",
         "'PLOT TWIST!' banner. A card flips for THINK: opinion (lightbulb) ↔ the action of thinking (turning "
         "gears): 'What is she thinking now?' Then HAVE: own (family icon) ↔ eat (sushi icon): 'We were having "
         "dinner at a Japanese restaurant.'",
         "Plot twist! Some of these verbs can take -ing, but then the meaning changes. They become actions. "
         "What is she thinking now? That's the action of thinking. We were having dinner at a Japanese "
         "restaurant. Here, having means eating!", 2.0),
        ("3.06", "Answer to the hook",
         "Button B glows green: 'I know the answer.' ✓",
         "So, the correct answer is: I know the answer!", 0.8),
        ("3.07", "Quiz intro", "'QUICK QUIZ' burst.", "Quiz time! Say your answers out loud!", 0.8),
        ("3.08", "Quiz Q1",
         "'I ________ (want) a new phone.' Countdown, then 'want' + tag 'feeling = no -ing'.",
         "Want! It's a feeling.", 5.0),
        ("3.09", "Quiz Q2",
         "'Shh! I ________ (think) about the question.' Countdown, then 'am thinking' + tag 'action of thinking'.",
         "Am thinking! It's the action of thinking.", 5.0),
        ("3.10", "Quiz Q3",
         "'This soup ________ (smell) delicious.' Countdown, then 'smells' + tag 'sense = no -ing'.",
         "Smells! It's a sense.", 5.0),
        ("3.11", "Cheat sheet",
         "NO -ING ZONE: like · want · think (opinion) · know · see · smell · have (own). -ING IS OK when it's an "
         "action: thinking = using your brain · having dinner = eating.",
         "Here's your cheat sheet. Pause and take a screenshot!", 4.0),
    ])

EPISODES[4] = dict(
    title="Tenses in Stories",
    source="Pages 52 and 54 (speech bubbles, 2.1-2.3)",
    scenes=[
        ("4.01", "Hook",
         "A storybook flips open with sparkles: 'Once upon a time …'",
         "Once upon a time... Stories always use the past tense, right? Well, not always!", 1.0),
        ("4.02", "Stories that happened: past tense",
         "Storybook page: 'Once upon a time, there was a beautiful princess who had a kind heart. One day, while "
         "she was walking in the forest …' Verbs light up one by one: was, had (yellow, simple past), was walking "
         "(pink, past continuous).",
         "When we write a story that happened in the past, we usually use the past tense. Once upon a time, "
         "there was a beautiful princess who had a kind heart. One day, while she was walking in the forest...", 1.0),
        ("4.03", "Synopses and retelling: present tense",
         "Word card: 'synopsis = a short summary of a film, play or book'. A comic panel: a beach, a shark fin "
         "speeding in, dramatic zoom. 'Dora and Sam are resting on the beach when suddenly, they spot a shark. "
         "It is heading towards them at lightning speed …' Present verbs flash; tag: 'lively · immediate · dramatic'.",
         "But when we write a synopsis, that's a short summary of a film, play or book, or when we retell a "
         "story, we often use the present tense. It makes the story lively and dramatic, as if it's happening "
         "right now! Dora and Sam are resting on the beach when suddenly, they spot a shark. It is heading "
         "towards them at lightning speed!", 1.0),
        ("4.04", "Another synopsis (optional, can be cut to save time)",
         "Fairy-tale panel with an apple and a heart: 'The story reaches its climax when the evil queen gives Snow "
         "White a poisoned apple. Luckily, the prince's kiss saves her and they live happily ever after.'",
         "Here's another one. The story reaches its climax when the evil queen gives Snow White a poisoned "
         "apple. Luckily, the prince's kiss saves her, and they live happily ever after.", 1.0),
        ("4.05", "Inside vs outside the story",
         "A cinema screen. INSIDE THE STORY (the plot) = present tense. OUTSIDE THE STORY (real-world facts) = "
         "past tense. 'The film was a big hit when it came out in 2008. In the film, Harry the superhero saves the "
         "lives of hundreds of thousands of people using magic …' 'was' and 'came out' fly to the outside zone; "
         "'saves' flies onto the screen.",
         "But be careful! Facts that are not part of the plot still use the past tense. The film was a big hit "
         "when it came out in 2008. In the film, Harry the superhero saves the lives of hundreds of thousands "
         "of people using magic. Was and came out are real-life facts. But saves is part of the plot.", 1.5),
        ("4.06", "Talking about a favourite story",
         "Speech bubble: ''Snow White and the Seven Dwarfs' is one of my favourite stories. I first read it when "
         "I was only three.' 'is' tagged 'true now'; 'read' and 'was' tagged 'finished past'.",
         "And when you talk about a story you love, you can mix tenses. Snow White and the Seven Dwarfs is one of "
         "my favourite stories. That's true now. I first read it when I was only three. That's finished.", 1.0),
        ("4.07", "Quiz intro", "'QUICK QUIZ' burst.", "Quiz time! Say your answers out loud!", 0.8),
        ("4.08", "Quiz Q1",
         "Synopsis tag. 'In the film, the hero ________ (fly) to the moon.' Countdown, then 'flies' + tag 'plot'.",
         "Flies! It's the plot.", 5.0),
        ("4.09", "Quiz Q2",
         "'The book ________ (come out) in 2015.' Countdown, then 'came out' + tag 'real-world fact'.",
         "Came out! It's a real-world fact.", 5.0),
        ("4.10", "Quiz Q3",
         "Retelling tag. 'Suddenly, the door ________ (open) and a ghost ________ (walk) in!' Countdown, then "
         "'opens' / 'walks' + tag 'lively retelling'.",
         "Opens, and walks! The present tense makes it dramatic.", 5.0),
        ("4.11", "Cheat sheet",
         "STORY (narrative) → past tense · SYNOPSIS / RETELLING → present tense (lively, dramatic) · REAL-WORLD "
         "FACTS about a story → past tense.",
         "Here's your cheat sheet. Pause and take a screenshot!", 4.0),
    ])


def est(text, hold):
    if text.startswith("("):
        return hold
    return len(text.split()) / WPS + hold


if __name__ == "__main__":
    lib = {k: est(t, h) for k, _, _, t, h in LIBRARY}
    print("library", {k: round(v, 1) for k, v in lib.items()})
    wrap = lib["L0"] + lib["L1"] + lib["L3"] + lib["L4"]
    for n, ep in EPISODES.items():
        body = sum(est(t, h) for _, _, _, t, h in ep["scenes"])
        print(f"Ep{n}: body {body:.0f}s = {int(body//60)}:{int(body%60):02d}; total with wrap {body+wrap:.0f}s = "
              f"{int((body+wrap)//60)}:{int((body+wrap)%60):02d}")
