"""Crater dungeon (audit P2): three short rooms down into the crater before the Sentinel (Ch 23).

1. Lumoran Wall: Tricia reads the wall and the seal opens (the bridge lines move here from the Ch 23 opening).
2. Sunken Ledge: Lindsey raises the crater pool so the crates float; Josh rebuilds the fallen bridge.
3. Crater Floor: Joseph shadow-steps behind the bars to a gold box with the last Lumora memory;
   the Sentinel's door and a save crystal.
Gold boxes can now hold a page with no charm.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from patch import Patch
p = Patch(); rep = p.rep

AREAS = r"""
// ======== Chapter 23: down into the crater ========
Object.assign(AREAS,{
 cr_wall:{name:'The Crater · Lumoran Wall',short:'the crater wall',ch:'ch23',theme:'mine',tf:{z:'cr_wall'},
  rows:["#########D##########","#pppppppzzzpppppppp#","#..................#","#...r..........r...#","#..................#","#..c...........c...#","#..................#","#..................#","#..................#","#########E##########"],
  spawns:{entry:[9,8,'up'],back:[9,2,'down']},
  intro:()=>[['','A path of loose stones winds down the inside of the crater. Faint purple writing covers the walls.'],['nightshade','Lumoran. The whole wall.']],
  objs:()=>[AEXIT(9,9,'town'),AEXIT(9,0,'cr_pool','fromWall'),PRIZE('cr_c1',17,8,{item:'bandaid'}),
    {type:'runestone',area:true,id:'cr_runes',tx:12,ty:3,name:'Lumoran Wall',power:'hex',sets:'cr_wall',solid:true,hint:'Purple writing covers the wall from top to bottom. A glowing seal blocks the path down.',
     done:[['','Tricia lays her hand on the wall. The writing lights up, one line at a time.'],['nightshade','"The lights were a bridge. Sent to guard this world until it could guard itself."'],['kaytahn','And then give their power away.'],['','The purple seal across the path fades.']]}],
  goal(){return aSt().cr_wall?goalTo('The seal is open. Keep going down.',9,0):goalTo('Lumoran writing covers the wall. Tricia can read it.',12,3)}},
 cr_pool:{name:'The Crater · Sunken Ledge',short:'the sunken ledge',ch:'ch23',theme:'mine',tf:{f:'cr_fill',k:'cr_slab'},
  rows:["#########D##########","#p......c..c......p#","#..................#","#________kk________#","#..................#","#ffffffffffffffffff#","#..................#","#.c..............c.#","#..................#","#########E##########"],
  spawns:{fromWall:[9,8,'up'],back:[9,1,'down']},
  intro:()=>[['','Halfway down, rainwater has pooled across the crater. A crack splits the ledge beyond it.'],['thornforge','There was a bridge here once. Pieces of one, anyway.']],
  objs:()=>[AEXIT(9,9,'cr_wall','back'),AEXIT(9,0,'cr_floor','fromPool'),
    {type:'basin',area:true,id:'cr_basin',tx:4,ty:6,name:'Crater Pool',power:'tide',sets:'cr_fill',solid:true,hint:'The pool sits low in a bed of mud. Broken crates are stuck at the bottom.',
     done:[['','Lindsey lifts her hands. The pool rises, and the crates float up level with the ledge.'],['me:kaytahn','Still got it.']]},
    {type:'repair',area:true,id:'cr_fix',tx:14,ty:4,name:'Fallen Bridge',power:'heave',sets:'cr_slab',solid:true,hint:'The old bridge across the crack has fallen in. The planks are still here.',
     done:[['','Josh drags the planks into place and wedges them tight with a chunk of black glass.'],['me:thornforge','Not my best work. It will hold.']]}],
  goal(){const S2=aSt();return !S2.cr_fill?goalTo('The pool is too low to cross. Lindsey could raise it.',4,6):!S2.cr_slab?goalTo('The bridge across the crack fell in. Josh can fix it.',14,4):goalTo('Keep going down.',9,0)}},
 cr_floor:{name:'The Crater · Crater Floor',short:'the crater floor',ch:'ch23',theme:'mine',
  rows:["####################","#pppppp......pp|...#","#..............|...#","#..............|...#","#..............||||#","#..................#","#..c...........c...#","#..................#","#..................#","#########E##########"],
  spawns:{fromPool:[9,8,'up']},
  intro:()=>[['','The bottom of the crater. Something big is down here, and it is not moving.'],['scareth','Cool. I hate it.']],
  objs:()=>[AEXIT(9,9,'cr_pool','back'),SAVEPT(4,7),GOLD('gold_ch23',17,2,{page:'warden'}),
    {type:'shadow',area:true,id:'cr_sh1',tx:13,ty:3,to:[17,3],name:'Deep Shadow',power:'shadow',hint:'A shadow pools against the bars. Behind them, something gold glints.',done:[['','Joseph slips into the shadow and steps out on the other side of the bars.'],['me:scareth','Still the best at this.']]},
    {type:'shadow',area:true,id:'cr_sh2',tx:16,ty:3,to:[12,3],name:'Deep Shadow',power:'shadow',hint:'The way back out.'},
    BOSSD('ch23',9,1,'The Crater Floor','At the very bottom of the crater, a suit of crimson armor kneels in the dust.','Go down')],
  goal(){return progress.ch23?null:goalTo('Something is waiting at the very bottom.',9,1)}}});
DUNGEONS.ch23={start:'cr_wall',name:'the crater',town:[6,27],enterText:'The crater is quiet. A path of loose stones winds down the inside wall.',againText:'The crater is quiet. Lumoran writing glows faintly on the walls.'};
"""
rep("const siteGoal=(id,hint)=>()=>aSt()[id]?goalTo('Head back to the Relic Road.',9,9):goalTo(hint,9,3);\n",
    "const siteGoal=(id,hint)=>()=>aSt()[id]?goalTo('Head back to the Relic Road.',9,9):goalTo(hint,9,3);\n" + AREAS)

# The last Lumora memory
rep(" mem2:{n:11,part:2,", """ warden:{n:15,part:2,ch:'ch23',where:'the crater',kind:'memory',find:'a sliver of crystal, still warm',title:"Memory: The Warden's Last Note",
  text:['Before the dark reached the tower, the Warden wrote one last message and sealed it inside the crimson light.','"To the five who come after: we held our lights too tightly, and we hid our cracks from each other. Do not. The light was never ours to keep."'],
  react:()=>[['nightshade','Aldric carried this for fifty years and never knew.'],['lightheart','Then we read it for him.']]},
 mem2:{n:11,part:2,""")

# Gold boxes can hold just a page
rep("S2[o.id]=true;if(!p.charms.includes(o.charm))p.charms.push(o.charm);", "S2[o.id]=true;if(o.charm&&!p.charms.includes(o.charm))p.charms.push(o.charm);")
rep("""  await hubSay([['',`Inside the gold box: the ${c.name}! ${c.desc}.`],['','(Only one exists. Give it to someone on the Party screen.)'],['',`Tucked underneath is ${g.find}.`],""",
    """  await hubSay([...(c?[['',`Inside the gold box: the ${c.name}! ${c.desc}.`],['','(Only one exists. Give it to someone on the Party screen.)'],['',`Tucked underneath is ${g.find}.`]]:[['',`Inside the gold box is ${g.find}.`]]),""")

# Town: the crater sign leads into the dungeon; after Ch 23 you can still explore it
rep("    if(!progress.ch23)return exitHubTo(CHAPTERS.find(c=>c.key==='ch23'));",
    "    if(!progress.ch23)return enterDungeon(CHAPTERS.find(c=>c.key==='ch23'),o.name);")
rep("    if(!progress.ch27){const r=await hubChoice('The rift over the crater is open. Go through and face Vorath?',['Go','Not yet']);if(r===0)exitHubTo(CHAPTERS.find(c=>c.key==='ch27'));return}",
    "    if(!progress.ch27){const r=await hubChoice('The rift over the crater is open. Go through and face Vorath?',['Go','Explore the crater','Not yet']);if(r===0)exitHubTo(CHAPTERS.find(c=>c.key==='ch27'));else if(r===1){HUB.down=new Set();goArea('cr_wall','entry')}return}")

# Ch 23 opening: the walk down and the wall lines now happen in the dungeon
rep("""  {fx:'reset'},{bg:'woods',woods:{red:false,crater:true},music:'mystery'},...P3S,{fade:'in',ms:1000},
  {cap:'The crater. This time, they go down.',top:true},
  {say:'nightshade',text:'The walls are covered in Lumoran. "The lights were a bridge. Sent to guard this world until it could guard itself."'},
  {say:'kaytahn',text:'And then give their power away.'},
  {fx:'shake',n:14}""",
    """  {fx:'reset'},{bg:'woods',woods:{red:false,crater:true},music:'mystery'},...P3S,{fade:'in',ms:1000},
  {fx:'shake',n:14}""")
p.save()
