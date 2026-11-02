"""Expansion coverage, asset provenance and selectable-faction boundaries."""
import hashlib
import json
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from additional_realms_data import REALMS,UNITS,STRUCTURES
from build_new_realms import blocks

class AdditionalRealmContracts(unittest.TestCase):
 def test_four_independent_choices_and_hidden_campaign_faction(self):
  actors=blocks((ROOT/'mods/sevenfall/rules/80-additional-realms.yaml').read_text())
  world=actors['^BaseWorld']
  self.assertEqual(world.count('\tFaction@'),5) # four + random override
  self.assertIn('Selectable: False',world)
  pool=world.split('RandomFactionMembers: ')[1].splitlines()[0]
  self.assertNotIn('v_veilborn',pool)
  for p,r in REALMS.items():
   self.assertIn(r['faction'],actors['World'])
   self.assertIn('~sf.'+r['family'],actors[(p+'_rifleman').upper()])
   if p!='v':self.assertIn(r['faction'],pool)
 def test_every_role_has_own_painted_art_and_preserved_sources(self):
  manifest=json.loads((ROOT/'art/additional-realms/painted-manifest.json').read_text())
  byid={x['id']:x for x in manifest}
  self.assertEqual(len(byid),94)
  for p in REALMS:
   for role in STRUCTURES+['yard','mcv']+[u[0] for u in UNITS[p]]:self.assertIn(p+'_'+role,byid)
  for a in manifest:
   self.assertEqual(hashlib.sha256((ROOT/a['file']).read_bytes()).hexdigest(),a['sha256'])
   self.assertEqual(hashlib.sha256((ROOT/a['source']).read_bytes()).hexdigest(),a['sourceSha256'])
   self.assertEqual(a['authoredFrames'],32 if a['kind']=='unit' else 6)
   self.assertTrue((ROOT/'docs/assets/additional-realms'/f"{a['id']}.webp").is_file())
 def test_site_roster_and_no_new_subfactions(self):
  records=json.loads((ROOT/'docs/roster.json').read_text())
  self.assertEqual(len(records),275)
  self.assertEqual(sum(r['kind']=='units' for r in records),117)
  for realm in REALMS.values():
   rows=[r for r in records if r['faction']==realm['family']]
   self.assertGreaterEqual(len(rows),23)
   self.assertEqual({r['subfaction'] for r in rows},{'shared'})
   self.assertTrue((ROOT/'docs/assets/roster'/f"{realm['family']}-emblem.webp").is_file())
 def test_campaign_enclaves_are_non_player(self):
  for name in ['h03-glass-fields','a03-glass-wrath','d02-seeds-ruin']:
   path=ROOT/'mods/sevenfall/maps'/name
   text=(path/'map.yaml').read_text()
   self.assertIn('enclave.lua',text)
   for section in text.split('PlayerReference@Enclave')[1:]:
    section=section.split('PlayerReference@')[0].split('Actors:')[0]
    self.assertNotIn('Playable: True',section)
   self.assertIn('AddSecondaryObjective',(path/'enclave.lua').read_text())

if __name__=='__main__':unittest.main()
