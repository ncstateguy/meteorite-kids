"""Fewer stated morals (audit P2, approved list): four victory lines, two scene lines cut, three 'Together' rally cries trimmed."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from patch import Patch
p = Patch(); rep = p.rep
rep("victory:'Strike Out is bowled over. Scareth learns that speed and timing beat brute force, and that setting up his friends wins more than showing off.'",
    "victory:'Strike Out is bowled over. Scareth spent the whole fight knocking down pins so his friends could land the big hits. He looks weirdly proud about it.'")
rep("victory:'Captain Chomp flops back into the lake. Kaytahn kept everyone standing the whole fight, and the team knows it: she is their backbone.'",
    "victory:'Captain Chomp flops back into the lake. Kaytahn is soaked, exhausted, and the only reason anyone is still standing.'")
rep("victory:'Overclock winds down for good and the tower bells ring true. Lightheart learned that leading means lifting the others up.'",
    "victory:'Overclock winds down for good, and the tower bells ring true.'")
rep("victory:'Hollow Hart\\'s lantern shatters and the Hollow goes quiet. Every time one of them was trapped, someone came for them.'",
    "victory:'Hollow Hart\\'s lantern shatters, and the Hollow goes quiet.'")
rep("""{say:'kaytahn',text:"That's what a team is for."},""", "")
rep("""{say:'thornforge',text:"That's the whole trick, isn't it? Nobody fights alone."},""", "")
rep("text:'Then we get him out. Together!'", "text:'Then we get him out of there!'")
rep("text:'Same as always. Together.'", "text:'Same as always.'")
rep("text:'Then we give it. All of it. Together.'", "text:'Then we give it. All of it.'")
p.save()
