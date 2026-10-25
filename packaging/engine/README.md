# Reviewed engine overlay

Base: OpenRA release-20250330, commit
`b4f3d8ae02b6bd6f4a3a5441e6d0daf7c5073787` (GPL-3.0-or-later).
`scripts/engine_patches.py` applies `patches.json` only to the exact expected
source, accepts an already-applied overlay, and rejects unknown modifications.
Packaging validates all patched file hashes and refuses unrelated engine edits.
The source archive supplies the base engine tar and the Sevenfall tar containing
the manifest and application script; `scripts/build.py` applies it automatically.

- Build the engine for .NET 10 LTS; remove framework-provided loader, channels
  and registry package references. Pin NuGet.CommandLine 6.12.5 to override
  BeaconLib's obsolete transitive tool dependency (GHSA-g4vj-cjjj-v7hg).
- Initialize a new Sheet's zero pixel buffer before creating its first texture.
  MapCache can release an empty sheet before any map previews arrive; subsequent
  reads previously accessed a zero-size uninitialized texture.
- Use framebuffer readback for ANGLE, as for GLES, rather than glGetTexImage.

Native terrain diagnostics exercise empty-sheet and nonempty-pixel readback.
Python tests enforce patch idempotence and rejection of unreviewed source changes.
