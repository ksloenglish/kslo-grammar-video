"use strict";
// Kayla's Grammar Lab: shared design-led motion library (plain JS, time-driven, deterministic).
// Every scene page defines window.init(cues) and window.seek(t); render_gfx.py screenshots each frame.

// ---------------------------------------------------------------- palette, easing
const C = { yellow: "#FFD93D", cyan: "#2EE6FF", pink: "#FF4FA8", lilac: "#C0A6FF", dim: "#CDC3F0", ink: "#281450",
            white: "#FFFFFF" };
const GLOW = { yellow: "rgba(255,217,61,0.35)", cyan: "rgba(46,230,255,0.35)", pink: "rgba(255,79,168,0.40)" };
const MARK = { v: "yellow", y: "yellow", t: "cyan", p: "pink" };      // highlight keys in sentence markup
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
function spring(s, w = 15, z = 0.68) {               // damped spring, s = seconds since start, 0 -> ~1.05 -> 1
  if (s <= 0) return 0;
  const wd = w * Math.sqrt(1 - z * z);
  return 1 - Math.exp(-z * w * s) * (Math.cos(wd * s) + (z * w / wd) * Math.sin(wd * s));
}
function mix(c1, c2, p) {
  const a = [1, 3, 5].map(i => parseInt(c1.slice(i, i + 2), 16)), b = [1, 3, 5].map(i => parseInt(c2.slice(i, i + 2), 16));
  return `rgb(${a.map((v, i) => Math.round(lerp(v, b[i], p))).join(",")})`;
}
// ---------------------------------------------------------------- DOM helpers
const stage = document.getElementById("stage");
const SVGNS = "http://www.w3.org/2000/svg";
function el(tag, cls, style, parent = stage) {
  const e = tag === "svg" ? document.createElementNS(SVGNS, "svg") : document.createElement(tag);
  if (cls) e.setAttribute("class", cls);
  Object.assign(e.style, style || {});
  parent.appendChild(e);
  return e;
}
function masked(text, style, parent = stage) {       // text that rises through an invisible mask
  const o = el("div", "mask", style, parent), i = el("div", "inner", {}, o);
  i.textContent = text;
  return { o, i };
}
function reveal(m, p) { m.i.style.transform = `translateY(${(1 - p) * 115}%)`; }
function panel(x, y, w, h, parent = stage) {
  return el("div", null, { position: "absolute", left: x + "px", top: y + "px", width: w + "px", height: h + "px",
    borderRadius: "28px", boxSizing: "border-box", border: "1.5px solid rgba(255,255,255,0.14)",
    background: "linear-gradient(180deg, rgba(255,255,255,0.075), rgba(255,255,255,0.028))",
    boxShadow: "0 30px 80px rgba(6,2,28,0.45), inset 0 1px 0 rgba(255,255,255,0.10)" }, parent);
}
function hrule(x, y, w, alpha, parent = stage) {
  return el("div", null, { position: "absolute", left: x + "px", top: y + "px", width: w + "px", height: "2px",
    background: `rgba(255,255,255,${alpha})`, transformOrigin: "left center" }, parent);
}
// ---------------------------------------------------------------- line icons (64 x 64), role 0 outline, 1 accent, 2 fill
const ICONS = {
  thermometer: [["path", "M27 37.5 V13 a5 5 0 0 1 10 0 V37.5 a10 10 0 1 1 -10 0 Z", 0],
                ["path", "M43 16 h6 M43 23 h6 M43 30 h6", 0], ["path", "M32 44 V24", 1], ["circle", [32, 46, 4.2], 2]],
  pin: [["path", "M32 58 C24 47 14 37 14 25 a18 18 0 0 1 36 0 C50 37 40 47 32 58 Z", 0], ["circle", [32, 25, 6.5], 1]],
  alarm: [["circle", [32, 35, 19], 0], ["path", "M12 18 a9 9 0 0 1 12 -9 M40 9 a9 9 0 0 1 12 9", 0],
          ["path", "M19 51 l-5 6 M45 51 l5 6", 0], ["path", "M32 24 V35 L39.5 40", 1]],
  clock: [["circle", [32, 32, 24], 0], ["path", "M32 14 v4 M50 32 h-4 M32 50 v-4 M14 32 h4", 0],
          ["path", "M32 32 V19 M32 32 H43", 1], ["circle", [32, 32, 2.6], 2]],
  bolt: [["path", "M37 4 L15 36 H30 L25 60 L49 25 H34 Z", 0]],
  tick: [["path", "M13 34 L26 47 L51 18", 0]],
  cross: [["path", "M18 18 L46 46 M46 18 L18 46", 0]],
  arrow: [["path", "M8 32 H52 M38 18 L52 32 L38 46", 0]],
  question: [["path", "M22 23 a10 10 0 1 1 14.5 8.9 c-3 1.6 -4.5 3.8 -4.5 7.1 v2", 0], ["circle", [32, 50.5, 3], 2]],
  book: [["path", "M8 15 C18 11 26 12 32 17 C38 12 46 11 56 15 V52 C46 48 38 49 32 54 C26 49 18 48 8 52 Z", 0],
         ["path", "M32 17 V54", 1]],
  star: [["path", "M32 7 L39.3 23.6 L57 25.4 L43.6 37.4 L47.5 55 L32 45.8 L16.5 55 L20.4 37.4 L7 25.4 L24.7 23.6 Z", 0]],
};
function icon(name, x, y, size, outline = "rgba(255,255,255,0.88)", accent = C.yellow, parent = stage, sw = 3.4) {
  const s = el("svg", null, { position: "absolute", left: x + "px", top: y + "px", width: size + "px", height: size + "px",
    overflow: "visible" }, parent);
  s.setAttribute("viewBox", "0 0 64 64");
  const parts = ICONS[name].map(([kind, d, role]) => {
    const e = document.createElementNS(SVGNS, kind);
    if (kind === "path") e.setAttribute("d", d);
    else { e.setAttribute("cx", d[0]); e.setAttribute("cy", d[1]); e.setAttribute("r", d[2]); }
    e.setAttribute("stroke", role === 0 ? outline : accent);
    e.setAttribute("stroke-width", role === 2 ? 0 : sw);
    e.setAttribute("fill", role === 2 ? accent : "none");
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
// ---------------------------------------------------------------- badge icons: Phosphor duotone (icons.js PH) in a tinted tile
function rgba(hex, a) { const v = [1, 3, 5].map(i => parseInt(hex.slice(i, i + 2), 16)); return `rgba(${v.join(",")},${a})`; }
function badge(name, x, y, size, col, parent = stage, round = false) {
  const b = el("div", null, { position: "absolute", left: x + "px", top: y + "px", width: size + "px", height: size + "px",
    boxSizing: "border-box", borderRadius: round ? "50%" : Math.round(size * 0.28) + "px", border: `2px solid ${rgba(col, 0.55)}`,
    background: `linear-gradient(150deg, ${rgba(col, 0.24)}, ${rgba(col, 0.07)})`,
    boxShadow: `0 0 ${Math.round(size * 0.28)}px ${rgba(col, 0.30)}, inset 0 1px 0 rgba(255,255,255,0.14)`,
    display: "flex", alignItems: "center", justifyContent: "center", color: col, opacity: 0 }, parent);
  const s = Math.round(size * 0.64);
  b.innerHTML = `<svg viewBox="0 0 256 256" width="${s}" height="${s}" fill="currentColor" style="overflow:visible;` +
    `filter:drop-shadow(0 0 ${Math.max(3, Math.round(size * 0.06))}px ${rgba(col, 0.6)})">${PH[name]}</svg>`;
  return b;
}
function popBadge(b, t, t0, d = 0.5) {                // fade + overshoot scale from 0.55
  const p = ease.outBack(prog(t, t0, d));
  b.style.opacity = clamp(prog(t, t0, 0.14));
  b.style.transform = `scale(${lerp(0.55, 1, Math.max(0, p))})`;
}
// ---------------------------------------------------------------- ink-centred glyphs (countdown digits, ? token)
// Centres the rendered INK box on the canvas (x = cx - (right - left) / 2), then moves `optical` of the way towards the
// ink's centre of mass so a flagged '1' sits visually centred.
function inkGlyph(cv, ch, font, fill, optical = 0.6, glow = null) {
  const ctx = cv.getContext("2d"), W = cv.width, H = cv.height;
  ctx.font = font; ctx.textBaseline = "alphabetic"; ctx.textAlign = "left"; ctx.fillStyle = fill;
  const m = ctx.measureText(ch);
  const x = W / 2 - (m.actualBoundingBoxRight - m.actualBoundingBoxLeft) / 2;
  const y = H / 2 + (m.actualBoundingBoxAscent - m.actualBoundingBoxDescent) / 2;
  ctx.clearRect(0, 0, W, H); ctx.fillText(ch, x, y);
  const px = ctx.getImageData(0, 0, W, H).data; let sx = 0, sa = 0;
  for (let i = 3; i < px.length; i += 4) if (px[i]) { sx += ((i >> 2) % W) * px[i]; sa += px[i]; }
  const dx = sa ? (W / 2 - sx / sa) * optical : 0;
  ctx.clearRect(0, 0, W, H);
  if (glow) { ctx.shadowColor = glow; ctx.shadowBlur = Math.round(H * 0.11); }
  ctx.fillText(ch, x + dx, y);
  return dx;
}
// Bold yellow '?' token (same footprint as the mint finish dot in 4.4): centre (cx, cy), diameter d.
function qToken(cx, cy, d = 126, parent = stage) {
  const q = el("div", null, { position: "absolute", left: (cx - d / 2) + "px", top: (cy - d / 2) + "px", width: d + "px", height: d + "px",
    borderRadius: "50%", background: "radial-gradient(circle at 36% 30%, #FFF2A6 0%, #FFD93D 52%, #F4AE22 100%)",
    boxShadow: `0 0 ${Math.round(d * 0.3)}px rgba(255,217,61,.62), inset 0 -${Math.round(d * 0.04)}px 0 rgba(150,80,0,.22), inset 0 2px 0 rgba(255,255,255,.55)`,
    opacity: 0, transformOrigin: "50% 50%" }, parent);
  const cv = el("canvas", null, { position: "absolute", left: "0", top: "0", width: d + "px", height: d + "px" }, q);
  cv.width = d * 2; cv.height = d * 2;              // 2x for crisp edges
  inkGlyph(cv, "?", `600 ${Math.round(d * 1.42)}px Fredoka`, "#281450", 0);
  return q;
}
function animQToken(q, t, t0, out = null) {          // pop in, gentle puzzled wobble, optional shrink-out
  const p = ease.outBack(prog(t, t0, 0.46)), o = out == null ? 0 : ease.inCubic(prog(t, out, 0.18));
  q.style.opacity = clamp(prog(t, t0, 0.12)) * (1 - o);
  const w = Math.sin((t - t0) * 3.1) * 7 * clamp(prog(t, t0 + 0.3, 0.4)), f = Math.sin((t - t0) * 2.2) * 4;
  q.style.transform = `translateY(${f}px) rotate(${w}deg) scale(${Math.max(0, p) * (1 - 0.4 * o)})`;
}
// ---------------------------------------------------------------- sentences: word masks + highlighter groups
// markup: plain words, {phrase|k} highlight group (k: v/y yellow, t cyan, p pink), "\n" = line break
function sentence(src, x, y, size, parent = stage) {
  const box = el("div", "sent", { left: x + "px", top: y + "px", fontSize: size + "px" }, parent);
  const words = [], groups = [];
  const re = /\{([^}|]+)(?:\|(\w))?\}|([^{\s]+)|(\s+)/g;
  let m;
  while ((m = re.exec(src))) {
    if (m[4]) { box.appendChild(m[4].includes("\n") ? document.createElement("br") : document.createTextNode(" ")); continue; }
    const host = m[1] ? el("span", "hl", {}, box) : box;
    const text = m[1] || m[3];
    text.split(" ").forEach((w, k) => {
      if (k) host.appendChild(document.createTextNode(" "));
      const wm = el("span", "wm", {}, host), wi = el("span", "wi", {}, wm);
      wi.textContent = w;
      words.push(wi);
      if (m[1]) wi.dataset.g = groups.length;
    });
    if (m[1]) {
      const col = MARK[m[2] || "v"];
      const mk = el("span", "mk", { background: C[col] }, host);
      host.insertBefore(mk, host.firstChild);
      groups.push({ host, mk, col, key: m[2] || "v", words: words.filter(w => w.dataset.g == groups.length) });
    }
  }
  return { box, words, groups };
}
function riseWords(sn, t, t0, stagger = 0.05) {
  sn.words.forEach((w, k) => { w.style.transform = `translateY(${(1 - ease.outExpo(prog(t, t0 + k * stagger, 0.6))) * 115}%)`; });
}
function sweep(g, t, ts, d = 0.42) {                 // highlighter sweep; text turns ink as the marker passes
  const p = ease.outCubic(prog(t, ts, d));
  g.mk.style.transform = `scaleX(${p})`;
  g.mk.style.boxShadow = `0 0 ${18 * p}px ${GLOW[g.col]}`;
  const q = prog(p, 0.3, 0.5);
  g.words.forEach(w => (w.style.color = mix(C.white, C.ink, q)));
}
// fonts load lazily, so request every face used BEFORE init() measures any text (fallback widths break layouts)
window.ready = Promise.all(["600 58px Fredoka", "800 30px Nunito", "700 22px Nunito", "900 30px Nunito"]
  .map(f => document.fonts.load(f))).then(() => document.fonts.ready).then(() =>
  document.fonts.check("800 30px Nunito") && document.fonts.check("600 58px Fredoka"));

// ---------------------------------------------------------------- scene runtime (used with shell.html)
let CUES = null;                                     // set by boot(); all times are scene-local seconds
const SFX = [];                                      // [t, name, gain]; names = files in audio/sfx/*.wav
function fx(t, name, gain = 1) { SFX.push([Math.round(t * 1000) / 1000, name, gain]); }
const _norm = s => s.toLowerCase().replace(/[^a-z0-9]/g, "");
// time of the n-th occurrence of a phrase in the scene's voice (word START; end=true -> last word's END)
function cue(phrase, n = 1, end = false) {
  const ws = CUES.words.map(w => _norm(w[0])), ph = phrase.split(/\s+/).map(_norm);
  let k = 0;
  for (let i = 0; i + ph.length <= ws.length; i++) {
    if (ph.every((p, j) => ws[i + j] === p) && ++k === n) return end ? CUES.words[i + ph.length - 1][2] : CUES.words[i][1];
  }
  throw new Error(`${CUES.sid}: '${phrase}' #${n} not in: ${CUES.words.map(w => w[0]).join(" ")}`);
}
const _fi = (t, arr) => arr[clamp(Math.round(t * CUES.fps), 0, arr.length - 1)];
function panelAt(t) { const p = _fi(t, CUES.panel); return { right: p[0], alpha: p[1] }; }
function kaylaAt(t) { const k = _fi(t, CUES.kayla); return { cx: k[0], top: k[1], h: k[2] }; }
// glass panel that follows the engine's layout (its right edge moves with Kayla; alpha 0 in the 'large' layout)
function followPanel(pn, t, x0 = 60) { const p = panelAt(t); pn.style.width = (p.right - x0) + "px"; pn.style.opacity = p.alpha; return p; }
// standard exit: content lifts 16 px and fades out over 0.42 s from dur - 0.45
function exitLift(node, t, d = 0.42) {
  const pe = ease.inCubic(prog(t, CUES.dur - 0.45, d));
  node.style.opacity = 1 - pe; node.style.transform = `translateY(${-16 * pe}px)`;
}
window.boot = function (cues) {
  CUES = cues; SFX.length = 0;
  const info = window.init(cues);
  window.seek(0);
  return { info: info === undefined ? null : info, sfx: SFX.slice() };
};
