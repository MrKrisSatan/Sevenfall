# Standalone alpha readiness

Status: **Windows candidate builds and launches without Red Alert content; not yet approved for publication.**

The [latest skirmish-alpha audit](SKIRMISH_ALPHA_AUDIT.md) reviews commit
`360d23f`, distinguishes the portable executable from an installer, and records
the next acceptance and release-engineering steps.

## Scope of the first alpha

Nine faction selections, original ground-unit/building artwork, faction combat doctrines,
land skirmishes, explosive Veilglass, garrisonable houses, repairable/destructible bridges,
neutral menus and faction HUDs. Aircraft, naval and beast production facilities are
hidden until their playable rosters exist. Campaign previews remain development content.
Legacy voices/music are deliberately silent; combat compatibility effects are simple
original vector sprites. This is an early playable-art pass, not final presentation.

## Completed standalone work

- `stage_standalone.py` adapts only textual GPL OpenRA definitions and retains attribution.
  Original Sevenfall assets replace file palettes, legacy sequences, cursors, glyphs and terrain.
- The manifest audit reports **0 external Red Alert references**. Engine CI now requires this.
- Native missing-sprite validation passes. The manifest scanner alone does not prove this.
- The Windows packaging script bundles the runtime, portable settings, file hashes and ZIP checksum.
  It refuses proprietary game archive formats and preserves existing candidates.
- Source-bundle and dependency-notice inventory scripts are available. Inventory entries with
  missing licence texts still require resolution before public distribution.
- Native tests fixed bridge-post targeting, invalid engineer inheritance used by map previews,
  and a Veilglass scatter accounting bug (empty cells had received one extra resource unit).

## Verified evidence (25 October 2026)

| Check | Result |
|---|---|
| Python regression suite | 71 passed |
| Native environment diagnostic, empty support folder | 11 passed |
| Native harvesting/hazard diagnostic, all nine factions | 24 passed |
| Native defenses and conversion/counters | 33 passed |
| Self-contained Windows executable, environment diagnostic | 11 passed |
| Manifest external-reference gate | PASS, 0 |
| Original chrome bounds at 1x/2x/3x | 208 collections passed |
| Engine YAML, sequences and Fluent | Passed; unused upstream text warnings remain |
| MCV and paid production diagnostic | 99 passed across all nine factions |
| Unassisted AI conquest match | In progress; economy and armies observed, no completed-match pass yet |
| Replay acceptance | Not passed; terminated diagnostic recordings are not completed-match evidence |
| Two-client multiplayer, save/load, independent clean machine | NOT RUN |

The portable executable has been tested on the development Windows host with isolated
support data. This is not an independent clean-PC or clean-VM installation test.

## Remaining publication gates

1. Complete conquest win/loss acceptance for all parent factions.
2. Complete an unassisted AI match, inspect combat/economy behavior and verify a finalized replay.
3. Exercise two-client synchronization and save/load; record any limitations explicitly.
4. Complete exact third-party licence texts/corresponding-source inventory, including fonts
   and native libraries. Package the committed Sevenfall and pinned engine/SDK sources.
5. Remove or clearly separate diagnostic maps and unaccepted campaign previews from the
   public skirmish build; test the final archive, launch path, settings and first-run menu.
6. Test the final archive on a clean Windows machine/VM, run CI at the published commit,
   then tag and publish binaries, source and checksums together.
7. Resolve the runtime support decision: the pinned engine targets .NET 6, whose
   support ended on 12 November 2024. Prefer a tested engine/runtime upgrade before
   public distribution; a self-contained package carries its own runtime.
   See [Microsoft's lifecycle policy](https://dotnet.microsoft.com/en-us/platform/support/policy/dotnet-core).

## Reproduce native checks

Build with `python scripts/build.py build`, then use a fresh support directory:

```powershell
python scripts/run_defense_test.py --scenario environment --support-dir artifacts/native-environment --dotnet .tools/dotnet/dotnet.exe
python scripts/run_defense_test.py --scenario release --support-dir artifacts/native-release --dotnet .tools/dotnet/dotnet.exe --timeout 260
python scripts/run_defense_test.py --scenario defense --support-dir artifacts/native-defense --dotnet .tools/dotnet/dotnet.exe
python scripts/run_defense_test.py --scenario production --support-dir artifacts/native-production --dotnet .tools/dotnet/dotnet.exe --timeout 600
python scripts/run_defense_test.py --scenario match --support-dir artifacts/native-match --dotnet .tools/dotnet/dotnet.exe --timeout 1400
```

For an extracted candidate use `--package PATH` instead of `--dotnet PATH`.
No `conquer.mix` or other external game content is needed. Reports distinguish
scripted component checks from complete matches; neither is silently substituted for the other.

