-- Real MCV deployment, paid queues, validated placement and unit production.
local states, checks, failures, finished = {}, 0, 0, false
local power = { 'i_generator', 'f_spire' }
local barracks = { 'i_barracks', 'f_chapel' }
local factory = { 'i_motorpool', 'f_armory' }
local infantry = { 'i_rifleman', 'f_watcher' }
local armor = { 'i_bulwark', 'f_aegis' }
local special = { {'i_ghost', 'i_lance'}, {'i_endurer', 'i_crucible'}, {'i_thread', 'i_relay'}, {'i_savant', 'i_gambit'}, {'f_regent', 'f_reliquary'}, {'f_canticle', 'f_lamentor'}, {'f_flayer', 'f_martyr'}, {'f_pinions', 'f_harrow'} }
local function Check(ok, name)
    if ok then checks = checks + 1; print('NEWREALMS_TEST PASS: ' .. name)
    else failures = failures + 1; print('NEWREALMS_TEST FAIL: ' .. name) end
end
local function Finish()
    if finished then return end
    finished = true
    for i=0,7 do
        local s = states[i]
        Check(s.stage == 6 and s.units == 4, 'complete paid construction and shared infantry/armor and both exclusive units P' .. i)
        Check(s.p.RefinedCredits > 0, 'constructed refinery accepts real deliveries P' .. i)
        Check(s.p.Cash < 20000, 'production spent cash P' .. i)
    end
    if failures == 0 then print('NEWREALMS_TEST COMPLETE checks=' .. checks) end
end
WorldLoaded = function()
    Camera.Position = Map.CenterOfCell(CPos.New(10,10))
    for i = 0, 7 do
        local p = Player.GetPlayer('P' .. i)
        local x, y = 5 + (i % 3) * 38, 5 + math.floor(i / 3) * 34
        local family = math.floor(i / 4) + 1
        local prefix = ({'i', 'f'})[family]
        p.Cash = 20000
        local mcv = Actor.Create('mcv', true, {Owner=p, Location=CPos.New(x+2,y+2)})
        mcv.Deploy()
        states[i] = {p=p, stage=0, x=x, y=y, family=family, index=i, units=0,
            buildings={power[family], barracks[family], prefix .. '_veilworks', factory[family]},
            locations={CPos.New(x+5,y+1), CPos.New(x+1,y+6), CPos.New(x+4,y+4), CPos.New(x,y-3)}}
    end
    Trigger.AfterDelay(DateTime.Seconds(550), Finish)
end
Tick = function()
    local complete = true
    for i=0,7 do
        local s = states[i]
        if s.stage ~= 6 or s.units ~= 4 or s.p.RefinedCredits == 0 then complete = false end
        if DateTime.GameTime % DateTime.Seconds(30) == 0 then
            print('NEWREALMS_TEST DETAIL: P' .. i .. ' stage=' .. s.stage .. ' units=' .. s.units .. ' queued=' .. tostring(s.queued) .. ' cash=' .. s.p.Cash .. ' ready=' .. tostring(s.stage <= 4 and s.stage > 0 and s.p.BuildingReady(s.buildings[s.stage])))
        end
        if s.stage == 0 and #s.p.GetActorsByType('fact') > 0 then
            Check(true, 'MCV deploys P' .. i)
            s.stage = 1
        end
        if s.stage >= 1 and s.stage <= 4 then
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
        elseif s.stage == 5 then
            local types = { infantry[s.family], armor[s.family], special[i+1][1], special[i+1][2] }
            local kind = types[s.units+1]
            local units = s.p.GetActorsByType(kind)
            if #units > 0 then
                Check(#units == 1, 'produced ' .. kind .. ' P' .. i)
                s.units = s.units + 1
                units[1].Move(CPos.New(s.x+16,s.y+2+s.units))
                s.queued = false
                if s.units == 4 then s.stage = 6 end
            elseif not s.queued then
                s.queued = s.p.QueueProduction(kind)
            end
        end
    end
    if complete then Finish() end
end
