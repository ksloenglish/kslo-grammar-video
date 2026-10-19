"use strict";
// Shared title-card system for 1.0, 2.0, 3.0 and 4.0. The engine owns Kayla's large-layout animation.
(() => {
  document.head.insertAdjacentHTML("beforeend", `<style>
    .lvl-root { position:absolute; inset:0; }
    .lvl-rail { position:absolute; width:4px; border-radius:3px; background:#FFD93D; box-shadow:0 0 16px rgba(255,217,61,.45); transform-origin:center top; }
    .lvl-kicker { position:absolute; font-family:Nunito; font-weight:900; font-size:22px; letter-spacing:.16em; color:#C0A6FF; line-height:1; }
    .lvl-number { position:absolute; font-family:Fredoka; font-weight:600; font-size:98px; color:#FFD93D; line-height:.9; font-feature-settings:"tnum" 1; }
    .lvl-name { position:absolute; font-family:Fredoka; font-weight:600; font-size:52px; line-height:1.04; color:#fff; letter-spacing:.025em; word-spacing:.18em; white-space:nowrap; }
    .lvl-rule { position:absolute; height:2px; background:rgba(255,255,255,.20); transform-origin:left center; }
    .lvl-xp { position:absolute; font-family:Fredoka; font-weight:600; font-size:34px; color:#FFD93D; line-height:1; }
    .lvl-track { position:absolute; box-sizing:border-box; height:30px; border:1.5px solid rgba(255,255,255,.28); border-radius:15px; background:rgba(255,255,255,.08); overflow:hidden; }
    .lvl-fill { position:absolute; left:5px; top:5px; height:18px; border-radius:10px; background:#FFD93D; box-shadow:0 0 14px rgba(255,217,61,.48); transform-origin:left center; }
    .lvl-progress { position:absolute; font-family:Nunito; font-weight:800; font-size:24px; color:#CDC3F0; line-height:1; }
  </style>`);

  const LEFT = 104, TEXT = 154, RIGHT = 750;
  let S = null;

  window.init = function(c) {
    const root = el("div", "lvl-root");
    const rail = el("div", "lvl-rail", { left: LEFT + "px", top:"298px", height:"438px" }, root);
    const kicker = masked("LEVEL", { left:TEXT + "px", top:"304px", fontFamily:"Nunito", fontWeight:900, fontSize:"22px", letterSpacing:".16em", color:C.lilac, lineHeight:"1" }, root);
    const number = masked(String(c.level).padStart(2, "0"), { left:TEXT + "px", top:"340px", fontFamily:"Fredoka", fontWeight:600, fontSize:"98px", color:C.yellow, lineHeight:".9" }, root);
    const name = masked(c.label.replace(/^LEVEL \d+ · /, ""), { left:TEXT + "px", top:"490px", fontFamily:"Fredoka", fontWeight:600, fontSize:"52px", letterSpacing:".025em", wordSpacing:".18em", color:C.white, lineHeight:"1.04", whiteSpace:"nowrap" }, root);
    const rule = el("div", "lvl-rule", { left:TEXT + "px", top:"576px", width:(RIGHT - TEXT) + "px" }, root);
    const xp = masked("XP", { left:TEXT + "px", top:"626px", fontFamily:"Fredoka", fontWeight:600, fontSize:"34px", color:C.yellow, lineHeight:"1" }, root);
    const track = el("div", "lvl-track", { left:"216px", top:"627px", width:"440px" }, root);
    const fill = el("div", "lvl-fill", { width:"428px" }, track);
    const progress = masked(`${c.level} of 4 levels`, { left:TEXT + "px", top:"692px", fontFamily:"Nunito", fontWeight:800, fontSize:"24px", color:C.dim, lineHeight:"1" }, root);
    S = { c, root, rail, kicker, number, name, rule, xp, track, fill, progress };
    return { template:"level", level:c.level };
  };

  window.seek = function(t) {
    const { c } = S;
    const p0 = ease.outExpo(prog(t, .05, .65));
    const pName = ease.outExpo(prog(t, .30, .75));
    const pXP = ease.outExpo(prog(t, .50, .65));
    reveal(S.kicker, p0);
    reveal(S.number, p0);
    S.rail.style.transform = `scaleY(${ease.outExpo(prog(t, .05, .75))})`;
    reveal(S.name, pName);
    S.rule.style.transform = `scaleX(${ease.outExpo(prog(t, .22, .8))})`;
    reveal(S.xp, pXP);
    S.track.style.opacity = pXP;
    S.track.style.transform = `translateY(${(1 - pXP) * 14}px)`;
    S.fill.style.transform = `scaleX(${(c.level / 4) * ease.outCubic(prog(t, .52, .8))})`;
    reveal(S.progress, ease.outExpo(prog(t, .58, .65)));
    exitLift(S.root, t);
    return true;
  };

  const _init = window.init;
  window.init = function(c) {
    const info = _init(c);
    fx(.05, "levelup", .85);
    return info;
  };
})();
