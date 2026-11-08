"""Accessibility (audit P2): a text size option, and a warning icon on red status tags.

Text size: Normal / Large / Larger. Scales menus, battle panels, dialogs, dialogue, captions and banter.
Set from the title screen or the town menu; remembered in this browser.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from patch import Patch
p = Patch(); rep = p.rep

# CSS: one scale variable
rep(".chip.warn{border-color:var(--danger);color:var(--danger)}",
    ".chip.warn{border-color:var(--danger);color:var(--danger)}.chip.warn::before{content:'\\26A0  '}"
    ":root{--ts:1}#menu,#battleUI,.modal-box{zoom:var(--ts)}")
rep("font-size:clamp(13px,2.4vw,18px)", "font-size:calc(clamp(13px,2.4vw,18px)*var(--ts))")
rep("font-size:clamp(11px,1.9vw,15px)", "font-size:calc(clamp(11px,1.9vw,15px)*var(--ts))")
rep("font-size:clamp(14px,2.7vw,20px)", "font-size:calc(clamp(14px,2.7vw,20px)*var(--ts))")

# JS: setting, saved per browser
rep("function toggleBanter(){",
"""const TEXT_SIZES=[[1,'Normal'],[1.2,'Large'],[1.4,'Larger']];
let TEXT_SIZE=0;try{TEXT_SIZE=Math.max(0,Math.min(2,+localStorage.getItem('mk-text')||0))}catch(e){}
function applyTextSize(){document.documentElement.style.setProperty('--ts',TEXT_SIZES[TEXT_SIZE][0]);document.querySelectorAll('.textBtn').forEach(b=>b.textContent=`Text size: ${TEXT_SIZES[TEXT_SIZE][1]}`)}
function cycleTextSize(){TEXT_SIZE=(TEXT_SIZE+1)%TEXT_SIZES.length;try{localStorage.setItem('mk-text',String(TEXT_SIZE))}catch(e){}sfx('cursor');applyTextSize()}
applyTextSize();
function toggleBanter(){""")

# Town menu (both places it is built)
rep("""<button class="banterBtn" id="hubBanter">Banter: ${BANTER_ON?'On':'Off'}</button><button id="hubSave">Save</button>""",
    """<button class="banterBtn" id="hubBanter">Banter: ${BANTER_ON?'On':'Off'}</button><button class="textBtn" id="hubText">Text size: ${TEXT_SIZES[TEXT_SIZE][1]}</button><button id="hubSave">Save</button>""", n=2)
rep("$('hubBanter').onclick=toggleBanter;", "$('hubBanter').onclick=toggleBanter;if($('hubText'))$('hubText').onclick=cycleTextSize;", n=2)

# Title screen
rep("""<button id="tLog">Playtest log<small>Send fight results to Claude</small></button></div>`;""",
    """<button id="tLog">Playtest log<small>Send fight results to Claude</small></button><button class="textBtn" id="tText">Text size: ${TEXT_SIZES[TEXT_SIZE][1]}</button></div>`;""")
rep("$('tMove').onclick=()=>XFER.open();$('tLog').onclick=()=>PLOG.open();",
    "$('tMove').onclick=()=>XFER.open();$('tLog').onclick=()=>PLOG.open();$('tText').onclick=cycleTextSize;")
# The boss-warning chip had its own icon; the CSS one replaces it
rep('<span class="chip warn tele">⚠ Next: ${bw}</span>','<span class="chip warn tele">Next: ${bw}</span>')
p.save()
