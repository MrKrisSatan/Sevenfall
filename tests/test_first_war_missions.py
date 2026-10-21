"""Contract tests for the first three source-backed Sevenfall 0.3 Lua scenarios.

Source-level tests and OpenRA --check-yaml cannot prove gameplay, but they
prevent mission-selector, binary-map and production-rule regressions.
"""
from pathlib import Path
import importlib.util
import re
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "mods" / "sevenfall"
PROJECT = ROOT / "scripts" / "install_into_sdk.py"
spec = importlib.util.spec_from_file_location("sevenfall_installer", PROJECT)
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)

SCENARIOS = {
    "h03-glass-fields": {
        "faction": "h_union", "opponent": "d_brood",
        "power": "h_generator", "refinery": "h_veilworks",
        "infantry": "h_rifleman", "vehicle": "h_bulwark",
        "harvester": "h_harvester", "title": "The Glass Fields",
    },
    "a03-glass-wrath": {
        "faction": "a_warden", "opponent": "d_brood",
        "power": "a_spire", "refinery": "a_veilworks",
        "infantry": "a_watcher", "vehicle": "a_aegis",
        "harvester": "a_gatherer", "title": "A Glass of Wrath",
    },
    "d02-seeds-ruin": {
        "faction": "d_brood", "opponent": "h_bastion",
        "power": "d_heart", "refinery": "d_veilworks",
        "infantry": "d_thrall", "vehicle": "d_ravager",
        "harvester": "d_devourer", "title": "Seeds of Ruin",
    },
}


class FirstWarMissionContracts(unittest.TestCase):
    def test_mission_selector_contains_three_named_campaigns(self):
        missions = (MOD / "missions.yaml").read_text(encoding="utf-8")
        self.assertEqual(re.findall(r"(?m)^\t([a-z0-9-]+)$", missions),
                         list(SCENARIOS))
        self.assertIn("Ashes of Earth (0.3 preview):", missions)
        self.assertIn("War in Heaven (0.3 preview):", missions)
        self.assertIn("The Ninth Mouth (0.3 preview):", missions)
        installer_text = PROJECT.read_text(encoding="utf-8")
        self.assertIn("('Missions', 'missions.yaml')", installer_text)
        self.assertIn("'Version: 0.3-dev'", installer_text)

    def test_maps_have_real_actor_rosters_and_objective_scripts(self):
        for slug, data in SCENARIOS.items():
            with self.subTest(mission=slug):
                folder = MOD / "maps" / slug
                yaml = (folder / "map.yaml").read_text(encoding="utf-8")
                lua = (folder / "mission.lua").read_text(encoding="utf-8")
                self.assertIn("Visibility: MissionSelector", yaml)
                self.assertIn("LockFaction: True", yaml)
                self.assertIn("Playable: True", yaml)
                self.assertIn("Required: True", yaml)
                self.assertIn("Faction: " + data["faction"], yaml)
                self.assertIn("Faction: " + data["opponent"], yaml)
                self.assertIn("Bot: sevenfall", yaml)
                self.assertIn("Scripts: mission.lua", yaml)
                self.assertIn("MissionObjectives:", yaml)
                self.assertIn("-ConquestVictoryConditions:", yaml)
                self.assertIn("-SpawnStartingUnits:", yaml)
                self.assertIn("CommanderMcv: mcv", yaml)
                self.assertIn("EnemyYard: fact", yaml)
                self.assertIn(data["power"], lua)
                self.assertIn(data["refinery"], lua)
                self.assertIn(data["infantry"], lua)
                self.assertIn(data["vehicle"], lua)
                self.assertIn("WorldLoaded = function()", lua)
                self.assertIn("Tick = function()", lua)
                self.assertIn("Trigger.OnAnyProduction(", lua)
                self.assertIn("commander.Resources", lua)
                self.assertIn("refinedCredits >= 900", lua)
                self.assertIn("Has(\"fact\")", lua)
                self.assertIn('GetActorsByType("fact")', lua)
                self.assertIn("MarkCompletedObjective(", lua)
                self.assertIn("MarkFailedObjective(", lua)
                self.assertIn("AddSecondaryObjective(", lua)
                self.assertNotIn("commander.Resources = ", lua)
                # Actual Lua should never credit the player directly.
                self.assertNotIn("commander.Cash = commander.Cash +", lua)

    def test_mission_terrain_is_generated_without_modifying_source(self):
        terrain = MOD / "maps/broken-choir/map.bin"
        original = terrain.read_bytes()
        with tempfile.TemporaryDirectory() as name:
            output = Path(name)
            for slug in SCENARIOS:
                dest = output / "maps" / slug
                dest.mkdir(parents=True)
                for source in ("map.yaml", "mission.lua"):
                    (dest / source).write_bytes((MOD / "maps" / slug / source).read_bytes())
            installer.install_campaign_map_binaries(output)
            for slug in SCENARIOS:
                binary = output / "maps" / slug / "map.bin"
                self.assertEqual(binary.read_bytes(), original)
        self.assertEqual(terrain.read_bytes(), original)

    def test_original_unit_sheet_staging_matches_sources(self):
        source = ROOT / "art" / "unit-turnarounds" / "sheets"
        originals = sorted(source.glob("*.png"))
        self.assertEqual(len(originals), 39)
        with tempfile.TemporaryDirectory() as name:
            dest = Path(name)
            count = installer.stage_original_unit_turnarounds(dest)
            self.assertEqual(count, 39)
            staged = dest / "art" / "unit-turnarounds"
            self.assertEqual({f.name for f in staged.glob("*.png")},
                             {f.name for f in originals})
            for name in ("a-watcher", "h-rifleman", "d-thrall",
                         "a-aegis", "h-bulwark", "d-ravager"):
                self.assertEqual((staged / (name + ".png")).read_bytes(),
                                 (source / (name + ".png")).read_bytes())

    def test_all_player_and_opponent_actors_exist_in_sevenfall_rules(self):
        from test_gameplay_contract import load_actors
        actors = load_actors()
        for slug, data in SCENARIOS.items():
            yaml = (MOD / "maps" / slug / "map.yaml").read_text(encoding="utf-8")
            for name in re.findall(r"(?m)^\t(?:Enemy|Commander)\w+: ([a-z0-9_]+)$", yaml):
                if name in {"fact", "mcv"}:
                    continue
                self.assertIn(name, actors, (slug, name))


if __name__ == "__main__":
    unittest.main()
