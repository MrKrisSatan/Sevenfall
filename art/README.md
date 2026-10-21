# Sevenfall faction art

![In-game-size sprites enlarged 3x](power-buildings-preview.png)

Left to right: **Radiant Spire** (Angels), **Veil Generator** (Humans),
**Furnace Heart** (Demons). The high-resolution source PNGs are in `source/`.

## Implemented

- Three original, transparent power-building sprites and matching 56×42 production icons.
- Three original refinery sprites with open unloading aprons and matching 56×42 icons.
  Their 128×128 frames contain artwork up to 88×96 pixels. Existing footprints,
  docking offsets, free harvesters, storage, costs and power use are preserved.
- Three parent faction emblems, mapped to all nine subfaction selectors.
- Three Construction Yard designs and faction-specific MCVs, mapped to all nine subfactions.
- Three original harvesters and six eight-direction vehicle sheets, with matching icons.
- Rough and enriched Veilglass deposits with four density frames each.
  See [the logistics pass](LOGISTICS.md) for frame conventions and validation limits.
- Sevenfall menu/loading graphic with the three emblems and game title, replacing the RA logo.
- 1×, 2× and 3× UI atlases, padded to power-of-two GPU texture dimensions.
- PNG sequence loader registration and actor sequence bindings. Each building has an
  always-visible player-coloured `===` ownership marker; PNG pixels themselves are not remapped.
- Main-menu showcase contains all nine structures, three MCVs, three collectors and
  small Veilglass deposits. It suppresses refinery free actors and places one collector
  per faction explicitly; these collect and eventually deplete the showcase deposits.

![Refinery sprites enlarged 3x](refinery-buildings-preview.png)

Left to right: Angel, Human and Demon Veilworks. These designs share an open front
unloading apron, with faction-specific processing towers and materials.

## Art direction

| Faction | Architecture | Materials / palette |
|---|---|---|
| Celestial Host | Tall crystal spire, halo rings, wing buttresses | Ivory, gold, cyan |
| Last Dominion | Armoured compact reactor, cooling stacks, conduits | Graphite concrete, olive steel, amber |
| Infernal Legions | Horned living furnace, rib cage, crystal heart | Black iron, scorched bone, crimson, magenta |

## Provenance

The source PNGs were generated for Sevenfall using the built-in OpenAI image
generation tool on 21 October 2026. Prompts described original faction concepts from
the design bible; no third-party reference artwork was supplied. File provenance and
SHA-256 hashes are recorded in `sources.json`. These are AI-generated development assets,
not hand-painted work. The repository's original-content licensing decision remains open;
this pass does not assign a new content licence or claim exclusive rights.
The exact refinery generation prompts are recorded in `refinery-prompts.json`.
Logistics and Veilglass prompts, including the Angel MCV correction, are recorded
in `logistics-prompts.json`.

The script performs technical resizing and atlas packing, preserving source transparency.
It adds ordinary text for the title and random-faction question mark. Existing Red Alert
terrain, combat units, other structures, interface borders and audio remain placeholders.

## Rebuild derived assets

The game consumes committed PNGs, so Node is **not** needed to build or play it.
To regenerate the derived artwork, use Node 20.9+ and install the exact `sharp` version
from the root `package.json`, then run:

```sh
npm install
npm run art
python scripts/build.py test
python -m unittest discover -s tests
```

The title uses Georgia/sans-serif fonts resolved by the host; exact typography may vary
when rebuilding on another OS. Inspect the result before committing regenerated atlases.

## Deliberate limitations

This is a static sprite pass. Idle, damaged-idle and make currently use the same image.
There is no custom construction animation or damaged artwork yet; inherited
power-building, yard and refinery bib/death art is removed. Vehicle husks provisionally
reuse the new intact silhouettes with the inherited dark overlay and fire.
The inherited refinery roof overlay
is removed because the new art has an open dock; there is no separate foreground
occlusion layer yet. Docking alignment and occlusion need a full harvesting playtest.
Earlier art passes kept gameplay values unchanged. The expanded building roster adds new prerequisites and repair targets; see BUILDINGS.md.
The nine subfactions share their parent's emblem; distinct subfaction heraldry is still pending.

## Verification

- OpenRA `--check-yaml` passes for the mod and both maps.
- OpenRA `--check-missing-sprites` passes for all four inherited tilesets with local content installed.
- Six regression tests pass, including PNG dimensions/alpha, frame metadata and CRCs,
  provenance hashes, texture sizes and flag-region bounds.
- All three building PNGs and the new menu graphic were visually inspected in the running engine.
- Observed the Angel spire, production icon and player-colour marker in a live skirmish.
- High-DPI atlas files are checked structurally; 2×/3× display hardware has not been playtested.

Refinery pass validation: YAML checks pass for both maps, missing-sprite checks pass
for all four tilesets, and the five regression tests include refinery frame dimensions
and transparency. Derived sprites were visually inspected and the updated game
launched successfully; the Angel refinery icon was observed in the live sidebar.
All-faction harvesting and damage-state playtests remain outstanding.

The [expanded building pass](BUILDINGS.md) covers production and support buildings. Next: units;
add construction/damage animations and team-colour masks as the animation pipeline develops.

## Eight-direction unit artwork

[39 designs / 312 transparent views](unit-turnarounds/README.md), including the current roster and new naval, aircraft and kennel-beast concepts. Includes individual PNGs, OpenRA-format strips, source sheets and generation prompts. Combat integration and animation remain pending.
