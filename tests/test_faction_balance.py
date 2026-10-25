"""Doctrine/counter contracts; engine lint separately validates inherited traits.

These tests do not predict match win rates or replace live balance testing.
"""
from pathlib import Path
import re
import unittest
from test_gameplay_contract import load_actors, trait, field

ROOT = Path(__file__).resolve().parents[1]

def weapon_field(body, key):
    match = re.search(r'(?m)^\t' + re.escape(key) + r': ([^\n]+)$', body)
    return match[1] if match else None


def weapon_trait(body, name):
    match = re.search(r'(?ms)^\t' + re.escape(name) + r':[^\n]*\n(.*?)(?=^\t[^\t]|\Z)', body)
    return match[1] if match else ''


class FactionBalanceTests(unittest.TestCase):
    def setUp(self):
        self.actors = load_actors()
        source = (ROOT / 'mods/sevenfall/weapons/sevenfall.yaml').read_text()
        self.weapons = dict(re.findall(r'(?ms)^(SF_\w+):\n(.*?)(?=^SF_\w+:|\Z)', source))

    def number(self, actor, name, key):
        return int(field(trait(self.actors[actor], name), key))

    def weapon(self, actor, slot='Armament@PRIMARY'):
        return self.weapons[field(trait(self.actors[actor], slot), 'Weapon')]

    def test_line_infantry_have_distinct_strengths_and_tradeoffs(self):
        a, h, d = 'a_watcher', 'h_rifleman', 'd_thrall'
        for name, key in [('Health', 'HP'), ('Valued', 'Cost'), ('Buildable', 'BuildDurationModifier')]:
            self.assertGreater(self.number(a, name, key), self.number(h, name, key))
            self.assertGreater(self.number(h, name, key), self.number(d, name, key))
        self.assertLess(self.number(a, 'Mobile', 'Speed'), self.number(h, 'Mobile', 'Speed'))
        self.assertLess(self.number(h, 'Mobile', 'Speed'), self.number(d, 'Mobile', 'Speed'))
        def range_of(actor):
            cells, sub = weapon_field(self.weapon(actor), 'Range').split('c')
            return int(cells)*1024 + int(sub)
        self.assertGreater(range_of(h), range_of(a))
        self.assertGreater(range_of(a), range_of(d))
        damage = [int(field(weapon_trait(self.weapon(u), 'Warhead@1Dam'), 'Damage')) for u in [a,h,d]]
        self.assertEqual(len(set(damage)), 3)
        def nominal_dps(actor):
            w = self.weapon(actor)
            return int(field(weapon_trait(w, 'Warhead@1Dam'), 'Damage')) / int(weapon_field(w, 'ReloadDelay'))
        self.assertGreater(nominal_dps(d), nominal_dps(a))
        self.assertGreater(nominal_dps(h)/self.number(h,'Valued','Cost'), nominal_dps(a)/self.number(a,'Valued','Cost'))

    def test_all_combat_weapons_are_explicit_and_not_shared_between_factions(self):
        owners = {}
        combat = [u for u in self.actors if u in {m.lower() for m in re.findall(r'(?m)^([A-Z_]+):', (ROOT/'mods/sevenfall/rules/30-units.yaml').read_text())} and u not in ('a_gatherer','h_harvester','d_devourer')]
        self.assertEqual(len(combat),18)
        for u in combat:
            self.assertTrue(trait(self.actors[u], 'Health'),u)
            weapons = re.findall(r'(?m)^\t\tWeapon: (\S+)', self.actors[u])
            self.assertTrue(weapons,u)
            for w in weapons:
                self.assertIn(w,self.weapons,u)
                self.assertEqual(owners.setdefault(w,u[0]),u[0],w)
                self.assertEqual(weapon_field(self.weapons[w],'Burst'),'1',w)
                self.assertTrue(field(weapon_trait(self.weapons[w],'Warhead@1Dam'),'Damage'),w)
            if 'Queue: Infantry' in self.actors[u]:
                self.assertEqual(field(trait(self.actors[u],'Armament@PRIMARY'),'Weapon'),field(trait(self.actors[u],'Armament@GARRISONED'),'Weapon'))
                if trait(self.actors[u],'Armament@SECONDARY'):
                    self.assertEqual(field(trait(self.actors[u],'Armament@SECONDARY'),'Weapon'),field(trait(self.actors[u],'Armament@GARRISONEDSECONDARY'),'Weapon'))

    def test_renewal_is_angel_combat_only_and_interruptible(self):
        for u,b in self.actors.items():
            healing = trait(b,'ChangesHealth@SF_RENEWAL')
            if healing:
                self.assertTrue(u.startswith('a_'))
                self.assertGreaterEqual(int(field(healing,'DamageCooldown')),200)
                self.assertEqual(field(healing,'Step'),'0')
                self.assertEqual(field(healing,'PercentageStep'),'1')
        self.assertEqual(sum(bool(trait(b,'ChangesHealth@SF_RENEWAL')) for b in self.actors.values()),6)

    def test_frenzy_is_temporary_nonstacking_and_demon_only(self):
        count=0
        for u,b in self.actors.items():
            frenzy=trait(b,'GrantConditionOnAttack@SF_FRENZY')
            if not frenzy:continue
            count+=1;self.assertTrue(u.startswith('d_'))
            self.assertEqual(field(frenzy,'MaximumInstances'),'1')
            self.assertEqual(field(frenzy,'RequiredShotsPerInstance'),'1')
            self.assertEqual(field(frenzy,'RevokeDelay'),'100')
            for modifier in ['FirepowerMultiplier@SF_FRENZY','SpeedMultiplier@SF_FRENZY']:
                self.assertEqual(field(trait(b,modifier),'RequiresCondition'),'sf-frenzy')
        self.assertEqual(count,6)

    def test_human_engineering_and_economy_remain_separate(self):
        for u in ['h_bulwark','h_siegegun','h_harvester']:
            self.assertEqual(self.number(u,'Repairable','HpPerStep'),1500)
        for u in ['a_gatherer','h_harvester','d_devourer']:
            self.assertNotIn('Weapon:',self.actors[u])
            self.assertNotIn('SF_FRENZY',self.actors[u])
            self.assertNotIn('SF_RENEWAL',self.actors[u])
        self.assertLess(self.number('h_generator','Valued','Cost'), self.number('a_spire','Valued','Cost'))
        self.assertLess(self.number('h_generator','Valued','Cost'), self.number('d_heart','Valued','Cost'))

    def test_missile_range_and_anti_armour_counters(self):
        for name,w in self.weapons.items():
            if weapon_field(w,'Inherits') in ('Dragon','RedEye'):
                self.assertEqual(field(weapon_trait(w,'Projectile'),'RangeLimit'),'12c0')
        for name in ['SF_PulseRifle','SF_HellClaw','SF_SkitterClaw']:
            heavy=int(re.search(r'\t\t\tHeavy: (\d+)',self.weapons[name])[1])
            self.assertLessEqual(heavy,12)
        self.assertEqual(weapon_field(self.weapons['SF_SiegeShell'],'MinRange'),'4c0')
