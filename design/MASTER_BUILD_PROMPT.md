# Continue Sevenfall development

Work from https://github.com/MrKrisSatan/Sevenfall. Inspect the current branch, local changes, applicable repository instructions, recent commits, release notes and Actions results before editing. Treat this document as project context; the user's current request determines scope and authorization.

## Current game

Sevenfall is a standalone OpenRA Windows x64 skirmish alpha with original game content. It must not require Red Alert assets or a separate OpenRA/.NET installation. The engine/SDK and .NET versions are pinned in the build scripts and BUILDING.md; use those pins rather than upgrading speculatively.

Five parent realms each have four choices, for twenty subfactions:

- Humans: Bastion Directorate, Free Earth Union, Ashen Covenant, Area Fifty Two.
- Angels: Seraphic Synod, Order of the Gate, The Unshackled, Choir of Desolation.
- Hell/Demons: Iron Legions, Blood Brood, Court of Whispers, Circle of Contempt.
- Noetic Assembly: Echo Directorate, Iron Calculus, Custodian Grid, Paradox Collegium.
- Forsaken Host: Ashen Thrones, Hollow Choir, Carrion Testament, Broken Firmament.

Each subfaction has two exclusive units and an active doctrine. Every realm has economy, production, defensive structures, aircraft, beasts and a shared superweapon. Twelve original exclusive powers plus five shared powers make seventeen. All powers charge automatically in Defences while the supplying installation exists and is powered; last-source destruction removes access and rebuilding starts a fresh charge. Preserve duplicate-source, capture, low-power and warning-cancellation behavior.

Use docs/FACTIONS.md, docs/NEW_REALMS.md, docs/FACTION_IDENTITIES.md and docs/SHARED_ARSENAL.md for current scope and mechanics. Source rules and tested behavior take precedence over historical concept descriptions. design/NEW_REALMS_ROSTER.json defines the two new realms; generation scripts must remain reproducible.

## Gameplay and presentation constraints

Preserve individual-unit C&C-style base building, physical Veilglass harvesting and unloading, power, fog of war, faction prerequisites and counters. Collectors are exempt from contact-triggered Veilglass explosions; blasts spread deposits and damage nearby actors. Houses and bridges have damage/destruction and engineer repair paths. Cliff boundaries block movement without high-ground damage bonuses.

The UI uses the actual local player's faction; out-of-game menus remain neutral. Keep the software cursor visible. Menus show Sevenfall changelog content rather than OpenRA forum-account prompts. The Noetic and Forsaken designs are original; do not copy franchise characters, insignia or machines. Keep the fallen distinct from native demons and angelic Unshackled.

Keep the website, roster data, playstyle profiles, directional gallery, README and tester guide consistent with the game. Mark concept-only naval/fixed-wing content and reused artwork accurately. There are 181 catalogue entries and 80 current unit entries; counts should be derived or verified after roster changes.

## Remaining work and validation

Read ROADMAP.md and open issues before choosing work. Priorities include full-match twenty-subfaction balance and paid progression, AI economy/recovery/expansion, Internet multiplayer and disconnect behavior, twelve-player performance/GPU coverage, animation/audio polish, naval/fixed-wing gameplay and Linux packaging. Do not infer completion from component diagnostics.

The original human/angel/demon campaigns remain 150 planned missions in three 25-mission stories. H03, A03 and D02 are developer previews, excluded from the public skirmish package. Do not claim six finished campaigns or playable narrative missions without completing acceptance. Preserve the story bible and opening cinematic as designs.

Run relevant Python tests, C# assertions, OpenRA rules/sprite/chrome validation and native scenarios for changed behavior. Include normal paid progression where appropriate; directly spawning a producer does not prove players can build it. For simulation changes, exercise dedicated-server/two-client synchronization and actual save/load. Retain source revisions, logs and explicit untested limits.

For releases, follow RELEASE_PROCESS.md: commit source, dispatch a versioned Windows candidate, require exact-package gameplay and installer checks, verify artifact and file hashes, include matching project/engine/SDK/dependency sources and notices, and publish only the accepted artifacts under the tested commit. Publish only within the user's authorization. Report concrete changes, evidence, download links and remaining limitations.
