"""Skirmish distribution allowlist and installer provenance validation."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from package_profiles import stage_mod,SKIRMISH_MAPS
from package_installer import validate_package
class CandidateProfileTests(unittest.TestCase):
 def test_skirmish_profile_excludes_developer_and_campaign_maps(self):
  with tempfile.TemporaryDirectory() as t:
   root=Path(t);source=root/'source'
   for name in SKIRMISH_MAPS|{'doctrine-test','h03-glass-fields','twelve-test'}:
    folder=source/'maps'/name;folder.mkdir(parents=True);(folder/'map.yaml').write_text(name)
   (source/'missions.yaml').write_text('unfinished campaign entries')
   names=stage_mod(source,root/'package','skirmish')
   self.assertEqual(set(names),SKIRMISH_MAPS)
   self.assertNotIn('unfinished',(root/'package/missions.yaml').read_text())
   self.assertTrue((source/'maps/doctrine-test/map.yaml').exists())
 def test_development_profile_preserves_diagnostics(self):
  with tempfile.TemporaryDirectory() as t:
   root=Path(t);(root/'source/maps/terrain-test').mkdir(parents=True)
   (root/'source/maps/terrain-test/map.yaml').write_text('test')
   self.assertIn('terrain-test',stage_mod(root/'source',root/'package','development'))
 def fixture(self,root):
  (root/'Sevenfall.exe').write_bytes(b'candidate fixture')
  (root/'BUILD_INFO.json').write_text(json.dumps({'version':'0.3.0-test','profile':'skirmish'}))
  (root/'FILES.sha256.json').write_text(json.dumps({'Sevenfall.exe':hashlib.sha256(b'candidate fixture').hexdigest()}))
 def test_installer_rejects_modified_candidate(self):
  with tempfile.TemporaryDirectory() as t:
   root=Path(t);self.fixture(root);self.assertEqual(validate_package(root)['profile'],'skirmish')
   (root/'Sevenfall.exe').write_bytes(b'modified')
   with self.assertRaisesRegex(ValueError,'hash mismatch'):validate_package(root)
 def test_installer_rejects_development_profile(self):
  with tempfile.TemporaryDirectory() as t:
   root=Path(t);self.fixture(root)
   (root/'BUILD_INFO.json').write_text(json.dumps({'profile':'development'}))
   with self.assertRaisesRegex(ValueError,'skirmish'):validate_package(root)
 def test_installer_rejects_inventory_path_traversal(self):
  with tempfile.TemporaryDirectory() as t:
   root=Path(t);self.fixture(root)
   (root/'FILES.sha256.json').write_text(json.dumps({'../outside':'00'}))
   with self.assertRaisesRegex(ValueError,'Unsafe inventory'):validate_package(root)
if __name__=='__main__':unittest.main()
