# Sevenfall changelog

## Skirmish alpha release audit � 2026-10-25

- Reviewed standalone staging, gameplay diagnostics, source and Windows distribution.
- Rebuild candidates from committed pinned sources and record their three source revisions.
- Collect notices for the actual resolved Windows runtime across all package caches.
- Verified 74 Python tests, 111 C# assertions, 208 chrome collections, and fresh native
  environment (11) and nine-faction harvesting/hazard (24) diagnostics.
- Recorded remaining match/replay, runtime-support, distribution, installer and clean-PC
  gates in docs/SKIRMISH_ALPHA_AUDIT.md. No public alpha is released by this audit.

## Standalone alpha and Sevenfall menu — 2026-10-25

- Removed the OpenRA forum account connection panel from the main menu.
- Replaced Battlefield News with Sevenfall Changelog, fetching the latest entry
  from this GitHub changelog. Offline launches display the bundled entry.
- Removed the remaining external Red Alert content dependency and built a
  portable Windows alpha candidate with the .NET runtime included.
- Verified nine-faction construction, production and harvesting in native tests,
  plus Veilglass explosions, faction defenses, civilian damage and bridge repair.
- Completed an autonomous AI economy and elimination match. Public release
  remains pending multiplayer, save/replay and distribution acceptance checks.

## Faction interface and neutral menus — 2026-10-25

- Angels use ivory/gold HUD trim, Humans steel/teal, and Demons obsidian/ember.
  All nine subfactions map to their parent skin using the actual local faction.
- Added themed command bars, production/sidebar controls and inactive radar
  emblems, with original vector sources and three display-density exports.
- Menus, dialogs, spectators and loading branding use charcoal/silver styling.
  The menu background is now a civilian scene without armies or faction bases.
- Replaced the RA title font and added merged-engine UI bounds checks to builds.
  68 Python tests and 152 chrome collections pass; native visual checks pending.

## Environment damage and repair pass — 2026-10-25

- Added original terrain, roads, paths, cliffs, four trees and Ashen Crossing.
- Civilian cottages and townhouses support garrisons, damage frames, forced-fire
  destruction, occupant ejection and engineer repair while still standing.
- Bridges have damage/ruin frames, lose their crossing when destroyed, and can
  be restored by engineers through bankside maintenance posts.
- Added three asymmetrical faction engineers and a native environment diagnostic.
- Replaced all four RA tileset imports with one original alpha tileset; 91 external
  RA manifest references remain. Native gameplay acceptance remains NOT RUN.

## Release blockers and explosive Veilglass — 2026-10-25

- Campaign objectives count real accepted refinery income instead of sampling
  the stored balance, fixing objectives that stalled when income was spent.
- Non-harvester ground contact detonates Veilglass, damaging units and structures
  and scattering a bounded amount of mineral. Harvesters do not trigger blasts;
  airborne units are excluded. Added a procedural purple shockwave.
- Added a native nine-faction harvesting/hazard diagnostic, dependency inventory
  and standalone manifest gate; expanded engine CI to Windows and Ubuntu.
- Replaced all 77 cursor states with original vector-derived RGBA graphics,
  retaining the software-cursor workaround and eliminating RA cursor sprites.
- Native acceptance, asset independence and standalone packaging remain pending.

## Faction asymmetry development pass — 2026-10-25

- Explicit HP, cost, speed, production pacing and faction weapons for all 18
  combat designs, including consistent garrison weapons and specialist missiles.
- Angel Renewal restores 1% maximum health per second after eight seconds without
  taking damage. Human tanks, artillery and harvesters receive 50% faster depot
  repair. Demon combat units gain temporary, non-stacking Blood Frenzy on attack.
- Human rifles, rockets and tanks outrange direct faction counterparts; Demon
  Ravagers and Hellreavers now use close-range claws instead of borrowed tank guns.
- Updated lobby descriptions, tooltips and website catalogues; documented current
  balance and a repository-wide implementation audit.
- Validation: 53 Python tests, seven C# dread assertions, Windows compilation and
  engine YAML/Fluent checks pass. Competitive and full-match acceptance remain.

## Faction defenses development pass — 2026-10-25

- Added 15 faction defenses: angelic light curtains, sanctuary and energy/AA
  emplacements; human concrete, razorwire, occupied entrenchments and independent
  gun/missile positions; demonic flesh walls, thorns and organic turrets.
- Implemented powered flesh-wall dread and ownership conversion, visible exposure,
  non-stacking influence, retreat decay, sanctuary protection and conversion immunity.
- Added lethal powered light crossings, infantry obstacle penalties, vehicle
  crushing, regeneration, faction construction gates and AI defense preferences.
- Added original six-state art, icons, mourning audio, source prompts, hash manifests,
  a 78-entry field guide, native C# extension and live acceptance scenario.
- Validation: 47 Python tests, seven dread-rule assertions and 33 native gameplay
  assertions pass. Competitive balance and large-match performance remain unmeasured.

## Animation and damage development pass — 2026-10-25

- Added authored movement, attack/work and collapse/death cycles for all 24
  implemented faction unit designs, using original Sevenfall design references.
- Added damaged animation variants for vehicles/beasts and heavy/critical damage
  sprites for all 39 implemented building designs, with repair returning healthy art.
- Preserved facing through unit death actors, followed by a short corpse/wreck hold.
- Added source prompts, hashed manifests, reproducible atlas packing/binding tools,
  an animation diagnostic map and regression coverage.
- Verified 43 automated tests, engine YAML checks for eight maps, sprite loading
  across four tilesets, and the native diagnostic through all 24 death spawns.
- Initial animation pass: prone/parachuting/construction cycles, visual polish,
  full campaign/skirmish acceptance and a standalone release remain outstanding.
- Also fixed campaign preservation bonuses and defeat/victory ordering.

## 0.3 development candidate — 2026-10-21

**Integration source, not a playable release.**

- Wrote three OpenRA Lua scenario previews: H03 The Glass Fields (Humans),
  A03 A Glass of Wrath (Angels), and D02 Seeds of Ruin (Demons).
- Registered the new three-campaign mission selection, with starting MCVs,
  preplaced enemy bases and Sevenfall land AI; included economy/production/
  destruction objectives and game failure.
- Reused the original Broken Choir terrain in three locally generated test
  map binaries, avoiding false claims that final campaign maps exist.
- Staged the 39 original eight-direction character/vehicle sheets in the SDK;
  still missing original walking, combat, death and damage animation cycles.
- Added mission contract tests, developer runbook and an easy Windows
  `PLAY_SEVENFALL_DEV.cmd` build/launch command.
- Source-level and engine checks are distinct from real mission completion,
  live AI reliability, independent Windows packaging and a public release.

## 0.2 development — 2026-10-21

- Expanded the building artwork pass to barracks, factories, advanced power,
  repair depots, radar, naval facilities, helipads, airfields, kennels and tech centres
  for all three parent factions. Added faction-specific support-building rules,
  repair targets and a 39-building inspection map. See [coverage and limits](art/BUILDINGS.md).

- Added custom faction power-building sprites, production icons, parent emblems and menu/loading branding; preserved transparent sources and reproducible art export tooling.
- Verified all three new structures in the renderer and the Angel spire/icon/owner marker in a live skirmish; added power-of-two texture regression coverage.

- Imported missing starter game source, pinned OpenRA/SDK and added build/test/launch tooling.
- Fixed inherited Buildable removal and infantry production metadata; isolated custom maps.
- Added a generated two-player proving ground, menu map and Sevenfall land AI rules.
- Verified Windows compilation, engine lint and main-menu rendering; fixed invisible cursor
  with a larger software cursor (user confirmed).
- Added tooling regression tests and Windows CI. Full economy/combat, AI, multiplayer,
  original asset replacement and standalone packaging remain unverified or incomplete.

This log records verified changes. Planned features belong in the [roadmap](ROADMAP.md).

## Initial source seed: 21 October 2026
### Added
- Original Sevenfall game concept, three major factions and nine subfaction designs.
- Veilglass resource system design and initial OpenRA MiniYaml source seed.
- Repository README, GitHub Pages-ready project site, roadmap and development issue tracker.

### Known limitations
- The initial OpenRA prototype has not been launched or compiled in the target SDK.
- No playable builds or release binaries have been published.
- Campaigns, faction passives, production art, skirmish AI and balance are not ready.

> A passing text-level consistency check is not a substitute for OpenRA engine tests.
