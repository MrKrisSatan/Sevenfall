# SEVENFALL: The War for Creation
## Original RTS design bible | Concept version 0.1

**Tagline:** *The Apocalypse wasn't the end. It was the beginning of the war for everything.*

**Genre:** original dark-fantasy/science-fantasy RTS, built with OpenRA, individual-unit C&C combat, not squad capture-point combat. **Players:** 1–8 target for skirmish and multiplayer, subject to performance testing. **Platform targets:** Windows/Linux first. **Camera:** isometric 2D with readable terrain, infantry, air, and siege machinery.

## The world

When the Seventh Seal shattered, it did not call forth a single moment of divine judgment. It tore open the Veil that had held three orders of existence apart for countless ages. The first day brought storms that burned without consuming oxygen. On the second, mountains rose where cities had stood. On the third, the banners of Heaven appeared on the horizon, and beneath them came judgment. On the fourth, the gates below the world opened.

The Celestial Host declared Earth an evacuation ground and a future holy citadel. The Infernal Legions regarded it as territory owed from the beginning. Humanity was told to surrender its tools, cities, weapons and right to decide. Instead, surviving generals, refugee councils, engineers, unorthodox clerics and scientists formed the Last Dominion. They had already seen how to kill a godling. Then they learned how to mass-produce the ammunition.

The campaign is explicitly told through multiple perspectives. Angels have genuine compassion and fanatical institutions. Humanity can become authoritarian or monstrous in the name of survival. Demons include tyrants, pragmatists, and a few factions that see the cosmic war as a prison they too want to escape. None of these is a religious statement about living people; it is the fiction's internal conflict.

## Veilglass: the thing worth destroying a world for

Veilglass forms at **Seamfalls**, pressure cracks between material existence and the other two realms. It grows in jagged blue-violet crystalline banks with gold or blood-red inclusions. Wild deposits are mixed-grade and dangerous; pure condensed nodes are brighter and significantly more valuable.

- **One physical commodity; two grades**: rough Veilglass and enriched Veilglass. Both enter the same inventory, buildings and production-credit economy.
- **C&C economy**: player purchases a harvester, orders it to the field, it gathers discrete loads, returns to a dockable refinery, unloads to the credit reserve, and sets out again. Loss of harvesters hurts throughput immediately.
- **Faction harvesting**: Angel Gatherers are resilient and cautious (slow); Human Harvesters are efficient general-purpose machines; Demon Devourers are quick and vulnerable.
- **Field hazards (later milestone)**: unpurified rich deposits periodically emit a warning pulse, temporarily reducing accuracy or calling neutral manifestations. Hazard radius is legible and never pure random punishment. Angel processing may stabilize a fissure, Human rigs may deploy shielding, and Demons may accelerate growth at a cost.
- **Why the sides fight**: Heaven needs it to lock the breaches, Hell needs it to widen them, humanity needs it to end dependence on either realm.

### Economic prototype constants (subject to balance)

| Variable | Angels | Humans | Demons |
|---|---:|---:|---:|
| Starting credits (target) | 5,000 | 5,000 | 5,000 |
| Basic power cost | 420 | 300 | 370 |
| Refinery cost | 1,650 | 1,350 | 1,450 |
| Free mining unit with refinery | Yes | Yes | Yes |
| Dedicated miner cost | 1,320 | 1,000 | 950 |
| Miner HP | 74,000 | 62,000 | 45,000 |
| Miner speed | 65 | 75 | 88 |
| Basic infantry cost | 170 | 90 | 55 |
| Basic infantry HP | 7,200 | 5,100 | 3,500 |

These values are exact in the starter MiniYaml where corresponding actor entries exist; starting credits remain dependent on selected map settings.

## Strategic identity and win conditions

**Annihilation:** destroy opposing construction yards and remaining production-capable buildings, using OpenRA short-game logic. **Veil Dominion (post prototype):** hold several named Seamfalls to accrue victory progress. **Story goals:** rescue convoys, seize an enclave, collapse an invasion portal, escape a celestial quarantine, or take a holy city; each should change gameplay rather than merely flavor it.

No infinite income from fighting. No strat-point requisition. Expanding to map Veilglass remains the strategic heart of the game. Fog-of-war scouting, harvester raids and timing pushes should matter in every match.

## Angels: The Celestial Host

Their soldiers are costly but individually powerful. Buildings look like impossibly slender basilicas and airborne choirs; their weapons combine blinding geometric light with ancient armed combat. Angels prefer decisive precision and protected supply lines. They struggle with fast expanding maps and resource-sapping attrition.

**Shared doctrine (full vision):** Celestial Ward: units near a Consecration Beacon regenerate modest shields if out of combat. This shield has a cap and consumes normal power, preventing eternal defense. Their aircraft are individually powerful; anti-air missile networks are a counter. Economy is at a disadvantage versus Human factories.

| Subfaction | Theme | Exclusive combat unit in starter | Full-game advantage | Explicit tradeoff |
|---|---|---|---|---|
| Seraphic Synod | Fire and judgment | Seraphim | Radiant AoE and aerial strike | Fewer static defenses |
| Order of the Gate | Protectors of the thresholds | Gatekeeper | Fortresses, shield projectors | Slower mobility, expensive reinforcements |
| The Unshackled | Outcasts of Heaven | Penitent | Early raids, unconventional maneuver | Reduced ward strength |

**Full-release units:** Watcher line infantry; Cherubic Scout; Judicator missile bearer; Choirbearer healer; Winged Lancer; Aegis Engine; Censer artillery; Halo Interceptor; Throne Carrier; Ophanim siege-wheel. **Structures:** Ascension Bastion (conyard), Radiant Spire (power), Sanctification Crucible (refinery), Choir Citadel (infantry), Heavenforge (vehicles), Halo Gate (air), Edict Spire (superweapon). **Superweapon:** Edict of Dawn: warning-marked radiant strike; precision and area purification, very high construction cost.

## Humans: The Last Dominion of Man

Not the weakest faction, merely the most technologically pragmatic. They combine conventional rifles, armored columns, heavy artillery, battlefield construction, mobile repairs, sensor nets and experimental anti-entity devices. Efficient economy and adaptability offset inferior raw supernatural power. A human army wins when its front line, reconnaissance, logistics and guns cooperate.

**Shared doctrine (full vision):** Entrenchment and Field Engineering: infantry can occupy prepared cover, construction vehicles repair damaged tanks and siege engines, and radar can reveal intermittent firing positions. Humans have cheaper power/refineries but can lose shock engagements without combined arms.

| Subfaction | Theme | Exclusive combat unit in starter | Full-game advantage | Explicit tradeoff |
|---|---|---|---|---|
| Bastion Directorate | Military emergency government | Siege Cannon | Fortifications, long-range siege | Slow map control, weak rapid assault |
| Free Earth Union | Network of free settlements | Wasteland Ranger | Mobile war, scouting, fast production | Fragile defenses |
| Ashen Covenant | Relic-science survivors | Ash Templar | Anti-entity ammunition, wards | Pricey low-throughput elite branch |

**Full-release units:** Rifleman, Rocketeer, Ranger, Field Medic, Combat Engineer, Bulwark tank, Judas APC, Lazarus repair vehicle, siege howitzer, Veilbreaker anti-air truck, Nightjar attack helicopter, Crucible assault gun. **Structures:** Command Vault, Veil Generator, Fracture Refinery, Survival Barracks, Motor Pool, Rocket Battery, Listening Tower, Research Bunker, Lazarus Launch Array. **Superweapon:** Lazarus Protocol: expensive Veilglass-driven orbital kinetic battery with audible countdown and counterplay.

## Demons: The Infernal Legions

Hell has numbers, cruelty and unnatural biology, but its most useful weapon is the ability to make a defended position unsafe. Living flesh fortresses root in the ground; blacksmiths graft molten armor over monsters; smaller horrors raid unguarded workers. Greater demons are terrifying but cannot be spammed cheaply.

**Shared doctrine (full vision):** Corruption: certain units emit temporary contamination zones that punish enemy stationary positioning, but zones decay, do not permanently repaint maps and cannot replace scouting or harvester management. Fallen friendly Thralls may give nearby beasts short-lived battle frenzy, not free economy.

| Subfaction | Theme | Exclusive combat unit in starter | Full-game advantage | Explicit tradeoff |
|---|---|---|---|---|
| Iron Legions | Armored infernal hierarchy | Hellreaver | Shock beasts, siege endurance | Expensive heavy units |
| Blood Brood | Hunger, spawn and rapid mutation | Skitter | Speed, swarm replenishment | Extreme AoE vulnerability |
| Court of Whispers | Sorcery and subterfuge | Hexer | Disruption, infiltration, rituals | Vulnerable in direct combat |

**Full-release units:** Thrall, Skitter, Cinderling, Horned Reaver, Bone Scavenger, Hexer, Hellreaver, Malefic artillery larva, Screamwing, Blackiron Fiend, Infernal Colossus. **Structures:** Crown of Ash, Furnace Heart, Maw of Want, Birthing Pit, Flesh Forge, Pain Spire, Rift Chamber, Ninth Mouth. **Superweapon:** The Ninth Mouth: a visible dimensional tear that births timed waves and poisons ground while open; area defenses counter the spawned host.

## Three faction combat equations

- Angel precision > vulnerable exposed human artillery; Human cheap anti-air and rockets > isolated expensive Angels; Demon swarms > unsupported Angel harvesters.
- Human splash and suppression > Demon light swarms; Demon corruption + raiders > undefended Human economic expansion; Angel wards + air > slow Demon artillery.
- None of these is an automatic win. Terrain, technology timing, scouting, army composition, positioning and skill must outweigh simple rock-paper-scissors.

## Production trees (prototype integration)

| Stage | Angel side | Human side | Demon side |
|---|---|---|---|
| Start | MCV → core construction yard | MCV → core construction yard | MCV → core construction yard |
| Power | Radiant Spire | Veil Generator | Furnace Heart |
| Economy | Sanctification Crucible → Gatherer | Fracture Refinery → Harvester | Maw of Want → Devourer |
| Infantry | Choir Citadel → Watcher/Judicator | Survival Barracks → Rifleman/Rocketeer | Birthing Pit → Thrall/Cinderling |
| Vehicles/beasts | Heavenforge → Aegis | Motor Pool → Bulwark | Flesh Forge → Ravager |
| Subfaction | Seraphim / Gatekeeper / Penitent | Siege Cannon / Ranger / Ash Templar | Hellreaver / Skitter / Hexer |

The starter uses the existing OpenRA engine actors, animations and maps as temporary integration placeholders. Some full-release traits (wards, corruption, hero units, repair mechanics, original terrain, campaign logic, AI, audio) are intentionally not yet implemented.

## The three campaigns: 75 missions

The canonical campaign specification has been expanded to **25 missions each for Humans, Angels and Demons**, grouped into **five acts per faction** (75 total). The old eight-mission concept was a narrative skeleton; its original mission titles are preserved in expanded order. All campaigns remain design-only until OpenRA mission maps and objectives have been implemented and engine-verified.

| Campaign | Acts | Beginning | Key shared battles | Finale |
|---|---|---|---|---|
| **Ashes of Earth** (Human H01–H25) | The Breaking; War of Claims; False Edicts; Witness Ledger; Harrow | Evacuate Crown Vale, refine Veilglass, form the Last Dominion | Broken Choir (H07), Causeway (H10), the coerced enclave (H14) | **We Remain (H25)**: Open Earth / Iron Earth |
| **War in Heaven** (Angel A01–A25) | Same five acts through an Angel perspective | Arrive at Empty Gate, protect the Host's wards, mine Veilglass | Sable Crown (A06), Broken Choir (A08), Causeway (A10) | **Judgment Deferred (A25)**: Open Gate / Radiant Quarantine |
| **The Ninth Mouth** (Demon D01–D25) | Same five acts through an infernal perspective | Raise Birthing Pits, mine with Devourers, fight Hell's internal chains | Sable Crown (D05), Court contracts (D10), Causeway (D12) | **The Shape of Freedom (D25)**: Unbound Fire / Crown of Ash |

See **[STORY_BIBLE.md](STORY_BIBLE.md)** for researched inspiration and characters, and **[CAMPAIGN_MISSIONS.md](CAMPAIGN_MISSIONS.md)** for all 75 scenarios with primary objectives, optional objectives, failure states, planned mechanics and crossover safeguards. H25, A25 and D25 are alternate resolutions of a common crisis, not three simultaneously canonical victories.

## Presentation and art direction

- Angel: ivory stone, fractured gilding, white-blue fire, stained-glass gold, abstract wings and turning halo mechanisms. Elegant geometry with intimidating scale. Avoid uniformly white 'good' visuals.
- Human: graphite, olive, dust-grey, salvaged steel, industrial amber, portable power grids, angular concrete and battlefield trenchworks. Functional silhouettes and mechanical construction animations.
- Demon: oxidized crimson, scorched bone, black iron, ash and luminous sickly magenta, organic bulwarks and breathing forge structures. Units must still read distinctly at standard RTS zoom.
- Veilglass: blue-violet base crystal with rare gold/pink/blood-rich cracks; visibility against all biome palettes is mandatory.
- UI: triptych faction skins, accessible team colors, unambiguous unit icons, attack type icons, power/credit display, harvester and production alerts, fast build queues.
- Sound: per-faction voices, whispered foreshadowing, huge machinery, layered choral percussion, distorted brass and industrial rhythm. Use original audio only.

## Milestones, in order

**M0 / starter included:** faction IDs, tech prerequisite plan, three harvesting chains, first combat units, subfaction exclusives, and YAML-backed prototype installation tools. Static-linted, engine-unverified.

**M1 / first executable slice:** OpenRA SDK boots to Sevenfall lobby; one test map; all nine faction choices load; a human player in each faction can complete build-power-harvest-train-fight cycle; all harvesters return and resume. No major errors in OpenRA utility tests.

**M2 / skirmish:** dedicated AI profiles for nine subfactions; unique counters; mixed-army pathfinding; deterministic multiplayer; three original tilesets/art replacement pipeline.

**M3 / full roster:** complete unique actor rules/assets for ground and air, defensive structures, support powers, superweapons, post-match statistics and balance.

**M4 / campaigns:** 75 scripted missions, objectives/briefings, narrative cinematics and mission progression; save/resume verified against engine support.

**M5 / launch candidate:** visual/audio polish, localisation, accessibility, installer and mod licensing review, extensive game test matrix.

## Intellectual property and licensing

Sevenfall's names, lore, original art assets and core faction designs should be independently created. The starter relies on OpenRA/Red Alert game data and assets in a **development-only overlay**. Do not ship EA/Westwood assets as standalone owned material. OpenRA/Mod SDK is under GPLv3; any custom executable extension code must be compatible with the relevant open-source licenses. Data/artwork may be distributed separately under a chosen compatible content license when properly authored and rights-cleared. Source references: OpenRAModSDK and OpenRA official docs.