# Authored animation and damage pass

This pass targets the **24 implemented faction unit designs** and **39 building
designs**. The 15 additional aircraft, naval and beast concepts in the directional
art catalogue do not yet have gameplay actors and are outside this roster.

Artwork is generated with the built-in image-generation tool using the existing
original Sevenfall sprite sheets/buildings as design references. Exact prompts,
reference paths and intended outputs are recorded in `plan.json`. Source atlases
are preserved in `source/`; the deterministic packer only slices, scales and
packs them. It does not manufacture motion by translating a still image, or
manufacture damage by applying a dark filter.

## Frame layout

- Unit sources: eight facing columns (N, NE, E, SE, S, SW, W, NW), normally twelve pose rows.
  Rows 1–4 are movement keyframes; 5–8 attack or work-action keyframes; the
  remaining rows are collapse/destruction keyframes. Source row spacing is
  detected from alpha coverage. Three-pose deaths hold their final pose; five-pose
  deaths select four timing frames. Per-source row maps are recorded in the manifest. Unarmed MCVs/miners do not gain weapons.
- Vehicle and beast damage sources repeat those cycles with authored damage.
- Building sources: three equal-width cells, heavy damage, critical damage and
  rubble. The packer retains the original game image dimensions and base anchor.
- Exported unit frames are ordered by **state → facing → time**, matching OpenRA
  `Length: 4`, `Facings: -8`. Healthy movement starts at 0, attack/work at 32,
  death at 64. Damaged movement starts at 96 and damaged attack/work at 128.
- Every PNG export includes `FrameSize` and `FrameAmount` metadata. Source/export
  SHA-256 hashes and individual frame hashes are in `manifest.json`.

## Reproduce exports and bindings

```sh
npm install
npm run art:animations
python scripts/bind_animations.py
python scripts/generate_animation_test.py
python -m pip install -r requirements-test.txt
python -m unittest discover -s tests
python scripts/build.py build
```

`--available` on the packer and binder is for local iteration only. The normal
binder requires all 24 unit and 39 building exports before writing game bindings.
The installer copies the validated exports into the SDK's `art/animations/`.

## Runtime behavior and limits

Movement and firing use the corresponding OpenRA trait callbacks. Destroyed units
spawn a short-lived death actor that receives the parent's facing, plays the
collapse cycle, holds its final corpse/wreck pose, then disappears after six
seconds. Corpses are not production-capable or victory targets. Heavy damage
switches vehicle movement/attack frames; buildings have heavy and critical
variants, and repair returns them to their healthier artwork.

Four keyframes per state are a first animation pass. Distinct prone, idle,
parachuting, construction and repair animation cycles are not authored here.
Infantry retain their normal movement/firing cycles while under TakeCover.
Existing engine sounds, projectiles and generic effects still include Red Alert
placeholders; this pass does not make a standalone asset-clean release.

The **Sevenfall Animation Diagnostic** map exercises movement, attacks, heavy
damage, critical building damage, repair and death spawns. Its log is a scripting
and engine diagnostic, not evidence of campaign playability or visual perfection.
