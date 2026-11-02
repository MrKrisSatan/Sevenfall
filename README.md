# SEVENFALL: The War for Creation

An original apocalyptic real-time strategy game built on OpenRA.

**Alpha.3 released: five factions, twenty subfactions, three skirmish maps.**
**Development roster: nine parent factions; the four new factions have no subfactions.**
The Noetic Assembly and Forsaken Host join Humans, Angels and Hell. Each parent
faction has an economy, production buildings, defenses, aircraft, beasts and a
shared superweapon. Each subfaction has two exclusive units and its own doctrine.

[Website](https://mrkrissatan.github.io/Sevenfall/) · [Illustrated field guide](https://mrkrissatan.github.io/Sevenfall/forces.html) · [New factions](https://mrkrissatan.github.io/Sevenfall/new-realms.html) · [Shared arsenal](https://mrkrissatan.github.io/Sevenfall/arsenal.html) · [Releases](https://github.com/MrKrisSatan/Sevenfall/releases) · [Report feedback](https://github.com/MrKrisSatan/Sevenfall/issues)

## Playtesting

[**Download v0.3.0-alpha.3**](https://github.com/MrKrisSatan/Sevenfall/releases/tag/v0.3.0-alpha.3). The release includes the original five realms and twenty choices. The four independent factions below are development additions and are not included in that binary.

Use the Windows x64 setup EXE or extract the entire portable ZIP and run
`Sevenfall.exe`. The package includes its runtime and original game content;
no separate OpenRA, Red Alert or .NET installation is needed.
Choose **Singleplayer → Skirmish**. Deploy your MCV with **F**, build power,
a refinery and production, and fight for Veilglass. Ashen Crossing, Broken Choir
and The Twelvefold Scar are included; the latter supports up to twelve players.
Twenty faction choices do not mean twenty simultaneous player slots.

[Tester guide](docs/TESTER_GUIDE.md) · [Acceptance and known limitations](docs/TESTER_ALPHA_ACCEPTANCE.md) · [Changelog](CHANGELOG.md)

## The original five factions, twenty doctrines

| Faction | Specialisation | Four subfactions |
|---|---|---|
| Humans | Range, combined arms and efficient repairs | Bastion Directorate; Free Earth Union; Ashen Covenant; Area Fifty Two |
| Angels | Durable, costly elites and recovery between engagements | Seraphic Synod; Order of the Gate; The Unshackled; Choir of Desolation |
| Hell | Rapid production, aggressive swarms and combat frenzy | Iron Legions; Blood Brood; Court of Whispers; Circle of Contempt |
| Noetic Assembly | Machine precision, armor, relay networks and adaptive harassment | Echo Directorate; Iron Calculus; Custodian Grid; Paradox Collegium |
| Forsaken Host | Fallen aristocrats, dangerous hymn formations, wounded aggression and isolated hunters | Ashen Thrones; Hollow Choir; Carrion Testament; Broken Firmament |

The new factions use original designs inspired by broad science-fiction and
religious-horror themes. They are distinct from both native demons and the
angelic Unshackled. [New faction mechanics and counterplay](docs/NEW_REALMS.md).
[Original twelve doctrines](docs/FACTION_IDENTITIES.md).

## Four independent factions — no subfactions

| Faction | Army and playstyle | Building-bound power |
|---|---|---|
| Veilborn | Living crystal; protect costly units inside a powered growth network | Bloom / Heart Prism |
| Unwritten | Fragile Memory Infantry, decoys and temporary infantry restored from recent losses | Restoration / Archive of Names |
| Outer Silence | Cloaked Hush Stalkers, isolated flanking groups, suppression and Null Leviathans | Absolute Silence / Null Cathedral |
| Nephilim Remnant | Oathbound Giants and Mountain Bearers supported by vulnerable attendants | Earthbreaker / Ancestral Cairn |

Each has a complete economy, construction yard/MCV, production, technology, repair, two defenses, aircraft, beast, engineer, harvester and signature combat roster. Their **94 original painted atlases** include construction/damage states and eight-direction units. The field guide now contains **275 entries: 158 buildings and 117 units**, including explicitly labelled future concepts.

The Unwritten, Outer Silence and Nephilim Remnant are selectable in development skirmish and appear only as NPCs in campaigns, usually neutral. **Veilborn is authored but hidden from the normal lobby while campaign progression is unfinished.** No extra subfactions have been added.

[Illustrated profiles and complete rosters](https://mrkrissatan.github.io/Sevenfall/additional-realms.html) · [Design and counterplay](design/ADDITIONAL_REALMS.md)

## Shared arsenal and battlefield systems

| Faction | Aircraft | Beast | Shared superweapon |
|---|---|---|---|
| Humans | Bastion Gunship | Ironjaw Warhound | Nuclear missile |
| Angels | Sky Warden | Covenant Gryphon | Witness of Salt |
| Hell | Ash Wyvern | Cinder Hound | Hellrift |
| Noetic Assembly | Vector Interceptor | Logic Stalker | Extinction |
| Forsaken Host | Mourning Kite | Carrion Chimera | Sepulchral Rapture |

The published alpha’s **17 superweapons** are building-bound: twelve original subfaction powers
and five shared realm powers. Their icons automatically charge in **Defences**.
Losing the last supplying building removes the power; rebuilding starts a fresh
charge. Low power pauses charging. The shared installations require technology,
cost 6000 and consume 250 power, with a five-minute recharge and five-second warning.
The Witness opens three wing pairs, flashes, and turns units, structures, trees
and bridges within four cells into salt statues that crumble four seconds later.
Both it and Nuclear can harm friendly and neutral actors. [Full arsenal](docs/SHARED_ARSENAL.md).

Veilglass supports a physical harvesting economy and explodes on non-harvester
contact, spreading deposits and damaging nearby actors. Civilian houses can be
garrisoned, damaged and destroyed. Engineers repair surviving houses and restore
bridges through repair posts. Cliff terraces block movement; they do not grant
high-ground combat bonuses.

The field guide contains **275 illustrated entries: 158 buildings and 117 units**,
including six clearly labelled unavailable naval/fixed-wing production concepts.
The released five-realm expansion adds **71 painted sprite sheets**: 51 for the two new realms and
20 for the shared arsenal. Units include eight directions and initial animation
poses. Twelve original power arrays and the human nuclear installation reuse
technology-building artwork. [Artwork and source provenance](art/README.md).

## Alpha scope

- Windows x64 skirmishes, AI opponents, local multiplayer, saves and replays.
- Aircraft and beasts are playable. Naval units and fixed-wing aircraft remain future work.
- Early animation, audio and balance; broad Internet, GPU and large-army testing is welcome.
- Three campaign previews remain developer-only. The planned 150-mission campaigns are unfinished.
- Unsigned executables. Save/replay compatibility between alpha versions is not promised.

## Development

Run [PLAY_SEVENFALL_DEV.cmd](PLAY_SEVENFALL_DEV.cmd), or follow [BUILDING.md](BUILDING.md)
with .NET SDK 10.0.402. The pinned engine is bundled with a reviewed source overlay.
Corresponding project, engine, SDK, dependency and font sources accompany releases.

[Roadmap](ROADMAP.md) · [Game design](design/GAME_DESIGN.md) · [Story bible](design/STORY_BIBLE.md) · [Planned opening cinematic](design/OPENING_CINEMATIC.md) · [Campaign previews](https://mrkrissatan.github.io/Sevenfall/campaigns.html) · [License](COPYING)
