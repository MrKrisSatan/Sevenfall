"""Candidate provenance and resolved-runtime notice regression checks."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import build
from collect_package_notices import collect
from package_windows import source_revisions


class PackagingTests(unittest.TestCase):
    def test_runtime_notices_follow_restored_patch_and_all_package_caches(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            engine, first, second = root/'engine', root/'cache-one', root/'cache-two'
            for index, cache in enumerate((first, second)):
                project = engine/f'OpenRA.Test{index}/obj'
                project.mkdir(parents=True)
                (project/'project.assets.json').write_text(json.dumps({
                    'packageFolders': {str(cache): {}}, 'libraries': {},
                    'project': {'frameworks': {'net6.0': {'downloadDependencies':
                        [{'name': 'Microsoft.NETCore.App.Runtime.win-x64',
                          'version': '[6.0.22, 6.0.22]'}] if index == 0 else []}}}}))
            runtime = first/'microsoft.netcore.app.runtime.win-x64/6.0.22'
            runtime.mkdir(parents=True)
            (runtime/'runtime.nuspec').write_text('<package><metadata><license type="expression">MIT</license></metadata></package>')
            (runtime/'LICENSE.TXT').write_text('Runtime licence fixture')
            report = collect(engine, root/'notices')
            self.assertEqual([p['package'] for p in report], ['Microsoft.NETCore.App.Runtime.win-x64/6.0.22'])
            self.assertEqual(report[0]['included_texts'], ['LICENSE.TXT'])

    def test_missing_resolved_runtime_cannot_silently_omit_notices(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            project = root/'OpenRA.Test/obj'
            project.mkdir(parents=True)
            (project/'project.assets.json').write_text(json.dumps({
                'packageFolders': {str(root/'missing-cache'): {}}, 'libraries': {},
                'project': {'frameworks': {'net6.0': {'downloadDependencies': [{
                    'name': 'Microsoft.NETCore.App.Runtime.win-x64', 'version': '[6.0.22, 6.0.22]'}]}}}}))
            with self.assertRaisesRegex(RuntimeError, 'runtime dependency missing'):
                collect(root, root/'notices')

    def test_candidate_rejects_dirty_source_but_allows_generated_sdk_overlay(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            revisions = []
            for repo in (root, root/'.sdk', root/'.sdk/engine'):
                repo.mkdir(exist_ok=True)
                subprocess.run(['git', 'init', '-q', str(repo)], check=True)
                (repo/'.gitignore').write_text('.sdk/\nengine/\n')
                (repo/'source.txt').write_text('committed source')
                subprocess.run(['git', 'add', '.'], cwd=repo, check=True)
                subprocess.run(['git', '-c', 'user.name=Test', '-c', 'user.email=test@localhost',
                                'commit', '-qm', 'fixture'], cwd=repo, check=True)
                revisions.append(subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=repo, text=True).strip())
            (root/'.sdk/mod.config').write_text('generated configuration')
            (root/'.sdk/mods/sevenfall').mkdir(parents=True)
            (root/'.sdk/mods/sevenfall/mod.yaml').write_text('generated overlay')
            with patch.object(build, 'ENGINE_COMMIT', revisions[2]), patch.object(build, 'SDK_COMMIT', revisions[1]), patch('engine_patches.verify', return_value={}):
                self.assertEqual(source_revisions(root)['sevenfall'], revisions[0])
                (root/'.sdk/engine/source.txt').write_text('uncommitted engine change')
                with self.assertRaisesRegex(RuntimeError, 'engine: commit or isolate'):
                    source_revisions(root)


if __name__ == '__main__':
    unittest.main()
