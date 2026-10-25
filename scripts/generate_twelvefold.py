"""The Twelvefold Scar: symmetric twelve-start land skirmish with cliff terraces."""
from pathlib import Path
import json
import math
import struct
ROOT=Path(__file__).resolve().parents[1]
SIZE=256
CLIFFS=set(range(200,216))|{112,113}
STARTS=[]
for quarter in range(4):
 for initial in [(128,27),(178,40),(215,78)]:
  x,y=initial
  for _ in range(quarter):x,y=256-y,x
  STARTS.append((x,y))
BLOCKING={'sf_cottage':(2,2),'sf_townhouse':(2,2),'sf_oak':(1,1),'sf_pine':(1,1),'sf_deadtree':(1,1),'sf_burntree':(1,1),'sf_bridge_post':(1,1)}

def line(a,b):
 n=max(abs(a[0]-b[0]),abs(a[1]-b[1]))
 return {(round(a[0]+(b[0]-a[0])*i/max(1,n)),round(a[1]+(b[1]-a[1])*i/max(1,n))) for i in range(n+1)}

def layout():
 tiles={(x,y):(255,(x*7+y*11)%16) for x in range(SIZE) for y in range(SIZE)}
 resources={};actors=[];roads=set();cliffs=set();terraces={}
 def paint_path(a,b,width=1,tile=105):
  for x,y in line(a,b):
   for dx in range(-width,width+1):
    for dy in range(-width,width+1):
     q=(x+dx,y+dy)
     # Broad roads use solid gravel, rather than repeating narrow lane markings
     # across their width (which produced disconnected stripes in the live view).
     if 1<=q[0]<255 and 1<=q[1]<255:tiles[q]=(217,0);roads.add(q)
 # Lowland biomes use all four authored ground families and gravel/path variants.
 for x in range(1,255):
  for y in range(1,255):
   v=((x//17)+(y//17)*3)%4
   if (x*13+y*7)%11<7:tiles[x,y]=(100+v,0)
 # Wide orbital routes remain outside the central rivers and inside the bases.
 nodes=[]
 for cx,cy in STARTS:
  dx,dy=cx-128,cy-128;r=math.hypot(dx,dy)
  nodes.append((round(128+dx/r*72),round(128+dy/r*72)))
 for i in range(12):paint_path(nodes[i],nodes[(i+1)%12],1,116+i%3)
 def plateau(x0,y0,x1,y1,gates,level=1):
  for x in range(x0+1,x1):
   for y in range(y0+1,y1):tiles[x,y]=(216,0);terraces[x,y]=level
  for x in range(x0,x1+1):
   for y,frame in [(y0,0),(y1,2)]:tiles[x,y]=(200+frame,0);cliffs.add((x,y))
  for y in range(y0,y1+1):
   for x,frame in [(x0,3),(x1,1)]:tiles[x,y]=(200+frame,0);cliffs.add((x,y))
  for x,y,frame in [(x0,y0,4),(x1,y0,5),(x1,y1,6),(x0,y1,7)]:tiles[x,y]=(200+frame,0)
  for side,c in gates:
   for d in range(-3,4):
    q=(c+d,y0 if side=='n' else y1) if side in ('n','s') else (x0 if side=='w' else x1,c+d)
    tiles[q]=(217,0);roads.add(q);cliffs.discard(q)
 # Every player has the same clear deployment zone, plateau dimensions and deposits.
 for i,(cx,cy) in enumerate(STARTS):
  plateau(cx-16,cy-16,cx+16,cy+16,[('n',cx),('s',cx),('e',cy),('w',cy)])
  paint_path((cx-16,cy),(cx+16,cy),1,104)
  paint_path((cx,cy-16),(cx,cy+16),1,104)
  dx,dy=cx-128,cy-128
  if abs(dx)>abs(dy):end=(cx-19*(1 if dx>0 else -1),cy)
  else:end=(cx,cy-19*(1 if dy>0 else -1))
  paint_path((cx,cy),end,1,104);paint_path(end,nodes[i],1,120)
  for ox in (-9,9):
   for dx in range(ox-3,ox+4):
    for dy in range(4,11):
     if (dx-ox)**2+(dy-7)**2<=9:
      rx,ry=dx,dy
      for _ in range(i//3):rx,ry=-ry,rx
      resources[cx+rx,cy+ry]=(1,12)
  dx,dy=cx-128,cy-128
  r=math.hypot(dx,dy);ex,ey=round(128+dx/r*60),round(128+dy/r*60)
  for x in range(ex-4,ex+5):
   for y in range(ey-4,ey+5):
    if (x-ex)**2+(y-ey)**2<=16:resources[x,y]=(1,12)
  actors.append((f'Spawn{i+1}','mpspawn',cx,cy))
 # A second tier of scarred central high ground, split by two canals.
 plateau(98,98,158,158,[('n',107),('n',148),('s',107),('s',148),('w',107),('w',148),('e',107),('e',148)],2)
 for x in range(84,173):
  for y in range(127,130):tiles[x,y]=(1,0);cliffs.discard((x,y));roads.discard((x,y))
 for y in range(84,173):
  for x in range(127,130):tiles[x,y]=(1,0);cliffs.discard((x,y));roads.discard((x,y))
 # Four crossings form a cycle, with ordinary land routes around the canal ends.
 for y in (107,148):
  paint_path((92,y),(125,y),1,105);paint_path((131,y),(164,y),1,105)
  actors += [(f'EW{y}','sf_bridge_ew',127,y),(f'EW{y}West','sf_bridge_post',126,y-1),(f'EW{y}East','sf_bridge_post',130,y+1)]
 for x in (107,148):
  paint_path((x,92),(x,125),1,105);paint_path((x,131),(x,164),1,105)
  actors += [(f'NS{x}','sf_bridge_ns',x,127),(f'NS{x}North','sf_bridge_post',x-1,126),(f'NS{x}South','sf_bridge_post',x+1,130)]
 # Connect each central approach to the orbital road without severing ledges.
 for a,b in [((107,92),(107,60)),((148,92),(148,60)),((107,164),(107,196)),((148,164),(148,196)),((92,107),(60,107)),((92,148),(60,148)),((164,107),(196,107)),((164,148),(196,148))]:paint_path(a,b,1,121)
 # Central enriched fields stay clear of the bridges and their repair approaches.
 for cx,cy in [(116,116),(140,116),(116,140),(140,140)]:
  for x in range(cx-3,cx+4):
   for y in range(cy-3,cy+4):
    if (x-cx)**2+(y-cy)**2<=9:resources[x,y]=(2,3)
 # Symmetric settlements, forest mixes and eroded outcrops use all environment props.
 for quadrant,(cx,cy) in enumerate([(90,90),(166,90),(166,166),(90,166)]):
  for j,(dx,dy) in enumerate([(-3,-3),(2,1)]):actors.append((f'Village{quadrant}_{j}','sf_cottage' if j==0 else 'sf_townhouse',cx+dx,cy+dy))
  for j in range(12):
   x=cx-8+(j%4)*3;y=cy+6+(j//4)*3
   if (x,y) not in roads and (x,y) not in resources:actors.append((f'Grove{quadrant}_{j}',['sf_oak','sf_pine','sf_deadtree','sf_burntree'][j%4],x,y))
 # Remote ridges expose every authored junction/erosion variant, without choking routes.
 for quarter in range(4):
  for i in range(16):
   x=5+i%8;y=4+i//8
   for _ in range(quarter):x,y=256-y,x
   tiles[x,y]=(200+i,0);cliffs.add((x,y))
 # Never allow road carving or water to accidentally erase a claimed barrier cell.
 cliffs={q for q,v in tiles.items() if v[0] in CLIFFS}
 return tiles,actors,resources,cliffs,terraces

def write_map(folder,players=12,title='The Twelvefold Scar'):
 tiles,actors,resources,cliffs,terraces=layout();folder.mkdir(parents=True,exist_ok=True)
 data=bytearray(struct.pack('<BHHIII',2,SIZE,SIZE,17,0,17+SIZE*SIZE*3))
 for x in range(SIZE):
  for y in range(SIZE):data.extend(struct.pack('<HB',*tiles[x,y]))
 for x in range(SIZE):
  for y in range(SIZE):data.extend(bytes(resources.get((x,y),(0,0))))
 (folder/'map.bin').write_bytes(data)
 lines=['MapFormat: 12','RequiresMod: sevenfall','Title: '+title,'Author: Sevenfall contributors','Tileset: TEMPERAT',f'MapSize: {SIZE},{SIZE}','Bounds: 1,1,254,254','Visibility: Lobby','Categories: Conquest','Players:','\tPlayerReference@Neutral:','\t\tName: Neutral','\t\tOwnsWorld: True','\t\tNonCombatant: True','\t\tFaction: h_bastion']
 for i in range(players):lines.extend([f'\tPlayerReference@Multi{i}:',f'\t\tName: Multi{i}','\t\tPlayable: True','\t\tFaction: Random'])
 lines.append('Actors:')
 for name,kind,x,y in actors:lines.extend([f'\t{name}: {kind}','\t\tOwner: Neutral',f'\t\tLocation: {x},{y}'])
 (folder/'map.yaml').write_text('\n'.join(lines)+'\n',encoding='utf-8')
 summary={'schema':1,'name':title,'size':SIZE,'players':players,'starts':STARTS,'cliff_cells':len(cliffs),'resource_cells':len(resources),'starting_ore_credits_each':20880,'bridges':4,'topography':'Visual raised terraces on the rectangular grid; cliffs use native impassable Rock. No height-based combat bonus.'}
 (ROOT/'art/terrain/twelvefold-layout.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
 return summary

def main():print(json.dumps(write_map(ROOT/'mods/sevenfall/maps/twelvefold-scar')))
if __name__=='__main__':main()
