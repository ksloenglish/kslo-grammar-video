"use strict";
// Scene 2.1 — Simple past: completed actions, verb forms, examples and time words.
(() => {
document.head.insertAdjacentHTML("beforeend", `<style>
html,body{margin:0;width:1920px;height:1080px;background:transparent;overflow:hidden}body{-webkit-font-smoothing:antialiased;text-rendering:geometricPrecision}.mask{position:absolute;overflow:hidden;padding:.10em .04em .18em;margin:-.10em -.04em -.18em}.inner{display:block;white-space:nowrap;will-change:transform}.sent{position:absolute;white-space:nowrap;font-family:"Nunito";font-weight:800;color:#fff;line-height:1.18}.wm{display:inline-block;overflow:hidden;vertical-align:top;padding:0 .03em .16em;margin:0 -.03em -.16em}.wi{display:inline-block;will-change:transform}.hl{position:relative;display:inline-block;isolation:isolate;margin:0 .07em}.mk{position:absolute;left:-.09em;right:-.09em;top:.17em;bottom:.05em;border-radius:.2em;z-index:-1;transform-origin:left center}.label{font-family:"Nunito";font-weight:800;letter-spacing:.14em;text-transform:uppercase}.num{font-family:"Fredoka";font-weight:600;font-feature-settings:"tnum" 1}.tok{position:absolute;display:flex;align-items:center;justify-content:center;height:64px;padding:0 20px;box-sizing:border-box;border-radius:16px;font-family:"Nunito";font-weight:800;font-size:36px;line-height:1;white-space:nowrap;transform-origin:left center}.pair{position:absolute;height:66px;box-sizing:border-box;border:1.5px solid rgba(192,166,255,.60);background:rgba(192,166,255,.09);border-radius:16px;font-family:"Nunito";font-weight:800;font-size:29px;line-height:1;transform-origin:left center}.chip{position:absolute;display:flex;align-items:center;height:48px;padding:0 17px;box-sizing:border-box;border-radius:24px;border:2px solid rgba(46,230,255,.58);background:rgba(46,230,255,.10);color:#2EE6FF;font-family:"Nunito";font-weight:800;font-size:23px;white-space:nowrap;transform-origin:left center}
</style>`);
const PANEL={x:60,y:130,h:900},L=116,R=1114;
let S=null;
function token(text,x,y,border,bg,color,parent){const e=el("div","tok",{left:x+"px",top:y+"px",border:`2px solid ${border}`,background:bg,color:color||C.white},parent);e.textContent=text;return e;}
function pairCard(a,b,x,y,parent){
  const box=el("div","pair",{left:x+"px",top:y+"px"},parent);   // measured layout: equal 16 px gaps around the arrow
  const first=el("div",null,{position:"absolute",left:"17px",top:"19px",color:C.white},box);first.textContent=a;
  const ax=Math.round(17+first.getBoundingClientRect().width+16);
  const ar=icon("arrow",ax,11,42,"rgba(255,255,255,.70)",C.white,box,3.2);
  const second=el("div",null,{position:"absolute",left:(ax+42+16)+"px",top:"19px",color:C.yellow},box);second.textContent=b;
  const w=Math.round(ax+42+16+second.getBoundingClientRect().width+17);box.style.width=w+"px";
  return {box,ar,w};
}
window.init=function(cues){
  const c=cues;
  const pn=panel(PANEL.x,PANEL.y,1110,PANEL.h),content=el("div",null,{position:"absolute",inset:"0"});
  const title=masked("Simple past",{left:L+"px",top:"176px",fontFamily:"Fredoka",fontWeight:600,fontSize:"58px",color:C.white,lineHeight:"1"},content);
  const rule0=hrule(L,266,R-L,.18,content);
  const useTitle=masked("FINISHED ACTIONS",{left:L+"px",top:"295px",fontSize:"20px",color:C.lilac,lineHeight:"1"},content);useTitle.o.classList.add("label");
  const axis=hrule(196,393,806,.54,content),arrow=icon("arrow",997,361,64,"rgba(255,255,255,.58)",C.white,content,3.1);
  const past=masked("PAST",{left:"196px",top:"423px",fontFamily:"Fredoka",fontWeight:600,fontSize:"22px",color:C.dim,lineHeight:"1"},content);
  const now=masked("NOW",{left:"853px",top:"306px",fontFamily:"Fredoka",fontWeight:600,fontSize:"27px",color:C.cyan,lineHeight:"1"},content);
  const nowLine=el("div",null,{position:"absolute",left:"883px",top:"356px",width:"3px",height:"61px",borderRadius:"2px",background:C.cyan,boxShadow:"0 0 12px rgba(46,230,255,.45)",transformOrigin:"center top"},content);
  const points=[342,535,728].map(x=>{const dot=el("div",null,{position:"absolute",left:(x-13)+"px",top:"380px",width:"26px",height:"26px",borderRadius:"13px",background:C.yellow,boxShadow:"0 0 12px rgba(255,217,61,.4)"},content);const tick=icon("tick",x-17,333,34,"rgba(255,255,255,.88)",C.yellow,content,3.7);return {dot,tick};});
  const regLabel=masked("REGULAR (-ed)",{left:L+"px",top:"492px",fontSize:"20px",color:C.lilac,lineHeight:"1"},content);regLabel.o.classList.add("label");{const n=[regLabel.o,...regLabel.o.querySelectorAll("*")].find(e=>e.childNodes.length===1&&e.firstChild.nodeType===3&&e.textContent==="REGULAR (-ed)");n.innerHTML='REGULAR (<span style="text-transform:none">-ed</span>)';}
  const walk=token("walk",330,472,"rgba(255,255,255,.50)","rgba(255,255,255,.06)",C.white,content);
  const ed=token("+ed",481,472,C.yellow,"rgba(255,217,61,.12)",C.yellow,content);
  const regArrow=icon("arrow",589,482,46,"rgba(255,255,255,.72)",C.white,content,3.2);
  const walked=token("walked",657,472,C.yellow,"rgba(255,217,61,.12)",C.yellow,content);
  const irrLabel=masked("IRREGULAR:",{left:L+"px",top:"611px",fontSize:"20px",color:C.lilac,lineHeight:"1"},content);irrLabel.o.classList.add("label");
  const pair1=pairCard("break","broke",315,584,content),pair2=pairCard("is","was",315+pair1.w+24,584,content);
  const ex1=sentence("I {was} born {in 2013|t}.",L,707,44,content);
  const ex2=sentence("A fire {broke out} in my building {yesterday|t}.",L,790,40,content);
  const twLabel=masked("Time words that go with the simple past:",{left:L+"px",top:"874px",fontFamily:"Nunito",fontWeight:700,fontSize:"24px",color:C.dim,lineHeight:"1"},content);
  const chips=[], words=["yesterday","last week","two years ago","in 2013"];let x=L;
  words.forEach(w=>{const chip=el("div","chip",{left:x+"px",top:"912px"},content);chip.textContent=w;chips.push(chip);x+=chip.getBoundingClientRect().width+14;});
  S={c,pn,content,title,rule0,useTitle,axis,arrow,past,now,nowLine,points,regLabel,walk,ed,regArrow,walked,irrLabel,pair1,pair2,ex1,ex2,twLabel,chips};
  return {chipRight:x};
};
window.seek=function(t){
  const {c}=S, exit0=c.dur-.45,pp=followPanel(S.pn,t,PANEL.x);
  reveal(S.title,ease.outExpo(prog(t,.05,.8)));S.rule0.style.transform=`scaleX(${ease.outExpo(prog(t,.2,1))})`;
  reveal(S.useTitle,ease.outExpo(prog(t,c.finished-.08,.65)));
  const pa=ease.outExpo(prog(t,c.finished,.75));S.axis.style.transform=`scaleX(${pa})`;drawIcon(S.arrow,prog(t,c.finished+.45,.65));reveal(S.past,ease.outExpo(prog(t,c.finished+.18,.55)));
  reveal(S.now,ease.outBack(prog(t,c.finished+.30,.45)));S.nowLine.style.transform=`scaleY(${ease.outExpo(prog(t,c.finished+.42,.5))})`;S.nowLine.style.opacity=clamp(prog(t,c.finished+.42,.12));
  S.points.forEach((p,i)=>{const p0=ease.outBack(prog(t,c.finished+.48+i*.24,.38));p.dot.style.opacity=clamp(prog(t,c.finished+.48+i*.24,.13));p.dot.style.transform=`scale(${Math.max(0,p0)})`;drawIcon(p.tick,prog(t,c.finished+.61+i*.24,.62));});
  reveal(S.regLabel,ease.outExpo(prog(t,c.most-.06,.6)));const inTok=(e,t0)=>{const p=ease.outExpo(prog(t,t0,.6));e.style.opacity=clamp(p*1.5);e.style.transform=`translateY(${(1-p)*18}px)`;};inTok(S.walk,c.most);inTok(S.ed,c.ed-.12);drawIcon(S.regArrow,prog(t,c.ed+.10,.65));inTok(S.walked,c.ed+.20);
  reveal(S.irrLabel,ease.outExpo(prog(t,c.irregular-.08,.6)));const cardIn=(pair,t0)=>{const p=ease.outBack(prog(t,t0,.42));pair.box.style.opacity=clamp(prog(t,t0,.14));pair.box.style.transform=`translateY(${(1-p)*18}px) scale(${lerp(.92,1,p)})`;drawIcon(pair.ar,prog(t,t0+.12,.55));};cardIn(S.pair1,c.irregular+.10);cardIn(S.pair2,c.irregular+.36);
  riseWords(S.ex1,t,c.i-.10);S.ex1.groups.forEach((g,k)=>{const last=S.ex1.words.indexOf(g.words[g.words.length-1]),landed=c.i-.10+last*.05+.3;sweep(g,t,Math.max(k?c.in2013:c.was,landed),.38);});
  riseWords(S.ex2,t,c.fire-.10);S.ex2.groups.forEach((g,k)=>{const last=S.ex2.words.indexOf(g.words[g.words.length-1]),landed=c.fire-.10+last*.05+.3;sweep(g,t,Math.max(k?c.yesterday:c.broke,landed),.38);});
  reveal(S.twLabel,ease.outExpo(prog(t,c.yesterday+.10,.6)));S.chips.forEach((chip,i)=>{const p=ease.outBack(prog(t,c.yesterday+.20+i*.12,.42));chip.style.opacity=clamp(prog(t,c.yesterday+.20+i*.12,.13));chip.style.transform=`translateY(${(1-p)*18}px) scale(${lerp(.92,1,p)})`;});
  const pe=ease.inCubic(prog(t,exit0,.42));S.content.style.opacity=1-pe;S.content.style.transform=`translateY(${-16*pe}px)`;S.pn.style.opacity=pp.alpha*(1-pe);return true;
};
const _init=window.init;
window.init=function(cues){
  const M={finished:["finished",1],most:["most",1],ed:["ed",1],irregular:["irregular",1],i:["i",1],was:["was",1],in2013:["2013",1],fire:["fire",1],broke:["broke",1],yesterday:["yesterday",1]};
  for(const [k,[p,n]] of Object.entries(M))cues[k]=cue(p,n);return _init(cues);
};
})();
