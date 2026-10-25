import importlib.util
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/audit_release_dependencies.py'
spec = importlib.util.spec_from_file_location('release_dependencies', SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ReleaseDependenciesTests(unittest.TestCase):
    def inspect(self, source):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'mod.yaml'
            path.write_text(source)
            return module.inspect(path)

    def test_external_dependencies_include_optional_content(self):
        report = self.inspect('Rules:\n\tra|rules/world.yaml\nFileSystem:\n\t~^SupportDir|Content/ra/v2/: content\n')
        self.assertFalse(report['independent_manifest'])
        self.assertEqual(len(report['external_ra_references']), 2)
        self.assertEqual(report['external_ra_references'][0]['section'], 'Rules')

    def test_project_and_common_references_are_not_ra_dependencies(self):
        report = self.inspect('# old ra| reference\nRules:\n\tsevenfall|rules/world.yaml\nChrome:\n\tcommon|chrome.yaml\n')
        self.assertTrue(report['independent_manifest'])

    def test_missing_manifest_cannot_pass(self):
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaises(FileNotFoundError):
                module.inspect(Path(folder) / 'missing.yaml')
