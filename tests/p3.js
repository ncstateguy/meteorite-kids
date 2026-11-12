const path=require('path');const GAME='file://'+path.resolve(process.env.GAME||path.join(__dirname,'../src/meteorite-kids-battle.html'));const OUT=path.join(__dirname,'out');require('fs').mkdirSync(OUT,{recursive:true});
// P3s: long boss name fits the card, Combo! appears only on set-up hits, online gives a message when the service never answers.
const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1366,height:768}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.route('**/fonts.googleapis.com/**',r=>r.abort());await p.goto(GAME);await p.waitForTimeout(800);
const r=await p.evaluate(async()=>{window.playCutscene=async()=>{};TITLE.active=false;HUB.active=false;const out={};const L=[];const _l=log;window.log=m=>{L.push(String(m));_l(m)};
 startBattle(CHAPTERS.find(c=>c.key==='ch23'),true);await new Promise(r=>setTimeout(r,500));
 const bn=document.querySelector('#status .card .bossnm');out.longName=bn&&bn.textContent;out.nameFits=bn&&bn.scrollWidth<=bn.clientWidth+1&&getComputedStyle(bn).whiteSpace==='normal';out.nm={sw:bn.scrollWidth,cw:bn.clientWidth,ws:getComputedStyle(bn).whiteSpace,fs:getComputedStyle(bn).fontSize};
 S.over=true;startBattle(CHAPTERS.find(c=>c.key==='ch3'),true);await new Promise(r=>setTimeout(r,400));
 const k=S.roster.find(x=>x.id!=='nightshade');S.boss.hex=0;S.boss.vuln=1;k.temper=false;L.length=0;await hitBoss(k,5,{});out.plainCombo=L.some(x=>/Combo!/.test(x));
 S.boss.hp=9999;S.boss.hex=2;L.length=0;progress.comboTips=0;await hitBoss(k,5,{});out.hexCombo=L.find(x=>/Combo!/.test(x))||null;out.cap=!$('cap').hidden&&$('cap').textContent;out.tips=progress.comboTips;
 out.tip3=CHAPTERS.find(c=>c.key==='ch3').tip.slice(0,30);
 return out});
// online: the service never answers
const net=await p.evaluate(async()=>{S.over=true;NET.libs=async()=>{};window.Peer=function(){this.on=()=>{};this.destroy=()=>{};this.connect=()=>({on(){}})};
 NET.open&&NET.open();$('netDlg').hidden=false;NET.render&&NET.render();
 const real=window.setTimeout;window.setTimeout=(f,ms,...a)=>real(f,ms>=12000?50:ms,...a);
 await NET.startHost();await new Promise(r=>real(r,300));const host=$('netStatus')&&$('netStatus').textContent;
 NET.host=false;NET.peer=null;$('netCode').value='ABCDE';await NET.join();await new Promise(r=>real(r,300));const join=$('netStatus')&&$('netStatus').textContent;
 window.setTimeout=real;return {host,join}});
console.log(JSON.stringify({...r,net},null,1),errs);
const ok=r.nameFits&&!r.plainCombo&&r.hexCombo&&/hex/.test(r.hexCombo)&&r.cap&&r.tips===1&&/Feeding Frenzy/.test(r.tip3)&&/online service/.test(net.host||'')&&/ABCDE/.test(net.join||'')&&!errs.length;
console.log(ok?'PASS':'FAIL');await b.close();process.exit(ok?0:1)})();
