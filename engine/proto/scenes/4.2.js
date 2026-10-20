"use strict";
// Level 4.2 — a synopsis uses present tenses: story-card family.
(() => {
document.head.insertAdjacentHTML("beforeend", `<style>
.definition{position:absolute;box-sizing:border-box;border:1.5px solid rgba(46,230,255,.64);border-radius:22px;background:rgba(46,230,255,.07)}
.story-comic{position:absolute;box-sizing:border-box;overflow:hidden;border:2px solid rgba(255,255,255,.72);border-radius:24px;background:linear-gradient(180deg,#14275F 0%,#1B4189 48%,#3A7FC2 66%)}
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
  // Illustrated beach (comic-local 1228 x 486): sky (CSS) > sun > back/mid waves > shark > front wave > sand, umbrella, towels > splash > burst.
  const PER=120, wave=(y,a)=>{let d=`M${-2*PER} ${y}`;for(let x=-2*PER;x<1228+2*PER;x+=PER)d+=` q${PER/4} ${-a} ${PER/2} 0 t${PER/2} 0`;return d+` L${1228+2*PER} 500 L${-2*PER} 500 Z`;};
  const rays=Array.from({length:12},(_,i)=>{const a=i*Math.PI/6;return `<line x1="${Math.cos(a)*58}" y1="${Math.sin(a)*58}" x2="${Math.cos(a)*76}" y2="${Math.sin(a)*76}"/>`;}).join("");
  const wedges=Array.from({length:6},(_,i)=>{const a0=Math.PI+i*Math.PI/6,a1=a0+Math.PI/6,r=98;
    return `<path d="M0 0 L${(Math.cos(a0)*r).toFixed(1)} ${(Math.sin(a0)*r).toFixed(1)} A${r} ${r} 0 0 1 ${(Math.cos(a1)*r).toFixed(1)} ${(Math.sin(a1)*r).toFixed(1)} Z" fill="${i%2?"#FFF3F8":"#FF4FA3"}"/>`;}).join("");
  const svg=(z,inner)=>{const d=el("div",null,{position:"absolute",left:"0",top:"0",width:"1228px",height:"486px",zIndex:z},comic);
    d.innerHTML=`<svg width="1228" height="486" viewBox="0 0 1228 486" style="position:absolute;left:0;top:0;overflow:visible">${inner}</svg>`;return d;};
  const back=svg(1,`<defs><radialGradient id="sunGlow"><stop offset="0" stop-color="#FFE873" stop-opacity=".55"/><stop offset="1" stop-color="#FFD93D" stop-opacity="0"/></radialGradient></defs>
    <g transform="translate(905 100)"><circle r="120" fill="url(#sunGlow)"/><g class="sunRays" stroke="#FFD93D" stroke-width="7" stroke-linecap="round" opacity=".85">${rays}</g><circle r="46" fill="#FFD93D"/></g>
    <path class="w1" d="${wave(314,9)}" fill="#1B5FA8"/><path class="w2" d="${wave(350,11)}" fill="#1A7EC4"/>`);
  const shark=el("div",null,{position:"absolute",left:"792px",top:"164px",width:"276px",height:"276px",zIndex:2,transformOrigin:"50% 80%",filter:"drop-shadow(0 8px 14px rgba(8,20,60,.45))"},comic);
  shark.innerHTML=ART.shark;
  const front=svg(3,`<defs><linearGradient id="sand" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F7D894"/><stop offset="1" stop-color="#E2A458"/></linearGradient></defs>
    <path class="w3" d="${wave(394,10)}" fill="#22A8DE" stroke="#8FE9FF" stroke-opacity=".75" stroke-width="4"/>
    <path d="M0 402 C160 386 330 404 480 446 C540 462 580 476 616 490 L0 490 Z" fill="url(#sand)"/>
    <g transform="rotate(-4 70 446)"><rect x="40" y="432" width="150" height="30" rx="8" fill="#2EE6FF"/><rect x="40" y="443" width="150" height="8" fill="#FFFFFF" opacity=".8"/></g>
    <g transform="rotate(3 410 462)"><rect x="345" y="450" width="140" height="28" rx="8" fill="#FFD93D"/><rect x="345" y="460" width="140" height="8" fill="#FF8A3D" opacity=".85"/></g>
    <g transform="rotate(-8 300 456)"><line x1="300" y1="346" x2="300" y2="456" stroke="#F4EEFF" stroke-width="7" stroke-linecap="round"/>
      <g transform="translate(300 346)">${wedges}<circle cy="-98" r="7" fill="#F4EEFF"/></g></g>
    <g class="splash"><ellipse class="foam" cx="905" cy="392" rx="120" ry="16" fill="#E8FBFF" opacity="0"/>${Array.from({length:9},()=>'<circle class="drop" r="9" fill="#D9F8FF" opacity="0"/>').join("")}</g>`);
  const burst=el("div",null,{position:"absolute",left:"1034px",top:"98px",width:"156px",height:"156px",zIndex:4,opacity:0},comic);
  const pts=Array.from({length:28},(_,i)=>{const a=-Math.PI/2+i*Math.PI/14,r=i%2?52:78;return `${(78+Math.cos(a)*r).toFixed(1)},${(78+Math.sin(a)*r).toFixed(1)}`;}).join(" ");
  burst.innerHTML=`<svg width="156" height="156" viewBox="0 0 156 156" style="overflow:visible;filter:drop-shadow(0 0 14px rgba(255,217,61,.55))"><polygon points="${pts}" fill="#FFD93D" stroke="#FF4FA3" stroke-width="5" stroke-linejoin="round"/>
    <text x="78" y="106" text-anchor="middle" font-family="Fredoka" font-weight="600" font-size="84" fill="#281450">!</text></svg>`;
  const drops=[...front.querySelectorAll(".drop")].map((e,i)=>({e,a:Math.PI*(.18+.64*i/8),v:110+(i%3)*38}));
  const sn=sentence("Dora and Sam {are resting|p} on the\nbeach when suddenly, they {spot|y} a\nshark …",150,510,42,content);
  S={c,pn,content,def,defSn,formA,arrow,formB,rule,lively,dramatic,comic,sn,shark,burst,drops,PER,rays:back.querySelector(".sunRays"),
    w:[back.querySelector(".w1"),back.querySelector(".w2"),front.querySelector(".w3")],foam:front.querySelector(".foam")};
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
  s.rays.setAttribute("transform",`rotate(${t*12})`);
  [14,-22,30].forEach((v,i)=>s.w[i].setAttribute("transform",`translate(${((t*v)%s.PER+s.PER)%s.PER-s.PER} 0)`));
  riseWords(s.sn,t,c.dora-.1);s.sn.groups.forEach((g,i)=>sweep(g,t,i?c.spot:c.resting,.38));
  const re=ease.outBack(prog(t,c.spot-.14,.62)),bob=t>c.spot+.5?Math.sin((t-c.spot-.5)*2.6)*5:0;   // shark leaps out of the sea on 'spot'
  s.shark.style.opacity=clamp(prog(t,c.spot-.14,.10));s.shark.style.transform=`translateY(${(1-re)*250+bob}px) rotate(${lerp(16,-4,re)}deg)`;
  const sq=prog(t,c.spot+.02,.75);
  s.drops.forEach(d=>{d.e.setAttribute("cx",(905+Math.cos(d.a)*d.v*sq*1.6).toFixed(1));d.e.setAttribute("cy",(390-Math.sin(d.a)*d.v*sq*1.5+170*sq*sq).toFixed(1));d.e.setAttribute("opacity",sq>0&&sq<1?(.95*(1-sq)).toFixed(3):0);});
  s.foam.setAttribute("opacity",sq>0&&sq<1?(.8*(1-sq)).toFixed(3):0);s.foam.setAttribute("rx",(60+90*ease.outCubic(sq)).toFixed(1));
  const bp=ease.outBack(prog(t,c.shark,.32));s.burst.style.opacity=clamp(prog(t,c.shark,.06));s.burst.style.transform=`scale(${Math.max(0,bp)}) rotate(${lerp(-24,-6,clamp(bp))}deg)`;
  exitLift(s.content,t);return true;
};
})();
