"use strict";
// Q0 — Boss Quiz introduction. Large-layout content stays clear of Kayla.
(() => {
  document.head.insertAdjacentHTML("beforeend", `<style>
    .q0-root { position:absolute; inset:0; }
    .q0-title { position:absolute; left:90px; top:272px; font-family:"Fredoka"; font-weight:600; font-size:112px;
      line-height:1; color:#fff; letter-spacing:0.01em; white-space:nowrap; text-shadow:0 0 22px rgba(255,79,168,.52); }
    .q0-rule { position:absolute; left:90px; top:408px; width:650px; height:4px; border-radius:2px;
      background:#FF4FA8; box-shadow:0 0 16px rgba(255,79,168,.65); transform-origin:left center; }
    .q0-numbers { position:absolute; left:96px; top:475px; display:flex; gap:22px; }
    .q0-number { width:94px; height:94px; box-sizing:border-box; border-radius:50%; border:2px solid rgba(255,217,61,.74);
      background:rgba(255,217,61,.10); color:#FFD93D; display:flex; align-items:center; justify-content:center;
      font-family:"Fredoka"; font-weight:600; font-size:48px; box-shadow:0 0 18px rgba(255,217,61,.14); transform-origin:center; }
    .q0-prompt { position:absolute; left:96px; top:644px; font-family:"Nunito"; font-weight:800; font-size:32px;
      color:#2EE6FF; line-height:1; letter-spacing:.02em; white-space:nowrap; }
  </style>`);

  let S = null;
  window.init = function(cues) {
    const root = el("div", "q0-root");
    const title = el("div", "q0-title", {}, root); title.textContent = "BOSS QUIZ";
    const rule = el("div", "q0-rule", {}, root);
    const numsBox = el("div", "q0-numbers", {}, root);
    const nums = [1, 2, 3, 4].map(n => { const e = el("div", "q0-number", {}, numsBox); e.textContent = n; return e; });
    const prompt = el("div", "q0-prompt", {}, root); prompt.textContent = "Say your answers out loud!";
    S = { cues, root, title, rule, nums, prompt };
    fx(0.05, "sting", 0.7);
    [0.4, 0.52, 0.64, 0.76].forEach(t => fx(t, "pop", 0.4));
    return { layout: "large", contentRight: 760 };
  };

  window.seek = function(t) {
    const pTitle = ease.outBack(prog(t, 0.05, 0.42));
    S.title.style.opacity = clamp(prog(t, 0.05, 0.15));
    S.title.style.transform = `translateY(${(1 - pTitle) * 26}px) scale(${lerp(.90, 1, pTitle)})`;
    S.title.style.transformOrigin = "left center";
    S.title.style.setProperty("filter", `drop-shadow(0 0 ${14 * clamp(pTitle)}px rgba(255,79,168,.28))`);
    const pr = ease.outExpo(prog(t, 0.16, 0.72));
    S.rule.style.opacity = pr;
    S.rule.style.transform = `scaleX(${pr})`;
    S.nums.forEach((n, k) => {
      const p = ease.outBack(prog(t, 0.4 + k * 0.12, 0.34));
      n.style.opacity = clamp(prog(t, 0.4 + k * 0.12, 0.12));
      n.style.transform = `translateY(${(1 - p) * 20}px) scale(${Math.max(0, p)})`;
    });
    const ps = cue("say");
    const pp = ease.outExpo(prog(t, ps - 0.08, 0.62));
    S.prompt.style.opacity = pp;
    S.prompt.style.transform = `translateY(${(1 - pp) * 18}px)`;
    exitLift(S.root, t);
    return true;
  };
})();
