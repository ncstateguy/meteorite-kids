const path=require('path');const GAME='file://'+path.resolve(process.env.GAME||path.join(__dirname,'../src/meteorite-kids-battle.html'));const OUT=path.join(__dirname,'out');require('fs').mkdirSync(OUT,{recursive:true});
// Forge: Part 2 and Part 3 tiers appear only once that part is reached, cost the new boss materials, and boss wins drop them.
const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1000,height:1100}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.route('**/fonts.googleapis.com/**',r=>r.abort());await p.goto(GAME);await p.waitForTimeout(800);
const r=await p.evaluate(async()=>{TITLE.active=false;const out={};const q=P();const g=G();
 ['opening','dream','ch1','ch2','ch3','ch4','ch5','ch6','ch7','ch8','ch9','ch10','ch11','ch12'].forEach(k=>progress[k]=true);
 g.gear.lightheart.w=3;g.gear.lightheart.o=3;q.coins=1000;q.mats={Soot:20,'Rift Shard':3,'Guardian Stone':3};
 openForge('lightheart');out.part1=!!document.getElementById('craftW');
 progress.ch13=true;openForge('lightheart');out.part2Offer=document.getElementById('craftW')&&document.getElementById('craftW').textContent;
 document.getElementById('craftW').click();out.afterBuy={w:g.gear.lightheart.w,coins:q.coins,rift:q.mats['Rift Shard']};
 out.part3Hidden=!document.getElementById('craftW');progress.ch19=true;openForge('lightheart');out.part3Offer=document.getElementById('craftW')&&document.getElementById('craftW').textContent;
 out.mats={ch14:MATS.ch14[0],ch18:MATS.ch18[0],ch22:MATS.ch22[0]};return out});
console.log(JSON.stringify(r,null,1));await p.screenshot({path:path.join(OUT,'forge.png')});console.log(errs);
const ok=!r.part1&&/Rift-Tempered/.test(r.part2Offer)&&r.afterBuy.w===4&&r.afterBuy.coins===920&&r.afterBuy.rift===2&&r.part3Hidden&&/Guardian-Forged/.test(r.part3Offer)&&!errs.length;
console.log(ok?'PASS':'FAIL');await b.close();process.exit(ok?0:1)})();
