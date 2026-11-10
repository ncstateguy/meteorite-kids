const path=require('path');const GAME='file://'+path.resolve(process.env.GAME||path.join(__dirname,'../src/meteorite-kids-battle.html'));const OUT=path.join(__dirname,'out');require('fs').mkdirSync(OUT,{recursive:true});
// Simulated Xbox-layout controller: Start opens the town menu, D-pad/A/B work in it and in every pop-up window.
const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1000,height:1100}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.addInitScript(()=>{const pad={index:0,connected:true,id:'Test pad',axes:[0,0,0,0],buttons:Array.from({length:17},()=>({pressed:false,value:0}))};window.__pad=pad;navigator.getGamepads=()=>[pad]});
await p.route('**/fonts.googleapis.com/**',r=>r.abort());await p.goto(GAME);await p.waitForTimeout(900);
const B={A:0,B:1,X:2,Y:3,LB:4,RB:5,Select:8,Start:9,Up:12,Down:13,Left:14,Right:15};
const press=async n=>{await p.evaluate(i=>{__pad.buttons[i].pressed=true},B[n]);await p.waitForTimeout(90);await p.evaluate(i=>{__pad.buttons[i].pressed=false},B[n]);await p.waitForTimeout(160)};
const st=()=>p.evaluate(()=>({menu:!!HUB.menuNav,focus:(document.activeElement&&(document.activeElement.id||(document.activeElement.tagName==='BUTTON'?document.activeElement.textContent.slice(0,20):'')))||null,saving:!!HUB.saving,modal:(openModal()||{}).id||null,choosing:!!HUB.choosing}));
const r={};const clear=async()=>{for(let i=0;i<15&&await p.evaluate(()=>!!(HUB.talking||CUT.active));i++)await press('A')};
// into town (story mode, after Part 1 so every button shows)
await p.evaluate(()=>{['opening','dream','ch1','ch2','ch3','ch4','ch5','ch6','ch7','ch8','ch9','ch10','ch11','ch12','interlude','part2'].forEach(k=>progress[k]=true);HUB.state.hero='lightheart';TITLE.active=false;enterHub()});await p.waitForTimeout(500);
await p.waitForTimeout(900);await clear();r.pre=await p.evaluate(()=>({talking:!!HUB.talking,cut:!!CUT.active,choosing:!!HUB.choosing,choice:!!HUB.choice,active:HUB.active,saving:!!HUB.saving,padActive:PAD.active}));await press('Start');r.open=await st();
await press('Right');r.moved=await st();
await press('B');r.closed=await st();
await press('Start');await p.evaluate(()=>setFocus($('hubParty'),true));await press('A');r.party=await st();
await press('B');await p.waitForTimeout(300);r.backFromParty=await st();
await press('Start');await p.evaluate(()=>setFocus($('hubDiff'),true));await press('A');await p.waitForTimeout(200);r.diff=await st();
await press('Down');r.diffFocus=await st();await press('B');r.diffClosed=await st();
await press('Start');await p.evaluate(()=>setFocus($('hubSwitch'),true));await press('A');r.heroPick=await st();
await p.screenshot({path:path.join(OUT,'controller.png')});
await press('B');
await press('Select');r.exitOpen=await p.evaluate(()=>EXIT.open);await press('B');r.exitClosed=!(await p.evaluate(()=>EXIT.open));
console.log(JSON.stringify(r,null,1),errs);
const ok=r.open.menu&&r.open.focus==='hubSwitch'&&r.moved.focus&&r.moved.focus!=='hubSwitch'&&!r.closed.menu&&r.party.saving&&!r.party.menu&&!r.backFromParty.saving&&r.diff.modal==='diffDlg'&&/^$|.*/.test(r.diffFocus.focus||'')&&r.diffFocus.modal==='diffDlg'&&!r.diffClosed.modal&&r.heroPick.choosing&&r.exitOpen&&r.exitClosed&&!errs.length;
console.log(ok?'PASS':'FAIL');await b.close();process.exit(ok?0:1)})();
