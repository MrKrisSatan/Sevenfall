-- Native defense-extension acceptance. Uses real actors, ownership, power and cargo.
local actors = {}
local function A(name)
	if not actors[name] then actors[name] = Map.NamedActor(name) end
	return actors[name]
end
local checks, failures = 0, 0
local function Check(ok, name)
	if not ok then failures = failures + 1; print("DEFENSE_TEST FAIL: " .. name); return end
	checks = checks + 1
	print("DEFENSE_TEST PASS: " .. name)
end
local function Later(seconds, callback) Trigger.AfterDelay(DateTime.Seconds(seconds), callback) end
local humans, demons, victims, ally, air = nil, nil, nil, nil, {}
local gunHealth
WorldLoaded = function()
	humans = Player.GetPlayer("Humans")
	demons = Player.GetPlayer("Demons")
	victims = Player.GetPlayer("Victims")
	Camera.Position = Map.CenterOfCell(CPos.New(35, 25))
	for _, name in ipairs({"HumanPower","VictimPower","SilentPower","DarkPower","ConvertWall","OverlapWall","OpposingWall","ConvertVictim","WardWall","Ward","WardVictim","RetreatWall","RetreatVictim","VehicleWall","VehicleVictim","DestroyedWall","DestroyedVictim","SilentWall","SilentVictim","LightWall","LightVictim","LightTankWall","LightTank","DarkWall","DarkVictim","WireWalker","WireControl","CrushWire","Crusher","BlastWall","BlockedTank","ThornWalker","ThornControl","HumanGun","GunTarget","Bunker","BunkerTarget","AngelGun","AngelGunTarget","AngelLance","LanceTarget","Spines","SpineTarget","Maw","MawTarget","AngelAA","HumanAA","DemonAA","AAGroundTarget","Wire","Thorn"}) do A(name) end
	print("DEFENSE_TEST START")
	A("WardVictim").Health = 2500
	A("ConvertWall").Health = 18000
	for _, name in ipairs({"WireWalker", "WireControl", "ThornWalker", "ThornControl", "Crusher", "BlockedTank", "LightVictim", "LightTank"}) do A(name).Stop() end
	A("WireWalker").Move(CPos.New(19,50)); A("WireControl").Move(CPos.New(19,53))
	A("ThornWalker").Move(CPos.New(49,50)); A("ThornControl").Move(CPos.New(49,53))
	A("Crusher").Move(CPos.New(11,55)); A("BlockedTank").Move(CPos.New(29,55))
	A("LightVictim").Move(CPos.New(57,35)); A("LightTank").Move(CPos.New(57,38))
	for _, x in ipairs({18,43,73}) do
		local plane = Actor.Create("sf_defense_airtarget", true, {Owner=victims, Location=CPos.New(x,80)})
		plane.Move(CPos.New(x,81))
		table.insert(air, plane)
	end
	Later(1, function() A("DarkPower").Kill("DefaultDeath") end)
	Later(2, function() A("DarkVictim").Stop(); A("DarkVictim").Move(CPos.New(77,35)) end)
	Later(3, function()
		ally = Actor.Create("h_rifleman", true, {Owner=humans, Location=CPos.New(53,35)})
		ally.Move(CPos.New(57,35))
	end)
	Later(4, function()
		Check(A("WireWalker").Location.X < A("WireControl").Location.X, "razorwire slows enemy infantry")
		Check(A("WireWalker").Health < A("WireWalker").MaxHealth, "razorwire damages crossing infantry")
		Check(A("ThornWalker").Location.X < A("ThornControl").Location.X, "living thorns slow enemy infantry")
		Check(A("ThornWalker").Health < A("ThornWalker").MaxHealth, "living thorns damage crossing infantry")
	end)
	Later(6, function()
		A("RetreatVictim").Stop(); A("RetreatVictim").Move(CPos.New(63,15))
		A("DestroyedWall").Kill("DefaultDeath")
		A("SilentPower").Kill("DefaultDeath")
		Check(A("ConvertVictim").Owner == victims, "overlapping flesh walls do not convert early")
		Check(A("BunkerTarget").Health == A("BunkerTarget").MaxHealth, "empty entrenchment cannot shoot")
		Check(A("CrushWire").IsDead and not A("Crusher").IsDead, "hostile vehicles crush razorwire")
		Check(not A("BlastWall").IsDead and A("BlockedTank").Location ~= CPos.New(29,55), "concrete wall blocks ordinary tracked vehicles")
	end)
	Later(8, function()
		Check(A("LightVictim").IsDead, "powered light wall incinerates enemy infantry")
		Check(A("LightTank").IsDead, "powered light wall incinerates crossing armor")
		Check(ally and not ally.IsDead and ally.Location.X >= 57, "allied infantry can cross friendly light")
		print("DEFENSE_TEST DARK dead=" .. tostring(A("DarkVictim").IsDead) .. " x=" .. tostring(A("DarkVictim").Location.X))
		Check(not A("DarkVictim").IsDead and A("DarkVictim").Location.X >= 77, "power cut opens safe passage through hostile light")
		for i=1,3 do
			local passenger = Actor.Create("h_rifleman", true, {Owner=humans, Location=CPos.New(74,54+i)})
			passenger.Stance = "HoldFire"
			passenger.EnterTransport(A("Bunker"))
		end
	end)
	Later(10, function()
		gunHealth = A("GunTarget").Health
		A("HumanPower").Kill("DefaultDeath")
		A("HumanGun").Stop(); A("HumanGun").Attack(A("GunTarget"))
	end)
	Later(14, function()
		Check(A("ConvertVictim").Owner == demons, "sustained moaning converts enemy infantry")
		Check(A("WardVictim").Owner == humans, "sanctuary prevents conversion")
		Check(A("WardVictim").Health > 2500, "sanctuary heals allied infantry")
		Check(A("RetreatVictim").Owner == victims and A("RetreatVictim").Location.X >= 62, "retreat escapes conversion")
		Check(A("VehicleVictim").Owner == victims, "vehicles are immune to insanity")
		Check(A("DestroyedVictim").Owner == victims, "destroying flesh wall stops its influence")
		Check(A("SilentVictim").Owner == victims, "power cut silences flesh-wall conversion")
		print("DEFENSE_TEST HEALTH flesh=" .. tostring(A("ConvertWall").Health) .. " gun=" .. tostring(A("GunTarget").Health) .. " before=" .. tostring(gunHealth))
		Check(A("ConvertWall").Health > 18000, "living flesh regenerates after damage cooldown")
		Check(A("GunTarget").Health < gunHealth, "human autocannon fires through power loss")
		Check(A("Bunker").PassengerCount == 3, "entrenchment accepts three infantry")
		Check(A("BunkerTarget").Health < A("BunkerTarget").MaxHealth, "garrisoned infantry fire from entrenchment")
		for _, name in ipairs({"AngelGunTarget", "LanceTarget", "SpineTarget", "MawTarget"}) do
			Check(A(name).Health < A(name).MaxHealth, "defense damages " .. name)
		end
		for i, plane in ipairs(air) do Check(plane.Health < plane.MaxHealth, "anti-air defense " .. i .. " hits aircraft") end
		Check(A("AAGroundTarget").Health == A("AAGroundTarget").MaxHealth, "dedicated anti-air ignores ground armor")
		if failures == 0 then print("DEFENSE_TEST PRIMARY_CASES_PASS checks=" .. checks) end
	end)
	Later(35, function() Check(A("ConvertVictim").Owner == demons, "recent converts resist immediate reconversion") end)
	Later(58, function()
		Check(A("ConvertVictim").Owner == victims, "conversion immunity expires and opposing influence works")
		if failures == 0 and checks == 33 then print("DEFENSE_TEST COMPLETE checks=" .. checks) end
	end)
end
