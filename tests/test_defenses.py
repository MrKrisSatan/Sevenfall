"""Defense coverage, authored exports and counterplay configuration."""
import hashlib
import json
from pathlib import Path
import struct
import unittest
import wave

ROOT = Path(__file__).resolve().parents[1]


class Defenses(unittest.TestCase):
    def test_five_unique_defenses_per_faction_and_buildable_gates(self):
        catalogue = json.loads((ROOT / 'art/defenses/catalogue.json').read_text())
        self.assertEqual(len({e['id'] for e in catalogue}), 15)
        rules = (ROOT / 'mods/sevenfall/rules/45-defenses.yaml').read_text()
        for prefix, faction in [('a', 'angels'), ('h', 'humans'), ('d', 'demons')]:
            entries = [e for e in catalogue if e['id'].startswith(prefix + '_')]
            self.assertEqual(len(entries), 5)
            for entry in entries:
                block = rules.split(entry['id'].upper() + ':\n', 1)[1].split('\n\n', 1)[0]
                self.assertIn('Queue: Defense', block)
                self.assertIn('~sf.' + faction, block)

    def test_all_six_authored_states_and_runtime_exports_match(self):
        manifest = json.loads((ROOT / 'art/defenses/manifest.json').read_text())
        self.assertEqual(len(manifest['assets']), 15)
        for entry in manifest['assets']:
            with self.subTest(actor=entry['id']):
                data = (ROOT / entry['file']).read_bytes()
                self.assertEqual(hashlib.sha256(data).hexdigest(), entry['sha256'])
                source = (ROOT / entry['source']).read_bytes()
                self.assertEqual(hashlib.sha256(source).hexdigest(), entry['sourceSha256'])
                self.assertEqual(data, (ROOT / 'mods/sevenfall/art/defenses' / (entry['id'] + '.png')).read_bytes())
                self.assertEqual(struct.unpack_from('>II', data, 16), (entry['frameSize'] * 6, entry['frameSize']))
                self.assertEqual(data[25], 6)
                self.assertEqual(len(set(entry['frameHashes'])), 6)
                self.assertTrue((ROOT / 'mods/sevenfall/art/defenses' / (entry['id'] + '-icon.png')).is_file())

    def test_original_moaning_audio_is_valid_pcm(self):
        with wave.open(str(ROOT / 'mods/sevenfall/audio/sf-mourning.wav')) as audio:
            self.assertEqual((audio.getnchannels(), audio.getsampwidth(), audio.getframerate()), (1, 2, 22050))
            self.assertGreater(audio.getnframes(), 22050)

    def test_native_runner_requires_completion_and_surfaces_lua_failures(self):
        runner = (ROOT / 'scripts/run_defense_test.py').read_text()
        self.assertIn('DEFENSE_TEST COMPLETE checks=', runner)
        self.assertIn('Fatal Lua Error:', runner)
        self.assertIn('process.terminate()', runner)


if __name__ == '__main__':
    unittest.main()
