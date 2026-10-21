#!/usr/bin/env python3
"""Install the Sevenfall OpenRA prototype as a Red Alert overlay.

Usage: python scripts/install_into_sdk.py PATH_TO_OPENRA_MOD_SDK
No network access needed; run SDK `make` first to fetch its engine.
"""
from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
MOD_SOURCE = PROJECT / 'mods' / 'sevenfall'


def scan_buildables(rule_dir: Path) -> list[str]:
    """Find built-in actors declaring Buildable without relying on a YAML library.

    OpenRA uses MiniYaml (tabs for indentation), not ordinary YAML.
    """
    found: set[str] = set()
    for path in sorted(rule_dir.glob('*.yaml')):
        actor = None
        for line in path.read_text(encoding='utf-8-sig').splitlines():
            if not line.strip() or line.lstrip().startswith('#'):
                continue
            if not line.startswith((' ', '\t')) and line.endswith(':'):
                actor = line[:-1]
            elif actor and line.startswith('\tBuildable:') and not actor.startswith('^'):
                found.add(actor)
    return sorted(found)


def append_manifest_section(source: str, section: str, line: str) -> str:
    pattern = rf'(?m)^({re.escape(section)}:\n)((?:(?:\t|\s*#)[^\n]*\n|\n)*)'
    matches = list(re.finditer(pattern, source))
    if len(matches) != 1:
        raise RuntimeError(f'Could not identify exactly one manifest section {section}')
    match = matches[0]
    block = match.group(0)
    if line in block:
        return source
    return source[:match.start()] + block.rstrip('\n') + f'\n\t{line}\n\n' + source[match.end():]


# These missions deliberately reuse the existing Proving Ground terrain while
# mission-specific maps, scripted objectives and encounter design are validated.
# Map binaries are generated in the installed SDK, never guessed or distributed
# as independently completed campaign maps.
CAMPAIGN_PROTOTYPES = (
    'h03-glass-fields', 'a03-glass-wrath', 'd02-seeds-ruin',
)


def stage_original_unit_turnarounds(target: Path) -> int:
    """Stage authored direction-specific sprites for future animation bindings.

    The source pack contains eight distinct facings per unit, not movement,
    firing, or death cycles. These sprites are NOT yet active combat sprites.
    """
    source = PROJECT / 'art' / 'unit-turnarounds' / 'sheets'
    sprites = sorted(source.glob('*.png'))
    if len(sprites) != 39:
        raise RuntimeError(f'Expected 39 original directional sprite sheets, found {len(sprites)}')
    destination = target / 'art' / 'unit-turnarounds'
    destination.mkdir(parents=True, exist_ok=True)
    for sprite in sprites:
        shutil.copy2(sprite, destination / sprite.name)
    return len(sprites)


def install_campaign_map_binaries(target: Path) -> None:
    """Install the three source-only mission maps onto the prototype terrain."""
    terrain = MOD_SOURCE / 'maps' / 'broken-choir' / 'map.bin'
    if not terrain.is_file():
        raise RuntimeError('Broken Choir prototype terrain is missing.')
    for mission in CAMPAIGN_PROTOTYPES:
        folder = target / 'maps' / mission
        for file in ('map.yaml', 'mission.lua'):
            if not (folder / file).is_file():
                raise RuntimeError(f'Missing campaign source: {mission}/{file}')
        shutil.copy2(terrain, folder / 'map.bin')


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('sdk', type=Path, help='OpenRAModSDK checkout root')
    parser.add_argument('--no-config', action='store_true', help='Do not modify SDK mod.config')
    args = parser.parse_args()
    sdk = args.sdk.expanduser().resolve()
    ra_mod = sdk / 'engine' / 'mods' / 'ra'
    ra_manifest = ra_mod / 'mod.yaml'
    if not ra_manifest.is_file():
        parser.error('SDK engine/mods/ra/mod.yaml is missing. Run SDK make.cmd/make first.')
    target = sdk / 'mods' / 'sevenfall'
    target.mkdir(parents=True, exist_ok=True)
    for item in MOD_SOURCE.rglob('*'):
        if item.is_file():
            dest = target / item.relative_to(MOD_SOURCE)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, dest)

    install_campaign_map_binaries(target)
    staged_unit_count = stage_original_unit_turnarounds(target)

    # All SDK-provided RA content stays mounted as ra|. Only our additions use sevenfall|.
    content = ra_manifest.read_text(encoding='utf-8-sig')
    content = content.replace('\t\t$ra: ra', '\t\t$ra: ra\n\t\t$sevenfall: sevenfall', 1)
    if '$sevenfall: sevenfall' not in content:
        raise RuntimeError('Could not add sevenfall package mount; manifest version unsupported.')
    content = re.sub(r'(?m)^\tTitle: .*$', '\tTitle: sf-title', content, count=1)
    content = re.sub(r'(?m)^\tWindowTitle: .*$', '\tWindowTitle: sf-title', content, count=1)
    content = content.replace('ra|rules/ai.yaml', 'sevenfall|rules/40-ai.yaml')
    content = content.replace('ra|maps: System', 'sevenfall|maps: System')
    content = content.replace('maps/ra/{DEV_VERSION}', 'maps/sevenfall/0.2')
    content = content.replace('Version: {DEV_VERSION}', 'Version: 0.3-dev')
    content = content.replace('SupportsMapsFrom: ra', 'SupportsMapsFrom: sevenfall')
    content = content.replace('SpriteFormats: ShpD2,', 'SpriteFormats: PngSheet, ShpD2,')
    content = content.replace('ra|uibits/loadscreen', 'sevenfall|art/loadscreen')
    content = content.replace('Missions:\n\tra|missions.yaml', 'Missions:')
    content = content.replace('AllowUnusedFluentMessagesInExternalPackages: false',
                              'AllowUnusedFluentMessagesInExternalPackages: true')
    for section, file in [
        ('Missions', 'missions.yaml'),
        ('Rules', 'rules/00-hide-red-alert.yaml'),
        ('Rules', 'rules/10-factions.yaml'),
        ('Rules', 'rules/20-structures.yaml'),
        ('Rules', 'rules/25-support-structures.yaml'),
        ('Rules', 'rules/30-units.yaml'),
        ('Weapons', 'weapons/sevenfall.yaml'),
        ('FluentMessages', 'fluent/sevenfall.ftl'),
        ('Chrome', 'chrome.yaml'),
        ('ChromeMetrics', 'metrics.yaml'),
        ('Sequences', 'sequences/power.yaml'),
        ('Sequences', 'sequences/refineries.yaml'),
        ('Sequences', 'sequences/logistics.yaml'),
        ('Sequences', 'sequences/buildings.yaml'),
    ]:
        content = append_manifest_section(content, section, f'sevenfall|{file}')
    (target / 'mod.yaml').write_text(content, encoding='utf-8')

    original = scan_buildables(ra_mod / 'rules')
    if len(original) < 30:
        raise RuntimeError(f'Expected dozens of Red Alert buildables; found {len(original)}.')
    hide = '# Generated from the exact OpenRA engine files in this SDK.\n'
    hide += '# This keeps the original economy/engine available while removing legacy build menus.\n'
    hide += ''.join(f'{actor}:\n\tBuildable:\n\t\tPrerequisites: ~disabled\n' for actor in original)
    (target / 'rules' / '00-hide-red-alert.yaml').write_text(hide, encoding='utf-8')

    if not args.no_config:
        cfg_path = sdk / 'mod.config'
        if not cfg_path.is_file():
            raise RuntimeError(f'mod.config not found: {cfg_path}')
        cfg = cfg_path.read_text(encoding='utf-8')
        cfg, matches = re.subn(r'(?m)^(MOD_ID=)[^\n]*$', r'\1"sevenfall"', cfg, count=1)
        if matches != 1:
            raise RuntimeError('Cannot update MOD_ID in SDK mod.config')
        # Default SDK already includes RA content in the engine folder. Packaging
        # settings are intentionally not modified or claimed to be release ready.
        cfg_path.write_text(cfg, encoding='utf-8')

    print(f'Sevenfall overlay installed: {target}')
    print(f'Generated vanilla actor exclusions: {len(original)}')
    print(f'Original eight-facing unit turnarounds staged (not yet animated): {staged_unit_count}')
    print('Next: SDK make.cmd [all] and make.cmd [test] (Windows), or make && make test (Linux).')
    print('NOTE: 0.3 candidate: three source-backed campaign previews installed; live victory/combat remain unverified.')


if __name__ == '__main__':
    main()
