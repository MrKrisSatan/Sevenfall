local types={'sf_a_seraph_ultimate','sf_a_warden_ultimate','sf_a_exile_ultimate','sf_a_desolation_ultimate','sf_h_bastion_ultimate','sf_h_union_ultimate','sf_h_covenant_ultimate','sf_h_area52_ultimate','sf_d_legion_ultimate','sf_d_brood_ultimate','sf_d_court_ultimate','sf_d_contempt_ultimate','h_cataclysm','a_cataclysm','d_cataclysm','i_cataclysm','f_cataclysm'}
local players,sources,plants,remaining={},{},{},{}
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
