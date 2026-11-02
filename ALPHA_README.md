# Sevenfall Windows skirmish tester alpha

This is an unfinished skirmish alpha for testers. Release notes and the source
acceptance report describe verified checks and remaining scope.

Run the Setup EXE for a per-user installation, or extract the entire
portable archive to a writable folder and run `Sevenfall.exe`.
OpenRA, Red Alert and a separately installed .NET runtime are not required.
Windows x64 is the initial target. Saves, settings, replays and logs are kept in
the adjacent `Support` folder. Keep the full folder together when moving it.

The build prefers native OpenGL (Modern). The engine overlay fixes empty map-preview
textures and uses framebuffer readback for ANGLE/GLES. Additional GPU/driver
combinations remain useful tester feedback.

The alpha focuses on skirmishes with five parent factions and twenty
subfactions, original buildings/units, physical Veilglass harvesting, explosive
Veilglass hazards, defenses, faction HUDs and destructible civilian environments.
Ashen Crossing, Broken Choir and The Twelvefold Scar are the skirmish maps.
The Twelvefold Scar supports up to twelve players, with impassable cliff terraces,
alternate routes, villages and repairable bridges. Elevation is visual; there is
no high-ground combat bonus. Diagnostic maps and campaign previews are excluded
from this skirmish distribution.

Aircraft and beasts are playable. Naval and fixed-wing aircraft remain unavailable.
Superweapon powers automatically charge in Defences while their building exists;
losing the building removes access and rebuilding starts a fresh charge cycle.
See the website for the Noetic Assembly and Forsaken Host doctrines. Audio is intentionally limited; inherited
speech/music is absent. Some effects and glyphs use simple original vector art.
Engineers reuse existing infantry artwork and have a plus marker. House rubble
cannot be rebuilt; engineers repair surviving houses and restore bridges through
their bankside repair posts. Bridge collapse can kill units on the crossing.

Report bugs at https://github.com/MrKrisSatan/Sevenfall/issues. Include the version,
map, faction, steps to reproduce and relevant files from `Support/Logs`. Review
logs before sharing them. Keep replay files when reporting gameplay problems.
