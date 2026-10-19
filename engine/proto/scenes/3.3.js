"use strict";
// 3.3 Plot twist — large opening then an adaptive standard-layout contrast system.
(() => {
  document.head.insertAdjacentHTML("beforeend", `<style>
    .tw-root, .tw-early, .tw-standard { position:absolute; inset:0; }
    .tw-card { position:absolute; width:390px; height:148px; box-sizing:border-box; border:1.5px solid; border-radius:20px; background:rgba(255,255,255,.04); overflow:hidden; }
    .tw-card::before { content:""; position:absolute; left:0; top:22px; bottom:22px; width:4px; border-radius:2px; background:currentColor; }
    .tw-word { position:absolute; font-family:Fredoka; font-weight:600; font-size:38px; line-height:1; letter-spacing:.02em; word-spacing:.16em; }
    .tw-meaning { position:absolute; font-family:Nunito; font-weight:800; font-size:25px; color:#fff; line-height:1; }
    .tw-card svg path, .tw-card svg circle { stroke-linecap:round; stroke-linejoin:round; }
  </style>`);

  ICONS.bulb = [["path", "M20 28 a12 12 0 1 1 24 0 c0 7 -5 9 -7 15 H27 c-2 -6 -7 -8 -7 -15 Z", 0], ["path", "M27 49 h10 M28 55 h8", 1]];
  ICONS.gears = [["path", "M32 14 l3 5 6 1 3 -4 5 5 -4 3 1 6 5 3 v7 l-5 3 -1 6 4 3 -5 5 -3 -4 -6 1 -3 5 h-7 l-3 -5 -6 -1 -3 4 -5 -5 4 -3 -1 -6 -5 -3 v-7 l5 -3 1 -6 -4 -3 5 -5 3 4 6 -1 3 -5 Z", 0], ["circle", [32,32,8], 1]];
  ICONS.family = [["circle", [32,20,8], 0], ["circle", [17,29,6], 0], ["circle", [47,29,6], 0], ["path", "M19 54 v-8 a13 13 0 0 1 26 0 v8 M7 54 v-5 a10 10 0 0 1 14 -9 M57 54 v-5 a10 10 0 0 0 -14 -9", 1]];
  ICONS.sushi = [["circle", [32,32,22], 0], ["circle", [32,32,14], 1], ["path", "M24 25 l5 4 5 -5 7 7 -6 7 -7 -4 -5 4 -3 -7 Z", 1]];

  const PANEL={x:60,y:130,h:900}, L=116, R=1114;
  let S=null;

  window.init=function(c){
    const pn=panel(PANEL.x,PANEL.y,R-PANEL.x,PANEL.h);
    const root=el("div","tw-root");
    const early=el("div","tw-early",{},root);
    const big=masked("PLOT TWIST!",{left:"96px",top:"430px",fontFamily:"Fredoka",fontWeight:600,fontSize:"68px",color:C.yellow,lineHeight:"1",letterSpacing:".02em",wordSpacing:".16em",textShadow:"0 0 18px rgba(255,79,168,.55)"},early);
    const standard=el("div","tw-standard",{},root);
    // The title and the explanatory line deliberately share L exactly.
    const title=masked("PLOT TWIST!",{left:L+"px",top:"176px",fontFamily:"Fredoka",fontWeight:600,fontSize:"54px",color:C.yellow,lineHeight:"1",letterSpacing:".02em",wordSpacing:".16em"},standard);
    const line=masked("Some can take -ing when they are actions.",{left:L+"px",top:"237px",fontFamily:"Nunito",fontWeight:700,fontSize:"30px",color:C.dim,lineHeight:"1"},standard);
    const rule=hrule(L,281,R-L,.18,standard);
    const defs=[
      { y:326, word:"THINK", meaning:"= opinion", icon:"bulb", colour:C.yellow, word2:"THINKING", meaning2:"= using your brain", icon2:"gears", colour2:C.pink, leftAt:c.what, rightAt:c.action, ex:"What {is|p} she {thinking|p} now?", exAt:c.what, marks:[c.is,c.thinking] },
      { y:654, word:"HAVE", meaning:"= own", icon:"family", colour:C.yellow, word2:"HAVING", meaning2:"= eating", icon2:"sushi", colour2:C.pink, leftAt:c.we, rightAt:c.means, ex:"We {were having|p} dinner at a Japanese restaurant.", exAt:c.we, marks:[c.were] },
    ];
    const rows=defs.map(d=>{
      const g=el("div",null,{position:"absolute",inset:"0"},standard);
      const makeCard=(x,word,meaning,ic,col)=>{
        const card=el("div","tw-card",{left:x+"px",top:d.y+"px",borderColor:col,color:col},g);
        const iconObj=icon(ic,x+28,d.y+43,52,"rgba(255,255,255,.88)",col,g,3.1);
        const wd=el("div","tw-word",{left:(x+103)+"px",top:(d.y+27)+"px",color:col},g); wd.textContent=word;
        const mn=el("div","tw-meaning",{left:(x+103)+"px",top:(d.y+84)+"px"},g); mn.textContent=meaning;
        return {card,iconObj,wd,mn};
      };
      const a=makeCard(L,d.word,d.meaning,d.icon,d.colour);
      const b=makeCard(664,d.word2,d.meaning2,d.icon2,d.colour2);
      const ar=icon("arrow",542,d.y+52,44,"rgba(255,255,255,.72)","rgba(255,255,255,.72)",g,3.2);
      const sn=sentence(d.ex,L,d.y+180,38,g);
      return Object.assign({},d,{g,a,b,ar,sn});
    });
    S={c,pn,root,early,big,standard,title,line,rule,rows};
    return {rows:rows.length};
  };

  window.seek=function(t){
    const {c,rows}=S;
    const p=followPanel(S.pn,t,PANEL.x), k=kaylaAt(t);
    // During the large opening, clip at a Kayla-safe right edge even while the engine is in motion.
    const safeBig=Math.min(760,k.cx-Math.max(700,k.h*.45));
    S.early.style.clipPath=`inset(0 ${Math.max(0,1920-safeBig)}px 0 0)`;
    const bp=ease.outBack(prog(t,.05,.42)); reveal(S.big,Math.max(0,bp));
    const be=ease.inCubic(prog(t,1.14,.20)); S.early.style.opacity=1-be;
    const stdIn=ease.outCubic(prog(t,1.35,.30)); S.standard.style.opacity=stdIn * clamp(p.alpha*1.25);
    // Standard content never exceeds the actual panel’s inner right edge; the static geometry is already <= 1114.
    S.standard.style.clipPath=`inset(0 ${Math.max(0,1920-Math.min(R,p.right-56,k.cx-k.h*.18))}px 0 0)`;
    reveal(S.title,ease.outExpo(prog(t,c.some-.30,.7)));
    reveal(S.line,ease.outExpo(prog(t,c.some-.10,.65)));
    S.rule.style.transform=`scaleX(${ease.outExpo(prog(t,c.some+.06,.9))})`;
    rows.forEach((r,i)=>{
      const showCard=(card,at)=>{
        const q=ease.outExpo(prog(t,at-.06,.55)); card.card.style.opacity=q; card.card.style.transform=`translateY(${(1-q)*14}px)`;
        card.wd.style.opacity=q; card.wd.style.transform=`translateY(${(1-q)*12}px)`;
        card.mn.style.opacity=q; card.mn.style.transform=`translateY(${(1-q)*12}px)`;
        drawIcon(card.iconObj,prog(t,at+.05,.75));
      };
      showCard(r.a,r.leftAt); showCard(r.b,r.rightAt);
      const ap=ease.outExpo(prog(t,r.rightAt-.08,.55)); r.ar.s.style.opacity=ap; r.ar.s.style.transform=`translateX(${(1-ap)*-12}px)`; drawIcon(r.ar,prog(t,r.rightAt-.08,.7));
      riseWords(r.sn,t,r.exAt-.10);
      r.sn.groups.forEach((g,j)=>sweep(g,t,Math.max(r.marks[j]||r.marks[0],r.exAt+.18+j*.25),.38));
    });
    exitLift(S.root,t);
    return true;
  };

  const _init=window.init;
  window.init=function(c){
    const M={some:["some",1],what:["what",1],is:["is",1],thinking:["thinking",1],action:["action",1],we:["we",1],were:["were",1],having:["having",1],means:["means",1]};
    for(const [k,[p,n]] of Object.entries(M)) c[k]=cue(p,n);
    const info=_init(c);
    fx(.05,"glitch",.8); fx(.10,"whoosh",.5);
    [c.what,c.action,c.we,c.means].forEach(t=>fx(t,"pop",.6));
    return info;
  };
})();
