"""Native expansion acceptance. Prices/prerequisites are real; build time is accelerated."""
from pathlib import Path
import struct
from additional_realms_data import REALMS,UNITS,STRUCTURES
ROOT=Path(__file__).resolve().parents[1]
dest=ROOT/'mods/sevenfall/maps/additionalrealms-test';dest.mkdir(exist_ok=True)
size=128
resource_offset=17+size*size*3
data=bytearray(struct.pack('<BHHIII',2,size,size,17,0,resource_offset)+struct.pack('<HB',255,0)*size*size+bytes(size*size*2))
# Give each isolated production base its own equally distant untouched field.
for i in range(4):
 for x in range(14+i*30,19+i*30):
  for y in range(18,23):
   offset=resource_offset+(x*size+y)*2
   data[offset:offset+2]=bytes((1,12))
(dest/'map.bin').write_bytes(data)
lines=['MapFormat: 12','RequiresMod: sevenfall','Title: Sevenfall Additional Realms Diagnostic','Author: Sevenfall contributors','Tileset: TEMPERAT','MapSize: 128,128','Bounds: 1,1,126,126','Visibility: Lobby','Categories: Test','Players:',
'\tPlayerReference@Neutral:\n\t\tName: Neutral\n\t\tOwnsWorld: True\n\t\tNonCombatant: True\n\t\tFaction: h_bastion',
'\tPlayerReference@Observer:\n\t\tName: Observer\n\t\tPlayable: True\n\t\tNonCombatant: True\n\t\tFaction: h_bastion',
'\tPlayerReference@Enemy:\n\t\tName: Enemy\n\t\tFaction: h_bastion\n\t\tEnemies: P0, P1, P2, P3']
for i,r in enumerate(REALMS.values()):lines.append(f'\tPlayerReference@P{i}:\n\t\tName: P{i}\n\t\tFaction: {r["faction"]}\n\t\tEnemies: Enemy')
lines+=['Actors:\n\tSpawn: mpspawn\n\t\tOwner: Neutral\n\t\tLocation: 45,65','Rules:\n\tWorld:\n\t\t-SpawnStartingUnits:\n\t\tLuaScript:\n\t\t\tScripts: additionalrealms-test.lua\n\tPlayer:\n\t\t-ConquestVictoryConditions:\n\t\tShroud:\n\t\t\tFogCheckboxEnabled: False\n\t\t\tFogCheckboxLocked: True\n\t\t\tExploredMapCheckboxEnabled: True\n\t\t\tExploredMapCheckboxLocked: True']
for p in REALMS:
 for suffix in STRUCTURES+[u[0] for u in UNITS[p]]:
  lines.append(f'\t{p.upper()}_{suffix.upper()}:\n\t\tBuildable:\n\t\t\tBuildDuration: 25\n\t\t\tBuildDurationModifier: 100'+ ('\n\t\tSFFactionPower:\n\t\t\tChargeInterval: 50' if suffix=='cataclysm' else ''))
(dest/'map.yaml').write_text('\n'.join(lines)+'\n')
lua='''local checks,failures,states=0,0,{}
local names={'v','u','o','n'}
local function Check(ok,name)
 if ok then checks=checks+1;print('ADDITIONALREALMS_TEST PASS: '..name)
 else failures=failures+1;print('ADDITIONALREALMS_TEST FAIL: '..name) end
end
local function Make(kind,p,x,y) return Actor.Create(kind,true,{Owner=p,Location=CPos.New(x,y)}) end
local function TestMemories(p)
 local count=0
 for _,a in ipairs(p.GetActorsByType('u_remnant')) do if a.Location==CPos.New(40,85) then count=count+1 end end
 return count
end
WorldLoaded=function()
 local enemy=Player.GetPlayer('Enemy')
 for i,prefix in ipairs(names) do
  local p=Player.GetPlayer('P'..(i-1));p.Cash=100000
  local x=5+(i-1)*30
  local mcv=Make('mcv',p,x,7);mcv.Deploy()
  states[i]={p=p,prefix=prefix,x=x,stage=1,queued=false,count=0}
 end
 Camera.Position=Map.CenterOfCell(CPos.New(35,20))
 Trigger.AfterDelay(DateTime.Seconds(180),function()
  for i,s in ipairs(states) do Check(s.stage==15,'complete paid tree '..s.prefix);Check(s.count==(s.prefix=='n' and 9 or 8),'all units paid '..s.prefix);Check(s.p.Cash<100000,'cash debited '..s.prefix);Check(s.p.RefinedCredits>0,'actual Veilglass deliveries '..s.prefix) end
  if failures==0 then print('ADDITIONALREALMS_TEST COMPLETE checks='..checks) end
 end)
 Trigger.AfterDelay(DateTime.Seconds(35),function()
  local v,u,o,n=states[1].p,states[2].p,states[3].p,states[4].p
  local anchor=Make('v_resonator',v,9,80);local shard=Make('v_rifleman',v,11,80)
  local giant=Make('n_bulwark',n,95,80);local attendant=Make('n_attendant',n,97,80)
  local hush=Make('o_rifleman',o,70,80);local companion=Make('o_rifleman',o,72,80)
  local collector=Make('n_harvester',n,96,83)
  Trigger.AfterDelay(DateTime.Seconds(1),function()
   Check(shard.ActiveIdentity=='sf-growth' and shard.IdentityArmor==80,'powered Veilborn network')
   Check(giant.ActiveIdentity=='sf-attended' and giant.IdentityArmor==85,'attendant protection')
   Check(collector.ActiveIdentity=='none','collectors excluded from aura')
   Check(hush.ActiveIdentity=='none','nearby combatant cancels isolation')
   shard.IdentityDamage(shard,3000);giant.IdentityDamage(giant,20000)
   local hp=giant.Health
   Trigger.AfterDelay(DateTime.Seconds(2),function()
    Check(giant.Health>hp,'attendant recovery');attendant.Destroy();anchor.Destroy();companion.Destroy()
    Trigger.AfterDelay(DateTime.Seconds(1),function()
     Check(shard.ActiveIdentity=='none','lost resonator removes bonus')
     Check(giant.ActiveIdentity=='none','lost attendant removes bonus')
     Check(hush.ActiveIdentity=='sf-isolation' and hush.IdentitySpeed==125,'isolated stalker speed')
    end)
   end)
  end)
  -- Sources use normal SupportPowerManager orders, with the warning intact.
  local sources={}
  for i,s in ipairs(states) do
   sources[i]=Make(s.prefix..'_cataclysm',s.p,s.x+12,60)
   for j=0,4 do Make(s.prefix..'_advpower',s.p,s.x+j*3,65) end
  end
  local killer=Make('h_rifleman',enemy,120,120);killer.Stance='HoldFire'
  local victim=Make('u_rifleman',u,40,85);Trigger.AfterDelay(1,function() killer.IdentityDamage(victim,10000) end)
  local decoy=Make('u_special',u,45,85);Trigger.AfterDelay(1,function() killer.IdentityDamage(decoy,10000) end)
  local ground=Make('h_bulwark',enemy,100,100)
  local flyer=Make('h_gunship',enemy,101,100)
  local building=Make('h_generator',enemy,98,100)
  local quiet=Make('h_bulwark',enemy,70,100)
  quiet.Stance='HoldFire';flyer.Stance='HoldFire';ground.Stance='HoldFire'
  Trigger.AfterDelay(DateTime.Seconds(3),function()
   print('ADDITIONALREALMS_TEST DETAIL memories='..#u.GetActorsByType('u_remnant')..' victimdead='..tostring(victim.IsDead)..' corpses='..#u.GetActorsByType('u_rifleman.death'))
   Check(TestMemories(u)==1,'real death leaves memory')
   Check(u.FireFactionPower(CPos.New(40,85)),'Restoration launch')
   Check(o.FireFactionPower(CPos.New(70,100)),'Absolute Silence launch')
   Check(n.FireFactionPower(CPos.New(100,100)),'Earthbreaker launch')
   Check(v.FireFactionPower(shard.Location),'Bloom launch')
  end)
  Trigger.AfterDelay(DateTime.Seconds(10),function()
   Check(TestMemories(u)==0,'Restoration consumes target memory')
   Check(#u.GetActorsByType('u_memory_echo')==1,'temporary infantry restored')
   Check(flyer.Health==flyer.MaxHealth,'Earthbreaker excludes aircraft')
   Check(ground.Health<ground.MaxHealth and building.IsDead,'Earthbreaker damages ground and structures')
   Check(quiet.IdentityFirepower==30,'Absolute Silence suppresses weapons and doctrine')
   Check(shard.IdentityArmor==65,'Bloom protects allied combatant')
   for i,s in ipairs(states) do for _,a in ipairs(s.p.GetActorsByType(s.prefix..'_cataclysm')) do a.Kill('DefaultDeath') end end
   Trigger.AfterDelay(25,function() for _,s in ipairs(states) do Check(s.p.FactionPowerCount==0,'power removed with source '..s.prefix) end end)
  end)
  Trigger.AfterDelay(DateTime.Seconds(42),function()
   Check(#u.GetActorsByType('u_memory_echo')==0 and TestMemories(u)==0,'echo expires without recursive memory')
   Check(quiet.IdentityFirepower==100,'suppression expires')
  end)
 end)
end
Tick=function()
 local structures={'generator','barracks','veilworks','motorpool','radar','advpower','service','tech','helipad','kennel','autocannon','missilenest','cataclysm'}
 local units={'rifleman','rocketeer','bulwark','special','air','beast','engineer','harvester','attendant'}
 for _,s in ipairs(states) do
  if DateTime.GameTime%250==0 then print('ADDITIONALREALMS_TEST DETAIL '..s.prefix..' stage='..s.stage..' queued='..tostring(s.queued)..' ready='..tostring(s.stage<=13 and s.p.BuildingReady(s.prefix..'_'..structures[s.stage]))) end
  if s.stage<=13 then
   local kind=s.prefix..'_'..structures[s.stage]
   if #s.p.GetActorsByType(kind)>0 then
    Check(true,'paid building '..kind);s.stage=s.stage+1;s.queued=false
   elseif s.p.BuildingReady(kind) then
    local k=s.stage-1;s.p.PlaceCompletedBuilding(kind,CPos.New(s.x+3+(k%4)*3,5+math.floor(k/4)*4))
   elseif not s.queued then s.queued=s.p.QueueProduction(kind) end
  elseif s.stage==14 then
   local kind=s.prefix..'_'..units[s.count+1]
   local actors=s.p.GetActorsByType(kind)
   if #actors>0 and (units[s.count+1]~='harvester' or #actors>1) then
    Check(true,'paid unit '..kind);actors[#actors].Move(CPos.New(s.x+23,4+s.count));s.count=s.count+1;s.queued=false
    if s.count==(s.prefix=='n' and 9 or 8) then s.stage=15 end
   elseif not s.queued then s.queued=s.p.QueueProduction(kind) end
  end
 end
end
'''
(dest/'additionalrealms-test.lua').write_text(lua)
