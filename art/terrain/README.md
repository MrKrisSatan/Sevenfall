# Original alpha terrain

Two original textures generated with the built-in imagegen tool on 2026-10-25.
Ground prompt: seamless overhead muted olive-grey dirt, sparse grey-green grass,
tiny stone flecks, uniform diffuse lighting, low contrast, no focal objects or
grid, designed for a 24px dark-fantasy RTS tile. Water prompt: seamless overhead
dark slate-teal water, fine low-contrast ripples, no shore, objects or horizon,
uniform overcast lighting, designed for a 24px repeating tile.

`source/` preserves the generated images. `manifest.json` records SHA-256 hashes
of sources and packed exports. `node scripts/prepare_terrain.cjs` (requires sharp)
exports sixteen 24px ground samples and one 24px water sample. Tileset bindings
retain IDs 255/65535 (clear) and 1 (water) used by the current original maps.

The environment extension adds an authored atlas of grass, dirt, ash, gravel, stone roads, dirt paths and cliff faces; four trees; two civilian houses; and two bridge orientations. House and bridge sheets contain intact, light damage, heavy damage and destroyed states. All were generated with built-in imagegen on 2026-10-25, then technically cropped, resized and packed with sharp by `scripts/prepare_environment.cjs`. No damage artwork was synthesized by the packer.

`environment-manifest.json` records source and export hashes. Source variants are preserved for provenance. The atlas includes unused flat bridge samples; gameplay uses destructible bridge actors instead. House and bridge damage edits used the intact generated designs as references, requesting consistent material, footprint and camera direction across all four states.

Shore transitions, cliff junctions, seams and damage anchors still need native camera-scale review. Distribution-rights/content licensing review remains part of release clearance. See `design/ENVIRONMENT.md` for gameplay and acceptance limits.
