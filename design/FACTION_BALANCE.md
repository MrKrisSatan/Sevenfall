# Faction asymmetry — initial playable tuning

Implemented 25 October 2026 against upstream `681cf3b`. This is an initial balance
pass, not a claim of competitive balance or completed faction technology trees.

## Three specialisations

| Faction | Best at | Implemented specialty | Weakness / counterplay |
|---|---|---|---|
| Angels | Individual durability and heavy precision volleys | **Renewal:** all six implemented combat designs regain 1% maximum HP each second after eight seconds without receiving damage. | Expensive units and longer production; generally slower and outranged by comparable human units. Keep damaging them to interrupt recovery; raid their slow collectors. |
| Humans | Ranged combined arms and efficient logistics | **Field Engineering:** Bulwarks, Siege Cannons and Harvesters repair 1,500 HP per depot step instead of 1,000. Rifles, rockets and tanks have the longest range among their direct counterparts. | Modest individual durability, no automatic faction regeneration. Depots still cost credits and require travel. Artillery needs screening and cannot fire inside four cells. |
| Demons | Fast production, closing distance and sustained close combat | **Blood Frenzy:** all six combat designs gain 20% firepower and 10% movement speed when attacking, expiring four seconds after their last attack. One instance only; later attacks refresh it. | Fragile basic troops and collectors, short ranges and melee beasts. Kite, focus fire and use splash; stopping attacks removes frenzy. |

These are unit-design traits, not player-wide modifiers: captured units retain
their design's specialty. Starting MCVs are unaffected. Harvesters remain unarmed;
only the human collector receives the depot repair benefit. Renewal restores
health, not a separate shield pool. Blood Frenzy triggers on firing/attacking,
not on kills or confirmed hits, and generates no income or free units.

Existing defenses reinforce these identities: powered Angel light curtains and
Sanctuary, independent human guns and occupied entrenchments, and demonic dread
conversion. Sanctuary is allied-infantry healing/protection, not the planned full
Celestial Ward shield system.

## Line infantry comparison

Values below use the engine's internal health/damage units. Damage is the base
per-shot value, before armour, cover, veterancy, frenzy and other modifiers.
Normal simulation speed is 25 ticks per second.

| Unit | HP | Cost | Base damage | Reload ticks | Range in cells | Speed |
|---|---:|---:|---:|---:|---:|---:|
| Angel Watcher | 9,000 | 200 | 4,800 | 60 | 5 | 72 |
| Human Rifleman | 4,800 | 90 | 1,200 | 18 | 6 | 87 |
| Demon Thrall | 3,200 | 55 | 2,800 | 20 | 1.5 | 110 |

Against unarmoured targets, before cover/veterancy and excluding approach time,
their theoretical sustained damage is respectively 2,500, 2,000 and 4,375 internal
HP/second. Thrall frenzy raises its theoretical figure to 5,250. These values are
not duel predictions: range, movement, splash, overkill and army cost matter.
Rifles and basic claws remain weak against heavy armour (12% and 10% damage).

Combat-unit build-duration modifiers are Angels 75, Humans 60 and Demons 45,
compared with the engine's default 60. Cost also affects build time. Expensive
Angel losses take longer to replace; cheap Demon units reinforce quickly.

## Complete implemented combat roster

All 18 combat designs now explicitly define HP, cost, speed, production modifier
and faction weapons. Angel and Human missile infantry no longer share unmodified
RedEye/Dragon damage. Hexers have distinct curses rather than Angel HaloLance.
Ravagers and Hellreavers use short-range claws rather than inherited tank guns.
The Gatekeeper and Siege Cannon also have explicit faction weapons.

Infantry garrison armaments use the same faction weapons as their field versions,
including both ground and air missiles where applicable. This prevents a hidden
fallback to shared Red Alert weapons when entering a human entrenchment.

Each custom weapon explicitly uses one shot per volley. Inherited projectile,
impact, damage-type and visual primitives remain, including artillery splash;
these are not claims of a finished original-effects pass. Missile travel limits
are extended to cover the new firing ranges. Existing actor gates, production
queues, nine exclusive units, animation bindings and economic chains are preserved.

## Validation and next balance pass

- 53 Python tests pass, including distinct infantry tradeoffs, all combat weapon
  bindings, garrison consistency, healing restrictions, frenzy limits, missile
  travel range, anti-armour counters and unarmed collectors.
- The pinned engine and Sevenfall extension build; engine YAML/Fluent checks pass
  for nine maps and four tilesets. Seven pure C# dread assertions also pass.
- No new full-match or multiplayer balance acceptance is claimed. Run equal-cost
  armies as well as individual duels, test kiting/obstacles, interrupted Renewal,
  frenzy expiry, depot credit consumption and nine-subfaction AI matchups.
- Full shield mechanics, research, advanced units, air/naval production, support
  powers and superweapons remain on the implementation backlog.

Source of truth: `mods/sevenfall/rules/30-units.yaml` and
`mods/sevenfall/weapons/sevenfall.yaml`. Tooltips and the website catalogue describe
the same implemented specialisations.
