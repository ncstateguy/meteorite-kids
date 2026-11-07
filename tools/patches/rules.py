"""Trim one-off battle rules (audit P1) and add a one-line retry tip on the defeat screen."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from patch import Patch
p = Patch(); rep = p.rep

# ---- 1. Ch 10 Embermaw: no burnout. His heat and water weakness stay. ----
rep("chips(b){return [{t:`Heat ${b.heat}/5`,w:b.heat>=4},{t:'Morphing builds burnout',w:false}]},",
    "chips(b){return [{t:`Heat ${b.heat}/5`,w:b.heat>=4},{t:'Water cools him',o:true}]},")
rep("  activeAlive().forEach(k=>{if(k.powered&&k.burn){log(`${k.name} is burning out!`);damageKid(k,5*k.burn)}else if(k.burn)k.burn--});\n", "")
rep("  if(S.ch.key==='embermaw'){k.burn=(k.burn||0)+1}\n", "")
rep("""  {say:'boss',text:'Morph again, little ones. And again. Burn brighter until you burn out.'},
  {say:'kaytahn',text:"Don't overdo it. Take turns resting!"},
  {cap:'Every morph builds burnout. Rest tired friends on the bench to cool them off.',top:true}]},""",
"""  {say:'boss',text:'Burn brighter, little ones. Let us see who melts first.'},
  {say:'kaytahn',text:"He's heating up. I'll cool him down!"},
  {cap:'His heat climbs every turn. At 5, Cinder Wave hits everyone. Water attacks cool him down.',top:true}]},""")

# ---- 2. Ch 10 Vane: no repeat-hit rule. Plain weakness: magic slips past his armor. ----
rep("""chips(b){return [{t:b.last?`Braced against ${b.last.name}`:'Unbraced',w:!!b.last},{t:'Take turns attacking',o:true}]},""",
    """chips(b){return [{t:'Magic slips past his armor',o:true}]},""")
rep("""onHit(b,k,dmg,m){if(b.last===k){floatText(BOSS_C[0],BOSS_C[1]-30,'Shrugged off','#f4e8a8');sfx('clang');return Math.round(dmg*.2)}b.last=k;return Math.round(dmg*1.15)},""",
    """onHit(b,k,dmg,m){if(m.magic){floatText(BOSS_C[0],BOSS_C[1]-30,'Through the armor','#c8b8ff');return Math.round(dmg*1.4)}return dmg},""")
rep("""  {say:'scareth',text:'Then we hit him together. One after another.'},
  {cap:'Vane shrugs off repeated hits from the same kid. Take turns attacking.',top:true}]},""",
"""  {say:'nightshade',text:'Armor stops fists. Let us see it stop magic.'},
  {cap:'Magic slips past Vane\\'s armor. Kaytahn and Moritania hit him hardest.',top:true}]},""")
rep("Embermaw: every morph builds burnout, so rest kids on the bench. Vane: he shrugs off repeat hits from the same kid, so take turns.",
    "Embermaw: his heat climbs every turn, and water cools him. Vane: magic slips past his armor.")

# ---- 3. Ch 5 Overclock: no Alarm Ring. Wind-up and the Key stay. ----
rep("Strike the Key to unwind him, and stun him if he is fully wound. Alarm Ring adds a turn to everyone\\'s cooldown; Rally Cry and Inspire take it back.",
    "Strike the Key to unwind him, and stun him if he is fully wound.")
rep("init(b){b.wind=0;b.ring=0},draw:drawClock,", "init(b){b.wind=0},draw:drawClock,")
rep("chips(b){return [{t:`Wind ${b.wind}/3`,w:b.wind>=3},{t:`Alarm in ${3-b.ring}`,w:b.ring>=2}]},",
    "chips(b){return [{t:`Wind ${b.wind}/3`,w:b.wind>=3}]},")
rep("""    b.ring++;
    if(b.ring>=3){b.ring=0;log('ALARM RING! Everyone\\'s cooldowns lengthen.');await bossDash(b);activeAlive().forEach(k=>damageKid(k,8+rnd(3)));
      S.roster.forEach(k=>{if(!k.down&&k.cd>0)k.cd=Math.min(6,k.cd+1)})}
    else{const t=pickTarget();if(t){log(`Second Hand slashes ${t.name}.`);await lunge(b,-1);damageKid(t,12+rnd(4))}}""",
"""    {const t=pickTarget();if(t){log(`Second Hand slashes ${t.name}.`);await lunge(b,-1);damageKid(t,12+rnd(4))}}""")
rep(" ch5:b=>b.ring>=2?'Alarm Ring: damage and longer cooldowns':null,\n", " ch5:b=>b.wind>=2?'Fully wound next turn: double speed':null,\n")

# ---- 4. Ch 17 and Ch 18 Herald: the Mace hits hard, no cooldown penalty. ----
rep("Proclamation hits everyone and Humbles the team for two turns. Mace of Judgment adds a turn to a morph cooldown.',",
    "Proclamation hits everyone and Humbles the team for two turns.',")
rep("damageKid(t,14+rnd(4));if(!t.down){if(t.powered){t.powered=Math.max(1,t.powered-1)}else t.cd=(t.cd||0)+1;log(`${t.name}'s stone dims. One more turn to wait.`)}}}",
    "damageKid(t,14+rnd(4))}}")
rep("damageKid(t,14+rnd(4));if(!t.down){if(t.powered){t.powered=Math.max(1,t.powered-1)}else t.cd=(t.cd||0)+1}}}",
    "damageKid(t,14+rnd(4))}}")
rep("'MACE OF JUDGMENT: one kid, plus a cooldown turn'", "'MACE OF JUDGMENT on one kid'")
rep("Humbled, taking more damage for two turns. Mace of Judgment hits hard and adds a turn to a morph cooldown.",
    "Humbled, taking more damage for two turns. Mace of Judgment hits one kid hard.")

# ---- 5. Rest (Ch 15) and Confide (Ch 16) become Check In, the one Part 2 support action. ----
rep("extra(k){return [{label:'Rest',desc:'Catch your breath. Recover a quarter of your HP, and his flames die down.'",
    "extra(k){return [{label:'Check In',desc:'Check in with yourself: catch your breath, recover a quarter of your HP, and his flames die down.'")
rep("The team starts worn out. Rest trades your turn for a quarter of your HP and cools his flames. Every round nobody rests, the flames grow,",
    "The team starts worn out. Check In trades your turn for a quarter of your HP and cools his flames. Every round nobody checks in, the flames grow,")
rep("The team starts worn out. Rest trades your turn for a quarter of your HP and cools his flames. Every round nobody rests, his flames grow.",
    "The team starts worn out. Check In trades your turn for a quarter of your HP and cools his flames. Every round nobody checks in, his flames grow.")
rep("'CINDER WAVE hits everyone (unless someone rests)'", "'CINDER WAVE hits everyone (unless someone checks in)'")
rep("// They start the fight worn down. Rest trades a turn", "// They start the fight worn down. Check In trades a turn")
rep("extra(k){return [{label:'Confide',desc:k.confided?'You already told them':'Tell the team the truth about your stone.",
    "extra(k){return [{label:'Check In',desc:k.confided?'You already told them':'Tell the team the truth about your stone.")
rep("Spend a turn to Confide: your hits land in full, and every confession makes the whole team hit harder. When everyone has confided, the shield shatters.",
    "Spend a turn to Check In and tell the truth: your hits land in full, and every confession makes the whole team hit harder. When everyone has told the truth, the shield shatters.")
rep("Spend a turn to Confide: your hits land in full, and every confession makes the team stronger.",
    "Spend a turn to Check In and tell the truth: your hits land in full, and every confession makes the team stronger.")
rep("'\"I NEED NO ONE\": he hunts the weakest kid who has not confided'", "'\"I NEED NO ONE\": he hunts the weakest kid still hiding a flicker'")

# ---- 6. Ch 18 phase 2: morphing is free. The stones still crack (story), no HP cost. ----
rep("if(S.ch.key==='ch18'&&S.boss&&S.boss.phase===2){const c=Math.round(k.hpMax*.1);k.hp=Math.max(1,k.hp-c);floatText(...kidCenter(k),'-'+c,'#ff8a8a');log(`${k.name}'s stone cracks a little more.`)}",
    "if(S.ch.key==='ch18'&&S.boss&&S.boss.phase===2)log(`${k.name}'s stone cracks a little more.`);")
rep("Phase 2: your stones go past the limit. Morphing has no cooldown but costs HP. Only Meteor",
    "Phase 2: your stones go past the limit. Morphing has no cooldown. Only Meteor")
rep("Phase 2: your stones are past the limit. Morphing has no cooldown, but every morph costs HP. Only Meteor Strike can finish him.",
    "Phase 2: your stones are past the limit. Morphing has no cooldown. Only Meteor Strike can finish him.")

# ---- 7. Retry tip: one short line on the defeat screen, full rules tucked underneath. ----
rep("// Each boss gets the last word when the team goes down.\n",
"""// One short line on the defeat screen: the most likely reason the team went down. Full rules sit under it.
const RETRY={
 dream:'Use a skill, and heal anyone who gets hurt.',
 patrol:'Focus one group until it drops. Fewer Ashlings means fewer pile-ons.',
 ch1:'Swat the Ashlings before five gather. Their CHARGE hits everyone.',
 ch2:'Bowl the pins before he rolls. Save your morphs for when he is dizzy.',
 ch3:'Keep everyone above half HP. Below that, he attacks twice.',
 ch4:'Use Reforge when kids are disarmed. At 4 stolen weapons he overloads, so hit hard then.',
 ch5:'Strike the Key before he is fully wound. If he already is, the Key stuns him.',
 ch6:'Let Moritania break the reflections. Everyone else does half damage while they are up.',
 ch8:'Break the cage right away. Freeing a friend stuns Hart.',
 ch9:'Shield up before its fourth morph, then hit hard while it is down.',
 embermaw:'Cool him with water before his heat reaches 5.',
 vane:'Magic slips past his armor. Let Kaytahn and Moritania lead.',
 ch11:b=>b&&b.phase>=3?'Normal hits heal the shard. Morph three kids at once for Meteor Strike.':'Save your morphs. Only a Meteor Strike breaks the shard at the end.',
 ch13:'Focus right after the MEGAPHONE, then morph on your next turn.',
 ch14:'Help a friend every other turn: heal, shield or Check In. Lonely kids get caged.',
 ch15:'Have someone Check In every round. Each one cools his flames.',
 ch16:'Check In early. Until you tell the truth, his shield throws your hits back.',
 ch17:'Weapons while the Aegis is up, magic while it is down. Watch the chip.',
 ch18a:'Jake can Call the Team. Use it every time it is ready.',
 ch18:b=>b&&b.phase===2?'Morph everyone, then Meteor Strike. Nothing else can finish him.':'Save your big hits for right after the Tithe. He takes 50% more for two turns.',
 ch19:'Hit her hard on the turn right after she Showboats.',
 ch20:'Every third turn the wisps drain everyone. Heal right before it lands.',
 ch21:'Every third turn the wisps drain everyone. Heal first, and save your Stone Echo for a bad moment.',
 ch22:'Pop Bastion\\'s shield with a small hit first, then use your big ones.',
 ch23:'Swap the bench friends in. Every friend has to use their Stone Echo.',
 ch25r:'Hit her hard on the turn right after she Showboats.',
 ch27:b=>b&&b.phase===2?'Only light and magic hurt the Unmade. Let Joseph and Josh protect the team.':'Use Starfall Blade on the crown. Every shard you break weakens his shield.'};
function retryTip(){const c=S.ch,B=S.base||c,r=RETRY[c.key]||RETRY[B.key];return typeof r==='function'?r(S.boss):r}
// Each boss gets the last word when the team goes down.
""")
rep("""<p class="tip"><strong>Tip:</strong> ${B.tip}</p>""",
    """${(()=>{const r=retryTip();return r?`<p class="tip"><strong>Tip:</strong> ${r}</p><details class="tip"><summary>All the rules for this fight</summary>${B.tip}</details>`:`<p class="tip"><strong>Tip:</strong> ${B.tip}</p>`})()}""")

p.save()
