# SEVENFALL: The War for Creation

> Historical v0.1 starter notes. Current setup and results are in [BUILDING.md](BUILDING.md) and [the integration report](tests/INTEGRATION_REPORT.md).

**OpenRA pre-alpha technical seed • 2026-10-21 • original RTS concept**

**Status: SOURCE STARTER, NOT A FINISHED OR ENGINE-VERIFIED GAME.** Static checks on this archive have passed, but an actual OpenRA build/launch could not be run in this environment. The mod uses Red Alert placeholder visuals, maps and engine content; original art/audio, campaigns, functional AI and complete trait implementations are future milestones.

## Contents

- `design/MASTER_BUILD_PROMPT.md` — comprehensive coding-agent prompt; use this to continue building and testing.
- `design/GAME_DESIGN.md` — world, Veilglass economy, nine factions, tech, units, campaigns and milestones.
- `mods/sevenfall/rules/10-factions.yaml` — nine lobby subfactions, first tech gate rules, Veilglass credit values.
- `mods/sevenfall/rules/20-structures.yaml` — 12 faction-specific production/economy/power building variants.
- `mods/sevenfall/rules/30-units.yaml` — 21 first-pass units including 3 harvesters, 9 subfaction-exclusives.
- `mods/sevenfall/weapons/sevenfall.yaml` — six prototype weapon stat sets.
- `mods/sevenfall/fluent/sevenfall.ftl` — names/descriptions for factions, actors, resource.
- `scripts/install_into_sdk.py` — constructs SDK-registered overlay with original RA mod files and hides old RA units from build palettes.
- `scripts/check_project.py` — static consistency checks (not an engine simulation).
- `tests/` — planned integration test checklist.

## Windows setup (SDK + Python 3 required)

1. Obtain the OpenRA Mod SDK: https://github.com/OpenRA/OpenRAModSDK . Follow the SDK's current documentation. Work with a compatible SDK/engine commit.
2. In the SDK directory run `make.cmd`, then choose `all`. This populates/compiles the SDK engine and dependencies; you need internet when fetching it.
3. Unzip this archive to any folder and open a command prompt inside the unzipped folder.
4. Run `py -3 scripts\check_project.py`.
5. Run `py -3 scripts\install_into_sdk.py "C:\path\to\OpenRAModSDK"`, replacing the path with your own SDK folder.
6. Back in the SDK folder run `make.cmd`, choose `all`, then run it again and choose `test`.
7. Run `launch-game.cmd`, choose the Sevenfall game, and try a built-in Red Alert skirmish map with MCV-only starting units.
8. If it fails, use the first full error log to patch the MiniYaml or engine mismatches. Do not assume this pre-alpha compiles unmodified across releases.

### Linux/macOS setup

Follow the SDK's platform prerequisites. Run `make` in the SDK root first, then `python3 scripts/check_project.py`, `python3 scripts/install_into_sdk.py /path/to/OpenRAModSDK`, then `make && make test` in the SDK root and finally `./launch-game.sh`.

**Important:** The package's script overwrites `mods/sevenfall` and alters SDK `mod.config` to target Sevenfall. Use a separate SDK checkout dedicated to this mod and keep your original example for reference. It copies no Red Alert licensed asset files into this ZIP. The game may ask for legal Red Alert content when launching.

## Why the mod is an overlay

Official OpenRA documentation recommends an overlay using a base game instead of building the entire rules, UI, tilesets and renderer from zero on day one. Our first step uses the Red Alert economy and unit behaviors as scaffolding but creates original faction IDs, gating, actors, stats and locale strings. When the first gameplay loop is running, replace the inherited RA models, maps, rules and UI with wholly original assets and definitions.

## Known unfinished systems

- The three main faction tech trees are skeletal, not full roster implementations. Most original visuals are temporarily shared and not faction-identifiable yet.
- Nine subfactions each offer one exclusive actor, but **subfaction passives, special buildings and special powers are design-only**.
- New Veilglass graphics, custom deposit generation, radiation hazards and faction purity/corruption mechanics are not yet implemented. In prototype, RA Ore and Gems are two grades of Veilglass using RA sprite placeholders.
- Skirmish AI still references RA actor IDs and will need rewritten bot plans; don't interpret AI failure as balanced gameplay.
- First-play testing, build validation, AI testing, original maps and all campaign missions are not completed.
- The prototype shares RA map support and content requirements; it is not a standalone original asset release.

## Next development checkpoint

In an SDK checkout: verify all nine factions appear, that each starts with MCV → construction yard, builds power → refinery, spawns a side-specific harvester, completes one full gather/unload loop, builds infantry production and fights one opposing player. Resolve every runtime and missing-asset error before expanding the roster.

## Sources

- OpenRA Mod SDK: https://github.com/OpenRA/OpenRAModSDK
- Mod SDK Getting Started: https://github.com/OpenRA/OpenRAModSDK/wiki/Getting-Started
- OpenRA traits: https://docs.openra.net/en/playtest/traits/

**Licensing:** project design/content independently authored; OpenRA engine source GPLv3; temporary RA visuals/content must be acquired via permitted existing game content installation. Do not repackage proprietary RA art, music or sound effects in a distributed original game.
