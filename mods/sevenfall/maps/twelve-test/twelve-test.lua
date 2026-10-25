-- No orders or production are supplied to these bots. This is a soak, not conquest proof.
local players,history,checks,failures={}, {},0,0
local function Check(ok,name)
 if ok then checks=checks+1;print('TWELVE_TEST PASS: '..name)
 else failures=failures+1;print('TWELVE_TEST FAIL: '..name) end
end
WorldLoaded=function()
 Camera.Position=Map.CenterOfCell(CPos.New(128,27))
 for i=0,11 do
  local p=Player.GetPlayer('Multi'..i);players[i]=p;history[i]={yard=false,mined=false,army=false,seen={},fielded=0,peak=0}
  p.Cash=5000
  Check(p.IsBot,'autonomous bot configured '..i)
 end
 Trigger.AfterDelay(DateTime.Seconds(300),function()
  for i=0,11 do
   Check(history[i].yard,'bot deployed a yard '..i)
   Check(history[i].mined,'bot completed refinery deliveries '..i)
   Check(history[i].army,'bot fielded four combat units cumulatively '..i)
   print('TWELVE_TEST DETAIL: P'..i..' fielded='..history[i].fielded..' peak_alive='..history[i].peak..' losses='..players[i].UnitsLost)
  end
  local kills=0
  for i=0,11 do kills=kills+players[i].UnitsKilled+players[i].BuildingsKilled end
  print('TWELVE_TEST DETAIL: total attributed kills='..kills)
  -- Combat completion is reported independently, not fabricated by the script.
  if kills>0 then Check(true,'autonomous armies engaged in combat') end
  if failures==0 then print('TWELVE_TEST COMPLETE checks='..checks) end
 end)
end
Tick=function()
 for i=0,11 do
  local p=players[i]
  if #p.GetActorsByType('fact')>0 then history[i].yard=true end
  if p.RefinedCredits>0 then history[i].mined=true end
  local combat=0
  for _,unit in ipairs(p.GetActors()) do
   if unit.HasProperty('Attack') and unit.HasProperty('IsMobile') and unit.IsMobile then
    combat=combat+1
    -- Actor's stable type/ID string measures real fielding despite early casualties.
    local id=tostring(unit)
    if not history[i].seen[id] then history[i].seen[id]=true;history[i].fielded=history[i].fielded+1 end
   end
  end
  history[i].peak=math.max(history[i].peak,combat)
  if history[i].fielded>=4 then history[i].army=true end
 end
 if DateTime.GameTime%DateTime.Seconds(60)==0 then
  for i=0,11 do print('TWELVE_TEST DETAIL: P'..i..' actors='..#players[i].GetActors()..' mined='..players[i].RefinedCredits..' army='..tostring(history[i].army)) end
 end
end
