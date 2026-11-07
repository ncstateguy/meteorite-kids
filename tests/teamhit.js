const path=require('path');const GAME='file://'+path.resolve(process.env.GAME||path.join(__dirname,'../src/meteorite-kids-battle.html'));
// Checks the team-wide hit rules: healthy heroes hold on at 1 HP, hurt ones can go down, Ch 7 is exempt, a shield halves Crown Barrage.
const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.route('**/fonts.googleapis.com/**',r=>r.abort());await p.goto(GAME);await p.waitForTimeout(800);
const r=await p.evaluate(async()=>{window.playCutscene=async()=>{};TITLE.active=false;HUB.active=false;const out={};
 const go=async key=>{startBattle(CHAPTERS.find(c=>c.key===key),true);await new Promise(r=>setTimeout(r,300))};
 await go('ch3');const [a,c]=S.roster;a.hp=Math.ceil(a.hpMax*.5);c.hp=Math.floor(c.hpMax*.3);
 teamHit(k=>damageKid(k,999));out.healthyHoldsOn=a.hp===1&&!a.down;out.hurtGoesDown=c.down;
 S.roster.forEach(k=>{k.down=false;k.hp=k.hpMax});damageKid(S.roster[0],999);out.singleHitStillKO=S.roster[0].down;
 S.over=true;await go('ch27');const B=S.boss;B.shards=5;B.cycle=1;S.roster.forEach(k=>{k.hp=k.hpMax;k.barrier=false;k.veil=false;k.guard=0});
 const run=async()=>{S.roster.forEach(k=>{k.hpMax=5000;k.hp=5000});B.shards=5;B.cycle=1;const h0=S.roster.map(k=>k.hp);await S.ch.turn(B);return S.roster.reduce((s,k,i)=>s+(h0[i]-k.hp),0)};
 const plain=await run();S.roster[1].barrier=true;const shielded=await run();
 out.barrage={plain,shielded};out.shieldHalves=shielded<plain*.62;return out});
console.log(JSON.stringify(r),errs);await b.close();process.exit(Object.values(r).every(v=>v!==false)?0:1)})();
