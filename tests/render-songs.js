const path=require('path');const GAME='file://'+path.resolve(process.env.GAME||path.join(__dirname,'../src/meteorite-kids-battle.html'));const OUT=path.join(__dirname,'out');require('fs').mkdirSync(OUT,{recursive:true});
const {chromium}=require('playwright');const fs=require('fs');(async()=>{const b=await chromium.launch();const p=await b.newPage();
await p.route('**/fonts.googleapis.com/**',r=>r.abort());
await p.goto(GAME);await p.waitForTimeout(600);
for(const [name,secs] of JSON.parse(process.argv[2])){
 const b64=await p.evaluate(async([name,secs])=>{const sr=44100,off=new OfflineAudioContext(1,sr*secs,sr);const saved={...AU};
  AU.ctx=off;AU.master=off.createGain();AU.master.gain.value=.8;AU.master.connect(off.destination);AU.music=off.createGain();AU.music.gain.value=.7;const mlp=off.createBiquadFilter();mlp.type='lowpass';mlp.frequency.value=2600;mlp.Q.value=.4;const msh=off.createBiquadFilter();msh.type='highshelf';msh.frequency.value=1800;msh.gain.value=-5;AU.music.connect(mlp);mlp.connect(msh);msh.connect(AU.master);AU.sfx=off.createGain();AU.sfx.connect(AU.master);
  const len=sr,buf=off.createBuffer(1,len,sr),d=buf.getChannelData(0);for(let i=0;i<len;i++)d[i]=Math.random()*2-1;AU.noise=buf;
  const S2={name,...SONGS[name]},sd=60/S2.bpm/4,total=S2.bars*16;let t=.05,st=0;
  while(t<secs-.5){const bar=Math.floor(st/16);S2.play(t,st,bar,S2.chords[bar],sd);S2.mel.forEach(([s,m,l])=>{if(s===st)tone(t,m,sd*l*.92,S2.lead)});st=(st+1)%total;t+=sd}
  const out=await off.startRendering();Object.assign(AU,saved);const ch=out.getChannelData(0);
  let peak=0,ss=0;for(const v of ch){peak=Math.max(peak,Math.abs(v));ss+=v*v}window.__lv=[peak.toFixed(3),Math.sqrt(ss/ch.length).toFixed(4)];const g=peak>0?.9/peak:1;
  const wav=new DataView(new ArrayBuffer(44+ch.length*2));const w=(o,str)=>{for(let i=0;i<str.length;i++)wav.setUint8(o+i,str.charCodeAt(i))};
  w(0,'RIFF');wav.setUint32(4,36+ch.length*2,true);w(8,'WAVE');w(12,'fmt ');wav.setUint32(16,16,true);wav.setUint16(20,1,true);wav.setUint16(22,1,true);wav.setUint32(24,sr,true);wav.setUint32(28,sr*2,true);wav.setUint16(32,2,true);wav.setUint16(34,16,true);w(36,'data');wav.setUint32(40,ch.length*2,true);
  for(let i=0;i<ch.length;i++)wav.setInt16(44+i*2,Math.max(-1,Math.min(1,ch[i]*g))*32767,true);
  let s='';const u=new Uint8Array(wav.buffer);for(let i=0;i<u.length;i+=32768)s+=String.fromCharCode.apply(null,u.subarray(i,i+32768));return btoa(s)},[name,secs]);
 fs.writeFileSync(path.join(OUT,`${name}.wav`),Buffer.from(b64,'base64'));console.log(name,await p.evaluate(()=>window.__lv))}
await b.close()})();
