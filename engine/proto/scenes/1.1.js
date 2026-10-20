"use strict";
// Simple present form: subject choices, basic verb, and the third-person -s ending.
(() => {
document.head.insertAdjacentHTML("beforeend", `<style>
  .form-box{position:absolute;display:flex;align-items:center;height:70px;padding:0 25px;box-sizing:border-box;border-radius:17px;font-family:Nunito;font-weight:800;font-size:39px;line-height:1;color:#fff;white-space:nowrap}
  .form-plus{position:absolute;font-family:Fredoka;font-weight:600;font-size:43px;line-height:1;color:rgba(255,255,255,.76);white-space:nowrap}
  .ending-box{position:absolute;display:flex;align-items:center;justify-content:center;height:70px;padding:0 23px;box-sizing:border-box;border-radius:35px;background:#FFD93D;color:#281450;font-family:Nunito;font-weight:900;font-size:42px;line-height:1;white-space:nowrap;box-shadow:0 0 21px rgba(255,217,61,.45);transform-origin:center}
</style>`);
const PANEL={x:60,y:130,h:900},L=116,R=1114;
let S=null;
function formulaBox(text,x,y,border,bg,parent){const n=el("div","form-box",{left:x+"px",top:y+"px",border:`2px solid ${border}`,background:bg},parent);n.textContent=text;return n;}
function enter(n,t,t0,d=.60){const p=ease.outExpo(prog(t,t0,d));n.style.opacity=clamp(p*1.35);n.style.transform=`translateY(${(1-p)*18}px)`;}
function burst(x,y,parent){const s=el("svg",null,{position:"absolute",left:(x-65)+"px",top:(y-65)+"px",width:"130px",height:"130px",overflow:"visible",pointerEvents:"none"},parent);s.setAttribute("viewBox","0 0 130 130");s.innerHTML='<path d="M65 7 L70 58 L123 65 L70 72 L65 123 L60 72 L7 65 L60 58 Z" fill="#FFD93D"/><path d="M102 18 L105 42 L128 45 L105 48 L102 72 L99 48 L76 45 L99 42 Z" fill="#2EE6FF"/><path d="M26 65 L29 86 L50 89 L29 92 L26 113 L23 92 L2 89 L23 86 Z" fill="#FF4FA8"/>';return s;}
window.init=function(c){
  c.simple=cue("simple");c.basic=cue("basic");c.he=cue("he");c.add=cue("add");c.plays=cue("plays");
  const pn=panel(PANEL.x,PANEL.y,1110,PANEL.h),content=el("div",null,{position:"absolute",inset:"0"});
  const title=masked("Simple present",{left:L+"px",top:"176px",fontFamily:"Fredoka",fontWeight:600,fontSize:"58px",color:C.white,lineHeight:"1"},content);
  const rule=hrule(L,266,R-L,.18,content);
  const sub1=formulaBox("I / you / we / they",L,322,"#2EE6FF","rgba(46,230,255,.09)",content);
  const plus1=el("div","form-plus",{top:"334px"},content);plus1.textContent="+";
  const verb1=formulaBox("play",0,322,"#FFD93D","rgba(255,217,61,.11)",content);
  const sub2=formulaBox("he / she / it",L,480,"#2EE6FF","rgba(46,230,255,.09)",content);
  const plus2=el("div","form-plus",{top:"492px"},content);plus2.textContent="+";
  const verb2=formulaBox("play",0,480,"#FFD93D","rgba(255,217,61,.11)",content);
  const ending=el("div","ending-box",{top:"480px"},content);ending.textContent="+S";
  plus1.style.left=(L+sub1.getBoundingClientRect().width+28)+"px";verb1.style.left=(L+sub1.getBoundingClientRect().width+76)+"px";
  plus2.style.left=(L+sub2.getBoundingClientRect().width+28)+"px";verb2.style.left=(L+sub2.getBoundingClientRect().width+76)+"px";
  const endX=L+sub2.getBoundingClientRect().width+76+verb2.getBoundingClientRect().width+24;ending.style.left=endX+"px";
  const ex=sentence("She play{s|v}.",L,694,132,content);   // R13: enlarged from 68 px to fill the lower panelex.groups[0].host.style.margin="0";ex.groups[0].mk.style.left="-.04em";ex.groups[0].mk.style.right="-.04em";
  const sp=burst(L+sub2.getBoundingClientRect().width+76+verb2.getBoundingClientRect().width+76,510,content);
  S={c,pn,content,title,rule,sub1,plus1,verb1,sub2,plus2,verb2,ending,ex,sp,endX};
  fx(c.add+.5,"click",.8);fx(c.plays,"sparkle",.6);
  return {formulaEnd:endX+ending.getBoundingClientRect().width,example:"She plays."};
};
window.seek=function(t){
 const {c}=S;followPanel(S.pn,t);
 reveal(S.title,ease.outExpo(prog(t,c.simple-.18,.78)));S.rule.style.transform=`scaleX(${ease.outExpo(prog(t,c.simple+.02,1))})`;
 [S.sub1,S.plus1,S.verb1].forEach((n,i)=>enter(n,t,c.basic-.05+i*.12));
 [S.sub2,S.plus2,S.verb2].forEach((n,i)=>enter(n,t,c.he-.04+i*.12));
 const ep=ease.outBack(prog(t,c.add,.55));S.ending.style.opacity=clamp(prog(t,c.add,.12));S.ending.style.transform=`translate(${(1-ep)*(820-S.endX)}px,${(1-ep)*(-158)}px) scale(${lerp(.82,1,Math.max(0,ep))})`;
 riseWords(S.ex,t,c.plays-.12,.05);sweep(S.ex.groups[0],t,c.plays,.36);
 const bp=prog(t,c.plays+.10,.58);S.sp.style.opacity=bp>0&&bp<1?1-bp:0;S.sp.style.transform=`scale(${lerp(.34,1.12,ease.outCubic(bp))})`;
 exitLift(S.content,t);return true;
};
})();
