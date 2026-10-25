local checks=0
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
