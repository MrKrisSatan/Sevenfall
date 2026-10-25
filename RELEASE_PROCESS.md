# Windows skirmish tester release process

The public release is a self-contained Windows x64 skirmish alpha. Planned campaign
content is not represented as finished. See [acceptance evidence](docs/TESTER_ALPHA_ACCEPTANCE.md).

1. Commit source and the reviewed dependency/engine manifests. Run Python/C# checks
   and engine validation; preserve completed-conquest/replay and twelve-bot evidence.
2. Dispatch `windows-candidate.yml` with an exact alpha version, for example
   `0.3.0-alpha.1`. Leaving it empty produces a numbered development candidate.
3. Require its exact-package rules/sprite/interface gates, fresh Windows native
   terrain, standalone two-client sync, standalone save/load and installer lifecycle
   checks to pass. It bundles project/engine/SDK and dependency/font sources.
4. Download accepted artifacts. Verify the GitHub artifact digest, all per-file
   SHA-256 checksums, source revision, skirmish map profile and notice audit.
5. Prepare a GitHub Release tagged `vVERSION` at the tested source revision. Attach
   setup EXE, portable ZIP, both source archives and checksums. Mark the tester alpha
   as a prerelease and document its known scope, controls and reporting instructions.
6. Publish only after all assets are uploaded and checksums verified. Confirm the
   unauthenticated public release API/downloads and the project's release page.

No forced victory is used to satisfy autonomous match acceptance. Controlled network
and save maps are classified separately. The public archive omits every diagnostic
map; CI overlays diagnostics only in a disposable copy of the same binaries.

Source builds need .NET SDK 10.0.402; the distributed game does not. The reviewed
engine overlay, runtime notices, source manifests and LGPL replacement instructions
are part of the source/package. Preserve them when redistributing.
