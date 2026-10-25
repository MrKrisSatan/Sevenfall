# Original additional-subfaction art

Nine original game assets: six units and three defenses, generated with the built-in
OpenAI image tool. Exact prompts and relative source paths are in `prompts.json`;
`catalogue.json` contains gameplay roles. `manifest.json` records source/export
SHA-256 and individual packed-frame hashes. No external game artwork is included.

Unit sources have eight views and eight pose rows. Technical packing produces
64 frames: eight standing views, sixteen walking, sixteen firing and twenty-four
destruction/corpse frames. Defenses have six authored intact/damage/pulse states.
The packer accepts fractional source cell boundaries caused by transparent-output
cropping, aligns the authored silhouettes, exports icons and makes web previews.
It does not synthesize poses or damage art. Initial facing/animation polish remains.

Run `npm run art:subfactions`, `python scripts/build_subfactions.py` and
`python scripts/build_site_catalogue.py`. Rules are separate from the earlier
animation/defense manifests, preserving their original provenance.

See `docs/SUBFACTIONS.md` for mechanics, controls, counters and acceptance scope.
Original-content licensing follows the project's existing distribution review.
