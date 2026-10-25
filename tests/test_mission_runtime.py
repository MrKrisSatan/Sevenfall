"""Run real Lua 5.1 mission scripts against a limited OpenRA API double.

This verifies script decisions, not engine scheduling, harvesting or AI.
Install requirements-test.txt before running the suite.
"""
from pathlib import Path
import unittest

from lupa.lua51 import LuaRuntime
from test_first_war_missions import SCENARIOS

ROOT = Path(__file__).resolve().parents[1]
BUILDINGS = {
    'h': ('h_barracks', 'h_motorpool'),
    'a': ('a_chapel', 'a_armory'),
    'd': ('d_pit', 'd_forge'),
}


class Mission:
    def __init__(self, slug, data):
        self.lua = LuaRuntime()
        self.lua.execute((ROOT / 'tests/mission_harness.lua').read_text())
        self.g = self.lua.globals()
        self.data = data
        self.mcv = self.add('mcv')
        self.yard = self.add('fact', self.g.enemy)
        self.lua.execute((ROOT / 'mods/sevenfall/maps' / slug / 'mission.lua').read_text())
        self.g.WorldLoaded()

    def add(self, type, owner=None):
        return self.g.AddActor(type, owner)

    def tick(self, time=25):
        self.g.DateTime.GameTime = time
        self.g.Tick()

    def establish(self):
        self.mcv.IsInWorld = False
        self.command = self.add('fact')
        for type in (self.data['power'], *BUILDINGS[self.data['faction'][0]]):
            self.add(type)
        self.refinery = self.add(self.data['refinery'])
        self.harvester = self.add(self.data['harvester'])
        self.tick(1)  # FreeActor miners are discovered between objective polls.

    def produce(self, owner=None):
        for type in (self.data['infantry'], self.data['vehicle']):
            self.g.production(None, self.add(type, owner), 'test')

    def ready(self):
        self.g.commander.Resources = 900
        self.produce()
        self.yard.IsDead = True

    def state(self, id):
        return self.g.commander.objectives[id].state


class MissionRuntimeTests(unittest.TestCase):
    def missions(self):
        for slug, data in SCENARIOS.items():
            yield slug, Mission(slug, data)

    def test_deployment_and_normal_victory(self):
        for slug, m in self.missions():
            with self.subTest(mission=slug):
                m.establish()
                self.assertIsNone(m.g.commander.result)
                m.ready()
                m.tick()
                self.assertEqual(m.g.commander.result, 'won')
                self.assertEqual(m.state(4), 'completed')
                events = list(m.g.events.values())
                self.assertLess(events.index('completed:4'), events.index('won'))

    def test_starting_guards_and_enemy_production_do_not_count(self):
        for slug, m in self.missions():
            with self.subTest(mission=slug):
                m.establish()
                m.add(m.data['infantry'])
                m.add(m.data['vehicle'])
                m.produce(m.g.enemy)
                m.g.commander.Resources = 900
                m.yard.IsDead = True
                m.tick()
                self.assertEqual(m.state(2), 'incomplete')
                self.assertIsNone(m.g.commander.result)

    def test_cash_and_insufficient_mining_cannot_complete_economy(self):
        for slug, m in self.missions():
            with self.subTest(mission=slug):
                m.establish()
                m.produce()
                m.yard.IsDead = True
                m.g.commander.Cash = 100000
                m.g.commander.Resources = 899
                m.tick()
                self.assertEqual(m.state(1), 'incomplete')
                self.assertIsNone(m.g.commander.result)
                m.g.commander.Resources = 900
                m.tick(50)
                self.assertEqual(m.g.commander.result, 'won')

    def test_recapture_does_not_restore_preservation(self):
        for slug, m in self.missions():
            with self.subTest(mission=slug):
                m.establish()
                m.g.LoseActor(m.harvester, 'capture')
                m.harvester.Owner = m.g.commander
                m.ready()
                m.tick()
                self.assertEqual(m.state(4), 'failed')
                self.assertEqual(m.g.commander.result, 'won')

    def test_completed_production_stays_complete_after_factory_loss(self):
        for slug, m in self.missions():
            with self.subTest(mission=slug):
                m.establish()
                m.produce()
                m.g.commander.Resources = 900
                m.tick()
                factory_type = BUILDINGS[m.data['faction'][0]][1]
                factory = m.g.commander.GetActorsByType(factory_type)[1]
                factory.IsDead = True
                m.yard.IsDead = True
                m.tick(50)
                self.assertEqual(m.g.commander.result, 'won')
                self.assertEqual(m.state(4), 'completed')

    def test_replacing_lost_first_economy_actors_does_not_restore_bonus(self):
        for slug, data in SCENARIOS.items():
            for target in ('refinery', 'harvester'):
                for reason in ('kill', 'capture', 'remove'):
                    with self.subTest(mission=slug, target=target, reason=reason):
                        m = Mission(slug, data)
                        m.establish()
                        actor = getattr(m, target)
                        m.g.LoseActor(actor, reason)
                        self.assertEqual(m.state(4), 'failed')
                        m.add(data[target])
                        m.ready()
                        m.tick()
                        self.assertEqual(m.g.commander.result, 'won')
                        self.assertEqual(m.state(4), 'failed')

    def test_later_economy_actor_loss_does_not_fail_bonus(self):
        for slug, m in self.missions():
            with self.subTest(mission=slug):
                m.establish()
                for type in (m.data['refinery'], m.data['harvester']):
                    later = m.add(type)
                    m.tick(2)
                    m.g.LoseActor(later, 'kill')
                m.ready()
                m.tick()
                self.assertEqual(m.state(4), 'completed')

    def test_command_loss_takes_priority_over_same_tick_victory(self):
        for slug, m in self.missions():
            with self.subTest(mission=slug):
                m.establish()
                m.ready()
                # Economy and army completed earlier; assault is the final goal.
                m.g.commander.MarkCompletedObjective(1)
                m.g.commander.MarkCompletedObjective(2)
                m.command.IsDead = True
                m.tick()
                self.assertEqual(m.g.commander.result, 'lost')
                self.assertEqual(m.state(3), 'failed')
                self.assertNotIn('won', list(m.g.events.values()))

    def test_surviving_mcv_prevents_defeat_and_post_victory_callbacks_are_ignored(self):
        for slug, m in self.missions():
            with self.subTest(mission=slug):
                m.tick()
                self.assertIsNone(m.g.commander.result)
                m.establish()
                m.ready()
                m.tick()
                m.g.LoseActor(m.harvester, 'kill')
                m.tick(50)
                self.assertEqual(m.state(4), 'completed')
                self.assertEqual(m.g.commander.result, 'won')


if __name__ == '__main__':
    unittest.main()
