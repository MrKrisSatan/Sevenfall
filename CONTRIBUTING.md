# Contributing to Sevenfall

Sevenfall is in early pre-alpha. Please open an issue before large architectural changes.

## Workflow
1. Read the [design bible](design/GAME_DESIGN.md) and [roadmap](ROADMAP.md).
2. Select or open an issue describing the change.
3. Make changes on a feature branch with a concise, focused commit.
4. Verify MiniYaml and engine compatibility with the same OpenRA SDK version.
5. Describe testing performed, screenshots/logs and any known limitations in the pull request.
6. Never claim a build is playable without verifying its install/launch, resource economy, combat and victory states.

## Assets and copyright
Do not commit Red Alert's proprietary graphics, audio, music, maps or other copyrighted content. During prototyping use assets provided by an appropriately licensed local OpenRA game installation. Do not introduce third-party assets without recording their authorship and licence. A final licence for original Sevenfall assets is not yet chosen.

## Releases
Releases must link to source commit, list the tested engine version, include installation steps, a changelog and any known blockers. See [release checklist](RELEASE_PROCESS.md).