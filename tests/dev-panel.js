const path=require('path');const GAME='file://'+path.resolve(process.env.GAME||path.join(__dirname,'../src/meteorite-kids-battle.html'));const OUT=path.join(__dirname,'out');require('fs').mkdirSync(OUT,{recursive:true});
const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto(GAME.replace('-battle.html','-dev.html'));await p.waitForTimeout(1500);
await p.click('#devBtn');await p.waitForTimeout(400);
const r=await p.evaluate(()=>({open:!document.getElementById('devDlg').hidden,body:document.getElementById('devBody').innerText.length,story:typeof STORY!=='undefined'?STORY:'?'}));
console.log(JSON.stringify(r),errs);await b.close()})();
