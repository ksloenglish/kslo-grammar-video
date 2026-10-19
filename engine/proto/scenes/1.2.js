"use strict";
// Scene 1.2 Simple present uses (approved design-led prototype, round 9). Ported from proto/scene12.html.
(() => {
document.head.insertAdjacentHTML("beforeend", `<style>
html, body { margin: 0; width: 1920px; height: 1080px; background: transparent; overflow: hidden; }
body { -webkit-font-smoothing: antialiased; text-rendering: geometricPrecision; }
#stage { position: absolute; inset: 0; }
.abs { position: absolute; }
.mask { position: absolute; overflow: hidden; padding: 0.10em 0.04em 0.18em; margin: -0.10em -0.04em -0.18em; }
.inner { display: block; white-space: nowrap; will-change: transform; }
.sent { position: absolute; white-space: nowrap; font-family: "Nunito"; font-weight: 800; color: #fff; line-height: 1.2; }
.wm { display: inline-block; overflow: hidden; vertical-align: top; padding: 0 0.03em 0.16em; margin: 0 -0.03em -0.16em; }
.wi { display: inline-block; will-change: transform; }
.hl { position: relative; display: inline-block; isolation: isolate; margin: 0 0.07em; }
.mk { position: absolute; left: -0.09em; right: -0.09em; top: 0.17em; bottom: 0.05em; border-radius: 0.2em; z-index: -1;
      transform-origin: left center; }
.label { font-family: "Nunito"; font-weight: 800; letter-spacing: 0.14em; text-transform: uppercase; }
.num { font-family: "Fredoka"; font-weight: 600; font-feature-settings: "tnum" 1; }
.tag { position: absolute; display: flex; align-items: center; height: 54px; padding: 0 24px; box-sizing: border-box;
       border-radius: 27px; border: 2px solid rgba(46, 230, 255, 0.6); background: rgba(46, 230, 255, 0.11);
       color: #2EE6FF; font-family: "Nunito"; font-weight: 800; font-size: 28px; white-space: nowrap; transform-origin: 0 0; }
svg path, svg circle, svg line { fill: none; stroke-linecap: round; stroke-linejoin: round; }
</style>`);
// ---------------------------------------------------------------- palette, grid, easing
const C = { yellow: "#FFD93D", cyan: "#2EE6FF", lilac: "#C0A6FF", dim: "#CDC3F0", ink: "#281450", white: "#FFFFFF" };
const PANEL = { x: 60, y: 130, w: 1110, h: 900 };
const L = 116, R = 1114, COL = 196;                  // content grid: numeral column at L, text column at COL
const ROW_Y = [286, 470, 654], ROW_H = 184;
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const prog = (t, t0, d) => clamp((t - t0) / d);
const lerp = (a, b, p) => a + (b - a) * p;
const ease = {
  outExpo: p => (p >= 1 ? 1 : 1 - Math.pow(2, -10 * p)),
  outCubic: p => 1 - Math.pow(1 - p, 3),
  inCubic: p => p * p * p,
  inOutCubic: p => (p < 0.5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2),
  outBack: p => { const c1 = 1.9, c3 = c1 + 1; return 1 + c3 * Math.pow(p - 1, 3) + c1 * Math.pow(p - 1, 2); },
};
function spring(s, w = 15, z = 0.68) {               // damped spring, s = seconds since start, returns 0..~1.05..1
  if (s <= 0) return 0;
  const wd = w * Math.sqrt(1 - z * z);
  return 1 - Math.exp(-z * w * s) * (Math.cos(wd * s) + (z * w / wd) * Math.sin(wd * s));
}
function mix(c1, c2, p) {                            // hex colour interpolation
  const a = [1, 3, 5].map(i => parseInt(c1.slice(i, i + 2), 16)), b = [1, 3, 5].map(i => parseInt(c2.slice(i, i + 2), 16));
  return `rgb(${a.map((v, i) => Math.round(lerp(v, b[i], p))).join(",")})`;
}
const stage = document.getElementById("stage");
function el(tag, cls, style, parent = stage) {
  const e = tag === "svg" ? document.createElementNS("http://www.w3.org/2000/svg", "svg") : document.createElement(tag);
  if (cls) e.setAttribute("class", cls);
  Object.assign(e.style, style || {});
  parent.appendChild(e);
  return e;
}
function masked(text, style, parent = stage) {
  const o = el("div", "mask", style, parent), i = el("div", "inner", {}, o);
  i.textContent = text;
  return { o, i };
}
function reveal(m, p) { m.i.style.transform = `translateY(${(1 - p) * 115}%)`; }
// ---------------------------------------------------------------- icons (64 x 64 line drawings)
const ICONS = {
  thermometer: [["path", "M27 37.5 V13 a5 5 0 0 1 10 0 V37.5 a10 10 0 1 1 -10 0 Z", 0],
                ["path", "M43 16 h6 M43 23 h6 M43 30 h6", 0], ["path", "M32 44 V24", 1], ["circle", [32, 46, 4.2], 2]],
  pin: [["path", "M32 58 C24 47 14 37 14 25 a18 18 0 0 1 36 0 C50 37 40 47 32 58 Z", 0], ["circle", [32, 25, 6.5], 1]],
  alarm: [["circle", [32, 35, 19], 0], ["path", "M12 18 a9 9 0 0 1 12 -9 M40 9 a9 9 0 0 1 12 9", 0],
          ["path", "M19 51 l-5 6 M45 51 l5 6", 0], ["path", "M32 24 V35 L39.5 40", 1]],
};
function icon(name, x, y, size) {
  const s = el("svg", null, { position: "absolute", left: x + "px", top: y + "px", width: size + "px", height: size + "px", overflow: "visible" });
  s.setAttribute("viewBox", "0 0 64 64");
  const parts = ICONS[name].map(([kind, d, role]) => {
    const e = document.createElementNS("http://www.w3.org/2000/svg", kind);
    if (kind === "path") e.setAttribute("d", d);
    else { e.setAttribute("cx", d[0]); e.setAttribute("cy", d[1]); e.setAttribute("r", d[2]); }
    e.setAttribute("stroke", role === 0 ? "rgba(255,255,255,0.88)" : C.yellow);
    e.setAttribute("stroke-width", role === 2 ? 0 : 3.4);
    if (role === 2) e.setAttribute("fill", C.yellow);
    s.appendChild(e);
    return { e, role };
  });
  return { s, parts };
}
function drawIcon(ic, p) {                            // outlines draw on, then accents, then the filled dot
  ic.parts.forEach(({ e, role }) => {
    if (role === 2) { e.style.opacity = ease.outCubic(prog(p, 0.75, 0.25)); return; }
    const len = e.getTotalLength(), q = role === 0 ? ease.inOutCubic(clamp(p / 0.75)) : ease.outCubic(prog(p, 0.45, 0.45));
    e.style.strokeDasharray = `${len} ${len}`;
    e.style.strokeDashoffset = `${len * (1 - q)}`;
  });
}
// ---------------------------------------------------------------- sentence with word masks and highlight groups
function sentence(src, x, y, size, parent = stage) {
  const box = el("div", "sent", { left: x + "px", top: y + "px", fontSize: size + "px" }, parent);
  const words = [], groups = [];
  const re = /\{([^}|]+)(?:\|(\w))?\}|([^{\s]+)|(\s+)/g;
  let m;
  while ((m = re.exec(src))) {
    if (m[4]) { box.appendChild(document.createTextNode(" ")); continue; }
    const host = m[1] ? el("span", "hl", {}, box) : box;
    const text = m[1] || m[3];
    const ws = text.split(" ");
    ws.forEach((w, k) => {
      if (k) host.appendChild(document.createTextNode(" "));
      const wm = el("span", "wm", {}, host), wi = el("span", "wi", {}, wm);
      wi.textContent = w;
      words.push(wi);
      if (m[1]) wi.dataset.g = groups.length;
    });
    if (m[1]) {
      const mk = el("span", "mk", { background: m[2] === "t" ? C.cyan : C.yellow }, host);
      host.insertBefore(mk, host.firstChild);
      groups.push({ host, mk, words: words.filter(w => w.dataset.g == groups.length), kind: m[2] || "v" });
    }
  }
  return { box, words, groups };
}
// ---------------------------------------------------------------- build
let S = null;
window.init = function (cues) {
  const c = cues;
  const rows = [
    { lab: "Facts & general truths", ex: "Water {freezes} at 0°C.", ic: "thermometer", c1: c.facts, c2: c.water, verb: c.freezes },
    { lab: "True now", ex: "I {live} in Tsing Yi.", ic: "pin", c1: c.things, c2: c.live, verb: c.live },
    { lab: "Habits", ex: "Richard {wakes up} at 7 a.m. {every day|t}.", ic: "alarm", c1: c.habits, c2: c.richard, verb: c.wakes },
  ];
  // panel
  el("div", null, { position: "absolute", left: PANEL.x + "px", top: PANEL.y + "px", width: PANEL.w + "px", height: PANEL.h + "px",
    borderRadius: "28px", boxSizing: "border-box", border: "1.5px solid rgba(255,255,255,0.14)",
    background: "linear-gradient(180deg, rgba(255,255,255,0.075), rgba(255,255,255,0.028))",
    boxShadow: "0 30px 80px rgba(6,2,28,0.45), inset 0 1px 0 rgba(255,255,255,0.10)" });
  const content = el("div", null, { position: "absolute", inset: "0" });
  // title + counter + header rule
  const title = masked("Simple present", { left: L + "px", top: "176px", fontFamily: "Fredoka", fontWeight: 600, fontSize: "58px",
    color: C.white, lineHeight: "1" }, content);
  const cnt = el("div", "num", { position: "absolute", top: "192px", right: (1920 - R) + "px", fontSize: "30px", lineHeight: "1",
    display: "flex", alignItems: "flex-start", color: "rgba(255,255,255,0.45)" }, content);
  const cntMask = el("div", null, { position: "relative", overflow: "hidden", height: "36px", width: "38px", marginRight: "10px" }, cnt);
  const cntStrip = el("div", null, { position: "absolute", left: "0", top: "0", color: C.yellow, lineHeight: "36px" }, cntMask);
  cntStrip.innerHTML = "01<br>02<br>03";
  const cntTot = el("div", null, { lineHeight: "36px" }, cnt); cntTot.textContent = "/ 03";
  const rule0 = el("div", null, { position: "absolute", left: L + "px", top: "266px", width: (R - L) + "px", height: "2px",
    background: "rgba(255,255,255,0.18)", transformOrigin: "left center" }, content);
  // rail (progress indicator) in the left margin
  const railX = 86;
  const rail = el("div", null, { position: "absolute", left: railX + "px", top: (ROW_Y[0] + 26) + "px", width: "2px",
    height: (ROW_Y[2] + ROW_H - 26 - ROW_Y[0] - 26) + "px", background: "rgba(255,255,255,0.10)", transformOrigin: "center top" }, content);
  const act = el("div", null, { position: "absolute", left: (railX - 1) + "px", width: "4px", borderRadius: "2px", background: C.yellow,
    boxShadow: "0 0 14px rgba(255,217,61,0.65)" }, content);
  // rows
  const R_ = rows.map((r, i) => {
    const y = ROW_Y[i];
    const g = el("div", null, { position: "absolute", inset: "0" }, content);
    const num = masked(String(i + 1).padStart(2, "0"), { left: L + "px", top: (y + 30) + "px", fontFamily: "Fredoka", fontWeight: 600,
      fontSize: "30px", color: C.yellow, lineHeight: "1" }, g);
    const lab = masked(r.lab, { left: COL + "px", top: (y + 34) + "px", fontSize: "22px", color: C.lilac, lineHeight: "1" }, g);
    lab.o.classList.add("label");
    const ic = icon(r.ic, R - 58, y + 18, 58); g.appendChild(ic.s);
    const sn = sentence(r.ex, COL, y + 82, 46, g);
    const rule = el("div", null, { position: "absolute", left: L + "px", top: (y + ROW_H) + "px", width: (R - L) + "px", height: "2px",
      background: "rgba(255,255,255,0.10)", transformOrigin: "left center" }, g);
    return Object.assign({}, r, { y, g, num, lab, ic, sn, rule });
  });
  // fit all sentences to one size that leaves 24 px clear of the panel's inner right edge
  let size = 46;
  const widest = () => Math.max(...R_.map(r => r.sn.box.getBoundingClientRect().width));
  while (COL + widest() > R - 4 && size > 34) { size -= 1; R_.forEach(r => (r.sn.box.style.fontSize = size + "px")); }
  // habit words
  const hlab = masked("Habit words that go with the simple present:", { left: COL + "px", top: "866px", fontFamily: "Nunito",
    fontWeight: 700, fontSize: "24px", color: C.dim, lineHeight: "1" }, content);
  const tags = [];
  let tx = COL;
  ["every day", "often", "usually", "always"].forEach(w => {
    const tg = el("div", "tag", { left: tx + "px", top: "904px" }, content);
    tg.textContent = w;
    tags.push(tg);
    tx += tg.getBoundingClientRect().width + 16;
  });
  // shared-element start: the 'every day' group in sentence 3
  const evg = R_[2].sn.groups.find(g => g.kind === "t");
  const a = evg.host.getBoundingClientRect(), b = tags[0].getBoundingClientRect();
  const sc0 = a.height / b.height * 0.92;
  const tagFrom = { dx: a.left - 0.09 * size - b.left, dy: a.top + a.height / 2 - (b.top + b.height * sc0 / 2), sc: sc0 };
  S = { c, rows: R_, title, cntStrip, cnt, rule0, rail, act, hlab, tags, tagFrom, content, size };
  return { size, tagFrom };
};
// ---------------------------------------------------------------- per-frame state
window.seek = function (t) {
  const { c, rows } = S;
  const review = c.voice_end + 0.35, exit0 = c.dur - 0.45;
  // title, counter, header rule
  reveal(S.title, ease.outExpo(prog(t, 0.05, 0.8)));
  S.rule0.style.transform = `scaleX(${ease.outExpo(prog(t, 0.2, 1.0))})`;
  const active = t < rows[1].c1 ? 0 : t < rows[2].c1 ? 1 : 2;
  S.cnt.style.opacity = ease.outCubic(prog(t, rows[0].c1, 0.4));
  let ci = 0;
  rows.forEach((r, i) => { if (i > 0) ci += ease.outExpo(prog(t, r.c1, 0.6)); });
  S.cntStrip.style.transform = `translateY(${-36 * ci}px)`;
  // rail + active segment (springs between rows; grows over all rows for the review)
  S.rail.style.transform = `scaleY(${ease.outExpo(prog(t, rows[0].c1, 1.0))})`;
  let top = rows[0].y + 26, bot = rows[0].y + ROW_H - 26;
  rows.forEach((r, i) => {
    if (i === 0) return;
    const p = spring(t - r.c1);
    top = lerp(top, r.y + 26, p); bot = lerp(bot, r.y + ROW_H - 26, p);
  });
  const pr = ease.inOutCubic(prog(t, review, 0.7));
  top = lerp(top, rows[0].y + 26, pr);
  const grow = ease.outExpo(prog(t, rows[0].c1, 0.6));
  S.act.style.top = top + "px";
  S.act.style.height = Math.max(0, (bot - top) * grow) + "px";
  S.act.style.opacity = grow;
  // rows
  rows.forEach((r, i) => {
    const pin = prog(t, r.c1, 0.7);
    reveal(r.num, ease.outExpo(pin));
    reveal(r.lab, ease.outExpo(prog(t, r.c1 + 0.06, 0.7)));
    drawIcon(r.ic, prog(t, r.c1 + 0.1, 1.0));
    r.rule.style.transform = `scaleX(${ease.outExpo(prog(t, r.c1 + 0.2, 1.0))})`;
    const t0 = r.c2 - 0.12;
    r.sn.words.forEach((w, k) => { w.style.transform = `translateY(${(1 - ease.outExpo(prog(t, t0 + k * 0.05, 0.6))) * 115}%)`; });
    r.sn.groups.forEach(g => {
      const k0 = r.sn.words.indexOf(g.words[g.words.length - 1]);
      const landed = t0 + k0 * 0.05 + 0.3;
      const ts = g.kind === "t" ? c.every : Math.max(r.verb, landed);
      const p = ease.outCubic(prog(t, ts, g.kind === "t" ? 0.35 : 0.42));
      g.mk.style.transform = `scaleX(${p})`;
      g.mk.style.boxShadow = `0 0 ${18 * p}px ${g.kind === "t" ? "rgba(46,230,255,0.35)" : "rgba(255,217,61,0.35)"}`;
      const q = prog(p, 0.3, 0.5);
      g.words.forEach(w => (w.style.color = mix(C.white, C.ink, q)));
    });
    // focus: dim this row while a later row is being explained, restore for the review
    let dim = 0;
    if (c.dim !== false && i < rows.length - 1) dim = ease.inOutCubic(prog(t, rows[i + 1].c1, 0.5));
    dim *= 1 - ease.inOutCubic(prog(t, review, 0.6));
    r.g.style.opacity = 1 - 0.6 * dim;
  });
  // habit words: label, then 'every day' travels down from the sentence, then the other tags
  reveal(S.hlab, ease.outExpo(prog(t, c.every + 0.1, 0.7)));
  const f = S.tagFrom, pt = ease.inOutCubic(prog(t, c.every + 0.36, 0.45));
  const t0g = S.tags[0];
  t0g.style.opacity = clamp(prog(t, c.every + 0.36, 0.12));
  t0g.style.transform = `translate(${f.dx * (1 - pt)}px, ${f.dy * (1 - pt)}px) scale(${lerp(f.sc, 1, pt)})`;
  S.tags.slice(1).forEach((tg, k) => {
    const p = prog(t, c.every + 0.68 + k * 0.12, 0.5);
    tg.style.opacity = ease.outCubic(clamp(p * 2));
    tg.style.transform = `translateY(${(1 - ease.outBack(p)) * 22}px) scale(${lerp(0.9, 1, ease.outBack(p))})`;
  });
  // exit: everything except the panel lifts and fades, top to bottom
  const pe = ease.inCubic(prog(t, exit0, 0.42));
  S.content.style.opacity = 1 - pe;
  S.content.style.transform = `translateY(${-16 * pe}px)`;
  return true;
};
window.ready = Promise.all(["600 58px Fredoka", "800 30px Nunito", "700 22px Nunito"]
  .map(f => document.fonts.load(f))).then(() => document.fonts.ready).then(() =>
  document.fonts.check("800 30px Nunito") && document.fonts.check("600 58px Fredoka"));
const _init = window.init;
window.init = function (cues) {
  for (const k of ["facts", "water", "things", "live", "habits", "richard", "every", "freezes", "wakes"]) cues[k] = cue(k);
  cues.panel_right = cues.panel.map(p => p[0]);
  const info = _init(cues);
  const c = cues;
  [c.facts, c.things, c.habits].forEach(t => fx(t, "whoosh", 0.4));
  fx(c.every + 0.36, "whoosh", 0.22);
  for (let k = 0; k < 3; k++) fx(c.every + 0.68 + k * 0.12 + 0.12, "pop", 0.4);
  return info;
};
})();
