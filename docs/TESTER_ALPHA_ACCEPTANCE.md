# Skirmish tester alpha acceptance — 25 October 2026

## Alpha.2 faction identity pass

The [twelve-faction identity pass](FACTION_IDENTITIES.md) adds two exclusive units
per faction, nine new specialist variants, nine additional passives and twelve
exclusive superweapons. Source validation: **103 Python tests**, **120 C# assertions**,
engine YAML and chrome checks. Native faction acceptance: **78 checks** covering
all twelve real powers and their counterplay. A separate prepared-army AI scenario
verifies **12 independent faction superweapon launches**, without scripted targeting.

The new two-client variant runs the full 78-check scenario on each independent
client and compares five world-state hashes. The new save/load variant saves at
tick 200, **during the first set of pending strike warnings**, restores through
the normal load order and compares four later hashes plus the full 78 checks.
The Windows packaging workflow runs all these against a disposable copy of the
exact self-contained release binaries, alongside the original regression gates.
The additional diagnostic maps remain absent from the public skirmish profile.

## Alpha.1 baseline evidence

Scope: a complete, self-contained **Windows x64 skirmish alpha for testers**.
This is an early playtest release, not the finished campaign game or a claim that
every faction matchup is balanced. Public downloads include setup, portable game,
project/engine/SDK source, dependency/font source, and SHA-256 checksums.

## Verified evidence

| Check | Evidence |
|---|---|
| Python regression suite | 98 passed |
| C# mechanics and original squad inference | 120 assertions passed |
| Native terrain, locomotion, twelve MCV starts, delayed-projectile regression and actual map-preview rendering | 31 passed |
| Native doctrine mechanics | 34 passed |
| Native defenses | 33 passed in the preceding gameplay pass |
| Unassisted conquest on Broken Choir | Actual win/loss callbacks; both economies harvested; no scripted production, movement, attack or victory orders |
| Conquest after replacing the unavailable-source fuzzy dependency | Humans won naturally; finalized replay metadata ends at tick 18,753 |
| Playback of that completed match | Same win/loss callbacks and normal completion; no sync error |
| Two independent native clients plus dedicated server | 34 doctrine checks on each client, five identical world sync hashes, normal exits |
| Same test with self-contained executable clients/server | Passed locally; also exercised by the fresh Windows runner workflow |
| Save/load through normal save API and load-game lobby order | Four matching world-state hashes against uninterrupted play; 34 doctrine checks on both runs |
| Windows runtime | Self-contained .NET 10.0.13, built with SDK 10.0.402 |
| Distribution notices | 16 runtime packages covered; zero unresolved runtime notices; 21 pinned source components |
| Twelve-faction standalone executable soak | 49 passed; all deployed/mined/fielded at least four combat units cumulatively; 191 attributed kills |
| Fonts | Both shipped TTF files matched GNU FreeFont 20090104 byte for byte; exact SFD source and notices supplied |
| Public map profile | Ashen Crossing, Broken Choir, The Twelvefold Scar, plus hidden menu map; diagnostics and campaign previews excluded |

The [Windows candidate/release workflow](../.github/workflows/windows-candidate.yml)
rebuilds committed source, validates the actual package, and runs native terrain,
two-client synchronization, save/load and installer lifecycle checks on a fresh
Windows runner. External .NET lookup is disabled for native self-contained tests.
Setup is per-user and requires no administrator account. Reinstall and uninstall
must preserve settings and saves; installed payload hashes are verified.

The engine remains pinned to upstream `b4f3d8a`, with a small, source-included,
hash-verified overlay for .NET 10, texture initialization/ANGLE readback and reviewed
dependencies. Unknown engine modifications prevent packaging. Build details and
patch provenance: [engine overlay](../packaging/engine/README.md).

## Test classification and practical limits

The conquest map observes normal bot queues and combat, not a forced outcome.
The network and save/load maps are controlled component scenarios stressing real
doctrine timers, ownership/target state and actor damage. They prove those paths;
they are not claims of Internet latency, every faction pairing or every save from
a months-long campaign being tested. The first human-vs-demon result and the new
inference match were independently observed; matchup balance remains tester work.

The final twelve-bot pass uses the new runtime/inference implementation. An earlier
concurrent-army-size criterion failed when Choir lost units under pressure. The
revised diagnostic tracks stable actor identities over time, records peak concurrent
size and losses, and still requires four unique combat units to have been fielded.
It does not equate casualties with failed production. The revised pass completed
49 checks with 191 attributed kills. A timed soak is kept distinct from completed
conquest/replay acceptance.

No source developer diagnostic maps are present in the public archive. CI adds
them only to a disposable copy of the candidate, retaining the exact executable
and library files. This does not modify the published archive or its checksums.

## Known alpha scope

- Land skirmishes and twelve faction selections. Campaign previews, aircraft,
  naval and beast production are excluded from the public playtest.
- Original art and animation are an early presentation pass. Music and voice
  coverage are intentionally limited; some effects/glyphs use simple vector art.
- Cliff terraces block ground movement and visually mark elevation. They do not
  confer height-based sight, range or damage bonuses.
- Balance, very large armies, additional GPUs and wide-area Internet play need
  broader tester coverage. Only local two-client synchronization is claimed.
- Windows executables are unsigned. No signing certificate is represented.

Report the exact version, map, faction, reproduction steps and relevant logs or
replay at [GitHub Issues](https://github.com/MrKrisSatan/Sevenfall/issues).
