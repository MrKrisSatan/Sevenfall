import hashlib
import importlib.util
import json
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('completion',ROOT/'scripts/build_realm_completion.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class RealmCompletionContracts(unittest.TestCase):
 def test_all_families_have_air_beasts_and_shared_powers(self):
  rules=(m.MOD/'rules/75-realm-completion.yaml').read_text()
  factions=(m.MOD/'rules/10-factions.yaml').read_text()
  for p,(family,*_) in m.REALMS.items():
   self.assertIn('Prerequisite: sf.'+family,factions)
   for name in [m.AIR[p][0],m.BEAST[p][0],'cataclysm']:
    self.assertIn((p+'_'+name).upper()+':',rules)
   self.assertIn('~sf.'+family,rules)
  self.assertEqual(len({v[1] for v in m.AIR.values()}),5)
  self.assertEqual(len({v[1] for v in m.BEAST.values()}),5)
 def test_art_provenance_and_required_effect_states(self):
  assets=json.loads((ROOT/'art/realm-completion/painted-manifest.json').read_text())
  self.assertEqual(len(assets),20)
  for a in assets:
   self.assertEqual(hashlib.sha256((ROOT/a['source']).read_bytes()).hexdigest(),a['sourceSha256'])
   self.assertEqual(hashlib.sha256((ROOT/a['file']).read_bytes()).hexdigest(),a['sha256'])
  seq=(m.MOD/'sequences/realm-completion.yaml').read_text()
  for key in ['sf_witness:','sf_nuclear:','\twarning:','\timpact:','\tcrumble:']:self.assertIn(key,seq)
 def test_statue_time_and_counterplay_have_native_assertions(self):
  lua=(m.MOD/'maps/realmcompletion-test/realmcompletion-test.lua').read_text()
  for label in ['statue persists before crumble','salt crumbles even after source loss','destroying source during warning cancels flash','nuclear friendly and neutral damage','outside radius survives']:
   self.assertIn(label,lua)
