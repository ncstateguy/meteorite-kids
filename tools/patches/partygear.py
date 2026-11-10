"""Party screen: make the gear slots usable (playtest: "I can't figure out how to equip gear").

Weapons and outfits are upgraded at the Old Forge, not swapped, so their slots now open the forge for
that hero (Back returns to Party). The charm slot jumps to the charm list, or opens the forge to craft
one. A line at the top of Equipment explains how it works.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from patch import Patch
p = Patch(); rep = p.rep

rep("""   <h3>Equipment</h3>
   <div class="slots">
    <div class="slot" style="cursor:default">Weapon: ${weaponName(who,g.w)}<small>${g.w?`+${WEAPON_TIERS[g.w].v} ${main}`:'No bonus yet'} · ${tierOpen(WEAPON_TIERS[g.w+1])?(progress.ch4?'Josh can upgrade it at the Old Forge.':'Josh can upgrade it once he joins the team.'):'Fully upgraded for now.'}</small></div>
    <div class="slot" style="cursor:default">Outfit: ${g.o?OUTFIT_TIERS[g.o].name:'Everyday clothes'}<small>${g.o?`+${OUTFIT_TIERS[g.o].v} HP`:'No bonus yet'} · ${tierOpen(OUTFIT_TIERS[g.o+1])?(progress.ch4?'Josh can upgrade it at the Old Forge.':'Josh can upgrade it once he joins the team.'):'Fully upgraded for now.'}</small></div>
    <div class="slot" style="cursor:default">Charm: ${g.c?`${CHARMS[g.c].name}`:'None'}<small>${g.c?CHARMS[g.c].desc:(owned.length?'Pick one below.':'Josh can craft charms at the Old Forge.')}</small></div>""",
"""   <h3>Equipment</h3>
   <p class="tip" style="margin:0 0 6px">Each hero has one weapon and one outfit. Josh upgrades them at the Old Forge, and the new one is worn right away. Charms are crafted there too, then equipped here.</p>
   <div class="slots">
    <button class="slot" id="pgW" ${progress.ch4?'':'disabled'}>Weapon: ${weaponName(who,g.w)}<small>${g.w?`+${WEAPON_TIERS[g.w].v} ${main}`:'No bonus yet'} · ${tierOpen(WEAPON_TIERS[g.w+1])?(progress.ch4?'Upgrade at the forge':'Josh can upgrade it once he joins the team.'):'Fully upgraded for now.'}</small></button>
    <button class="slot" id="pgO" ${progress.ch4?'':'disabled'}>Outfit: ${g.o?OUTFIT_TIERS[g.o].name:'Everyday clothes'}<small>${g.o?`+${OUTFIT_TIERS[g.o].v} HP`:'No bonus yet'} · ${tierOpen(OUTFIT_TIERS[g.o+1])?(progress.ch4?'Upgrade at the forge':'Josh can upgrade it once he joins the team.'):'Fully upgraded for now.'}</small></button>
    <button class="slot" id="pgC" ${owned.length||progress.ch4?'':'disabled'}>Charm: ${g.c?`${CHARMS[g.c].name}`:'None'}<small>${g.c?CHARMS[g.c].desc:(owned.length?'Pick one below.':progress.ch4?'Craft one at the forge':'Josh can craft charms once he joins the team.')}</small></button>""")

# Handlers, next to the Party back button
rep("$('partyBack').onclick=()=>{HUB.saving=false;",
    """const toForge=()=>{FORGE_RET=who;openForge(who)};if($('pgW'))$('pgW').onclick=toForge;if($('pgO'))$('pgO').onclick=toForge;
  if($('pgC'))$('pgC').onclick=()=>{const first=$('menu').querySelector('[id^="pc-"]:not([disabled])');if(first){setFocus(first);first.scrollIntoView({block:'nearest'})}else if(progress.ch4)toForge()};
  $('partyBack').onclick=()=>{HUB.saving=false;""")

# Forge: Back returns to Party when it was opened from there
rep("function openForge(who){", "let FORGE_RET=null;\nfunction openForge(who){")
rep("$('forgeBack').onclick=()=>{HUB.saving=false;enterHub()};",
    "$('forgeBack').onclick=()=>{if(FORGE_RET){const r=FORGE_RET;FORGE_RET=null;openParty(FORGE_WHO||r);return}HUB.saving=false;enterHub()};")
# The forge's own "Back" label says where it goes
rep("""<p class="tip" id="forgeMsg"></p><div class="row"><button id="forgeBack">Back</button>""",
    """<p class="tip" id="forgeMsg"></p><div class="row"><button id="forgeBack">${FORGE_RET?'Back to Party':'Back'}</button>""")
p.save()
