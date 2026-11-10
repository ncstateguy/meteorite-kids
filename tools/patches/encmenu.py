"""No menu flash on the way into a fight (playtest).

The town menu only shows over the map when it was opened; any menu is hidden while the battle intro plays.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from patch import Patch
p = Patch(); rep = p.rep
rep("body.wide.hubwalk .screen #menu,body.cut .screen #menu{display:none}",
    "body.wide.hubwalk .screen #menu,body.cut .screen #menu,body.wide .screen #menu:has(#hubSwitch):not(.menu-open),body.enc #menu,body.enc #hubHud,body.enc #mapBtns{display:none!important}")
rep("  if(fx)await ENC.cover(fx,c);\n", "  document.body.classList.add('enc');try{if(fx)await ENC.cover(fx,c)}catch(e){}\n")
rep("renderStatus();if(fx)await ENC.reveal(fx);battle();", "renderStatus();try{if(fx)await ENC.reveal(fx)}finally{document.body.classList.remove('enc')}battle();")
p.save()
