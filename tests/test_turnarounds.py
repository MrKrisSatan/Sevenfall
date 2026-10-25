"""Validate complete directional assets and OpenRA PNG metadata without an image dependency."""
from pathlib import Path
import hashlib
import json
import struct
import unittest
import zlib

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'art/unit-turnarounds'
DIRECTIONS = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']


class TurnaroundTests(unittest.TestCase):
    def setUp(self):
        self.roster = json.loads((ART / 'roster.json').read_text(encoding='utf-8'))
        self.manifest = json.loads((ART / 'manifest.json').read_text(encoding='utf-8'))

    def test_all_current_units_and_new_domains_have_eight_views(self):
        current = json.loads((ROOT / 'docs/roster.json').read_text(encoding='utf-8'))
        current_ids = {r.get('variant_of',r['id']) for r in current if r['kind'] == 'units'}
        ids = {r['id'] for r in self.roster}
        new = json.loads((ROOT / 'art/subfactions/manifest.json').read_text(encoding='utf-8'))
        animated_ids = {e['id'].replace('_','-') for e in new['assets'] if e['frames']==64}
        self.assertTrue(current_ids <= ids | animated_ids)
        self.assertEqual(len(ids), 39)
        self.assertEqual({r['id'] for r in self.manifest['assets']}, ids)
        self.assertEqual(self.manifest['directionOrder'], DIRECTIONS)
        self.assertEqual(self.manifest['openraFacings'], -8)
        for faction in ['angels', 'humans', 'demons']:
            units = [r for r in self.roster if r['faction'] == faction]
            self.assertEqual(len(units), 13)
            self.assertEqual(sum(r['category'] == 'ships' for r in units), 2)
            self.assertEqual(sum(r['category'] == 'aircraft' for r in units), 2)
            self.assertGreaterEqual(sum(r['category'] == 'beasts' for r in units), 1)
        for r in self.manifest['assets']:
            self.assertEqual(r['directions'], DIRECTIONS)
            self.assertEqual(len(r['frames']), 8)
            self.assertEqual(len(set(r['frameHashes'])), 8)

    def test_pngs_have_valid_metadata_dimensions_and_provenance(self):
        for r in self.manifest['assets']:
            self.assertEqual(hashlib.sha256((ROOT / r['source']).read_bytes()).hexdigest(), r['sourceSha256'])
            for filename, expected_hash in [(r['sheet'], r['sheetSha256']), *zip(r['frames'], r['frameHashes'])]:
                data = (ROOT / filename).read_bytes()
                self.assertEqual(hashlib.sha256(data).hexdigest(), expected_hash)
                self.assertEqual(data[:8], b'\x89PNG\r\n\x1a\n')
                self.assertEqual(data[25], 6, 'RGBA transparency must be retained')
                sheet = filename == r['sheet']
                self.assertEqual(struct.unpack_from('>II', data, 16), (1024, 128) if sheet else (256, 256))
                offset = 8
                metadata = {}
                while offset < len(data):
                    length = struct.unpack_from('>I', data, offset)[0]
                    kind = data[offset+4:offset+8]
                    payload = data[offset+8:offset+8+length]
                    self.assertEqual(zlib.crc32(kind+payload), struct.unpack_from('>I', data, offset+8+length)[0])
                    if kind == b'tEXt':
                        key, value = payload.split(b'\0', 1)
                        metadata[key.decode()] = value.decode()
                    offset += length+12
                if sheet:
                    self.assertEqual(metadata['FrameSize'], '128,128')
                    self.assertEqual(metadata['FrameAmount'], '8')

    def test_gallery_has_every_unit_and_preview(self):
        page = (ROOT / 'docs/turnarounds.html').read_text(encoding='utf-8')
        for r in self.manifest['assets']:
            self.assertIn('id="'+r['id']+'"', page)
            self.assertIn(r['preview'], page)
            data = (ROOT / 'docs' / r['preview']).read_bytes()
            self.assertEqual(data[:4], b'RIFF')
            self.assertEqual(data[8:12], b'WEBP')
        prompts = json.loads((ART / 'prompts.json').read_text(encoding='utf-8'))
        self.assertEqual({r['id'] for r in prompts}, {r['id'] for r in self.roster if r['generate']})


if __name__ == '__main__':
    unittest.main()
