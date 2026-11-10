const path=require('path');const GAME='file://'+path.resolve(process.env.GAME||path.join(__dirname,'../src/meteorite-kids-battle.html'));
// No menu shows while the battle intro plays: from a town patrol, and from the chapter list. Samples every 50 ms.
const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1366,height:768}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.route('**/fonts.googleapis.com/**',r=>r.abort());await p.goto(GAME);await p.waitForTimeout(800);
const run=key=>p.evaluate(async key=>{ENC.off=false;window.playCutscene=async()=>{};const seen=[];const vis=id=>{const e=document.getElementById(id);return !!(e&&e.offsetParent!==null&&getComputedStyle(e).display!=='none')};
  const t=setInterval(()=>{const enc=$('encfx')&&$('encfx').style.display!=='none';if(enc||!$('battleUI').hidden===false)seen.push({enc,menu:vis('menu'),hud:vis('hubHud')})},50);
  if(key==='patrol'){['opening','dream','ch1','ch2'].forEach(k=>progress[k]=true);HUB.state.hero='lightheart';Object.keys(HERO_JOIN).forEach(id=>HUB.state['met_'+id]=true);HUB.firstMorning=false;TITLE.active=false;enterHub();await new Promise(r=>setTimeout(r,500));HUB.talking=false;$('dlg').hidden=true;
    HUB.active=false;await startBattle(CHAPTERS.find(c=>c.key==='ch2'),true)}
  else{showChapters();await new Promise(r=>setTimeout(r,300));const C=CHAPTERS.find(c=>c.key==='ch3');await startBattle(C,true)}
  clearInterval(t);const during=seen.filter(s=>s.enc);return {samples:during.length,menuShown:during.filter(s=>s.menu).length,hudShown:during.filter(s=>s.hud).length,battleUp:!$('battleUI').hidden}},key);
const a=await run('patrol');await p.evaluate(()=>{S.over=true});const c=await run('chapters');
console.log(JSON.stringify({fromTown:a,fromChapterList:c}),errs);
const ok=a.samples>3&&a.menuShown===0&&a.hudShown===0&&a.battleUp&&c.samples>3&&c.menuShown===0&&c.battleUp&&!errs.length;
console.log(ok?'PASS':'FAIL');await b.close();process.exit(ok?0:1)})();
