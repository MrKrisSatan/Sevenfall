import hashlib
import importlib.util
from pathlib import Path
import re
import unittest
import json
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('realms',ROOT/'scripts/build_new_realms.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class NewRealmContracts(unittest.TestCase):
 def test_eight_selections_have_isolated_tech_and_two_unique_units(self):
  rules=(m.MOD/'rules/65-new-realms.yaml').read_text()
  actors=m.blocks(rules)
  for f in m.FACTIONS:
   units=[u for u in m.UNITS if u[0]==f[0]]
   self.assertEqual(len(units),2)
   for u in units:
    b=actors[u[1].upper()]
    self.assertIn('~sf.'+f[0],b)
    self.assertIn('Weapon: SF_'+u[1],b)
    self.assertIn('Image: '+u[1],b)
  for prefix,(family,old,oldfamily,names) in m.FAMILIES.items():
   for suffix in names:
    b=actors[(prefix+'_'+suffix).upper()]
    self.assertIn('~sf.'+family,b)
    self.assertNotIn('~sf.'+oldfamily,b)
   refinery=actors[(prefix+'_veilworks').upper()]
   self.assertIn('Actor: '+prefix+('_harvester' if prefix=='i' else '_gatherer'),refinery)
 def test_all_new_choices_have_start_gates_and_huds(self):
  factions=(m.MOD/'rules/10-factions.yaml').read_text()
  metrics=(m.MOD/'metrics.yaml').read_text()
  pool=re.search(r'RandomFactionMembers: (.+)',factions)[1].split(', ')
  self.assertEqual(len(pool),20)
  for fid,*_ in m.FACTIONS:
   self.assertIn(fid,pool)
   self.assertIn('Prerequisite: sf.'+fid,factions)
   self.assertIn('FactionSuffix-'+fid+': '+('machine' if fid[0]=='i' else 'fallen'),metrics)
 def test_exclusive_sprites_are_hashed_and_have_64_frames(self):
  manifest=json.loads((ROOT/'art/new-realms/manifest.json').read_text())
  self.assertEqual(len(manifest),16)
  for a in manifest:
   png=(m.MOD/'art/new-realms'/(a['id']+'.png')).read_bytes()
   self.assertEqual(hashlib.sha256(png).hexdigest(),a['sha256'])
   self.assertIn(b'FrameAmount\x0064',png)
   self.assertIn(b'FrameSize\x0072,72',png)
 def test_economy_is_excluded_from_combat_doctrines(self):
  src=(ROOT/'code/OpenRA.Mods.Sevenfall/FactionIdentity.cs').read_text()
  self.assertIn('!self.Info.HasTraitInfo<ArmamentInfo>()',src)
  for f in m.FACTIONS:self.assertIn('case "'+f[0]+'"',src)
