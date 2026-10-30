local checks, failures=0,0
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
 Trigger.AfterDelay(DateTime.Seconds(45),function()
  for i,a in ipairs(airtargets) do Check(a.IsDead or a.Health<a.MaxHealth,'aircraft damages ground target '..air[i]) end
  if failures==0 then print('REALMCOMPLETION_TEST COMPLETE checks='..checks) end
 end)
end
