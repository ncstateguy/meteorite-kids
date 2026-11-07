
// ================= Dev build: jump anywhere, tweak anything =================
const DEV={skipScenes:true,skipRewards:true,autoLevel:true,open:false};
// "Skip story scenes" only skips the opening and ending scenes that wrap battles. Scenes you pick on purpose
// (Prologue, Farewell, the interlude, previews, gallery) always play.
const AUTO_SCENES=new Set();Object.values(SCENES).forEach(v=>{if(v&&v.pre)AUTO_SCENES.add(v.pre);if(v&&v.post)AUTO_SCENES.add(v.post)});
const _playCutscene=playCutscene;playCutscene=async function(sc){if(DEV.skipScenes&&!DEV.force&&AUTO_SCENES.has(sc))return;DEV.force=false;return _playCutscene(sc)};
const _awardRewards=awardRewards;awardRewards=async function(B,first){if(DEV.skipRewards)return;return _awardRewards(B,first)};
isUnlocked=()=>true;heroUnlocked=()=>true;part1Done=()=>true;
function devStopAll(){DEV.token=(DEV.token||0)+1;if(CUT.active){CUT.skip=true;const w=CUT.wait;CUT.wait=null;if(w)w();CUT.active=false}TITLE.active=false;HUB.active=false;HUB.saving=false;HUB.choosing=false;HUB.talking=false;
  if(S&&!S.over){S.over=true}$('dlg').hidden=true;$('cap').hidden=true;$('skipBtn').hidden=true;$('tut').hidden=true}
function devBattle(c){devClose();devStopAll();if(DEV.autoLevel)devSetLevel(expectedLevel(c));setTimeout(()=>{HUB.fromHub=false;if(DEV.skipScenes)startBattle(c,true);else startBattle(c)},60)}
function devScene(sc,label){devClose();devStopAll();setTimeout(async()=>{const tk=DEV.token;DEV.force=true;await playCutscene(sc);if(tk===DEV.token)showChapters()},60)}
function devSetLevel(L){const p=P();HERO_IDS.forEach(id=>{p.party.lv[id]=Math.max(1,L);p.party.xp[id]=0});saveProgress()}
function devGear(t){const g=G();HERO_IDS.forEach(id=>{g.gear[id].w=t;g.gear[id].o=t});saveProgress()}
function devCharms(){const g=G();g.charms=Object.keys(CHARMS);const order=['spark','cool','ward','lantern','echo'];HERO_IDS.forEach((id,i)=>g.gear[id].c=order[i]);saveProgress()}
function devClose(){$('devDlg').hidden=true;DEV.open=false}
function devOpen(){DEV.open=true;renderDev();$('devDlg').hidden=false}
function devMsg(t){const m=$('devMsg');if(m)m.textContent=t}
function renderDev(){
  const p=G(),lv=p.party.lv.lightheart,inBattle=!$('battleUI').hidden&&S&&!S.over;
  const battles=[['Dream (tutorial)',DREAM],...CHAPTERS.slice().sort((a,b)=>a.num-b.num).map(c=>[`Ch. ${c.num} · ${c.title}`,c])];
  const scenes=[['Prologue',SCENES.opening],['Dream: opening',SCENES.dream.pre],['Dream: ending',SCENES.dream.post],
    ...CHAPTERS.slice().sort((a,b)=>a.num-b.num).flatMap(c=>{const s=SCENES[c.key]||{};return [[`Ch. ${c.num} opening`,s.pre],[`Ch. ${c.num} ending`,s.post]].filter(x=>x[1])}),
    ['Ch. 12 · Farewell',SCENES.farewell],['Interlude · Earth Awakens',SCENES.interlude],['Part 2 opening',SCENES.part2],['Preview · Shard-Born',SCENES.shardborn],['Preview · Herald',SCENES.herald],['Preview · Vorath',SCENES.vorath],['Preview · Five Into One',SCENES.preview5],['Character Gallery',SCENES.gallery]].filter(x=>x[1]);
  const b=(id,label,extra)=>`<button id="${id}" ${extra||''}>${label}</button>`;
  $('devBody').innerHTML=`
   ${inBattle?`<h3>This battle</h3><div class="row">${b('dvWin','Win now','class="primary"')}${b('dvLose','Lose now')}${b('dvHeal','Heal team')}${b('dvMorph','Morph the active three')}${b('dvLow','Boss to 10% HP')}</div>`:''}
   <h3>Jump into a battle</h3><p class="tip">Starts the fight directly with your gear below. With "Match the story level" on, the party is set to the level the story expects for that chapter.</p><div class="row">${battles.map(([l],i)=>b('dvB'+i,l)).join('')}${b('dvPatrol','Ashling patrol')}</div>
   <h3>Watch a story scene</h3><div class="row">${scenes.map(([l],i)=>b('dvS'+i,l)).join('')}</div>
   <h3>Party</h3><p class="tip">Level ${lv} · Weapon and outfit tier ${p.gear.lightheart.w} · Coins ${p.coins}</p>
   <div class="row">${b('dvL-','Level −1')}${b('dvL+','Level +1')}${b('dvL5','Level 5')}${b('dvL10','Level 10')}${b('dvL15','Level 15')}${b('dvLpar','Story level')}</div>
   <div class="row">${[0,1,2,3].map(t=>b('dvG'+t,`Gear tier ${t}`)).join('')}${b('dvCh','All charms')}${b('dvCh0','No charms')}</div>
   <div class="row">${b('dvItems','Max items')}${b('dvCoins','+500 coins')}${b('dvMats','+10 of every material')}</div>
   <h3>World</h3><div class="row">${b('dvTown','Go to Hometown')}${[['kid','kids'],['teen','teens'],['adult','adults']].map(([a,l])=>b('dvE'+a,`Town era: ${l}`)).join('')}${b('dvTitle','Title screen')}${b('dvList','Chapter list')}${b('dvReveal',`Identities revealed: ${progress.reveal?'ON':'OFF'}`)}</div>
   <div class="row">${b('dvAll','Mark all chapters cleared')}${b('dvReset','Reset all progress')}</div>
   <h3>Options</h3><div class="row">${b('dvSkip',`Skip battle intro and ending scenes: ${DEV.skipScenes?'ON':'OFF'}`)}${b('dvRw',`Skip reward screens: ${DEV.skipRewards?'ON':'OFF'}`)}${b('dvAuto',`Match the story level on jump: ${DEV.autoLevel?'ON':'OFF'}`)}</div>
   <p class="tip" id="devMsg"></p>`;
  const on=(id,f)=>{const e=$(id);if(e)e.onclick=f};
  on('dvWin',()=>{devClose();if(S.base&&S.base.stages)S.stageIdx=S.base.stages.length-1;S.boss.hp=0;if(S.ch.phased||S.ch.final||S.base)S.finalDone=true;win()});
  on('dvLose',()=>{devClose();S.roster.forEach(k=>{k.hp=0;k.down=true});lose()});
  on('dvHeal',()=>{S.roster.forEach(k=>{k.down=false;k.hp=k.hpMax});renderStatus();devMsg('Team healed.')});
  on('dvMorph',()=>{activeAlive().forEach(k=>{if(!k.stoneless&&!k.seraph){k.powered=3;k.cd=0}});renderStatus();devMsg('The active three are morphed. Meteor Strike is ready.')});
  on('dvLow',()=>{S.boss.hp=Math.max(1,Math.round(S.boss.hpMax*.1));renderStatus();devMsg('Boss at 10% HP.')});
  battles.forEach(([l,c],i)=>on('dvB'+i,()=>devBattle(c)));
  on('dvPatrol',()=>{devClose();devStopAll();HUB.age='kid';enterHub();setTimeout(()=>startPatrol({z:PATROL_ZONES[0],x:0,y:0,dir:1},false),80)});
  scenes.forEach(([l,sc],i)=>on('dvS'+i,()=>devScene(sc,l)));
  on('dvL-',()=>{devSetLevel(lv-1);renderDev()});on('dvL+',()=>{devSetLevel(lv+1);renderDev()});
  [5,10,15].forEach(n=>on('dvL'+n,()=>{devSetLevel(n);renderDev()}));
  on('dvReveal',()=>{progress.reveal=!progress.reveal;saveProgress();renderDev();devMsg(progress.reveal?'The town now knows who the Meteorite Kids are (as after the Herald fight). Talk to people in the teen era.':'Identities are secret again.')});
  on('dvLpar',()=>{devSetLevel(storyLevel());renderDev();devMsg(`Set to the level the story expects right now (${storyLevel()}).`)});
  [0,1,2,3].forEach(t=>on('dvG'+t,()=>{devGear(t);renderDev()}));
  on('dvCh',()=>{devCharms();renderDev();devMsg('Charms: Jake Spark Plug, Joseph Cool Stone, Lindsey Shard Ward, Josh Lantern Charm, Tricia Red Hero\'s Ember.')});
  on('dvCh0',()=>{HERO_IDS.forEach(id=>G().gear[id].c=null);saveProgress();renderDev()});
  on('dvItems',()=>{Object.keys(ITEMS).forEach(k=>P().items[k]=ITEM_CAP);saveProgress();devMsg('Pockets full.')});
  on('dvCoins',()=>{P().coins+=500;saveProgress();renderDev()});
  on('dvMats',()=>{Object.values(MATS).forEach(([m])=>P().mats[m]=(P().mats[m]||0)+10);saveProgress();devMsg('Added 10 of every material.')});
  on('dvTown',()=>{devClose();devStopAll();enterHub()});
  [['kid'],['teen'],['adult']].forEach(([a])=>on('dvE'+a,()=>{devClose();devStopAll();HUB.age=a;enterHub();buildObjs();buildPatrols();const bt=$('hubEra');const er=ERAS.find(e=>e[0]===a);if(bt&&er)bt.textContent=`Era: ${er[1]}`}));
  on('dvTitle',()=>{devClose();location.reload()});
  on('dvList',()=>{devClose();devStopAll();showChapters()});
  on('dvAll',()=>{storyOrder().forEach(k=>progress[k]=true);progress.opening=true;progress.interlude=true;saveProgress();devMsg('Every chapter is marked cleared.')});
  on('dvReset',()=>{if(DEV.confirmReset){for(const k in progress)delete progress[k];Object.keys(HUB.state).forEach(k=>delete HUB.state[k]);saveProgress();saveHub();DEV.confirmReset=false;renderDev();devMsg('Progress reset.')}else{DEV.confirmReset=true;devMsg('Press Reset again to confirm.')}});
  on('dvSkip',()=>{DEV.skipScenes=!DEV.skipScenes;renderDev()});
  on('dvRw',()=>{DEV.skipRewards=!DEV.skipRewards;renderDev()});
  on('dvAuto',()=>{DEV.autoLevel=!DEV.autoLevel;renderDev()});
}
$('devBtn').onclick=()=>DEV.open?devClose():devOpen();$('devX').onclick=devClose;
document.addEventListener('keydown',e=>{if(e.key==='`'){e.preventDefault();e.stopImmediatePropagation();DEV.open?devClose():devOpen()}else if(DEV.open){if(e.key==='Escape'){e.preventDefault();devClose()}e.stopImmediatePropagation()}},true);
