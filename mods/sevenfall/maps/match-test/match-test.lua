-- Observe normal bot production, combat and conquest; never order an outcome.
local humans,demons,winner,loser,finished
local function Evaluate()
 if finished or not winner or not loser then return end
 finished=true
 if winner==loser then print('MATCH_TEST FAIL: conflicting outcomes');return end
 if humans.RefinedCredits<=0 or demons.RefinedCredits<=0 then
  print('MATCH_TEST FAIL: outcome before both economies mined');return
 end
 print('MATCH_TEST PASS: both autonomous economies harvested and delivered')
 print('MATCH_TEST PASS: real OnPlayerWon and OnPlayerLost callbacks observed')
 print('MATCH_TEST PASS: conquest winner='..winner.InternalName..' loser='..loser.InternalName)
 print('MATCH_TEST READY_FOR_GAME_OVER checks=3')
end
WorldLoaded=function()
 humans,demons=Player.GetPlayer('Humans'),Player.GetPlayer('Demons')
 humans.Cash,demons.Cash=10000,10000
 Camera.Position=Map.CenterOfCell(CPos.New(15,15))
 if not humans.IsBot or not demons.IsBot then print('MATCH_TEST FAIL: both players must be bots') end
 for _,p in ipairs({humans,demons}) do
  Trigger.OnPlayerWon(p,function(player) winner=player;Evaluate() end)
  Trigger.OnPlayerLost(p,function(player) loser=player;Evaluate() end)
 end
end
Tick=function()
 if DateTime.GameTime%DateTime.Seconds(60)==0 then
  print('MATCH_TEST DETAIL: time='..DateTime.GameTime..' human='..#humans.GetActors()..' demon='..#demons.GetActors()..' mined='..humans.RefinedCredits..','..demons.RefinedCredits)
 end
end
