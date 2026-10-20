"use strict";
// Level 4.3 — distinguish a story’s present from real-world past facts.
(() => {
document.head.insertAdjacentHTML("beforeend", `<style>
.facts-card{position:absolute;box-sizing:border-box;border-radius:24px;border:1.5px solid;background:rgba(26,14,63,.48);overflow:hidden}
.card-kicker{position:absolute;font:800 20px Nunito;letter-spacing:.14em;text-transform:uppercase;white-space:nowrap}
.word-pill{position:absolute;display:flex;align-items:center;height:42px;padding:0 18px;border-radius:21px;color:#281450;font:800 26px Nunito;white-space:nowrap;transform-origin:center center}
</style>`);
const X=60,L=116,R=1344,ORANGE="#FFA448",MINT="#5CF2B0";
let S=null;
ICONS.clapper=[["path","M10 25 H54 V54 H10 Z M8 16 L53 8 L57 23 L12 31 Z",0],["path","M18 14 L28 26 M34 11 L44 23",1]];
function fadeUp(e,t,t0,d=.58,dy=16){const p=ease.outExpo(prog(t,t0,d));e.style.opacity=p;e.style.transform=`translateY(${(1-p)*dy}px)`;return p;}
window.init=function(c){
  c.careful=cue("careful");c.the=cue("the",2);c.was=cue("was");c.came=cue("came");c.saves=cue("saves");
  const pn=panel(X,130,1340,900),content=el("div",null,{position:"absolute",inset:"0"});
  const careful=masked("Careful!",{left:L+"px",top:"176px",fontFamily:"Fredoka",fontWeight:600,fontSize:"52px",color:ORANGE,lineHeight:"1"},content);
  const title=masked("Real-world facts stay in the past.",{left:"354px",top:"181px",fontFamily:"Fredoka",fontWeight:600,fontSize:"44px",color:C.white,lineHeight:"1"},content);
  const rule=hrule(L,266,R-L,.18,content);
  const inside=el("div","facts-card",{left:"116px",top:"314px",width:"570px",height:"300px",borderColor:"rgba(92,242,176,.72)"},content);
  const outside=el("div","facts-card",{left:"716px",top:"314px",width:"628px",height:"300px",borderColor:"rgba(255,164,72,.72)"},content);
  const clapper=badge("film-slate",146,344,72,MINT,content), globe=badge("globe-hemisphere-west",746,344,72,ORANGE,content);  // badge x = card + 30, text x = card + 126
  const inK=el("div","card-kicker",{left:"242px",top:"356px",color:MINT},content);inK.textContent="INSIDE THE STORY";
  const inSub=masked("present",{left:"242px",top:"398px",fontFamily:"Nunito",fontWeight:800,fontSize:"29px",color:C.white,lineHeight:"1"},content);
  const outK=el("div","card-kicker",{left:"842px",top:"356px",color:ORANGE},content);outK.textContent="OUTSIDE THE STORY";
  const outSub=masked("real-world facts: past",{left:"842px",top:"398px",fontFamily:"Nunito",fontWeight:800,fontSize:"29px",color:C.white,lineHeight:"1"},content);
  const inRail=hrule(146,470,510,.18,content),outRail=hrule(746,470,568,.18,content);
  const was=el("div","word-pill",{left:"842px",top:"506px",background:ORANGE},content);was.textContent="was";
  const came=el("div","word-pill",{left:"0px",top:"506px",background:ORANGE},content);came.textContent="came out";came.style.left=(842+was.offsetWidth+16)+"px";
  const saves=el("div","word-pill",{left:"242px",top:"506px",background:MINT},content);saves.textContent="saves";
  const sn=sentence("The film {was|y} a big hit when it {came out|y} {in 2008|t}.\nIn the film, Harry the superhero {saves|y} thousands of lives.",116,690,40,content);
  S={c,pn,content,careful,title,rule,inside,outside,clapper,globe,inK,inSub,outK,outSub,inRail,outRail,was,came,saves,sn};
  fx(c.was+.8,"pop",.55);fx(c.came+.8,"pop",.55);fx(c.saves+.8,"pop",.55);
  return {layout:"small-story-facts"};
};
window.seek=function(t){
  const s=S,c=s.c,pe=ease.inCubic(prog(t,c.dur-.45,.42));
  followPanel(s.pn,t);s.pn.style.opacity=panelAt(t).alpha*(1-pe);
  reveal(s.careful,ease.outExpo(prog(t,c.careful-.05,.64)));reveal(s.title,ease.outExpo(prog(t,1.38,.72)));s.rule.style.transform=`scaleX(${ease.outExpo(prog(t,1.48,.9))})`;
  const ip=ease.outExpo(prog(t,c.the-.3,.48)),op=ease.outExpo(prog(t,c.the-.12,.48));
  s.inside.style.opacity=ip;s.inside.style.transform=`translateY(${(1-ip)*20}px)`;s.outside.style.opacity=op;s.outside.style.transform=`translateY(${(1-op)*20}px)`;
  popBadge(s.clapper,t,c.the-.18,.5);popBadge(s.globe,t,c.the-.04,.5);fadeUp(s.inK,t,c.the-.14);reveal(s.inSub,ease.outExpo(prog(t,c.the-.06,.6)));fadeUp(s.outK,t,c.the);reveal(s.outSub,ease.outExpo(prog(t,c.the+.06,.6)));
  s.inRail.style.transform=`scaleX(${ease.outExpo(prog(t,c.the+.10,.6))})`;s.outRail.style.transform=`scaleX(${ease.outExpo(prog(t,c.the+.18,.6))})`;
  riseWords(s.sn,t,c.the-.1);s.sn.groups.forEach((g,i)=>sweep(g,t,[c.was,c.came,c.came+.42,c.saves][i],.36));
  fadeUp(s.was,t,c.was+.28,.5,22);fadeUp(s.came,t,c.came+.28,.5,22);fadeUp(s.saves,t,c.saves+.28,.5,22);
  exitLift(s.content,t);return true;
};
})();
