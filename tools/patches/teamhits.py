"""Make team-wide boss hits fair (audit P1).

- Cap: a hit that strikes the whole team can't knock out anyone who was at 40% HP or more
  when it landed; they hold on at 1 HP. Ch 7 is excluded (a fight you are meant to lose).
- Ch 3: the frenzy follow-up no longer lands on the same turn as Tail Sweep.
- Ch 24: a shield on anyone halves Crown Barrage for the whole team.
"""
import re, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from patch import Patch
p = Patch(); rep = p.rep

# Helper, defined next to damageKid
rep("function damageKid(k,dmg){\n  if(!k||k.down)return;\n",
"""// Team-wide hits: anyone at 40% HP or more when the hit lands holds on at 1 HP.
function teamHit(f){const L=activeAlive();S.aoeHp=new Map(S.roster.map(k=>[k,k.hp/k.hpMax]));try{L.forEach(f)}finally{S.aoeHp=null}}
function damageKid(k,dmg){
  if(!k||k.down)return;
""")
# Apply the cap right before the existing knockout checks
rep("  dmg=Math.max(1,Math.round(dmg*mult));k.barrier=false;\n",
"""  dmg=Math.max(1,Math.round(dmg*mult));k.barrier=false;
  if(S.aoeHp&&k.hp-dmg<=0&&(S.aoeHp.get(k)||0)>=.4){dmg=k.hp-1;floatText(...kidCenter(k),'Hold on!','#ffe8a0');log(`${k.name} holds on!`)}
""")

# Route every team-wide hit through teamHit, except Ch 7
s = p.s
pat = re.compile(r"activeAlive\(\)\.forEach\((\w)=>(\{?)damageKid")
out, last, n = [], 0, 0
for m in pat.finditer(s):
    j = s.rfind("{key:'", 0, m.start())
    if s.startswith("{key:'ch7'", j):
        continue
    out.append(s[last:m.start()]); out.append(f"teamHit({m.group(1)}=>{m.group(2)}damageKid"); last = m.end(); n += 1
out.append(s[last:]); p.s = ''.join(out)
assert n == 25, n
print('team-wide hits routed:', n)

# Ch 3: no frenzy on a Tail Sweep turn
rep("  if(b.tail>=3){b.tail=0;log('Tail Sweep!');await bossDash(b);teamHit(k=>damageKid(k,9+rnd(3)))}\n  else{const t=pickTarget();if(t){log(`Captain Chomp bites ${t.name}!`);await lunge(b,-1);damageKid(t,13+rnd(4))}}\n  if(b.frenzy&&activeAlive().length){",
    "  let swept=false;\n  if(b.tail>=3){b.tail=0;swept=true;log('Tail Sweep!');await bossDash(b);teamHit(k=>damageKid(k,9+rnd(3)))}\n  else{const t=pickTarget();if(t){log(`Captain Chomp bites ${t.name}!`);await lunge(b,-1);damageKid(t,13+rnd(4))}}\n  if(b.frenzy&&!swept&&activeAlive().length){")

# Ch 24: a shield on anyone halves Crown Barrage
rep("if(b.shards>=4&&b.cycle%2===0){log(`CROWN BARRAGE! ${b.shards} stolen stones fire at once.`);await bossDash(b);teamHit(p=>damageKid(p,2*b.shards+2));b.shards=1}",
    "if(b.shards>=4&&b.cycle%2===0){log(`CROWN BARRAGE! ${b.shards} stolen stones fire at once.`);await bossDash(b);const sh=activeAlive().find(p=>p.barrier||p.veil||p.guard>0);if(sh){log(`${sh.name}'s shield breaks the barrage! It hits everyone at half power.`);floatText(...kidCenter(sh),'Barrage broken','#9fc0ff')}teamHit(p=>damageKid(p,Math.round((2*b.shards+2)*(sh?.5:1))));b.shards=1}")
rep("return 'CROWN BARRAGE: every stolen stone fires'", "return 'CROWN BARRAGE: every stolen stone fires (a shield on anyone halves it)'")
rep("Starfall Blade shatters 2 shards. Phase 2:", "Starfall Blade shatters 2 shards. A shield on anyone halves Crown Barrage. Phase 2:")
rep("ch27:b=>b&&b.phase===2?'Only light and magic hurt the Unmade. Let Joseph and Josh protect the team.':'Use Starfall Blade on the crown. Every shard you break weakens his shield.'",
    "ch27:b=>b&&b.phase===2?'Only light and magic hurt the Unmade. Let Joseph and Josh protect the team.':'Shield someone before Crown Barrage, and use Starfall Blade on the crown.'")
# Ch 3 retry tip still right; Ch 18 phase 2 is covered by the cap.
p.save()
