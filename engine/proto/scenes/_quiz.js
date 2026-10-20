"use strict";
// Q1–Q4 — one deterministic large-layout quiz template. Data below mirrors s_Q() calls in render/scenes.py.
(() => {
  document.head.insertAdjacentHTML("beforeend", `<style>
    .quiz-root { position:absolute; inset:0; }
    .quiz-chip { position:absolute; left:90px; top:154px; height:48px; padding:0 19px; box-sizing:border-box; border-radius:24px;
      display:flex; align-items:center; font:800 20px/1 "Nunito"; color:#281450; background:#FFD93D; letter-spacing:.055em; }
    .quiz-q { position:absolute; left:90px; top:244px; width:670px; color:#fff; font:800 52px/1.5 "Nunito"; letter-spacing:.005em; }
    .quiz-blank { display:inline-block; position:relative; height:48px; vertical-align:baseline; }
    .quiz-blankline { position:absolute; left:0; right:0; bottom:-22px; height:4px; border-radius:2px; background:#fff; transform-origin:left center; }
    .quiz-answer-canvas { position:absolute; pointer-events:none; }
    .quiz-count { position:absolute; width:168px; height:168px; border-radius:50%; box-sizing:border-box;
      background:radial-gradient(circle at 50% 34%, #3E2388 0%, #23104F 100%); box-shadow:0 0 34px rgba(255,217,61,.30), inset 0 2px 0 rgba(255,255,255,.12); transform-origin:center; }
    .quiz-count canvas { position:absolute; inset:0; }
    .quiz-answer-row { position:absolute; left:90px; min-height:74px; display:flex; align-items:center; gap:16px; transform-origin:left center; }
    .quiz-pill { height:86px; padding:0 32px; box-sizing:border-box; display:flex; align-items:center; border-radius:43px; white-space:nowrap;
      font:800 54px/1 "Nunito"; }
    .quiz-correct { color:#281450; box-shadow:0 0 19px rgba(255,217,61,.18); }
    .quiz-wrong { position:relative; color:#CDC3F0; background:rgba(205,195,240,.15); border:2px solid rgba(205,195,240,.24); }
    .quiz-strike { position:absolute; left:16px; right:16px; height:5px; border-radius:3px; background:#FF5468; box-shadow:0 0 9px rgba(255,84,104,.55); transform-origin:left center; }
    .quiz-tick { position:relative; width:72px; height:72px; border-radius:50%; background:#5CF2B0; flex:0 0 72px; box-shadow:0 0 18px rgba(92,242,176,.45); }
    .quiz-tags { position:absolute; left:90px; width:690px; display:flex; flex-wrap:wrap; align-items:flex-start; gap:14px; transform-origin:left top; }
    .quiz-tag { height:54px; padding:0 21px; box-sizing:border-box; border-radius:27px; display:flex; align-items:center; gap:8px; white-space:nowrap;
      color:#2EE6FF; border:1.5px solid rgba(46,230,255,.62); background:rgba(46,230,255,.09); font:800 24px/1 "Nunito"; }
    .quiz-tag.grammar { color:#C0A6FF; border-color:rgba(192,166,255,.62); background:rgba(192,166,255,.09); }
    .quiz-tag svg { width:22px; height:22px; flex:0 0 22px; }
  </style>`);

  // Exact old calls: (n, voice, q, ph, ans, acol, tags, cue2). grammarTags are additive context labels required for recap surfaces.
  const DATA = {
    Q1: { n:1, voice:"SQ1", q:"Look! The baby ___ (sleep).", ph:"is sleep", ans:"is sleeping", acol:"#FF4FA8", tags:["Look! = right now"], cue2:"its", grammarTags:["Present continuous"] },
    Q2: { n:2, voice:"SQ2", q:"I ___ (do) my homework when the lights went out.", ph:"was doing", ans:"was doing", acol:"#FF4FA8", tags:["long action, interrupted"], cue2:"long", grammarTags:["Past continuous"] },
    Q3: { n:3, voice:"SQ3", q:"Right now, I ___ (want) a new phone.", ph:"wanting", ans:"want", acol:"#FFD93D", tags:["no -ing"], cue2:"its", grammarTags:["Non-action verbs"], wrong:"am wanting" },
    Q4: { n:4, voice:"SQ4", q:"In the film, the hero ___ (fly) to the moon and saves the planet.", ph:"flies", ans:"flies", acol:"#FFD93D", tags:["synopsis = present", "fly → flies"], cue2:"in", grammarTags:["Tenses in stories"] }
  };
  let S = null;

  function fontMetrics(font, text) {
    const cv = document.createElement("canvas"), ctx = cv.getContext("2d");
    ctx.font = font;
    return { ctx, m: ctx.measureText(text) };
  }
  // Canvas placement centres the actual rendered ink, not the glyph's advance box. This fixes the narrow '1'.
  // Old bug: x = cx - (left + right) / 2 pushed a '1' ~5 px right. inkGlyph centres the ink box, then corrects optically.
  function drawCountdownDigit(cv, digit) {
    inkGlyph(cv, String(digit), `600 ${Math.round(cv.height * 0.6)}px Fredoka`, "#FFD93D", 0.6, "rgba(255,217,61,.55)");
  }
  function makeTag(text, kind, parent) {
    const tag = el("div", `quiz-tag ${kind || ""}`, {}, parent);
    if (text === "fly → flies") {
      const a = el("span", null, {}, tag); a.textContent = "fly";
      const ar = icon("arrow", 0, 0, 22, "#2EE6FF", "#2EE6FF", tag, 4.3);
      ar.s.style.position = "relative"; ar.s.style.left = "0"; ar.s.style.top = "0";
      const b = el("span", null, {}, tag); b.textContent = "flies";
      return { tag, arrow: ar };
    }
    tag.textContent = text;
    return { tag, arrow: null };
  }

  window.init = function(cues) {
    const d = DATA[cues.sid];
    if (!d) throw new Error(`Unknown quiz SID ${cues.sid}`);
    const root = el("div", "quiz-root");
    const chip = el("div", "quiz-chip", {}, root); chip.textContent = `QUESTION ${d.n} of 4`;
    const q = el("div", "quiz-q", {}, root);
    const [before, after] = d.q.split("___");
    q.appendChild(document.createTextNode(before));
    const blank = el("span", "quiz-blank", {}, q);
    const { m: ansM } = fontMetrics("800 68px Nunito", d.ans);
    blank.style.width = `${Math.ceil(ansM.width + 28)}px`;
    const line = el("span", "quiz-blankline", {}, blank);
    q.appendChild(document.createTextNode(after));

    // The revealed answer itself is canvas-drawn so its ink baseline can be exactly 18 px above the solid line.
    const answerCanvas = el("canvas", "quiz-answer-canvas", {}, root);
    const am = fontMetrics("800 68px Nunito", d.ans).m;
    answerCanvas.width = Math.ceil(am.actualBoundingBoxLeft + am.actualBoundingBoxRight + 8);
    answerCanvas.height = Math.ceil(am.actualBoundingBoxAscent + am.actualBoundingBoxDescent + 8);
    const ac = answerCanvas.getContext("2d");
    ac.font = "800 68px Nunito"; ac.fillStyle = d.acol; ac.textBaseline = "alphabetic";
    ac.fillText(d.ans, 4, 4 + am.actualBoundingBoxAscent);

    // Countdown timer disc (168 px, centre x 434): faint track + yellow arc that runs down while the digit shows.
    const CD = 168, CR = 72, CC = 2 * Math.PI * CR;
    const count = [3, 2, 1].map(digit => {
      const outer = el("div", "quiz-count", { left:`${434 - CD / 2}px`, top:"458px" }, root);
      outer.innerHTML = `<svg width="${CD}" height="${CD}" viewBox="0 0 ${CD} ${CD}" style="position:absolute;left:0;top:0;overflow:visible">
        <circle cx="${CD / 2}" cy="${CD / 2}" r="${CR}" fill="none" stroke="rgba(255,255,255,.14)" stroke-width="10"/>
        <circle class="arc" cx="${CD / 2}" cy="${CD / 2}" r="${CR}" fill="none" stroke="#FFD93D" stroke-width="10" stroke-linecap="round"
          stroke-dasharray="${CC.toFixed(2)}" stroke-dashoffset="0" transform="rotate(-90 ${CD / 2} ${CD / 2})" style="filter:drop-shadow(0 0 7px rgba(255,217,61,.75))"/></svg>`;
      const cv = el("canvas", null, { position:"absolute", left:"0", top:"0", width:`${CD}px`, height:`${CD}px` }, outer);
      cv.width = CD * 2; cv.height = CD * 2; drawCountdownDigit(cv, digit);
      outer.arc = outer.querySelector(".arc"); outer.CC = CC;
      return outer;
    });

    const answerRow = el("div", "quiz-answer-row", {}, root);
    let wrong = null, strike = null;
    if (d.wrong) {
      wrong = el("div", "quiz-pill quiz-wrong", {}, answerRow); wrong.textContent = d.wrong;
      strike = el("div", "quiz-strike", {}, wrong);
      // Measure x-height to place the stroke through it, rather than through descenders.
      const fm = fontMetrics("800 54px Nunito", d.wrong).m, xm = fontMetrics("800 54px Nunito", "x").m;
      const baseline = 43 + (fm.actualBoundingBoxAscent - fm.actualBoundingBoxDescent) / 2;
      strike.style.top = `${baseline - xm.actualBoundingBoxAscent / 2}px`;
    }
    const correct = el("div", "quiz-pill quiz-correct", { background:d.acol }, answerRow); correct.textContent = d.ans;
    const tickWrap = el("div", "quiz-tick", {}, answerRow);
    const tick = icon("tick", 8, 8, 56, "#281450", "#281450", tickWrap, 4.8);

    const tags = el("div", "quiz-tags", {}, root);
    const tagEntries = [...d.grammarTags.map(x => makeTag(x, "grammar", tags)), ...d.tags.map(x => makeTag(x, "", tags))];
    const qr = q.getBoundingClientRect(), br = blank.getBoundingClientRect(), lr = line.getBoundingClientRect();
    const baseline = lr.top - 18;
    answerCanvas.style.left = `${Math.round(br.left - am.actualBoundingBoxLeft - 4)}px`;
    answerCanvas.style.top = `${Math.round(baseline - am.actualBoundingBoxAscent - 4)}px`;
    const answerY = Math.max(620, Math.ceil(qr.bottom + 110));
    const cdTop = Math.max(458, Math.ceil(qr.bottom + 44));   // countdown always clear of the question text
    count.forEach(o => (o.style.top = `${cdTop}px`));
    answerRow.style.top = `${answerY}px`;
    tags.style.top = `${answerY + 108}px`;

    S = { cues, d, root, chip, q, blank, line, answerCanvas, count, answerRow, wrong, strike, correct, tickWrap, tick, tags, tagEntries };
    fx(0.10, "whoosh", 0.4);
    [0.85, 1.85, 2.85].forEach(t => fx(t, "tick", 0.55));
    fx(cues.lead, "correct", 0.75);
    return { blankLine: "solid", answerBaselineAboveLine: 18, countdownInkCentred: true, data: d.n };
  };

  window.seek = function(t) {
    const { cues:c, d } = S;
    const cq = ease.outExpo(prog(t, 0.10, 0.65));
    S.chip.style.opacity = cq;
    S.chip.style.transform = `translateX(${(1 - cq) * -20}px)`;
    S.q.style.opacity = cq;
    S.q.style.transform = `translateY(${(1 - cq) * 18}px)`;
    S.line.style.transform = `scaleX(${ease.outExpo(prog(t, 0.16, 0.42))})`;

    S.count.forEach((n, k) => {
      const t0 = 0.85 + k;
      const pin = ease.outBack(prog(t, t0, 0.23));
      const pout = ease.inCubic(prog(t, t0 + 0.66, 0.18));
      n.style.opacity = clamp(pin) * (1 - pout);
      n.style.transform = `scale(${Math.max(0, pin)})`;
      n.arc.setAttribute("stroke-dashoffset", (n.CC * ease.inOutCubic(prog(t, t0 + 0.08, 0.76))).toFixed(2));
    });

    const revealP = ease.outBack(prog(t, c.lead, 0.34));
    S.answerCanvas.style.opacity = clamp(prog(t, c.lead, 0.12));
    S.answerCanvas.style.transform = `translateY(${(1 - revealP) * 17}px) scale(${Math.max(.86, revealP)})`;
    S.answerRow.style.opacity = clamp(prog(t, c.lead + 0.05, 0.18));
    S.answerRow.style.transform = `translateY(${(1 - revealP) * 22}px) scale(${Math.max(.9, revealP)})`;
    drawIcon(S.tick, prog(t, c.lead + 0.22, 0.62));
    if (S.strike) S.strike.style.transform = `scaleX(${ease.outCubic(prog(t, c.lead + 0.20, 0.34))})`;

    const tagT = cue(d.cue2);
    const pt = ease.outExpo(prog(t, tagT, 0.55));
    S.tags.style.opacity = pt;
    S.tags.style.transform = `translateY(${(1 - pt) * 14}px)`;
    S.tagEntries.forEach((entry, k) => {
      const p = ease.outBack(prog(t, tagT + k * 0.10, 0.36));
      entry.tag.style.opacity = clamp(prog(t, tagT + k * 0.10, 0.13));
      entry.tag.style.transform = `translateY(${(1 - p) * 12}px) scale(${Math.max(.88, p)})`;
      if (entry.arrow) drawIcon(entry.arrow, prog(t, tagT + k * 0.10 + 0.05, 0.42));
    });
    exitLift(S.root, t);
    return true;
  };
})();
