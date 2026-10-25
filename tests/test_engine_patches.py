"""Pinning, idempotence and preservation contracts for corresponding engine source."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
import engine_patches as ep

class EnginePatchTests(unittest.TestCase):
    def fixture(self, root):
        source=root/'source.cs';source.write_text('before\n')
        manifest=root/'patch.json'
        manifest.write_text(json.dumps({'patches':[{'path':'source.cs',
            'before':'before', 'after':'after',
            'before_sha256':ep.digest('before\n'), 'after_sha256':ep.digest('after\n')}]}))
        return source,manifest

    def test_patching_is_idempotent_and_verified(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);source,manifest=self.fixture(root)
            with patch.object(ep,'MANIFEST',manifest):
                first=ep.apply(root);self.assertEqual(first,ep.apply(root))
                self.assertEqual(source.read_text(),'after\n')
                self.assertEqual(first,ep.verify(root))

    def test_unexpected_source_is_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);source,manifest=self.fixture(root);source.write_text('local change')
            with patch.object(ep,'MANIFEST',manifest),self.assertRaisesRegex(RuntimeError,'preserving local edits'):
                ep.apply(root)
            self.assertEqual(source.read_text(),'local change')

    def test_modified_patched_source_fails_verification(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);source,manifest=self.fixture(root)
            with patch.object(ep,'MANIFEST',manifest):
                ep.apply(root);source.write_text('after\nunaudited extra')
                with self.assertRaisesRegex(RuntimeError,'modified'):ep.verify(root)
