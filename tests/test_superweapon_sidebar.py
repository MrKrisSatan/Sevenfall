import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('sidebar', ROOT/'scripts/superweapon_sidebar.py')
sidebar = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sidebar)


class SidebarIntegrationTests(unittest.TestCase):
    def test_moves_powers_inside_production_without_losing_neighbors(self):
        source = ('Container@PLAYER_WIDGETS:\n\tChildren:\n'
                  '\t\tContainer@SUPPORT_POWERS:\n\t\t\tOld: True\n'
                  '\t\tSupportPowerTimer@SUPPORT_POWER_TIMER:\n\t\t\tY: 10\n'
                  '\t\tContainer@SIDEBAR_PRODUCTION:\n\t\t\tLogic: ClassicProductionLogic\n'
                  '\t\t\tChildren:\n\t\t\t\tLogicTicker@PRODUCTION_TICKER:\n')
        actual = sidebar.integrate(source)
        self.assertNotIn('Container@SUPPORT_POWERS:', actual)
        self.assertIn('SupportPowerTimer@SUPPORT_POWER_TIMER:', actual)
        self.assertIn('Logic: SFDefenseProductionLogic', actual)
        self.assertIn('\t\t\t\tSFDefensePowers@DEFENSE_POWERS:', actual)
        self.assertIn('Columns: 3', actual)
        self.assertIn('LogicTicker@PRODUCTION_TICKER:', actual)

    def test_changed_upstream_layout_fails_instead_of_silently_dropping_powers(self):
        with self.assertRaises(ValueError):
            sidebar.integrate('Container@UNEXPECTED:\n')
