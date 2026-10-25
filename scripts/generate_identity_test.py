"""Build isolated native faction/superweapon acceptance, using the public support-power order path."""
from pathlib import Path
import shutil
from build_faction_identities import FACTIONS
ROOT=Path(__file__).resolve().parents[1]
dest=ROOT/'mods/sevenfall/maps/identity-test'
dest.mkdir(exist_ok=True)
shutil.copyfile(ROOT/'mods/sevenfall/maps/doctrine-test/map.bin',dest/'map.bin')
lines=['MapFormat: 12','RequiresMod: sevenfall','Title: Sevenfall Twelve Faction Identity Diagnostic','Author: Sevenfall contributors','Tileset: TEMPERAT','MapSize: 96,96','Bounds: 1,1,94,94','Visibility: Lobby','Categories: Test','Players:', '\tPlayerReference@Neutral:\n\t\tName: Neutral\n\t\tOwnsWorld: True\n\t\tNonCombatant: True\n\t\tFaction: h_area52', '\tPlayerReference@Observer:\n\t\tName: Observer\n\t\tPlayable: True\n\t\tNonCombatant: True\n\t\tFaction: h_area52', '\tPlayerReference@Enemy:\n\t\tName: Enemy\n\t\tFaction: h_area52\n\t\tEnemies: '+', '.join(f'F{i+1}' for i in range(12))]
for i,f in enumerate(FACTIONS,1):lines += [f'\tPlayerReference@F{i}:\n\t\tName: F{i}\n\t\tFaction: {f[0]}\n\t\tEnemies: Enemy']
lines+=['Actors:', '\tSpawn: mpspawn\n\t\tOwner: Neutral\n\t\tLocation: 45,45']
def actor(name,kind,owner,x,y):lines.append(f'\t{name}: {kind}\n\t\tOwner: {owner}\n\t\tLocation: {x},{y}')
for i,f in enumerate(FACTIONS,1):
 x=8+((i-1)%3)*28;y=8+((i-1)//3)*21
 actor(f'Power{i}',{'a':'a_spire','h':'h_generator','d':'d_heart'}[f[0][0]],f'F{i}',x,y)
 actor(f'Reserve{i}',{'a':'a_spire','h':'h_generator','d':'d_heart'}[f[0][0]],f'F{i}',x+4,y)
 actor(f'Ultimate{i}',f'sf_{f[0]}_ultimate',f'F{i}',x,y+3)
 actor(f'Unit{i}','sf_identity_infantry',f'F{i}',x+9,y+7)
 actor(f'Enemy{i}','sf_identity_infantry','Enemy',x+10,y+7)
 actor(f'Armor{i}','sf_identity_armor','Enemy',x+11,y+7)
 actor(f'Building{i}','h_generator','Enemy',x+12,y+7)
 actor(f'Specialist{i}',f[6],f'F{i}',x+8,y+9)
actor('Gate','a_gatekeeper','F2',43,15)
actor('Supply','h_pathfinder','F6',72,36)
actor('Oath','h_confessor','F7',16,57)
actor('Iron','d_taskmaster','F9',72,57)
actor('BroodKiller','d_goremaw','F10',13,81)
actor('BroodVictim','sf_identity_infantry','Enemy',14,81)
actor('BroodFriendly','sf_identity_infantry','F10',15,77)
actor('CourtCaster','d_silencer','F11',40,87)
actor('CourtVictim','sf_identity_infantry','Enemy',43,87)
lines+=['Rules:', '\tWorld:\n\t\t-SpawnStartingUnits:\n\t\tLuaScript:\n\t\t\tScripts: identity-test.lua', '\tPlayer:\n\t\tShroud:\n\t\t\tExploredMapCheckboxEnabled: True', '\tSF_IDENTITY_INFANTRY:\n\t\tInherits: H_RIFLEMAN\n\t\t-Buildable:\n\t\tHealth:\n\t\t\tHP: 30000', '\tSF_IDENTITY_ARMOR:\n\t\tInherits: H_BULWARK\n\t\t-Buildable:\n\t\tHealth:\n\t\t\tHP: 300000']
for kind in ['H_RIFLEMAN','H_BULWARK','D_GOREMAW','D_SILENCER','A_GATEKEEPER','H_PATHFINDER','H_CONFESSOR','D_TASKMASTER']+[f[6].upper() for f in FACTIONS]:
 # Unique overrides only.
 if kind in [s.split(':')[0].strip() for s in lines if s.startswith('\t')]:continue
 lines += [f'\t{kind}:\n\t\tAutoTarget:\n\t\t\tInitialStance: HoldFire\n\t\t\tInitialStanceAI: HoldFire']
for f in FACTIONS:lines += [f'\tSF_{f[0].upper()}_ULTIMATE:\n\t\tSFFactionPower:\n\t\t\tChargeInterval: 25']
(dest/'map.yaml').write_text('\n'.join(lines)+'\n',encoding='utf-8')
for name,probe in [('identitynetwork-test','\t\tSFNetworkProbe:'),('identitysave-test','\t\tSFSaveProbe:\n\t\t\tSaveTick: 200\n\t\t\tFinalTick: 1250\n\t\t\tDetailedSnapshots: True')]:
 folder=dest.with_name(name);folder.mkdir(exist_ok=True)
 shutil.copyfile(dest/'map.bin',folder/'map.bin')
 shutil.copyfile(dest/'identity-test.lua',folder/'identity-test.lua')
 text=(dest/'map.yaml').read_text().replace('\tWorld:\n','\tWorld:\n'+probe+'\n')
 if name=='identitynetwork-test':
  text=text.replace('Actors:\n','\tPlayerReference@Observer2:\n\t\tName: Observer2\n\t\tPlayable: True\n\t\tNonCombatant: True\n\t\tFaction: h_area52\nActors:\n')
  text=text.replace('Actors:\n','Actors:\n\tSpawn2: mpspawn\n\t\tOwner: Neutral\n\t\tLocation: 46,45\n')
 (folder/'map.yaml').write_text(text,encoding='utf-8')
# Separate AI acceptance: no scripted targeting and no army manager orders.
aidest=dest.with_name('identityai-test');aidest.mkdir(exist_ok=True)
shutil.copyfile(dest/'map.bin',aidest/'map.bin')
source=(dest/'map.yaml').read_text().replace('Identity Diagnostic','Superweapon AI Diagnostic').replace('Scripts: identity-test.lua','Scripts: identityai-test.lua')
for i,f in enumerate(FACTIONS,1):source=source.replace(f'Name: F{i}\n\t\tFaction: {f[0]}',f'Name: F{i}\n\t\tBot: sevenfall\n\t\tFaction: {f[0]}')
source=source.replace('\tPlayer:\n\t\tShroud:', '\tPlayer:\n'+''.join(f'\t\t-{name}:\n' for name in ('McvManagerBotModule','HarvesterBotModule','BuildingRepairBotModule','BaseBuilderBotModule','UnitBuilderBotModule','SquadManagerBotModule'))+'\t\tShroud:')
(aidest/'map.yaml').write_text(source,encoding='utf-8')
(aidest/'identityai-test.lua').write_text('''local checks=0
WorldLoaded=function()
 Camera.Position=Map.CenterOfCell(CPos.New(44,36))
 Trigger.AfterDelay(DateTime.Seconds(35),function()
  for i=1,12 do
   local p=Player.GetPlayer('F'..i)
   if p.FactionPowerLaunches>0 then checks=checks+1;print('IDENTITYAI_TEST PASS: bot '..i..' independently launched its faction superweapon')
   else print('IDENTITYAI_TEST FAIL: bot '..i..' did not use its superweapon') end
  end
  if checks==12 then print('IDENTITYAI_TEST COMPLETE checks='..checks) end
 end)
end
Tick=function() end
''',encoding='utf-8')
