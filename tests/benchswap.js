const path=require('path');const GAME='file://'+path.resolve(process.env.GAME||path.join(__dirname,'../src/meteorite-kids-battle.html'));const OUT=path.join(__dirname,'out');require('fs').mkdirSync(OUT,{recursive:true});
// Ch 23: after the active friends use their Stone Echo, the Swap button glows, sits on top, names who is waiting, and a caption appears once.
const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1000,height:800}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.route('**/fonts.googleapis.com/**',r=>r.abort());await p.goto(GAME);await p.waitForTimeout(800);
const r=await p.evaluate(async()=>{window.playCutscene=async()=>{};TITLE.active=false;HUB.active=false;
 startBattle(CHAPTERS.find(c=>c.key==='ch23'),true);await new Promise(r=>setTimeout(r,400));
 const act=activeAlive(),bench=benchAlive();const before=actionsFor(act.find(k=>k.id!=='lightheart'));
 S.friendUsed={};act.forEach(k=>{if(k.id!=='lightheart')S.friendUsed[k.id]=true});
 const J=act.find(k=>k.id==='lightheart')||act[0];const A=actionsFor(J);const sw=A.find(a=>a.label==='Swap');
 const chips=S.ch.chips(S.boss).map(c=>c.t);
 return {active:act.map(k=>k.name),bench:bench.map(k=>k.name),swapBeforeIsFirst:before[0].label==='Swap',swapFirst:A[0].label==='Swap',pulse:!!sw.pulse,desc:sw.desc,cap:document.getElementById('cap').hidden?null:document.getElementById('cap').textContent,chips}});
console.log(JSON.stringify(r,null,1));
await p.evaluate(()=>{const J=activeAlive().find(k=>k.id==='lightheart');chooseAction(J)});await p.waitForTimeout(500);
await p.screenshot({path:path.join(OUT,'benchswap.png')});console.log(errs);await b.close()})();
