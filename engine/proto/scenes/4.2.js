"use strict";
// Level 4.2 — a synopsis uses present tenses: story-card family.
(() => {
document.head.insertAdjacentHTML("beforeend", `<style>
.definition{position:absolute;box-sizing:border-box;border:1.5px solid rgba(46,230,255,.64);border-radius:22px;background:rgba(46,230,255,.07)}
.story-comic{position:absolute;box-sizing:border-box;overflow:hidden;border:2px solid rgba(255,255,255,.72);border-radius:24px;background:linear-gradient(180deg,rgba(29,71,126,.76),rgba(19,45,95,.82))}
.mint-pill{position:absolute;display:flex;align-items:center;height:42px;padding:0 18px;border-radius:21px;border:1.5px solid rgba(92,242,176,.65);background:rgba(92,242,176,.12);color:#5CF2B0;font:800 25px Nunito;white-space:nowrap}
</style>`);
const X=60,L=116,R=1344,MINT="#5CF2B0";
let S=null;
ICONS.shark=[["path","M8 39 C17 27 28 24 38 28 C46 19 53 15 59 15 L54 30 C59 34 61 39 62 43 C53 43 47 45 41 49 C30 54 18 51 8 39 Z",0],["path","M28 29 L23 16 L36 25 M41 49 L35 58 L31 49",0],["circle",[49,31,2.6],2]];
function fadeUp(e,t,t0,d=.58,dy=16){const p=ease.outExpo(prog(t,t0,d));e.style.opacity=p;e.style.transform=`translateY(${(1-p)*dy}px)`;return p;}
window.init=function(c){
  c.synopsis=cue("synopsis");c.retell=cue("retell");c.present=cue("present");c.dramatic=cue("dramatic");
  c.dora=cue("dora");c.resting=cue("resting");c.spot=cue("spot");c.shark=cue("shark");
  const pn=panel(X,130,1340,900),content=el("div",null,{position:"absolute",inset:"0"});
  const def=el("div","definition",{left:"116px",top:"166px",width:"1228px",height:"92px"},content);
  const defSn=sentence("{synopsis|t} = a short summary of a film, play or book",146,190,35,content);
  const formA=masked("SYNOPSIS / RETELLING",{left:"116px",top:"300px",fontFamily:"Fredoka",fontWeight:600,fontSize:"40px",color:C.white,lineHeight:"1"},content);
  const arrow=icon("arrow",616,289,52,"rgba(255,255,255,.72)",C.cyan,content,3.2);
  const formB=masked("PRESENT TENSES",{left:"684px",top:"300px",fontFamily:"Fredoka",fontWeight:600,fontSize:"40px",color:MINT,lineHeight:"1"},content);
  const rule=hrule(L,366,R-L,.18,content);
  const lively=el("div","mint-pill",{left:"116px",top:"388px"},content);lively.textContent="lively";
  const dramatic=el("div","mint-pill",{left:"252px",top:"388px"},content);dramatic.textContent="dramatic";
  const comic=el("div","story-comic",{left:"116px",top:"456px",width:"1228px",height:"486px"},content);
  const sun=el("div",null,{position:"absolute",right:"86px",top:"48px",width:"90px",height:"90px",borderRadius:"50%",background:C.yellow,boxShadow:"0 0 18px rgba(255,217,61,.24)"},comic);
  const waves=el("svg",null,{position:"absolute",left:"0",bottom:"0",width:"100%",height:"178px",overflow:"visible"},comic);waves.setAttribute("viewBox","0 0 1228 178");waves.innerHTML='<path d="M0 92 Q55 72 110 92 T220 92 T330 92 T440 92 T550 92 T660 92 T770 92 T880 92 T990 92 T1100 92 T1228 92" fill="none" stroke="#2EE6FF" stroke-opacity=".82" stroke-width="5"/><path d="M0 124 Q55 104 110 124 T220 124 T330 124 T440 124 T550 124 T660 124 T770 124 T880 124 T990 124 T1100 124 T1228 124" fill="none" stroke="#2EE6FF" stroke-opacity=".55" stroke-width="5"/><path d="M0 156 Q55 136 110 156 T220 156 T330 156 T440 156 T550 156 T660 156 T770 156 T880 156 T990 156 T1100 156 T1228 156" fill="none" stroke="#2EE6FF" stroke-opacity=".34" stroke-width="5"/>';
  const sn=sentence("Dora and Sam {are resting|p} on the\nbeach when suddenly, they {spot|y} a\nshark …",150,510,42,content);
  const shark=icon("shark",1018,677,184,"rgba(255,255,255,.9)",MINT,content,3.6);
  const shock=masked("!",{left:"932px",top:"592px",fontFamily:"Fredoka",fontWeight:600,fontSize:"122px",color:C.yellow,lineHeight:"1"},content);
  S={c,pn,content,def,defSn,formA,arrow,formB,rule,lively,dramatic,comic,sun,waves,sn,shark,shock};
  fx(c.synopsis,"whoosh",.4);fx(c.present,"pop",.6);fx(c.dramatic,"pop",.35);fx(c.spot,"whoosh",.6);fx(c.shark,"glitch",.5);
  return {layout:"small-story-comic"};
};
window.seek=function(t){
  const s=S,c=s.c,pe=ease.inCubic(prog(t,c.dur-.45,.42));
  followPanel(s.pn,t);s.pn.style.opacity=panelAt(t).alpha*(1-pe);
  const dp=ease.outExpo(prog(t,c.synopsis-.1,.5));s.def.style.opacity=dp;s.def.style.transform=`translateY(${(1-dp)*16}px)`;
  riseWords(s.defSn,t,c.synopsis-.06);sweep(s.defSn.groups[0],t,c.synopsis+.05,.35);
  reveal(s.formA,ease.outExpo(prog(t,c.retell-.10,.68)));drawIcon(s.arrow,prog(t,c.present-.18,.58));reveal(s.formB,ease.outExpo(prog(t,c.present-.06,.68)));
  s.rule.style.transform=`scaleX(${ease.outExpo(prog(t,c.present+.05,.72))})`;
  fadeUp(s.lively,t,c.dramatic-.22,.44,12);fadeUp(s.dramatic,t,c.dramatic,.44,12);
  const cp=ease.outExpo(prog(t,c.dora-.22,.58));let j=0;if(t>=c.shark){const q=prog(t,c.shark,.28);j=Math.sin(q*48)*(1-q)*7;}s.comic.style.opacity=cp;s.comic.style.transform=`translate(${j}px,${(1-cp)*22}px)`;
  s.sun.style.opacity=cp;s.waves.style.opacity=cp;
  riseWords(s.sn,t,c.dora-.1);s.sn.groups.forEach((g,i)=>sweep(g,t,i?c.spot:c.resting,.38));
  const sp=ease.outCubic(prog(t,c.spot-.10,.5));drawIcon(s.shark,sp);const rise=ease.outCubic(prog(t,c.spot-.1,.5));s.shark.s.style.transform=`translateY(${(1-rise)*58}px)`;
  reveal(s.shock,ease.outBack(prog(t,c.shark,.28)));s.shock.o.style.opacity=prog(t,c.shark,.05);
  exitLift(s.content,t);return true;
};
})();
