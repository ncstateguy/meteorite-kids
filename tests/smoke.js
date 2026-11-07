const path=require('path');const GAME='file://'+path.resolve(process.env.GAME||path.join(__dirname,'../src/meteorite-kids-battle.html'));const OUT=path.join(__dirname,'out');require('fs').mkdirSync(OUT,{recursive:true});
const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1000,height:950}});const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error')errs.push('console: '+m.text())});
await p.route('**/fonts.googleapis.com/**',r=>r.abort());const t0=Date.now();await p.goto(GAME);await p.waitForTimeout(800);const load=Date.now()-t0;
const r=await p.evaluate(async()=>{TITLE.active=false;const out={};const L=[];
 const sc=[];Object.entries(SCENES).forEach(([k,v])=>{if(v.steps)sc.push(v);else Object.values(v).forEach(x=>x&&x.steps&&sc.push(x))});
 let says=0,caps=0;sc.forEach(s=>s.steps.forEach(st=>{if(st.say)says++;if(st.cap)caps++}));out.scenes=sc.length;out.says=says;out.caps=caps;
 out.chapters=CHAPTERS.map(c=>c.key).join(',');out.areas=Object.keys(AREAS).length;out.dungeons=Object.keys(DUNGEONS).length;out.banter=BANTER.length;out.pages=Object.keys(PAGES).length;
 out.foes=Object.keys(FOES).length;out.songs=Object.keys(SONGS).length;
 // area entry smoke
 const bad=[];for(const a of Object.keys(AREAS)){try{HUB.area=a;HUB.age=AREAS[a].age||'kid';enterArea();await sleep(10);if(AREAS[a].goal)AREAS[a].goal()}catch(e){bad.push(a+': '+e.message)}}out.areaErrors=bad;
 HUB.area=null;
 // battle start smoke
 const bb=[];for(const c of CHAPTERS){try{startBattle(c,true);await sleep(400);if(!S||!S.slots)bb.push(c.key);S.over=true}catch(e){bb.push(c.key+': '+e.message)}}out.battleErrors=bb;
 out.saveSlots=typeof SAVE!=='undefined'?SAVE.slots.length:'?';
 return out});
console.log('load ms',load);console.log(JSON.stringify(r,null,1));console.log('errors',errs.slice(0,10));await b.close()})();
