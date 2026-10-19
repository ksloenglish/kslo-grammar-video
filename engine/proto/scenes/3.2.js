"use strict";
// 3.2 Non-action verbs — right and wrong, with -ing absorbed by the teaching sign.
(() => {
  document.head.insertAdjacentHTML("beforeend", `<style>
    .rw-root { position:absolute; inset:0; }
    .rw-zone { position:absolute; display:flex; align-items:center; justify-content:center; width:310px; height:62px; box-sizing:border-box;
      border:2px solid #FF4FA8; border-radius:14px; background:rgba(255,79,168,.10); box-shadow:0 0 18px rgba(255,79,168,.28);
      color:#FF4FA8; font-family:Fredoka; font-weight:600; font-size:28px; letter-spacing:.025em; word-spacing:.12em; white-space:nowrap; }
    .rw-pair { position:absolute; left:116px; width:998px; height:272px; box-sizing:border-box; border-top:1.5px solid rgba(255,255,255,.12); }
    .rw-good, .rw-bad { position:absolute; left:80px; }
    .rw-ing { position:absolute; display:flex; align-items:center; height:42px; padding:0 15px; box-sizing:border-box; border-radius:21px;
      background:#FF4FA8; color:#281450; box-shadow:0 0 14px rgba(255,79,168,.45); font-family:Nunito; font-weight:900; font-size:23px; line-height:1; transform-origin:center center; }
    .rw-ring { position:absolute; width:42px; height:42px; box-sizing:border-box; border:3px solid #FF4FA8; border-radius:50%; transform-origin:center center; }
    .rw-strike { position:absolute; overflow:visible; }
    .rw-strike path { fill:none; stroke:#FF5468; stroke-width:6; stroke-linecap:round; }
  </style>`);

  const PANEL={x:60,y:130,h:900}, L=116, COL=196, R=1114;
  let S=null;
  const makeStrike=(x,y,w,parent)=>{
    const s=el("svg","rw-strike",{left:x+"px",top:y+"px",width:w+"px",height:"30px"},parent); s.setAttribute("viewBox",`0 0 ${w} 30`);
    const p=document.createElementNS("http://www.w3.org/2000/svg","path"); p.setAttribute("d",`M 4 24 L ${w-4} 6`); s.appendChild(p);
    const len=p.getTotalLength(); p.style.strokeDasharray=`${len} ${len}`; p.style.strokeDashoffset=len;
    return {s,p,len};
  };

  window.init=function(c){
    const pn=panel(PANEL.x,PANEL.y,R-PANEL.x,PANEL.h);
    const root=el("div","rw-root");
    const title=masked("Non-action verbs",{left:L+"px",top:"176px",fontFamily:"Fredoka",fontWeight:600,fontSize:"58px",color:C.white,lineHeight:"1",wordSpacing:".11em"},root);
    const zone=el("div","rw-zone",{left:"704px",top:"182px"},root); zone.textContent="NO -ing ZONE";
    const rule=hrule(L,266,R-L,.18,root);
    const defs=[
      { y:312, ok:"I {think} game shows are exciting.", bad:"I {am thinking|p} game shows are exciting.", okStart:c.i1, badStart:c.not1, verb:c.think, mark:c.thinking, end:c.thinkingEnd },
      { y:628, ok:"Mike {has} one brother and one sister.", bad:"Mike {is having|p} one brother and one sister.", okStart:c.mike, badStart:c.not2, verb:c.has, mark:c.having, end:c.havingEnd },
    ];
    const pairs=defs.map((d,i)=>{
      const g=el("div",null,{position:"absolute",inset:"0"},root);
      const divider=hrule(L,d.y,R-L,.10,g);
      const ok=sentence(d.ok,COL,d.y+30,36,g);
      const bad=sentence(d.bad,COL,d.y+151,36,g); bad.box.style.color=C.dim;
      const okW=ok.box.getBoundingClientRect().width, badW=bad.box.getBoundingClientRect().width;
      const tic=icon("tick",Math.min(R-65,COL+okW+34),d.y+22,54,"#5CF2B0","#5CF2B0",g,4.2);
      const cross=icon("cross",Math.min(R-65,COL+badW+34),d.y+143,54,"#FF5468","#FF5468",g,4.2);
      const strike=makeStrike(COL,d.y+163,Math.min(badW+2,R-COL-38),g);
      const grp=bad.groups[0].host.getBoundingClientRect();
      const ing=el("div","rw-ing",{left:(grp.right-34)+"px",top:(grp.top-48)+"px"},g); ing.textContent="-ing";
      const ring=el("div","rw-ring",{left:"838px",top:"192px"},root); // centred on the sign; a disappearing pill never rests over it
      return Object.assign({},d,{g,divider,ok,bad,tic,cross,strike,ing,ring,from:{x:grp.right-34,y:grp.top-48}});
    });
    S={c,pn,root,title,zone,rule,pairs};
    return {pairs:pairs.length};
  };

  window.seek=function(t){
    const {c,pairs}=S;
    followPanel(S.pn,t,PANEL.x);
    reveal(S.title,ease.outExpo(prog(t,.05,.75)));
    const zp=ease.outExpo(prog(t,.20,.6)); S.zone.style.opacity=zp; S.zone.style.transform=`translateY(${(1-zp)*14}px)`;
    S.rule.style.transform=`scaleX(${ease.outExpo(prog(t,.20,1.0))})`;
    pairs.forEach((r,i)=>{
      const enter=ease.outExpo(prog(t,r.okStart-.08,.55)); r.g.style.opacity=enter; r.g.style.transform=`translateY(${(1-enter)*12}px)`;
      r.divider.style.transform=`scaleX(${ease.outExpo(prog(t,r.okStart-.04,.8))})`;
      riseWords(r.ok,t,r.okStart-.05); riseWords(r.bad,t,r.badStart-.03);
      r.ok.groups.forEach(g=>sweep(g,t,c[i?"has":"think"],.34));
      r.bad.groups.forEach(g=>sweep(g,t,r.mark,.32));
      const pc=ease.outBack(prog(t,r.okStart+.50,.38)); r.tic.s.style.opacity=clamp(pc*1.4); r.tic.s.style.transform=`scale(${Math.max(0,pc)})`; drawIcon(r.tic,clamp(pc));
      const px=ease.outBack(prog(t,r.end+.30,.38)); r.cross.s.style.opacity=clamp(px*1.4); r.cross.s.style.transform=`scale(${Math.max(0,px)})`; drawIcon(r.cross,clamp(px));
      const ps=ease.outCubic(prog(t,r.end+.05,.35)); r.strike.p.style.strokeDashoffset=r.strike.len*(1-ps);
      const fly=ease.inOutCubic(prog(t,r.end-.10,.50));
      const dx=859-(r.from.x+26), dy=213-(r.from.y+21);
      const vanish=ease.inCubic(prog(t,r.end+.18,.20));
      r.ing.style.opacity=(t<r.end-.10?0:1-vanish); r.ing.style.transform=`translate(${dx*fly}px,${dy*fly}px) scale(${lerp(1,.10,fly)})`;
      const rp=prog(t,r.end+.36,.40); r.ring.style.opacity=rp>0&&rp<1?(1-rp)*.9:0; r.ring.style.transform=`scale(${lerp(.35,1.9,ease.outCubic(rp))})`;
    });
    exitLift(S.root,t);
    return true;
  };

  const _init=window.init;
  window.init=function(c){
    const M={i1:["i",1],think:["think",1],not1:["not",1],thinking:["thinking",1],thinkingEnd:["thinking",1,true],mike:["mike",1],has:["has",1],not2:["not",2],having:["having",1],havingEnd:["having",1,true]};
    for(const [k,a] of Object.entries(M)) c[k]=cue(a[0],a[1],a[2]||false);
    const info=_init(c);
    fx(c.i1+.50,"correct",.6); fx(c.mike+.50,"correct",.6);
    fx(c.thinkingEnd+.05,"buzz",.6); fx(c.havingEnd+.05,"buzz",.6);
    return info;
  };
})();
