# Building Sevenfall 0.3 development candidate

This is a working engine integration milestone, not a finished standalone game.
Standalone staging uses original Sevenfall graphics and terrain, deliberately limited
alpha audio, and adapted GPL OpenRA definitions. No Red Alert installation is required.

## Requirements

- Git and Python 3.10 or later.
- .NET SDK 10.0.402 (runtime 10.0.13). Sevenfall's reviewed engine overlay targets net10.0.
- Windows x64 or Linux x64 with OpenRA's SDL2/OpenAL/OpenGL prerequisites.
- No external game-content installer is required.

The SDK and engine are cloned into ignored `.sdk/` directories and verified against
exact commits by `scripts/build.py`. Existing checkouts at another commit are rejected.
The [reviewed engine overlay](packaging/engine/README.md) is applied and hash-verified
automatically; all other engine source changes are rejected when packaging.

| Dependency | Version | Commit |
|---|---|---|
| OpenRAModSDK | 20250330 | 0059e22e0e3bfc862500aaaa9fe1aed4ea4e994a |
| OpenRA | release-20250330 | b4f3d8ae02b6bd6f4a3a5441e6d0daf7c5073787 |

## Windows

You can double-click `PLAY_SEVENFALL_DEV.cmd` in the repository root to run
source tests, build the pinned SDK and launch the local prototype in order.
Alternatively, run the commands manually:

```powershell
py -3 scripts/build.py build
py -3 -m pip install -r requirements-test.txt
py -3 -m unittest discover -s tests
py -3 scripts/build.py launch
```

For a custom .NET installation, append `--dotnet C:\path\to\dotnet.exe`.
The current development workstation has a private SDK/runtime under `.tools/dotnet`,
which the script detects automatically. Python is available in the Codex bundled runtime.

## Linux

```sh
python3 scripts/build.py build
python3 -m pip install -r requirements-test.txt
python3 -m unittest discover -s tests
python3 scripts/build.py launch
```

Linux commands are provided but not yet executed on Linux. The Python build command
invokes the same engine solution and `--check-yaml` utility used by SDK all/test;
the unmodified SDK itself remains available in `.sdk`. The build wrapper also compiles `code/OpenRA.Mods.Sevenfall`, which implements deterministic defense auras and infantry conversion. Use the wrapper rather than building the SDK alone.

## Play the prototype

Choose Singleplayer → Skirmish, select **Broken Choir - Proving Ground**, select a
Sevenfall faction and add **Sevenfall AI (prototype)** to the other slot. Start with
MCV-only units and 5,000 credits. Deploy the MCV, build power, a refinery, and infantry
production. The refinery provides the matching mining unit. Build a vehicle factory
to replace miners and produce armor. Both resource grades feed one currency:
rough Veilglass is worth 30 credits per resource unit and enriched Veilglass 55.

The arena is deliberately flat and symmetric for economic testing. It has equal
starting deposits, exposed expansion deposits, and a central enriched basin. It is
not yet the finished asymmetric Broken Choir battlefield.

For artwork inspection, choose **Sevenfall Building Gallery**. Its three player slots
are locked to Angels, Humans and Demons, with each faction's complete current building
roster preplaced. Naval facilities sit in the southern water strip. This is a developer
gallery without an economy, not a normal skirmish map. See [building coverage](art/BUILDINGS.md).

Launch defaults to a 1280×720 window and a double-size **software cursor**. This fixes
the invisible hardware cursor observed on the development workstation. Resize or
change display mode through Settings after launch if desired.

## Campaign preview missions (0.3 source integration)

After a successful build, open **Singleplayer → Missions** or the mission selector and select one of the new campaign previews:

| Campaign | Preview | Locked faction | Enemy |
|---|---|---|---|
| Ashes of Earth | **H03: The Glass Fields** | Free Earth Union | Blood Brood |
| War in Heaven | **A03: A Glass of Wrath** | Order of the Gate | Blood Brood |
| The Ninth Mouth | **D02: Seeds of Ruin** | Blood Brood | Bastion Directorate |

The SDK stages all 39 directional reference sheets and the 63 authored animation/damage exports. All 24 implemented faction unit designs now have movement, attack/work and death cycles; all 39 building designs have heavy and critical damage states. See [animation frame layout and limitations](art/animations/README.md).

The campaign preview missions use **Broken Choir prototype terrain copied into
the local SDK during installation**, not yet authored story maps. Their source
folders contain `map.yaml` and `mission.lua`. The installer stages the required
`map.bin` from the repository's original arena. No new map binary or proprietary
assets are downloaded from a third party.

**Prototype scripted objectives:** deploy a construction yard, construct faction
power and refinery, refine at least **900 credits of physically gathered
Veilglass**, build the faction barracks and vehicle factory, produce both required
combat units, and destroy the enemy Construction Yard. There is a secondary
objective to keep the first refinery and at least one harvester alive. Loss of
all own construction yards and MCVs fails the scenario.

**Important test caveat:** currently the script observes increases in a player's
stored resource credits rather than a dedicated harvester-unload callback. It
cannot *independently* prove that two separate unloading cycles occurred. The
nine-faction runbook still requires visual confirmation of two complete trips.
Enemy AI is the existing prototype `sevenfall` bot, whose complete campaign
behavior must still be verified during a real match. Lua mission scripts have
not yet been observed running to a full win/loss on a Windows desktop.

### Windows validation steps

1. Clone the repository, install Python 3, Git, .NET 8 SDK and .NET 6 runtime.
2. Run `py -3 -m pip install -r requirements-test.txt`, then
   `py -3 -m unittest discover -s tests`. Mission behavior tests run the actual
   scripts under Lua 5.1 against a limited OpenRA API double; they do not
   simulate engine scheduling, harvesting, combat or AI.
3. Run `py -3 scripts/build.py build` to populate the pinned SDK, copy the
   three campaign map binaries, compile OpenRA and execute engine YAML lint.
4. Run `py -3 scripts/build.py launch` and select a campaign preview.
5. Complete **all three** scripted objectives and one failure test for each map.
   Confirm enemy AI behavior, combat damage, harvest/unload income and log errors
   before marking a scenario PLAYABLE.
6. Record results against [the 0.3 acceptance log](tests/FIRST_WAR_RUNBOOK.md).
   A CI compile/lint pass is **not** proof of an interactive working build.

The existing reproducible Windows workflow compiles the pinned engine in GitHub
Actions. No independently installable, asset-clean Windows release archive has
been published. Source development needs the SDK/runtime; the portable Windows
candidate bundles its own runtime and content.

## Portable Windows candidate and native diagnostics

After `scripts/build.py build`, run:

```powershell
python scripts/package_windows.py --profile development --version 0.3.0-alpha.1
python scripts/run_defense_test.py --scenario environment --package dist/Sevenfall-0.3.0-alpha.1-windows-x64 --support-dir artifacts/portable-test
```

The package contains `Sevenfall.exe` and a local `Support` directory. Packaging
requires committed Sevenfall and unmodified pinned engine/SDK source (the generated
SDK configuration and mod overlay are allowed). It rebuilds/restages the game before
copying assets and the extension, and records all three commits in `BUILD_INFO.json`.
The default .NET command uses `.tools/dotnet/dotnet.exe` when present, otherwise
`dotnet` from PATH. Pass `--dotnet PATH` to select another installation.
Packaging
refuses external RA manifest references and proprietary game archive formats.
It creates a ZIP, file inventory and SHA-256 checksum; these do not imply release
approval. Use a fresh version suffix when rebuilding to preserve prior candidates.
Commit the tested sources, then run `scripts/package_source.py --version VERSION`
to bundle Sevenfall and the pinned engine/SDK sources. Third-party dependency
source and licence verification remains separate.

Native scenarios are `environment`, `release`, `defense`, `production`, and `match`.
The first three have passed with fresh support folders. `production` exercises
normal paid queues and validated placement; `match` observes unassisted AI conquest.
Use longer `--timeout` values for those scenarios. For source builds, pass
`--dotnet PATH` instead of `--package PATH`.

The default packaging profile is `skirmish`: only the three playable skirmish maps
and menu are included. Use `--profile development` for the diagnostic command above.
Additional native scenarios include `doctrine`, `subproduction`, `terrain` and
`twelve`; see [the twelve-player map notes](docs/TWELVEFOLD_SCAR.md).
The `Windows skirmish candidate` workflow produces a setup EXE, portable archive,
source archive and checksums. It checks installation, reinstallation and removal
with preserved user data. It does not publish a release or replace clean-PC testing.

## Validation and remaining work

Use the [nine-faction skirmish runbook](tests/SKIRMISH_RUNBOOK.md) to record
real economy, combat, AI and victory results. All cases begin as NOT RUN.

See [the integration report](tests/INTEGRATION_REPORT.md). Passing engine lint does
not prove harvesting, balance, victory, replay safety or AI quality. The next milestone
is measured end-to-end economy/combat testing for all three parent factions, followed
by the nine-faction matrix. Animation polish, the remaining 72 campaign missions, defense balance,
expansion MCVs, support powers and superweapons remain future work.

Sources: [OpenRA SDK](https://github.com/OpenRA/OpenRAModSDK),
[OpenRA stable release](https://www.openra.net/news/release-20250330/).

## Animation diagnostic

Choose **Sevenfall Animation Diagnostic** from the skirmish map list, or launch
the installed SDK with `Launch.Map=animation-test`. This developer-only map
orders movement and attacks, applies heavy and critical damage, repairs buildings,
and kills units to check all 24 death actor spawns. Inspect `Logs/lua.log` for
`ANIMATION_DIAGNOSTIC PASS`. This diagnostic does not prove campaign completion.

To rebuild authored exports: `npm install`, `npm run art:animations`, then
`python scripts/bind_animations.py`. Run source tests and the engine build afterward.

## Additional faction doctrines

Choir of Desolation, Area Fifty Two and Circle of Contempt are additive lobby choices.
See [roles, controls and counters](docs/SUBFACTIONS.md). For Area Fifty Two, select
a powered Containment Pylon and use Deploy (F) to switch SERAPH/ABYSS. The oldest
powered pylon controls the army; switching pauses Janus fire for three seconds.

Native acceptance: `python scripts/run_defense_test.py --scenario doctrine --support-dir artifacts/doctrines`
and `python scripts/run_defense_test.py --scenario subproduction --support-dir artifacts/subproduction --timeout 650`.
The latter uses real paid construction, placement and harvesting for the three new choices.
