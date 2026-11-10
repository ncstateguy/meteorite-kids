"""Layout touch-ups: page fits exactly, short landscape screens keep cards in the side panel, log box sizing, no turn-order label on the picture."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from patch import Patch
p = Patch(); rep = p.rep
rep(".log::after{content:'\\25BE  Log';position:absolute;right:8px;top:6px;font-size:11px;color:var(--muted)}",
    ".log::after{content:'\\25BE  Log';position:absolute;right:8px;top:6px;font-size:11px;color:var(--muted)}.log:not(.open){align-self:start;padding-right:56px}.screen .tq-row .tq-label{display:none}")
# cards go under the picture only when the screen is tall enough; otherwise they stay in the side panel
rep("if(wide&&inB){if(stt.parentElement!==lc)lc.appendChild(stt)}", "const under=wide&&inB&&vh>=600;if(under){if(stt.parentElement!==lc)lc.appendChild(stt)}")
rep("cardsH=wide&&inB?stt.offsetHeight+8:0,avH=vh-top-8-6-cardsH;", "cardsH=under?stt.offsetHeight+8:0,avH=vh-top-8-6-cardsH-10;")
p.save()
