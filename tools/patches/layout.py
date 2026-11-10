"""Screen layout (playtest: menus take more room than the game).

Landscape screens (laptop, TV, tablet, phone sideways):
- The game picture fills the window: the largest 16:9 that fits under a slim header.
- Header is one thin bar: title, chapter, Settings, Fullscreen, Exit. Sound, volume, difficulty,
  autosave, online, manual, text size, guide arrow and banter live in a Settings window.
- Town and dungeons: the map is the whole picture. Goal, hero and coins sit in a small HUD on the map.
  The menu opens over the map (Start, Esc or the Menu button) and closes with B, Esc or Close menu.
- Battles: the turn order runs across the top of the picture; hero cards and actions sit in a side panel;
  the battle log shows its latest line and opens on a click.
Portrait phones keep the stacked layout (menus below the picture), since the picture is too small to cover.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from patch import Patch
p = Patch(); rep = p.rep

# ---------------- CSS ----------------
CSS = r"""
/* ---- layout: picture fills the window ---- */
body{padding-block:8px}
.wrap{max-width:none;gap:8px}
header{flex-wrap:nowrap;align-items:center;gap:10px}
header h1{font-size:16px;white-space:nowrap}
header .hud{flex-wrap:nowrap;gap:6px;justify-content:flex-end}
header .chapter{white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:34vw}
#stageRow{display:flex;flex-direction:column;align-items:center;gap:10px;width:100%}
body.wide.in-battle #stageRow{flex-direction:row;align-items:flex-start;justify-content:center}
.screen{width:var(--sw,100%);max-width:100%;flex:0 0 auto}
@media (orientation:landscape) and (max-height:520px){.screen{max-width:100%}}
#battleUI{width:100%}
body.wide.in-battle #battleUI{flex:0 0 auto;overflow-y:auto;overflow-x:hidden;scrollbar-width:thin}
body.wide.in-battle #battleUI .deck{grid-template-columns:1fr}
body.wide.in-battle #battleUI .status{grid-template-columns:repeat(2,minmax(0,1fr))}
/* turn order across the top of the picture */
.screen .tq-row{position:absolute;top:5px;left:6px;right:6px;margin:0;z-index:6;padding:3px 4px;background:rgba(8,6,20,.62);border-radius:4px}
body:not(.in-battle) .screen .tq-row,body.cut .screen .tq-row{display:none}
/* battle log: latest line, click to open */
.log{cursor:pointer;position:relative}
.log:not(.open){max-height:none!important;overflow:hidden}
.log:not(.open) div{display:none}
.log:not(.open) div:last-child{display:block}
.log::after{content:'\25BE  Log';position:absolute;right:8px;top:6px;font-size:11px;color:var(--muted)}
.log.open::after{content:'\25B4  Close'}
.log.open{max-height:220px;overflow-y:auto}
/* menu as a window over the picture (landscape) */
body.wide .screen #menu{position:absolute;left:50%;bottom:2.5%;transform:translateX(-50%);width:min(94%,820px);max-height:92%;overflow-y:auto;z-index:8;background:rgba(22,18,42,.96);box-shadow:0 6px 30px rgba(0,0,0,.6)}
body.wide.hubwalk .screen #menu,body.cut .screen #menu{display:none}
/* town HUD and on-map buttons */
#hubHud{display:none;font-size:calc(12px*var(--ts));line-height:1.35;color:#e8ecff}
#hubHud p{margin:0}
#hubHud .goal{margin:0 0 2px;padding:2px 6px;border-left:3px solid var(--accent);background:rgba(0,0,0,.25)}
#hubHud #hubLeader,#hubHud #hubShards{color:#c9c4e6}
#hubHud #hubPrompt{color:#ffe9a8;font-weight:700}
#hubHud #hubPrompt:empty{display:none}
body.inhub #hubHud{display:block}
body.wide .screen #hubHud{position:absolute;top:6px;right:6px;max-width:44%;z-index:5;background:rgba(8,6,20,.72);padding:6px 8px;border-radius:4px;pointer-events:none}
body:not(.wide) #hubHud{width:100%;padding:6px 2px}
#mapBtns{display:none;position:absolute;right:6px;bottom:6px;z-index:5;gap:6px}
body.wide.hubwalk:not(.talking) #mapBtns{display:flex}
#mapBtns button{padding:4px 12px;background:rgba(8,6,20,.8)}
@media (pointer:fine){#mapBtns #hubTalk{display:none}}
/* settings window */
#setBody{display:flex;flex-direction:column;gap:10px}
#setBody .row{display:flex;flex-wrap:wrap;gap:6px;align-items:center}
#setBody .vol{display:flex;align-items:center;gap:6px}
/* phone held upright */
#rotHint{display:none;background:var(--panel2);border:1px solid var(--accent);padding:6px 10px;font-size:13px;align-items:center;justify-content:space-between;gap:8px}
@media (orientation:portrait) and (max-width:700px){#rotHint:not([hidden]){display:flex}}
"""
rep("</style>", CSS + "</style>", n=1) if p.s.count("</style>") == 1 else None
if p.s.count(CSS) != 1:
    i = p.s.find("</style>"); p.s = p.s[:i] + CSS + p.s[i:]

# ---------------- town and dungeon menus: info moves to the HUD, options move to Settings ----------------
HUD = """$('hubHud').innerHTML='<p class="goal" id="hubGoal" hidden></p><p id="hubLeader"></p><p id="hubShards"></p><p id="hubPrompt"></p>';"""
rep("""  $('menu').innerHTML=`<h2>Hometown</h2><p class="goal" id="hubGoal" hidden></p><p class="tip" id="hubLeader"></p><p class="tip" id="hubShards"></p><p id="hubPrompt">Walk around town. Look for people to help and places to visit.</p>
   <div class="row"><button id="hubTalk">Talk / use</button><button id="hubSwitch">Change hero</button>${eraOK?'<button id="hubEra">Era: kids</button>':''}<button id="hubParty">Party</button>${STORY?(part1Done()?'<button id="hubChapters">Extras</button>':''):'<button id="hubChapters">Chapters</button>'}</div>""",
    "  " + HUD + """$('menu').innerHTML=`<h2>Hometown</h2>
   <div class="row"><button id="hubSwitch">Change hero</button>${eraOK?'<button id="hubEra">Era: kids</button>':''}<button id="hubParty">Party</button>${STORY?(part1Done()?'<button id="hubChapters">Extras</button>':''):'<button id="hubChapters">Chapters</button>'}<button id="hubSave">Save</button></div>""")
rep("""$('menu').innerHTML=`<h2>${A.name}</h2><p class="goal" id="hubGoal" hidden></p><p class="tip" id="hubLeader"></p><p class="tip" id="hubShards"></p><p id="hubPrompt">Explore. Each kid's field power solves a different kind of puzzle.</p>
   <div class="row"><button id="hubTalk">Talk / use</button><button id="hubSwitch">Change hero</button><button id="hubParty">Party</button></div>""",
    HUD + """$('menu').innerHTML=`<h2>${A.name}</h2>
   <div class="row"><button id="hubSwitch">Change hero</button><button id="hubParty">Party</button><button id="hubSave">Save</button></div>""")
# both menus: one row of system buttons, replacing the options rows and the long controls text
rep("""   <div class="row" style="margin-top:6px"><button class="guideBtn" id="hubGuide">Guide arrow: ${GUIDE?'On':'Off'}</button><button class="banterBtn" id="hubBanter">Banter: ${BANTER_ON?'On':'Off'}</button><button class="textBtn" id="hubText">Text size: ${TEXT_SIZES[TEXT_SIZE][1]}</button><button id="hubSave">Save</button></div>
   <div class="row" style="margin-top:6px"><button id="hubDiff">Difficulty</button><button id="hubManual">Manual</button><button id="hubExit">Exit game</button></div>""",
    """   <div class="row" style="margin-top:6px"><button id="hubSettings">Settings</button><button id="hubExit">Exit game</button><button id="hubClose">Close menu</button></div>
   <p class="tip">Talk or use: A, Enter or Space. Change hero: X/Y, Tab or Q. Menu: Start or Esc. The Manual (in Settings) has the rest.</p>""", n=2)
rep("""   <p class="controls">Move with the arrow keys or WASD, the D-pad or left stick, or tap where you want to go. Talk or use: Enter, Space, or A. Change hero: Tab, Q, or X/Y.${STORY?' Follow the yellow arrow to find where the story goes next.':''}${eraOK?' Change era (kids, teens, or adults): R or the bumpers.':''} Party: levels, items, and coins. Save: the Save button or the glowing meteor crystal by the fountain. Ashling patrols roam the edges of town: walk into one to fight, or sneak up from behind for an ambush. ${STORY?(part1Done()?'Extras: Esc.':'Exit: Esc.'):'Chapter list: Esc.'} Controller: Start opens this menu, Select exits. Each kid's human power solves a different problem around town.</p>`;""", "`;")
rep("""   <p class="controls">Move with the arrow keys or WASD, the D-pad or left stick, or tap where you want to go. Talk or use a field power: Enter, Space, or A. Change hero: Tab, Q, or X/Y. Controller: Start opens this menu, Select exits. Walk into enemies to fight them, or sneak up from behind for an ambush. Doorways lead to the next room. Save at a meteor crystal.</p>`;""", "`;")
# handlers: options buttons are gone from these menus; new ones added
for old in ["$('hubGuide').onclick=toggleGuide;", "$('hubBanter').onclick=toggleBanter;", "if($('hubText'))$('hubText').onclick=cycleTextSize;",
            "$('hubDiff').onclick=()=>$('diffTop').click();", "$('hubManual').onclick=()=>$('manualBtn').click();"]:
    rep(old, "", n=2)
rep("$('hubExit').onclick=openExit;", "$('hubExit').onclick=openExit;$('hubSettings').onclick=openSettings;$('hubClose').onclick=()=>closeHubMenu();", n=2)
# the nearby-thing prompt is empty when there is nothing to use
rep("""el.textContent=p?`Talk / use (Enter, Space, or A): ${p}`:'Walk around town. Look for people to help and places to visit.'""",
    """el.textContent=p?`A: ${p}`:''""")

# ---------------- town menu: open/close from mouse, keyboard and controller ----------------
rep("""function openHubMenu(){if(HUB.talking||HUB.choosing||HUB.choice)return;HUB.menuNav=true;HUB.keys={};HUB.pad=[0,0];HUB.target=null;navMode='pad';
  $('menu').classList.add('menu-open');const first=$('hubSwitch')||$('menu').querySelector('button');if(first)setFocus(first,true);
  try{$('menu').scrollIntoView({block:'nearest',behavior:'smooth'})}catch(e){}HUB.banner={s:'Menu · B to close',t:100};sfx('cursor')}""",
"""function openHubMenu(){if(HUB.talking||HUB.choosing||HUB.choice)return;HUB.menuNav=true;HUB.keys={};HUB.pad=[0,0];HUB.target=null;
  $('menu').classList.add('menu-open');syncLayout();const first=$('hubSwitch')||$('menu').querySelector('button');if(first&&navMode!=='mouse')setFocus(first,true);
  if(!document.body.classList.contains('wide'))try{$('menu').scrollIntoView({block:'nearest',behavior:'smooth'})}catch(e){}sfx('cursor')}""")
rep("""  try{document.activeElement&&document.activeElement.blur()}catch(e){}if(!quiet){sfx('cancel');try{$('screen').scrollIntoView({block:'nearest',behavior:'smooth'})}catch(e){}}}""",
    """  try{document.activeElement&&document.activeElement.blur()}catch(e){}syncLayout();if(!quiet){sfx('cancel');if(!document.body.classList.contains('wide'))try{$('screen').scrollIntoView({block:'nearest',behavior:'smooth'})}catch(e){}}}""")
rep("      if(edge('Start')&&!HUB.talking){HUB.pad=[0,0];openHubMenu()}", "      if(edge('Start')&&!HUB.talking){HUB.pad=[0,0];navMode='pad';openHubMenu()}")
rep("if(edge('A')){pressA();setTimeout(()=>{if(HUB.saving||!HUB.active||HUB.choosing||HUB.talking||openModal())closeHubMenu(true)},0)}",
    "if(edge('A')){pressA();setTimeout(()=>{if(HUB.saving||!HUB.active||HUB.choosing||HUB.talking)closeHubMenu(true)},0)}")
# keyboard: Esc opens the menu; arrows move inside it while it is open
rep("""  else if(HUB.active){const k=e.key.length===1?e.key.toLowerCase():e.key;
""", """  else if(HUB.active){const k=e.key.length===1?e.key.toLowerCase():e.key;
    if(HUB.menuNav){const dirs={ArrowUp:[0,-1],ArrowDown:[0,1],ArrowLeft:[-1,0],ArrowRight:[1,0]};if(dirs[e.key]){e.preventDefault();navMode='key';moveFocus(...dirs[e.key])}
      else if(e.key==='Escape'){e.preventDefault();closeHubMenu()}else if(e.key==='Enter'||e.key===' '){const ae=document.activeElement;if(!(ae&&ae.tagName==='BUTTON')){e.preventDefault();pressA()}}return}
""")
rep("    if(k==='Escape'){e.preventDefault();hubMenuKey();return}", "    if(k==='Escape'){e.preventDefault();navMode='key';openHubMenu();return}")
# B on the settings window closes it
rep("const x=m.querySelector('#diffCancel,#netX,#xferX,#devX,#manualX,#exitNo');", "const x=m.querySelector('#diffCancel,#netX,#xferX,#devX,#manualX,#exitNo,#setX');")

# ---------------- layout engine ----------------
rep("function openModal(){",
r"""// ---- Layout: fit the picture to the window, move panels on or off it ----
function openSettings(){const d=$('setDlg');if(!d)return;d.hidden=false;sfx('cursor');setTimeout(()=>{if(navMode!=='mouse')setFocus($('setX'),true)},0)}
function syncLayout(){
  const b=document.body,scr=$('screen'),bu=$('battleUI'),menu=$('menu'),row=$('stageRow');if(!row)return;
  const vw=document.documentElement.clientWidth,vh=window.innerHeight,inB=!bu.hidden,cut=!!(typeof CUT!=='undefined'&&CUT.active);
  const wide=vw>=640&&vw>vh*1.05,inhub=!!(HUB.active&&!(typeof TITLE!=='undefined'&&TITLE.active)&&!inB);
  b.classList.toggle('wide',wide);b.classList.toggle('in-battle',inB);b.classList.toggle('cut',cut);b.classList.toggle('inhub',inhub);
  b.classList.toggle('talking',!!HUB.talking);
  if(HUB.menuNav&&(HUB.saving||HUB.choosing||!HUB.active))HUB.menuNav=false,menu.classList.remove('menu-open');
  b.classList.toggle('hubwalk',inhub&&!HUB.menuNav&&!HUB.saving&&!HUB.choosing);
  // where the panels live
  const hud=$('hubHud'),tq=$('turnOrder');
  if(wide){if(menu.parentElement!==scr)scr.appendChild(menu);if(hud.parentElement!==scr)scr.appendChild(hud);if(tq.parentElement!==scr)scr.appendChild(tq)}
  else{if(menu.parentElement!==row.parentElement||menu.previousElementSibling!==row)row.after(menu);if(hud.parentElement!==row.parentElement)row.after(hud);if(tq.parentElement!==bu)bu.insertBefore(tq,$('status'))}
  // picture size
  const hdr=document.querySelector('header').offsetHeight,wrapW=row.clientWidth,avH=vh-hdr-8*2-8-6;
  const side=inB&&wide?Math.round(Math.min(430,Math.max(300,wrapW*.3))):0;
  let w=wide?Math.min(wrapW-(side?side+10:0),avH*16/9):wrapW;w=Math.max(240,Math.floor(w));
  scr.style.setProperty('--sw',w+'px');bu.style.width=side?side+'px':'';bu.style.maxHeight=side?Math.round(w*9/16+6)+'px':'';
}
function setupLayout(){
  const scr=$('screen'),bu=$('battleUI');const row=document.createElement('div');row.id='stageRow';scr.before(row);row.append(scr,bu);
  const hud=document.createElement('div');hud.id='hubHud';scr.appendChild(hud);
  const mb=document.createElement('div');mb.id='mapBtns';mb.innerHTML='<button id="hubTalk">Talk</button><button id="mapMenu">Menu</button>';scr.appendChild(mb);
  $('mapMenu').onclick=()=>{navMode='mouse';openHubMenu()};
  // Settings window: sound, volume, difficulty, autosave, online, manual, controller, text, guide, banter
  const d=document.createElement('div');d.className='modal';d.id='setDlg';d.hidden=true;
  d.innerHTML=`<div class="modal-box" style="width:min(94%,560px)"><div class="row" style="justify-content:space-between;align-items:center"><h2 style="margin:0">Settings</h2><button id="setX">Close</button></div><div id="setBody">
    <div class="row" id="setA"></div><div class="row" id="setB"></div><div class="row" id="setC"></div><div class="row" id="setD"></div></div></div>`;
  scr.appendChild(d);
  const mv=(id,to)=>{const e=$(id);if(e)$(to).appendChild(e.tagName==='INPUT'?e.closest('label'):e)};
  mv('soundBtn','setA');mv('volMusic','setA');mv('volSfx','setA');
  mv('diffTop','setB');mv('autoTop','setB');
  $('setC').innerHTML=`<button class="textBtn">Text size: ${TEXT_SIZES[TEXT_SIZE][1]}</button><button class="guideBtn">Guide arrow: ${GUIDE?'On':'Off'}</button><button class="banterBtn">Banter: ${BANTER_ON?'On':'Off'}</button>`;
  $('setC').querySelector('.textBtn').onclick=cycleTextSize;$('setC').querySelector('.guideBtn').onclick=toggleGuide;$('setC').querySelector('.banterBtn').onclick=toggleBanter;
  mv('netBtn','setD');mv('manualBtn','setD');mv('padStatus','setD');
  $('setX').onclick=()=>{sfx('cancel');d.hidden=true};
  d.addEventListener('click',e=>{if(e.target.closest('#diffTop,#manualBtn,#netBtn'))d.hidden=true},true);
  // header: Settings and Fullscreen
  const hudBar=document.querySelector('header .hud');const sb=document.createElement('button');sb.className='mini';sb.id='settingsBtn';sb.textContent='Settings';sb.onclick=openSettings;
  const fs=document.createElement('button');fs.className='mini';fs.id='fsBtn';fs.textContent='Fullscreen';
  fs.onclick=()=>{try{document.fullscreenElement?document.exitFullscreen():document.documentElement.requestFullscreen()}catch(e){}};
  document.addEventListener('fullscreenchange',()=>{fs.textContent=document.fullscreenElement?'Exit fullscreen':'Fullscreen';setTimeout(syncLayout,50)});
  if(!document.fullscreenEnabled)fs.hidden=true;
  hudBar.insertBefore(fs,$('exitBtn'));hudBar.insertBefore(sb,fs);
  // phone held upright: one hint, dismissible
  const rh=document.createElement('div');rh.id='rotHint';rh.innerHTML='<span>Turn your phone sideways for a bigger view.</span><button class="mini" id="rotX">OK</button>';
  document.querySelector('header').after(rh);let seen=false;try{seen=sessionStorage.getItem('mk-rot')==='1'}catch(e){}if(seen)rh.hidden=true;
  $('rotX').onclick=()=>{rh.hidden=true;try{sessionStorage.setItem('mk-rot','1')}catch(e){}};
  // battle log: click to open or close
  $('log').addEventListener('click',()=>$('log').classList.toggle('open'));
  window.addEventListener('resize',syncLayout);setInterval(syncLayout,150);syncLayout();
}
function openModal(){""")
# run setup once the page has its parts (end of the main script, next to the exit-menu setup)
rep("setInterval(()=>{$('exitBtn').hidden=TITLE.active},250);\n", "setInterval(()=>{$('exitBtn').hidden=TITLE.active},250);\nsetupLayout();\n")
p.save()
