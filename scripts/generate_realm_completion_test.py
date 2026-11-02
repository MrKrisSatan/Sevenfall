"""Native paid-production, aerial combat and shared-superweapon acceptance."""
from pathlib import Path
from build_realm_completion import REALMS,AIR,BEAST
ROOT=Path(__file__).resolve().parents[1];dest=ROOT/'mods/sevenfall/maps/realmcompletion-test';dest.mkdir(exist_ok=True)
(dest/'map.bin').write_bytes((ROOT/'mods/sevenfall/maps/newrealms-test/map.bin').read_bytes())
lines=['MapFormat: 12','RequiresMod: sevenfall','Title: Sevenfall Shared Realm Arsenal Diagnostic','Author: Sevenfall contributors','Tileset: TEMPERAT','MapSize: 128,128','Bounds: 1,1,126,126','Visibility: Lobby','Categories: Test','Players:',
'\tPlayerReference@Neutral:\n\t\tName: Neutral\n\t\tOwnsWorld: True\n\t\tNonCombatant: True\n\t\tFaction: h_bastion',
'\tPlayerReference@Observer:\n\t\tName: Observer\n\t\tPlayable: True\n\t\tNonCombatant: True\n\t\tFaction: h_bastion',
'\tPlayerReference@Enemy:\n\t\tName: Enemy\n\t\tFaction: h_bastion\n\t\tEnemies: P0, P1, P2, P3, P4, Cancel']
for i,fid in enumerate(['h_bastion','a_seraph','d_legion','i_echo','f_thrones']):lines.append(f'\tPlayerReference@P{i}:\n\t\tName: P{i}\n\t\tFaction: {fid}\n\t\tEnemies: Enemy')
lines+=['\tPlayerReference@Cancel:\n\t\tName: Cancel\n\t\tFaction: a_warden\n\t\tEnemies: Enemy','Actors:\n\tSpawn: mpspawn\n\t\tOwner: Neutral\n\t\tLocation: 45,65',
'Rules:\n\tWorld:\n\t\t-SpawnStartingUnits:\n\t\tLuaScript:\n\t\t\tScripts: realmcompletion-test.lua\n\tPlayer:\n\t\t-ConquestVictoryConditions:\n\t\tShroud:\n\t\t\tFogCheckboxEnabled: False\n\t\t\tFogCheckboxLocked: True\n\t\t\tExploredMapCheckboxEnabled: True\n\t\t\tExploredMapCheckboxLocked: True']
for p in REALMS:
 lines.append(f'\t{p.upper()}_CATACLYSM:\n\t\tSFFactionPower:\n\t\t\tChargeInterval: 25')
 for suffix in ['helipad','kennel']:lines.append(f'\t{p.upper()}_{suffix.upper()}:\n\t\tBuildable:\n\t\t\tBuildDuration: 25\n\t\t\tBuildDurationModifier: 100')
 for data in (AIR[p],BEAST[p]):lines.append(f'\t{p.upper()}_{data[0].upper()}:\n\t\tBuildable:\n\t\t\tBuildDuration: 25\n\t\t\tBuildDurationModifier: 100')
(dest/'map.yaml').write_text('\n'.join(lines)+'\n')
lua='''local checks, failures=0,0
local players,sources,targets,allies,neutrals,outsiders,airtargets={}, {}, {}, {}, {}, {}, {}
local names={'h','a','d','i','f'}
local air={'h_gunship','a_skywarden','d_wyvern','i_interceptor','f_bonekite'}
local beasts={'h_warhound','a_gryphon','d_hellhound','i_stalker','f_carrion'}
local powers={'h_generator','a_spire','d_heart','i_generator','f_spire'}
local cancelSource,cancelTarget,cancelPlayer,saltTree,saltBridge,saltAircraft
local function Check(ok,name)
 if ok then checks=checks+1;print('REALMCOMPLETION_TEST PASS: '..name)
 else failures=failures+1;print('REALMCOMPLETION_TEST FAIL: '..name) end
end
local function Make(kind,owner,x,y) return Actor.Create(kind,true,{Owner=owner,Location=CPos.New(x,y)}) end
WorldLoaded=function()
 local enemy=Player.GetPlayer('Enemy');local neutral=Player.GetPlayer('Neutral')
 for i,prefix in ipairs(names) do
  local p=Player.GetPlayer('P'..(i-1));players[i]=p;p.Cash=30000
  local x=8+(i-1)*24
  Make('fact',p,x,6);Make(prefix..'_tech',p,x+6,6)
  Make(prefix..'_radar',p,x,31)
  Make(({'h_barracks','a_chapel','d_pit','i_barracks','f_chapel'})[i],p,x+6,31)
  Make(prefix..'_helipad',p,x,16);Make(prefix..'_kennel',p,x+6,16)
  for j=0,4 do Make(powers[i],p,x+j*3,26) end
  sources[i]=Make(prefix..'_cataclysm',p,x+10,6)
  targets[i]=Make('h_generator',enemy,x,80)
  allies[i]=Make('h_rifleman',p,x+1,82)
  neutrals[i]=Make('h_rifleman',neutral,x-1,82)
  outsiders[i]=Make('h_rifleman',enemy,x+9,80)
  airtargets[i]=Make('h_generator',enemy,x,45)
 end
 saltAircraft=Make('h_gunship',neutral,33,81)
 saltTree=Make('sf_oak',neutral,30,80)
 saltBridge=Make('sf_bridge_ew',neutral,31,78)
 cancelPlayer=Player.GetPlayer('Cancel')
 for j=0,4 do Make('a_spire',cancelPlayer,8+j*3,106) end
 cancelSource=Make('a_cataclysm',cancelPlayer,24,106)
 cancelTarget=Make('h_rifleman',enemy,45,106)
 Camera.Position=Map.CenterOfCell(CPos.New(38,80))
 Trigger.AfterDelay(DateTime.Seconds(4),function()
  for i,p in ipairs(players) do
   Check(p.QueueProduction(air[i]),'paid aircraft queue '..air[i])
   Check(p.QueueProduction(beasts[i]),'paid beast queue '..beasts[i])
   Check(p.FireFactionPower(targets[i].Location),'shared power order '..names[i])
  end
  Check(cancelPlayer.FireFactionPower(cancelTarget.Location),'cancellable Witness order')
  cancelSource.Kill('DefaultDeath')
 end)
 Trigger.AfterDelay(DateTime.Seconds(7),function()
  for i,p in ipairs(players) do
   local flyers=p.GetActorsByType(air[i]);local animals=p.GetActorsByType(beasts[i])
   Check(#flyers==1,'aircraft produced '..air[i]);Check(#animals==1,'beast produced '..beasts[i])
   Check(p.Cash<30000,'production deducted credits '..names[i])
   if #flyers>0 then flyers[1].Attack(airtargets[i],true,true) end
  end
 end)
 Trigger.AfterDelay(DateTime.Seconds(10),function()
  Check(saltAircraft.IsPetrified,'aircraft becomes salt')
  Check(targets[2].IsPetrified,'building becomes salt')
  Check(saltTree.IsPetrified and saltBridge.IsPetrified,'trees and bridges become salt')
  Check(allies[2].IsPetrified,'friendly unit becomes salt')
  Check(neutrals[2].IsPetrified,'neutral unit becomes salt')
  Check(not outsiders[2].IsPetrified,'outside radius remains free')
  Check(not targets[2].IsDead,'statue persists before crumble')
  Check(not cancelTarget.IsPetrified and not cancelTarget.IsDead,'destroying source during warning cancels flash')
  sources[2].Kill('DefaultDeath')
 end)
 Trigger.AfterDelay(DateTime.Seconds(15),function()
  Check(targets[2].IsDead and allies[2].IsDead and neutrals[2].IsDead,'salt crumbles even after source loss')
  Check(not outsiders[2].IsDead,'outside radius survives')
  Check(saltAircraft.IsDead,'aircraft crumbles')
  Check(saltTree.IsDead and saltBridge.IsDead,'trees and bridges crumble')
  Check(allies[1].IsDead and neutrals[1].IsDead,'nuclear friendly and neutral damage')
  for _,i in ipairs({1,3,4,5}) do Check(targets[i].IsDead or targets[i].Health<targets[i].MaxHealth,'shared strike damages target '..names[i]) end
 end)
 Trigger.AfterDelay(DateTime.Seconds(20),function()
  for i,p in ipairs(players) do Check(p.QueueProduction(names[i]..'_helipad'),'normal helipad construction queue '..names[i]) end
 end)
 Trigger.AfterDelay(DateTime.Seconds(22),function()
  for i,p in ipairs(players) do p.PlaceCompletedBuilding(names[i]..'_helipad',CPos.New(11+(i-1)*24,6)) end
 end)
 Trigger.AfterDelay(DateTime.Seconds(24),function()
  for i,p in ipairs(players) do Check(#p.GetActorsByType(names[i]..'_helipad')==2,'paid helipad placed '..names[i]);Check(p.QueueProduction(names[i]..'_kennel'),'normal kennel construction queue '..names[i]) end
 end)
 Trigger.AfterDelay(DateTime.Seconds(26),function()
  for i,p in ipairs(players) do p.PlaceCompletedBuilding(names[i]..'_kennel',CPos.New(11+(i-1)*24,10)) end
 end)
 Trigger.AfterDelay(DateTime.Seconds(30),function()
  for i,p in ipairs(players) do Check(#p.GetActorsByType(names[i]..'_kennel')==2,'paid kennel placed '..names[i]) end
 end)
 Trigger.AfterDelay(DateTime.Seconds(45),function()
  for i,a in ipairs(airtargets) do Check(a.IsDead or a.Health<a.MaxHealth,'aircraft damages ground target '..air[i]) end
  if failures==0 then print('REALMCOMPLETION_TEST COMPLETE checks='..checks) end
 end)
end
'''
(dest/'realmcompletion-test.lua').write_text(lua)

for name,probe in [('realmcompletionnetwork-test','\t\tSFNetworkProbe:'),('realmcompletionsave-test','\t\tSFSaveProbe:\n\t\t\tSaveTick: 250\n\t\t\tFinalTick: 1250')]:
 folder=dest.with_name(name);folder.mkdir(exist_ok=True)
 (folder/'map.bin').write_bytes((dest/'map.bin').read_bytes())
 (folder/'realmcompletion-test.lua').write_text(lua,encoding='utf-8')
 text=(dest/'map.yaml').read_text(encoding='utf-8').replace('\tWorld:\n','\tWorld:\n'+probe+'\n')
 if 'network' in name:
  text=text.replace('Actors:\n','\tPlayerReference@Observer2:\n\t\tName: Observer2\n\t\tPlayable: True\n\t\tNonCombatant: True\n\t\tFaction: h_bastion\nActors:\n\tSpawn2: mpspawn\n\t\tOwner: Neutral\n\t\tLocation: 46,65\n')
 (folder/'map.yaml').write_text(text,encoding='utf-8')
