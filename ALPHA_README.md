# Sevenfall Windows skirmish alpha candidate

This is an unfinished playtest build. Publication requires the recorded release
checks to pass; merely producing this directory does not approve it for release.

Run the candidate Setup EXE for a per-user installation, or extract the entire
portable archive to a writable folder and run `Sevenfall.exe`.
OpenRA, Red Alert and a separately installed .NET runtime are not required.
Windows x64 is the initial target. Saves, settings, replays and logs are kept in
the adjacent `Support` folder. Keep the full folder together when moving it.

The build prefers native OpenGL (Modern). The engine overlay fixes empty map-preview
textures and uses framebuffer readback for ANGLE/GLES. Additional GPU/driver
combinations remain useful tester feedback.

The alpha focuses on land skirmishes with three parent factions and twelve
subfactions, original buildings/units, physical Veilglass harvesting, explosive
Veilglass hazards, defenses, faction HUDs and destructible civilian environments.
Ashen Crossing, Broken Choir and The Twelvefold Scar are the skirmish maps.
The Twelvefold Scar supports up to twelve players, with impassable cliff terraces,
alternate routes, villages and repairable bridges. Elevation is visual; there is
no high-ground combat bonus. Diagnostic maps and campaign previews are excluded
from this skirmish distribution.

Air/naval/beast production is hidden. Audio is intentionally limited; inherited
speech/music is absent. Some effects and glyphs use simple original vector art.
Engineers reuse existing infantry artwork and have a plus marker. House rubble
cannot be rebuilt; engineers repair surviving houses and restore bridges through
their bankside repair posts. Bridge collapse can kill units on the crossing.

Report bugs at https://github.com/MrKrisSatan/Sevenfall/issues. Include the version,
map, faction, steps to reproduce and relevant files from `Support/Logs`. Review
logs before sharing them. Keep replay files when reporting gameplay problems.
