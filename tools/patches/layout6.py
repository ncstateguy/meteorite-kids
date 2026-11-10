"""Manual: describe the new menu, Settings window and Fullscreen."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from patch import Patch
p = Patch(); rep = p.rep
rep("On a controller, Start opens the menu (Party, Save, Extras, options): the D-pad moves, A picks, B closes. The View button opens Exit. On a keyboard, Esc opens the exit menu.</li>",
    "The menu (Party, Save, Extras, Settings) opens with Start on a controller, Esc on a keyboard, or the Menu button in the corner of the map. On a controller the D-pad moves, A picks and B closes; the View button opens Exit.</li>")
rep("You can turn it off on the title screen or in town.</li>", "You can turn it off in Settings.</li>")
rep("<li><b>Save by hand</b> in town with the Save button or the glowing Meteor Crystal", "<li><b>Save by hand</b> with Save in the menu or the glowing Meteor Crystal")
rep("<li><b>Exit</b> (top bar) lets you", "<li><b>Settings</b> (top bar) has sound, music and effects volume, difficulty, autosave, text size, the guide arrow, banter, online play and this manual. <b>Fullscreen</b> (top bar) fills the whole screen.</li>\n    <li><b>Exit</b> (top bar) lets you")
p.save()
