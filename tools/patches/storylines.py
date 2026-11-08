"""Approved story drafts (audit P2): Vorath's motive, Tricia's notebook, Josh and Lindsey in Part 3."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from patch import Patch
p = Patch(); rep = p.rep

# 1. Vorath's motive and the Eternal Silence (Ch 24, phase 2)
rep("""  {say:'nightshade',text:"They're not singing for you. You kept them from having a future."},
  {cap:'Phase 2: the Unmade is a spirit.""",
"""  {say:'nightshade',text:"They're not singing for you. You kept them from having a future."},
  {say:'boss',text:'Every light I took was burning in fear. When it goes out, it stops being afraid. That is the Eternal Silence. I am not cruel. I am the only one who ever made them quiet.'},
  {say:'nightshade',text:"They weren't afraid. They were alive. You couldn't tell the difference."},
  {cap:'Phase 2: the Unmade is a spirit.""")

# 2. Tricia's notebook (Ch 22 road trip), echoing Mr. Hollis's "Somebody had to remember him."
rep("""  {say:'nightshade',text:'Canyon, temple, forge, grove, and the peak. Each one held a relic.'},
  {say:'lightheart',text:"Then let's go get your light back."},""",
"""  {say:'nightshade',text:'Canyon, temple, forge, grove, and the peak. Each one held a relic.'},
  {say:'scareth',text:'You still have that notebook?'},
  {say:'nightshade',text:'Somebody has to remember him right.'},
  {say:'lightheart',text:"Then let's go get your light back."},""")
# ...and after the finale, at Mr. Hollis's bench, the clippings go to the museum
rep("""['me:nightshade','I kept every clipping, Mr. Hollis. Every single one.'],['me','He would have loved Founders\\' Day.']]));""",
    """['me:nightshade','I kept every clipping, Mr. Hollis. Every single one.'],...(progress.ch27?[['me:nightshade',"They're going to the museum, next to yours. He belongs to everyone now."]]:[]),['me','He would have loved Founders\\' Day.']]));""")

# 3. Josh and Lindsey (Ch 21, the night at the crater)
rep("""  {say:'lightheart',text:'Everybody ready?'},
  {cap:'Five cracked stones, set together in the grass.',top:true},""",
"""  {say:'lightheart',text:'Everybody ready?'},
  {cap:'Lindsey hums under her breath.',top:true},
  {say:'thornforge',text:"You still hum when you're nervous."},
  {say:'kaytahn',text:'You still notice.'},
  {cap:'Five cracked stones, set together in the grass.',top:true},""")
p.save()
