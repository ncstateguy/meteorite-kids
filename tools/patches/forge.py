"""Forge upgrades for Parts 2 and 3 (audit P2: nothing to buy after Part 1).

Part 2 bosses drop Rift Shards, Part 3 bosses drop Guardian Stones. Each unlocks one more weapon and
outfit tier, shown once you reach that part. Coins are the main cost, so they matter again.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from patch import Patch
p = Patch(); rep = p.rep

# Materials from Part 2 and Part 3 bosses
rep("ch10:['Keep Iron','from the Knight\\'s Keep'],ch11:['Black Shard Dust','from the Knight\\'s broken shard'],patrol:",
    "ch10:['Keep Iron','from the Knight\\'s Keep'],ch11:['Black Shard Dust','from the Knight\\'s broken shard'],\n"
    "  ch13:['Rift Shard','a sliver of the rift'],ch14:['Rift Shard','a sliver of the rift'],ch15:['Rift Shard','a sliver of the rift'],ch16:['Rift Shard','a sliver of the rift'],ch17:['Rift Shard','from the Herald\\'s spire'],ch18a:['Rift Shard','from the Herald\\'s spire'],ch18:['Rift Shard','from the Herald\\'s spire'],\n"
    "  ch19:['Guardian Stone','a pebble the Guardians left behind'],ch20:['Guardian Stone','a pebble the Guardians left behind'],ch21:['Guardian Stone','a pebble the Guardians left behind'],ch22:['Guardian Stone','warm from a relic site'],ch23:['Guardian Stone','from the crater'],patrol:")

# Two more tiers; `need` is the chapter that unlocks the tier at the forge
rep("  {pre:'Keep-Iron',v:7,cost:{'Keep Iron':1,'Crimson Flake':1,Soot:4},coins:50}];",
    "  {pre:'Keep-Iron',v:7,cost:{'Keep Iron':1,'Crimson Flake':1,Soot:4},coins:50},\n"
    "  {pre:'Rift-Tempered',v:10,cost:{'Rift Shard':1,Soot:4},coins:80,need:'ch13'},\n"
    "  {pre:'Guardian-Forged',v:13,cost:{'Guardian Stone':1,Soot:5},coins:100,need:'ch19'}];")
rep("  {name:'Keep-Plate Vest',v:32,cost:{'Lantern Glass':1,'Keep Iron':1,Soot:4},coins:50}];",
    "  {name:'Keep-Plate Vest',v:32,cost:{'Lantern Glass':1,'Keep Iron':1,Soot:4},coins:50},\n"
    "  {name:'Rift-Lined Coat',v:44,cost:{'Rift Shard':1,Soot:4},coins:80,need:'ch13'},\n"
    "  {name:'Guardian Coat',v:56,cost:{'Guardian Stone':1,Soot:5},coins:100,need:'ch19'}];\n"
    "const tierOpen=t=>!!t&&(!t.need||!!progress[t.need]);")

# Forge screen: only offer a tier once its part is reached
rep("const wn=WEAPON_TIERS[g.w+1],on=OUTFIT_TIERS[g.o+1];",
    "const wn=tierOpen(WEAPON_TIERS[g.w+1])?WEAPON_TIERS[g.w+1]:null,on=tierOpen(OUTFIT_TIERS[g.o+1])?OUTFIT_TIERS[g.o+1]:null;")

# Party screen: "can upgrade" follows the open tiers, not a fixed 3
rep("g.w<3?(progress.ch4?'Josh can upgrade it at the Old Forge.':'Josh can upgrade it once he joins the team.'):'Fully upgraded.'",
    "tierOpen(WEAPON_TIERS[g.w+1])?(progress.ch4?'Josh can upgrade it at the Old Forge.':'Josh can upgrade it once he joins the team.'):'Fully upgraded for now.'")
s = p.s
old = "g.o<3?(progress.ch4?'Josh can upgrade it at the Old Forge.':'Josh can upgrade it once he joins the team.'):'Fully upgraded.'"
if old in s:
    rep(old, "tierOpen(OUTFIT_TIERS[g.o+1])?(progress.ch4?'Josh can upgrade it at the Old Forge.':'Josh can upgrade it once he joins the team.'):'Fully upgraded for now.'")
p.save()
