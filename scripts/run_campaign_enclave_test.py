"""Exercise the actual three preview enclave scripts in disposable staged maps."""
import os
from pathlib import Path
import shutil
import subprocess
import time
ROOT=Path(__file__).resolve().parents[1]
engine=ROOT/'.sdk/engine';mod=ROOT/'.sdk/mods/sevenfall'
cases=[('h03-glass-fields','u','h_engineer',False),('a03-glass-wrath','n','a_engineer',False),('d02-seeds-ruin','o','d_engineer',True)]
for name,prefix,engineer,hostile in cases:
 target=mod/'maps'/('enclave-'+name+'-test')
 target.mkdir(exist_ok=True)
 for source in (mod/'maps'/name).iterdir():
  if source.is_file():shutil.copy2(source,target/source.name)
 yaml=(target/'map.yaml').read_text().replace('mission.lua, enclave.lua','mission.lua, enclave.lua, probe.lua')
 (target/'map.yaml').write_text(yaml)
 probe='''local startEnclave=WorldLoaded
local function Check(ok,name) if ok then print('ENCLAVE_TEST PASS: '..name) else print('ENCLAVE_TEST FAIL: '..name) end end
WorldLoaded=function()
 startEnclave()
 local commander=Player.GetPlayer('Commander')
 local neutral=Player.GetPlayer('Enclave')
 local friendly=Player.GetPlayer('EnclaveFriendly')
 local hostile=Player.GetPlayer('EnclaveHostile')
 Trigger.AfterDelay(DateTime.Seconds(2),function()
  INITIAL_CHECK
  AID
 end)
end
'''
 if hostile:
  probe=probe.replace('INITIAL_CHECK',f"Check(#hostile.GetActorsByType('{prefix}_bulwark')==1,'hostile enclave exists');print('ENCLAVE_TEST COMPLETE')").replace('AID','')
 else:
  probe=probe.replace('INITIAL_CHECK',f"Check(#neutral.GetActorsByType('{prefix}_bulwark')==1,'neutral enclave exists')")
  probe=probe.replace('AID',f'''local engineer=Actor.Create('{engineer}',true,{{Owner=commander,Location=CPos.New(48,26)}})
  Trigger.AfterDelay(DateTime.Seconds(3),function()
   Check(#friendly.GetActorsByType('{prefix}_bulwark')==1,'engineer aid befriends enclave')
   local attacker=Actor.Create('h_rifleman',true,{{Owner=commander,Location=CPos.New(48,24)}})
   attacker.Stance='HoldFire'
   Trigger.AfterDelay(1,function()
    local victim=friendly.GetActorsByType('{prefix}_bulwark')[1]
    if victim then attacker.IdentityDamage(victim,100) end
    Trigger.AfterDelay(DateTime.Seconds(2),function()
     Check(#hostile.GetActorsByType('{prefix}_bulwark')==1,'attacking aided enclave turns it hostile')
     print('ENCLAVE_TEST COMPLETE')
    end)
   end)
  end)''')
 (target/'probe.lua').write_text(probe)
 support=ROOT/'.tools'/('acceptance-enclave-'+prefix);support.mkdir(exist_ok=True)
 log=support/'native.log'
 command=[str(ROOT/'.tools/dotnet10/dotnet.exe'),str(engine/'bin/OpenRA.dll'),'Game.Mod=sevenfall',f'Engine.EngineDir={engine}',f'Engine.ModSearchPaths={ROOT/".sdk/mods"},{engine/"mods"}',f'Engine.SupportDir={support}','Graphics.Mode=Windowed','Graphics.WindowedSize=1280,720','Graphics.DisableHardwareCursors=True','Debug.SendSystemInformation=False','Debug.SystemInformationVersionPrompt=999','Game.IntroductionPromptVersion=999',f'Launch.Map={target.name}']
 with log.open('w',encoding='utf-8') as output:
  process=subprocess.Popen(command,cwd=ROOT,stdout=output,stderr=subprocess.STDOUT)
  try:
   deadline=time.monotonic()+50
   while time.monotonic()<deadline:
    data=log.read_text(encoding='utf-8',errors='replace')
    if 'ENCLAVE_TEST COMPLETE' in data or 'Fatal Lua Error' in data or process.poll() is not None:break
    time.sleep(.5)
  finally:
   if process.poll() is None:process.terminate();process.wait(timeout=15)
 data=log.read_text(encoding='utf-8',errors='replace')
 for line in data.splitlines():
  if 'ENCLAVE_TEST' in line:print(name,line)
 assert 'ENCLAVE_TEST COMPLETE' in data and 'ENCLAVE_TEST FAIL' not in data and 'Fatal Lua Error' not in data,str(log)
 # Only remove the disposable map created above, inside this exact staged mod.
 assert target.resolve().parent==(mod/'maps').resolve() and target.name.startswith('enclave-')
 shutil.rmtree(target)
print('PASS: all three preview enclave scripts, neutral aid and hostility transitions.')
