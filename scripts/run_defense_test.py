"""Run native standalone diagnostics and fail on missing acceptance markers.

Requires an already-built SDK. Use an empty --support-dir for clean-content checks.
This launches a local game window, collects evidence, and closes only its own process.
"""
import argparse
from pathlib import Path
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]


def diagnostic_status(data, scenario):
    marker = scenario.upper() + '_TEST'
    if marker + ' FAIL:' in data or 'Fatal Lua Error:' in data:
        return 'failed'
    if marker + ' COMPLETE checks=' in data:
        return 'passed'
    return 'pending'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--support-dir', type=Path, required=True)
    parser.add_argument('--dotnet', default='dotnet')
    parser.add_argument('--engine-dir', type=Path, help='An isolated built engine directory for concurrent diagnostics')
    parser.add_argument('--package', type=Path, help='Test the self-contained executable in this extracted candidate')
    parser.add_argument('--replay', type=Path, help='Replay a recorded diagnostic instead of launching its map')
    parser.add_argument('--scenario', choices=['defense', 'release', 'environment', 'production', 'match', 'doctrine', 'subproduction'], default='defense')
    parser.add_argument('--timeout', type=int)
    args = parser.parse_args()
    support = args.support_dir.resolve()
    from audit_release_dependencies import inspect
    engine = args.package.resolve() if args.package else args.engine_dir.resolve() if args.engine_dir else ROOT / '.sdk/engine'
    mod = engine / 'mods/sevenfall' if args.package else ROOT / '.sdk/mods/sevenfall'
    if not inspect(mod / 'mod.yaml')['independent_manifest']:
        parser.error('Standalone diagnostic requires a manifest without external RA dependencies')
    support.mkdir(parents=True, exist_ok=True)
    timeout = args.timeout or (230 if args.scenario == 'release' else 110)
    marker = args.scenario.upper() + '_TEST'
    transcript = support / f'{args.scenario}-diagnostic-output.log'
    command = [args.dotnet, str(engine / 'bin/OpenRA.dll'), 'Game.Mod=sevenfall',
               f'Engine.EngineDir={engine}', f'Engine.ModSearchPaths={ROOT / ".sdk/mods"},{engine / "mods"}',
               f'Engine.SupportDir={support}', 'Graphics.Mode=Windowed', 'Graphics.WindowedSize=1600,900',
               'Graphics.DisableHardwareCursors=True', 'Graphics.CursorDouble=True',
               'Debug.SendSystemInformation=False', 'Debug.SystemInformationVersionPrompt=999',
               'Game.IntroductionPromptVersion=999', f'Launch.Map={args.scenario}-test']
    if args.package:
        command = [str(engine / 'Sevenfall.exe'), 'Game.Mod=sevenfall',
                   f'Engine.LaunchPath={engine / "Sevenfall.exe"}',
                   f'Engine.ModSearchPaths={engine / "mods"}'] + command[5:]
    if args.replay:
        command[-1] = f'Launch.Replay={args.replay.resolve()}'
    success = False
    with transcript.open('w', encoding='utf-8') as output:
        process = subprocess.Popen(command, cwd=ROOT, stdout=output, stderr=subprocess.STDOUT)
        try:
            deadline = time.monotonic() + timeout
            while time.monotonic() < deadline:
                data = transcript.read_text(encoding='utf-8', errors='replace')
                state = diagnostic_status(data, args.scenario)
                if state == 'failed' or process.poll() is not None:
                    break
                if state == 'passed':
                    success = True
                    break
                time.sleep(.5)
        finally:
            if process.poll() is None:
                process.terminate()
                process.wait(timeout=15)
    data = transcript.read_text(encoding='utf-8', errors='replace')
    for line in data.splitlines():
        if marker in line:
            print(line)
    print('Full native transcript:', transcript)
    if not success:
        print('Game process exit code:', process.returncode)
        raise SystemExit('Native acceptance failed or timed out; inspect the transcript and Logs/lua.log')


if __name__ == '__main__':
    main()
