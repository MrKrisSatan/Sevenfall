# The Twelvefold Scar

A 256×256 land skirmish for up to twelve players, with twelve equivalent starting
terraces and all twelve faction choices available through normal production.
The map uses the existing environment families: both civilian houses, all four
tree types, both bridge orientations and repair posts, water, Veilglass and enriched
Veilglass. Units and defenses are built by players rather than preplaced as scenery.

Each starting terrace has four seven-cell entrances, a clear MCV deployment area
and 20,880 credits of starting Veilglass. Twelve expansion deposits lead toward
the orbital road. Four enriched fields reward control of the central terrace.
Four destructible, repairable bridges cross its canals; alternate land routes keep
every starting position connected even if all four bridges collapse.

The original sixteen-frame cliff atlas marks terrace edges and eroded outcrops.
Its 1,436 cliff cells use native impassable Rock terrain, blocking infantry,
harvesters and tracked vehicles. Upper surfaces visually indicate raised ground.
The current rectangular engine grid has no actual height layer or high-ground
range/damage bonus. This pass does not change line-of-sight height rules.

Source: `scripts/generate_twelvefold.py`; artwork provenance and hashes are in
`art/terrain/cliff-prompt.json` and `cliff-manifest.json`. Export artwork using
`node scripts/prepare_cliffs.cjs`, regenerate the map, then regenerate its two
development diagnostics with `python scripts/generate_twelvefold_tests.py`.

## Acceptance

Seven Python contracts check clear starts, equal starting resources, accessible
deposits, terrain/prop separation, environment coverage and connectivity with
all bridges present or destroyed. The native `terrain` scenario adds 27 checks:
terrain rejection, actual routing through gates, twelve MCV deployments, loaded
environment props and a delayed-projectile regression. The latter caught and
fixed a doctrine crash when a projectile outlived its shooter.

The autonomous `twelve` scenario starts all twelve faction bots with equal cash.
It observes deployment, harvesting, army production and combat for five game
minutes without scripted production or attack orders. This soak is not a completed
conquest, replay, multiplayer or balance certification. The 25 October native run
passed all 49 checks, with 214 attributed kills and all twelve economies and armies
observed. Continuous gravel replaces the striped roads seen during that run;
terrain types, resources and connectivity are unchanged.

```powershell
python scripts/run_defense_test.py --scenario terrain --support-dir artifacts/cliffs --timeout 120
python scripts/run_defense_test.py --scenario twelve --support-dir artifacts/twelve --timeout 750
```

## Windows distribution

The default `skirmish` packaging profile includes Broken Choir, Ashen Crossing,
The Twelvefold Scar and the menu map. It excludes diagnostics and campaign previews.
Use `--profile development` when packaging a native diagnostic.
The Windows candidate workflow compiles a per-user setup EXE with the runner's
preinstalled Inno Setup, verifies the exact package, tests installation/reinstallation/
uninstallation while preserving settings and saves, and bundles corresponding
project/engine source and checksums. Its artifacts are test candidates, not public
GitHub Releases. Remaining publication gates are in [RELEASE_BLOCKERS.md](RELEASE_BLOCKERS.md).
