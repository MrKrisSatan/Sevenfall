# Shared arsenal source art

Twenty accepted sprite sheets created using the built-in image-generation tool.
Exact prompts are in `painted-prompts.json`, copied original PNGs in
`painted-source/`, and source/runtime SHA-256 hashes in `painted-manifest.json`.
The original tool outputs remain in the local Codex generated-images directory.

Use `node scripts/prepare_realm_painted_art.cjs realm-completion` to crop, anchor,
resize and pack the source cells for OpenRA. This technical importer does not
synthesize painted content. It also produces build icons and gallery WebP images.

Units use 8 directions by 4 authored states, packed into the existing 64-frame
sequence layout with alternating idle/stride and action/rest poses, and held
wrecks. Buildings and effects contain 6 authored states. The Witness effect
opens three pairs of wings; nuclear effects include a descending missile and
mushroom cloud. Animation and sound polish remain ongoing.

The image service rejected the proposed human silo sprite (violence category).
No blocked asset was used; the human installation intentionally uses the existing
human technology-building sprite. Its gameplay and nuclear effect are implemented.
