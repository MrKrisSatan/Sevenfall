"""Validate authored animation exports, provenance and engine binding coverage."""
import hashlib
import json
from pathlib import Path
import struct
import unittest

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'art/animations'
MOD = ROOT / 'mods/sevenfall'


class AnimationExports(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((ART / 'manifest.json').read_text(encoding='utf-8'))
        cls.assets = cls.manifest['assets']

    def test_complete_implemented_roster_and_building_damage_coverage(self):
        units = {a['id'] for a in self.assets if a['kind'] == 'unit'}
        buildings = {a['id'] for a in self.assets if a['kind'] == 'building'}
        catalogue = json.loads((ROOT / 'docs/roster.json').read_text(encoding='utf-8'))
        extras = json.loads((ROOT / 'art/subfactions/catalogue.json').read_text(encoding='utf-8'))
        newunits = {e['id'].replace('_', '-') for e in extras if e['kind']=='unit'}
        newbuildings = {e['id'].replace('_', '-') for e in extras if e['kind']=='building'}
        self.assertEqual(units | newunits, {r['id'] for r in catalogue if r['kind'] == 'units'})
        defenses = {a['id'].replace('_', '-') for a in json.loads((ROOT / 'art/defenses/catalogue.json').read_text())}
        self.assertEqual(buildings | defenses | newbuildings, {r['id'] for r in catalogue if r['kind'] == 'buildings'})
        self.assertFalse(buildings & defenses)
        self.assertEqual((len(units), len(buildings)), (24, 39))

    def test_hashes_metadata_and_real_frame_variation(self):
        for asset in self.assets:
            with self.subTest(asset=asset['id']):
                data = (ROOT / asset['file']).read_bytes()
                self.assertEqual(hashlib.sha256(data).hexdigest(), asset['sha256'])
                self.assertEqual(data[25], 6, 'RGBA transparency is required')
                width, height = struct.unpack_from('>II', data, 16)
                fw, fh = asset['frameSize']
                self.assertEqual(width, fw * 8)
                self.assertGreaterEqual((width // fw) * (height // fh), asset['frames'])
                self.assertIn(b'FrameSize\x00' + f'{fw},{fh}'.encode(), data)
                self.assertIn(b'FrameAmount\x00' + str(asset['frames']).encode(), data)
                for source in asset['inputs']:
                    self.assertEqual(hashlib.sha256((ROOT / source['source']).read_bytes()).hexdigest(), source['sha256'])
                if asset['kind'] == 'unit':
                    self.assertIn(asset['frames'], (96, 192))
                    # Four genuine authored poses per facing/state, not a
                    # repeated still presented as a movement or death cycle.
                    for start in range(0, asset['frames'], 4):
                        self.assertGreater(len(set(asset['frameHashes'][start:start + 4])), 1)
                else:
                    self.assertEqual(len(set(asset['frameHashes'])), 3)

    def test_all_assets_have_consuming_sequences_and_death_bindings(self):
        sequences = (MOD / 'sequences/animations.yaml').read_text(encoding='utf-8')
        rules = (MOD / 'rules/35-animations.yaml').read_text(encoding='utf-8')
        for asset in self.assets:
            with self.subTest(asset=asset['id']):
                filename = Path(asset['file']).name
                self.assertIn('Filename: sevenfall|art/animations/' + filename, sequences)
                if asset['kind'] == 'unit' and not asset['id'].endswith('-mcv'):
                    self.assertIn('Actor: ' + asset['id'].replace('-', '_') + '.death', rules)
        self.assertIn('StartSequence: die', rules)
        self.assertIn('Sequence: corpse', rules)
        self.assertIn('Actor: mcv.sfdeath', rules)
        self.assertIn('critical-idle:', sequences)
        self.assertIn('damaged-move:', sequences)
        self.assertIn('damaged-shoot:', sequences)


if __name__ == '__main__':
    unittest.main()
