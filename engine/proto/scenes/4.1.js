"use strict";
// Level 4.1 — stories in the past: story-card family.
(() => {
document.head.insertAdjacentHTML("beforeend", `<style>
.story-page{position:absolute;box-sizing:border-box;border-radius:24px;border:1.5px solid rgba(255,255,255,.18);background:rgba(26,14,63,.46);overflow:hidden}
.story-spine{position:absolute;width:2px;background:rgba(255,217,61,.48);box-shadow:0 0 10px rgba(255,217,61,.25);transform-origin:center top}
.past-tag{position:absolute;display:flex;align-items:center;justify-content:center;height:44px;padding:0 18px;box-sizing:border-box;border-radius:22px;background:#FFD93D;color:#281450;font:800 28px Nunito;white-space:nowrap}
</style>`);
const X=60, L=116, R=1344, ORANGE="#FFA448";
let S=null;
ICONS.heart=[["path","M32 54 C27 47 13 37 13 24 A11 11 0 0 1 32 16 A11 11 0 0 1 51 24 C51 37 37 47 32 54 Z",0]];
function fadeUp(e,t,t0,d=.6,dy=18){const p=ease.outExpo(prog(t,t0,d));e.style.opacity=p;e.style.transform=`translateY(${(1-p)*dy}px)`;return p;}
window.init=function(c){
  c.stories=cue("stories"); c.past1=cue("past",1); c.tenses=cue("tenses");
  c.once=cue("once"); c.was=cue("was"); c.had=cue("had");
  const pn=panel(X,130,1340,900);
  const content=el("div",null,{position:"absolute",inset:"0"});
  const title=masked("Stories in the past",{left:L+"px",top:"176px",fontFamily:"Fredoka",fontWeight:600,fontSize:"58px",color:C.white,lineHeight:"1"},content);
  const arr=icon("arrow",618,176,58,"rgba(255,255,255,.72)",C.yellow,content,3.2);
  const past=masked("past tenses",{left:"696px",top:"181px",fontFamily:"Fredoka",fontWeight:600,fontSize:"44px",color:C.yellow,lineHeight:"1"},content);
  const rule=hrule(L,266,R-L,.18,content);
  const book=el("div","story-page",{left:"116px",top:"310px",width:"1228px",height:"590px"},content);
  const left=el("div","story-page",{left:"22px",top:"22px",width:"575px",height:"546px",borderColor:"rgba(255,217,61,.52)",background:"rgba(52,30,95,.52)"},book);
  const right=el("div","story-page",{left:"631px",top:"22px",width:"575px",height:"546px",borderColor:"rgba(255,217,61,.52)",background:"rgba(52,30,95,.52)"},book);
  const spine=el("div","story-spine",{left:"613px",top:"36px",height:"518px"},book);
  const sn=sentence("Once upon a time, there\n{was|y} a beautiful princess\nwho {had|y} a kind heart …",152,386,46,content);
  const bookIc=icon("book",1000,418,112,"rgba(255,255,255,.9)",C.yellow,content,3.2);
  const heartIc=icon("heart",1024,574,92,"rgba(255,255,255,.9)",C.pink,content,3.4);
  const cap=masked("PAST TENSES",{left:"1010px",top:"714px",fontFamily:"Nunito",fontWeight:800,fontSize:"22px",letterSpacing:".14em",color:ORANGE,lineHeight:"1"},content);cap.o.classList.add("label");
  const tagWas=el("div","past-tag",{left:"984px",top:"762px"},content);tagWas.textContent="was";
  const tagHad=el("div","past-tag",{left:"1116px",top:"762px"},content);tagHad.textContent="had";
  S={c,pn,content,title,arr,past,rule,book,left,right,spine,sn,bookIc,heartIc,cap,tagWas,tagHad};
  fx(.38,"whoosh",.5); fx(c.was,"pop",.55); fx(c.had,"pop",.55);
  return {layout:"small-storybook"};
};
window.seek=function(t){
  const s=S,c=s.c, pe=ease.inCubic(prog(t,c.dur-.45,.42));
  followPanel(s.pn,t); s.pn.style.opacity=panelAt(t).alpha*(1-pe);
  reveal(s.title,ease.outExpo(prog(t,c.stories-.12,.72)));
  drawIcon(s.arr,prog(t,c.past1-.06,.58));
  reveal(s.past,ease.outExpo(prog(t,c.past1+.04,.68)));
  s.rule.style.transform=`scaleX(${ease.outExpo(prog(t,.14,1))})`;
  const pb=ease.outExpo(prog(t,c.once-.62,.52));   // book arrives just before its words
  s.book.style.opacity=pb;s.book.style.transform=`translateY(${(1-pb)*26}px) scale(${.97+.03*pb})`;
  s.left.style.opacity=pb;s.right.style.opacity=pb;s.spine.style.transform=`scaleY(${ease.outExpo(prog(t,c.once-.47,.65))})`;
  riseWords(s.sn,t,c.once-.12);
  s.sn.groups.forEach((g,i)=>sweep(g,t,i?c.had:c.was,.38));
  drawIcon(s.bookIc,prog(t,c.once-.25,.72));
  drawIcon(s.heartIc,prog(t,c.had-.14,.68));
  fadeUp(s.cap.o,t,c.was+.02); fadeUp(s.tagWas,t,c.was+.18,.48,14); fadeUp(s.tagHad,t,c.had+.18,.48,14);
  exitLift(s.content,t); return true;
};
})();
