"use strict";
// Level 4 close: the same Snow White book quotations used in the hook.
(() => {
document.head.insertAdjacentHTML("beforeend", `<style>
  .book-label{position:absolute;display:flex;align-items:center;gap:12px;font-family:Nunito;font-size:24px;font-weight:800;color:#2EE6FF;white-space:nowrap}
  .book-tag{position:absolute;display:flex;align-items:center;justify-content:center;height:30px;padding:0 12px;border-radius:15px;box-sizing:border-box;font-family:Nunito;font-weight:900;font-size:18px;line-height:1;letter-spacing:.01em;color:#281450;white-space:nowrap;transform-origin:center bottom}
  .book-bubble{position:absolute;overflow:visible;pointer-events:none}
  .finish-dot{position:absolute;border-radius:50%;background:#5CF2B0;box-shadow:0 0 24px rgba(92,242,176,.65);transform-origin:center}
</style>`);
const PANEL={x:60,y:130,h:900}, L=116, BW=1024;
let S=null;
function bubble(x,y,w,h,parent){
  const s=el("svg","book-bubble",{left:x+"px",top:y+"px",width:w+"px",height:(h+33)+"px"},parent);
  s.setAttribute("viewBox",`0 0 ${w} ${h+33}`);
  // One continuous SVG path includes the tail, avoiding a line across the tail base.
  s.innerHTML=`<path d="M28 1 H${w-28} Q${w-1} 1 ${w-1} 28 V${h-28} Q${w-1} ${h-1} ${w-28} ${h-1} H68 L30 ${h+30} L39 ${h-1} H28 Q1 ${h-1} 1 ${h-28} V28 Q1 1 28 1 Z" fill="rgba(46,230,255,.050)" stroke="#2EE6FF" stroke-width="3" stroke-linejoin="round"/>`;
  return s;
}
function speechLabel(text,x,y,parent){const d=el("div","book-label",{left:x+"px",top:y+"px"},parent);d.innerHTML=`<svg width="28" height="26" viewBox="0 0 28 26" aria-hidden="true"><path d="M3 3 H25 V18 H12 L6 24 L7 18 H3 Z" fill="none" stroke="#2EE6FF" stroke-width="2.5" stroke-linejoin="round"/></svg><span>${text}</span>`;return d;}
function lines(srcs,x,y,size,step,parent){   // one standard sentence per line -> exact baselines + fixed line gaps for tags
  const box=el("div",null,{position:"absolute",left:"0",top:"0",width:"1920px",height:"1080px"},parent),words=[],groups=[];
  srcs.forEach((src,i)=>{const s=sentence(src,x,y+i*step,size,box);words.push(...s.words);groups.push(...s.groups);});
  return {box,words,groups,top:y,bottom:y+(srcs.length-1)*step+size*1.25,width:()=>Math.max(...[...box.children].map(n=>n.getBoundingClientRect().width))};
}
function tag(text,col,parent){const d=el("div","book-tag",{background:col,boxShadow:`0 0 14px ${col}80`},parent);d.textContent=text;return d;}
function inTag(node,t,t0){const p=ease.outBack(prog(t,t0,.32));node.style.opacity=clamp(prog(t,t0,.10));node.style.transform=`translateY(${(1-p)*-13}px) scale(${lerp(.82,1,Math.max(0,p))})`;}
function layTag(node,g){const r=g.host.getBoundingClientRect(),w=node.getBoundingClientRect().width;node.style.left=clamp(r.left+r.width/2-w/2,100,1110-w)+"px";node.style.top=(r.top-27)+"px";}
function sparkle(x,y,col,parent){
  const d=el("svg",null,{position:"absolute",left:(x-56)+"px",top:(y-56)+"px",width:"112px",height:"112px",overflow:"visible",pointerEvents:"none"},parent);
  d.setAttribute("viewBox","0 0 112 112");
  d.innerHTML=`<path d="M56 5 L60 52 L107 56 L60 60 L56 107 L52 60 L5 56 L52 52 Z" fill="${col}" opacity=".9"/><path d="M88 12 L90 27 L105 29 L90 31 L88 46 L86 31 L71 29 L86 27 Z" fill="#FFD93D"/><path d="M23 74 L25 87 L38 89 L25 91 L23 104 L21 91 L8 89 L21 87 Z" fill="#2EE6FF"/>`;
  return d;
}
window.init=function(c){
  c.is=cue("is");c.true=cue("true");c.read=cue("read");c.was=cue("was");c.finished=cue("finished");c.reaches=cue("reaches");c.gives=cue("gives");c.saves=cue("saves");c.live=cue("live");c.every=cue("every");
  const pn=panel(PANEL.x,PANEL.y,1340,PANEL.h),content=el("div",null,{position:"absolute",inset:"0"});
  const l1=speechLabel("Someone talks about a favourite story",L,160,content),b1=bubble(94,208,BW,190,content);
  const s1=lines(["‘Snow White and the Seven Dwarfs’ {is|v} one of my favourite","stories. I first {read|v} it when I {was|v} only three."],118,250,34,75,content);
  const l2=speechLabel("The same person then sums up what happens in the story",L,448,content),b2=bubble(94,485,BW,315,content);
  const s2=lines(["The story {reaches|v} its climax when the evil queen {gives|v}","Snow White a poisoned apple. Luckily the prince’s kiss","{saves|v} her and they {live|v} happily ever after."],118,538,34,75,content);
  // bubbles are sized from the measured text (tags sit in the 2.05 line gaps; top pad leaves room for line-1 tags)
  let b1f=null,b2f=null;
  [[b1,s1,1],[b2,s2,2]].forEach(([b,s,k])=>{const w=s.width();if(w>BW-48)throw new Error("bubble text overflows: "+Math.round(w));const nb=bubble(94,s.top-42,BW,s.bottom-s.top+64,content);content.replaceChild(nb,b);if(k===1)b1f=nb;else b2f=nb;});
  const ts=[tag("TRUE NOW","#5CF2B0",content),tag("FINISHED","#FFA448",content),tag("FINISHED","#FFA448",content),tag("SYNOPSIS","#2EE6FF",content),tag("SYNOPSIS","#2EE6FF",content),tag("SYNOPSIS","#2EE6FF",content),tag("SYNOPSIS","#2EE6FF",content)];
  [s1.groups[0],s1.groups[1],s1.groups[2],s2.groups[0],s2.groups[1],s2.groups[2],s2.groups[3]].forEach((g,i)=>layTag(ts[i],g));
  const q=icon("question",986,842,118,"#FFD93D","#FFD93D",content,4.6);q.s.style.filter="drop-shadow(0 0 13px rgba(255,217,61,.70))";
  const dot=el("div","finish-dot",{left:"982px",top:"838px",width:"126px",height:"126px"},content);
  const tick=icon("tick",1013,869,64,"#281450","#281450",content,7.2);const sp=sparkle(1045,901,"#5CF2B0",content);
  S={c,pn,content,l1,b1:b1f,s1,l2,b2:b2f,s2,ts,q,dot,tick,sp};
  [c.true,c.finished,c.reaches,c.gives,c.saves,c.live].forEach(t=>fx(t,"pop",.56));fx(c.every+.1,"correct",.8);
  return {bubbleWidth:BW,textSize:34};
};
window.seek=function(t){
  const {c}=S;followPanel(S.pn,t);
  const a1=ease.outExpo(prog(t,.05,.65)),a2=ease.outExpo(prog(t,.30,.65));
  [S.l1,S.b1,S.s1.box].forEach(n=>{n.style.opacity=a1;n.style.transform=`translateY(${(1-a1)*14}px)`});
  [S.l2,S.b2,S.s2.box].forEach(n=>{n.style.opacity=a2;n.style.transform=`translateY(${(1-a2)*14}px)`});
  S.s1.groups.forEach((g,i)=>sweep(g,t,[c.true,c.finished,c.finished][i],.34));
  S.s2.groups.forEach((g,i)=>sweep(g,t,[c.reaches,c.gives,c.saves,c.live][i],.34));
  [c.true,c.finished,c.finished,c.reaches+.1,c.gives+.1,c.saves+.1,c.live+.1].forEach((tt,i)=>inTag(S.ts[i],t,tt));
  const qOut=ease.inCubic(prog(t,c.every,.16));S.q.s.style.opacity=1-qOut;drawIcon(S.q,prog(t,-.02,.58));
  const done=ease.outBack(prog(t,c.every+.1,.42));S.dot.style.opacity=clamp(prog(t,c.every+.1,.10));S.dot.style.transform=`scale(${Math.max(0,done)})`;drawIcon(S.tick,prog(t,c.every+.15,.55));
  const burst=prog(t,c.every+.2,.65);S.sp.style.opacity=(burst>0&&burst<1?1-burst:0);S.sp.style.transform=`scale(${lerp(.30,1.15,ease.outCubic(burst))})`;
  exitLift(S.content,t);return true;
};
})();
