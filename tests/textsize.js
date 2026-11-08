const path=require('path');const GAME='file://'+path.resolve(process.env.GAME||path.join(__dirname,'../src/meteorite-kids-battle.html'));const OUT=path.join(__dirname,'out');require('fs').mkdirSync(OUT,{recursive:true});
// Text size: cycles Normal, Large, Larger; scales the menus and dialogue; remembered after reload; no sideways scroll at phone width.
const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const ctx=await b.newContext({viewport:{width:1000,height:1100}});const p=await ctx.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.route('**/fonts.googleapis.com/**',r=>r.abort());await p.goto(GAME);await p.waitForTimeout(900);
const r={};
await p.evaluate(()=>{TITLE.pressed=true;titlePress(true)});r.titleBtn=await p.textContent('#tText');
const size=()=>p.evaluate(()=>{const m=document.getElementById('menu');return {ts:getComputedStyle(document.documentElement).getPropertyValue('--ts').trim(),h:Math.round(m.getBoundingClientRect().height),w:Math.round(m.getBoundingClientRect().width)}});
r.normal=await size();await p.click('#tText');await p.click('#tText');r.larger=await size();r.btn=await p.textContent('#tText');
await p.screenshot({path:path.join(OUT,'text_larger.png')});
// battle at Larger
await p.evaluate(async()=>{window.playCutscene=async()=>{};TITLE.active=false;startBattle(CHAPTERS.find(c=>c.key==='ch3'),true);await new Promise(r=>setTimeout(r,500));S.boss.frenzy=true});await p.waitForTimeout(400);
await p.screenshot({path:path.join(OUT,'text_battle.png'),fullPage:true});
r.warnChip=await p.evaluate(()=>{const c=document.querySelector('.chip.warn');return c?getComputedStyle(c,'::before').content:null});
await p.reload();await p.waitForTimeout(900);r.afterReload=(await size()).ts;
// phone width
await p.setViewportSize({width:390,height:800});await p.evaluate(()=>{TITLE.pressed=true;titlePress(true)});await p.waitForTimeout(300);
r.phoneOverflow=await p.evaluate(()=>document.documentElement.scrollWidth>window.innerWidth+1);
console.log(JSON.stringify(r,null,1),errs);
const ok=r.normal.ts==='1'&&r.larger.ts==='1.4'&&r.larger.h>r.normal.h*1.2&&/Larger/.test(r.btn)&&r.afterReload==='1.4'&&!r.phoneOverflow&&!errs.length;
console.log(ok?'PASS':'FAIL');await b.close();process.exit(ok?0:1)})();
