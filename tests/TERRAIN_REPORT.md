# Cliff terrain and twelve-player acceptance — 25 October 2026

Gameplay source: `331f80bc47d93ef378e16af46ea3c093016d7e39`.
Windows development host, pinned OpenRA release-20250330 engine, fresh support
directories per diagnostic. The terrain test ran against the committed map.

| Check | Result |
|---|---|
| Python suite, including seven map and five package-profile checks | 91 passed |
| Native terrain/pathing/MCV/delayed-projectile diagnostic | 27 passed |
| Native doctrine regression after disposed-shooter fix | 34 passed |
| Native defense regression | 33 passed |
| Twelve-faction, five-game-minute autonomous soak before road texture correction | 49 passed; 214 attributed kills |
| Twelve-faction soak on committed final map | 49 passed; 240 attributed kills |
| Engine integration on GitHub, Windows and Linux | Passed |
| Exact packaged rules, sprites and interface validation on GitHub | Passed |
| Setup EXE compilation and install/reinstall/uninstall with preserved user data | Passed on GitHub Windows runner |
| Source archives and binary/source SHA-256 artifacts | Generated successfully |

The first autonomous soak exposed a real impact-time exception when doctrine
damage code queried traits on a disposed shooter. Damage now skips doctrine
lookup for disposed actors while preserving the base projectile hit. The native
terrain diagnostic kills a shooter before its slow projectile lands, then verifies
that the target takes damage without a crash.

Live visual inspection checked a starting terrace, cliff entrances, active
harvesting and buildings. Wide roads were changed to continuous gravel after
the first soak; native terrain checks were rerun and passed afterward.

Map binary SHA-256:
`8dd728c104a666eb06d6e7d3beb598eebdfb7193c898eb80d8fc6708e697e7f6`.

The twelve-bot scenario observes real queues, mining and combat without scripted
production/movement/attack orders. It stops after the timed assertions; it does
not certify completed conquest, finalized replay, all-faction balance, multiplayer,
save/load or an independent clean Windows machine. Native impassable Rock blocks
ground movement; terrace elevation remains visual and grants no combat bonus.

Reproduction commands and content notes: [TWELVEFOLD_SCAR.md](../docs/TWELVEFOLD_SCAR.md).

Candidate build and artifacts:
[Windows skirmish candidate #1](https://github.com/MrKrisSatan/Sevenfall/actions/runs/40217579692).
This creates a test candidate, not a public release.

## Downloaded candidate graphics finding

The exact candidate #1 archive was downloaded and its SHA-256 checksums verified.
Its installer lifecycle checked 860 installed file hashes and preserved settings
and saves. Local menu testing then exposed an ANGLE texture-readback/framebuffer
exception while loading map thumbnails (NVIDIA RTX 3060, driver 610.88).
This demonstrates why installer and utility acceptance alone cannot approve release.
Selecting native OpenGL (`Graphics.GLProfile=Modern`) avoided that exception and
allowed selection of The Twelvefold Scar in the normal twelve-slot lobby.
The package now seeds that tested renderer preference; a rebuilt candidate must
pass before replacing #1. Other GPU/driver combinations remain untested.
