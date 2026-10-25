from pathlib import Path
import json
import re
import struct
import unittest
import zlib

ROOT = Path(__file__).resolve().parents[1]


class CursorTests(unittest.TestCase):
    def test_all_cursor_states_have_valid_rgba_frames_and_hotspots(self):
        names = json.loads((ROOT / 'art/cursors/names.json').read_text())
        yaml = (ROOT / 'mods/sevenfall/cursors.yaml').read_text()
        bindings = re.findall(r'\t\t([\w-]+):\n\t\t\tStart: (\d+)', yaml)
        self.assertEqual([name for name, _ in bindings], names)
        self.assertEqual([int(frame) for _, frame in bindings], list(range(len(names))))
        self.assertIn('sevenfall|art/cursors.png:', yaml)
        self.assertNotIn('.shp', yaml)
        png = (ROOT / 'mods/sevenfall/art/cursors.png').read_bytes()
        width, height, depth, color = struct.unpack_from('>IIBB', png, 16)
        self.assertEqual((depth, color), (8, 6))  # Full RGBA, no external palette.
        self.assertGreaterEqual(width * height // (32 * 32), len(names))
        metadata, offset = {}, 8
        while offset < len(png):
            size = struct.unpack_from('>I', png, offset)[0]
            kind = png[offset + 4:offset + 8]
            data = png[offset + 8:offset + 8 + size]
            crc = struct.unpack_from('>I', png, offset + 8 + size)[0]
            self.assertEqual(zlib.crc32(kind + data), crc)
            if kind == b'tEXt':
                key, value = data.decode().split('\0', 1)
                metadata[key] = value
            offset += size + 12
        self.assertEqual(metadata['FrameSize'], '32,32')
        self.assertEqual(int(metadata['FrameAmount']), len(names))
        for name in ('default', 'default-minimap', 'joystick-all'):
            body = yaml.split('\t\t' + name + ':\n')[1].split('\n\t\t', 1)[0]
            # Offsets must stay inside a 32px frame; tip is at (3,3).
            self.assertIn('Start:', body)
            self.assertRegex(yaml, rf'\t\t{name}:\n\t\t\tStart: \d+\n\t\t\tX: -13\n\t\t\tY: -13')
