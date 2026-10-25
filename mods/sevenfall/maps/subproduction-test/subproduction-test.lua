-- Real MCV deployment, paid queues, validated placement and unit production.
local states, checks, failures, finished = {}, 0, 0, false
local power = { 'a_spire', 'h_generator', 'd_heart' }
local barracks = { 'a_chapel', 'h_barracks', 'd_pit' }
local factory = { 'a_armory', 'h_motorpool', 'd_forge' }
local infantry = { 'a_congregant', 'h_retrieval', 'd_magistrate' }
local armor = { 'a_cantor', 'h_janus', 'd_contemptor' }
local special = { 'a_processional', 'h_containment', 'd_throne' }
local function Check(ok, name)
    if ok then checks = checks + 1; print('SUBPRODUCTION_TEST PASS: ' .. name)
    else failures = failures + 1; print('SUBPRODUCTION_TEST FAIL: ' .. name) end
end
local function Finish()
    if finished then return end
    finished = true
    for i=0,2 do
        local s = states[i]
        Check(s.stage == 9 and s.units == 2, 'complete paid construction, two units and exclusive defense P' .. i)
        Check(s.p.RefinedCredits > 0, 'constructed refinery accepts real deliveries P' .. i)
        Check(s.p.Cash < 20000, 'production spent cash P' .. i)
    end
    if failures == 0 then print('SUBPRODUCTION_TEST COMPLETE checks=' .. checks) end
end
WorldLoaded = function()
    Camera.Position = Map.CenterOfCell(CPos.New(10,10))
    for i = 0, 2 do
        local p = Player.GetPlayer('P' .. i)
        local x, y = 5 + (i % 3) * 38, 5 + math.floor(i / 3) * 34
        local family = i + 1
        local prefix = ({'a', 'h', 'd'})[family]
        p.Cash = 20000
        local mcv = Actor.Create('mcv', true, {Owner=p, Location=CPos.New(x+2,y+2)})
        mcv.Deploy()
        states[i] = {p=p, stage=0, x=x, y=y, family=family, index=i, units=0,
            buildings={power[family], barracks[family], prefix .. '_veilworks', factory[family], prefix .. '_radar', prefix .. '_advpower', special[i+1]},
            locations={CPos.New(x+5,y+1), CPos.New(x+1,y+6), CPos.New(x+4,y+4), CPos.New(x,y-3), CPos.New(x+8,y+1), CPos.New(x+8,y+5), CPos.New(x+5,y+9)}}
    end
    Trigger.AfterDelay(DateTime.Seconds(550), Finish)
end
Tick = function()
    local complete = true
    for i=0,2 do
        local s = states[i]
        if s.stage ~= 9 or s.units ~= 2 or s.p.RefinedCredits == 0 then complete = false end
        if DateTime.GameTime % DateTime.Seconds(30) == 0 then
            print('SUBPRODUCTION_TEST DETAIL: P' .. i .. ' stage=' .. s.stage .. ' units=' .. s.units .. ' queued=' .. tostring(s.queued) .. ' cash=' .. s.p.Cash .. ' ready=' .. tostring(s.stage <= 7 and s.stage > 0 and s.p.BuildingReady(s.buildings[s.stage])))
        end
        if s.stage == 0 and #s.p.GetActorsByType('fact') > 0 then
            Check(true, 'MCV deploys P' .. i)
            s.stage = 1
        end
        if s.stage >= 1 and s.stage <= 7 then
            local kind = s.buildings[s.stage]
            if #s.p.GetActorsByType(kind) > 0 then
                Check(true, 'paid and placed ' .. kind .. ' P' .. i)
                s.stage = s.stage + 1
                s.queued = false
            elseif s.p.BuildingReady(kind) then
                s.p.PlaceCompletedBuilding(kind, s.locations[s.stage])
            elseif not s.queued then
                s.queued = s.p.QueueProduction(kind)
            end
        elseif s.stage == 8 then
            local types = { infantry[s.family], armor[s.family] }
            local kind = types[s.units+1]
            local units = s.p.GetActorsByType(kind)
            if #units > 0 then
                print('SUBPRODUCTION_TEST DETAIL: produced count=' .. #units .. ' type=' .. kind); Check(#units == 1, 'produced ' .. kind .. ' P' .. i)
                s.units = s.units + 1
                units[1].Move(CPos.New(s.x+16,s.y+2+s.units))
                s.queued = false
                if s.units == 2 then s.stage = 9 end
            elseif not s.queued then
                s.queued = s.p.QueueProduction(kind)
            end
        end
    end
    if complete then Finish() end
end
