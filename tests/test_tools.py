import importlib.util
from pathlib import Path
import struct
import tempfile
import re
import unittest
import zlib
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('installer', ROOT / 'scripts/install_into_sdk.py')
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class IntegrationTools(unittest.TestCase):
    def test_logistics_png_sheet_metadata_and_provenance(self):
        art = ROOT / 'mods/sevenfall/art'
        for name, size, count in [
            *((f'{f}-{kind}', (64, 64), 8) for f in 'ahd' for kind in ['mcv', 'harvester']),
            ('veilglass-rough', (24, 24), 4), ('veilglass-enriched', (24, 24), 4),
        ]:
            data = (art / (name + '.png')).read_bytes()
            self.assertEqual(struct.unpack_from('>II', data, 16), (size[0]*count, size[1]))
            self.assertEqual(data[25], 6)
            metadata = {}
            offset = 8
            while offset < len(data):
                length = struct.unpack_from('>I', data, offset)[0]
                kind = data[offset+4:offset+8]
                payload = data[offset+8:offset+8+length]
                crc = struct.unpack_from('>I', data, offset+8+length)[0]
                self.assertEqual(zlib.crc32(kind+payload), crc, name)
                if kind == b'tEXt':
                    key, value = payload.split(b'\0', 1)
                    metadata[key.decode()] = value.decode()
                offset += length+12
            self.assertEqual(metadata['FrameSize'], ','.join(map(str, size)))
            self.assertEqual(int(metadata['FrameAmount']), count)
        for f in 'ahd':
            self.assertEqual(struct.unpack_from('>II', (art / f'{f}-yard.png').read_bytes(), 16), (128, 128))
            for kind in ['yard', 'mcv', 'harvester']:
                self.assertEqual(struct.unpack_from('>II', (art / f'{f}-{kind}-icon.png').read_bytes(), 16), (56, 42))
        for asset in json.loads((ROOT / 'art/sources.json').read_text())['assets']:
            self.assertEqual(hashlib.sha256((ROOT / asset['file']).read_bytes()).hexdigest(), asset['sha256'])

    def test_art_dimensions_and_atlas_regions(self):
        art = ROOT / 'mods/sevenfall/art'
        def png_size(name):
            data = (art / name).read_bytes()
            self.assertEqual(data[:8], b'\x89PNG\r\n\x1a\n')
            return struct.unpack_from('>II', data, 16)
        for name in ['a-spire', 'h-generator', 'd-heart']:
            self.assertEqual(png_size(name + '.png'), (96, 112))
            self.assertEqual(png_size(name + '-icon.png'), (56, 42))
            # PNG color type 6 is RGBA: retain alpha for terrain compositing.
            self.assertEqual((art / (name + '.png')).read_bytes()[25], 6)
        for name in ['a-veilworks', 'h-veilworks', 'd-veilworks']:
            self.assertEqual(png_size(name + '.png'), (128, 128))
            self.assertEqual(png_size(name + '-icon.png'), (56, 42))
            self.assertEqual((art / (name + '.png')).read_bytes()[25], 6)
        for scale in [1, 2, 3]:
            suffix = '' if scale == 1 else f'-{scale}x'
            for name, minimum in [('factions', (30*scale, 60*scale)), ('loadscreen', (512*scale, 256*scale))]:
                actual = png_size(f'{name}{suffix}.png')
                for size, required in zip(actual, minimum):
                    self.assertGreaterEqual(size, required)
                    self.assertEqual(size & (size-1), 0, 'Chrome textures must be power-of-two')
        chrome = (ROOT / 'mods/sevenfall/chrome.yaml').read_text()
        for x, y, width, height in re.findall(r'^\t\t\w+: (\d+), (\d+), (\d+), (\d+)$', chrome, re.M):
            self.assertLessEqual(int(x)+int(width), 30)
            self.assertLessEqual(int(y)+int(height), 60)

    def test_every_faction_has_lobby_icon_and_ingame_theme(self):
        mod = ROOT / 'mods/sevenfall'
        factions = re.findall(r'InternalName: ([ahd]_[a-z]+)', (mod / 'rules/10-factions.yaml').read_text())
        self.assertEqual(len(factions), 9)
        chrome = (mod / 'chrome.yaml').read_text()
        metrics = (mod / 'metrics.yaml').read_text()
        for faction in factions:
            self.assertIn(f'\t\t{faction}:', chrome)
            self.assertIn(f'\tFactionSuffix-{faction}:', metrics)

    def test_manifest_addition_preserves_next_section_and_is_idempotent(self):
        source = 'Rules:\n\tra|rules.yaml\n\nWeapons:\n\tra|weapons.yaml\n'
        result = installer.append_manifest_section(source, 'Rules', 'sevenfall|rules/test.yaml')
        self.assertIn('\nWeapons:\n\tra|weapons.yaml\n', result)
        self.assertEqual(result, installer.append_manifest_section(result, 'Rules', 'sevenfall|rules/test.yaml'))

    def test_buildable_scan_ignores_abstracts_and_removals(self):
        with tempfile.TemporaryDirectory() as directory:
            Path(directory, 'rules.yaml').write_text('^Base:\n\tBuildable:\nTANK:\n\tBuildable:\nHUSK:\n\t-Buildable:\n')
            self.assertEqual(installer.scan_buildables(Path(directory)), ['TANK'])

    def test_map_binary_and_equal_starting_resources(self):
        data = (ROOT / 'mods/sevenfall/maps/broken-choir/map.bin').read_bytes()
        version, width, height, tiles, heights, resources = struct.unpack_from('<BHHIII', data)
        self.assertEqual((version, width, height, tiles, heights), (2, 96, 96, 17, 0))
        self.assertEqual(len(data), resources + width * height * 2)
        def cell(x, y):
            offset = resources + (x * height + y) * 2
            return data[offset:offset+2]
        for x in range(width):
            for y in range(height):
                self.assertEqual(cell(x, y), cell(95-x, 95-y))
        self.assertEqual(cell(23, 23), bytes((1, 12)))
        self.assertEqual(cell(48, 48), bytes((2, 3)))
        self.assertEqual(cell(15, 15), bytes((0, 0)))


if __name__ == '__main__':
    unittest.main()
