"""Run the native, content-dependent defense diagnostic and fail on missing acceptance markers.

Requires an already-built SDK and --support-dir containing installed game content.
This launches a local game window, collects evidence, and closes only its own process.
"""
import argparse
from pathlib import Path
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--support-dir', type=Path, required=True)
    parser.add_argument('--dotnet', default='dotnet')
    parser.add_argument('--timeout', type=int, default=110)
    args = parser.parse_args()
    support = args.support_dir.resolve()
    if not (support / 'Content/ra/v2/conquer.mix').is_file():
        parser.error('The selected support directory must already contain installed Red Alert content')
    support.mkdir(parents=True, exist_ok=True)
    engine = ROOT / '.sdk/engine'
    transcript = support / 'defense-diagnostic-output.log'
    command = [args.dotnet, str(engine / 'bin/OpenRA.dll'), 'Game.Mod=sevenfall',
               f'Engine.EngineDir={engine}', f'Engine.ModSearchPaths={ROOT / ".sdk/mods"},{engine / "mods"}',
               f'Engine.SupportDir={support}', 'Graphics.Mode=Windowed', 'Graphics.WindowedSize=1600,900',
               'Graphics.DisableHardwareCursors=True', 'Graphics.CursorDouble=True',
               'Debug.SendSystemInformation=False', 'Debug.SystemInformationVersionPrompt=999',
               'Game.IntroductionPromptVersion=999', 'Launch.Map=defense-test']
    success = False
    with transcript.open('w', encoding='utf-8') as output:
        process = subprocess.Popen(command, cwd=ROOT, stdout=output, stderr=subprocess.STDOUT)
        try:
            deadline = time.monotonic() + args.timeout
            while time.monotonic() < deadline:
                data = transcript.read_text(encoding='utf-8', errors='replace')
                if 'DEFENSE_TEST FAIL:' in data or 'Fatal Lua Error:' in data or process.poll() is not None:
                    break
                if 'DEFENSE_TEST COMPLETE checks=' in data:
                    success = True
                    break
                time.sleep(.5)
        finally:
            if process.poll() is None:
                process.terminate()
                process.wait(timeout=15)
    data = transcript.read_text(encoding='utf-8', errors='replace')
    for line in data.splitlines():
        if 'DEFENSE_TEST' in line:
            print(line)
    print('Full native transcript:', transcript)
    if not success:
        raise SystemExit('Native defense acceptance failed or timed out; inspect the transcript and Logs/lua.log')


if __name__ == '__main__':
    main()
