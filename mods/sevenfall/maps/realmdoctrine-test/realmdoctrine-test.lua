local checks, failures = 0, 0
local actors, players, relays = {}, {}, {}
local function Check(ok, name)
 if ok then checks=checks+1; print('REALMDOCTRINE_TEST PASS: '..name)
 else failures=failures+1; print('REALMDOCTRINE_TEST FAIL: '..name) end
end
WorldLoaded=function()
 local kinds={'i_ghost','i_endurer','i_thread','i_savant','f_regent','f_canticle','f_flayer','f_pinions'}
 for i=1,8 do
  players[i]=Player.GetPlayer('P'..(i-1))
  actors[i]=Actor.Create(kinds[i],true,{Owner=players[i],Location=CPos.New(115,8+i*12)})
  actors[i].Stop()
 end
 Trigger.AfterDelay(DateTime.Seconds(5),function()
  local expected={'sf-focus','sf-machine-iron','none','none','sf-fallen-throne','none','none','sf-fallen-wings'}
  for i=1,8 do Check(actors[i].ActiveIdentity==expected[i], 'initial doctrine '..kinds[i]..' got '..actors[i].ActiveIdentity) end
  Check(actors[2].IdentityArmor==80,'Iron damage reduction')
  Check(actors[5].IdentityArmor==70,'Throne damage reduction')
  relays[3]=Actor.Create('i_relay',true,{Owner=players[3],Location=actors[3].Location+CVec.New(2,0)})
  relays[6]=Actor.Create('f_lamentor',true,{Owner=players[6],Location=actors[6].Location+CVec.New(2,0)})
  relays[8]=Actor.Create('f_pinions',true,{Owner=players[8],Location=actors[8].Location+CVec.New(2,0)})
  actors[4].IdentityDamage(actors[4],3000)
  actors[7].IdentityDamage(actors[7],6000)
  Trigger.AfterDelay(DateTime.Seconds(1),function()
   Check(actors[3].ActiveIdentity=='sf-machine-grid','Grid relay activates network')
   Check(actors[6].ActiveIdentity=='sf-fallen-choir','Lamentor activates hymn')
   Check(actors[4].ActiveIdentity=='sf-machine-paradox','wounded Paradox activates')
   Check(actors[7].ActiveIdentity=='sf-fallen-scars','wounded Testament activates')
   Check(actors[8].ActiveIdentity=='none','nearby combat ally cancels isolation')
   Check(actors[3].IdentityArmor==90,'Grid network armor is applied')
   Check(actors[6].IdentityArmor==110,'Choir vulnerability tradeoff is applied')
   Check(actors[4].IdentitySpeed==130,'Paradox escape speed is applied')
   for _,i in ipairs({3,6,8}) do relays[i].Destroy() end
   Trigger.AfterDelay(DateTime.Seconds(1),function()
    Check(actors[3].ActiveIdentity=='none','lost relay removes network')
    Check(actors[6].ActiveIdentity=='none','lost Lamentor removes hymn')
    Check(actors[8].ActiveIdentity=='sf-fallen-wings','isolation returns after ally removal')
    Check(actors[3].IdentityArmor==100,'network modifier expires')
    Check(actors[6].IdentityArmor==100,'hymn modifier expires')
    local harv=Actor.Create('i_harvester',true,{Owner=players[2],Location=CPos.New(120,5)})
    Check(harv.ActiveIdentity=='none','collector excluded from combat doctrine')
    if failures==0 then print('REALMDOCTRINE_TEST COMPLETE checks='..checks) end
   end)
  end)
 end)
end
