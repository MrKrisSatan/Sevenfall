"""Two independent native clients and a local dedicated server; compare real sync hashes."""
import argparse
import json
import os
from pathlib import Path
import re
import socket
import subprocess
import time

ROOT=Path(__file__).resolve().parents[1]

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--engine-dir',type=Path,default=ROOT/'.sdk/engine')
    parser.add_argument('--package',type=Path)
    parser.add_argument('--dotnet',default=str(ROOT/'.tools/dotnet10/dotnet.exe'))
    parser.add_argument('--support-dir',type=Path,required=True)
    parser.add_argument('--timeout',type=int,default=240)
    args=parser.parse_args();engine=(args.package or args.engine_dir).resolve();support=args.support_dir.resolve()
    if support.exists():parser.error('Preserving existing acceptance evidence; choose a fresh directory')
    support.mkdir(parents=True)
    search=str(engine/'mods') if args.package else f'{ROOT/".sdk/mods"},{engine/"mods"}'
    env=dict(os.environ,ENGINE_DIR=str(engine),MOD_SEARCH_PATHS=search)
    utility=[str(engine/'OpenRA.Utility.exe')] if args.package else [args.dotnet,str(engine/'bin/OpenRA.Utility.dll')]
    network_map=engine/'mods/sevenfall/maps/network-test' if args.package else ROOT/'.sdk/mods/sevenfall/maps/network-test'
    uid=subprocess.check_output([*utility,'sevenfall','--map-hash',str(network_map)],env=env,text=True).strip()
    if not re.fullmatch('[0-9a-f]{40}',uid):raise RuntimeError('Invalid map hash output')
    with socket.socket() as reservation:
        reservation.bind(('127.0.0.1',0));port=reservation.getsockname()[1]
    server_support=support/'server';server_support.mkdir()
    common=[f'Engine.EngineDir={engine}',f'Engine.ModSearchPaths={env["MOD_SEARCH_PATHS"]}','Game.Mod=sevenfall']
    files=[];processes=[]
    try:
        server_log=(support/'server.log').open('w',encoding='utf-8');files.append(server_log)
        server_command=[str(engine/'OpenRA.Server.exe')] if args.package else [args.dotnet,str(engine/'bin/OpenRA.Server.dll')]
        server=subprocess.Popen([*server_command,*common,f'Engine.SupportDir={server_support}',f'Server.ListenPort={port}',f'Server.Map={uid}','Server.AdvertiseOnline=False','Server.DiscoverNatDevices=False','Server.EnableGeoIP=False','Server.EnableSyncReports=True','Server.QueryMapRepository=False','Server.RecordReplays=True'],env=env,cwd=ROOT,stdout=server_log,stderr=subprocess.STDOUT)
        processes.append(server)
        deadline=time.monotonic()+30
        while time.monotonic()<deadline:
            if server.poll() is not None:raise RuntimeError('Dedicated server failed; inspect server.log')
            try:
                with socket.create_connection(('127.0.0.1',port),timeout=.25):break
            except OSError:time.sleep(.25)
        else:raise RuntimeError('Dedicated server did not start')
        clients=[]
        for i in range(2):
            folder=support/f'client-{i}';folder.mkdir()
            transcript=(support/f'client-{i}.log').open('w',encoding='utf-8');files.append(transcript)
            client_command=[str(engine/'Sevenfall.exe'),f'Engine.LaunchPath={engine/"Sevenfall.exe"}'] if args.package else [args.dotnet,str(engine/'bin/OpenRA.dll')]
            client=subprocess.Popen([*client_command,*common,f'Engine.SupportDir={folder}',f'Player.Name=NetworkTester{i}',f'Launch.Connect=127.0.0.1:{port}','Sevenfall.NetworkAcceptance=2','Graphics.Mode=Windowed','Graphics.WindowedSize=1024,768','Graphics.DisableHardwareCursors=True','Debug.SendSystemInformation=False','Debug.SystemInformationVersionPrompt=999','Game.IntroductionPromptVersion=999'],env=env,cwd=ROOT,stdout=transcript,stderr=subprocess.STDOUT)
            clients.append(client);processes.append(client)
        deadline=time.monotonic()+args.timeout
        while time.monotonic()<deadline and any(c.poll() is None for c in clients):time.sleep(.5)
        texts=[(support/f'client-{i}.log').read_text(encoding='utf-8',errors='replace') for i in range(2)]
        snapshots=[dict(re.findall(r'NETWORK_TEST SNAPSHOT tick=(\d+) hash=(-?\d+)',text)) for text in texts]
        for i,(client,text) in enumerate(zip(clients,texts)):
            if client.poll()!=0 or 'NETWORK_TEST COMPLETE ticks=1250' not in text or 'DOCTRINE_TEST COMPLETE checks=34' not in text:
                raise RuntimeError(f'Client {i} did not complete native network/doctrine acceptance')
            if 'out of sync' in text.lower() or 'Fatal Lua Error' in text or 'Exception of type' in text:
                raise RuntimeError(f'Client {i} logged an exception or synchronization failure')
        if len(snapshots[0])<5 or snapshots[0]!=snapshots[1]:raise RuntimeError('Independent client sync snapshots differ')
        report={'clients':2,'dedicated_server':True,'doctrine_assertions_per_client':34,'matching_sync_snapshots':snapshots[0],'ticks':1250,'normal_client_exit_codes':[c.returncode for c in clients]}
        (support/'network-acceptance.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
        print('PASS: two native clients, 34 doctrine checks each, matching sync hashes and graceful exits.')
    finally:
        for process in reversed(processes):
            if process.poll() is None:
                process.terminate();process.wait(timeout=15)
        for file in files:file.close()

if __name__=='__main__':main()
