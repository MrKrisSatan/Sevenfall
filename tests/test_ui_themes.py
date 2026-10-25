from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / 'mods/sevenfall'


class UIThemeTests(unittest.TestCase):
    def test_every_playable_faction_resolves_to_its_parent_theme(self):
        factions = re.findall(r'InternalName: ([ahd]_[a-z]+)', (MOD/'rules/10-factions.yaml').read_text())
        metrics = dict(re.findall(r'FactionSuffix-([^:]+): (\w+)', (MOD/'metrics.yaml').read_text()))
        expected = {'a': 'angelic', 'h': 'human', 'd': 'infernal'}
        self.assertEqual(len(factions), 9)
        for faction in factions:
            self.assertEqual(metrics[faction], expected[faction[0]])

    def test_each_theme_has_full_button_states_and_density_assets(self):
        chrome = (MOD/'chrome-ui.yaml').read_text()
        for theme in ('neutral', 'angelic', 'human', 'infernal'):
            for group in ('sidebar', 'commandbar'):
                self.assertIn(f'\n{group}-{theme}:\n', chrome)
            for group in ('sidebar-button', 'command-button'):
                for state in ('', '-hover', '-pressed', '-disabled', '-highlighted',
                              '-highlighted-hover', '-highlighted-pressed', '-highlighted-disabled'):
                    self.assertIn(f'\n{group}-{theme}{state}:\n', chrome)
        for asset in re.findall(r'\tImage(?:2x|3x)?: sevenfall\|([^\n]+)', chrome):
            self.assertTrue((MOD/asset).is_file(), asset)

    def test_menu_has_only_neutral_civilian_scenery(self):
        menu = (MOD/'maps/sevenfall-menu/map.yaml').read_text()
        self.assertEqual(re.findall(r'Owner: (\w+)', menu), ['Neutral']*8)
        actors = menu.split('Actors:\n')[1].split('Rules:\n')[0]
        types = re.findall(r'^\t\w+: (\w+)', actors, re.M)
        self.assertTrue(set(types) <= {'waypoint', 'sf_cottage', 'sf_townhouse', 'sf_oak', 'sf_pine', 'sf_deadtree'})


if __name__ == '__main__':
    unittest.main()
