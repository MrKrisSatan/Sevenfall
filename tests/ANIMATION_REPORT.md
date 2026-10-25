# Sevenfall animation and damage verification — 25 October 2026

Implemented in the local branch `fix/campaign-objective-lifecycle`, based on upstream `b53ac9d`.

## Delivered scope

- 24 implemented faction unit designs: eight directions, movement, attack/work and death cycles.
- 13 damaged unit variants (vehicles/logistics and beast designs).
- 39 building designs: authored heavy damage, critical damage and rubble.
- 3,669 packed frames across 63 exported PNG sheets, from 76 preserved source atlases.
- Original bodies/icons for all implemented units, facing-preserving death actors, six-second corpse/wreck lifetime, repair-aware building state changes.
- Source prompts, hashes, row mappings, deterministic packing/binding scripts, installer validation and an offline preview generator.

The 15 additional aircraft, naval and beast concepts without gameplay actors remain outside the implemented roster.

## Verification actually performed

- 43 Python tests: PASS, including all-roster coverage, source/export hashes, PNG metadata, distinct timing frames, campaign Lua decisions and original visual bindings.
- Pinned OpenRA build on Windows: PASS (SDK `0059e22e0e3bfc862500aaaa9fe1aed4ea4e994a`, engine `b4f3d8ae02b6bd6f4a3a5441e6d0daf7c5073787`). Existing .NET SDK 7.0.401 compiled the engine; native execution used .NET 6.0.22, SDL2, OpenGL and NVIDIA RTX 3060.
- OpenRA YAML/Fluent checks: PASS without warnings for eight maps and four tilesets.
- `--check-missing-sprites`: PASS for SNOW, INTERIOR, TEMPERAT and DESERT.
- Native animation diagnostic: PASS through movement, attacks, heavy unit/building damage, critical building damage, repair and **24 spawned unit death actors**. Repeated after final death-image bindings.
- Native rendered unit wrecks/corpses inspected through Computer Use; no old tank turret overlays or opaque sprite rectangles observed in that inspection.
- `git diff --check`: PASS.

The diagnostic is an isolated engine/script exercise. It is not a complete skirmish, campaign victory, balance test or pixel-by-pixel visual acceptance of every frame.

## Art and implementation notes

The built-in image-generation tool authored the pose/damage changes from original Sevenfall references. No API-key fallback was used. A missing Bulwark damaged death row was corrected before packing. Some source sheets contain 11 or 13 pose rows rather than 12; the packer records their actual bands and selects four death timing frames from three to five authored poses. A three-pose death holds its final pose rather than inventing a new motion frame.

Idle art and animation art share the intended draw size. Production icons were adjusted to avoid double-scaling already normalized sprites. Infantry under TakeCover use their normal movement/attack cycles; separate prone, parachute, idle and building construction cycles remain future work. Unarmed MCVs and miners gain no weapons; their action frames represent work.

Damage variants and animation cycles are an initial AI-authored art pass. Further gait, facing consistency, effects and visual polish remain appropriate. Existing sounds, generic effects and projectile assets still include engine/Red Alert placeholders. No standalone or asset-clean release is claimed.

## Reproduce

```text
npm install
npm run art:animations
python scripts/bind_animations.py
python scripts/generate_animation_test.py
python -m pip install -r requirements-test.txt
python -m unittest discover -s tests
python scripts/build.py build
```

Open **Sevenfall Animation Diagnostic** from the skirmish map list. Its automatic exercise writes `ANIMATION_DIAGNOSTIC PASS` to the support directory's `Logs/lua.log` after checking the 24 death actors. The developer build uses locally installed game content; that content is not included in source archives.

An offline viewer is generated with `python scripts/build_animation_preview.py --output PATH`.
