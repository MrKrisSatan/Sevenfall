-- Sevenfall pre-alpha 0.3 / H03: The Glass Fields
-- This map requires actual mining, original faction buildings and combat.
-- All gameplay outcomes need manual verification on the pinned OpenRA engine.
local commander
local enemy
local economyObjective
local armyObjective
local assaultObjective
local optionalObjective
local refinedCredits = 0
local startingRefinedCredits = 0
local sawInfantry = false
local sawArmour = false
local winOrLoss = false
local firstRefinery
local firstHarvester
local preservationFailed = false

local function Has(type)
	return #commander.GetActorsByType(type) > 0
end

-- Keep actor identities: replacements must not restore this bonus. Removal
-- covers selling as well as destruction; capture fails even if recaptured.
local function FailPreservation()
	if winOrLoss or preservationFailed then
		return
	end
	preservationFailed = true
	commander.MarkFailedObjective(optionalObjective)
end

local function TrackFirst(type)
	local actor = commander.GetActorsByType(type)[1]
	if actor then
		Trigger.OnKilledOrCaptured(actor, FailPreservation)
		Trigger.OnRemovedFromWorld(actor, FailPreservation)
	end
	return actor
end

WorldLoaded = function()
	commander = Player.GetPlayer("Commander")
	enemy = Player.GetPlayer("Enemy")
	commander.Cash = 7000
	Camera.Position = Map.CenterOfCell(CPos.New(19, 19))
	economyObjective = commander.AddPrimaryObjective("Deploy the MCV, build h_generator and h_veilworks, and refine at least 900 credits of Veilglass.")
	armyObjective = commander.AddPrimaryObjective("Build h_barracks and h_motorpool; produce h_rifleman and h_bulwark.")
	assaultObjective = commander.AddPrimaryObjective("Destroy the hostile Construction Yard.")
	optionalObjective = commander.AddSecondaryObjective("Preserve the first h_harvester and its refinery.")
	startingRefinedCredits = commander.RefinedCredits
	Media.DisplayMessage("H03: The Glass Fields. Establish your Veilglass economy and destroy the enemy command.", "Sevenfall")

	-- Only units really produced after mission start count. The starting
	-- defensive infantry cannot satisfy the combat-production objective.
	Trigger.OnAnyProduction(function(producer, produced, productionType)
		if produced.Owner ~= commander then
			return
		end
		if produced.Type == "h_rifleman" then
			sawInfantry = true
		end
		if produced.Type == "h_bulwark" then
			sawArmour = true
		end
	end)
end

Tick = function()
	if winOrLoss then
		return
	end

	-- Inspect new economy actors every tick, including refinery FreeActor miners
	-- which do not pass through OnAnyProduction.
	if not firstRefinery then
		firstRefinery = TrackFirst("h_veilworks")
	end
	if not firstHarvester then
		firstHarvester = TrackFirst("h_harvester")
	end

	-- Defeat takes priority over completing the final objective on this tick.
	-- Deploying replaces the MCV with FACT, so either command actor suffices.
	if not Has("fact") and not Has("mcv") then
		commander.MarkFailedObjective(assaultObjective)
		winOrLoss = true
		return
	end

	if DateTime.GameTime % 25 ~= 0 then
		return
	end

	-- Count actual accepted unloads, even when income is spent between polls.
	refinedCredits = commander.RefinedCredits - startingRefinedCredits

	local economyReady = commander.IsObjectiveCompleted(economyObjective)
		or (Has("fact") and Has("h_generator") and Has("h_veilworks") and refinedCredits >= 900)
	local armyReady = commander.IsObjectiveCompleted(armyObjective)
		or (Has("h_barracks") and Has("h_motorpool") and sawInfantry and sawArmour)
	local assaultReady = commander.IsObjectiveCompleted(assaultObjective)
		or #enemy.GetActorsByType("fact") == 0

	-- Resolve the bonus before the final primary objective awards victory.
	if economyReady and armyReady and assaultReady then
		if not preservationFailed and firstRefinery and firstHarvester then
			commander.MarkCompletedObjective(optionalObjective)
		else
			FailPreservation()
		end
	end

	if economyReady then
		commander.MarkCompletedObjective(economyObjective)
	end
	if armyReady then
		commander.MarkCompletedObjective(armyObjective)
	end
	if assaultReady then
		commander.MarkCompletedObjective(assaultObjective)
	end

	if commander.IsObjectiveCompleted(economyObjective)
		and commander.IsObjectiveCompleted(armyObjective)
		and commander.IsObjectiveCompleted(assaultObjective) then
		winOrLoss = true
	end
end
