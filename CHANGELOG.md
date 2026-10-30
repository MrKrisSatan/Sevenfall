# Sevenfall changelog

## Shared realm arsenal — development

- All five parent realms now offer aircraft, beasts and shared superweapons to
  their four subfactions, alongside their existing buildings and defenses.
- Added ten asymmetrical units, four machine/fallen production buildings, five
  shared superweapon installations, AI build preferences and targeting decisions.
- Humans gain a nuclear missile. Angels summon a six-winged Witness whose flash
  petrifies units, structures, trees and bridges; salt statues crumble four seconds
  later. Both powers can harm friendly and neutral actors. Terrain is unchanged.
- Hell gains Hellrift, machines gain the three-pulse Extinction strike, and the
  Forsaken gain Sepulchral Rapture. Existing subfaction powers remain available.
- Added twenty generated sprite sheets, icons and a shared-arsenal website gallery.
  The human missile installation currently reuses human tech-building artwork.
- Passed 111 Python tests, 120 C# assertions, engine asset validation and 53
  native production/combat/superweapon checks, plus 78 existing-power regression
  checks. Published alpha.2 is unchanged.

## Painted new-realm roster — development

- Replaced temporary graphics with 51 painted sheets: 23 buildings and 28 units
  across the Noetic Assembly, Forsaken Host and all eight subfactions.
- Added matching build icons, eight-direction unit poses, building construction
  and damage states, collector graphics, MCVs, yards and wreck bindings.
- Expanded the development website gallery to the full current roster. Preserved
  source images, exact prompts and SHA-256 provenance for reproducible packing.
- Added eight distinct subfaction flags and fixed the missing tooltip flag crash.
- Passed 108 Python tests, engine asset checks, native rendering smoke and all
  96 paid-production checks across the eight new subfactions.
- This is initial animation coverage: four authored states per unit facing, with
  held wrecks; longer cycles and bespoke mobile damage bodies remain polish.
  Published alpha.2 downloads remain unchanged.

## Noetic Assembly and Forsaken Host — development expansion

- Added two original realms with four subfactions each, bringing development
  selection to twenty while preserving all twelve existing choices.
- Added sixteen exclusive units, separate shared armies/economies and eight
  combat doctrines with distinct strengths and counterplay.
- Added machine and fallen HUD themes and original eight-direction vector
  prototype unit sprites with movement, firing and death phases.
- Existing building/shared-unit bodies remain temporary. Expanded-roster balance,
  full-match multiplayer and save/load acceptance remain pending; alpha.2 downloads
  are unchanged. See docs/NEW_REALMS.md for mechanics and scope.

## Twelve-faction identity pass (alpha.2)

- Added unique passive mechanics to the nine original choices, retaining the
  Choir, Area Fifty Two and Circle of Contempt doctrines.
- Added nine specialist variants; every faction now has two exclusive units.
- Added twelve distinct powered superweapon arrays, targeting previews, warning
  and impact effects, recharge timers and destruction/power/capture counterplay.
- Added AI technology/array production and faction-specific support decisions.
- Added native twelve-power, autonomous AI, two-client and pending-strike save/load
  acceptance maps. See `docs/FACTION_IDENTITIES.md` for actual mechanics and limits.


## Windows skirmish tester release — 0.3.0-alpha.1

- Self-contained .NET 10.0.13 Windows game, per-user setup, portable ZIP and
  dedicated server; committed project/engine/SDK and dependency/font source archives.
- Fixed empty map-preview texture initialization and ANGLE readback. All three
  public skirmish maps now have previews; developer maps and campaigns stay excluded.
- Replaced an unavailable-source fuzzy dependency with original GPL squad inference,
  retained existing squad rules, and verified completed conquest/replay.
- Added two-client sync-hash and actual save/load round-trip acceptance. Save tests
  resume after the engine's normal paused load menu. Fresh Windows CI repeats them
  against self-contained binaries, then tests installer data preservation.
- Pinned and collected exact library notices and font sources. Packaging reports
  16 covered runtime packages, zero unresolved runtime notices and 21 source components.
- Verified 98 Python tests, 120 C# assertions, 31 native terrain/graphics checks and
  a 49-check twelve-faction executable soak. Detailed scope: docs/TESTER_ALPHA_ACCEPTANCE.md.

## Cliff terrain and twelve-player candidate - 2026-10-25

- Added an original sixteen-frame cliff atlas and native impassable terrain.
- Added The Twelvefold Scar: twelve starting terraces, equal base deposits,
  contested expansions, villages, forests and four repairable bridge crossings.
  Raised ground is visual on the rectangular grid; no elevation combat bonus.
- Fixed a doctrine crash when a projectile hits after its shooter is disposed.
- Added skirmish-only packaging and a per-user Windows setup candidate workflow
  with exact-content validation and user-data-preserving lifecycle checks.
- Verified 91 Python tests, 27 native terrain/projectile checks, 34 doctrine
  regressions, 33 defense regressions and a 49-check twelve-bot combat soak.
- Full map and release limitations: docs/TWELVEFOLD_SCAR.md.

## Three additional subfaction doctrines - 2026-10-25

- Added Choir of Desolation, Area Fifty Two and Circle of Contempt, preserving the
  original nine choices. Lobby, random selection, economy gates and HUDs support twelve.
- Added two exclusive units and one defense per faction, with nine original assets,
  eight-view movement/firing/death frames, icons and a field guide expanded to 87 entries.
- Implemented capped Last Hymn martyrdom, Conviction, SERAPH/ABYSS switching and null
  fields, condemned targets, execution bonuses and temporary Ascendancy.
- Native acceptance: 34 doctrine checks and 39 real paid-production/economy checks
  for the three additions. Full-match balance and multiplayer acceptance remain open.
- Full mechanics, controls and counterplay: docs/SUBFACTIONS.md.

## Skirmish alpha release audit — 2026-10-25

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
