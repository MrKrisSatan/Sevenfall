import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('standalone', ROOT/'scripts/stage_standalone.py')
stage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(stage)


class StandaloneStagingTests(unittest.TestCase):
    def test_direct_legacy_audio_is_replaced_without_touching_original_wav(self):
        self.assertEqual(stage.quiet('Sounds: gun.aud, voice.v00, ra|audio/unit.r01, sevenfall|audio/impact.wav'),
                         'Sounds: sevenfall|audio/silence.wav, sevenfall|audio/silence.wav, sevenfall|audio/silence.wav, sevenfall|audio/impact.wav')

    def test_staging_excludes_binary_game_assets_and_removes_external_mounts(self):
        with tempfile.TemporaryDirectory() as folder:
            sdk = Path(folder)
            ra = sdk/'engine/mods/ra'
            target = sdk/'mods/sevenfall'
            for directory in ('rules', 'weapons', 'chrome', 'fluent', 'scripts', 'sequences', 'audio'):
                (ra/directory).mkdir(parents=True)
            for directory in ('rules', 'weapons', 'sequences'):
                (target/directory).mkdir(parents=True)
            (ra/'rules/palettes.yaml').write_text('World:\n\tPaletteFromFile@test:\n\t\tName: terrain\n\t\tFilename: temperate.pal\n')
            (ra/'rules/proprietary.shp').write_bytes(b'do not copy')
            (ra/'rules/example.yaml').write_text('Actor:\n\tSounds: gun.aud\n')
            for name in ('chrome.yaml', 'metrics.yaml', 'hotkeys.yaml'):
                (ra/name).write_text('')
            for name in ('COPYING', 'AUTHORS'):
                (sdk/'engine'/name).write_text(name)
            (ra/'audio/voices.yaml').write_text('Generic:\n\tVoices:\n\t\tSelect: yes1\n')
            (ra/'audio/notifications.yaml').write_text('Speech:\n\tNotifications:\n\t\tReady: ready1\n')
            (ra/'sequences/test.yaml').write_text('explosion:\n\tidle: old.shp\n')
            (target/'mod.yaml').write_text('FileSystem: ContentInstallerFileSystem\n\tPackages:\n\t\tra|conquer.mix\nMapFolders:\nSequences:\n\tra|sequences/test.yaml\nRules:\n\tra|rules/example.yaml\n\tsevenfall|rules/51-engineers.yaml\nVoices:\n\tra|audio/voices.yaml\n')
            stage.stage(sdk, target)
            manifest = (target/'mod.yaml').read_text()
            self.assertNotIn('ra|', manifest)
            self.assertNotIn('conquer.mix', manifest)
            self.assertIn('rules/90-alpha.yaml', manifest)
            self.assertFalse((target/'upstream/rules/proprietary.shp').exists())
            self.assertIn('PaletteFromGrayscale@test', (target/'upstream/rules/palettes.yaml').read_text())
            self.assertNotIn('temperate.pal', (target/'upstream/rules/palettes.yaml').read_text())
            self.assertIn('\t\tSelect:\n', (target/'audio/voices.yaml').read_text())
            self.assertIn('art/effects/blast.png', (target/'sequences/compatibility.yaml').read_text())

    def test_original_effects_are_available(self):
        for name in ('blank', 'projectile', 'indicator', 'blast', 'smoke', 'clock', 'shroud', 'fog'):
            data = (ROOT/f'mods/sevenfall/art/effects/{name}.png').read_bytes()
            self.assertTrue(data.startswith(b'\x89PNG\r\n\x1a\n'))
            self.assertIn(b'FrameSize', data)

if __name__ == '__main__':
    unittest.main()
