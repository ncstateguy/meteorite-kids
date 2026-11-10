const path=require('path');const GAME='file://'+path.resolve(process.env.GAME||path.join(__dirname,'../src/meteorite-kids-battle.html'));const OUT=path.join(__dirname,'out','layout');require('fs').mkdirSync(OUT,{recursive:true});
// Layout check: picture size, no page scroll on landscape screens, panels where they belong. Saves screenshots per screen size.
const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const errs=[];const report=[];
const sizes=(process.argv[2]||'1366x768,1920x1080,844x390,390x844').split(',').map(s=>s.split('x').map(Number));
for(const [w,h] of sizes){const p=await b.newPage({viewport:{width:w,height:h}});p.on('pageerror',e=>errs.push(`${w}x${h} ${e.message}`));
 await p.route('**/fonts.googleapis.com/**',r=>r.abort());await p.goto(GAME);await p.waitForTimeout(800);
 const m=()=>p.evaluate(()=>{const c=document.getElementById('cv').getBoundingClientRect();return {cw:Math.round(c.width),ch:Math.round(c.height),pageH:document.documentElement.scrollHeight,vh:innerHeight,pageW:document.documentElement.scrollWidth,vw:innerWidth,body:document.body.className}});
 const shot=async n=>{await p.waitForTimeout(350);await p.screenshot({path:path.join(OUT,`${w}x${h}_${n}.png`)});const r=await m();report.push(`${w}x${h} ${n}: picture ${r.cw}x${r.ch} (${Math.round(100*r.cw*r.ch/(r.vw*r.vh))}% of screen) page ${r.pageW}x${r.pageH} [${r.body}]`)};
 await p.evaluate(()=>{TITLE.pressed=true;titlePress(true)});await shot('title');
 await p.evaluate(async()=>{['opening','dream','ch1','ch2','ch3','ch4','ch5','ch6','ch7','ch8','ch9','ch10','ch11','ch12','interlude','part2'].forEach(k=>progress[k]=true);HUB.state.hero='lightheart';Object.keys(HERO_JOIN).forEach(id=>HUB.state['met_'+id]=true);HUB.firstMorning=false;TITLE.active=false;enterHub();await new Promise(r=>setTimeout(r,700));for(let i=0;i<10&&HUB.talking;i++){hubAdvance();await new Promise(r=>setTimeout(r,120))}});
 await shot('town');
 await p.evaluate(()=>{navMode='key';openHubMenu()});await shot('town_menu');
 await p.evaluate(()=>{openParty()});await shot('party');
 await p.evaluate(()=>{HUB.saving=false;enterHub();openSettings()});await shot('settings');
 await p.evaluate(async()=>{$('setDlg').hidden=true;window.playCutscene=async()=>{};HUB.active=false;startBattle(CHAPTERS.find(c=>c.key==='ch5'),true);await new Promise(r=>setTimeout(r,600))});await shot('battle');
 await p.evaluate(async()=>{S.roster.forEach(k=>{k.hp=0;k.down=true});lose();await new Promise(r=>setTimeout(r,1300))});await shot('defeat');
 await p.close()}
console.log(report.join('\n'));console.log(errs);await b.close()})();
