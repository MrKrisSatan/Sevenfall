-- Real refinery events and hazard contact, not a replacement for full matches.
local checks, failures = 0, 0
local players, passed = {}, {}
local victim, collector, building
local collectorHP, buildingHP, beforeDensity
local function Check(ok, name)
	if ok then checks = checks + 1; print("RELEASE_TEST PASS: " .. name)
	else failures = failures + 1; print("RELEASE_TEST FAIL: " .. name) end
end
local function Later(seconds, callback) Trigger.AfterDelay(DateTime.Seconds(seconds), callback) end
WorldLoaded = function()
	Camera.Position = Map.CenterOfCell(CPos.New(60,116))
	for i = 0, 8 do
		players[i] = Player.GetPlayer("P" .. i)
		Check(players[i].RefinedCredits == 0, "initial refined total P" .. i)
	end
	beforeDensity = Veilglass.DensityAt(CPos.New(60,116))
	collector = Actor.Create("h_harvester", true, { Owner=players[0], Location=CPos.New(60,116) })
	collector.Stop()
	collectorHP = collector.Health
	Later(1, function()
		Check(collector.Health == collectorHP, "harvester contact does not detonate")
		Check(Veilglass.DensityAt(CPos.New(60,116)) > 0, "harvester contact does not consume entire deposit")
		collector.Destroy()
		building = Actor.Create("h_generator", true, { Owner=players[1], Location=CPos.New(63,116) })
		buildingHP = building.Health
		victim = Actor.Create("h_rifleman", true, { Owner=players[0], Location=CPos.New(61,116) })
	end)
	Later(2, function()
		Check(victim.IsDead, "non-harvester contact triggers lethal infantry damage")
		Check(Veilglass.DensityAt(CPos.New(61,116)) == 0, "triggered cell consumed")
		Check(building.Health < buildingHP, "blast damages nearby structure footprint")
		local spread = 0
		for _, cell in ipairs({CPos.New(64,116), CPos.New(63,118), CPos.New(61,119),
			CPos.New(59,118), CPos.New(58,116), CPos.New(59,114), CPos.New(61,113), CPos.New(63,114)}) do
			-- Only destinations outside the initial 5x5 field count as spreading.
			if cell.X < 58 or cell.X > 62 or cell.Y < 114 or cell.Y > 118 then
				spread = spread + Veilglass.DensityAt(cell)
			end
		end
		Check(spread > 0 and spread <= 6, "blast scatters capped Veilglass onto new cells")
	end)
	Later(180, function()
		for i = 0, 8 do Check(passed[i] == true, "real mining while spending P" .. i) end
		if failures == 0 then print("RELEASE_TEST COMPLETE checks=" .. checks)
		else print("RELEASE_TEST FAIL: total=" .. failures) end
	end)
end
Tick = function()
	for i = 0, 8 do
		if players[i].RefinedCredits >= 900 then passed[i] = true end
		-- Spend accepted income every tick. Polling the stored balance would fail.
		players[i].Resources = 0
		players[i].Cash = 7000
	end
end
