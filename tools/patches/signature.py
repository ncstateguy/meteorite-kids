"""Adult signature moves (audit P2: adults have a thin kit in Ch 19 to 21).

One move each, from their grown-up lives, with a 3-turn recharge. Used in Ch 19 to 21 and the Ch 25
rematch, the adult fights without relic powers.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from patch import Patch
p = Patch(); rep = p.rep

rep("function actionsFor(k){\n",
"""// Adult signature moves: Ch 19 to 21 and the Ch 25 rematch (the adult fights without relics)
const SIG_CH=['ch19','ch20','ch21','ch25r'];
const SIG={
  lightheart:{label:'Rally Call',desc:'Every friend on the field acts sooner',run:async k=>{activeAlive().filter(p=>p!==k).forEach(p=>{p.haste=Math.max(p.haste|0,1);floatText(...kidCenter(p),'Rallied!','#ffd76a')});sfx('confirm');burst(...kidCenter(k),'#ffd76a',18);log('Rally Call! Jake gets everyone moving.')}},
  scareth:{label:'Stunt Double',desc:"Draw the boss's next attack and dodge it",run:async k=>{k.stunt=true;sfx('dodge');burst(...kidCenter(k),'#c8d0dc',16);log('Stunt Double! Joseph waves both arms at the boss. "Over here!"')}},
  kaytahn:{label:'Triage',desc:'Heal the most hurt friend by 30% and clear slow or disarm',run:async k=>{const pool=activeAlive();const t=pool.sort((a,c)=>a.hp/a.hpMax-c.hp/c.hpMax)[0];if(!t)return;heal(t,Math.round(t.hpMax*.3));t.slow=0;t.disarmed=false;burst(...kidCenter(t),'#4fe0d0',16);log(`Triage! Lindsey patches up ${t.kid}.`)}},
  thornforge:{label:'Field Repair',desc:'Every friend gets a shield that halves their next hit',run:async k=>{activeAlive().forEach(p=>{p.barrier=true;floatText(...kidCenter(p),'Shielded','#9fc0ff')});sfx('shield');burst(...kidCenter(k),'#ff9a3a',16);log('Field Repair! Josh fixes up everyone\\'s gear with duct tape and hope.')}},
  nightshade:{label:'Recall',desc:'You have seen this before: hex the boss for 2 turns and slow it',run:async k=>{const b=S.boss;b.hex=Math.max(b.hex|0,2);b.slow=Math.max(b.slow|0,1);sfx('magic');floatText(BOSS_C[0],BOSS_C[1]-30,'Recalled','#c8b8ff');log('Recall! Tricia remembers exactly how this fight goes.')}}};
function sigAction(k){const g=SIG[k.id];if(!g||!SIG_CH.includes(S.ch.key)||k.powered)return null;
  return {label:g.label,desc:k.sgcd?`Recharging: ${k.sgcd} turn${k.sgcd>1?'s':''}`:g.desc,disabled:k.sgcd>0,run:async()=>{k.sgcd=3;await g.run(k);renderStatus()}}}
function actionsFor(k){
""")
rep("  if(C.age==='adult'&&!k.powered){const r=relicAction(k);if(r)A.push(r);",
    "  {const sg=sigAction(k);if(sg)A.push(sg)}\n  if(C.age==='adult'&&!k.powered){const r=relicAction(k);if(r)A.push(r);")
# recharge ticks with the other cooldowns
rep("if(k.rcd>0)k.rcd--;if(k.scd>0)k.scd--;if(k.guard>0)k.guard--;", "if(k.rcd>0)k.rcd--;if(k.scd>0)k.scd--;if(k.sgcd>0)k.sgcd--;if(k.guard>0)k.guard--;")
# Stunt Double: draws the next single-target hit, then dodges it (also dodges one team-wide hit)
rep("  if(S.boss.taunt>0){const t=a.find(k=>k.id==='thornforge');if(t)return t}\n",
    "  {const sd=a.find(k=>k.stunt);if(sd)return sd}\n  if(S.boss.taunt>0){const t=a.find(k=>k.id==='thornforge');if(t)return t}\n")
rep("  if(k.veil){k.veil=false;",
    "  if(k.stunt){k.stunt=false;sfx('dodge');floatText(...kidCenter(k),'Stunt double!','#c8d0dc');log(`${k.kid} dives out of the way. The boss hits nothing but air.`);return}\n  if(k.veil){k.veil=false;")
# Teach it once, in Ch 19
rep("{cap:'Nobody can morph anymore. When Gale Showboats for the crowd, hit her hard.',top:true}",
    "{cap:'Nobody can morph anymore, but each of you has a new signature move. When Gale Showboats for the crowd, hit her hard.',top:true}")
rep("tip:'Nobody can morph anymore. When Gale Showboats for the crowd, she leaves herself open: hit her hard on the next turn.',",
    "tip:'Nobody can morph anymore, but each of you has a new signature move from your grown-up life, with a 3-turn recharge. When Gale Showboats for the crowd, she leaves herself open: hit her hard on the next turn.',")
p.save()
