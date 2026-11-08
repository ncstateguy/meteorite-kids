"""Extras menu: describe the whole game, group chapters by part, and retire the old pre-release previews.

The Part 2 and Part 3 preview scenes were teasers from before those parts existed. They now spoil or
contradict the real story, so their buttons are removed (the scenes stay in the code).
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from patch import Patch
p = Patch(); rep = p.rep

rep(".chlist{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:8px}",
    ".chlist{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:8px}.chlist .chpart{grid-column:1/-1;margin:10px 0 0;font-size:14px;color:var(--accent)}.chlist .chpart small{color:var(--muted,#a9a3c4);font-weight:normal;margin-left:6px}")

rep("""$('chLabel').textContent='Part 1 · Ages 10 to 13';""", """$('chLabel').textContent='Extras';""")
rep("""<h2>Part 1: The Meteorite Kids</h2><p class="tip">From the night the stones fell to the Black Knight's last stand, plus a playable Part 3 finale. Chapters cleared: ${cleared} of ${CHAPTERS.length+1}.</p>""",
    """<h2>Extras</h2><p class="tip">Replay any chapter you have reached, from the night the stones fell to the last light over Hometown. Chapters cleared: ${cleared} of ${CHAPTERS.length+1}.</p>""")

# Chapters in story order, with a heading for each part
rep("""  CHAPTERS.forEach(c=>{const bt=document.createElement('button');bt.id='ch-'+c.key;""",
"""  const partOf=c=>c.num<=12?1:c.num<=18?2:3;let lastPart=0;
  const PARTS={1:['Part 1: The Meteorite Kids','Ages 10 to 13'],2:['Part 2: Called Back','Ages 15 to 18'],3:['Part 3: The Last Light','Fifteen years later']};
  [...CHAPTERS].sort((a,b)=>a.num-b.num).forEach(c=>{const pt=partOf(c);if(pt!==lastPart){lastPart=pt;const h=document.createElement('h3');h.className='chpart';h.innerHTML=`${PARTS[pt][0]}<small>${PARTS[pt][1]}</small>`;$('chlist').appendChild(h)}
    const bt=document.createElement('button');bt.id='ch-'+c.key;""")

# Retire the old previews; keep the Shard-Born intro (renamed) and the gallery
rep("""  const PREV=['ch-shardborn','ch-herald','ch-vorath','ch-preview5'];""", """  const PREV=['ch-shardborn'];""")
rep("""  [['shardborn','Preview · The Shard-Born',"Meet the Knight's three lieutenants"]].forEach(""",
    """  {const h=document.createElement('h3');h.className='chpart';h.textContent='More';$('chlist').appendChild(h)}
  [['shardborn','The Shard-Born',"Meet the Knight's three lieutenants"]].forEach(""")
rep("""  {const bt=document.createElement('button');bt.id='ch-herald';bt.innerHTML=`Preview · The Herald<small>Part 2 story scene · A dark crusader arrives</small>`;
   bt.onclick=async()=>{await playCutscene(SCENES.herald);showChapters()};$('chlist').appendChild(bt)}
  {const bt=document.createElement('button');bt.id='ch-vorath';bt.innerHTML=`Preview · Vorath the Unmaker<small>Part 3 story scene · The Dark King arrives</small>`;
   bt.onclick=async()=>{await playCutscene(SCENES.vorath);showChapters()};$('chlist').appendChild(bt)}
  {const bt=document.createElement('button');bt.id='ch-preview5';bt.innerHTML=`Preview · The Last Light<small>Part 3 story scene · the Last Light Forms</small>`;
   bt.onclick=async()=>{await playCutscene(SCENES.preview5);showChapters()};$('chlist').appendChild(bt)}
""", "")
p.save()
