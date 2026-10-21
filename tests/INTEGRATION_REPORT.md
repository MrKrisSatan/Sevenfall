# Engine integration report — 21 October 2026

## Passed on Windows x64

- Built the pinned OpenRA solution in Release with .NET SDK 8.0.408 and runtime 6.0.36.
- OpenRA Utility `sevenfall --check-yaml`: no errors or warnings, including both maps,
  all four inherited tileset sequence definitions and Fluent references.
- Started the renderer and loaded the Sevenfall main menu; visually inspected the
  rendered window. Placeholder Red Alert menu and art are clearly still present.
- Visually inspected the skirmish lobby and faction dropdown after fixing missing flag
  regions; added per-faction sidebar theme mappings and regression coverage.
- Observed a running skirmish with a deployed construction yard, placed power building,
  active construction queue and functioning faction-themed sidebar. This is a smoke
  check, not completion of the full faction/economy acceptance matrix.
- User confirmed the cursor became visible after enabling a double-size software cursor.
- Python regression tests cover manifest insertion, buildable scanning, binary map
  layout, clear starting cells, and equal resources under 180-degree rotation.

## Implemented in this pass

Imported the missing source from the supplied starter ZIP: 12 buildings, 21 units,
six weapons, nine faction definitions and localisation. Fixed the overlay's destructive
Buildable removal (which broke inherited RA actors) using an unavailable prerequisite.
Sevenfall actors override that prerequisite with their own faction/tech requirements.
Restored infantry production type after palette exclusion overrides, added a dedicated
land AI using Sevenfall actor IDs, an original generated arena and a menu map, and
isolated Sevenfall map discovery from incompatible RA campaigns. Added pinned build,
test and windowed launch commands.

## Limitations / not yet verified

- No claim of completed 10-minute harvesting, 20-minute AI survival, nine-faction manual
  lobby/deploy matrix, combat victory, save/resume or deterministic multiplayer/replays.
- Bot modules pass engine lint but economic behavior and match completion need playtests.
- Menu launch was verified; a complete player-directed economy/combat loop was not.
- The source build reports upstream NU1901 warnings for NuGet.CommandLine 6.12.1.
  Engine sources have not been patched to mask the warnings.
- SDK `make all`/`make test` wrappers were not separately run; the project command
  builds OpenRA.sln and executes the same validation utility directly, preserving
  the engine's Fluent lint check (the SDK bootstrap normally removes that check).
- Linux, installers, campaigns, original audiovisual content and standalone packaging
  are not complete. Local test assets were fetched from the engine's official quickinstall
  mirror list and checked against its declared SHA-1; none are committed.

## Next executable milestone

Play all three parents on the proving ground: deploy → power → refinery → two full
harvest/unload cycles → infantry/vehicle production → attack → annihilation. Record
income, power, queue behavior and bot activity, fix failures, then repeat all nine
selectors and add automated simulation/replay checks before expanding the roster.
