# SEVENFALL: The War for Creation

**An original apocalyptic real-time strategy game using OpenRA.**

> The Seventh Seal has broken. Heaven has descended, Hell has risen, and humanity refuses to surrender its world.

**Development status:** Pre-alpha **0.3 development candidate**. The pinned Windows engine integration builds and an initial three-mission Lua campaign slice is in source. Live end-to-end skirmish, campaign-win verification and an independently installable release remain outstanding.

**[Project website](https://mrkrissatan.github.io/Sevenfall/)** · **[Campaign preview](https://mrkrissatan.github.io/Sevenfall/campaigns.html)** · **[Illustrated faction field guide](https://mrkrissatan.github.io/Sevenfall/forces.html)** · **[Development roadmap](ROADMAP.md)** · **[To-do list / issues](https://github.com/MrKrisSatan/Sevenfall/issues)** · **[Releases](https://github.com/MrKrisSatan/Sevenfall/releases)** · **[Game design bible](design/GAME_DESIGN.md)**

The field guide includes images and descriptions for all **39 current building designs
and 24 unit designs**, with faction and subfaction filters. Combat-unit images are
original concept illustrations. The [eight-direction artwork gallery](https://mrkrissatan.github.io/Sevenfall/turnarounds.html) adds **312 directional images for 39 designs**, including ships, aircraft and beasts. [PNG frames, sprite sheets and prompts](art/unit-turnarounds/README.md) are included. The [animation and damage pass](art/animations/README.md) now binds movement, attack/work and death cycles for all 24 implemented faction unit designs, damaged unit variants, and heavy/critical damage artwork for all 39 building designs. Additional aircraft, naval and beast concepts still require gameplay implementation.

## Try the 0.3 development candidate (Windows)

Clone the repository and double-click **[PLAY_SEVENFALL_DEV.cmd](PLAY_SEVENFALL_DEV.cmd)**,
or follow [the pinned manual build commands](BUILDING.md). This installs an
OpenRA SDK and builds it **locally**; legally acquired Red Alert game data
is still required and is **not bundled**. After launching, select
**Singleplayer → Missions** to inspect one of the three new 0.3 previews:

- **H03 The Glass Fields**: Humans versus Blood Brood.
- **A03 A Glass of Wrath**: Angels versus Blood Brood.
- **D02 Seeds of Ruin**: Demons versus Bastion Directorate.

Their sources include actual OpenRA Lua objective scripts and scenario actors.
They are **not yet proven playable through victory and defeat in a live match**.
Report observed outcomes using [the First War runbook](tests/FIRST_WAR_RUNBOOK.md).

## The premise

The Book of Revelation has come to pass. The broken boundary between Heaven, Earth and Hell has produced **Veilglass**, crystallised creation energy. Angels need it to sustain celestial war machines. Humans refine it to power their industrial resistance. Demons corrupt it to feed infernal armies.

The three major factions each have three playable subfactions:

| Angels | Humans | Demons |
|---|---|---|
| Seraphic Synod | Bastion Directorate | Iron Legions |
| Order of the Gate | Free Earth Union | Blood Brood |
| The Unshackled | Ashen Covenant | Court of Whispers |

## Gameplay pillars

- Classic **Command & Conquer** economy: construction yards, power plants, physical harvesters, refineries, base construction and large armies.
- Three **asymmetric faction doctrines**: elite Angels, flexible Human combined arms, and aggressive Demonic swarms.
- Nine subfactions, diverse units and tech trees, field control, superweapons and three planned campaigns.
- Custom art, audio and maps in the finished game.

## What is actually implemented?

The repository now includes nine faction choices, 36 structure variants plus three faction Construction Yard designs, 21 unit variants (including three harvesters), six weapons, localisation, a prototype land AI and an original two-player proving ground. The pinned OpenRA engine builds, all engine YAML checks pass, and the game menu launches on Windows. The full harvest → produce → combat loop and AI behavior still need measured playtests. **No standalone release or installable binary is available yet.**

The [custom artwork passes](art/README.md) add faction Construction Yards, power buildings, refineries, eight-direction MCVs and harvesters, fifteen production icons, two grades of Veilglass deposits, parent faction emblems and Sevenfall menu branding. The expanded [building pass](art/BUILDINGS.md) adds 30 building sprites and icons, including faction-specific radar, repair, naval, aircraft, beast-training and technology facilities. Implemented combat units now use original directional and animated art. Sounds, projectiles and other unconverted assets still use placeholders.

Use [BUILDING.md](BUILDING.md) to build and launch. See the [integration report](tests/INTEGRATION_REPORT.md) for verified results and [tests/ENGINE_TEST_CHECKLIST.md](tests/ENGINE_TEST_CHECKLIST.md) for the remaining playtest matrix. [TECHNICAL_STARTER.md](TECHNICAL_STARTER.md) preserves the original starter notes.

## Story campaigns

Sevenfall's narrative plan now includes **75 missions**, with **25 missions per main faction**, organized into five acts each. The three campaigns recount intertwined events from Human, Angel and Demon perspectives; their final missions are alternative versions of the same siege. See the [narrative story bible](design/STORY_BIBLE.md) and [full 75-mission atlas](design/CAMPAIGN_MISSIONS.md), including mission objectives, optional objectives, failure conditions and continuity notes. **Three source-backed previews (H03, A03 and D02) are implemented as described above; the remaining 72 missions are design only. Live end-to-end validation remains outstanding.**

The shared opening cinematic, **[The Seventh Silence](design/OPENING_CINEMATIC.md)**, introduces the three armies and ends at the faction selection screen. This is a written screenplay, not a rendered in-game cutscene.

## Project management

The living checklist is [ROADMAP.md](ROADMAP.md). Individual tasks are tracked in [GitHub Issues](https://github.com/MrKrisSatan/Sevenfall/issues); issues are only checked off once the change is verified. [CHANGELOG.md](CHANGELOG.md) tracks completed updates. Finished, tested builds will be published under [Releases](https://github.com/MrKrisSatan/Sevenfall/releases), not announced before they exist.

## GitHub Pages setup

Site files live in `docs/` and are published by `.github/workflows/pages.yml` when website files change on `main`. In repository Settings → Pages, select **GitHub Actions** as the publishing source. The published site is [https://mrkrissatan.github.io/Sevenfall/](https://mrkrissatan.github.io/Sevenfall/).

## Engine & rights

Sevenfall is an original game concept; OpenRA's engine is GPLv3. The current SDK overlay uses unbundled Red Alert content for temporary visuals/gameplay scaffolding. Do not redistribute proprietary assets. Art/audio licensing for the finished original project has not been chosen yet.

Created October 2026.
