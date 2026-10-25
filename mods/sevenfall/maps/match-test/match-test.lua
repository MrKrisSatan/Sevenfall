-- No production, movement, attack or victory orders are supplied by this script.
local humans, demons, finished
WorldLoaded = function()
    humans, demons = Player.GetPlayer('Humans'), Player.GetPlayer('Demons')
    humans.Cash, demons.Cash = 10000, 10000
    Camera.Position = Map.CenterOfCell(CPos.New(15,15))
    print('MATCH_TEST DETAIL: bots=' .. tostring(humans.IsBot) .. ',' .. tostring(demons.IsBot))
end
Tick = function()
    if DateTime.GameTime % DateTime.Seconds(60) == 0 then
        print('MATCH_TEST DETAIL: time=' .. DateTime.GameTime .. ' human=' .. #humans.GetActors() .. ' demon=' .. #demons.GetActors() .. ' mined=' .. humans.RefinedCredits .. ',' .. demons.RefinedCredits)
    end
    if not finished and DateTime.GameTime > DateTime.Seconds(30) and (humans.HasNoRequiredUnits() or demons.HasNoRequiredUnits()) then
        finished = true
        if humans.RefinedCredits > 0 and demons.RefinedCredits > 0 then
            print('MATCH_TEST PASS: autonomous economy and conquest elimination')
            print('MATCH_TEST COMPLETE checks=1')
        else print('MATCH_TEST FAIL: elimination before economy verified') end
    end
end
