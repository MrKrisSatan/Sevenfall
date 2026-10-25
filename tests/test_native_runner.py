import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('native_runner',
    Path(__file__).resolve().parents[1] / 'scripts/run_defense_test.py')
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


class NativeRunnerTests(unittest.TestCase):
    def test_only_selected_scenario_completion_passes(self):
        self.assertEqual(runner.diagnostic_status('DEFENSE_TEST COMPLETE checks=33', 'release'), 'pending')
        self.assertEqual(runner.diagnostic_status('RELEASE_TEST PASS: one check', 'release'), 'pending')
        self.assertEqual(runner.diagnostic_status('RELEASE_TEST COMPLETE checks=22', 'release'), 'passed')

    def test_failure_overrides_completion(self):
        complete = 'RELEASE_TEST COMPLETE checks=22\n'
        for failure in ['RELEASE_TEST FAIL: harvesting', 'Fatal Lua Error: bad call']:
            self.assertEqual(runner.diagnostic_status(complete + failure, 'release'), 'failed')
