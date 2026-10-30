"""Native acceptance of all seventeen building-bound powers and the Defences UI."""
from pathlib import Path
from build_faction_identities import FACTIONS
from build_realm_completion import REALMS
ROOT=Path(__file__).resolve().parents[1]
dest=ROOT/'mods/sevenfall/maps/powerlifecycle-test';dest.mkdir(exist_ok=True)
(dest/'map.bin').write_bytes((ROOT/'mods/sevenfall/maps/newrealms-test/map.bin').read_bytes())
roster=[(f[0],'sf_'+f[0]+'_ultimate') for f in FACTIONS]+[(fid,p+'_cataclysm') for p,fid in zip(REALMS,['h_bastion','a_seraph','d_legion','i_echo','f_thrones'])]
lines=['MapFormat: 12','RequiresMod: sevenfall','Title: Sevenfall Superweapon Lifecycle Diagnostic','Author: Sevenfall contributors','Tileset: TEMPERAT','MapSize: 128,128','Bounds: 1,1,126,126','Visibility: Lobby','Categories: Test','Players:', '\tPlayerReference@Neutral:\n\t\tName: Neutral\n\t\tOwnsWorld: True\n\t\tNonCombatant: True\n\t\tFaction: h_bastion']
for i,(fid,_) in enumerate(roster):
 name='Observer' if i==0 else 'P'+str(i)
 lines.append(f'\tPlayerReference@{name}:\n\t\tName: {name}\n\t\tFaction: {fid}'+('\n\t\tPlayable: True\n\t\tNonCombatant: True' if i==0 else ''))
lines+=['Actors:\n\tSpawn: mpspawn\n\t\tOwner: Neutral\n\t\tLocation: 40,40','Rules:\n\tWorld:\n\t\t-SpawnStartingUnits:\n\t\tSFPowerSidebarProbe:\n\t\tLuaScript:\n\t\t\tScripts: powerlifecycle-test.lua\n\tPlayer:\n\t\t-ConquestVictoryConditions:\n\t\tShroud:\n\t\t\tFogCheckboxEnabled: False\n\t\t\tExploredMapCheckboxEnabled: True']
for _,actor in roster:lines.append(f'\t{actor.upper()}:\n\t\tSFFactionPower:\n\t\t\tChargeInterval: 75')
(dest/'map.yaml').write_text('\n'.join(lines)+'\n')
actors=','.join("'"+actor+"'" for _,actor in roster)
lua="local types={"+actors+"}\n"+r'''local players,sources,plants,remaining={},{},{},{}
local checks,failures=0,0
local yard,duplicate
local function Check(ok,name)
 if ok then checks=checks+1;print('POWERLIFECYCLE_TEST PASS: '..name)
 else failures=failures+1;print('POWERLIFECYCLE_TEST FAIL: '..name) end
end
local function Make(kind,p,x,y) return Actor.Create(kind,true,{Owner=p,Location=CPos.New(x,y)}) end
local function Source(i)
 return Make(types[i],players[i],8+((i-1)%5)*23,12+math.floor((i-1)/5)*25)
end
local function Plants(i)
 local a={};for j=1,5 do a[j]=Make('h_generator',players[i],5+((i-1)%5)*23+j*3,5+math.floor((i-1)/5)*25) end
 return a
end
WorldLoaded=function()
 for i=1,#types do players[i]=Player.GetPlayer(i==1 and 'Observer' or 'P'..(i-1));plants[i]=Plants(i) end
 yard=Make('fact',players[1],8,18)
 Camera.Position=Map.CenterOfCell(CPos.New(12,12))
 Trigger.AfterDelay(DateTime.Seconds(1),function()
  for i,p in ipairs(players) do Check(p.FactionPowerCount==0,'no building means no power '..types[i]);sources[i]=Source(i) end
 end)
 Trigger.AfterDelay(DateTime.Seconds(2),function()
  for i,p in ipairs(players) do Check(p.FactionPowerCount==1 and not p.FactionPowerReady,'building automatically starts charging '..types[i]) end
 end)
 Trigger.AfterDelay(DateTime.Seconds(5),function()
  for i,p in ipairs(players) do Check(p.FactionPowerReady,'automatic charge completes '..types[i]) end
 end)
 Trigger.AfterDelay(DateTime.Seconds(8),function() for _,a in ipairs(sources) do a.Kill('DefaultDeath') end;yard.Kill('DefaultDeath') end)
 Trigger.AfterDelay(DateTime.Seconds(9),function()
  for i,p in ipairs(players) do Check(p.FactionPowerCount==0 and not p.FireFactionPower(CPos.New(120,120)),'destroyed building removes ready power and blocks orders '..types[i]) end
 end)
 Trigger.AfterDelay(DateTime.Seconds(10),function() for i=1,#types do sources[i]=Source(i) end end)
 Trigger.AfterDelay(DateTime.Seconds(11),function()
  for i,p in ipairs(players) do Check(p.FactionPowerCount==1 and not p.FactionPowerReady and p.FactionPowerRemaining>0,'rebuild restores fresh charging '..types[i]) end
 end)
 Trigger.AfterDelay(DateTime.Seconds(14),function()
  for i,p in ipairs(players) do Check(p.FactionPowerReady and p.FireFactionPower(CPos.New(120,120)) and not p.FactionPowerReady,'rebuilt building can deploy and recharge '..types[i]) end
 end)
 Trigger.AfterDelay(DateTime.Seconds(15),function() for _,group in ipairs(plants) do for _,a in ipairs(group) do a.Destroy() end end end)
 Trigger.AfterDelay(DateTime.Seconds(16),function() for i,p in ipairs(players) do remaining[i]=p.FactionPowerRemaining end end)
 Trigger.AfterDelay(DateTime.Seconds(17),function()
  for i,p in ipairs(players) do Check(p.FactionPowerCount==1 and not p.FactionPowerReady and p.FactionPowerRemaining==remaining[i],'low power pauses charge without removing icon '..types[i]);plants[i]=Plants(i) end
 end)
 Trigger.AfterDelay(DateTime.Seconds(21),function()
  for i,p in ipairs(players) do Check(p.FactionPowerReady,'restoring electricity resumes charge '..types[i]);sources[i].Destroy() end
 end)
 Trigger.AfterDelay(DateTime.Seconds(22),function()
  for i,p in ipairs(players) do Check(p.FactionPowerCount==0,'removal or sale removes power '..types[i]);sources[i]=Source(i) end
 end)
 Trigger.AfterDelay(DateTime.Seconds(26),function()
  for i,p in ipairs(players) do Check(p.FactionPowerReady,'rebuild after removal restores power '..types[i]) end
  duplicate=Make(types[17],players[17],110,100)
 end)
 Trigger.AfterDelay(DateTime.Seconds(28),function() sources[17].Kill('DefaultDeath') end)
 Trigger.AfterDelay(DateTime.Seconds(29),function() Check(players[17].FactionPowerReady,'surviving duplicate retains shared power');duplicate.Kill('DefaultDeath') end)
 Trigger.AfterDelay(DateTime.Seconds(30),function() Check(players[17].FactionPowerCount==0,'last duplicate lost removes shared power') end)
 Trigger.AfterDelay(DateTime.Seconds(32),function()
  for i=2,#types do Make(types[i],players[1],8+((i-1)%5)*23,105+math.floor((i-1)/5)*5) end
  for j=1,20 do Make('h_generator',players[1],3+j*5,124) end
 end)
 Trigger.AfterDelay(DateTime.Seconds(40),function()
  Check(players[1].FactionPowerCount==17,'captured installations expose seventeen distinct powers')
  if failures==0 then print('POWERLIFECYCLE_TEST COMPLETE checks='..checks) end
 end)
end
'''
(dest/'powerlifecycle-test.lua').write_text(lua)
