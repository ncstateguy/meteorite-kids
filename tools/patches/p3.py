"""Audit P3s: long boss names fit, a Combo! callout, clear online-service messages, rename 'Blood in the Water'."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from patch import Patch
p = Patch(); rep = p.rep

# 1. Long boss names wrap (and shrink a little) instead of being cut off
rep("""cards.push(`<div class="card"><div class="nm">${BN()}<small>${C.key==='patrol'?'Enemy':'Boss'}</small></div>""",
    """cards.push(`<div class="card"><div class="nm"><span class="bossnm${BN().length>16?' long':''}">${BN()}</span><small>${C.key==='patrol'?'Enemy':'Boss'}</small></div>""")
rep("#rotHint{display:none;", ".card .nm .bossnm{white-space:normal!important;line-height:1.15;min-width:0;overflow-wrap:anywhere}.card .nm .bossnm.long{font-size:11px!important}#rotHint{display:none;")  # outside the phone-only media block

# 2. Combo! when a friend's setup makes the hit land harder
rep("""  let dmg=base*(phys&&k.disarmed?.5:1)*(k.temper&&phys?1.6:1)""",
    """  const combo=[];if(k.temper&&phys&&k.id!=='thornforge')combo.push(`${KIDS.thornforge.name}'s Temper`);if(b.hex>0&&k.id!=='nightshade')combo.push(`${KIDS.nightshade.name}'s hex`);if(b.vuln>1)combo.push('the opening');
  let dmg=base*(phys&&k.disarmed?.5:1)*(k.temper&&phys?1.6:1)""")
rep("""  floatText(BOSS_C[0],BOSS_C[1]-14,dmg,'#fff');log(`${k.name} ${m.label||'hits'} ${BN()} for ${dmg}.`);""",
    """  floatText(BOSS_C[0],BOSS_C[1]-14,dmg,'#fff');log(`${k.name} ${m.label||'hits'} ${BN()} for ${dmg}.`);
  if(combo.length){floatText(BOSS_C[0],BOSS_C[1]-40,'COMBO!','#ffd76a');log(`Combo! ${andList(combo)} made ${k.name}'s hit land harder.`);
    if((progress.comboTips|0)<3){progress.comboTips=(progress.comboTips|0)+1;saveProgress();battleCap(`Combo! ${andList(combo)} made that hit land harder. Set each other up.`)}}""")

# 3. Online: clear messages when the online service doesn't answer or drops
rep("""      p.on('open',()=>{this.peer=p;this.host=true;""",
    """      p.on('open',()=>{if(this.host&&this.peer===p){this.status('Reconnected to the online service.');return}clearTimeout(this.wd);this.peer=p;this.host=true;""")
rep("""else if(!this.host)this.status("Couldn't reach the matchmaking server. Try again in a minute.",true)});
      p.on('connection',c=>this.addGuest(c))};
    open(0)},""",
    """else if(!this.host)this.status("Couldn't reach the matchmaking server. Try again in a minute.",true);
        else if(['network','server-error','socket-error','socket-closed'].includes(e.type))this.status("Lost touch with the online service. Players already here can keep playing; new players can't join until it comes back.",true)});
      p.on('disconnected',()=>{if(this.host&&this.peer===p){this.status("Lost touch with the online service. Reconnecting...",true);setTimeout(()=>{try{if(!p.destroyed)p.reconnect()}catch(e){}},2000)}});
      p.on('connection',c=>this.addGuest(c))};
    open(0);clearTimeout(this.wd);this.wd=setTimeout(()=>{if(!this.host)this.status("Couldn't reach the online service. It may be busy or down. Try again in a few minutes.",true)},12000)},""")
rep("""      c.on('close',()=>this.hostLeft());})},""",
    """      c.on('close',()=>this.hostLeft());});
    clearTimeout(this.wd);this.wd=setTimeout(()=>{if(!this.guest)this.status(`Couldn't connect to room ${code}. Check the code with your host. If it's right, the online service may be down; try again in a few minutes.`,true)},15000)},""")

# 4. Rename Captain Chomp's frenzy
rep("tip:'Blood in the Water: if anyone is below half HP,", "tip:'Feeding Frenzy: if anyone is below half HP,")
rep("log('Blood in the Water! He frenzies and strikes again.');", "log('Feeding Frenzy! He strikes again.');")
rep("Blood in the water, mateys!", "Feeding frenzy, mateys!")
rep("'Smells blood':'Circling'", "'Smells weakness':'Circling'")
p.save()
