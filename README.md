# SEVENFALL: The War for Creation

**An original apocalyptic real-time strategy game using OpenRA.**

> The Seventh Seal has broken. Heaven has descended, Hell has risen, and humanity refuses to surrender its world.

**Development status:** Pre-alpha **source prototype**. No engine-verified playable build has been released.

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

The previously prepared local v0.1 source seed contains MiniYaml designs for nine faction choices, twelve structure variants, 21 unit variants (including three harvesters), six weapons and initial UI strings, plus SDK overlay/validation scripts. **The prototype source files have not yet been copied into this GitHub repository**; that work is tracked in [issue #1](https://github.com/MrKrisSatan/Sevenfall/issues/1). The prototype is **not yet proven to run in OpenRA**, and the inherited Red Alert placeholders and AI plans require integration tests. **No playable release or installable binary is available yet.**

See [TECHNICAL_STARTER.md](TECHNICAL_STARTER.md) for setup caveats and [tests/ENGINE_TEST_CHECKLIST.md](tests/ENGINE_TEST_CHECKLIST.md) for verification requirements.

## Project management

The living checklist is [ROADMAP.md](ROADMAP.md). Individual tasks are tracked in [GitHub Issues](https://github.com/MrKrisSatan/Sevenfall/issues); issues are only checked off once the change is verified. [CHANGELOG.md](CHANGELOG.md) tracks completed updates. Finished, tested builds will be published under [Releases](https://github.com/MrKrisSatan/Sevenfall/releases), not announced before they exist.

## GitHub Pages setup

Site files live in `docs/`. Repository owner: **Settings → Pages → Build and deployment → Deploy from a branch → main → /docs → Save**. After GitHub publishes the site, visit https://mrkrissatan.github.io/Sevenfall/ . Adding files to the repo does **not** enable Pages automatically.

## Engine & rights

Sevenfall is an original game concept; OpenRA's engine is GPLv3. The current SDK overlay uses unbundled Red Alert content for temporary visuals/gameplay scaffolding. Do not redistribute proprietary assets. Art/audio licensing for the finished original project has not been chosen yet.

Created October 2026.