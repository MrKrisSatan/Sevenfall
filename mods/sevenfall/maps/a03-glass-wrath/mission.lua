-- Sevenfall pre-alpha 0.3 / A03: A Glass of Wrath
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
	economyObjective = commander.AddPrimaryObjective("Deploy the MCV, build a_spire and a_veilworks, and refine at least 900 credits of Veilglass.")
	armyObjective = commander.AddPrimaryObjective("Build a_chapel and a_armory; produce a_watcher and a_aegis.")
	assaultObjective = commander.AddPrimaryObjective("Destroy the hostile Construction Yard.")
	optionalObjective = commander.AddSecondaryObjective("Preserve the first a_gatherer and its refinery.")
	lastStoredCredits = commander.Resources
	Media.DisplayMessage("A03: A Glass of Wrath. Establish your Veilglass economy and destroy the enemy command.", "Sevenfall")

	-- Only units really produced after mission start count. The starting
	-- defensive infantry cannot satisfy the combat-production objective.
	Trigger.OnAnyProduction(function(producer, produced, productionType)
		if produced.Owner ~= commander then
			return
		end
		if produced.Type == "a_watcher" then
			sawInfantry = true
		end
		if produced.Type == "a_aegis" then
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
		and Has("fact") and Has("a_spire") and Has("a_veilworks")
		and refinedCredits >= 900 then
		commander.MarkCompletedObjective(economyObjective)
	end

	if not commander.IsObjectiveCompleted(armyObjective)
		and Has("a_chapel") and Has("a_armory")
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
		if Has("a_gatherer") and Has("a_veilworks") then
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
