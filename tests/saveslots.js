const path=require('path');const GAME='file://'+path.resolve(process.env.GAME||path.join(__dirname,'../src/meteorite-kids-battle.html'));
// Save files stay separate: progress in File 1 never leaks into a new game in File 2, and loading File 1 brings it back, also after a reload.
const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const ctx=await b.newContext();const p=await ctx.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.route('**/fonts.googleapis.com/**',r=>r.abort());await p.goto(GAME);await p.waitForTimeout(1000);
const st=()=>p.evaluate(()=>({ch12:!!progress.ch12,coins:progress.coins||0,hub:Object.keys(HUB.state).length,active:SAVE.active}));
const r={};
await p.evaluate(async()=>{window.startGame=()=>{};progress.opening=true;progress.dream=true;['ch1','ch2','ch3','ch12'].forEach(k=>progress[k]=true);P().coins=321;HUB.state.shard_a=true;HUB.state.hollisR=true;SAVE.active=0;await writeSlot(0)});
r.file1=await st();
await p.evaluate(async()=>{SAVE.mode='new';await slotPick(1)});r.newFile2=await st();
await p.evaluate(async()=>{progress.opening=true;P().coins=5;saveProgress();await writeSlot(1)});
await p.reload();await p.waitForTimeout(1200);
r.afterReload=await st();
await p.evaluate(async()=>{window.startGame=()=>{};SAVE.mode='load';await slotPick(0)});r.loadFile1=await st();
await p.evaluate(async()=>{SAVE.mode='load';await slotPick(1)});r.loadFile2=await st();
console.log(JSON.stringify(r,null,1),errs);
const ok=r.file1.ch12&&!r.newFile2.ch12&&r.newFile2.hub===0&&r.newFile2.coins===0&&r.loadFile1.ch12&&r.loadFile1.coins===321&&r.loadFile1.hub===2&&!r.loadFile2.ch12&&r.loadFile2.coins===5;
console.log(ok?'PASS':'FAIL');await b.close();process.exit(ok?0:1)})();
