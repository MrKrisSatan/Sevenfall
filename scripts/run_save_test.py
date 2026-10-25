"""Save through the normal world API, reload through the normal lobby order, compare state."""
import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess

ROOT=Path(__file__).resolve().parents[1]

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--package',type=Path)
    p.add_argument('--engine-dir',type=Path,default=ROOT/'.sdk/engine')
    p.add_argument('--support-dir',type=Path,required=True)
    p.add_argument('--dotnet',default=str(ROOT/'.tools/dotnet10/dotnet.exe'))
    p.add_argument('--timeout',type=int,default=180)
    a=p.parse_args();engine=(a.package or a.engine_dir).resolve();support=a.support_dir.resolve()
    if support.exists():p.error('Choose a fresh support directory; existing evidence is preserved')
    support.mkdir(parents=True)
    search=str(engine/'mods') if a.package else f'{ROOT/".sdk/mods"},{engine/"mods"}'
    env=dict(os.environ,ENGINE_DIR=str(engine),MOD_SEARCH_PATHS=search)
    prefix=[str(engine/'Sevenfall.exe'),f'Engine.LaunchPath={engine/"Sevenfall.exe"}'] if a.package else [a.dotnet,str(engine/'bin/OpenRA.dll')]
    snapshots=[]
    for mode in ('baseline','loaded'):
        folder=support/mode;folder.mkdir()
        if mode=='loaded':
            files=list((support/'baseline/Saves').rglob('sevenfall-acceptance.orasav'))
            if len(files)!=1 or files[0].stat().st_size==0:raise RuntimeError('Actual save file missing or ambiguous')
            shutil.copytree(support/'baseline/Saves',folder/'Saves')
        command=[*prefix,'Game.Mod=sevenfall',f'Engine.EngineDir={engine}',f'Engine.ModSearchPaths={search}',f'Engine.SupportDir={folder}',
            'Player.Name=SaveTester','Graphics.Mode=Windowed','Graphics.WindowedSize=1024,768','Graphics.DisableHardwareCursors=True',
            'Debug.SendSystemInformation=False','Debug.SystemInformationVersionPrompt=999','Game.IntroductionPromptVersion=999',
            'Launch.Map=save-test' if mode=='baseline' else 'Sevenfall.LoadAcceptance=sevenfall-acceptance.orasav']
        log=support/(mode+'.log')
        with log.open('w',encoding='utf-8') as output:
            subprocess.run(command,cwd=ROOT,env=env,stdout=output,stderr=subprocess.STDOUT,check=True,timeout=a.timeout)
        text=log.read_text(encoding='utf-8',errors='replace')
        if 'SAVE_TEST COMPLETE restored='+('False' if mode=='baseline' else 'True') not in text or 'DOCTRINE_TEST COMPLETE checks=34' not in text:
            raise RuntimeError('Save/load or doctrine acceptance failed: '+mode)
        if 'SAVE_TEST FAIL' in text or 'Fatal Lua Error' in text or 'Exception of type' in text:
            raise RuntimeError('Save/load logged a failure: '+mode)
        snapshots.append(dict(re.findall(r'SAVE_TEST SNAPSHOT tick=(\d+) hash=(-?\d+)',text)))
    if len(snapshots[0])!=4 or snapshots[0]!=snapshots[1]:raise RuntimeError('Restored state diverged from uninterrupted state')
    report={'normal_save_and_load_orders':True,'doctrine_assertions_per_run':34,'matching_state_checkpoints':snapshots[0],'normal_exit_codes':[0,0]}
    (support/'save-acceptance.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('PASS: real save/load, four matching world-state hashes and 34 doctrine checks per run.')

if __name__=='__main__':main()
