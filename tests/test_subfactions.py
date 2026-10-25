"""Coverage for additional faction gates and original sprite provenance."""
import hashlib
import json
from pathlib import Path
import re
import struct
import unittest
ROOT=Path(__file__).resolve().parents[1]
class AdditionalSubfactions(unittest.TestCase):
 def test_each_new_faction_has_two_units_and_one_defense(self):
  entries=json.loads((ROOT/'art/subfactions/catalogue.json').read_text(encoding='utf-8'))
  for faction in ['a_desolation','h_area52','d_contempt']:
   own=[e for e in entries if e['faction']==faction]
   self.assertEqual(sorted(e['kind'] for e in own),['building','unit','unit'])
   for e in own:
    rules=(ROOT/'mods/sevenfall/rules/55-subfactions.yaml').read_text(encoding='utf-8')
    block=rules.split(e['id'].upper()+':\n')[1].split('\n\n')[0]
    self.assertIn('~sf.'+faction,block)
    self.assertNotIn('~sf.'+{'a':'a_exile','h':'h_covenant','d':'d_court'}[faction[0]],block)
 def test_new_choices_keep_parent_economy_and_matching_hud(self):
  rules=(ROOT/'mods/sevenfall/rules/10-factions.yaml').read_text(encoding='utf-8')
  pool=re.search(r'RandomFactionMembers: (.+)',rules)[1].split(', ')
  self.assertEqual(len(pool),12)
  self.assertEqual(len(set(pool)),12)
  for faction in ['a_desolation','h_area52','d_contempt']:
   self.assertIn(faction,pool)
   self.assertIn(faction+': '+faction[0]+'_mcv',rules)
   self.assertIn(faction+': '+faction[0]+'_yard',rules)
   self.assertIn('FactionSuffix-'+faction+':',(ROOT/'mods/sevenfall/metrics.yaml').read_text())
 def test_all_new_art_is_original_hashed_and_bound(self):
  assets=json.loads((ROOT/'art/subfactions/manifest.json').read_text())['assets']
  self.assertEqual(len(assets),9)
  sequences=(ROOT/'mods/sevenfall/sequences/subfactions.yaml').read_text()
  for a in assets:
   with self.subTest(actor=a['id']):
    data=(ROOT/a['file']).read_bytes();source=(ROOT/a['source']).read_bytes()
    self.assertEqual(hashlib.sha256(data).hexdigest(),a['sha256'])
    self.assertEqual(hashlib.sha256(source).hexdigest(),a['sourceSha256'])
    self.assertEqual(data[25],6)
    self.assertIn(b'FrameAmount\0'+str(a['frames']).encode(),data)
    w,h=struct.unpack_from('>II',data,16)
    self.assertEqual((w//a['frameSize'])*(h//a['frameSize']),a['frames'])
    self.assertEqual(a['frames'],64 if a['id'] not in ['a_processional','h_containment','d_throne'] else 6)
    self.assertGreaterEqual(len(set(a['frameHashes'])),6)
    self.assertIn('Filename: sevenfall|'+a['file'].split('mods/sevenfall/')[1],sequences)
 def test_janus_protocol_weapons_have_distinct_ranges_and_no_duplicate_primary(self):
  text=(ROOT/'mods/sevenfall/weapons/subfactions.yaml').read_text()
  seraph=text.split('SF_JanusSeraph:\n')[1].split('\nSF_')[0]
  abyss=text.split('SF_JanusAbyss:\n')[1].split('\nSF_')[0]
  self.assertIn('Range: 7c0',seraph);self.assertIn('Range: 4c0',abyss)
  janus=(ROOT/'mods/sevenfall/rules/55-subfactions.yaml').read_text().split('H_JANUS:\n')[1].split('H_JANUS.DEATH:')[0]
  self.assertEqual(janus.count('\n\tArmament:\n'),1)
  self.assertIn('Name: abyss',janus)
  self.assertIn('PauseOnCondition: sf-protocol-offline',janus)
 def test_new_ai_can_build_exclusives_without_unlocking_other_factions(self):
  ai=(ROOT/'mods/sevenfall/rules/40-ai.yaml').read_text()
  for id in ['a_congregant','a_cantor','h_retrieval','h_janus','d_magistrate','d_contemptor']:
   self.assertIn('\t\t\t'+id+':',ai)
  for id in ['a_processional','h_containment','d_throne']:
   self.assertIn(id,ai)
if __name__=='__main__':unittest.main()
