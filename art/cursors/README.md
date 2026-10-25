# Sevenfall vector cursors

Original geometric UI symbols authored in `scripts/build_cursors.cjs`, licensed
GPL-3.0-or-later. These contain no Red Alert sprite pixels or palette data.
`names.json` lists the 77 engine cursor identifiers supported by the current
rules and UI. Minimap and blocked variants are included. States are static.

Rebuild using Node.js with `sharp` installed:

```
node scripts/build_cursors.cjs
```

Outputs: editable SVG atlas, RGBA PNG atlas with OpenRA frame metadata, and
MiniYaml bindings. Pointer hotspots align with the arrow tip; action cursors
use the center. Existing software-cursor launch settings are retained.
Native visibility/hotspot acceptance still needs testing in the game.
