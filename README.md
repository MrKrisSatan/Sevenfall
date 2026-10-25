# SEVENFALL: The War for Creation

**An original apocalyptic real-time strategy game using OpenRA.**

> The Seventh Seal has broken. Heaven has descended, Hell has risen, and humanity refuses to surrender its world.

**Development status:** **0.3 Windows skirmish tester alpha**. The standalone package includes twelve faction choices and three skirmish maps. Campaign completion and broader balance/content work remain in development. See the [tester guide](docs/TESTER_GUIDE.md) and [acceptance evidence](docs/TESTER_ALPHA_ACCEPTANCE.md).

The faction identity pass gives **all twelve hosts distinct mechanics, two exclusive
units each and a unique superweapon**. See [faction identities, controls and
counterplay](docs/FACTION_IDENTITIES.md). Nine specialist variants reuse the game's
authored animated bodies; twelve new arrays use faction technology-building art.

**[Project website](https://mrkrissatan.github.io/Sevenfall/)** · **[Campaign preview](https://mrkrissatan.github.io/Sevenfall/campaigns.html)** · **[Illustrated faction field guide](https://mrkrissatan.github.io/Sevenfall/forces.html)** · **[Development roadmap](ROADMAP.md)** · **[To-do list / issues](https://github.com/MrKrisSatan/Sevenfall/issues)** · **[Releases](https://github.com/MrKrisSatan/Sevenfall/releases)** · **[Game design bible](design/GAME_DESIGN.md)**

The field guide includes images and descriptions for all **69 building entries
and 39 unit entries**, including twelve superweapon arrays and nine specialist variants, with faction and subfaction filters. Combat-unit images are
original concept illustrations. The [eight-direction artwork gallery](https://mrkrissatan.github.io/Sevenfall/turnarounds.html) adds **312 directional images for 39 designs**, including ships, aircraft and beasts. [PNG frames, sprite sheets and prompts](art/unit-turnarounds/README.md) are included. The [animation and damage pass](art/animations/README.md) now binds movement, attack/work and death cycles for all 30 implemented faction unit designs, damaged unit variants, and heavy/critical damage artwork for all 57 building designs. Additional aircraft, naval and beast concepts still require gameplay implementation.

## Play the Windows skirmish alpha

Download the setup EXE or portable ZIP from **[v0.3.0-alpha.2](https://github.com/MrKrisSatan/Sevenfall/releases/tag/v0.3.0-alpha.2)**.
The game bundles its runtime and content: OpenRA, Red Alert and a separate .NET
installation are not required. Choose **Singleplayer → Skirmish**; The Twelvefold
Scar supports up to twelve players. Sources, dependency/font sources and checksums
accompany the tester release. Read [known alpha scope](docs/TESTER_ALPHA_ACCEPTANCE.md).

For development, clone and run **[PLAY_SEVENFALL_DEV.cmd](PLAY_SEVENFALL_DEV.cmd)**,
or follow [BUILDING.md](BUILDING.md) with .NET SDK 10.0.402. Contributor builds retain
three campaign previews, excluded from the public skirmish package. Select
**Singleplayer → Missions** to inspect one of the three new 0.3 previews:

- **H03 The Glass Fields**: Humans versus Blood Brood.
- **A03 A Glass of Wrath**: Angels versus Blood Brood.
- **D02 Seeds of Ruin**: Demons versus Bastion Directorate.

Their sources include actual OpenRA Lua objective scripts and scenario actors.
They are **not yet proven playable through victory and defeat in a live match**.
Report observed outcomes using [the First War runbook](tests/FIRST_WAR_RUNBOOK.md).

## The premise

The Book of Revelation has come to pass. The broken boundary between Heaven, Earth and Hell has produced **Veilglass**, crystallised creation energy. Angels need it to sustain celestial war machines. Humans refine it to power their industrial resistance. Demons corrupt it to feed infernal armies.

The three major factions each have four playable subfactions:

| Angels | Humans | Demons |
|---|---|---|
| Seraphic Synod | Bastion Directorate | Iron Legions |
| Order of the Gate | Free Earth Union | Blood Brood |
| The Unshackled | Ashen Covenant | Court of Whispers |
| Choir of Desolation | Area Fifty Two | Circle of Contempt |

## Gameplay pillars

- Classic **Command & Conquer** economy: construction yards, power plants, physical harvesters, refineries, base construction and large armies.
- Three **asymmetric faction doctrines**: elite Angels, flexible Human combined arms, and aggressive Demonic swarms.
- Twelve subfactions, diverse units and tech trees, field control, superweapons and three planned campaigns.
- Custom art, audio and maps in the finished game.

## What is actually implemented?

[The Twelvefold Scar](docs/TWELVEFOLD_SCAR.md) adds a 256×256 skirmish for up to
twelve players: impassable original cliff terraces, equal starting deposits,
contested expansions, villages, forests and four repairable crossings. Elevation
is visual on the existing rectangular grid. Windows candidate CI now packages
the skirmish content separately and builds/tests a per-user setup EXE; public
release acceptance remains open.

The [three additional doctrines](docs/SUBFACTIONS.md) add worshipper martyrdom,
SERAPH/ABYSS containment protocols, and condemned-target execution. Each new
subfaction has two exclusive units and a defense, bringing selection to twelve.


The [faction asymmetry pass](design/FACTION_BALANCE.md) gives Angels durable elites
with delayed health recovery, Humans longer-range combined arms and faster depot
repairs, and Demons rapid production and temporary attack-triggered frenzy. All 18
combat designs have explicit stats and faction weapons, including garrison weapons.
These are initial balance values; full-match tuning remains outstanding.

See the [25 October implementation audit](docs/IMPLEMENTATION_AUDIT_2026-10-25.md)
for evaluated changes, verification limits and the prioritized remaining backlog.

The [faction defense pass](docs/DEFENSES.md) adds moaning flesh walls that convert
enemy infantry, lethal powered light curtains, sanctuary protection, concrete and
razorwire, three-person entrenchments, and faction ground/anti-air turrets.
All 15 defenses have original art and damage states; 33 native acceptance checks
exercise their effects and counters.

The skirmish alpha includes twelve faction choices, original faction units, structures and defenses, physical harvesting, faction weapons, localisation and land AI. Completed autonomous conquest and replay, two-client synchronization and save/load checks are recorded in [tester acceptance](docs/TESTER_ALPHA_ACCEPTANCE.md). The package has a per-user installer and a portable executable; every faction matchup and large-army balance remain tester work.

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

Sevenfall is an original game concept using the GPLv3 OpenRA engine. Standalone staging copies only adapted textual OpenRA definitions, with attribution, and uses original Sevenfall graphics plus intentionally limited alpha audio. See [distribution notices](THIRD_PARTY_NOTICES.md). Dependency source/licence verification remains a publication gate.

Created October 2026.
