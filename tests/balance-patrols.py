import os
GAME='file://'+os.path.abspath(os.environ.get('GAME') or os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','src','meteorite-kids-battle.html'))
import json, sys
from playwright.sync_api import sync_playwright
N=int(sys.argv[1]) if len(sys.argv)>1 else 6
KEYS=sys.argv[2].split(',')
TUNE=json.loads(sys.argv[3]) if len(sys.argv)>3 else {}
PROFS=sys.argv[4].split(',') if len(sys.argv)>4 else ['story']
DIFFS=sys.argv[5] if len(sys.argv)>5 else 'story'
JS=r"""
async (args)=>{
 const [key,prof,N,TU,DF]=args;Object.keys(DMG_TUNE).forEach(k=>delete DMG_TUNE[k]);Object.assign(DMG_TUNE,TU);DIFF=DF;
 window.awardRewards=async()=>{};window.playCutscene=async()=>{};window.showResult=()=>{};window.startEpilogue=async()=>{};
 const C=CHAPTERS.find(c=>c.key===key);window.enterHub=()=>{};
 const out=[];
 for(let n=0;n<N;n++){
  // profile setup
  for(const k in progress)delete progress[k];
  const E=expectedLevel(C);const st=storyOrder();const idx=st.indexOf(key);st.slice(0,idx).forEach(k=>progress[k]=true);['scareth','kaytahn','thornforge','nightshade'].forEach(i=>progress['mv_'+i]=true);
  const q=P();const lv={story:E,some:E+1,lots:E+3}[prof];
  HERO_IDS.forEach(id=>{q.party.lv[id]=lv;const m=lv-1;q.party.bonus[id]={hp:Math.round(8*m/3),atk:Math.round(2*m/3),mag:Math.round(2*m/3)}});
  q.items=prof==='story'?{juice:2,granola:0,bandaid:0,marble:0}:prof==='some'?{juice:3,granola:1,bandaid:1,marble:0}:{juice:3,granola:3,bandaid:3,marble:3};
  const g=G();HERO_IDS.forEach(id=>{g.gear[id]={w:prof==='story'?0:prof==='some'?1:2,o:prof==='story'?0:prof==='some'?1:2,c:null}});
  if(prof==='lots'){g.gear.lightheart.c='spark';g.gear.scareth.c='cool';g.gear.kaytahn.c='ward';g.gear.thornforge.c='lantern';g.gear.nightshade.c='echo'}
  window.__res=null;
  const _w=win,_l=lose;
  window.win=function(){_w();if(S.over&&!window.__res)window.__res='win'};
  window.lose=function(){_l();if(!window.__res)window.__res='lose'};
  window.chooseAction=k=>{
   const A=actionsFor(k).filter(a=>!a.disabled);const lab=a=>a.label;
   const find=l=>A.find(a=>lab(a).startsWith(l));
   const pick=x=>Promise.resolve(x);
   if(find('Meteor Strike'))return pick(find('Meteor Strike'));
   const team=S.roster.filter(p=>kidPos(p));const hurt=team.filter(p=>!p.down&&p.hp/p.hpMax<.4);const down=team.some(p=>p.down);
   const mend=find('Mend');if(mend&&(down||hurt.length))return pick(mend);
   if(hurt.length&&find('Crest Barrier'))return pick(find('Crest Barrier'));
   const item=find('Item');if(item&&(hurt.length||down)&&Math.random()<.6){const s=item.sub.filter(x=>!x.disabled);const j=s.find(x=>x.label.startsWith(down?'Band-Aid':'Juice'))||s.find(x=>x.label.startsWith('Juice'));if(j)return pick(j)}
   if(find('Focus')&&S.boss.hp>S.boss.hpMax*.15&&Math.random()<.7)return pick(find('Focus'));
   if(find('Morph')&&S.boss.hp>S.boss.hpMax*.15)return pick(find('Morph'));
   const rest=A.filter(a=>!['Swap','Item','Morph'].includes(lab(a))&&a.run);
   return pick(rest[Math.floor(Math.random()*rest.length)]||A[0]);
  };
  HUB.age='adult';HUB.down=new Set();startPatrol({z:WISP_ZONES[0],x:0,y:0,dir:1},false);
  let t=0;while(!window.__res&&S.round<45&&t<6000){await new Promise(r=>setTimeout(r,0));t++}
  const alive=S.roster.filter(p=>!p.down).length;
  out.push({r:window.__res||'stall',rounds:S.round,alive,hpLeft:(()=>{const J=S.roster.find(p=>p.seraph);return J?Math.round(100*J.hp/J.hpMax):Math.round(100*S.roster.reduce((a,p)=>a+p.hp,0)/S.roster.reduce((a,p)=>a+p.hpMax,0))})()});
  window.win=_w;window.lose=_l;S.over=true;await new Promise(r=>setTimeout(r,0));
 }
 return out;
}
"""
res={}
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page()
    pg.route("**/fonts.googleapis.com/**", lambda r: r.abort())
    pg.add_init_script("const _st=window.setTimeout;window.setTimeout=(f,ms)=>_st(f,0);")
    errs=[];pg.on("pageerror",lambda e:errs.append(str(e)))
    pg.goto(GAME);pg.wait_for_timeout(500)
    pg.evaluate("TITLE.active=false")
    for key in KEYS:
        for prof in PROFS:
            o=pg.evaluate(JS,[key,prof,N,TUNE,DIFFS])
            w=sum(1 for x in o if x['r']=='win');rr=[x['rounds'] for x in o if x['r']=='win']
            res[(key,prof)]=(w,len(o),sum(rr)/len(rr) if rr else 0,(sum(x['hpLeft'] for x in o if x['r']=='win')/max(1,w)))
            print(f"{key:6} {prof:5} {DIFFS} T{TUNE.get(key,1)} win {w}/{len(o)}  rounds {res[(key,prof)][2]:.1f}  hpLeft {res[(key,prof)][3]:.0f}%",flush=True)
    print("ERR",errs[:5])
    b.close()
