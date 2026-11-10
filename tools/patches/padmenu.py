"""Controller: reach the town/dungeon menu, and drive every pop-up window (playtest fix).

- Start in town or a dungeon opens the menu: the hero stops, the D-pad moves between buttons,
  A presses, B or Start closes. Select still opens Exit.
- Town and dungeon menus get Difficulty, Manual and Exit buttons (those were header-only).
- Difficulty, Online and Move saves windows work with the controller; B closes them.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from patch import Patch
p = Patch(); rep = p.rep

# --- Focus lands in whatever window is open, or the menu while the town menu is open ---
rep("""function navItems(){
  const root=!$('manualDlg').hidden?$('manualDlg'):!$('exitDlg').hidden?$('exitDlg'):$('battleUI').hidden?$('menu'):$('btns');
  const extra=[...document.querySelectorAll('header button')];""",
"""function openModal(){return !$('exitDlg').hidden?$('exitDlg'):!$('manualDlg').hidden?$('manualDlg'):[...document.querySelectorAll('.modal')].find(m=>!m.hidden)||null}
function closeModal(m){const x=m.querySelector('#diffCancel,#netX,#xferX,#devX,#manualX,#exitNo');sfx('cancel');if(x)x.click();else m.hidden=true}
function navItems(){
  const mo=openModal();const root=mo||($('battleUI').hidden?$('menu'):$('btns'));
  const extra=mo||HUB.menuNav?[]:[...document.querySelectorAll('header button')];""")
rep("function pressB(){if(!$('exitDlg').hidden){sfx('cancel');closeExit();return}",
    "function pressB(){if(!$('exitDlg').hidden){sfx('cancel');closeExit();return}{const mo=openModal();if(mo&&mo.id!=='manualDlg'){closeModal(mo);return}}")

# --- Town menu mode ---
rep("function hubMenuKey(){",
"""function openHubMenu(){if(HUB.talking||HUB.choosing||HUB.choice)return;HUB.menuNav=true;HUB.keys={};HUB.pad=[0,0];HUB.target=null;navMode='pad';
  $('menu').classList.add('menu-open');const first=$('hubSwitch')||$('menu').querySelector('button');if(first)setFocus(first,true);
  try{$('menu').scrollIntoView({block:'nearest',behavior:'smooth'})}catch(e){}HUB.banner={s:'Menu · B to close',t:100};sfx('cursor')}
function closeHubMenu(quiet){if(!HUB.menuNav)return;HUB.menuNav=false;$('menu').classList.remove('menu-open');document.querySelectorAll('.pad-focus').forEach(x=>x.classList.remove('pad-focus'));
  try{document.activeElement&&document.activeElement.blur()}catch(e){}if(!quiet){sfx('cancel');try{$('screen').scrollIntoView({block:'nearest',behavior:'smooth'})}catch(e){}}}
function hubMenuKey(){""")
rep(".pad-focus{border-color:var(--accent);box-shadow:0 0 0 2px var(--accent);outline:none}",
    ".pad-focus{border-color:var(--accent);box-shadow:0 0 0 2px var(--accent);outline:none}#menu.menu-open{box-shadow:0 0 0 2px var(--accent)}")

# --- Controller polling: windows first, then the town menu ---
rep("    if(TITLE.active&&!TITLE.pressed){if(edge('A')||edge('Start'))titlePress();PAD.prev=st;requestAnimationFrame(pollPad);return}\n",
"""    if(TITLE.active&&!TITLE.pressed){if(edge('A')||edge('Start'))titlePress();PAD.prev=st;requestAnimationFrame(pollPad);return}
    {const mo=openModal();if(mo){HUB.pad=[0,0];if(rep('U'))moveFocus(0,-1);if(rep('D'))moveFocus(0,1);if(rep('L'))moveFocus(-1,0);if(rep('R'))moveFocus(1,0);if(edge('A'))pressA();if(edge('B'))closeModal(mo);PAD.prev=st;requestAnimationFrame(pollPad);return}}
""")
rep("""      if(edge('A')){HUB.talking?hubAdvance():hubInteract(HUB.near)}if(edge('B')&&HUB.talking)hubAdvance();""",
"""      if(HUB.menuNav){HUB.pad=[0,0];if(rep('U'))moveFocus(0,-1);if(rep('D'))moveFocus(0,1);if(rep('L'))moveFocus(-1,0);if(rep('R'))moveFocus(1,0);
        if(edge('A')){pressA();setTimeout(()=>{if(HUB.saving||!HUB.active||HUB.choosing||HUB.talking||openModal())closeHubMenu(true)},0)}
        else if(edge('B')||edge('Start'))closeHubMenu();PAD.prev=st;requestAnimationFrame(pollPad);return}
      if(edge('A')){HUB.talking?hubAdvance():hubInteract(HUB.near)}if(edge('B')&&HUB.talking)hubAdvance();""")
rep("      if(edge('Start')&&!HUB.talking){HUB.pad=[0,0];hubMenuKey()}",
    "      if(edge('Start')&&!HUB.talking){HUB.pad=[0,0];openHubMenu()}")
# leaving town for a scene or battle closes the menu mode
rep("function enterHub(){\n  if(HUB.area)return enterArea();", "function enterHub(){\n  HUB.menuNav=false;\n  if(HUB.area)return enterArea();")
rep("function enterArea(){const A=AREAS[HUB.area];", "function enterArea(){const A=AREAS[HUB.area];HUB.menuNav=false;")

# --- Difficulty, Manual, Exit in the town and dungeon menus ---
SYS = """<div class="row" style="margin-top:6px"><button id="hubDiff">Difficulty</button><button id="hubManual">Manual</button><button id="hubExit">Exit game</button></div>"""
rep("""<button class="textBtn" id="hubText">Text size: ${TEXT_SIZES[TEXT_SIZE][1]}</button><button id="hubSave">Save</button></div>""",
    """<button class="textBtn" id="hubText">Text size: ${TEXT_SIZES[TEXT_SIZE][1]}</button><button id="hubSave">Save</button></div>
   """ + SYS, n=2)
rep("$('hubBanter').onclick=toggleBanter;if($('hubText'))$('hubText').onclick=cycleTextSize;",
    "$('hubBanter').onclick=toggleBanter;if($('hubText'))$('hubText').onclick=cycleTextSize;$('hubDiff').onclick=()=>$('diffTop').click();$('hubManual').onclick=()=>$('manualBtn').click();$('hubExit').onclick=openExit;", n=2)

# --- Help text under the map ---
rep("""${STORY?(part1Done()?'Extras: Esc or Start.':'Exit: Esc or Start.'):'Chapter list: Esc or Start.'}""",
    """${STORY?(part1Done()?'Extras: Esc.':'Exit: Esc.'):'Chapter list: Esc.'} Controller: Start opens this menu, Select exits.""")
rep("Talk or use a field power: Enter, Space, or A. Change hero: Tab, Q, or X/Y.",
    "Talk or use a field power: Enter, Space, or A. Change hero: Tab, Q, or X/Y. Controller: Start opens this menu, Select exits.")
rep('<li><b>In town:</b> Tab, Q, or X/Y changes your hero. Esc or Start opens the exit menu.</li>',
    '<li><b>In town and dungeons:</b> Tab, Q, or X/Y changes your hero. On a controller, Start opens the menu (Party, Save, Extras, options): the D-pad moves, A picks, B closes. The View button opens Exit. On a keyboard, Esc opens the exit menu.</li>')
p.save()
