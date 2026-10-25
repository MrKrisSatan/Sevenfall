"""Static skirmish contracts for Sevenfall's nine OpenRA faction choices.

These guard MiniYaml source relationships, not runtime behavior. A passing result
does not demonstrate successful harvesting, production, AI, combat or victory.
"""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
RULES = ROOT / "mods" / "sevenfall" / "rules"
SIDES = {
    "a": ("angels", ("a_seraph", "a_warden", "a_exile", "a_desolation"),
          "a_spire", "a_veilworks", "a_chapel", "a_armory", "a_gatherer",
          "a_watcher", "a_aegis"),
    "h": ("humans", ("h_bastion", "h_union", "h_covenant", "h_area52"),
          "h_generator", "h_veilworks", "h_barracks", "h_motorpool",
          "h_harvester", "h_rifleman", "h_bulwark"),
    "d": ("demons", ("d_legion", "d_brood", "d_court", "d_contempt"),
          "d_heart", "d_veilworks", "d_pit", "d_forge", "d_devourer",
          "d_thrall", "d_ravager"),
}
EXCLUSIVES = {
    "a_seraphim": "a_seraph", "a_gatekeeper": "a_warden",
    "a_penitent": "a_exile", "h_siegegun": "h_bastion",
    "h_ranger": "h_union", "h_templar": "h_covenant",
    "d_hellreaver": "d_legion", "d_skitter": "d_brood",
    "d_hexer": "d_court",
}


def load_actors():
    """Only top-level actors in Sevenfall sources, not inherited OpenRA actors."""
    result = {}
    for name in ("20-structures.yaml", "25-support-structures.yaml",
                 "30-units.yaml", "45-defenses.yaml"):
        source = (RULES / name).read_text(encoding="utf-8")
        matches = list(re.finditer(r"(?m)^([A-Z][A-Z0-9_]*):$", source))
        for i, match in enumerate(matches):
            actor = match.group(1).lower()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(source)
            if actor in result:
                raise AssertionError(f"Duplicate actor {actor}")
            result[actor] = source[match.end():end]
    return result


def trait(body, name):
    """Read a level-one MiniYaml trait's level-two fields."""
    match = re.search(
        rf"(?ms)^\t{re.escape(name)}:\n(.*?)(?=^\t[^\t#\n][^\n]*:|\Z)",
        body,
    )
    return match.group(1) if match else ""


def field(section, key):
    match = re.search(rf"(?m)^\t\t{re.escape(key)}: *([^\n]+)$", section)
    return match.group(1).strip() if match else None


def prerequisites(body):
    value = field(trait(body, "Buildable"), "Prerequisites")
    return set(part.strip() for part in value.split(",")) if value else set()


class SkirmishContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.actors = load_actors()
        cls.factions = (RULES / "10-factions.yaml").read_text(encoding="utf-8")
        cls.ai = (RULES / "40-ai.yaml").read_text(encoding="utf-8")

    def test_twelve_factions_start_with_provided_gates(self):
        expected = {f for side in SIDES.values() for f in side[1]}
        names = re.findall(r"(?m)^\t\tInternalName: ([ahd]_[a-z0-9]+)$", self.factions)
        self.assertEqual(set(names), expected)
        self.assertEqual(len(names), len(expected))

        world_start = re.search(
            r"(?m)^\tStartingUnits@mcvonly:\n\t\tFactions: ([^\n]+)",
            self.factions,
        )
        self.assertIsNotNone(world_start)
        self.assertEqual(set(world_start.group(1).split(", ")), expected)
        random_pool = re.search(
            r"(?m)^\t\tRandomFactionMembers: ([^\n]+)", self.factions
        )
        self.assertIsNotNone(random_pool)
        self.assertEqual(set(random_pool.group(1).split(", ")), expected)

        fact = self.factions.split("\nFACT:\n", 1)[1].split("\nMCV:\n", 1)[0]
        for letter, (parent, subfactions, *_) in SIDES.items():
            parent_gate = trait(fact, f"ProvidesPrerequisite@sf_{parent}")
            self.assertEqual(field(parent_gate, "Prerequisite"), f"sf.{parent}")
            self.assertEqual(
                set(field(parent_gate, "Factions").split(", ")),
                set(subfactions),
            )
            for sub in subfactions:
                individual_gate = trait(fact, f"ProvidesPrerequisite@sf_{sub}")
                self.assertEqual(field(individual_gate, "Prerequisite"), f"sf.{sub}")
                self.assertEqual(field(individual_gate, "Factions"), sub)

    def test_veilglass_economy_has_three_complete_paths(self):
        self.assertIn("Ore: 30", self.factions)
        self.assertIn("Gems: 55", self.factions)
        self.assertIn("Image: sf_veilglass", self.factions)
        for letter, (parent, factions, power, refinery, barracks, factory,
                     harvester, infantry, vehicle) in SIDES.items():
            for name in (power, refinery, barracks, factory, harvester,
                         infantry, vehicle):
                self.assertIn(name, self.actors, name)
            self.assertEqual(field(trait(self.actors[power], "Buildable"), "Queue"),
                             "Building")
            self.assertGreater(int(field(trait(self.actors[power], "Power"),
                                         "Amount")), 0)
            refinery_body = self.actors[refinery]
            self.assertIn("\tInherits: PROC", refinery_body)
            self.assertEqual(field(trait(refinery_body, "FreeActor"), "Actor"),
                             harvester.upper())
            self.assertIn("anypower", prerequisites(refinery_body))
            self.assertIn(f"~sf.{parent}", prerequisites(refinery_body))
            harvester_body = self.actors[harvester]
            self.assertIn("\tInherits: HARV", harvester_body)
            self.assertIn("\tWithHarvesterSpriteBody:", harvester_body)
            self.assertEqual(field(trait(harvester_body, "Buildable"), "Queue"),
                             "Vehicle")
            self.assertIn(refinery, prerequisites(harvester_body))
            self.assertIn("anypower", prerequisites(self.actors[barracks]))
            self.assertIn(refinery, prerequisites(self.actors[factory]))
            self.assertIn(barracks, prerequisites(self.actors[infantry]))
            self.assertIn(factory, prerequisites(self.actors[vehicle]))

    def test_every_buildable_has_legal_own_side_prerequisites(self):
        for name, body in self.actors.items():
            if not name.startswith(("a_", "h_", "d_")):
                continue
            gate = {p for p in prerequisites(body) if p.startswith("~sf.")}
            self.assertTrue(trait(body, "Buildable"), f"{name} missing Buildable")
            self.assertTrue(gate, f"{name} lacks faction gate")
            parent = SIDES[name[0]][0]
            expected = (f"~sf.{EXCLUSIVES[name]}" if name in EXCLUSIVES
                        else f"~sf.{parent}")
            self.assertEqual(gate, {expected}, name)
            for dependency in prerequisites(body):
                if dependency.startswith("~") or dependency == "anypower":
                    continue
                self.assertIn(dependency, self.actors,
                              f"{name} has missing prerequisite {dependency}")
                self.assertTrue(dependency.startswith(name[0] + "_"),
                                f"{name} depends on enemy {dependency}")

    def test_nine_exclusives_and_three_ai_supply_chains(self):
        for actor, subfaction in EXCLUSIVES.items():
            self.assertIn(actor, self.actors)
            self.assertEqual(
                {x for x in prerequisites(self.actors[actor]) if x.startswith("~sf.")},
                {f"~sf.{subfaction}"},
            )
        expected_modules = {
            "PowerTypes": 3, "RefineryTypes": 3, "BarracksTypes": 3,
            "VehiclesFactoryTypes": 3, "HarvesterTypes": 3,
        }
        for key, count in expected_modules.items():
            fields = re.findall(rf"(?m)^\t\t{key}: ([^\n]+)$", self.ai)
            self.assertTrue(fields, f"Missing bot field {key}")
            for entry in fields:
                actors = [value.strip() for value in entry.split(",")]
                self.assertEqual(len(actors), count, key)
                for actor in actors:
                    self.assertIn(actor, self.actors, f"{key}: {actor}")
                self.assertEqual({actor[0] for actor in actors}, set("ahd"))


if __name__ == "__main__":
    unittest.main()
