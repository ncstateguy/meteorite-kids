const path=require('path');const GAME='file://'+path.resolve(process.env.GAME||path.join(__dirname,'../src/meteorite-kids-battle.html'));const OUT=path.join(__dirname,'out');require('fs').mkdirSync(OUT,{recursive:true});
// Lose a few fights on purpose and check the defeat screen shows the short retry tip.
const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1000,height:900}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.route('**/fonts.googleapis.com/**',r=>r.abort());await p.goto(GAME);await p.waitForTimeout(800);
const keys=(process.argv[2]||'ch1,ch5,ch16,ch18,ch27').split(',');
for(const key of keys){const r=await p.evaluate(async key=>{window.playCutscene=async()=>{};TITLE.active=false;HUB.active=false;
  const C=CHAPTERS.find(c=>c.key===key);startBattle(C,true);await new Promise(r=>setTimeout(r,300));if(key==='ch18'||key==='ch27')S.boss.phase=2;
  S.roster.forEach(k=>{k.hp=0;k.down=true});lose();await new Promise(r=>setTimeout(r,1300));
  const m=document.getElementById('menu');return {tip:(m.querySelector('p.tip strong')||{}).parentNode?.innerText,details:!!m.querySelector('details')}},key);
  console.log(key,JSON.stringify(r))}
await p.screenshot({path:path.join(OUT,'defeat.png')});console.log(errs);await b.close()})();
