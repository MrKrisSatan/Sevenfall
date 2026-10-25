"""Build an isolated Windows x64 portable candidate. Does not publish a release."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import zipfile
from audit_release_dependencies import inspect
from collect_package_notices import collect

ROOT = Path(__file__).resolve().parents[1]


def run(*args):
    subprocess.run([str(a) for a in args], cwd=ROOT, check=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--version', default='0.3.0-alpha.1')
    parser.add_argument('--dotnet', default=str(ROOT/'.tools/dotnet/dotnet.exe'))
    args = parser.parse_args()
    engine = ROOT/'.sdk/engine'
    mod = ROOT/'.sdk/mods/sevenfall'
    if not inspect(mod/'mod.yaml')['independent_manifest']:
        raise SystemExit('External RA references remain; packaging refused.')
    dest = ROOT/'dist'/f'Sevenfall-{args.version}-windows-x64'
    if dest.exists():
        raise SystemExit(f'Candidate already exists: {dest}. Use a new version suffix to preserve evidence.')
    dest.mkdir(parents=True)
    for project in ('OpenRA.Launcher', 'OpenRA.Mods.Common', 'OpenRA.Mods.Cnc', 'OpenRA.Platforms.Default', 'OpenRA.Utility'):
        run(args.dotnet, 'publish', engine/project/(project+'.csproj'), '-c', 'Release', '-r', 'win-x64',
            '--self-contained', 'true', '-p:TargetPlatform=win-x64', '-p:PublishDir='+str(dest))
    run(args.dotnet, 'publish', engine/'OpenRA.WindowsLauncher/OpenRA.WindowsLauncher.csproj', '-c', 'Release',
        '-r', 'win-x64', '--self-contained', 'true', '-p:TargetPlatform=win-x64', '-p:LauncherName=Sevenfall',
        '-p:ModID=sevenfall', '-p:DisplayName=Sevenfall', '-p:FaqUrl=https://github.com/MrKrisSatan/Sevenfall/issues',
        '-p:InformationalVersion='+args.version, '-p:PublishDir='+str(dest))
    shutil.copy2(engine/'bin/OpenRA.Mods.Sevenfall.dll', dest)
    for name in ('glsl', 'mods/common'):
        shutil.copytree(engine/name, dest/name)
    shutil.copytree(mod, dest/'mods/sevenfall')
    for name in ('COPYING', 'AUTHORS'):
        shutil.copy2(engine/name, dest/name)
    (dest/'VERSION').write_text('release-20250330\n')
    manifest = dest/'mods/sevenfall/mod.yaml'
    manifest.write_text(manifest.read_text().replace('Version: 0.3-dev', 'Version: '+args.version))
    # Portable settings are scoped to this directory, leaving existing installations alone.
    support = dest/'Support'
    support.mkdir()
    (support/'settings.yaml').write_text('Graphics:\n\tMode: Windowed\n\tWindowedSize: 1600,900\n'
        '\tDisableHardwareCursors: True\n\tCursorDouble: True\nDebug:\n\tSendSystemInformation: False\n')
    for file in ('THIRD_PARTY_NOTICES.md', 'ALPHA_README.md'):
        shutil.copy2(ROOT/file, dest/file)
    collect(engine, dest/'Notices')
    # No external proprietary formats are allowed to sneak into the candidate.
    forbidden = {'.mix', '.aud', '.vqa', '.shp', '.pal', '.vxl', '.hva'}
    violations = [str(p.relative_to(dest)) for p in dest.rglob('*') if p.suffix.lower() in forbidden]
    if violations:
        raise SystemExit('Forbidden content in package: '+str(violations))
    inventory = {str(p.relative_to(dest)).replace('\\', '/'): hashlib.sha256(p.read_bytes()).hexdigest()
                 for p in sorted(dest.rglob('*')) if p.is_file()}
    (dest/'FILES.sha256.json').write_text(json.dumps(inventory, indent=2)+'\n')
    archive = dest.parent / (dest.name + '.zip')
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for p in sorted(dest.rglob('*')):
            if p.is_file():
                z.write(p, Path(dest.name)/p.relative_to(dest))
    archive.with_suffix('.zip.sha256').write_text(hashlib.sha256(archive.read_bytes()).hexdigest()+'  '+archive.name+'\n')
    print('Candidate (NOT release-approved):', archive)


if __name__ == '__main__':
    main()

