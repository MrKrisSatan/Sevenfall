import importlib.util
from pathlib import Path
import struct
import tempfile
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('installer', ROOT / 'scripts/install_into_sdk.py')
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class IntegrationTools(unittest.TestCase):
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
