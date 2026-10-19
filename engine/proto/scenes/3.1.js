"use strict";
// 3.1 Non-action verbs — design-led category sequence.
(() => {
  document.head.insertAdjacentHTML("beforeend", `<style>
    .na-root { position:absolute; inset:0; }
    .na-zone { position:absolute; height:62px; padding:0 23px; display:flex; align-items:center; box-sizing:border-box;
      border:2px solid #FF4FA8; border-radius:14px; color:#FF4FA8; background:rgba(255,79,168,.10);
      box-shadow:0 0 18px rgba(255,79,168,.28); font-family:Fredoka; font-weight:600; font-size:29px; letter-spacing:.035em; word-spacing:.12em; white-space:nowrap; }
    .na-row { position:absolute; box-sizing:border-box; border-radius:20px; border:1.5px solid; background:rgba(255,255,255,.035); overflow:hidden; }
    .na-row::before { content:""; position:absolute; left:0; top:19px; bottom:19px; width:4px; border-radius:2px; background:currentColor; }
    .na-num { position:absolute; font-family:Fredoka; font-weight:600; font-size:30px; line-height:1; font-feature-settings:"tnum" 1; }
    .na-label { position:absolute; font-family:Nunito; font-weight:900; font-size:21px; letter-spacing:.14em; line-height:1; }
    .na-verb { position:absolute; height:46px; padding:0 18px; display:flex; align-items:center; box-sizing:border-box; border-radius:23px;
      background:#fff; color:#281450; font-family:Nunito; font-weight:900; font-size:28px; line-height:1; transform-origin:center center; white-space:nowrap; }
    .na-counter { position:absolute; display:flex; align-items:flex-start; font-family:Fredoka; font-weight:600; font-size:30px; line-height:1; color:rgba(255,255,255,.45); }
    .na-counter-mask { position:relative; overflow:hidden; width:39px; height:36px; margin-right:10px; }
    .na-counter-strip { position:absolute; left:0; top:0; color:#FFD93D; line-height:36px; }
    .na-icon svg path, .na-icon svg circle { stroke-linecap:round; stroke-linejoin:round; }
  </style>`);

  // Icons unique to this scene; roles match lib.js's drawIcon contract.
  ICONS.heart = [["path", "M32 55 C25 47 11 37 11 24 A12 12 0 0 1 32 16 A12 12 0 0 1 53 24 C53 37 39 47 32 55 Z", 0]];
  ICONS.bulb = [["path", "M20 28 a12 12 0 1 1 24 0 c0 7 -5 9 -7 15 H27 c-2 -6 -7 -8 -7 -15 Z", 0], ["path", "M27 49 h10 M28 55 h8", 1]];
  ICONS.eye = [["path", "M7 32 C14 20 23 15 32 15 C41 15 50 20 57 32 C50 44 41 49 32 49 C23 49 14 44 7 32 Z", 0], ["circle", [32,32,7], 1]];
  ICONS.gift = [["path", "M12 28 h40 v27 H12 Z M9 21 h46 v9 H9 Z M32 21 v34", 0], ["path", "M32 21 C22 21 17 18 17 13 a6 6 0 0 1 11 -3 l4 11 M32 21 C42 21 47 18 47 13 a6 6 0 0 0 -11 -3 l-4 11", 1]];

  const PANEL = { x:60, y:130, h:900 }, L=116, COL=196, R=1114;
  let S = null;

  window.init = function(c) {
    const pn = panel(PANEL.x, PANEL.y, R - PANEL.x, PANEL.h);
    const root = el("div", "na-root");
    const title = masked("Non-action verbs", { left:L+"px", top:"176px", fontFamily:"Fredoka", fontWeight:600, fontSize:"58px", color:C.white, lineHeight:"1", wordSpacing:".11em" }, root);
    const sub = [
      { m:masked("feelings", { left:L+"px", top:"246px", fontFamily:"Nunito", fontWeight:700, fontSize:"25px", color:C.dim, lineHeight:"1" }, root), k:"feelings" },
      { m:masked("·", { left:"239px", top:"246px", fontFamily:"Nunito", fontWeight:700, fontSize:"25px", color:C.dim, lineHeight:"1" }, root), k:"opinions", lead:.08 },
      { m:masked("opinions", { left:"267px", top:"246px", fontFamily:"Nunito", fontWeight:700, fontSize:"25px", color:C.dim, lineHeight:"1" }, root), k:"opinions" },
      { m:masked("·", { left:"391px", top:"246px", fontFamily:"Nunito", fontWeight:700, fontSize:"25px", color:C.dim, lineHeight:"1" }, root), k:"states", lead:.08 },
      { m:masked("states", { left:"419px", top:"246px", fontFamily:"Nunito", fontWeight:700, fontSize:"25px", color:C.dim, lineHeight:"1" }, root), k:"states" },
    ];
    const rule = hrule(L, 286, R-L, .18, root);
    const zone = el("div", "na-zone", { left:"736px", top:"181px" }, root); zone.textContent="NO -ing ZONE";
    const counter = el("div", "na-counter", { left:"1002px", top:"192px" }, root);
    const cmask = el("div", "na-counter-mask", {}, counter);
    const cstrip = el("div", "na-counter-strip", {}, cmask); cstrip.innerHTML="01<br>02<br>03<br>04";
    const ctotal = el("div", null, { lineHeight:"36px" }, counter); ctotal.textContent="/ 04";
    zone.style.left = `${Math.round(1002 - 40 - zone.getBoundingClientRect().width)}px`;   // 40 px clear of the counter
    const rail = el("div", null, { position:"absolute", left:"85px", top:"349px", width:"2px", height:"548px", background:"rgba(255,255,255,.10)", transformOrigin:"center top" }, root);
    const active = el("div", null, { position:"absolute", left:"84px", width:"4px", borderRadius:"2px", background:C.cyan, boxShadow:"0 0 14px rgba(46,230,255,.60)" }, root);
    const defs = [
      { label:"FEELINGS", colour:"#FF4FA8", icon:"heart", verbs:["like","want"], y:330 },
      { label:"THINKING", colour:"#FFD93D", icon:"bulb", verbs:["think","know"], y:474 },
      { label:"SENSES", colour:"#2EE6FF", icon:"eye", verbs:["see","smell"], y:618 },
      { label:"OWNING", colour:"#5CF2B0", icon:"gift", verbs:["have"], y:762 },
    ];
    const rows = defs.map((d,i) => {
      const g = el("div", null, { position:"absolute", inset:"0" }, root);
      const card = el("div", "na-row", { left:COL+"px", top:d.y+"px", width:"858px", height:"122px", borderColor:d.colour, color:d.colour }, g);
      const num = masked(String(i+1).padStart(2,"0"), { left:L+"px", top:(d.y+43)+"px", fontFamily:"Fredoka", fontWeight:600, fontSize:"30px", color:d.colour, lineHeight:"1" }, g);
      const lab = el("div", "na-label", { left:"36px", top:"26px", color:d.colour }, card); lab.textContent=d.label;
      const ic = icon(d.icon, COL+766, d.y+31, 58, "rgba(255,255,255,.88)", d.colour, g, 3.2); ic.s.classList.add("na-icon");
      let x=COL+36;
      const verbEls = d.verbs.map(v => {
        const e=el("div", "na-verb", { left:x+"px", top:(d.y+64)+"px" }, g); e.textContent=v;
        x += e.getBoundingClientRect().width + 14;
        return { v, e };
      });
      return Object.assign({},d,{g,card,num,lab,ic,verbEls,t0:c[d.verbs[0]]});
    });
    S={c,pn,root,title,sub,rule,zone,counter,cstrip,rail,active,rows};
    return { categories:rows.length };
  };

  window.seek = function(t) {
    const {c,rows}=S;
    followPanel(S.pn,t,PANEL.x);
    reveal(S.title,ease.outExpo(prog(t,c.non-.10,.75)));
    S.sub.forEach(o=>reveal(o.m,ease.outExpo(prog(t,c[o.k]+(o.lead||0),.55))));
    S.rule.style.transform=`scaleX(${ease.outExpo(prog(t,c.non+.12,1.0))})`;
    const z=ease.outExpo(prog(t,c.dont-.08,.55)); S.zone.style.opacity=z; S.zone.style.transform=`translateY(${(1-z)*14}px)`;
    S.counter.style.opacity=ease.outCubic(prog(t,rows[0].t0,.35));
    let ci=0; rows.forEach((r,i)=>{if(i)ci+=ease.outExpo(prog(t,r.t0,.55));}); S.cstrip.style.transform=`translateY(${-36*ci}px)`;
    S.rail.style.transform=`scaleY(${ease.outExpo(prog(t,rows[0].t0,.8))})`;
    let top=rows[0].y+23, bot=rows[0].y+99;
    rows.forEach((r,i)=>{if(!i)return; const p=spring(t-r.t0); top=lerp(top,r.y+23,p); bot=lerp(bot,r.y+99,p);});
    const review=c.voice_end+.35, rp=ease.inOutCubic(prog(t,review,.6)); top=lerp(top,rows[0].y+23,rp); bot=lerp(bot,rows[3].y+99,rp);
    const grow=ease.outExpo(prog(t,rows[0].t0,.5)); S.active.style.top=top+"px"; S.active.style.height=Math.max(0,(bot-top)*grow)+"px"; S.active.style.opacity=grow;
    rows.forEach((r,i)=>{
      const p=ease.outExpo(prog(t,r.t0-.08,.6)); r.card.style.opacity=p; r.card.style.transform=`translateY(${(1-p)*14}px)`;
      reveal(r.num,ease.outExpo(prog(t,r.t0,.55)));
      r.lab.style.opacity=p; r.lab.style.transform=`translateY(${(1-p)*10}px)`;
      drawIcon(r.ic,prog(t,r.t0+.08,.8));
      r.verbEls.forEach(({v,e})=>{ const q=ease.outBack(prog(t,c[v],.42)); e.style.opacity=clamp(q*1.5); e.style.transform=`translateY(${(1-q)*16}px) scale(${lerp(.88,1,q)})`; });
      let dim=0; if(i<rows.length-1) dim=ease.inOutCubic(prog(t,rows[i+1].t0,.5))*(1-ease.inOutCubic(prog(t,review,.6)));
      r.g.style.opacity=1-.6*dim;
    });
    exitLift(S.root,t);
    return true;
  };

  const _init=window.init;
  window.init=function(c) {
    const M={non:["non action",1],feelings:["feelings",1],opinions:["opinions",1],states:["states",1],dont:["dont",1],like:["like",1],want:["want",1],think:["think",1],know:["know",1],see:["see",1],smell:["smell",1],have:["have",1]};
    for(const [k,[p,n]] of Object.entries(M)) c[k]=cue(p,n);
    const info=_init(c);
    fx(c.dont,"glitch",.5);
    ["like","want","think","know","see","smell","have"].forEach(k=>fx(c[k],"pop",.6));
    return info;
  };
})();
