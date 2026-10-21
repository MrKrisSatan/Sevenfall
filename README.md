# SEVENFALL: The War for Creation

**An original apocalyptic real-time strategy game using OpenRA.**

> The Seventh Seal has broken. Heaven has descended, Hell has risen, and humanity refuses to surrender its world.

**Development status:** Pre-alpha **0.2 engine integration**. Builds and opens the game menu on Windows; full gameplay-loop validation and a standalone release remain outstanding.

**[Project website](https://mrkrissatan.github.io/Sevenfall/)** · **[Development roadmap](ROADMAP.md)** · **[To-do list / issues](https://github.com/MrKrisSatan/Sevenfall/issues)** · **[Releases](https://github.com/MrKrisSatan/Sevenfall/releases)** · **[Game design bible](design/GAME_DESIGN.md)**

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

The repository now includes nine faction choices, twelve structure variants, 21 unit variants (including three harvesters), six weapons, localisation, a prototype land AI and an original two-player proving ground. The pinned OpenRA engine builds, all engine YAML checks pass, and the game menu launches on Windows. The full harvest → produce → combat loop and AI behavior still need measured playtests. **No standalone release or installable binary is available yet.**

The first [custom artwork pass](art/README.md) adds three faction power-building sprites, production icons, parent faction emblems and Sevenfall menu branding. Remaining assets still use placeholders.

Use [BUILDING.md](BUILDING.md) to build and launch. See the [integration report](tests/INTEGRATION_REPORT.md) for verified results and [tests/ENGINE_TEST_CHECKLIST.md](tests/ENGINE_TEST_CHECKLIST.md) for the remaining playtest matrix. [TECHNICAL_STARTER.md](TECHNICAL_STARTER.md) preserves the original starter notes.

## Project management

The living checklist is [ROADMAP.md](ROADMAP.md). Individual tasks are tracked in [GitHub Issues](https://github.com/MrKrisSatan/Sevenfall/issues); issues are only checked off once the change is verified. [CHANGELOG.md](CHANGELOG.md) tracks completed updates. Finished, tested builds will be published under [Releases](https://github.com/MrKrisSatan/Sevenfall/releases), not announced before they exist.

## GitHub Pages setup

Site files live in `docs/`. Repository owner: **Settings → Pages → Build and deployment → Deploy from a branch → main → /docs → Save**. After GitHub publishes the site, visit https://mrkrissatan.github.io/Sevenfall/ . Adding files to the repo does **not** enable Pages automatically.

## Engine & rights

Sevenfall is an original game concept; OpenRA's engine is GPLv3. The current SDK overlay uses unbundled Red Alert content for temporary visuals/gameplay scaffolding. Do not redistribute proprietary assets. Art/audio licensing for the finished original project has not been chosen yet.

Created October 2026.
