"""Layout: no HUD or Menu button during scenes; the 'Saved' tag moves clear of the HUD."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from patch import Patch
p = Patch()
p.rep("body:not(.wide) #hubClose{display:none}", "body:not(.wide) #hubClose{display:none}body.cut #mapBtns,body.cut #hubHud{display:none!important}body.wide .screen .hub-saved{top:auto;bottom:44px}")
p.save()
