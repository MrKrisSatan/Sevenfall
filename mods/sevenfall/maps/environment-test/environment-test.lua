-- Native acceptance, not a mock. Run with run_defense_test.py --scenario environment.
local checks, failures = 0, 0
local engineer, rifle, attacker, walker
local function Check(ok, name)
    if ok then checks = checks + 1; print("ENVIRONMENT_TEST PASS: " .. name)
    else failures = failures + 1; print("ENVIRONMENT_TEST FAIL: " .. name) end
end
local function Later(seconds, fn) Trigger.AfterDelay(DateTime.Seconds(seconds), fn) end
WorldLoaded = function()
    local player = Player.GetPlayer("Multi0")
    Camera.Position = Bridge34.CenterPosition
    engineer = Actor.Create("h_engineer", true, {Owner=player, Location=CPos.New(53,30)})
    rifle = Actor.Create("h_rifleman", true, {Owner=player, Location=CPos.New(53,29)})
    House0.Health = 30000
    Later(2, function()
        Check(House0.Owner == player, "nearby infantry claim shelter")
        engineer.InstantlyRepair(House0)
        rifle.EnterTransport(House0)
    end)
    Later(14, function()
        Check(House0.Health == House0.MaxHealth, "engineer repairs surviving house")
        Check(not engineer.IsDead, "house repair preserves engineer")
        Check(House0.PassengerCount == 1, "infantry enters garrison")
        Bridge34.Health = 50000
        engineer.RepairBridge(WestPost34)
    end)
    Later(32, function()
        Check(Bridge34.Health == Bridge34.MaxHealth, "engineer repairs damaged bridge")
        Bridge34.Health = 1
        attacker = Actor.Create("h_rifleman", true, {Owner=player, Location=CPos.New(60,34)})
        attacker.Attack(Bridge34, true, true)
    end)
    Later(40, function()
        Check(Bridge34.IsDead, "forced fire destroys neutral bridge")
        attacker.Stop()
        engineer.RepairBridge(WestPost34)
    end)
    Later(55, function()
        local bridges = Player.GetPlayer("Neutral").GetActorsByType("sf_bridge_ew")
        Check(#bridges == 2, "engineer restores destroyed crossing")
        Check(not engineer.IsDead, "bridge repair preserves engineer")
        walker = Actor.Create("h_rifleman", true, {Owner=player, Location=CPos.New(60,34)})
        walker.Move(CPos.New(67,34))
        House0.Health = 1
        attacker.Move(CPos.New(53,30))
        attacker.Attack(House0, true, true)
    end)
    Later(75, function()
        Check(walker.Location.X > 64, "restored bridge allows ground passage")
        Check(House0.IsDead, "forced fire destroys claimed house")
        Check(not rifle.IsDead and rifle.IsInWorld, "destroyed house ejects garrison")
        if failures == 0 then print("ENVIRONMENT_TEST COMPLETE checks=" .. checks)
        else print("ENVIRONMENT_TEST FAIL: total=" .. failures) end
    end)
end
