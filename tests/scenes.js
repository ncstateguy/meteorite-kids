const path=require('path');const GAME='file://'+path.resolve(process.env.GAME||path.join(__dirname,'../src/meteorite-kids-battle.html'));const OUT=path.join(__dirname,'out');require('fs').mkdirSync(OUT,{recursive:true});
const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1000,height:950}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.route('**/fonts.googleapis.com/**',r=>r.abort());await p.goto(GAME);await p.waitForTimeout(600);
const r=await p.evaluate(async()=>{TITLE.active=false;const out=[];const iv=setInterval(()=>{if(CUT.active){try{cutAdvance()}catch(e){}}},40);
 for(const sc of [SCENES.ch21.pre,SCENES.ch21.post,SCENES.ch22open,SCENES.ch22.pre,SCENES.ch22.post,SCENES.ch23.pre,SCENES.ch23.post,SCENES.ch27.pre,SCENES.ch27.p2,SCENES.ch27.p3,SCENES.ch27.post,SCENES.preview5,SCENES.gallery]){try{await Promise.race([playCutscene(sc),sleep(90000)]);out.push(sc.label+' ok')}catch(e){out.push(sc.label+' ERR '+e.message)}}
 clearInterval(iv);return out});
console.log(r.join('\n'));
// screenshot the transformation moment
await p.evaluate(()=>{const iv=setInterval(()=>{if(CUT.active&&!CUT.typing)try{cutAdvance()}catch(e){}},900);window.__iv=iv;playCutscene(SCENES.ch27.pre)});
for(let i=0;i<40;i++){await p.waitForTimeout(500);const done=await p.evaluate(()=>Object.values(CUT.actors||{}).some(a=>a.form==='final'));if(done)break}
await p.waitForTimeout(2500);await p.screenshot({path:'ll_scene.png'});
console.log(errs);await b.close()})();
