# -*- coding: utf-8 -*-
"""English + Traditional Chinese (standard written Chinese) SRT captions for Kayla's Grammar Lab - The present and
the past. Body cues are timed from word timestamps (audio/vo_prep/words.json) via sequence alignment; the three library
clips use the final-audio ASR segments. Chinese cues: explanation in written Chinese, English examples kept in English
(a '\n' in a Chinese cue forces the line break between explanation and example)."""
import json, glob, re, difflib, sys
sys.path.insert(0, "/home/ubuntu/kslo_grammar/render")
ROOT = "/home/ubuntu/kslo_grammar"

CAP = {
 "L1": [("Hello, hello, K S Lo students!", "K S Lo 的同學們，大家好！"),
        ("It’s me, Kayla, your grammar study buddy!", "我是 Kayla，你們的文法學習夥伴！"),
        ("Grammar can be tricky, but don’t worry. We’ll break it down together, step by step.",
         "文法有時候會比較難，但不用擔心。\n我們會一起逐步拆解。"),
        ("Watch carefully, because there’s a quick quiz at the end.", "請留心觀看，因為最後會有一個小測驗。"),
        ("Ready?", "準備好了嗎？"),
        ("Let’s level up!", "我們一起升級吧！")],
 "H": [("Look! Is, read, was, reaches, gives…", "看！is、read、was、reaches、gives……"),
       ("Present, past, then present again!", "現在、過去，然後又是現在！"),
       ("Is that allowed?", "這樣可以嗎？"),
       ("Let’s find out!", "我們來看看吧！")],
 "M": [("Here’s our Tense Map.", "這是我們的時態地圖。"),
       ("Yellow is simple: facts, habits and finished actions.", "黃色代表簡單式：事實、習慣和已完成的動作。"),
       ("Pink is continuous: actions in progress.", "粉紅色代表進行式：正在進行的動作。"),
       ("Let’s unlock them!", "我們來逐一解鎖吧！")],
 "1.0": [("Level one: the present!", "第一關：現在時態！")],
 "1.1": [("The simple present uses the basic verb.", "簡單現在式使用動詞原形。"),
         ("With he, she or it, add an s.", "主語是 he、she 或 it 時，動詞要加 s。"),
         ("She plays!", "She plays!")],
 "1.2": [("Use it for facts. Water freezes at zero degrees Celsius.", "用來表達事實。\nWater freezes at zero degrees Celsius."),
         ("Things that are true now. I live in Tsing Yi.", "表達現在真實的情況。\nI live in Tsing Yi."),
         ("And habits. Richard wakes up at 7 a.m. every day.", "還有習慣。\nRichard wakes up at 7 a.m. every day.")],
 "1.3": [("The present continuous: am, is or are, plus -ing.", "現在進行式：am、is 或 are，加上 -ing。"),
         ("It has five uses. Give me five!", "它有五種用法。來擊個掌吧！"),
         ("One: right now. Look! Snow is falling.", "一：此刻正在發生的事。\nLook! Snow is falling."),
         ("Two: temporary situations. I am learning to swim at present.", "二：暫時的情況。\nI am learning to swim at present."),
         ("Three: changing trends. House husbands are becoming more popular.",
          "三：轉變中的趨勢。\nHouse husbands are becoming more popular."),
         ("Four: photos. Everyone is smiling happily in the photo.", "四：描述照片。\nEveryone is smiling happily in the photo."),
         ("Five: annoying habits, with always. He is always complaining about his job!",
          "五：令人厭煩的習慣，配合 always 使用。\nHe is always complaining about his job!")],
 "2.0": [("Level two: the past!", "第二關：過去時態！")],
 "2.1": [("The simple past is for finished actions.", "簡單過去式用來表達已完成的動作。"),
         ("Most verbs add -ed, but some are irregular.", "大部分動詞加 -ed，但有些是不規則動詞。"),
         ("I was born in 2013.", "I was born in 2013."),
         ("A fire broke out in my building yesterday.", "A fire broke out in my building yesterday.")],
 "2.2": [("The past continuous: was or were, plus -ing.", "過去進行式：was 或 were，加上 -ing。"),
         ("Use it for an action in progress at a past time.", "用來表達過去某一時間正在進行的動作。"),
         ("We were having a barbecue at four o’clock yesterday.", "We were having a barbecue at four o’clock yesterday."),
         ("For a long action interrupted by a short one.", "表達一個較長的動作被一個短暫的動作打斷。"),
         ("She was waiting for the bus when it suddenly rained.", "She was waiting for the bus when it suddenly rained."),
         ("And for two actions at the same time.", "以及同時進行的兩個動作。"),
         ("Fred was watching TV while his mum was preparing dinner.", "Fred was watching TV while his mum was preparing dinner.")],
 "T": [("Nice one!", "做得好！"), ("Now, let’s move on to the next part!", "現在，我們進入下一部分吧！")],
 "3.0": [("Level three: non-action verbs!", "第三關：非動作動詞！")],
 "3.1": [("Non-action verbs describe feelings, opinions or states.", "非動作動詞描述感受、意見或狀態。"),
         ("We don’t usually use them with -ing.", "我們通常不會把它們配合 -ing 使用。"),
         ("Like, want, think, know, see, smell and have.", "例如 like、want、think、know、\nsee、smell 和 have。")],
 "3.2": [("I think game shows are exciting. Not I am thinking!", "I think game shows are exciting.\n不是 I am thinking！"),
         ("Mike has one brother and one sister. Not Mike is having!", "Mike has one brother and one sister.\n不是 Mike is having！")],
 "3.3": [("Plot twist!", "劇情逆轉！"),
         ("Some of these verbs can take -ing when they’re actions.", "這些動詞表示動作時，有些可以加上 -ing。"),
         ("What is she thinking now? That’s the action of thinking.", "What is she thinking now?\n這是指「思考」這個動作。"),
         ("We were having dinner at a Japanese restaurant.", "We were having dinner at a Japanese restaurant."),
         ("Here, having means eating!", "這裏的 having 是「吃」的意思！")],
 "4.0": [("Level four: tenses in stories!", "第四關：故事中的時態！")],
 "4.1": [("Stories that happened in the past usually use past tenses.", "在過去發生的故事通常使用過去時態。"),
         ("Once upon a time, there was a beautiful princess who had a kind heart…",
          "Once upon a time, there was a beautiful princess who had a kind heart…")],
 "4.2": [("But in a synopsis, a short summary of a film, play or book,", "但在劇情簡介（即電影、戲劇或書本的簡短摘要）中，"),
         ("or when we retell a story, we often use present tenses.", "或在複述故事時，我們通常使用現在時態。"),
         ("It’s more dramatic!", "這樣更具戲劇性！"),
         ("Dora and Sam are resting on the beach when suddenly, they spot a shark!",
          "Dora and Sam are resting on the beach when suddenly, they spot a shark!")],
 "4.3": [("Careful! Real-world facts stay in the past.", "小心！現實世界中的事實仍然使用過去時態。"),
         ("The film was a big hit when it came out in 2008.", "The film was a big hit when it came out in 2008."),
         ("In the film, Harry the superhero saves thousands of lives.", "In the film, Harry the superhero saves thousands of lives.")],
 "4.4": [("Back to Snow White!", "回到白雪公主的故事！"),
         ("Is: true now. Read and was: finished.", "is：現在真實的情況。\nread 和 was：已完成的動作。"),
         ("Reaches, gives, saves and live: the story, told in the present.",
          "reaches、gives、saves 和 live：\n用現在時態講述的故事情節。"),
         ("Every tense has a reason!", "每個時態都有它的原因！")],
 "Q0": [("Boss quiz! Say your answers out loud!", "終極測驗！大聲說出你的答案！")],
 "Q1": [("Is sleeping! It’s happening right now.", "is sleeping！這件事此刻正在發生。")],
 "Q2": [("Was doing! A long action, interrupted.", "was doing！一個較長的動作被打斷了。")],
 "Q3": [("Want! It’s a non-action verb, so no -ing.", "want！它是非動作動詞，所以不加 -ing。")],
 "Q4": [("Flies! In a synopsis, we use the present.", "flies！在劇情簡介中，我們使用現在時態。")],
 "C": [("Here’s your cheat sheet.", "這是你的重點筆記。"), ("Pause the video and take a screenshot!", "暫停影片並截圖吧！")],
 "L3": [("Great work today, K S Lo students!", "K S Lo 的同學們，今天做得很好！"),
        ("Keep practising, and try using this grammar in your own writing and speaking.",
         "繼續練習，並嘗試在寫作和說話時\n運用這些文法。"),
        ("See you next time! Bye-bye!", "下次見！拜拜！")],
}

norm = lambda w: re.sub(r"[^a-z0-9]", "", w.lower())


def toks(s):
    return [t for t in (norm(w) for w in re.split(r"[\s\-]+", s)) if t]


def body_cues(sid, voice, t_base, words):
    chunks = CAP[sid]
    st, owner = [], []
    for k, (en, _) in enumerate(chunks):
        for t in toks(en):
            st.append(t); owner.append(k)
    asr = [norm(w[0]) for w in words]
    sm = difflib.SequenceMatcher(a=st, b=asr, autojunk=False)
    hit = {}
    for a, b, n in sm.get_matching_blocks():
        for i in range(n):
            hit.setdefault(owner[a + i], []).append(b + i)
    out = []
    for k in range(len(chunks)):
        if k not in hit:
            raise ValueError(f"{sid} chunk {k} not aligned: {chunks[k][0]}")
        i0, i1 = min(hit[k]), max(hit[k])
        out.append((t_base + words[i0][1], t_base + words[i1][2], *chunks[k]))
    return out


def clip_cues(sid, t0, t1, segs):
    """Align the scene's caption chunks to ASR segments by text (any segmentation); word times are interpolated
    inside each segment by character position."""
    ss = [s for s in segs if s["end"] > t0 + 0.3 and s["start"] < t1 and s["end"] <= t1 + 0.5]
    words = []
    for sg in ss:
        a = max(sg["start"], t0 + 0.4); b = sg["end"]
        ws = sg["text"].split(); n = sum(len(w) + 1 for w in ws); c = 0
        for w in ws:
            words.append([w, a + (b - a) * c / n, a + (b - a) * (c + len(w)) / n]); c += len(w) + 1
    return body_cues(sid, None, 0.0, words)


def wrap_en(s, n=42):
    if len(s) <= n:
        return s
    words, best = s.split(" "), None
    for i in range(1, len(words)):
        a, b = " ".join(words[:i]), " ".join(words[i:])
        if len(a) <= n and len(b) <= n:
            sc = abs(len(a) - len(b))
            if best is None or sc < best[0]:
                best = (sc, a + "\n" + b)
    return best[1] if best else (wrap_en(s, n + 4) if n < 50 else s)


def wrap_zh(s):
    if "\n" in s:
        return "\n".join(wrap_en(p, 46) if re.fullmatch(r"[\x00-\x7f’…]+", p) else p for p in s.split("\n"))
    if re.fullmatch(r"[\x00-\x7f’…]+", s):
        return wrap_en(s)
    return s


def ts(t):
    t = max(0, t); h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h:02d}:{m:02d}:{int(s):02d},{int(round((s - int(s)) * 1000)) % 1000:03d}"


def build():
    tl = json.load(open(f"{ROOT}/build/timeline.json"))
    words = json.load(open(f"{ROOT}/audio/vo_prep/words.json"))
    segs = json.load(open(sorted(glob.glob(f"{ROOT}/build/qa/final_audio_transcription_*.json"))[-1]))["segments"]
    bye = json.load(open(sorted(glob.glob(f"{ROOT}/build/qa/bye_transcription_*.json"))[-1]))["segments"]
    OFF = [d for d in tl if d["sid"] == "L3"][0]["t0"] + 6.13          # build/qa/bye.wav starts here
    segs = [s for s in segs if s["start"] < OFF - 0.5] + [dict(start=s["start"] + OFF, end=s["end"] + OFF, text=s["text"])
                                                          for s in bye if s["start"] + OFF >= OFF + 0.8]
    cues = []
    for d in tl:
        sid = d["sid"]
        if sid not in CAP:
            continue
        if d["voice"]:
            cues += body_cues(sid, d["voice"], d["t0"] + d["lead"], words[d["voice"]])
        else:
            cues += clip_cues(sid, d["t0"], d["t0"] + d["dur"], segs)
    cues.sort(key=lambda c: c[0])
    fixed = []
    for i, (a, b, en, zh) in enumerate(cues):
        nxt = cues[i + 1][0] if i + 1 < len(cues) else b + 1.5
        b = max(b + 0.35, a + 1.0)
        b = min(b, nxt - 0.1)
        fixed.append((a - 0.05, b, en, zh))
    for lang, idx, wrap in (("en", 2, wrap_en), ("zh-HK", 3, wrap_zh)):
        p = f"{ROOT}/output/Kayla_Grammar_Lab_The_present_and_the_past.{lang}.srt"
        with open(p, "w", encoding="utf-8") as f:
            for i, c in enumerate(fixed, 1):
                f.write(f"{i}\n{ts(c[0])} --> {ts(c[1])}\n{wrap(c[idx])}\n\n")
        print(p, len(fixed), "cues")
    return fixed


if __name__ == "__main__":
    cs = build()
    for c in cs[:6] + cs[-4:]:
        print(f"{c[0]:7.2f} {c[1]:7.2f} | {c[2][:60]}")
