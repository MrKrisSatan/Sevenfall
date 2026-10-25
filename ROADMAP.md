# Sevenfall development roadmap

**Status as of 21 October 2026: pre-alpha 0.3 development candidate.** This is a planning checklist, not proof of a running game. See GitHub Issues for current task ownership and discussion.

## Phase 0: Foundation and transparency
- [x] Define original world, factions and Veilglass economy
- [x] Draft first 9 subfaction choices
- [x] Produce OpenRA MiniYaml prototype and static checker locally
- [x] Initialize Sevenfall GitHub repository
- [x] Publish project website source and living roadmap
- [x] Import the starter game rules, weapons, localisation and scripts into the repository
- [x] Pin engine/SDK, build on Windows, pass engine lint and fix menu/lobby load errors
- [ ] Complete in-match runtime and nine-faction playtests
- [ ] Verify clean license/asset provenance for public builds

## Phase 1: First playable skirmish

**0.3 source integration progress (not live-game acceptance):**

- [x] Author Lua mission scripts and map sources for H03, A03 and D02
- [x] Register three previews in the OpenRA mission selector and generate their
      binary test maps from existing Broken Choir terrain during SDK install
- [x] Stage all 39 original eight-facing unit sprite sheets into local SDK
- [x] Add automated mission-map, faction-contract and sprite-staging tests
- [ ] Confirm the three scripts actually start, complete and fail correctly in game
- [x] Integrate an initial authored movement, attack/work and death animation pass for all 24 implemented faction unit designs, plus damage artwork for all 39 buildings; polish and wider gameplay acceptance remain
- [ ] Release a truly tested standalone Windows prototype, once asset rights permit


- [ ] Nine factions appear as selectable choices
- [ ] Construction yard / power plant / refinery placement works
- [ ] Three faction-specific harvesters mine and unload Veilglass
- [ ] Infantry and vehicle production works, including prerequisites
- [ ] Units navigate, attack, take damage and die
- [ ] Player victory and defeat conditions work
- [ ] Two human-controlled teams can finish a skirmish
- [ ] Bot AI can harvest, build and attack in a complete match
- [ ] Ship a reproducible, engine-verified pre-alpha build

## Phase 2: Mechanical asymmetry
- [ ] Angels: shields, elite air units, expensive reinforcements
- [ ] Humans: repair, fortifications, combined-arms and artillery doctrine
- [ ] Demons: swarms, corruption, infernal gateways and attrition
- [ ] Give each of nine subfactions an exclusive tech branch and meaningful passive
- [ ] Tune economy, counters, tech pacing and superweapons

## Phase 3: Original world and presentation
- [x] Add intact sprites and icons for the current base/support building roster across three parent factions
- [ ] Complete original combat-unit, aircraft, naval and beast sprites
- [ ] Add building construction/damage frames and unit animation sets
- [ ] Replace every Red Alert placeholder with licensable, original artwork and audio
- [ ] Original Veilglass deposits, refinery effects and resource hazards
- [ ] Nine subfaction colours/emblems, UI and ambient battlefield cues
- [ ] Original multiplayer and skirmish maps
- [ ] Full menus, tooltips, tutorial and accessibility settings

## Phase 4: Campaigns and release
- [x] Specify 75 narrative missions (25 each for Human, Angel and Demon) across five acts; design-only, not playable
- [ ] Angel campaign: implement and validate all 25 missions
- [ ] Human campaign: implement and validate all 25 missions
- [ ] Demon campaign: implement and validate all 25 missions
- [ ] Implement three alternate Harrow finales and all six narrative ending variants
- [ ] Scripted objectives, mission briefings and cinematics
- [ ] Save/resume and mission progression tests
- [ ] Windows and Linux packaging
- [ ] Automated builds, changelog and reproducible release process
- [ ] Gameplay balance, performance and regression passes

## Build policy

Only mark a build **playable** after OpenRA actually launches, the resource economy operates and a skirmish can end correctly. Publish tested binaries under [GitHub Releases](https://github.com/MrKrisSatan/Sevenfall/releases). Development notes and source commits must not be labelled as playable downloads.

The canonical narrative and 75 mission specifications live in [STORY_BIBLE.md](design/STORY_BIBLE.md) and [CAMPAIGN_MISSIONS.md](design/CAMPAIGN_MISSIONS.md). These are design specifications, not shipped game content.

Track fine-grained tasks in [GitHub Issues](https://github.com/MrKrisSatan/Sevenfall/issues).
