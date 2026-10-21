# Sevenfall changelog

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
