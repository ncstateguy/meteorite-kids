const path=require('path');const GAME='file://'+path.resolve(process.env.GAME||path.join(__dirname,'../src/meteorite-kids-battle.html'));const OUT=path.join(__dirname,'out');require('fs').mkdirSync(OUT,{recursive:true});
const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1000,height:950}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.route('**/fonts.googleapis.com/**',r=>r.abort());await p.addInitScript("const _st=window.setTimeout;window.setTimeout=(f,ms)=>_st(f,Math.min(ms||0,5));");
await p.goto(GAME);await p.waitForTimeout(500);
const r=await p.evaluate(async()=>{TITLE.active=false;window.playCutscene=async()=>{};window.awardRewards=async()=>{};window.showResult=()=>{};
  window.chooseAction=k=>Promise.resolve(actionsFor(k).filter(a=>!a.disabled&&a.run&&a.label!=='Swap'&&a.label!=='Item')[0]);
  for(const key of ['ch1','ch2','ch2']){startBattle(CHAPTERS.find(c=>c.key===key),true);await sleep(300);S.roster[0].hp=Math.round(S.roster[0].hpMax/2);S.round=7;S.boss.hp=0;win();await sleep(50)}PLOG.d.sec=1260;
  // a loss
  startBattle(CHAPTERS.find(c=>c.key==='ch3'),true);await sleep(50);S.roster.forEach(k=>{k.hp=0;k.down=true});lose();
  startBattle(CHAPTERS.find(c=>c.key==='ch4'),true);await sleep(50);
  startBattle(CHAPTERS.find(c=>c.key==='ch3'),true);await sleep(50);
  return PLOG.text().split('\nDATA')[0]});
console.log(r);
await p.evaluate(()=>{showTitle&&showTitle()});await p.waitForTimeout(300);await p.evaluate(()=>PLOG.open());await p.waitForTimeout(300);await p.screenshot({path:path.join(OUT,'plog.png')});
console.log(errs);await b.close()})();
