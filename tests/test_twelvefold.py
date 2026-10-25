"""Twelve-player map connectivity, barrier and economy regression contracts."""
from collections import deque,Counter
import importlib.util
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('twelvefold',ROOT/'scripts/generate_twelvefold.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class TwelvefoldTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.tiles,cls.actors,cls.resources,cls.cliffs,cls.terraces=m.layout()
 def reachable(self,bridges=True,avoid_resources=True):
  blocked={q for q,v in self.tiles.items() if v[0] in m.CLIFFS or v[0]==1}
  for _,kind,x,y in self.actors:
   if bridges and kind in ('sf_bridge_ew','sf_bridge_ns'):
    for i in range(3):blocked.discard((x+i,y) if kind.endswith('ew') else (x,y+i))
   if kind in m.BLOCKING:
    w,h=m.BLOCKING[kind];blocked.update((x+dx,y+dy) for dx in range(w) for dy in range(h))
  if avoid_resources:blocked.update(self.resources)
  seen={m.STARTS[0]};queue=deque(seen)
  while queue:
   x,y=queue.popleft()
   for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
    q=x+dx,y+dy
    if q not in seen and q not in blocked and 1<=q[0]<255 and 1<=q[1]<255:seen.add(q);queue.append(q)
  return seen
 def test_twelve_unique_clear_starts(self):
  self.assertEqual(len(set(m.STARTS)),12)
  for cx,cy in m.STARTS:
   for x in range(cx-4,cx+5):
    for y in range(cy-4,cy+5):
     self.assertNotIn((x,y),self.resources)
     self.assertNotIn(self.tiles[x,y][0],m.CLIFFS|{1})
 def test_every_start_connected_without_crossing_resources(self):
  self.assertTrue(set(m.STARTS)<=self.reachable())
 def test_all_starts_still_connected_after_all_bridges_collapse(self):
  self.assertTrue(set(m.STARTS)<=self.reachable(False))
 def test_equal_starting_resources_and_accessible_deposits(self):
  for cx,cy in m.STARTS:
   own={q:v for q,v in self.resources.items() if abs(q[0]-cx)<15 and abs(q[1]-cy)<15}
   self.assertEqual(sum(30*v[1] for v in own.values()),20880)
   self.assertEqual(len(own),58)
  self.assertEqual(len(self.resources),12*58+12*49+4*29)
  self.assertTrue(set(self.resources)<=self.reachable(avoid_resources=False))
 def test_resources_are_clear_of_cliffs_water_and_props(self):
  occupied=set()
  for _,kind,x,y in self.actors:
   if kind in m.BLOCKING:
    w,h=m.BLOCKING[kind];occupied.update((x+dx,y+dy) for dx in range(w) for dy in range(h))
  self.assertFalse(set(self.resources)&occupied)
  for q in self.resources:self.assertNotIn(self.tiles[q][0],m.CLIFFS|{1})
 def test_all_environment_families_and_both_minerals_are_used(self):
  kinds=Counter(a[1] for a in self.actors)
  for kind in m.BLOCKING:self.assertGreater(kinds[kind],0)
  self.assertEqual(kinds['sf_bridge_ew'],2);self.assertEqual(kinds['sf_bridge_ns'],2)
  self.assertEqual({v[0] for v in self.resources.values()},{1,2})
  self.assertTrue(set(range(200,216)) <= {v[0] for v in self.tiles.values()})
 def test_bridge_tiles_are_water_and_cliffs_have_distinct_upper_surfaces(self):
  for _,kind,x,y in self.actors:
   if kind in ('sf_bridge_ew','sf_bridge_ns'):
    for i in range(3):self.assertEqual(self.tiles[(x+i,y) if kind.endswith('ew') else (x,y+i)][0],1)
  self.assertEqual(set(self.terraces.values()),{1,2})
  self.assertGreater(len(self.cliffs),1000)
if __name__=='__main__':unittest.main()
