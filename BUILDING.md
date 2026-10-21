# Building Sevenfall 0.2 development prototype

This is a working engine integration milestone, not a finished standalone game.
The menu, graphics, sound and terrain still use locally installed Red Alert placeholders.
No proprietary content is included in this repository.

## Requirements

- Git and Python 3.10 or later.
- .NET SDK 8 (tested with 8.0.408) and .NET runtime 6.0.36. The pinned engine targets net6.0.
- Windows x64 or Linux x64 with OpenRA's SDL2/OpenAL/OpenGL prerequisites.
- Red Alert content installed through OpenRA's content manager on first launch.

The SDK and engine are cloned into ignored `.sdk/` directories and verified against
exact commits by `scripts/build.py`. Existing checkouts at another commit are rejected.

| Dependency | Version | Commit |
|---|---|---|
| OpenRAModSDK | 20250330 | 0059e22e0e3bfc862500aaaa9fe1aed4ea4e994a |
| OpenRA | release-20250330 | b4f3d8ae02b6bd6f4a3a5441e6d0daf7c5073787 |

## Windows

```powershell
py -3 scripts/build.py build
py -3 -m unittest discover -s tests
py -3 scripts/build.py launch
```

For a custom .NET installation, append `--dotnet C:\path\to\dotnet.exe`.
The current development workstation has a private SDK/runtime under `.tools/dotnet`,
which the script detects automatically. Python is available in the Codex bundled runtime.

## Linux

```sh
python3 scripts/build.py build
python3 -m unittest discover -s tests
python3 scripts/build.py launch
```

Linux commands are provided but not yet executed on Linux. The Python build command
invokes the same engine solution and `--check-yaml` utility used by SDK all/test;
the unmodified SDK itself remains available in `.sdk`. No custom C# assembly is needed.

## Play the prototype

Choose Singleplayer → Skirmish, select **Broken Choir - Proving Ground**, select a
Sevenfall faction and add **Sevenfall AI (prototype)** to the other slot. Start with
MCV-only units and 5,000 credits. Deploy the MCV, build power, a refinery, and infantry
production. The refinery provides the matching mining unit. Build a vehicle factory
to replace miners and produce armor. Both resource grades supply the same credits.

The arena is deliberately flat and symmetric for economic testing. It has equal
starting deposits, exposed expansion deposits, and a central enriched basin. It is
not yet the finished asymmetric Broken Choir battlefield.

For artwork inspection, choose **Sevenfall Building Gallery**. Its three player slots
are locked to Angels, Humans and Demons, with each faction's complete current building
roster preplaced. Naval facilities sit in the southern water strip. This is a developer
gallery without an economy, not a normal skirmish map. See [building coverage](art/BUILDINGS.md).

Launch defaults to a 1280×720 window and a double-size **software cursor**. This fixes
the invisible hardware cursor observed on the development workstation. Resize or
change display mode through Settings after launch if desired.

## Validation and remaining work

Use the [nine-faction skirmish runbook](tests/SKIRMISH_RUNBOOK.md) to record\nreal economy, combat, AI and victory results. All cases begin as NOT RUN.\n\nSee [the integration report](tests/INTEGRATION_REPORT.md). Passing engine lint does
not prove harvesting, balance, victory, replay safety or AI quality. The next milestone
is measured end-to-end economy/combat testing for all three parent factions, followed
by the nine-faction matrix. Original assets, campaigns, defenses, expansion MCVs,
support powers and superweapons remain future work.

Sources: [OpenRA SDK](https://github.com/OpenRA/OpenRAModSDK),
[OpenRA stable release](https://www.openra.net/news/release-20250330/).
