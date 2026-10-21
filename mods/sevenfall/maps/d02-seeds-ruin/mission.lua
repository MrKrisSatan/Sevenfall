-- Sevenfall pre-alpha 0.3 / D02: Seeds of Ruin
-- This map requires actual mining, original faction buildings and combat.
-- All gameplay outcomes need manual verification on the pinned OpenRA engine.
local commander
local enemy
local economyObjective
local armyObjective
local assaultObjective
local optionalObjective
local refinedCredits = 0
local lastStoredCredits = 0
local sawInfantry = false
local sawArmour = false
local winOrLoss = false

local function Has(type)
	return #commander.GetActorsByType(type) > 0
end

WorldLoaded = function()
	commander = Player.GetPlayer("Commander")
	enemy = Player.GetPlayer("Enemy")
	commander.Cash = 7000
	Camera.Position = Map.CenterOfCell(CPos.New(19, 19))
	economyObjective = commander.AddPrimaryObjective("Deploy the MCV, build d_heart and d_veilworks, and refine at least 900 credits of Veilglass.")
	armyObjective = commander.AddPrimaryObjective("Build d_pit and d_forge; produce d_thrall and d_ravager.")
	assaultObjective = commander.AddPrimaryObjective("Destroy the hostile Construction Yard.")
	optionalObjective = commander.AddSecondaryObjective("Preserve the first d_devourer and its refinery.")
	lastStoredCredits = commander.Resources
	Media.DisplayMessage("D02: Seeds of Ruin. Establish your Veilglass economy and destroy the enemy command.", "Sevenfall")

	-- Only units really produced after mission start count. The starting
	-- defensive infantry cannot satisfy the combat-production objective.
	Trigger.OnAnyProduction(function(producer, produced, productionType)
		if produced.Owner ~= commander then
			return
		end
		if produced.Type == "d_thrall" then
			sawInfantry = true
		end
		if produced.Type == "d_ravager" then
			sawArmour = true
		end
	end)
	Trigger.OnKilled(Map.NamedActor("CommanderMcv"), function()
		-- Do not fail if this actor was deployed into a construction yard.
		-- The tick loop checks if there is any surviving command facility.
	end)
end

Tick = function()
	if winOrLoss or DateTime.GameTime % 25 ~= 0 then
		return
	end

	local stored = commander.Resources
	if stored > lastStoredCredits then
		refinedCredits = refinedCredits + (stored - lastStoredCredits)
	end
	lastStoredCredits = stored

	if not commander.IsObjectiveCompleted(economyObjective)
		and Has("fact") and Has("d_heart") and Has("d_veilworks")
		and refinedCredits >= 900 then
		commander.MarkCompletedObjective(economyObjective)
	end

	if not commander.IsObjectiveCompleted(armyObjective)
		and Has("d_pit") and Has("d_forge")
		and sawInfantry and sawArmour then
		commander.MarkCompletedObjective(armyObjective)
	end

	if not commander.IsObjectiveCompleted(assaultObjective)
		and #enemy.GetActorsByType("fact") == 0 then
		commander.MarkCompletedObjective(assaultObjective)
	end

	if commander.IsObjectiveCompleted(economyObjective)
		and commander.IsObjectiveCompleted(armyObjective)
		and commander.IsObjectiveCompleted(assaultObjective) then
		winOrLoss = true
		if Has("d_devourer") and Has("d_veilworks") then
			commander.MarkCompletedObjective(optionalObjective)
		else
			commander.MarkFailedObjective(optionalObjective)
		end
	end

	-- Deployment replaces the starting MCV with a FACT; only fail if BOTH
	-- forms of command have vanished. A player without a yard or MCV
	-- cannot complete the building objectives.
	if not winOrLoss and not Has("fact") and not Has("mcv") then
		winOrLoss = true
		commander.MarkFailedObjective(assaultObjective)
	end
end
