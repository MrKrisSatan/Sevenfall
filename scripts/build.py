"""Reproducible Sevenfall developer build. Requires Git, Python 3 and .NET.

python scripts/build.py [build|test|launch] [--dotnet PATH]
The pinned engine targets .NET 6; install its 6.0.36 runtime alongside your SDK.
"""
import argparse
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SDK = ROOT / '.sdk'
SDK_COMMIT = '0059e22e0e3bfc862500aaaa9fe1aed4ea4e994a'
ENGINE_COMMIT = 'b4f3d8ae02b6bd6f4a3a5441e6d0daf7c5073787'

def run(*args, **kwargs):
    subprocess.run([str(a) for a in args], check=True, cwd=ROOT, **kwargs)

def checkout(path, repo, tag, commit):
    if not path.exists():
        run('git', 'clone', '--depth', '1', '--branch', tag, repo, path)
    actual = subprocess.check_output(['git', '-C', str(path), 'rev-parse', 'HEAD'], text=True).strip()
    if actual != commit:
        raise SystemExit(f'{path}: expected {commit}, found {actual}; refusing to replace checkout')

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['build', 'test', 'launch'], nargs='?', default='build')
    parser.add_argument('--dotnet', default=str(ROOT / '.tools/dotnet/dotnet.exe')
                        if (ROOT / '.tools/dotnet/dotnet.exe').exists() else 'dotnet')
    args = parser.parse_args()
    checkout(SDK, 'https://github.com/OpenRA/OpenRAModSDK.git', '20250330', SDK_COMMIT)
    checkout(SDK / 'engine', 'https://github.com/OpenRA/OpenRA.git', 'release-20250330', ENGINE_COMMIT)
    run(sys.executable, ROOT / 'scripts/check_project.py')
    run(sys.executable, ROOT / 'scripts/install_into_sdk.py', SDK)
    engine = SDK / 'engine'
    if args.action == 'build':
        run(args.dotnet, 'build', engine / 'OpenRA.sln', '-c', 'Release', '--nologo')
    run(args.dotnet, 'build', ROOT / 'code/OpenRA.Mods.Sevenfall/OpenRA.Mods.Sevenfall.csproj',
        '-c', 'Release', '--nologo', f'-p:OpenRAEngineDir={engine}',
        f'-p:OutputPath={engine / "bin"}')
    env = dict(os.environ, ENGINE_DIR=str(engine),
               MOD_SEARCH_PATHS=f'{SDK / "mods"},{engine / "mods"}')
    run(args.dotnet, engine / 'bin/OpenRA.Utility.dll', 'sevenfall', '--check-yaml', env=env)
    if args.action == 'launch':
        run(args.dotnet, engine / 'bin/OpenRA.dll', 'Game.Mod=sevenfall',
            f'Engine.EngineDir={engine}', f'Engine.ModSearchPaths={env["MOD_SEARCH_PATHS"]}',
            'Graphics.Mode=Windowed', 'Graphics.WindowedSize=1280,720',
            'Graphics.DisableHardwareCursors=True', 'Graphics.CursorDouble=True', env=env)

if __name__ == '__main__':
    main()
