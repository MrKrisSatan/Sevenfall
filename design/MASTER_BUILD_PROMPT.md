# SEVENFALL: MASTER DEVELOPMENT PROMPT

You are the lead game designer, OpenRA engine programmer, technical artist and systems designer for **SEVENFALL: The War for Creation**. Create a NEW, eventually standalone, original dark-apocalyptic RTS built on the OpenRA engine. The supplied starter repository contains an initial OpenRA Red Alert overlay for technical prototyping. Use it as the seed, NOT as the finished game's design or visual identity.

## Creative brief
The events described in the Book of Revelation have come to pass. The Seven Seals break and the boundary separating Heaven, Earth and Hell fractures. Heaven and Hell wage total war on the surface of Earth. Humanity, believed by both powers to be an irrelevant casualty, refuses annihilation and builds a third military superpower from surviving nations, salvaged technology and dangerously weaponized supernatural energy. None of the three sides is monolithic: each has three internal subfactions with competing philosophies and mechanics.

Tone: grand, grim, Gothic, war-torn, tragic, cinematic and unrelentingly apocalyptic, with occasional defiant human resilience. Do not simply reskin Red Alert, Dawn of War or other copyrighted units. Build original lore, machines, monsters, armies, artwork and sound. Biblical language and broad themes can be used, but distinguish Revelation's imagery from the game's original invented fiction. Avoid suggesting that an entire real-world religion, group or population is evil.

## Mandatory core gameplay
- **Classic Command & Conquer mechanics**: one or more construction yards, placeable buildings, base expansion, power supply, distinct unit production structures, fog of war, harvesters that travel to Veilglass fields and RETURN to refineries, silos/storage, map control, traditional individual units, large armies, walls, defenses, tactical targeting and superweapons. NO Dawn of War-style strategic-point requisition economy. NO squads as the only available unit type.
- Exactly three major factions: Angels, Humans, Demons. Each contains exactly three selectable subfactions at first release; allow later expansion.
- **Common finite mineable map resource: Veilglass**. Created when the Veil between realms fractures. It is one substance with rough deposits and highly enriched veins (two grades, not two unrelated resources). Each side requires Veilglass to fuel its economy, but extraction speed, storage, vehicle durability, refinery efficiency and special uses differ.
- Three distinct base architecture styles; unique faction tech tree, infantry line, vehicles/beasts, artillery, air, scouting, detectors, anti-air, repair/heal, defenses, siege and late-game superweapon. Units must have strengths AND counters.
- Subfactions each grant an exclusive combat unit, a passive rule, a support ability, a unique building or tech fork, and a meaningful trade-off.
- Single player skirmish vs AI, LAN/online multiplayer if supported, nine-choice faction lobby, 3 full narrative campaigns (25 missions per parent faction, 75 total, across five acts each), with all nine subfaction variants sharing their parent's maps, save and resume where engine permits, difficulty levels, hotkeys, tooltips, music and accessibility-friendly silhouettes.
- All stats and abilities defined as game data (OpenRA MiniYaml; C# custom traits only if essential). Scripts are reserved for missions and AI events when possible. Deterministic simulation and replay safety take priority.

## Faction asymmetry contract

ANGELS (Celestial Host): elite, slow-to-replace, high-cost individual troops; protective wards, long-range precision, air dominance. Weak to prolonged attrition, economy harassment and swarms. Their mining procession is resilient but slow.
Subfactions:
1. Seraphic Synod: heavy radiant attacks, best elite airborne assaults, weak static defense.
2. Order of the Gate: slow bastion warfare, superior protection, weak mobility.
3. The Unshackled: fallen/exiled angels using risky aggressive maneuvers, faster/cheaper but reduced divine defensive bonuses.

HUMANS (Last Dominion): economical refinery output, modular vehicles, suppression, trenches, artillery, repair logistics, combined arms. Weak to concentrated high-tier supernatural threats and battlefield magical disruption.
Subfactions:
1. Bastion Directorate: long-range artillery, fortified defensive grid, weaker scouts and slower redeploy.
2. Free Earth Union: mobility, reconnaissance, mechanized warfare, weaker permanent defenses.
3. Ashen Covenant: relic tech and faith-driven anti-supernatural weaponry, higher risk/cost and weaker industrial scaling.

DEMONS (Infernal Legions): disposable numbers, melee ambush, corruptive zones, monster upgrades and regenerating elites. Weak to ranged area damage, cleansing effects and poor early logistics durability.
Subfactions:
1. Iron Legions: heavily armored hell-forged monsters, costly and slow.
2. Blood Brood: fast cheap swarms and biological snowball, low survivability against splash/area attacks.
3. Court of Whispers: hexes, possession and battlefield manipulation, fragile in direct frontal assault.

## Resource, economy and victory
- Low-grade Veilglass yields 30 credit-equivalents per unit and high-grade yields 55 in the starter; these are provisional tuning values.
- Map design should offer safe low-yield starting deposits, exposed high-yield contested sites, and optional seam fissures whose hazards can be weaponized.
- Starter: one main credit economy, one power budget, storage capacity. Later: build faction-specific overdrive systems using Veilglass, not additional gatherables. Angel Concordance builds through sanctified kills, Demon Ruin through corrupted deaths, Human Preparedness through active logistics; these must remain secondary cooldown/ability meters, NOT replace harvesting.
- Three victory modes in production: annihilation, control of Veil Fractures over time, and optional story objectives. Annihilation must be the first implemented.
- Fair skirmish start: equal starting cash and equivalent initial economic access. Only starting-unit packages differ in role, not value.

## Combat and counterplay
- Angels: high personal durability and accurate attacks, but concentrated AoE or anti-shield weapons break formations.
- Humans: tanks beat light swarms, rockets beat heavy targets, artillery beats entrenched formations, fast raiders beat artillery.
- Demons: swarms beat undefended harvesters and isolated heavies; toxic ground controls paths; anti-infantry turret lines and flame weapons contain the tide.
- Air supremacy is powerful but no faction should be able to ignore dedicated anti-air. Superweapons need readable telegraph, meaningful cost, counterplay and long cooldowns.
- Aggression is rewarded without making turtling impossible; require strategic expansion for sustained armies.

## Unit roster goals for a finished faction
At least: builder/MCV, harvester, scout, cheap line infantry, anti-armor infantry, anti-air infantry, elite infantry, support medic/repair unit, light raider, main battle tank or beast equivalent, artillery, anti-air vehicle/beast, heavy siege piece, fast aircraft, air superiority unit, superheavy/heroic unit. Add unique faction equivalents (e.g. seraphic infantry instead of tanks where justified), not carbon copies with changed names.

## Three original superweapons
- **Heaven: Edict of Dawn**: a warning-lit shaft of judgment, severe focused damage and a brief purification zone; can be interrupted by destroying its spire before firing.
- **Humanity: Lazarus Protocol**: an orbital Veilglass kinetic barrage, line/area saturation effective against large armies, vulnerable to enemy reconnaissance and anti-orbital assets.
- **Hell: The Ninth Mouth**: opens a temporary Hell breach that corrupts ground and births waves of low-tier units; longer duration but easier to counter with anti-swarm and cleansing tactics.

## Technical build protocol
1. Read the repository and verify the pinned OpenRA SDK/engine compatibility. OpenRA MiniYaml uses **tabs**, unlike ordinary YAML; never assume generic YAML parsers will validate it. Do not silently rename traits or invent APIs.
2. Get `make all`, the SDK `test` action, and launch-game working. Record engine commit and reproducible setup. Run utilities when available. Report exact failures.
3. Integrate the nine faction selectors and construction-yard prerequisite gating. Verify the actual lobby and MCV deployment for each. Verify no vanilla RA buildables leak into production menus.
4. Verify all three power generators, Veilglass refineries, harvesters, barracks/spawning pits and vehicle factories. Harvesters MUST mine, return, unload, and resume mining. Production queues must build units, respect side gating, prerequisites and power.
5. Replace placeholder visuals and sounds with original art, with standalone manifests/sequences/tilesets, before calling the game original. The prototype's Red Alert assets are not ours.
6. Implement all subfaction passives/supports/exclusives in tested source. Avoid loading C# custom gameplay traits unless necessary; if used, license source GPLv3 compatible.
7. Implement real skirmish AI: economic build order, harvesters, production, army composition, target priorities, scouting and expansion for all nine choices. Bots must use actual Sevenfall actor IDs.
8. Build a custom asymmetrical map (e.g. 96x96 "Broken Choir") with two safe starts and a heavily contested enriched Veilglass basin. Avoid ambiguous spawn balance.
9. Run in-engine automated/static tests plus manual playtests: 10-minute economic sanity, 20-minute AI survival, 1v1 asymmetric matchup, replay determinism; then iterate balance.
10. After stable skirmish, implement the 75 scenario briefs in design/CAMPAIGN_MISSIONS.md as deterministic OpenRA missions, beginning with H03, A03 and D02. Follow five acts per parent faction, implement the three alternate final battles and six ethical ending variants, and create in-world presentation. Do not claim game-complete at a design-only or YAML-only stage.

## Delivery requirements
Write and modify real project files, not only suggestions. After each implementation pass, list files changed, tested features, exact blockers and the next executable milestone. Ship minimal integrated features rather than a huge untestable collection of promises. Treat placeholder art and incomplete AI honestly. Include user-facing run/build instructions on Windows and Linux. Keep gameplay cohesive, responsive on modest hardware and scalable to large C&C-style battles.

START by validating and fixing the attached starter repository, then make three parent factions play through their first complete Veilglass harvest → building → unit production → combat loop. Only then extend the roster.