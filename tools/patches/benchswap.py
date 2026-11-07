"""Ch 23: make the bench swap obvious (audit P1).

While a benched friend still owes their Stone Echo, the Swap button glows, names who is waiting,
and moves to the top once the current hero has nothing left to do. A one-time caption appears when
both active friends have used theirs, and the status chips name who is still on the bench.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from patch import Patch
p = Patch(); rep = p.rep

# Glow style for the button
rep(".special{border-color:var(--accent)}",
    ".special{border-color:var(--accent)}.special.pulse{animation:mkpulse 1.1s ease-in-out infinite}@keyframes mkpulse{50%{box-shadow:0 0 0 3px var(--accent),0 0 14px var(--accent)}}")
rep("if(a.special)bt.className='special';", "if(a.special)bt.className='special';if(a.pulse)bt.classList.add('pulse');")

# Helpers: who on the bench still owes an Echo, and a short in-battle caption
rep("function friendActions(k){",
"""const ECHO_IDS=['scareth','kaytahn','thornforge','nightshade'];
function echoWaiting(){if(!S.ch.allEchoWin)return [];const u=S.friendUsed||{};return benchAlive().filter(k=>ECHO_IDS.includes(k.id)&&!u[k.id])}
function andList(a){return a.length<2?a.join(''):a.slice(0,-1).join(', ')+' and '+a[a.length-1]}
function battleCap(text,ms=3800){const c=$('cap');c.textContent=text;c.style.top='16%';c.hidden=false;clearTimeout(battleCap.t);battleCap.t=setTimeout(()=>{if(!CUT.active)c.hidden=true},ms)}
function friendActions(k){""")

# Swap action: glow, name who is waiting, float to the top when this hero is done
rep("""  if(bench.length)A.push({label:'Swap',desc:'Tag in a benched friend (no turn lost)',sub:bench.map(nk=>({label:nk.name,desc:nk.cd?`Cooldown ${nk.cd} · HP ${nk.hp}`:`Ready · HP ${nk.hp}`,swapTo:nk}))});""",
"""  const wait=echoWaiting();
  if(bench.length){const sw={label:'Swap',desc:wait.length?`${andList(wait.map(n=>n.name))} ${wait.length>1?"haven't":"hasn't"} used their Stone Echo yet`:'Tag in a benched friend (no turn lost)',special:wait.length>0,pulse:wait.length>0,
    sub:bench.map(nk=>({label:nk.name,desc:wait.includes(nk)?`Stone Echo ready · HP ${nk.hp}`:nk.cd?`Cooldown ${nk.cd} · HP ${nk.hp}`:`Ready · HP ${nk.hp}`,swapTo:nk,special:wait.includes(nk)}))};
    const done=!ECHO_IDS.includes(k.id)||(S.friendUsed||{})[k.id];
    if(wait.length&&done)A.unshift(sw);else A.push(sw);
    if(wait.length&&!S.benchHint&&activeAlive().filter(p=>ECHO_IDS.includes(p.id)).every(p=>(S.friendUsed||{})[p.id])){S.benchHint=true;
      battleCap(`${andList(wait.map(n=>n.name))} ${wait.length>1?'are':'is'} still on the bench. Swap them in to use their Stone Echo.`)}}""")

# Status chips name who is still waiting
rep("""chips(b){const n=['scareth','kaytahn','thornforge','nightshade'].filter(id=>(S.friendUsed||{})[id]).length;return [{t:`Stone Echoes: ${n} of 4`,o:true},{t:'Blows do nothing',w:true}]},""",
    """chips(b){const n=ECHO_IDS.filter(id=>(S.friendUsed||{})[id]).length,w=echoWaiting();return [{t:`Stone Echoes: ${n} of 4`,o:true},w.length?{t:`On the bench: ${andList(w.map(k=>k.name))}`,w:true}:{t:'Blows do nothing',w:true}]},""")
p.save()

# Follow-up: use real names (adults have no stone powers)
p = Patch(); p.rep("wait.map(n=>n.name)","wait.map(n=>KIDS[n.id].kid)",n=2); p.rep("andList(w.map(k=>k.name))","andList(w.map(k=>KIDS[k.id].kid))"); p.save()
