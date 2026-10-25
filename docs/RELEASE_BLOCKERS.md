# Standalone tester alpha readiness

The release scope is a complete, self-contained **Windows x64 skirmish alpha for
testers**, with twelve faction choices and three skirmish maps. This is separate
from the finished campaign game's future release.

Current evidence: [tester alpha acceptance](TESTER_ALPHA_ACCEPTANCE.md).
Installation and play instructions: [tester guide](TESTER_GUIDE.md).
The [initial skirmish audit](SKIRMISH_ALPHA_AUDIT.md) is historical; its runtime,
preview, source-notice, multiplayer and save/load findings were addressed in this pass.

## Release gates

- Committed, pinned source plus hash-verified engine overlay; unknown engine edits rejected.
- Python/C# checks, engine rules/sprites/interface validation, original standalone assets.
- .NET 10.0.13 self-contained Windows runtime; no external RA content or runtime lookup.
- Native cliffs, texture readback and actual map-cache thumbnail rendering.
- Completed autonomous conquest with genuine win/loss callbacks and finalized replay playback.
- Two independent clients and dedicated server with matching simulation hashes.
- Actual save/load through normal engine paths with matching post-load world-state hashes.
- Exact runtime notices, font hashes and corresponding dependency/font sources.
- Public map allowlist, setup compilation and install/reinstall/uninstall with retained user data.
- Fresh Windows runner native checks of the exact package; final version CI, sources and checksums.

The Windows release workflow enforces the package, native, save/load and installer
checks. Publication uses the exact accepted artifacts; a compile alone cannot
approve a release. Check the release notes for its workflow run and source revision.

## Remaining alpha limitations

Balance across every pairing, wide-area Internet latency/NAT, additional GPUs and
very large armies need tester coverage. Campaign previews, aircraft/naval/beast
production and fuller audio are outside this public skirmish scope. Elevation is
visual with impassable cliff edges, without high-ground combat bonuses.

The initial five-minute twelve-bot diagnostic required four combat units to be
alive simultaneously. Choir could lose troops under pressure before meeting that
condition. The revised soak reports cumulative unique combat units fielded,
peak concurrent size and losses separately, retaining the four-unit fielding gate.
It does not promise every bot survives a real free-for-all.

The save/load harness must resume after loading: OpenRA intentionally opens the
paused options menu. The harness issues the normal unpause order; the public game
retains its normal Resume interaction. Final standalone CI must pass this path.
