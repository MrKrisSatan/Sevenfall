local checks,failures=0,0
local shooter,lateTarget
local player,infantry,tank,miner,violated,expected = nil,nil,nil,nil,false,{}
local function Check(ok,name)
 if ok then checks=checks+1;print('TERRAIN_TEST PASS: '..name)
 else failures=failures+1;print('TERRAIN_TEST FAIL: '..name) end
end
WorldLoaded=function()
 Check(GraphicsCheck.EmptySheetReadback(),'empty map-preview sheet initializes before GPU readback')
 Check(GraphicsCheck.PixelRoundTrip(),'GPU texture readback preserves uploaded pixels')
 player=Player.GetPlayer('Tester');Camera.Position=Map.CenterOfCell(CPos.New(114,20))
 infantry=Actor.Create('h_rifleman',true,{Owner=player,Location=CPos.New(114,17)})
 tank=Actor.Create('h_bulwark',true,{Owner=player,Location=CPos.New(114,19)})
 miner=Actor.Create('h_harvester',true,{Owner=player,Location=CPos.New(114,21)})
 miner.Stop()
 shooter=Actor.Create('sf_late_shooter',true,{Owner=player,Location=CPos.New(103,20)})
 lateTarget=Actor.Create('sf_late_target',true,{Owner=player,Location=CPos.New(103,17)})
 Trigger.AfterDelay(DateTime.Seconds(1),function()shooter.Attack(lateTarget,false,true) end)
 Trigger.AfterDelay(DateTime.Seconds(2),function()shooter.Kill() end)
 Trigger.AfterDelay(DateTime.Seconds(3),function()Check(not shooter.IsInWorld,'delayed projectile source has been removed') end)
 Trigger.AfterDelay(DateTime.Seconds(14),function()Check(lateTarget.Health<lateTarget.MaxHealth,'projectile still damages target after source disposal without crashing') end)
 Check(Map.TerrainType(CPos.New(112,17))=='Rock','cliff template is impassable Rock')
 for _,unit in ipairs({infantry,tank,miner}) do
  Check(not unit.CanEnterTerrainCell(CPos.New(112,17)),'locomotor cannot enter a cliff')
  Check(unit.CanEnterTerrainCell(CPos.New(112,27)),'locomotor can use an open terrace gate')
 end
 infantry.Move(CPos.New(110,17));tank.Move(CPos.New(110,19));miner.Move(CPos.New(110,21))
 for _,cell in ipairs({CPos.New(128,27),CPos.New(178,40),CPos.New(215,78),CPos.New(229,128),CPos.New(216,178),CPos.New(178,215),CPos.New(128,229),CPos.New(78,216),CPos.New(41,178),CPos.New(27,128),CPos.New(40,78),CPos.New(78,41)}) do
  local mcv=Actor.Create('mcv',true,{Owner=player,Location=cell});mcv.Deploy();table.insert(expected,cell)
 end
 Trigger.AfterDelay(DateTime.Seconds(8),function()
  Check(#player.GetActorsByType('fact')==12,'all twelve start cells support MCV deployment')
  for i,cell in ipairs(expected) do
   local found=false
   for _,yard in ipairs(player.GetActorsByType('fact')) do
    if yard.Location==cell or (yard.Location.X>=cell.X-2 and yard.Location.X<=cell.X+2 and yard.Location.Y>=cell.Y-2 and yard.Location.Y<=cell.Y+2) then found=true end
   end
   Check(found,'deployed construction yard at start '..i)
  end
 end)
 Trigger.AfterDelay(DateTime.Seconds(28),function()
  Check(infantry.Location==CPos.New(110,17),'infantry routes around the cliff through a gate')
  Check(tank.Location==CPos.New(110,19),'tracked armor routes around the cliff')
  Check(miner.Location==CPos.New(110,21),'harvester routes around the cliff')
  Check(not violated,'no moving test actor crossed a cliff cell')
  Check(#Map.ActorsInWorld>50,'environment props and bridges load in native map')
  if failures==0 then print('TERRAIN_TEST COMPLETE checks='..checks) end
 end)
end
Tick=function()
 if infantry then
  for _,unit in ipairs({infantry,tank,miner}) do
   if not unit.IsDead and Map.TerrainType(unit.Location)=='Rock' then violated=true end
  end
 end
end
