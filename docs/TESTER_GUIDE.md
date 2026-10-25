# Sevenfall skirmish alpha: tester guide

Download the setup EXE from [GitHub Releases](https://github.com/MrKrisSatan/Sevenfall/releases).
Install for your Windows account, then launch Sevenfall. Alternatively extract the
entire portable ZIP to a writable folder and run `Sevenfall.exe`. OpenRA, Red Alert
and a separate .NET installation are not required. Keep the portable folder intact.

Choose **Singleplayer → Skirmish**. Use **Change Map** to select Ashen Crossing,
Broken Choir or **The Twelvefold Scar** (up to twelve players). Pick your faction
and add Sevenfall AI opponents to open slots. Start the game, select your MCV and
press **F** to deploy. Build power, a Veilworks refinery, barracks and vehicle
production. Harvesters gather physical Veilglass and deliver it to the refinery.

Three parent factions each offer four choices. See the
[twelve faction mechanics, exclusive units and superweapons](FACTION_IDENTITIES.md),
[subfaction controls and counterplay](SUBFACTIONS.md) and [defenses](DEFENSES.md).
Area Fifty Two changes its SERAPH/ABYSS protocol by deploying a powered Containment
Pylon. Flesh-wall influence, powered light barriers and hazardous Veilglass can
change a fight; use engineers to repair surviving houses and bridge posts.

For multiplayer, one player creates a game under **Multiplayer** and others join
that host. All players need the same release. Local two-client synchronization has
been tested; Internet/NAT and latency coverage remains alpha feedback. A standalone
`OpenRA.Server.exe` is also bundled for dedicated hosting. By default do not advertise
private test servers; configure authentication/network access for your own group.

Use the in-game menu to save/load a singleplayer game. Settings, saves, replays and
logs are in the installed game's `Support` folder. Installer tests preserve this
folder through reinstall and uninstall. Keep a backup before moving a portable
installation or changing versions. Save and replay compatibility across different
alpha versions is not promised.

Please test economy, AI attacks, victory/defeat, performance, faction counterplay,
damage/animation visibility, maps, bridges and cliff routing. Include the version,
map, faction and reproduction steps in [an issue](https://github.com/MrKrisSatan/Sevenfall/issues).
Attach a replay or relevant `Support/Logs` files when possible; inspect logs before
sharing them. [Acceptance evidence and known scope](TESTER_ALPHA_ACCEPTANCE.md)
describe what has already been checked.
