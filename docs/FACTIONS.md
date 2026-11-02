# Nine peoples, distinct ways to fight

The published alpha.3 skirmish roster has five parent realms, each with four selectable subfactions and two exclusive units per choice. All share the physical Veilglass economy, while costs, health, damage, movement and doctrines create different strengths. Twenty choices do not imply twenty player slots: the largest public map supports twelve players.

| Parent faction | Specialisation | Four subfactions | Shared aircraft / beast / power |
|---|---|---|---|
| Humans / Last Dominion | Range, combined arms, efficient repairs and logistics | Bastion Directorate; Free Earth Union; Ashen Covenant; Area Fifty Two | Bastion Gunship / Ironjaw Warhound / Nuclear |
| Angels / Celestial Host | Durable expensive elites, heavy volleys and recovery between fights | Seraphic Synod; Order of the Gate; The Unshackled; Choir of Desolation | Sky Warden / Covenant Gryphon / Witness of Salt |
| Hell / Infernal Legions | Swarms, aggressive production, curses and combat frenzy | Iron Legions; Blood Brood; Court of Whispers; Circle of Contempt | Ash Wyvern / Cinder Hound / Hellrift |
| Noetic Assembly | Precision, armored attrition, relay formations and adaptive harassment | Echo Directorate; Iron Calculus; Custodian Grid; Paradox Collegium | Vector Interceptor / Logic Stalker / Extinction |
| Forsaken Host / Fallen Angels | Entrenched nobles, risky hymn formations, wounded aggression and isolated hunters | Ashen Thrones; Hollow Choir; Carrion Testament; Broken Firmament | Mourning Kite / Carrion Chimera / Sepulchral Rapture |

[Twenty illustrated playstyle profiles](https://mrkrissatan.github.io/Sevenfall/subfactions.html) explain each doctrine, tactical approach, counterplay and exclusive pair. [The 275-entry field guide](https://mrkrissatan.github.io/Sevenfall/forces.html) includes buildings, defenses, production, collectors, MCVs and units, with filters for every choice. [The directional gallery](https://mrkrissatan.github.io/Sevenfall/turnarounds.html) distinguishes current sprites, inherited reference art and future concepts.

## Four independent development factions

The Veilborn, Unwritten, Outer Silence and Nephilim Remnant each have a complete authored economy, buildings, defenses, aircraft, beast, logistics and combat roster. They have **no subfactions**; the existing twenty are unchanged.

- **Veilborn:** costly living crystal protected and healed by powered growth nodes. Bloom comes from the Heart Prism. Its secret sixth campaign and progression gate remain unfinished, so this faction is hidden in the normal lobby.
- **Unwritten:** fragile memories and decoys; recent combat losses can become temporary infantry through Restoration from the Archive of Names.
- **Outer Silence:** cloaked ambushers, isolated flanking troops and short-lived suppression. Absolute Silence comes from the Null Cathedral.
- **Nephilim Remnant:** expensive giants and vulnerable human attendants. Earthbreaker comes from the Ancestral Cairn and cannot hit aircraft.

The latter three are selectable development skirmish factions, and NPC-only campaign participants. H03/A03/D02 developer previews demonstrate neutral/helpable or hostile enclaves; the 150 campaign briefs do not represent completed maps.

[Complete illustrated independent rosters](https://mrkrissatan.github.io/Sevenfall/additional-realms.html) · [Detailed mechanics](../design/ADDITIONAL_REALMS.md). The four powers bring the development total to 21, while the published alpha.3 remains at 17.

## Build and fight

Deploy the MCV with **F**, establish power, build the faction refinery and protect its collector. Train infantry and vehicles; add radar, a service depot and advanced technology as required. Each realm can build a helipad/roost for aircraft and a kennel/cradle for beasts. Replacement MCVs unlock after a service depot. Collectors are safe from Veilglass contact blasts; other units can trigger explosions that spread deposits and damage nearby actors.

Civilian houses support garrisons and damage/destruction. Engineers repair surviving houses and restore bridges through repair posts. Roads, forests, cliffs and crossings shape movement. Cliff terraces do not grant high-ground combat bonuses.

## Seventeen building-bound powers

All twenty choices have their realm’s shared power. The original twelve subfactions additionally retain one exclusive power each; the eight new choices do not yet have separate exclusive superweapons. Powers automatically charge in **Defences** when their supplying building exists and has power. Losing the last source removes access; rebuilding starts a new charge. Low power pauses charging. Destroying or disabling the source during a warning can cancel the pending strike.

The Witness of Salt opens three pairs of wings, flashes after five seconds and petrifies destructible actors within four cells. Salt statues crumble four seconds later; destroying the source after impact does not reverse this. Nuclear and Witness can hit friendly and neutral actors. [Controls, exact values and limitations](SHARED_ARSENAL.md).

## Where to find current details

- [Original twelve doctrines and powers](FACTION_IDENTITIES.md), including [Choir / Area Fifty Two / Circle controls](SUBFACTIONS.md).
- [Noetic and Forsaken lore, units and eight doctrines](NEW_REALMS.md).
- [All five realms’ defensive structures](DEFENSES.md) and [shared arsenal](SHARED_ARSENAL.md).
- [Installation and tester instructions](TESTER_GUIDE.md), [acceptance evidence](TESTER_ALPHA_ACCEPTANCE.md) and [remaining work](../ROADMAP.md).

The public alpha is standalone Windows x64 skirmish with three maps, AI opponents, multiplayer, saves and replays. Naval and fixed-wing rosters, full campaigns, broader AI/balance testing and animation/audio polish remain unfinished. The planned 150 missions cover six interwoven campaigns; five completions unlock the Veilborn finale. The Unwritten, Outer Silence and Nephilim are non-player third parties in those missions. Planned stories are not finished playable campaigns.
