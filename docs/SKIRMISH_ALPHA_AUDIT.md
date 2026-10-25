# Skirmish alpha audit — 25 October 2026

Reviewed upstream `360d23f7326d546309b3ca249ad79042b1243ee3`, including the seven
commits since `681cf3b`: faction doctrines, Veilglass hazards/accounting,
destructible environments and engineers, themed HUDs, independent content staging,
Windows packaging, and the Sevenfall changelog menu. This review covers source,
rules, tests, build/staging, packaging and recorded acceptance evidence. It does
not certify every art frame or every gameplay combination.

**Assessment: close to a useful skirmish candidate, but not release-ready.**
The Red Alert content dependency has been removed from staging. A successful
component diagnostic is not a completed skirmish or a clean-machine install.
No public GitHub Release existed when inspected.

## Findings, in release priority order

1. **P1 — Full-match acceptance is still missing.** The nine-faction production
   evidence records 99 checks; the hazard/economy evidence records 24. Neither
   validates a player completing a normal skirmish. `maps/match-test/match-test.lua`
   observes two bots, accepted income and elimination; it currently checks
   `HasNoRequiredUnits`, not recorded `OnPlayerWon`/`OnPlayerLost` callbacks or a
   finalized replay. Complete human-vs-bot win/loss cases for all three parent
   factions, then the nine-choice matrix. Require an unassisted bot match and
   replay playback with recorded outcomes. Do not force-kill an opponent to pass
   the autonomous-AI gate.
2. **P1 — The bundled runtime is unsupported.** The engine and extension target
   .NET 6. Microsoft ended support on 12 November 2024. Self-contained publishing
   does not upgrade that runtime or receive machine-wide runtime servicing.
   Prefer a tested engine/runtime migration before public distribution; document
   the decision and exact published runtime. Sources:
   [Microsoft lifecycle](https://dotnet.microsoft.com/en-us/platform/support/policy/dotnet-core),
   [deployment servicing](https://dotnet.microsoft.com/en-us/platform/support/policy/dotnet-core).
3. **P1 — Distribution inventory remains incomplete.** The real restored NuGet
   inventory contains 16 entries without copied licence texts, including native
   wrappers and build-time analyzers. This is not proof that all 16 ship: reconcile
   the final published dependency set, supply its exact notices and required
   source, and finish GNU FreeFont attribution/source verification. The manifest
   dependency scanner explicitly does not provide rights clearance.
4. **P1 — Candidate packaging is not release automation.** `engine.yml` builds
   Windows/Linux source and uploads the dependency report; it does not publish
   or smoke-test a Windows candidate, create an installer, attach source/checksums,
   or create a GitHub prerelease. Add a versioned candidate-artifact workflow first,
   then a release job gated on the actual candidate's acceptance evidence.
5. **P2 — Public content needs a skirmish profile.** Packaging copies all staged
   maps, including developer diagnostics, galleries and unaccepted campaign previews.
   Publish only Broken Choir and Ashen Crossing initially, with their required
   support files; remove mission menu entries for omitted previews. Validate the
   final map list and first-run menu from the extracted archive.
6. **P2 — Multiplayer, persistence and machine coverage remain open.** Exercise
   two-client synchronization, reconnect/disconnect behavior, save/load, replay
   completion, settings retention, writable-folder handling and an independent
   Windows machine/VM. Stress defenses and Veilglass with representative armies;
   the custom field/hazard scans have not established a large-match performance limit.
7. **P2 — Documentation mixes historical milestones.** The roadmap's initial
   status date is 21 October and its first-skirmish checklist remains unaccepted;
   historical audit/build reports also describe obsolete RA dependencies. Keep
   those reports dated, link this audit and `RELEASE_BLOCKERS.md` as current, and
   update only acceptance cells supported by direct evidence.

## Fixes made during this review

- `package_windows.py` now requires committed source and the expected clean
  engine/SDK revisions, allowing only the SDK's generated overlay/configuration.
  It rebuilds/restages before copying the custom DLL and records all three source
  revisions in `BUILD_INFO.json`. Previously it could package stale staged data
  and an old extension under a new version label.
- The packager now finds `dotnet` on PATH when the private `.tools` runtime is absent.
- `collect_package_notices.py` follows exact resolved runtime download versions
  across all restored package caches, rather than assuming 6.0.36 and retaining
  only the last project's cache roots. A real restore on this workstation selected
  **6.0.22**; its LICENSE and THIRD-PARTY-NOTICES are now collected. A missing
  resolved runtime fails explicitly. Regression fixtures cover the patch/cache case,
  missing runtime and modified source rejection.

## Fresh verification

- 74 Python tests pass (71 upstream plus three packaging regressions).
- C# assertions pass: seven dread checks and 104 Veilglass boundary/budget checks.
- Pinned engine/custom extension build succeeds; YAML/Fluent validation passes
  for the current maps, with existing unused-upstream-text warnings.
- All 208 merged chrome collections pass bounds checks at 1x/2x/3x.
- Missing-sprite check passes for the standalone TEMPERAT tileset.
- Manifest audit passes with zero external RA references.
- Native environment diagnostic with a newly created, content-free support folder:
  **11 checks pass**, including house claiming/repair/garrison/ejection and bridge
  damage/destruction/repair/traversal.

- Native nine-faction harvesting/hazard diagnostic with a fresh content-free support
  folder: **24 checks pass**, including actual refinery income while balances are
  spent and finite resource scatter. This remains a component test.

- Portable packaging completed from committed source `11516cd`; its ZIP checksum
  and **866 file hashes** verified after extraction. The extracted `Sevenfall.exe`
  passed **11 environment checks** with separate empty support data on the development
  host. This does not replace an independent clean-machine test. A second candidate
  also packaged successfully after the changelog UTF-8 correction.

Existing 33-check defense and 99-check production transcripts were inspected as
historical evidence; they are not relabelled as fresh runs from this audit.

## What the Windows download will contain

The current implementation is a **self-contained portable folder**, distributed
as a ZIP containing `Sevenfall.exe`, engine/native libraries, mod assets and a
writable `Support` directory. It requires neither an installed OpenRA nor an
installed .NET runtime. `Sevenfall.exe` alone is not the whole game, and no
single-file installer is implemented. If the release download must itself be an
`.exe`, build a Windows setup executable around this verified folder and test
install, first launch, update and uninstall. Preserve user saves/settings.

Next sequence: complete-match outcomes/replays → runtime and distribution inventory
decision → skirmish-only candidate/installer → multiplayer/save-load and clean-PC
acceptance → source/checksum bundle → GitHub prerelease. Campaign expansion,
air/naval/beast rosters and further art expansion do not block this land-skirmish scope.
