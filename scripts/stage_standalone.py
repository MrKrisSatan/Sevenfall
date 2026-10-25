"""Stage GPL OpenRA definitions with original Sevenfall assets, without game archives.

Only textual OpenRA source is adapted. No upstream game sprites, palettes or audio
are copied. The retained compatibility actors are hidden from player production.
"""
from pathlib import Path
import re
import shutil
import wave


def blocks(text, depth=0):
    result = []
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith('#'):
            continue
        level = len(line)-len(line.lstrip('\t'))
        if level == depth:
            key, _, value = line.strip().partition(':')
            result.append([key, value.strip(), []])
        elif level > depth and result:
            result[-1][2].append(line)
    return result


def quiet(text):
    # Explicit silent-alpha policy for direct legacy sound references.
    return re.sub(r'[\w|/.-]+\.(?:aud|v0[0-9]|r0[0-9])\b',
                  'sevenfall|audio/silence.wav', text, flags=re.I)


def stage(sdk, target):
    ra = sdk / 'engine/mods/ra'
    source = target / 'upstream'
    source.mkdir(exist_ok=True)
    for directory in ('rules', 'weapons', 'chrome', 'fluent', 'scripts'):
        for file in (ra/directory).rglob('*'):
            if file.is_file() and file.suffix in ('.yaml', '.ftl', '.lua'):
                out = source/directory/file.relative_to(ra/directory)
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_text(quiet(file.read_text(encoding='utf-8-sig')), encoding='utf-8')
    for name in ('chrome.yaml', 'metrics.yaml', 'hotkeys.yaml'):
        shutil.copy2(ra/name, source/name)
    for name in ('COPYING', 'AUTHORS'):
        shutil.copy2(sdk/'engine'/name, source/name)
    (source/'README.txt').write_text(
        'Adapted OpenRA GPL-3.0-or-later text definitions from commit '
        'b4f3d8ae02b6bd6f4a3a5441e6d0daf7c5073787.\n'
        'Copyright the OpenRA Developers and Contributors. See COPYING and AUTHORS.\n'
        'No Red Alert archive, sprite, palette, font or audio file is included.\n'
        'Legacy actor names remain as hidden inheritance compatibility definitions.\n', encoding='utf-8')

    # Replace file palettes while retaining generated remap/effect palettes.
    palettes = []
    for key, value, children in blocks((ra/'rules/palettes.yaml').read_text()):
        palettes.append(key+':')
        for trait, value, lines in blocks('\n'.join(children), 1):
            if trait.startswith('PaletteFromFile'):
                lines = [line for line in lines if line.strip().startswith(('Name:', 'Tileset:', 'AllowModifiers:'))]
                trait = trait.replace('PaletteFromFile', 'PaletteFromGrayscale')
            palettes.append('\t'+trait+':'+(' '+value if value else ''))
            palettes.extend(lines)
    (source/'rules/palettes.yaml').write_text('\n'.join(palettes)+'\n')

    # Retain notification/voice keys so trait validation remains useful; no missing-file fallback.
    audio = target/'audio'
    audio.mkdir(exist_ok=True)
    with wave.open(str(audio/'silence.wav'), 'wb') as wav:
        wav.setparams((1, 2, 22050, 0, 'NONE', 'not compressed'))
        wav.writeframes(bytes(2205*2))
    for filename, childkey in [('voices.yaml', 'Voices'), ('notifications.yaml', 'Notifications')]:
        output = []
        for name, _, children in blocks((ra/'audio'/filename).read_text()):
            output += [name+':', '\t'+childkey+':']
            for key, _, lines in blocks('\n'.join(children), 1):
                if key == childkey:
                    output += ['\t\t'+entry+':' for entry, _, _ in blocks('\n'.join(lines), 2)]
        (audio/filename).write_text('\n'.join(output)+'\n')
    (audio/'music.yaml').write_text('# Music intentionally omitted in the skirmish alpha.\n')

    # Explicit compatibility sequences, not attempts to redistribute missing legacy art.
    sequences = []
    for file in sorted((ra/'sequences').glob('*.yaml')):
        for actor, _, lines in blocks(file.read_text()):
            if actor.startswith('^'):
                continue
            sequences.append(actor+':')
            for name, _, _ in blocks('\n'.join(lines), 1):
                if name.startswith(('Defaults', 'Inherits', '-')):
                    continue
                asset, length = 'blank', 1
                if actor == 'explosion': asset, length = 'blast', 8
                elif actor.startswith(('burn', 'smoke', 'scorch_flames')): asset, length = 'smoke', 8
                elif actor in ('120mm', '50cal', 'dragon', 'missile', 'bomblet', 'bullet', 'torpedo', 'fb1'): asset = 'projectile'
                elif actor in ('moveflsh', 'select', 'allyrepair', 'poweroff', 'powerdown', 'pips', 'rank', 'beacon'): asset = 'indicator'
                elif actor == 'clock': asset, length = 'clock', 32
                elif actor == 'shroud': asset, length = 'shroud', 16
                sequences += ['\t'+name+':', f'\t\tFilename: sevenfall|art/effects/{asset}.png', f'\t\tLength: {length}']
    (target/'sequences/compatibility.yaml').write_text('\n'.join(sequences)+'\n')
    with (target/'sequences/compatibility.yaml').open('a') as output:
        output.write('shroud:\n\tfog:\n\t\tFilename: sevenfall|art/effects/fog.png\n\t\tLength: 16\n')
    chrome = (source/'chrome.yaml').read_text()
    chrome = chrome.replace('Image: sidebar.png', 'Image: sevenfall|art/ui/hud-neutral.png\n\tImage2x: sevenfall|art/ui/hud-neutral-2x.png\n\tImage3x: sevenfall|art/ui/hud-neutral-3x.png')
    for scale in (1, 2, 3):
        suffix = '' if scale == 1 else f'-{scale}x'
        chrome = chrome.replace(f': glyphs{suffix}.png', f': sevenfall|art/ui/alpha-glyphs{suffix}.png')
    (source/'chrome.yaml').write_text(chrome)

    menu = (sdk/'engine/mods/common/chrome/mainmenu.yaml').read_text(encoding='utf-8-sig')
    menu = re.sub(r'(?ms)^\t\tContainer@PLAYER_PROFILE_CONTAINER:.*\Z', '', menu)
    menu = menu.replace('Logic: MainMenuLogic', 'Logic: SevenfallMainMenuLogic')
    menu = menu.replace('@NEWS_BG:', '@SF_CHANGELOG_BG:').replace('@NEWS_BUTTON:', '@SF_CHANGELOG_BUTTON:')
    (source/'chrome').mkdir(exist_ok=True)
    (source/'chrome/mainmenu.yaml').write_text(menu, encoding='utf-8')
    shutil.copy2(Path(__file__).resolve().parents[1]/'CHANGELOG.md', target/'CHANGELOG.md')

    # Modify the assembled manifest, keeping only our package and OpenRA common files.
    manifest = (target/'mod.yaml').read_text()
    manifest = re.sub(r'(?ms)^FileSystem:.*?(?=^MapFolders:)',
        'FileSystem: DefaultFileSystem\n\tPackages:\n\t\t^EngineDir\n'
        '\t\t$sevenfall: sevenfall\n\t\t^EngineDir|mods/common: common\n'
        '\t\tcommon|scripts\n\t\tsevenfall|upstream/scripts\n\n', manifest)
    manifest = re.sub(r'(?m)^\tra\|sequences/[^\n]+\n', '', manifest)
    manifest = manifest.replace('Sequences:\n', 'Sequences:\n\tsevenfall|sequences/compatibility.yaml\n')
    for section, filename in [('Voices', 'voices'), ('Notifications', 'notifications'), ('Music', 'music')]:
        manifest = manifest.replace(f'ra|audio/{filename}.yaml', f'sevenfall|audio/{filename}.yaml')
    manifest = manifest.replace('common|chrome/mainmenu.yaml', 'sevenfall|upstream/chrome/mainmenu.yaml')
    manifest = manifest.replace('ra|', 'sevenfall|upstream/')
    manifest = manifest.replace('Website: https://www.openra.net', 'Website: https://github.com/MrKrisSatan/Sevenfall')
    manifest = re.sub(r'(?m)^\tWebIcon32:.*\n', '', manifest)
    manifest = re.sub(r'(?ms)^DiscordService:.*\Z', '', manifest)
    manifest = manifest.replace('Rules:\n', 'Rules:\n')
    # Place final overrides after other actor definitions.
    manifest = manifest.replace('\tsevenfall|rules/51-engineers.yaml', '\tsevenfall|rules/51-engineers.yaml\n\tsevenfall|rules/90-alpha.yaml')
    manifest = manifest.replace('LoadScreen: LogoStripeLoadScreen', 'LoadScreen: SFAcceptanceLoadScreen')
    (target/'mod.yaml').write_text(manifest)
    # Direct sounds can be inherited by original Sevenfall actors too.
    for directory in ('rules', 'weapons'):
        for file in (target/directory).glob('*.yaml'):
            file.write_text(quiet(file.read_text(encoding='utf-8')), encoding='utf-8')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('sdk', type=Path)
    args = parser.parse_args()
    stage(args.sdk, args.sdk/'mods/sevenfall')
