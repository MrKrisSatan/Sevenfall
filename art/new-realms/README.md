# New realm painted artwork

All 51 current roster subjects have original raster sheets generated with the
built-in image-generation tool. `painted-prompts.json` records the exact prompts;
`painted-source/` retains the copied source PNGs. The original generated outputs
also remain in the creator's local generated-images directory.

`node scripts/prepare_realm_painted_art.cjs` technically crops, scales, anchors and
packs these sources; it does not synthesize painted content. It emits runtime
sprites, build icons, gallery WebP files and `painted-preview.png`.
`painted-manifest.json` records source and runtime SHA-256 hashes, dimensions and
individual frame hashes. Run `python scripts/bind_realm_painted_art.py` to bind
the renderers, including collectors, generic MCVs and construction yards.

Unit sources contain 8 directions by 4 states (idle, stride, action, wreck).
The 64-frame runtime layout alternates authored poses and holds one wreck pose
for three frames per direction. Building sources contain 6 states: intact,
damaged, critical, early construction, half construction, operating. Mobile
damaged/critical idle currently reuse the intact pose. Longer animation cycles,
dedicated mobile damage bodies and finer facing/weapon alignment remain polish.

The old SVG prototypes are retained as development history. Their generator is
guarded against overwriting this painted set. These assets cover the current
ground roster; aircraft/naval expansion is not part of this roster.
