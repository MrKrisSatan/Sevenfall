# Sevenfall development roadmap

## New realms development expansion

- [x] Noetic Assembly and Forsaken Host, four selectable subfactions each.
- [x] Sixteen exclusive units, two independent technology/economy branches, bot
  build lists, eight combat doctrines and two HUD themes.
- [x] Original prototype directional sprites and a development roster page.
- [ ] Bespoke building/shared-unit artwork and polished exclusive-unit animation.
- [ ] Expanded-roster full-match balance, multiplayer/save-load and release acceptance.

Mechanics, limitations and native component evidence: [new realms](docs/NEW_REALMS.md).

**Current milestone: [0.3.0-alpha.2 Windows skirmish tester alpha](https://github.com/MrKrisSatan/Sevenfall/releases/tag/v0.3.0-alpha.2).**
Twelve faction choices, two exclusive units and one superweapon per choice, and
three public skirmish maps are shipped. Campaigns and broader competitive balance
remain in development. This checklist distinguishes implemented features from
full-match and platform acceptance; see the [issue review](docs/ISSUE_REVIEW_2026-10-25.md)
and [native acceptance evidence](docs/TESTER_ALPHA_ACCEPTANCE.md).

## Phase 0: Foundation and distribution evidence

- [x] Define original world, factions, Veilglass economy and the initial starter source ([#1](https://github.com/MrKrisSatan/Sevenfall/issues/1)).
- [x] Pin engine/SDK, build and launch, validate rules/sprites/interface, and provide reproducible development commands ([#2](https://github.com/MrKrisSatan/Sevenfall/issues/2)).
- [x] Publish the project website and field guide; GitHub Pages is live ([#11](https://github.com/MrKrisSatan/Sevenfall/issues/11)).
- [x] Supply runtime notices, exact corresponding font/dependency sources, source revisions and checksums for accepted Windows builds.
- [x] Publish standalone Windows setup and portable downloads; validate installation, reinstallation and uninstall with retained user data.
- [ ] Deliver equivalent native Linux packaging and acceptance ([#27](https://github.com/MrKrisSatan/Sevenfall/issues/27)).

## Phase 1: Skirmish implementation and remaining acceptance

- [x] Twelve selectable factions, parent MCVs, deployed yards, legal structures and faction prerequisites ([#3](https://github.com/MrKrisSatan/Sevenfall/issues/3)).
- [x] Three physical Veilglass collector/refinery chains, accepted-income accounting, depleting deposits and original resource hazards ([#4](https://github.com/MrKrisSatan/Sevenfall/issues/4)).
- [x] Paid basic infantry/vehicle production and original/additional faction production diagnostics.
- [x] Native locomotion, cliffs, combat, damage and death behavior; genuine unassisted AI conquest and finalized replay playback.
- [x] Two independent clients plus dedicated server pass controlled mechanics and simulation-hash checks.
- [x] Native save/load uses normal game paths; alpha.2 also restores a save taken during pending superweapon warnings.
- [ ] Complete a normal two-player, player-controlled conquest match and record both results/replay ([#5](https://github.com/MrKrisSatan/Sevenfall/issues/5)).
- [ ] Finish ordinary AI expansion/recovery and human-vs-AI full-match acceptance ([#6](https://github.com/MrKrisSatan/Sevenfall/issues/6)).
- [ ] Cover deposit starvation, lost collectors/refineries and blocked-route recovery explicitly ([#23](https://github.com/MrKrisSatan/Sevenfall/issues/23)).
- [ ] Validate Internet/NAT/latency and disconnect/reconnect behavior ([#24](https://github.com/MrKrisSatan/Sevenfall/issues/24)).
- [ ] Benchmark sustained twelve-player load and graphics compatibility ([#25](https://github.com/MrKrisSatan/Sevenfall/issues/25)).

## Phase 2: Faction identity and balance

- [x] Implement parent Renewal, field engineering and Blood Frenzy.
- [x] Implement Choir hymn/Resonance, Area Fifty Two containment protocols and Circle condemnation/execution.
- [x] Give all twelve choices distinct mechanics, two exclusive units each and an exclusive powered superweapon ([#8](https://github.com/MrKrisSatan/Sevenfall/issues/8)).
- [x] Add targeting previews, visible warnings, recharge and destruction/power/capture counterplay; document all [faction identities](docs/FACTION_IDENTITIES.md).
- [x] Add AI technology/specialist/array production plans; prepared native tests verify independent power launches by all twelve faction AIs.
- [x] Implement original parent defenses: light barriers, sanctuary, garrisons, physical obstacles and demonic dread conversion.
- [ ] Validate normally paid advanced branches and full-match balance for all twelve choices ([#22](https://github.com/MrKrisSatan/Sevenfall/issues/22)).
- [ ] Extend parent asymmetry with actual infernal gateways and further domain mechanics ([#7](https://github.com/MrKrisSatan/Sevenfall/issues/7)).
- [ ] Implement and validate aircraft, naval and beast production/combat before enabling them in public packages ([#28](https://github.com/MrKrisSatan/Sevenfall/issues/28)).

## Phase 3: Original world and presentation

- [x] Integrate original unit/building bodies, initial motion/attack/death cycles and damage states, plus original public skirmish maps and impassable cliff terraces.
- [x] Publish a 108-entry field guide: 69 building entries and 39 unit entries, including twelve array variants and nine specialist variants using existing authored bodies.
- [x] Provide 39-design directional concept/reference artwork, including future aircraft/naval/beast designs.
- [ ] Finish bespoke faction emblems, variant artwork/icons where needed, construction/effect polish, SFX, voices, music and ambient coverage ([#9](https://github.com/MrKrisSatan/Sevenfall/issues/9)).
- [ ] Complete native audiovisual/accessibility and GPU acceptance as presentation expands ([#9](https://github.com/MrKrisSatan/Sevenfall/issues/9), [#25](https://github.com/MrKrisSatan/Sevenfall/issues/25)).

## Phase 4: Campaigns and full-game release

- [x] Specify 75 narrative missions, 25 per realm, with story continuity and planned finale/ending variants. These are design specifications.
- [x] Add H03, A03 and D02 developer preview scripts, mission registration, test terrain and automated objective/refinery-income tests.
- [ ] Validate those three previews through native victory, failure, economy and save/resume, and replace temporary layouts ([#26](https://github.com/MrKrisSatan/Sevenfall/issues/26)).
- [ ] Implement and validate the remaining 72 missions, campaign progression, three Harrow finales and six ethical ending variants ([#10](https://github.com/MrKrisSatan/Sevenfall/issues/10)).
- [ ] Integrate accepted campaigns into the full-game release profile and complete final cross-platform/content/balance acceptance ([#10](https://github.com/MrKrisSatan/Sevenfall/issues/10)).

## Evidence policy

Source contracts, controlled native scenarios, prepared-army AI tests, timed soaks,
complete matches and human playtests are distinct evidence categories. A passing
component test does not mark every matchup or campaign as accepted. Public builds
use the exact successful release-workflow artifacts, their sources and checksums.

The [story bible](design/STORY_BIBLE.md) and [mission atlas](design/CAMPAIGN_MISSIONS.md)
remain the narrative specifications. Track current work and outcomes in
[GitHub Issues](https://github.com/MrKrisSatan/Sevenfall/issues).
