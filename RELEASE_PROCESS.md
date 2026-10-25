# Release checklist

**There is currently no playable release.** The v0.1 starter is a code seed, not an executable build.

Current evidence and the asset replacement inventory are tracked in
[Standalone alpha readiness](docs/RELEASE_BLOCKERS.md). After staging, run
`python scripts/audit_release_dependencies.py --require-independent` before
attempting standalone packaging. Passing this narrow check does not replace the
licence review and clean-machine/runtime acceptance below.

For every verified release:
- [ ] Use a pinned OpenRA Mod SDK revision
- [ ] Run static consistency checks
- [ ] Run SDK build / tests; attach full logs
- [ ] Install and launch on a clean supported machine
- [ ] Verify factions, Veilglass gather/unload, unit production, combat and victory
- [ ] Document third-party assets and licences; no packaged proprietary placeholders
- [ ] Prepare downloadable archive, checksums, install guide and known issues
- [ ] Update README and CHANGELOG and publish a GitHub Release
- [ ] Confirm release is visible on project website

Suggested labels: `v0.1-source` (code only), `v0.2-prealpha` (first tested skirmish), `v0.3-asymmetry`, `v0.4-art`, `v0.5-campaign`.

The live website requests public GitHub Releases through GitHub's API, so a newly published release should appear there automatically. Manual page-source updates remain possible through repository commits.
