"use strict";
// Scene 1.3 — Present continuous: form plus five uses, with the approved give-me-five hand.
(() => {
document.head.insertAdjacentHTML("beforeend", `<style>
html,body{margin:0;width:1920px;height:1080px;background:transparent;overflow:hidden}body{-webkit-font-smoothing:antialiased;text-rendering:geometricPrecision}.mask{position:absolute;overflow:hidden;padding:.10em .04em .18em;margin:-.10em -.04em -.18em}.inner{display:block;white-space:nowrap;will-change:transform}.sent{position:absolute;white-space:nowrap;font-family:"Nunito";font-weight:800;color:#fff;line-height:1.18}.wm{display:inline-block;overflow:hidden;vertical-align:top;padding:0 .03em .16em;margin:0 -.03em -.16em}.wi{display:inline-block;will-change:transform}.hl{position:relative;display:inline-block;isolation:isolate;margin:0 .07em}.mk{position:absolute;left:-.09em;right:-.09em;top:.17em;bottom:.05em;border-radius:.2em;z-index:-1;transform-origin:left center}.label{font-family:"Nunito";font-weight:800;letter-spacing:.14em;text-transform:uppercase}.num{font-family:"Fredoka";font-weight:600;font-feature-settings:"tnum" 1}.tok{position:absolute;display:flex;align-items:center;justify-content:center;height:44px;padding:0 12px;box-sizing:border-box;border-radius:13px;font-family:"Nunito";font-weight:800;font-size:22px;line-height:1;white-space:nowrap;transform-origin:left center}.hand{position:absolute;object-fit:contain;pointer-events:none;transform-origin:center center}.chip{position:absolute;display:flex;align-items:center;height:48px;padding:0 18px;box-sizing:border-box;border-radius:24px;border:2px solid rgba(46,230,255,.58);background:rgba(46,230,255,.10);color:#2EE6FF;font-family:"Nunito";font-weight:800;font-size:24px;white-space:nowrap;transform-origin:left center}
</style>`);
const PANEL={x:60,y:130,h:900}, L=116, COL=196, R=1114;
const ROWY=[300,432,564,696,828], ROWH=112;
let S=null;
function token(text,x,y,border,bg,color,parent){const e=el("div","tok",{left:x+"px",top:y+"px",border:`2px solid ${border}`,background:bg,color:color||C.white},parent);e.textContent=text;return e;}
function counter(parent){
  const box=el("div","num",{position:"absolute",top:"192px",right:(1920-R)+"px",fontSize:"30px",lineHeight:"1",display:"flex",alignItems:"flex-start",color:"rgba(255,255,255,.45)"},parent);
  const mask=el("div",null,{position:"relative",overflow:"hidden",height:"36px",width:"40px",marginRight:"10px"},box);
  const strip=el("div",null,{position:"absolute",left:"0",top:"0",lineHeight:"36px",color:C.pink},mask);strip.innerHTML="01<br>02<br>03<br>04<br>05";
  const total=el("div",null,{lineHeight:"36px"},box);total.textContent="/ 05";return {box,strip};
}
window.init=function(cues){
  const c=cues; c.dim=c.dim!==false;
  const pn=panel(PANEL.x,PANEL.y,1110,PANEL.h);
  const content=el("div",null,{position:"absolute",inset:"0"});
  const title=masked("Present continuous",{left:L+"px",top:"176px",fontFamily:"Fredoka",fontWeight:600,fontSize:"58px",color:C.white,lineHeight:"1"},content);
  const tokA=token("am / is / are",640,186,C.pink,"rgba(255,79,168,.10)",C.white,content);
  const plus=el("div","num",{position:"absolute",left:"798px",top:"184px",fontSize:"34px",lineHeight:"44px",color:"rgba(255,255,255,.72)"},content);plus.textContent="+";
  const tokV=token("verb",830,186,"rgba(255,255,255,.42)","rgba(255,255,255,.06)",C.white,content);
  const tokI=token("-ing",914,186,C.pink,C.pink,C.ink,content);
  const ct=counter(content), rule0=hrule(L,266,R-L,.18,content);
  // The approved hand art is deliberately reused verbatim, not redrawn in CSS/SVG.
  const bigHands=[], smallHands=[];
  for(let i=0;i<6;i++){
    bigHands.push(el("img","hand",{left:"565px",top:"355px",width:"300px",height:"350px",opacity:0},content));bigHands[i].src=`assets/1.3/hand_${i}.png`;
    smallHands.push(el("img","hand",{left:"958px",top:"282px",width:"126px",height:"147px",opacity:0},content));smallHands[i].src=`assets/1.3/hand_small_${i}.png`;
  }
  const give=masked("GIVE ME FIVE!",{left:"507px",top:"750px",fontFamily:"Fredoka",fontWeight:600,fontSize:"64px",color:C.yellow,lineHeight:"1",whiteSpace:"nowrap"},content);
  const railX=86, rail=el("div",null,{position:"absolute",left:railX+"px",top:(ROWY[0]+16)+"px",width:"2px",height:(ROWY[4]+ROWH-16-ROWY[0]-16)+"px",background:"rgba(255,255,255,.10)",transformOrigin:"center top"},content);
  const activeRail=el("div",null,{position:"absolute",left:(railX-1)+"px",width:"4px",borderRadius:"2px",background:C.pink,boxShadow:"0 0 14px rgba(255,79,168,.65)"},content);
  const defs=[
    {lab:"RIGHT NOW",ex:"Look! Snow {is falling|p}.",start:c.one,labCue:c.right,exCue:c.look,marks:[c.is1]},
    {lab:"TEMPORARY SITUATIONS",ex:"I {am learning|p} to swim at present.",start:c.two,labCue:c.temporary,exCue:c.i,marks:[c.am]},
    {lab:"CHANGING TRENDS",ex:"House husbands {are becoming|p} more popular.",start:c.three,labCue:c.changing,exCue:c.house,marks:[c.are]},
    {lab:"PHOTOS & PICTURES",ex:"Everyone {is smiling|p} happily in the photo.",start:c.four,labCue:c.photos,exCue:c.everyone,marks:[c.is2]},
    {lab:"ANNOYING HABITS + always",ex:"He {is|p} {always|t} {complaining|p} about his job.",start:c.five,labCue:c.annoying,exCue:c.he,marks:[c.is3,c.always,c.complaining]}
  ];
  const rows=defs.map((r,i)=>{
    const y=ROWY[i], g=el("div",null,{position:"absolute",inset:"0"},content);
    const num=masked(String(i+1).padStart(2,"0"),{left:L+"px",top:(y+24)+"px",fontFamily:"Fredoka",fontWeight:600,fontSize:"30px",color:C.pink,lineHeight:"1"},g);
    const lab=masked(r.lab,{left:COL+"px",top:(y+27)+"px",fontSize:"20px",color:C.lilac,lineHeight:"1"},g);lab.o.classList.add("label");
    const sn=sentence(r.ex,COL,y+59,34,g);
    const rule=i<4?hrule(L,y+ROWH,R-L,.10,g):null;
    return Object.assign({},r,{y,g,num,lab,sn,rule});
  });
  let size=34;const widest=()=>Math.max(...rows.map(r=>r.sn.box.getBoundingClientRect().width));
  while(COL+widest()>936&&size>28){size--;rows.forEach(r=>r.sn.box.style.fontSize=size+"px");}
  S={c,pn,content,title,tokA,plus,tokV,tokI,ct,rule0,bigHands,smallHands,give,rail,activeRail,rows,size};
  return {size,handDisplay:[300,126]};
};
function setHand(images,index,transT,t,gate){
  const p=ease.outCubic(prog(t,transT,.20));
  images.forEach((im,k)=>{let op=0;if(k===index)op=p;else if(k===Math.max(0,index-1))op=1-p;im.style.opacity=op*gate;});
}
window.seek=function(t){
  const {c,rows}=S, review=c.voice_end+.35, exit0=c.dur-.45;
  const pp=followPanel(S.pn,t,PANEL.x);
  reveal(S.title,ease.outExpo(prog(t,.05,.8)));S.rule0.style.transform=`scaleX(${ease.outExpo(prog(t,.2,1))})`;
  const tokIn=(node,t0)=>{const p=ease.outExpo(prog(t,t0,.6));node.style.opacity=clamp(p*1.5);node.style.transform=`translateY(${(1-p)*18}px)`;};
  tokIn(S.tokA,2.0);tokIn(S.plus,2.18);tokIn(S.tokV,2.46);
  const pd=spring(t-c.plus,13,.72), po=clamp(prog(t,c.plus,.15));S.tokI.style.opacity=po;S.tokI.style.transform=`translateX(${(1-pd)*86}px)`;
  const dock=ease.outCubic(prog(t,c.plus+.25,.2));S.tokV.style.borderRadius=`14px ${lerp(14,3,dock)}px ${lerp(14,3,dock)}px 14px`;S.tokI.style.borderRadius=`${lerp(14,3,dock)}px 14px 14px ${lerp(14,3,dock)}px`;
  const useTimes=[c.one,c.two,c.three,c.four,c.five];let state=0;useTimes.forEach((u,i)=>{if(t>=u)state=i+1;});const stateT=state?useTimes[state-1]:c.give;
  const handIn=ease.outBack(prog(t,c.give+.06,.42)), handOff=ease.inOutCubic(prog(t,c.one-.22,.45));
  setHand(S.bigHands,state,stateT,t,handIn*(1-handOff));setHand(S.smallHands,state,stateT,t,handOff);
  reveal(S.give,ease.outBack(prog(t,c.give+.12,.42)));const giveOut=ease.inCubic(prog(t,c.one-.22,.25));S.give.o.style.opacity=1-giveOut;S.give.o.style.transform=`translateY(${-16*giveOut}px)`;
  const active=t<rows[1].start?0:t<rows[2].start?1:t<rows[3].start?2:t<rows[4].start?3:4;
  S.ct.box.style.opacity=ease.outCubic(prog(t,rows[0].start,.35));let ci=0;rows.forEach((r,i)=>{if(i)ci+=ease.outExpo(prog(t,r.start,.55));});S.ct.strip.style.transform=`translateY(${-36*ci}px)`;
  S.rail.style.transform=`scaleY(${ease.outExpo(prog(t,rows[0].start,.8))})`;
  let top=rows[0].y+16,bot=rows[0].y+ROWH-16;rows.forEach((r,i)=>{if(!i)return;const p=spring(t-r.start);top=lerp(top,r.y+16,p);bot=lerp(bot,r.y+ROWH-16,p);});top=lerp(top,rows[0].y+16,ease.inOutCubic(prog(t,review,.7)));const rg=ease.outExpo(prog(t,rows[0].start,.6));S.activeRail.style.top=top+"px";S.activeRail.style.height=Math.max(0,(bot-top)*rg)+"px";S.activeRail.style.opacity=rg;
  rows.forEach((r,i)=>{
    reveal(r.num,ease.outExpo(prog(t,r.start,.65)));reveal(r.lab,ease.outExpo(prog(t,r.labCue-.08,.65)));if(r.rule)r.rule.style.transform=`scaleX(${ease.outExpo(prog(t,r.start+.18,.9))})`;
    riseWords(r.sn,t,r.exCue-.12);r.sn.groups.forEach((g,k)=>{const last=r.sn.words.indexOf(g.words[g.words.length-1]);const landed=r.exCue-.12+last*.05+.3;sweep(g,t,Math.max(r.marks[k],landed),.38);});
    let dim=0;if(c.dim&&i<rows.length-1)dim=ease.inOutCubic(prog(t,rows[i+1].start,.5))*(1-ease.inOutCubic(prog(t,review,.6)));r.g.style.opacity=1-.6*dim;
  });
  const pe=ease.inCubic(prog(t,exit0,.42));S.content.style.opacity=1-pe;S.content.style.transform=`translateY(${-16*pe}px)`;S.pn.style.opacity=pp.alpha*(1-pe);
  return true;
};
const _init=window.init;
window.init=function(cues){
  const M={plus:["plus",1],give:["give",1],one:["one",1],right:["right",1],look:["look",1],is1:["is",2],two:["two",1],temporary:["temporary",1],i:["i",1],am:["am",1],three:["three",1],changing:["changing",1],house:["house",1],are:["are",1],four:["four",1],photos:["photos",1],everyone:["everyone",1],is2:["is",3],five:["five",3],annoying:["annoying",1],he:["he",1],is3:["is",4],always:["always",2],complaining:["complaining",1]};
  for(const [k,[p,n]] of Object.entries(M))cues[k]=cue(p,n);
  const info=_init(cues);const c=cues;fx(c.plus+.45,"click",.8);fx(c.give+.10,"pop",.8);[c.one,c.two,c.three,c.four,c.five].forEach(t=>fx(t,"pop",.6));return info;
};
})();
