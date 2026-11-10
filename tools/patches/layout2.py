"""Layout follow-up from screenshots.

- Battles (landscape): hero cards sit in one row under the picture; the side panel holds the actions and log,
  so the whole battle fits on one screen. Turn order stays on one line.
- The town HUD and walk mode only apply when the town menu is the one showing (results and other screens stay visible).
- Page height is measured from where the picture actually starts (no stray scroll).
- Phones held upright: the header wraps again.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from patch import Patch
p = Patch(); rep = p.rep

rep("#stageRow{display:flex;flex-direction:column;align-items:center;gap:10px;width:100%}",
    "#stageRow{display:flex;flex-direction:column;align-items:center;gap:10px;width:100%}"
    "#leftCol{display:flex;flex-direction:column;gap:8px;align-items:stretch;max-width:100%}"
    "body.wide.in-battle #leftCol .status{grid-template-columns:repeat(auto-fit,minmax(150px,1fr))}"
    "@media (max-width:640px){header{flex-wrap:wrap}header .hud{flex-wrap:wrap}}")
rep("body.wide.in-battle #battleUI .status{grid-template-columns:repeat(2,minmax(0,1fr))}", "")
rep(".screen .tq-row{position:absolute;top:5px;left:6px;right:6px;margin:0;z-index:6;padding:3px 4px;background:rgba(8,6,20,.62);border-radius:4px}",
    ".screen .tq-row{position:absolute;top:5px;left:6px;right:6px;margin:0;z-index:6;padding:3px 4px;background:rgba(8,6,20,.62);border-radius:4px;flex-wrap:nowrap!important;overflow:hidden!important}")

# layout engine: left column = picture + cards (battle), town-menu check, exact height
rep("""  const wide=vw>=640&&vw>vh*1.05,inhub=!!(HUB.active&&!(typeof TITLE!=='undefined'&&TITLE.active)&&!inB);""",
    """  const wide=vw>=640&&vw>vh*1.05,hubMenu=!!(menu.querySelector('#hubSwitch')||(!menu.children.length&&!HUB.saving)),inhub=!!(HUB.active&&!(typeof TITLE!=='undefined'&&TITLE.active)&&!inB&&hubMenu);""")
rep("""  const hud=$('hubHud'),tq=$('turnOrder');
  if(wide){if(menu.parentElement!==scr)scr.appendChild(menu);if(hud.parentElement!==scr)scr.appendChild(hud);if(tq.parentElement!==scr)scr.appendChild(tq)}
  else{if(menu.parentElement!==row.parentElement||menu.previousElementSibling!==row)row.after(menu);if(hud.parentElement!==row.parentElement)row.after(hud);if(tq.parentElement!==bu)bu.insertBefore(tq,$('status'))}""",
    """  const hud=$('hubHud'),tq=$('turnOrder'),stt=$('status'),lc=$('leftCol');
  if(wide){if(menu.parentElement!==scr)scr.appendChild(menu);if(hud.parentElement!==scr)scr.appendChild(hud);if(tq.parentElement!==scr)scr.appendChild(tq)}
  else{if(menu.parentElement!==row.parentElement||menu.previousElementSibling!==row)row.after(menu);if(hud.parentElement!==row.parentElement)row.after(hud);if(tq.parentElement!==bu)bu.insertBefore(tq,bu.querySelector('.deck'))}
  if(wide&&inB){if(stt.parentElement!==lc)lc.appendChild(stt)}else if(stt.parentElement!==bu)bu.insertBefore(stt,bu.querySelector('.deck'))""")
rep("""  const hdr=document.querySelector('header').offsetHeight,wrapW=row.clientWidth,avH=vh-hdr-8*2-8-6;
  const side=inB&&wide?Math.round(Math.min(430,Math.max(300,wrapW*.3))):0;
  let w=wide?Math.min(wrapW-(side?side+10:0),avH*16/9):wrapW;w=Math.max(240,Math.floor(w));
  scr.style.setProperty('--sw',w+'px');bu.style.width=side?side+'px':'';bu.style.maxHeight=side?Math.round(w*9/16+6)+'px':'';""",
    """  const top=row.getBoundingClientRect().top+window.scrollY,wrapW=row.clientWidth,cardsH=wide&&inB?stt.offsetHeight+8:0,avH=vh-top-8-6-cardsH;
  const side=inB&&wide?Math.round(Math.min(430,Math.max(290,wrapW*.28))):0;
  let w=wide?Math.min(wrapW-(side?side+10:0),avH*16/9):wrapW;w=Math.max(240,Math.floor(w));
  scr.style.setProperty('--sw',w+'px');lc.style.width=wide?w+'px':'100%';bu.style.width=side?side+'px':'';bu.style.maxHeight=side?Math.round(vh-top-8)+'px':'';""")
# build the left column once
rep("""  const scr=$('screen'),bu=$('battleUI');const row=document.createElement('div');row.id='stageRow';scr.before(row);row.append(scr,bu);""",
    """  const scr=$('screen'),bu=$('battleUI');const row=document.createElement('div');row.id='stageRow';scr.before(row);const lc=document.createElement('div');lc.id='leftCol';row.append(lc,bu);lc.appendChild(scr);""")
p.save()
