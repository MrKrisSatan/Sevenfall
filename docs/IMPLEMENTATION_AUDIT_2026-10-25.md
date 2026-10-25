# Sevenfall implementation audit — 25 October 2026

Audited upstream main **681cf3b1e2ee6f4eae4b1929efb1d0cb48998a18**, including all
nine commits since the directional artwork pass `44d6afa`. Sources inspected:
rules, weapons, native extension, animation bindings/manifests, Lua missions,
installer/build scripts, CI, tests/runbooks, design/story documents, galleries,
open issues, pull requests and releases. This is a source and automated-validation
audit, not an exhaustive visual acceptance of every animation frame or a full
interactive campaign/skirmish playthrough.

The subsequent user-requested faction asymmetry implementation is described in
[Faction balance](../design/FACTION_BALANCE.md). Items below account for that pass.

## Evaluation of the latest work

| Area | Evidence and assessment |
|---|---|
| Engine foundation | Pinned OpenRA/SDK, Windows build wrapper, original branding and software-cursor fix. Upstream Windows CI passed at the audited SHA. A working development overlay, not yet a standalone distribution. |
| Factions/economy | Nine faction selections, parent/subfaction prerequisite gates, three physical harvesting chains, land AI and an original two-player proving ground are implemented. Full nine-faction acceptance remains unrecorded. |
| Unit visuals | 24 implemented faction designs have authored movement, attack/work and death cycles, with 13 damaged variants. The 15 extra ship/aircraft/kennel concepts are directional art without gameplay actors. |
| Buildings/defenses | 39 base/support designs plus 15 defenses = 54 building designs. Damage states exist. The new native defense manager implements dread conversion, sanctuary protection, light crossings and obstacles; this is real mechanics work. |
| Diagnostic evidence | Committed reports record 33 native defense assertions and animation testing through 24 unit death spawns. These narrow diagnostic results do not establish full-match balance, network determinism or campaign completion. |
| Campaigns | Three scripted previews (H03/A03/D02), mission registration, objective tests and an expanded 75-mission design. The remaining 72 are specifications; the three previews reuse proving-ground terrain. Opening cinematic is a screenplay only. |
| Presentation/tooling | 78-entry field guide, 39-design directional gallery, reproducible packing, hashes and CI are substantial infrastructure. Website artwork counts must not be confused with buildable unit counts. |
| New asymmetry pass | Distinct weapon/stat tuning for 18 combat designs, Angel Renewal, Human depot engineering and Demon Blood Frenzy. Full tech trees and competitive balance remain unfinished. |

## Checks performed during this audit

- Upstream: **47 Python tests passed**, after installing the declared `lupa==2.6`
  test dependency into an ignored local tools directory; static project checker
  passed; **seven C# dread assertions passed**.
- After asymmetry implementation: **53 Python tests passed**, pinned engine and
  native extension compiled, engine YAML/Fluent checks passed for nine maps and
  four tilesets.
- The initial local engine checkout was incomplete. It was preserved under
  `.tools/engine-incomplete-20261025`, then replaced with a fresh checkout at the
  exact pinned engine commit before the successful build.
- The engine build reports two NU1901 warnings concerning its pinned upstream
  NuGet.CommandLine dependency. Resolve through a tested dependency/engine update;
  the warnings did not prevent compilation.
- GitHub had **no open pull requests and no published releases** at inspection.
- No fresh native defense diagnostic, complete match, multiplayer session or
  campaign victory/defeat was performed for this audit.

## Prioritized remaining implementation and acceptance work

### P0 — establish a trustworthy playable baseline

1. **Correct campaign harvesting accounting.** All three scripts accumulate only
   positive changes in stored resources sampled once per second. Spending between
   samples can hide valid income. A Lua harness reproduction with three 300-credit
   deliveries spent before each poll leaves the 900-credit objective incomplete in
   all three previews. Replace this with actual unload/cumulative-earned accounting,
   test spending while harvesting, and count deliveries independently if required.
2. **Complete the nine-subfaction runtime matrix.** Verify spawning/deployment,
   placement, two actual harvesting/unloading trips, depletion/starvation,
   replacement collectors, legal production/exclusives, combat and win/loss.
   Record failures and outcomes in `tests/SKIRMISH_RUNBOOK.md`.
3. **Finish acceptance of H03/A03/D02.** Test menu entry, actual production,
   objective ordering, preservation bonuses, selling/capture/replacement, defeat
   and enemy AI in the native engine. Passing Lua API-double tests is insufficient.
4. **Validate multiplayer and replay safety.** Test two human players, ownership
   conversion, alliances, capture, disconnects and replays. Stress the new defense
   manager: it scans units against sources every five ticks; large armies and long
   walls need profiling before optimization or deterministic-network claims.

### P1 — complete the playable army and technology loop

5. **Implement the 15 additional unit concepts.** For each faction add a surface
   ship, submarine, vertical aircraft, fixed-wing aircraft and kennel beast. Supply
   actor rules, movement/terrain layers, weapons and counters, production gates,
   docking/rearming, anti-sub detection, AI use and animation/death behavior.
   Existing naval yards, helipads, airfields and kennels currently lack these units.
6. **Enable and validate replacement/expansion MCV production.** The installer
   hides inherited vanilla buildables; MCV overrides do not restore Buildable.
   Starting deployment is present, but economic expansion and AI replacement need
   an intentional tech/cost/production rule and tests.
7. **Build meaningful research trees.** Technology centers exist, but research
   options are absent. Add upgrades, prerequisites, costs, completion effects and
   UI feedback; make nine exclusive branches more than one exclusive troop each.
8. **Extend faction mechanics beyond the new initial specialties.** Angel shield
   pools/beacons and elite air; Human mobile engineering, sensors and support units;
   Demon temporary corruption, gateways and swarm support. Preserve counterplay
   and avoid reimplementing the already-working dread/defense mechanics.
9. **Finish the wider designed roster.** Reconcile the new art names with the
   design bible before duplicating roles. Still-planned examples include Angel
   scouts/healers/carriers, Human medics/engineers/APCs/mobile repair/AA trucks and
   advanced Demon support, artillery and colossal units.
10. **Implement support powers and superweapons.** Edict of Dawn, Lazarus Protocol
    and the Ninth Mouth need structures, charge/power rules, telegraphs, targeting,
    effects, counterplay, AI and tests. Their existence in lore is not implementation.
11. **Develop the AI beyond one generic land profile.** Test current defense and
    economy behavior, then add expansion, tech progression, intelligent army mixes,
    faction tactics and air/naval usage. Existing AI is not absent; its strategic
    breadth and end-to-end reliability are the gap.

### P2 — balance, battlefields and presentation

12. **Measure and tune asymmetry.** Run equal-cost army matchups and nine-subfaction
    matches, not just unit duels. Validate recovery interruption, frenzy lifetime,
    depot repair cost/rate, garrison weapons, missile range, artillery minimum range
    and early economic timing. Revisit lethal light-wall cost and dread counterplay.
13. **Create production maps and original terrain.** The playable arena is a flat
    proving ground; galleries/diagnostics are not multiplayer maps. Add varied
    skirmish maps, naval routes, expansion layouts and 1–8-player performance tests.
    Campaign previews need their own objective-driven terrain.
14. **Finish visual animation and effects.** Polish gait, facings, ground anchors,
    occlusion and silhouettes. Add dedicated prone/parachute/idle and construction
    cycles, remaining air/naval/beast animation, original projectiles, muzzle and
    impact effects, refinery activity and resource hazards. Damage and combat
    animation already exist and should be refined rather than started over.
15. **Finish team readability and audio.** Replace owner-marker-only identification
    with suitable team-color treatment; add nine subfaction identity details,
    voices, alerts, music and original battlefield sounds. Mourning audio exists,
    but the wider sound/effects library still relies on placeholders.
16. **Finish player-facing UX.** Add tutorials, clear nontechnical objective text
    (current missions expose actor IDs), mission briefings, settings/accessibility
    validation, localization coverage and coherent faction help/technology views.
17. **Expand Veilglass mechanics.** Original deposits and physical economy are
    present. Seamfall warning pulses, rich-field hazards, faction mitigation and
    the planned Veil Dominion objective mode remain design work.

### P3 — campaigns and standalone release

18. **Implement the remaining 72 missions after accepting the first three.** Add
    bespoke maps, encounters, civilian/convoy/story actors, branching choices,
    progression/unlocks, three finales and six endings; validate save/load and
    mission transitions. The 75 mission entries are a design atlas, not 75 maps.
19. **Produce the opening cinematic and story presentation.** Storyboards, assets,
    voice/audio, rendering and in-game playback/skip/subtitles are still required.
20. **Remove the proprietary-content dependency.** The installer constructs an RA
    overlay and mounts `ra|` assets. Replace remaining terrain, UI, sounds, cursors,
    effects and dependencies; establish an asset-rights/attribution inventory and
    content license. Current art provenance hashes are useful but not the whole
    distribution review.
21. **Package and verify Windows/Linux releases.** Create clean standalone packages,
    test on clean machines, add Linux CI, publish binaries/checksums/install guides
    and known issues. Current Windows CI compiles/tests source and does not publish
    a release or run the native content-dependent scenarios.

## Documentation and tracking corrections

- `ROADMAP.md` still leaves broad animation/damage items unchecked although the
  initial pass is integrated. Separate implementation, polish and acceptance.
- `BUILDING.md` and `art/BUILDINGS.md` still describe defenses/damage as future work
  in places; read the newer defense and animation reports for actual coverage.
- Issue #10 opens by saying no mission code exists, then lists the three previews;
  issues #1/#2 also retain old foundational acceptance text. Reconcile evidence
  before closing issues; do not infer live acceptance from a commit.
- Build prose says both Veilglass grades supply the same credits, but rules define
  Ore=30 and Gems=55. Clarify that both feed one currency, at different values.
- The earlier broad design remains a target, not an instruction to claim every
  described feature has shipped. Preserve that distinction in future status pages.

Recommended order: mining-accounting fix → nine-faction/three-preview acceptance →
asymmetry tuning → full air/naval/beast production → research/AI expansion →
original maps/assets → campaign production → standalone releases.
