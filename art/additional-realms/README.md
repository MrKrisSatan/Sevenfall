# Four independent painted rosters

94 original painted RGBA atlases: 57 building sheets (including the Resonator) and 37 unit/MCV sheets. These replace the initial vector prototypes in game and on the website. None of these four factions has subfactions.

`painted-prompts.json` records every prompt and source path. `painted-source/` preserves the full-resolution built-in imagegen outputs. `painted-manifest.json` records source and packed hashes, dimensions and frame hashes. `painted-preview.png` is a contact sheet of the actual game-sized portraits.

Buildings have six authored construction, intact, active and damage states. Units have eight directions for idle, movement, action and wreck poses (32 authored cells); the packer arranges these into OpenRA's 64-frame sequences, holding wreck poses. Further animation interpolation and silhouette/scale polish remain possible; no mirrored frames are presented as newly authored views.

Rebuild using `node scripts/prepare_realm_painted_art.cjs additional-realms`, then `python scripts/prepare_extended_turnarounds.py`. Sharp performs extraction, alignment and resizing only. The website portraits are extracted from the original cells, rather than enlarged from the game sprites.

Veilborn uses living turquoise/violet crystal and gold veins; Unwritten uses pale silver memory architecture; Outer Silence uses obsidian and violet voids; Nephilim uses limestone, bronze and ochre monumental architecture.

Original game art is distributed under the repository's artwork license. These are development assets, not additions to the already published alpha.3 package.
