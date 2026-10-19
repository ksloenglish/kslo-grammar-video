"use strict";
// Scene 2.2 Past continuous (approved design-led prototype, round 10). Ported from proto/scene22.html.
(() => {
const PANEL = { x: 60, y: 130, h: 900 };
const L = 116, COL = 196, R = 1340, TX = 660;
const AX0 = COL, AX1 = 600, BX0 = 226, BX1 = 560, AXY = 146;      // timeline geometry inside each row
const ROW_Y = [280, 506, 750], ROW_H = [226, 244, 236];
let S = null;
window.init = function (cues) {
  const c = cues;
  c.dim = c.dim !== false;
  const pn = panel(PANEL.x, PANEL.y, 1340, PANEL.h);
  const content = el("div", null, { position: "absolute", inset: "0" });
  // ---- title, formula, counter, header rule
  const title = masked("Past continuous", { left: L + "px", top: "176px", fontFamily: "Fredoka", fontWeight: 600, fontSize: "58px",
    color: C.white, lineHeight: "1" }, content);
  const tw = title.i.getBoundingClientRect().width;
  let fx = L + tw + 64;
  const tokA = el("div", "tok", { left: fx + "px", top: "179px", border: `2px solid ${C.pink}`, background: "rgba(255,79,168,0.10)" }, content);
  tokA.textContent = "was / were";
  fx += tokA.getBoundingClientRect().width + 16;
  const plus = el("div", "num", { position: "absolute", left: fx + "px", top: "181px", fontSize: "40px", lineHeight: "48px",
    color: "rgba(255,255,255,0.7)" }, content);
  plus.textContent = "+";
  fx += plus.getBoundingClientRect().width + 16;
  const tokV = el("div", "tok", { left: fx + "px", top: "179px", border: "2px solid rgba(255,255,255,0.45)",
    background: "rgba(255,255,255,0.06)" }, content);
  tokV.textContent = "verb";
  const vr = fx + tokV.getBoundingClientRect().width;
  const tokI = el("div", "tok", { left: (vr - 2) + "px", top: "179px", border: `2px solid ${C.pink}`, background: C.pink,
    color: C.ink, boxShadow: "0 0 18px rgba(255,79,168,0.5)" }, content);
  tokI.textContent = "-ing";
  const cnt = el("div", "num", { position: "absolute", top: "192px", right: (1920 - R) + "px", fontSize: "30px", lineHeight: "1",
    display: "flex", alignItems: "flex-start", color: "rgba(255,255,255,0.45)" }, content);
  const cntMask = el("div", null, { position: "relative", overflow: "hidden", height: "36px", width: "38px", marginRight: "10px" }, cnt);
  const cntStrip = el("div", null, { position: "absolute", left: "0", top: "0", color: C.yellow, lineHeight: "36px" }, cntMask);
  cntStrip.innerHTML = "01<br>02<br>03";
  const cntTot = el("div", null, { lineHeight: "36px" }, cnt); cntTot.textContent = "/ 03";
  const rule0 = hrule(L, 266, R - L, 0.18, content);
  // ---- progress rail
  const railX = 86;
  const yEnd = ROW_Y[2] + ROW_H[2];
  const rail = el("div", null, { position: "absolute", left: railX + "px", top: (ROW_Y[0] + 26) + "px", width: "2px",
    height: (yEnd - 26 - ROW_Y[0] - 26) + "px", background: "rgba(255,255,255,0.10)", transformOrigin: "center top" }, content);
  const act = el("div", null, { position: "absolute", left: (railX - 1) + "px", width: "4px", borderRadius: "2px", background: C.pink,
    boxShadow: "0 0 14px rgba(255,79,168,0.65)" }, content);
  // ---- rows
  const defs = [
    { lab: "In progress at a past time", ex: "We {were having|p} a barbecue\n{at four o’clock yesterday|t}.", c1: c.use, c2: c.we,
      marks: [[c.were2, 0.42], [c.at, 0.9]] },
    { lab: "Long action + short action", ex: "She {was waiting|p} for the bus\n{when|t} it suddenly {rained|y}.", c1: c.long, c2: c.she,
      marks: [[c.was2, 0.42], [c.when, 0.3], [c.rained, 0.35]] },
    { lab: "Two actions at the same time", ex: "Fred {was watching|p} TV\n{while|t} his mum {was preparing|p} dinner.", c1: c.two,
      c2: c.fred, marks: [[c.was3, 0.42], [c.while, 0.3], [c.was4, 0.42]] },
  ];
  const rows = defs.map((r, i) => {
    const y = ROW_Y[i], h = ROW_H[i];
    const g = el("div", null, { position: "absolute", inset: "0" }, content);
    const num = masked(String(i + 1).padStart(2, "0"), { left: L + "px", top: (y + 30) + "px", fontFamily: "Fredoka", fontWeight: 600,
      fontSize: "30px", color: C.pink, lineHeight: "1" }, g);
    const lab = masked(r.lab, { left: COL + "px", top: (y + 34) + "px", fontSize: "20px", color: C.lilac, lineHeight: "1" }, g);
    lab.o.classList.add("label");
    // timeline axis + arrowhead
    const ax = el("div", null, { position: "absolute", left: AX0 + "px", top: (y + AXY - 1) + "px", width: (AX1 - AX0 - 2) + "px",
      height: "2px", background: "rgba(255,255,255,0.5)", transformOrigin: "left center" }, g);
    const ah = el("svg", null, { position: "absolute", left: (AX1 - 14) + "px", top: (y + AXY - 10) + "px", width: "16px",
      height: "20px", overflow: "visible" }, g);
    ah.innerHTML = '<path d="M2 2 L14 10 L2 18" fill="none" stroke="rgba(255,255,255,0.5)" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>';
    const sn = sentence(r.ex, TX, y + 76, 38, g);
    const tip = i ? el("div", "small", { left: TX + "px", top: (y + 189) + "px", fontSize: "24px" }, g) : null;
    if (tip) {
      const w = i === 1 ? ["when", "before the short action."] : ["while", "before a long action."];
      tip.innerHTML = `<span class="cap" style="color:${C.yellow};margin-right:14px">Tip</span>Use <span style="color:${C.cyan};font-weight:800">${w[0]}</span> ${w[1]}`;
    }
    const rule = i < 2 ? hrule(L, y + h, R - L, 0.10, g) : null;
    return Object.assign({}, r, { y, h, g, num, lab, ax, ah, sn, tip, rule, parts: {} });
  });
  // ---- diagram parts
  const r0 = rows[0], r1 = rows[1], r2 = rows[2];
  const xm = Math.round(BX0 + 0.62 * (BX1 - BX0)), xs = Math.round(BX0 + 0.72 * (BX1 - BX0));
  const mkbar = (row, yc) => el("div", "bar", { left: BX0 + "px", top: (row.y + yc - 11) + "px", width: "22px" }, row.g);
  r0.parts.bar = mkbar(r0, AXY);
  r0.parts.dash = el("div", null, { position: "absolute", left: (xm - 1) + "px", top: (r0.y + 114) + "px", width: "2px", height: "64px",
    background: `repeating-linear-gradient(to bottom, ${C.cyan} 0 6px, transparent 6px 11px)`, transformOrigin: "center top" }, r0.g);
  r0.parts.clock = icon("clock", xm - 20, r0.y + 70, 40, C.cyan, C.cyan, r0.g, 3.6);
  r0.parts.time = el("div", "num", { position: "absolute", left: (xm - 60) + "px", width: "120px", textAlign: "center",
    top: (r0.y + 184) + "px", fontSize: "22px", lineHeight: "1", color: C.cyan }, r0.g);
  r0.parts.time.textContent = "4:00";
  r1.parts.bar = mkbar(r1, AXY);
  r1.parts.bolt = icon("bolt", xs - 26, r1.y + AXY - 11 - 49, 52, C.yellow, C.yellow, r1.g, 3.4);
  r1.parts.dot = el("div", null, { position: "absolute", left: (xs - 7) + "px", top: (r1.y + AXY - 7) + "px", width: "14px", height: "14px",
    borderRadius: "7px", background: C.yellow, boxShadow: "0 0 12px rgba(255,217,61,0.8)" }, r1.g);
  r1.parts.ring = el("div", null, { position: "absolute", left: (xs - 30) + "px", top: (r1.y + AXY - 30) + "px", width: "60px",
    height: "60px", borderRadius: "30px", boxSizing: "border-box", border: `3px solid ${C.yellow}` }, r1.g);
  const legend = (yy, sw, word, col, rest) => {
    const d = el("div", "small", { left: BX0 + "px", top: yy + "px", display: "flex", alignItems: "center" }, r1.g);
    d.innerHTML = `${sw}<span class="cap" style="color:${col};font-size:19px;margin:0 10px 0 12px">${word}</span>= ${rest}`;
    return d;
  };
  r1.parts.legL = legend(r1.y + 174, `<span style="display:inline-block;width:28px;height:10px;border-radius:5px;background:${C.pink}"></span>`,
                         "Long", C.pink, "past continuous");
  r1.parts.legS = legend(r1.y + 204, `<span style="display:inline-block;width:10px;height:10px;border-radius:5px;margin:0 9px;background:${C.yellow}"></span>`,
                         "Short", C.yellow, "simple past");
  r2.parts.barA = mkbar(r2, AXY - 22);
  r2.parts.barB = mkbar(r2, AXY + 22);
  r2.parts.labA = el("div", "cap", { position: "absolute", left: BX0 + "px", top: (r2.y + AXY - 22 - 11 - 26) + "px", color: C.dim,
    lineHeight: "1" }, r2.g);
  r2.parts.labA.textContent = "Fred";
  r2.parts.labB = el("div", "cap", { position: "absolute", left: BX0 + "px", top: (r2.y + AXY + 22 + 11 + 10) + "px", color: C.dim,
    lineHeight: "1" }, r2.g);
  r2.parts.labB.textContent = "His mum";
  // ---- fit all sentences to one size inside the text column
  let size = 38;
  const widest = () => Math.max(...rows.map(r => r.sn.box.getBoundingClientRect().width));
  while (TX + widest() > R - 4 && size > 30) { size -= 1; rows.forEach(r => (r.sn.box.style.fontSize = size + "px")); }
  S = { c, pn, content, title, tokA, plus, tokV, tokI, cnt, cntStrip, rule0, rail, act, rows, xm, xs, size };
  return { size, xm, xs, formulaEnd: vr + tokI.getBoundingClientRect().width, widest: TX + widest() };
};
window.seek = function (t) {
  const { c, rows } = S;
  const review = c.voice_end + 0.35, exit0 = c.dur - 0.45;
  // panel follows the engine's layout (it widens as Kayla moves to the corner)
  const fi = Math.min(c.panel_right.length - 1, Math.max(0, Math.round(t * c.fps)));
  S.pn.style.width = (c.panel_right[fi] - PANEL.x) + "px";
  // title + formula
  reveal(S.title, ease.outExpo(prog(t, 0.05, 0.8)));
  S.rule0.style.transform = `scaleX(${ease.outExpo(prog(t, 0.2, 1.0))})`;
  const tokIn = (e, t0) => { const p = ease.outExpo(prog(t, t0, 0.6)); e.style.opacity = clamp(p * 1.6);
    e.style.transform = `translateY(${(1 - p) * 18}px)`; };
  tokIn(S.tokA, 0.35); tokIn(S.plus, 0.45); tokIn(S.tokV, 0.55);
  const pd = spring(t - c.plus, 13, 0.72), pdo = clamp(prog(t, c.plus, 0.15));
  S.tokI.style.opacity = pdo;
  S.tokI.style.transform = `translateX(${(1 - pd) * 110}px)`;
  const dock = ease.outCubic(prog(t, c.plus + 0.25, 0.2));
  S.tokV.style.borderRadius = `14px ${lerp(14, 3, dock)}px ${lerp(14, 3, dock)}px 14px`;
  S.tokI.style.borderRadius = `${lerp(14, 3, dock)}px 14px 14px ${lerp(14, 3, dock)}px`;
  // counter + rail
  S.cnt.style.opacity = ease.outCubic(prog(t, rows[0].c1, 0.4));
  let ci = 0;
  rows.forEach((r, i) => { if (i > 0) ci += ease.outExpo(prog(t, r.c1, 0.6)); });
  S.cntStrip.style.transform = `translateY(${-36 * ci}px)`;
  S.rail.style.transform = `scaleY(${ease.outExpo(prog(t, rows[0].c1, 1.0))})`;
  let top = rows[0].y + 26, bot = rows[0].y + rows[0].h - 26;
  rows.forEach((r, i) => { if (!i) return; const p = spring(t - r.c1); top = lerp(top, r.y + 26, p); bot = lerp(bot, r.y + r.h - 26, p); });
  top = lerp(top, rows[0].y + 26, ease.inOutCubic(prog(t, review, 0.7)));
  const grow = ease.outExpo(prog(t, rows[0].c1, 0.6));
  S.act.style.top = top + "px"; S.act.style.height = Math.max(0, (bot - top) * grow) + "px"; S.act.style.opacity = grow;
  // rows
  rows.forEach((r, i) => {
    reveal(r.num, ease.outExpo(prog(t, r.c1, 0.7)));
    reveal(r.lab, ease.outExpo(prog(t, r.c1 + 0.06, 0.7)));
    const pa = ease.outExpo(prog(t, r.c1 + 0.15, 0.7));
    r.ax.style.transform = `scaleX(${pa})`;
    r.ah.style.opacity = prog(pa, 0.85, 0.15);
    if (r.rule) r.rule.style.transform = `scaleX(${ease.outExpo(prog(t, r.c1 + 0.2, 1.0))})`;
    riseWords(r.sn, t, r.c2 - 0.12);
    r.sn.groups.forEach((g, k) => {
      const k0 = r.sn.words.indexOf(g.words[g.words.length - 1]);
      const landed = r.c2 - 0.12 + k0 * 0.05 + 0.3;
      sweep(g, t, Math.max(r.marks[k][0], landed), r.marks[k][1]);
    });
    let dim = 0;
    if (c.dim && i < rows.length - 1) dim = ease.inOutCubic(prog(t, rows[i + 1].c1, 0.5)) * (1 - ease.inOutCubic(prog(t, review, 0.6)));
    r.g.style.opacity = 1 - 0.6 * dim;
  });
  const barGrow = (b, t0, d, x1 = BX1) => { const p = ease.outCubic(prog(t, t0, d));
    b.style.width = lerp(22, x1 - BX0, p) + "px"; b.style.opacity = clamp(prog(t, t0, 0.1)); };
  const [r0, r1, r2] = rows;
  // row 1: the action is in progress; 4:00 lands in the middle of it
  barGrow(r0.parts.bar, r0.c1 + 0.35, 1.2);
  drawIcon(r0.parts.clock, prog(t, c.four - 0.05, 0.6));
  r0.parts.dash.style.transform = `scaleY(${ease.outCubic(prog(t, c.four + 0.15, 0.4))})`;
  r0.parts.time.style.opacity = ease.outCubic(prog(t, c.four + 0.3, 0.35));
  r0.parts.time.style.transform = `translateY(${(1 - ease.outExpo(prog(t, c.four + 0.3, 0.6))) * 10}px)`;
  // row 2: long bar, then the short action strikes it
  barGrow(r1.parts.bar, r1.c1 + 0.35, 1.0);
  const lgL = ease.outExpo(prog(t, r1.c1 + 0.6, 0.6));
  r1.parts.legL.style.opacity = lgL; r1.parts.legL.style.transform = `translateY(${(1 - lgL) * 12}px)`;
  const pb = prog(t, c.short - 0.05, 0.35);
  drawIcon(r1.parts.bolt, pb);
  r1.parts.bolt.parts[0].e.setAttribute("fill", `rgba(255,217,61,${0.9 * ease.outCubic(prog(t, c.short + 0.2, 0.25))})`);
  r1.parts.bolt.s.style.transform = `translateY(${(1 - ease.outCubic(clamp(pb * 1.3))) * -14}px)`;
  const ps = ease.outBack(prog(t, c.short + 0.2, 0.35));
  r1.parts.dot.style.transform = `scale(${Math.max(0, ps)})`;
  const pr = prog(t, c.short + 0.25, 0.6);
  r1.parts.ring.style.opacity = pr > 0 && pr < 1 ? (1 - pr) * 0.9 : 0;
  r1.parts.ring.style.transform = `scale(${lerp(0.3, 1.25, ease.outCubic(pr))})`;
  const lgS = ease.outExpo(prog(t, c.short + 0.3, 0.6));
  r1.parts.legS.style.opacity = lgS; r1.parts.legS.style.transform = `translateY(${(1 - lgS) * 12}px)`;
  const tip1 = ease.outExpo(prog(t, c.when + 1.0, 0.6));
  r1.tip.style.opacity = tip1; r1.tip.style.transform = `translateY(${(1 - tip1) * 14}px)`;
  // row 3: two bars run side by side; each gets its person's name when she says it
  barGrow(r2.parts.barA, r2.c1 + 0.35, 1.0);
  barGrow(r2.parts.barB, r2.c1 + 0.5, 1.0);
  const la = ease.outExpo(prog(t, c.fred, 0.6)), lb = ease.outExpo(prog(t, c.his, 0.6));
  r2.parts.labA.style.opacity = la; r2.parts.labA.style.transform = `translateY(${(1 - la) * 8}px)`;
  r2.parts.labB.style.opacity = lb; r2.parts.labB.style.transform = `translateY(${(1 - lb) * -8}px)`;
  const tip2 = ease.outExpo(prog(t, c.dinner + 0.2, 0.6));
  r2.tip.style.opacity = tip2; r2.tip.style.transform = `translateY(${(1 - tip2) * 14}px)`;
  // exit: content lifts and fades
  const pe = ease.inCubic(prog(t, exit0, 0.42));
  S.content.style.opacity = 1 - pe;
  S.content.style.transform = `translateY(${-16 * pe}px)`;
  return true;
};
const _init = window.init;
window.init = function (cues) {
  const M = { past: ["past", 1], was1: ["was", 1], plus: ["plus", 1], ing: ["ing", 1], use: ["use", 1], we: ["we", 1], were2: ["were", 2], having: ["having", 1], at: ["at", 2], four: ["four", 1], yesterday: ["yesterday", 1], long: ["long", 1], short: ["short", 1], she: ["she", 1], was2: ["was", 2], waiting: ["waiting", 1], when: ["when", 1], rained: ["rained", 1], two: ["two", 1], fred: ["fred", 1], was3: ["was", 3], while: ["while", 1], his: ["his", 1], was4: ["was", 4], preparing: ["preparing", 1], dinner: ["dinner", 1] };
  for (const [k, [p, n]] of Object.entries(M)) cues[k] = cue(p, n);
  cues.panel_right = cues.panel.map(p => p[0]);
  const info = _init(cues);
  const c = cues;
  fx(c.plus + 0.4, "click", 0.8); fx(c.four + 0.3, "click", 0.7); fx(c.short + 0.2, "glitch", 0.6);
  [c.use, c.long, c.two].forEach(t => fx(t, "whoosh", 0.4));
  return info;
};
})();
