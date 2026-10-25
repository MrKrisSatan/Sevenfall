# Standalone alpha readiness

Status: **not ready to publish a standalone executable release**.

## Implemented in the release-blocker pass

- The three preview missions now read cumulative accepted refinery income from
  a synced Sevenfall player trait. Spending, cash grants and resource assignments
  cannot inflate or hide actual deliveries. Lua regression coverage includes
  spending the entire delivery between polls and excluding resource grants.
- Explosive Veilglass is implemented; see [hazard behavior](../design/VEILGLASS_HAZARDS.md).
- All 77 cursor states now use original RGBA vector graphics and no external
  cursor palette. Native cursor visibility and hotspot acceptance remain pending.
- A native nine-faction harvesting/hazard diagnostic and runner are committed.
  It does not substitute for deployment, production, victory or network testing.
- Engine CI now includes Windows and Ubuntu 22.04 and uploads a manifest-level
  external-dependency report. Build success is separate from runtime acceptance.
- `scripts/audit_release_dependencies.py --require-independent` refuses an
  independent-manifest pass while Red Alert mounts/imports remain.

- Original terrain, trees, garrisonable houses, destructible bridges and faction engineers are implemented; see [environment behavior](../design/ENVIRONMENT.md). Native damage, repair and crossing acceptance remains NOT RUN.

## Asset replacement inventory

The [generated manifest report](release-dependencies.json) identifies **89**
external RA references after replacing the cursor manifest, four terrain imports, player layout import and title font. This counts manifest entries, not unique proprietary
files. OpenRA-authored rules/layout code and original game content must be
reviewed separately; a `ra|` reference alone does not establish ownership.

| Area | Current dependency | Required replacement or review |
|---|---|---|
| Manifest/content installation | RA content filesystem, MIX packages, ra-content | Own manifest and asset-only package mounts; no external game installation |
| Terrain | Original alpha tileset now replaces all four RA tilesets | Native renderer, transition and crossing validation; inherited world palettes still need review |
| Interface | Original neutral menus and three faction HUD skins; inherited glyph/layout definitions remain | Finish glyph/dependency review and attribution; native HUD, menu and cursor checks |
| Combat presentation | Inherited sequences, projectile/impact/death effects | Original effect sequences, remove unused inherited actors/assets |
| Audio | RA sound/voice/music definitions and archive mounts | Original audio or intentionally silent alpha definitions; no missing-file fallback |
| Rules | Shared RA actors, weapons, world/player definitions | Extract required OpenRA-authored gameplay definitions with licence notices; resolve inheritance |
| Original Sevenfall art | Source prompts and hashes exist | Complete distribution-rights/content licence inventory before packaging |

The scanner is deliberately a narrow architecture check, **not** a licence
clearance or a proof that transitive assets are complete. Do not package simply
because its reference count reaches zero.

## Runtime evidence still required

Local test content could not be located in this pass. Native diagnostics remain
NOT RUN. Once content is available, build first, then run:

```powershell
python scripts/run_defense_test.py --scenario release --support-dir PATH --dotnet .tools/dotnet/dotnet.exe
python scripts/run_defense_test.py --scenario defense --support-dir PATH --dotnet .tools/dotnet/dotnet.exe
```

PATH must contain `Content/ra/v2/conquer.mix` and the other required test content.
This is a development-only dependency; it must not ship in a standalone archive.

Then complete the [skirmish runbook](../tests/SKIRMISH_RUNBOOK.md),
[campaign runbook](../tests/FIRST_WAR_RUNBOOK.md), Veilglass flight/landing and
capture tests, multiplayer/replay checks and large-army profiling. Finally build
Windows packages with bundled runtime, notices, source availability and checksums;
verify launch and complete matches on a clean machine without Red Alert content.
Linux executable packaging/clean-machine testing remains separate from Linux CI.

## Validation recorded for this pass

- 68 Python tests passed, including campaign-spending regression, cursor atlas
  integrity and diagnostic-runner failure handling.
- Seven C# dread assertions and 104 Veilglass radius/spread assertions passed.
- Sevenfall native extension compiled without warnings or errors; engine YAML,
  sequence definitions and Fluent validation passed for twelve maps/one original tileset.
- Cursor atlas inspected visually. This is not an in-game cursor acceptance test.
- Independent-manifest gate correctly failed with the 89 remaining references.
- Native diagnostics, clean-machine launch and multiplayer were NOT RUN.
