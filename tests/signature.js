const path=require('path');const GAME='file://'+path.resolve(process.env.GAME||path.join(__dirname,'../src/meteorite-kids-battle.html'));
// Adult signature moves: present in Ch 19 to 21 and the Ch 25 rematch only, each does its job, and recharges.
const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.route('**/fonts.googleapis.com/**',r=>r.abort());await p.goto(GAME);await p.waitForTimeout(800);
const r=await p.evaluate(async()=>{window.playCutscene=async()=>{};TITLE.active=false;HUB.active=false;const out={};
 const go=async C=>{startBattle(C,true);await new Promise(r=>setTimeout(r,350))};
 const sigs=()=>activeAlive().map(k=>(actionsFor(k).find(a=>SIG[k.id]&&a.label===SIG[k.id].label)||{}).label||null);
 for(const key of ['ch19','ch20','ch21','ch22','ch13']){await go(CHAPTERS.find(c=>c.key===key));out[key]=sigs();S.over=true}
 await go(CH25R);out.ch25r=sigs();S.over=true;
 await go(CHAPTERS.find(c=>c.key==='ch19'));const K=id=>S.roster.find(k=>k.id===id);const act=(id)=>actionsFor(K(id)).find(a=>a.label===SIG[id].label);
 // put everyone on the field for the checks
 S.roster.forEach(k=>{k.hp=Math.round(k.hpMax*.5)});
 const J=K('lightheart');if(kidPos(J)){await act('lightheart').run();out.rally=activeAlive().filter(k=>k!==J).every(k=>k.haste>0);out.recharge=J.sgcd===3&&act('lightheart').disabled}
 const sc=K('scareth');if(kidPos(sc)){await act('scareth').run();out.stuntTarget=pickTarget()===sc;const h=sc.hp;damageKid(sc,50);out.stuntDodged=sc.hp===h&&!sc.stunt}
 const ka=K('kaytahn');if(kidPos(ka)){const t=activeAlive().sort((a,c)=>a.hp/a.hpMax-c.hp/c.hpMax)[0];const h=t.hp;await act('kaytahn').run();out.triage=t.hp>h}
 return out});
console.log(JSON.stringify(r),errs);
const want=['Rally Call','Stunt Double','Triage','Field Repair','Recall'];
const has=a=>a.filter(Boolean).length>0&&a.filter(Boolean).every(l=>want.includes(l));
const ok=has(r.ch19)&&has(r.ch20)&&has(r.ch21)&&has(r.ch25r)&&r.ch22.every(x=>!x)&&r.ch13.every(x=>!x)&&r.rally!==false&&r.recharge!==false&&r.stuntTarget!==false&&r.stuntDodged!==false&&r.triage!==false&&!errs.length;
console.log(ok?'PASS':'FAIL');await b.close();process.exit(ok?0:1)})();
