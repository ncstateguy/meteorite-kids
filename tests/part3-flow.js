const path=require('path');const GAME='file://'+path.resolve(process.env.GAME||path.join(__dirname,'../src/meteorite-kids-battle.html'));const OUT=path.join(__dirname,'out');require('fs').mkdirSync(OUT,{recursive:true});
const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1000,height:950}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.route('**/fonts.googleapis.com/**',r=>r.abort());await p.goto(GAME);await p.waitForTimeout(600);
const r=await p.evaluate(async()=>{TITLE.active=false;const out=[];
  const iv=setInterval(()=>{if(CUT.active){try{cutAdvance()}catch(e){}}if(HUB.talking&&(HUB.wait||HUB.typing))hubAdvance();if(HUB.choice)HUB.choice.res(0)},40);
  for(const sc of [SCENES.ch22open,SCENES.ch22.pre,SCENES.ch22.post,SCENES.ch23.pre,SCENES.ch23.post,SCENES.ch27.post,SCENES.ch25open,SCENES.ch25r.pre,SCENES.ch25r.post,SCENES.finale]){try{await Promise.race([playCutscene(sc),sleep(90000)]);out.push(sc.label+' ok')}catch(e){out.push(sc.label+' ERR '+e.message)}}
  ['opening','dream','ch1','ch2','ch3','ch4','ch5','ch6','ch7','ch8','ch9','ch10','ch11','ch12','interlude','part2','ch13','ch14','ch15','ch16','ch17','ch18a','ch18','whatsLeft','reveal','part3','ch19','ch20','ch21'].forEach(k=>progress[k]=true);HUB.state.clue=true;
  HUB.state.hero='lightheart';HUB.age='adult';HUB.map=townMap();enterHub();await sleep(400);out.push('goal: '+(nextGoal()||{}).text);
  const _e=exitHubTo;window.exitHubTo=(c)=>{window.__exit=c.key};
  const crater=OBJS.find(o=>o.type==='sign'&&o.ch==='ch7');await Promise.race([hubInteract(crater),sleep(20000)]);out.push('crater early ok');
  const s10=OBJS.find(o=>o.type==='sign'&&o.ch==='ch10');out.push('ch10 sign at '+s10.tx+','+s10.ty);
  await Promise.race([hubInteract(s10),sleep(30000)]);await sleep(600);out.push('area '+HUB.area+' goal: '+(nextGoal()||{}).text);
  // visit each site
  for(const [room,who] of [['rr_canyon','scareth'],['rr_temple','kaytahn'],['rr_forge','thornforge'],['rr_grove','nightshade'],['rr_peak','lightheart']]){
    HUB.area=room;enterArea();await sleep(300);const rel=OBJS.find(o=>o.type==='relic');HUB.leader=(who==='lightheart'?'scareth':'lightheart');
    await Promise.race([areaInteract(rel),sleep(20000)]);out.push(room+' wrong-lead done='+!!HUB.state[rel.id]);
    HUB.leader=who;await Promise.race([areaInteract(rel),sleep(30000)]);out.push(room+' done='+!!HUB.state[rel.id]+' mv='+!!progress['mv_'+who]);}
  HUB.area='rr_hub';enterArea();await sleep(300);out.push('after4 check: rr_all '+HUB.state.rr_all+' goal: '+(nextGoal()||{}).text);
  progress.ch22=true;HUB.area=null;HUB.map=townMap();enterHub();await sleep(300);out.push('goal: '+(nextGoal()||{}).text);
  window.__exit=null;await hubInteract(OBJS.find(o=>o.type==='sign'&&o.ch==='ch7'));out.push('crater -> '+window.__exit);
  progress.ch23=true;out.push('goal: '+(nextGoal()||{}).text);window.__exit=null;await Promise.race([hubInteract(OBJS.find(o=>o.type==='sign'&&o.ch==='ch7')),sleep(8000)]);out.push('crater -> '+window.__exit);
  window.exitHubTo=_e;progress.ch27=true;
  await Promise.race([startEpilogue(),sleep(60000)]);await sleep(500);out.push('ep area '+HUB.area+' age '+HUB.age+' goal: '+(nextGoal()||{}).text);
  out.push('objs '+OBJS.filter(o=>o.id==='arch'||o.id==='gale25').map(o=>o.id).join(','));
  for(const id of ['reed','corran','kylee','jared']){const o=OBJS.find(o=>o.id===id);if(!o){out.push('missing '+id);continue}await Promise.race([hubInteract(o),sleep(20000)])}
  window.__exit=null;window.exitHubTo=(c)=>{window.__exit=c.key};await Promise.race([hubInteract(OBJS.find(o=>o.id==='gale25')),sleep(20000)]);out.push('gale -> '+window.__exit);
  await Promise.race([playCutscene(SCENES.ch25r.pre),sleep(60000)]);await Promise.race([playCutscene(SCENES.ch25r.post),sleep(60000)]);CH25R.after();await sleep(400);out.push('cer '+HUB.state.ep_cer+' goal: '+(nextGoal()||{}).text);
  await Promise.race([hubInteract(OBJS.find(o=>o.type==='sign'&&o.ch==='ch7')),sleep(120000)]);await sleep(800);out.push('ch25 '+progress.ch25+' goal: '+(nextGoal()||{}).text);
  clearInterval(iv);return out});
console.log(r.join('\n'));await p.screenshot({path:path.join(OUT,'p3d.png')});console.log(errs);await b.close()})();
