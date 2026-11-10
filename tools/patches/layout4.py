"""Layout: short landscape battles show actions before cards; portrait town shows the HUD above the menu; no Close menu in portrait."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from patch import Patch
p = Patch(); rep = p.rep
rep("else{if(menu.parentElement!==row.parentElement||menu.previousElementSibling!==row)row.after(menu);if(hud.parentElement!==row.parentElement)row.after(hud);",
    "else{if(hud.previousElementSibling!==row)row.after(hud);if(menu.previousElementSibling!==hud)hud.after(menu);")
rep("const under=wide&&inB&&vh>=600;if(under){if(stt.parentElement!==lc)lc.appendChild(stt)}else if(stt.parentElement!==bu)bu.insertBefore(stt,bu.querySelector('.deck'))",
    "const under=wide&&inB&&vh>=600;if(under){if(stt.parentElement!==lc)lc.appendChild(stt)}else if(wide){if(bu.lastElementChild!==stt)bu.appendChild(stt)}else if(stt.nextElementSibling!==bu.querySelector('.deck'))bu.insertBefore(stt,bu.querySelector('.deck'))")
rep("#rotHint{display:none;", "body:not(.wide) #hubClose{display:none}#rotHint{display:none;")
p.save()
