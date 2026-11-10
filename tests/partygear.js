const path=require('path');const GAME='file://'+path.resolve(process.env.GAME||path.join(__dirname,'../src/meteorite-kids-battle.html'));const OUT=path.join(__dirname,'out');require('fs').mkdirSync(OUT,{recursive:true});
// Party screen gear slots: weapon/outfit open the forge for that hero and Back returns to Party; charm slot jumps to the charm list.
const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1000,height:1300}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.route('**/fonts.googleapis.com/**',r=>r.abort());await p.goto(GAME);await p.waitForTimeout(800);
const r=await p.evaluate(async()=>{const out={};['opening','dream','ch1','ch2','ch3','ch4','ch5'].forEach(k=>progress[k]=true);TITLE.active=false;
 openParty('scareth');out.slotsAreButtons=['pgW','pgO','pgC'].every(id=>document.getElementById(id)&&document.getElementById(id).tagName==='BUTTON'&&!document.getElementById(id).disabled);
 document.getElementById('pgW').click();out.forgeOpen=!!document.getElementById('forgeBack');out.forgeFor=FORGE_WHO;out.backLabel=document.getElementById('forgeBack').textContent;
 document.getElementById('forgeBack').click();out.backToParty=!!document.getElementById('partyBack')&&document.querySelector('#pw-scareth.primary')!==null;
 G().charms=['ring'];openParty('scareth');document.getElementById('pgC').click();out.charmFocus=document.activeElement&&document.activeElement.id;
 // before Josh joins, the forge slots are off
 delete progress.ch4;openParty('lightheart');out.preJoshDisabled=document.getElementById('pgW').disabled;
 // from town (not Party), forge Back still goes to town
 progress.ch4=true;FORGE_RET=null;openForge('lightheart');out.townBackLabel=document.getElementById('forgeBack').textContent;return out});
await p.evaluate(()=>openParty('scareth'));await p.screenshot({path:path.join(OUT,'partygear.png'),fullPage:true});
console.log(JSON.stringify(r,null,1),errs);
const ok=r.slotsAreButtons&&r.forgeOpen&&r.forgeFor==='scareth'&&r.backLabel==='Back to Party'&&r.backToParty&&r.charmFocus==='pc-ring'&&r.preJoshDisabled&&r.townBackLabel==='Back'&&!errs.length;
console.log(ok?'PASS':'FAIL');await b.close();process.exit(ok?0:1)})();
