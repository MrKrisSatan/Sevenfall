# Faction building pass

The current base roster has 39 intact building designs: 13 roles across Angels,
Humans and Demons. Each parent's three subfactions share these designs. This pass
adds 30 sprites and 30 build icons to the existing yards, basic power and refineries.

| Role | Angels | Humans | Demons |
|---|---|---|---|
| Infantry production | Chapel | Barracks | Pit |
| Vehicle production | Armory | Motorpool | Forge |
| Advanced power | Radiant Nexus | Veil Reactor | Abyssal Furnace |
| Vehicle repair | Restoration Dais | Service Depot | Mending Forge |
| Radar | All-Seeing Halo | Radar Dome | Scrying Spire |
| Naval production | Tidegate | Naval Yard | Abyssal Pen |
| Vertical aircraft | Sky Sanctum | Helipad | Harpy Roost |
| Fixed-wing aircraft | Seraph Launchway | Airfield | Hellwing Runway |
| Beast training | Guardian Cloister | Canine Compound | Hellhound Den |
| Advanced technology | Celestial Archive | Technology Centre | Forbidden Archive |

Naval Yard/Sub Pen and Allied/Soviet Tech Centre are represented by faction-specific
equivalents, rather than duplicate imported buildings in every faction. The Demon
Abyssal Pen uses the submarine-production foundation. New artwork contains no ships,
aircraft or beasts: those belong to the unit pass.

## Rules and progression

- Barracks and factories retain their existing costs, footprints and production exits.
- Radar requires the faction refinery; advanced power and air facilities require radar.
- Repair requires the faction vehicle factory. Existing ground vehicles now target the
  three custom depots instead of the unavailable Red Alert repair facility.
- Naval structures require power and water placement. Kennels require faction barracks.
- Tech centres require the faction factory and radar. Dedicated research and advanced
  unit unlocks are pending the unit roster pass; they currently provide prerequisites.
- New support buildings inherit provisional OpenRA costs, health and power values.
  Radar and repair traits are active; inherited Red Alert GPS and airfield support
  powers are removed. No faction aircraft, naval or beast units are available yet.
- The prototype AI continues its existing land build order. Expanded AI use of these
  facilities awaits the corresponding units and balance work.

## Rendering

`building-catalog.json` defines sprite dimensions and anchors. The preparation script
only trims, resizes and packs original transparent PNGs. Each building has a 128×128
frame and 56×42 icon. Pads and docks use centred anchors and a low render depth so
vehicles can appear above them. Other structures use a common ground anchor.

Inherited bibs and the old factory door overlay are removed. Factory entrances are
drawn open. Owner-colour markers remain visible because these truecolour images do
not yet have a team-colour mask. Idle, placement, construction, resupply and damaged
states share the intact drawing; dedicated animation and damage frames come later.
Service-arm/vehicle occlusion and production exit alignment still require playtests.

Exact generation prompts are in `production-building-prompts.json` and
`extended-building-prompts.json`, with the airfield edit in `building-corrections.json`; original PNG hashes are in `sources.json`.

## Inspection

Run `npm run art` to rebuild derived PNGs and per-role preview strips. The normal
build uses the committed derived PNGs and does not need Node.

The **Sevenfall Building Gallery** lobby map places all 39 designs, with one fixed
parent faction per player slot and a water strip for the naval facilities. It is a
developer inspection map, without resources or a balanced combat layout. Pick the
slot for the faction you want to inspect. Starting positions are fixed, fog is disabled,
the map starts explored, and gallery-only advanced power output is raised so radar
stays online. Regenerate it with
`python scripts/generate_building_gallery.py`.

Coverage tests check every requested role across all three factions, sprite/icon
dimensions, transparency, provenance and the gallery's naval terrain. Engine YAML
and missing-sprite validation are separate from functional gameplay acceptance.

Verified on Windows: all eight Python tests pass; OpenRA YAML checks pass for the
mod and three maps; missing-sprite checks pass for four tilesets. All derived role
preview strips were inspected. The gallery loads in the running engine; Angel
barracks, factory, advanced power, repair, radar, aircraft-facility sprites and all
12 building icons were observed, as was infantry emerging from the barracks.
The final locked visibility/spawn settings pass lint but have not been reloaded
in a second match. Full all-faction naval placement, repair, aircraft landing,
production exits and damage/occlusion playtests remain outstanding.

Defensive structures, support powers and superweapons are separate future roster
work; this pass completes the current base/support building roles, not all buildings
that might eventually appear in the finished game.
