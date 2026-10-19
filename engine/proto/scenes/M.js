"use strict";
// Tense Map: compact 2 x 2 overview of the four unit tenses.
(() => {
document.head.insertAdjacentHTML("beforeend", `<style>
  .map-card{position:absolute;box-sizing:border-box;border-radius:22px;border:2px solid;overflow:hidden;background:rgba(255,255,255,.045)}
  .map-name{position:absolute;left:30px;right:30px;top:29px;font-family:Nunito;font-weight:900;font-size:27px;line-height:1;color:#fff;white-space:nowrap}
  .map-example{position:absolute;left:30px;right:30px;bottom:31px;font-family:Nunito;font-weight:800;font-size:42px;line-height:1;color:#fff;white-space:nowrap}
  .map-row{position:absolute;font-family:Fredoka;font-weight:600;font-size:31px;letter-spacing:.04em;line-height:1;white-space:nowrap}
  .map-head{position:absolute;font-family:Fredoka;font-weight:600;font-size:42px;line-height:1;white-space:nowrap}
  .map-chip{position:absolute;display:flex;align-items:center;height:42px;padding:0 17px;box-sizing:border-box;border-radius:21px;font-family:Nunito;font-weight:900;font-size:21px;white-space:nowrap;transform-origin:center}
</style>`);
const PANEL={x:60,y:130,h:900}, L=116, R=1344;
let S=null;
function rise(n,t,t0,d=.62,dy=18){const p=ease.outExpo(prog(t,t0,d));n.style.opacity=clamp(p*1.3);n.style.transform=`translateY(${(1-p)*dy}px)`;return p;}
function card(x,y,name,example,col,parent){
  const d=el("div","map-card",{left:x+"px",top:y+"px",width:"440px",height:"198px",borderColor:col},parent);
  d.style.boxShadow=`inset 0 1px 0 rgba(255,255,255,.08), 0 0 0 1px ${col}14`;
  const n=el("div","map-name",{color:col},d);n.textContent=name;
  const e=el("div","map-example",{},d);e.textContent=example;
  const lock=icon("lock",374,24,44,"rgba(255,255,255,.88)",col,d,3.6);
  return {d,n,e,lock};
}
function sparkle(x,y,parent){
 const s=el("svg",null,{position:"absolute",left:(x-94)+"px",top:(y-94)+"px",width:"188px",height:"188px",overflow:"visible",pointerEvents:"none"},parent);s.setAttribute("viewBox","0 0 188 188");
 s.innerHTML='<path d="M94 7 L101 86 L181 94 L101 102 L94 181 L87 102 L7 94 L87 86 Z" fill="#2EE6FF" opacity=".88"/><path d="M144 25 L148 67 L181 71 L148 75 L144 117 L140 75 L107 71 L140 67 Z" fill="#FFD93D"/><path d="M41 79 L45 112 L78 116 L45 120 L41 153 L37 120 L4 116 L37 112 Z" fill="#FF4FA8"/>';
 return s;
}
window.init=function(c){
  c.map=cue("map");c.yellow=cue("yellow");c.facts=cue("facts");c.habits=cue("habits");c.finished=cue("finished");c.pink=cue("pink");c.actions=cue("actions",2);c.unlock=cue("unlock");
  ICONS.lock=[["path","M20 29 V21 a12 12 0 0 1 24 0 V29 M15 29 H49 V52 H15 Z",0],["path","M32 37 v7",1]];
  const pn=panel(PANEL.x,PANEL.y,1340,PANEL.h),content=el("div",null,{position:"absolute",inset:"0"});
  const title=masked("The Tense Map",{left:L+"px",top:"176px",fontFamily:"Fredoka",fontWeight:600,fontSize:"58px",color:C.white,lineHeight:"1"},content);
  const rule=hrule(L,266,R-L,.18,content);
  const simple=el("div","map-head",{left:"310px",top:"312px",color:C.yellow},content);simple.textContent="SIMPLE";
  const continuous=el("div","map-head",{left:"810px",top:"312px",color:C.pink},content);continuous.textContent="CONTINUOUS";
  const present=el("div","map-row",{left:L+"px",top:"455px",color:"#5CF2B0"},content);present.textContent="PRESENT";
  const past=el("div","map-row",{left:L+"px",top:"705px",color:"#FFA448"},content);past.textContent="PAST";
  const cards=[card(310,380,"simple present","I play",C.yellow,content),card(310,630,"simple past","I played",C.yellow,content),card(810,380,"present continuous","I am playing",C.pink,content),card(810,630,"past continuous","I was playing",C.pink,content)];
  const chipData=[["facts",C.yellow,310,c.facts],["habits",C.yellow,405,c.habits],["finished actions",C.yellow,514,c.finished],["actions in progress",C.pink,810,c.actions]];
  const chips=chipData.map(([text,col,x,t0])=>{const n=el("div","map-chip",{left:x+"px",top:"892px",background:col+"28",border:`1.5px solid ${col}99`,color:col},content);n.textContent=text;return {n,t0};});
  const burst=sparkle(780,605,content);
  S={c,pn,content,title,rule,simple,continuous,present,past,cards,chips,burst};
  [c.yellow+.15,c.yellow+.35,c.pink+.15,c.pink+.35].forEach(t=>fx(t,"pop",.55));fx(c.unlock,"sparkle",.8);
  return {grid:{left:310,right:1250},cards:4};
};
window.seek=function(t){
 const {c}=S;followPanel(S.pn,t);
 reveal(S.title,ease.outExpo(prog(t,c.map-.10,.78)));S.rule.style.transform=`scaleX(${ease.outExpo(prog(t,c.map+.05,1))})`;
 rise(S.present,t,c.map+.12);rise(S.past,t,c.map+.28);
 rise(S.simple,t,c.yellow,.6);rise(S.continuous,t,c.pink,.6);
 const times=[c.yellow+.15,c.yellow+.35,c.pink+.15,c.pink+.35];
 S.cards.forEach((card,i)=>{rise(card.d,t,times[i],.60);const unlocked=ease.inOutCubic(prog(t,c.unlock,.28));card.lock.s.style.opacity=1-unlocked;card.lock.s.style.transform=`scale(${lerp(1,.70,unlocked)})`;});
 S.chips.forEach(({n,t0})=>{const p=ease.outBack(prog(t,t0,.36));n.style.opacity=clamp(prog(t,t0,.1));n.style.transform=`translateY(${(1-p)*16}px) scale(${lerp(.88,1,Math.max(0,p))})`;});
 const p=prog(t,c.unlock,.78);S.burst.style.opacity=p>0&&p<1?1-p:0;S.burst.style.transform=`scale(${lerp(.28,1.12,ease.outCubic(p))})`;
 exitLift(S.content,t);return true;
};
})();
