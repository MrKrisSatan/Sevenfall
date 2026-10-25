"""Prevent active unit bodies from falling back to Red Alert artwork."""
from pathlib import Path
import re
import unittest

from test_gameplay_contract import load_actors, trait, field

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / 'mods/sevenfall'


class OriginalUnitVisualTests(unittest.TestCase):
    def test_every_combat_actor_uses_its_authored_sheet_and_icon(self):
        rules = load_actors()
        sequences = (MOD / 'sequences/units.yaml').read_text(encoding='utf-8')
        entries = dict(re.findall(r'(?ms)^(\w+):\n(.*?)(?=^\w+:|\Z)', sequences))
        combat = {name: body for name, body in rules.items()
                  if name[0] in 'ahd' and field(trait(body, 'Buildable'), 'Queue') in {'Infantry', 'Vehicle'}
                  and '\tInherits: HARV' not in body}
        self.assertEqual(len(combat), 18)
        self.assertEqual(set(entries), set(combat))
        for name, body in combat.items():
            with self.subTest(actor=name):
                self.assertEqual(field(trait(body, 'RenderSprites'), 'Image'), name)
                sheet = name.replace('_', '-') + '.png'
                self.assertTrue((ROOT / 'art/unit-turnarounds/sheets' / sheet).is_file())
                self.assertIn('Filename: sevenfall|art/unit-turnarounds/' + sheet, entries[name])
                self.assertIn('\ticon:\n', entries[name])
                self.assertIn('Facings: -8', entries[name])
                self.assertNotIn('.shp', entries[name])
                if '\tInherits: E' in body:
                    self.assertIn('\t-WithDeathAnimation:', body)
                    for sequence in ('stand', 'run', 'shoot', 'prone-run', 'prone-shoot', 'parachute'):
                        self.assertIn('\t' + sequence + ':\n', entries[name])
                if '\tInherits: 2TNK' in body or '\tInherits: 1TNK' in body:
                    for removal in ('WithSpriteTurret', 'WithMuzzleOverlay', 'AttackTurreted', 'Turreted'):
                        self.assertIn('\t-' + removal + ':', body)
                    self.assertIn('\tAttackFrontal:', body)
                if '\tInherits: 2TNK' in body:
                    self.assertIn('\t-SpawnActorOnDeath:', body)

    def test_gallery_contains_every_unit_and_faction_mcv(self):
        text = (MOD / 'maps/unit-gallery/map.yaml').read_text(encoding='utf-8')
        actors = re.findall(r'^\tUnit([ahd])\d+: (\w+)$', text, re.M)
        self.assertEqual(len(actors), 24)
        units = {name for name, body in load_actors().items()
                 if field(trait(body, 'Buildable'), 'Queue') in {'Infantry', 'Vehicle'}}
        self.assertEqual({name for _, name in actors}, units | {'mcv'})
        for faction in 'ahd':
            self.assertEqual(sum(side == faction for side, _ in actors), 8)


if __name__ == '__main__':
    unittest.main()
