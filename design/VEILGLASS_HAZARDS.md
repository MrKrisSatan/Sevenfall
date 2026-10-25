# Explosive Veilglass

Both Veilglass grades (engine resource types Ore and Gems) now detonate on
contact with a living, damageable ground actor that is not a harvester.
Ground vehicles, infantry, beasts and structure footprints count. Airborne
actors do not touch deposits; landed aircraft can. Harvesters of every faction
are exempt from triggering, including captured harvesters.

- Contact consumes the triggered cell before applying damage.
- Damage affects all owners, including allies and nearby harvesters. Damage is
  12,000 at contact, falling to 6,000 at two cells; outside two cells is safe.
  Structures use their nearest occupied footprint cell, not their center.
- Up to six resource units scatter to empty, legal terrain two to three cells
  away, usually in three deposits of two units. Scatter keeps the original grade
  and cannot create more mineral than was consumed. A one-unit deposit can
  relocate its one remaining unit. Blocked destinations discard their share.
- Newly scattered deposits arm after 50 simulation ticks (two seconds at normal
  speed). They remain harvestable during that delay. Blast damage alone does not
  detonate neighboring deposits; continued physical contact is required.
- A global eight-blast-per-tick limit bounds chain processing. Actor and cell
  ordering are deterministic, and arming state participates in sync checking.
  Multiplayer/replay acceptance is still required.
- A purple procedural shockwave provides an asset-independent initial effect.
  Bespoke particles, sound, visual polish and gameplay tuning remain outstanding.

The release diagnostic map exercises real mining for nine factions while stored
income is spent every tick, plus harvester safety, infantry detonation, structure
damage and spread. It has passed engine validation, but has **not yet been run**
against installed game content. These changes are not certified for release.
