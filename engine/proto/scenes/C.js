"use strict";
// C — aligned end-of-unit cheat sheet, retaining all legacy text and recap content.
(() => {
  document.head.insertAdjacentHTML("beforeend", `<style>
    .cheat-content { position:absolute; inset:0; }
    .cheat-title { font-family:"Fredoka"; font-weight:600; font-size:58px; color:#fff; line-height:1; }
    .cheat-col { position:absolute; font:800 20px/1 "Nunito"; letter-spacing:.14em; text-transform:uppercase; }
    .cheat-axis { position:absolute; width:112px; height:44px; box-sizing:border-box; border-radius:22px; display:flex; align-items:center; justify-content:center;
      font:800 18px/1 "Nunito"; letter-spacing:.12em; }
    .cheat-tile { position:absolute; box-sizing:border-box; width:514px; height:194px; padding:17px 20px 14px; border-radius:22px;
      background:rgba(255,255,255,.045); border:2px solid; overflow:hidden; transform-origin:left top; }
    .cheat-tile-title { font:600 25px/1.1 "Fredoka"; white-space:nowrap; }
    .cheat-list { margin-top:14px; display:flex; flex-direction:column; gap:5px; }
    .cheat-bullet { display:grid; grid-template-columns:15px 1fr; align-items:start; font:800 20px/1.26 "Nunito"; color:#fff; }
    .cheat-dot { width:8px; height:8px; margin-top:8px; border-radius:50%; }
    .cheat-bullet .cyan { color:#2EE6FF; }
    .cheat-dual { display:grid; grid-template-columns:1fr 1fr; gap:12px; }
    .cheat-dual .cheat-bullet { font-size:19px; }
    .cheat-strip { position:absolute; left:116px; width:1228px; height:72px; box-sizing:border-box; border:1.5px solid rgba(46,230,255,.72);
      border-radius:20px; background:rgba(46,230,255,.075); display:flex; align-items:center; padding:0 17px; }
    .cheat-strip-label { width:234px; height:42px; flex:0 0 234px; box-sizing:border-box; border-radius:21px; display:flex; align-items:center; justify-content:center;
      background:#2EE6FF; color:#281450; font:800 17px/1 "Nunito"; letter-spacing:.055em; }
    .cheat-strip-text { margin-left:21px; color:#fff; font:800 20px/1.2 "Nunito"; white-space:nowrap; }
    .cheat-story { display:flex; align-items:center; gap:9px; }
    .cheat-story svg { position:relative; width:22px; height:22px; flex:0 0 22px; }
    .cheat-pause { position:absolute; left:1057px; top:946px; height:60px; padding:0 24px; display:flex; align-items:center; box-sizing:border-box;
      border-radius:30px; background:#FFD93D; color:#281450; font:600 29px/1 "Fredoka"; transform-origin:center; box-shadow:0 0 18px rgba(255,217,61,.45); white-space:nowrap; }
  </style>`);

  const L = 116, TX = [250, 818], TY = [338, 550], TW = 514, TH = 194;
  let S = null;
  function rich(host, parts) {
    parts.forEach(part => { const sp = document.createElement("span"); sp.textContent = part[0]; if (part[1]) sp.className = part[1]; host.appendChild(sp); });
  }
  function bullet(parent, parts, col) {
    const row = el("div", "cheat-bullet", {}, parent);
    const dot = el("span", "cheat-dot", { background:col }, row);
    const text = el("div", null, {}, row); rich(text, parts);
    return row;
  }
  function tile(root, x, y, title, col, rows, dual) {
    const box = el("div", "cheat-tile", { left:x+"px", top:y+"px", borderColor:col }, root);
    const hd = el("div", "cheat-tile-title", { color:col }, box); hd.textContent = title;
    const list = el("div", dual ? "cheat-list cheat-dual" : "cheat-list", {}, box);
    rows.forEach(row => bullet(list, row, col));
    return box;
  }
  function strip(root, y, label, text, story) {
    const st = el("div", "cheat-strip", { top:y+"px" }, root);
    const lab = el("div", "cheat-strip-label", {}, st); lab.textContent = label;
    let body;
    if (!story) {
      body = el("div", "cheat-strip-text", {}, st); body.textContent = text;
    } else {
      body = el("div", "cheat-strip-text cheat-story", {}, st);
      const chunks = ["story", "past · synopsis / retelling", "present · real-world facts", "past"];
      chunks.forEach((chunk, i) => { const sp = el("span", null, {}, body); sp.textContent = chunk; if (i < chunks.length - 1) {
        const ar = icon("arrow", 0, 0, 22, "#2EE6FF", "#2EE6FF", body, 3.8); ar.s.style.position = "relative"; ar.s.style.left="0"; ar.s.style.top="0"; ar.s.dataset.arrow = "1";
      }});
    }
    return { st, arrows: [...st.querySelectorAll('[data-arrow="1"]')].map(s => ({ s, parts: [] })) };
  }

  window.init = function(cues) {
    const pn = panel(60, 130, 1340, 900);
    const content = el("div", "cheat-content");
    const title = masked("CHEAT SHEET", { left:L+"px", top:"176px", lineHeight:"1" }, content); title.o.classList.add("cheat-title");
    const rule = hrule(L, 266, 1228, 0.18, content);
    const simple = el("div", "cheat-col", { left:TX[0]+"px", top:"297px", color:C.yellow }, content); simple.textContent = "SIMPLE";
    const continuous = el("div", "cheat-col", { left:TX[1]+"px", top:"297px", color:C.pink }, content); continuous.textContent = "CONTINUOUS";
    const axes = [["PRESENT", 414, "#5CF2B0"], ["PAST", 626, "#FFA448"]].map(([tx, y, col]) => {
      const a = el("div", "cheat-axis", { left:L+"px", top:y+"px", border:`1.5px solid ${col}`, color:col, background:`${col}16` }, content); a.textContent = tx; return a;
    });
    const tiles = [
      tile(content, TX[0], TY[0], "Simple present · I play", C.yellow, [
        [["facts"]], [["true now"]], [["habits: "], ["every day, often,", "cyan"], ["\nusually, always", "cyan"]]
      ]),
      tile(content, TX[1], TY[0], "Present continuous · I am playing", C.pink, [
        [["right now"]], [["temporary"]], [["changing trends"]], [["photos"]], [["annoying habits ("], ["always", "cyan"], [")"]]
      ], true),
      tile(content, TX[0], TY[1], "Simple past · I played", C.yellow, [
        [["finished actions"]], [["time words: "], ["yesterday, last week,", "cyan"], ["\ntwo years ago, in 2013", "cyan"]]
      ]),
      tile(content, TX[1], TY[1], "Past continuous · I was playing", C.pink, [
        [["in progress at a past time"]], [["long action + short action ("], ["when", "cyan"], [")"]], [["two actions at the same time ("], ["while", "cyan"], [")"]]
      ])
    ];
    const stripA = strip(content, 765, "Non-action verbs", "like · want · think · know · see · smell · have: no -ing", false);
    const stripB = strip(content, 852, "Tenses in stories", "", true);
    const pause = el("div", "cheat-pause", {}, content); pause.textContent = "Pause & screenshot!";
    S = { cues, pn, content, title, rule, simple, continuous, axes, tiles, strips:[stripA, stripB], pause };
    [0.30, 0.45, 0.60, 0.75].forEach(t => fx(t, "pop", 0.4));
    fx(cue("pause"), "pop", 0.8);
    return { grid:[TX, TY], stripLabelWidth:234, hold:"4.2" };
  };

  window.seek = function(t) {
    const { cues:c } = S;
    followPanel(S.pn, t);
    const p0 = ease.outExpo(prog(t, .05, .75));
    reveal(S.title, p0);
    S.rule.style.transform = `scaleX(${ease.outExpo(prog(t, .18, .92))})`;
    [S.simple, S.continuous].forEach((h, k) => { const p = ease.outExpo(prog(t, .15 + k*.05, .55)); h.style.opacity=p; h.style.transform=`translateY(${(1-p)*12}px)`; });
    S.axes.forEach((a, k) => { const p=ease.outExpo(prog(t,.20+k*.05,.55)); a.style.opacity=p; a.style.transform=`translateX(${(1-p)*-12}px)`; });
    S.tiles.forEach((tileNode, k) => { const p=ease.outBack(prog(t,.30+k*.15,.38)); tileNode.style.opacity=clamp(prog(t,.30+k*.15,.13)); tileNode.style.transform=`translateY(${(1-p)*18}px) scale(${Math.max(.94,p)})`; });
    S.strips.forEach((st, k) => { const p=ease.outExpo(prog(t,.92+k*.20,.56)); st.st.style.opacity=p; st.st.style.transform=`translateX(${(1-p)*-20}px)`; });
    const pp=ease.outBack(prog(t,cue("pause"),.42)); S.pause.style.opacity=clamp(prog(t,cue("pause"),.12)); S.pause.style.transform=`rotate(4deg) translateY(${(1-pp)*17}px) scale(${Math.max(.90,pp)})`;
    exitLift(S.content, t);
    return true;
  };
})();
