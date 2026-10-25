"""Faction access, AI and generator contracts; native identity-test proves effects."""
import sys
from pathlib import Path
import re
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_faction_identities import FACTIONS, main

class IdentityContracts(unittest.TestCase):
 def test_each_faction_has_two_exclusives_and_its_own_ultimate(self):
  self.assertEqual(len(FACTIONS),12)
  self.assertEqual(len({f[2] for f in FACTIONS}),12)
  self.assertEqual(len({u for f in FACTIONS for u in f[5:7]}),24)
  text=(ROOT/'mods/sevenfall/rules/60-identities.yaml').read_text()
  for f in FACTIONS:
   faction=f[0]
   block=re.search(r'(?ms)^SF_'+faction.upper()+r'_ULTIMATE:\n(.*?)(?=^\S|\Z)',text)[1]
   self.assertIn('~sf.'+faction+',',block)
   self.assertIn('BuildLimit: 1',block)
   self.assertIn('Amount: -150',block)
   self.assertIn('OrderName: SF'+f[2]+'Order',block)
   self.assertIn('ChargeInterval: '+str(f[-1]*25),block)
   self.assertNotIn('StartFullyCharged: True',block)

 def test_bot_can_build_each_exclusive_and_target_every_power(self):
  text=(ROOT/'mods/sevenfall/rules/40-ai.yaml').read_text()+(ROOT/'mods/sevenfall/rules/60-identities.yaml').read_text()
  for f in FACTIONS:
   for unit in f[5:7]:self.assertRegex(text,rf'(?m)^\t\t\t{unit}: \d+$')
   self.assertIn('OrderName: SF'+f[2]+'Order',text)
  for kind in ('Sanctuary','Rebellion','Relief','Covenant','Bloodtide'):
   block=text.split('\t\t\t'+kind+':')[1].split('\t\t\t\n')[0]
   self.assertIn('Against: Ally',block)

 def test_generation_is_reproducible(self):
  paths=[ROOT/'mods/sevenfall'/p for p in ('rules/60-identities.yaml','weapons/identities.yaml','fluent/identities.ftl','fluent/sevenfall.ftl')]
  before=[p.read_bytes() for p in paths]
  main()
  self.assertEqual(before,[p.read_bytes() for p in paths])

 def test_superweapon_regeneration_can_heal_above_half_health(self):
  text=(ROOT/'mods/sevenfall/rules/60-identities.yaml').read_text()
  for condition in ('sanctum','bloodtide'):
   blocks=re.findall(r'(?ms)^\tChangesHealth@IDENTITY_'+condition+r':\n(.*?)(?=^\t[^\t]|\Z)',text)
   self.assertEqual(len(blocks),2)
   for block in blocks:self.assertIn('StartIfBelow: 100',block)

 def test_variant_artwork_matches_its_actual_inherited_body(self):
  from build_site_catalogue import build_records
  records=build_records();byid={r['id']:r for r in records}
  variants=[r for r in records if 'variant_of' in r]
  self.assertEqual(sum(r['kind']=='units' for r in variants),9)
  self.assertEqual(sum(r['kind']=='buildings' for r in variants),12)
  rules=(ROOT/'mods/sevenfall/rules/60-identities.yaml').read_text()
  for record in variants:
   parent=byid[record['variant_of']]
   block=re.search(r'(?ms)^'+record['actor']+r':\n(.*?)(?=^\S|\Z)',rules)[1]
   self.assertIn('\tInherits: '+parent['actor']+'\n',block)
   self.assertEqual(record['source'],parent['source'])
   self.assertEqual(record['art_id'],parent['id'])

if __name__=='__main__':unittest.main()
