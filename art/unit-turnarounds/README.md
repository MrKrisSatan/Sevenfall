# Eight-direction unit artwork

This library covers **39 unit designs / 312 directional images**: the current
24-unit roster plus 15 new naval, aerial and kennel concepts. Each parent faction
has 13 designs. The existing six MCV/harvester turnarounds are reused; 33 new
turnaround sheets were generated with the built-in OpenAI image generation tool.

[Browse the interactive gallery](https://mrkrissatan.github.io/Sevenfall/turnarounds.html).

## Files and orientation

- `roster.json`: names, categories, source paths and intended roles.
- `prompts.json`: exact generation prompts and original concept references.
- `corrections.json` and `corrections-extra.json`: targeted image-generation corrections after visual review.
- `manifest.json`: source/derived SHA-256 hashes, extraction bounds and frame paths.
- `frames/<unit>/{n,ne,e,se,s,sw,w,nw}.png`: eight individual transparent 256×256 PNGs.
- `sheets/<unit>.png`: a 1024×128 strip of eight 128×128 frames, containing OpenRA
  `FrameSize=128,128` and `FrameAmount=8` PNG metadata.
- `../../docs/assets/turnarounds/<unit>.webp`: optimized 4×2 viewing atlas.

Direction order is **N, NE, E, SE, S, SW, W, NW**, clockwise from north. North
shows the back of the unit travelling away/up. OpenRA sequences using these strips
need `Facings: -8`, matching the established logistics sheets. Bodies and weapons
are baked together; these are not separate turret layers.

The packer detects eight connected silhouettes, keeps nearby disconnected details,
and applies a common scale across all eight facings of a unit. It only slices,
resizes and packs; it never fabricates directions by mirroring or rotating a flat
image. Inspection is still necessary for orientation and design consistency.

## New concepts

| Role | Angels | Humans | Demons |
|---|---|---|---|
| Surface vessel | Tidebreaker | Breakwater Destroyer | Dreadwake |
| Submersible | Tideveil | Deepwatch Submarine | Leviathan Submersible |
| Vertical aircraft | Halo Skimmer | Kestrel Gunship | Harpy |
| Fixed-wing aircraft | Dawnwing | Stormhawk Fighter | Hellwing |
| Kennel beast | Guardian Gryphon | Patrol Hound | Hellhound |

These names and roles are an initial art roster, not balanced or buildable game
actors. Naval hulls are shown surfaced without wakes; aircraft use one flight pose.
The existing Demon Ravager, Hellreaver and Skitter are included alongside the new
kennel beasts. All nine subfaction exclusives are included.

## Integration boundary

This reference pack preserves **directional images**. The separate
[animation and damage pass](../animations/README.md) now integrates movement,
attack/work and death cycles for all 24 implemented faction unit designs, plus
vehicle and building damage artwork. These source views remain useful for idle
poses, icons and design references. The 15 expanded naval, aircraft and beast
concepts still need gameplay actors. Separate prone/flight cycles, turret layers,
team colours and further visual polish remain future work.

Original concept references and generated source sheets are retained. Corrected
`-v2` sources supersede their first drafts where selected by `roster.json`.
Original-content licensing remains unchanged. No borrowed game artwork is included.

## Rebuild

```sh
npm install
npm run art:units
python scripts/build_turnaround_gallery.py
python -m pip install -r requirements-test.txt
python -m unittest discover -s tests
```

The scripts require the existing pinned Sharp dependency. They do not call an image
generation API. The optional `--available` flag on the packer is for an unfinished
authoring batch; release verification must run without it.

## Validation

All 39 sources were visually reviewed, with seven targeted corrections. The strict
packer exported all 312 views. All 14 repository Python tests passed, including
roster coverage, frame uniqueness, transparency, dimensions, PNG metadata/CRC and
source hashes. The gallery was checked at desktop and 390-pixel mobile widths:
faction/category filters, all eight directions, keyboard navigation and closing.
This validates the artwork package and viewer, not in-engine animation readiness.
