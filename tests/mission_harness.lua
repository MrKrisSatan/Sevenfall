-- Small OpenRA API double, not an engine or gameplay simulator. Objective
-- transitions follow the pinned MissionObjectives.cs (including final victory).
actors = {}
events = {}
production = nil
local function NewPlayer()
	local player = { Resources = 0, Cash = 0, objectives = {}, result = nil }
	player.GetActorsByType = function(type)
		local found = {}
		for _, actor in ipairs(actors) do
			if actor.Type == type and actor.Owner == player and not actor.IsDead and actor.IsInWorld then
				table.insert(found, actor)
			end
		end
		return found
	end
	local function Add(description, required)
		table.insert(player.objectives, { state = 'incomplete', required = required })
		return #player.objectives
	end
	player.AddPrimaryObjective = function(description) return Add(description, true) end
	player.AddSecondaryObjective = function(description) return Add(description, false) end
	player.IsObjectiveCompleted = function(id) return player.objectives[id].state == 'completed' end
	player.MarkCompletedObjective = function(id)
		local objective = player.objectives[id]
		if objective.state ~= 'incomplete' then return end
		objective.state = 'completed'
		table.insert(events, 'completed:' .. id)
		if objective.required then
			for _, other in ipairs(player.objectives) do
				if other.required and other.state ~= 'completed' then return end
			end
			player.result = 'won'
			table.insert(events, 'won')
		end
	end
	player.MarkFailedObjective = function(id)
		local objective = player.objectives[id]
		if objective.state == 'failed' then return end
		objective.state = 'failed'
		table.insert(events, 'failed:' .. id)
		if objective.required then player.result = 'lost' end
	end
	return player
end
commander = NewPlayer()
enemy = NewPlayer()
Player = { GetPlayer = function(name) return name == 'Commander' and commander or enemy end }
Camera = {}
CPos = { New = function(x, y) return {x, y} end }
Map = { CenterOfCell = function(cell) return cell end }
Media = { DisplayMessage = function() end }
DateTime = { GameTime = 0 }
Trigger = {
	OnAnyProduction = function(callback) production = callback end,
	OnKilledOrCaptured = function(actor, callback) actor.lost = callback end,
	OnRemovedFromWorld = function(actor, callback) actor.removed = callback end
}
AddActor = function(type, owner)
	local actor = { Type = type, Owner = owner or commander, IsDead = false, IsInWorld = true }
	table.insert(actors, actor)
	return actor
end
LoseActor = function(actor, reason)
	if reason == 'capture' then actor.Owner = enemy
	elseif reason == 'kill' then actor.IsDead = true
	else actor.IsInWorld = false end
	local callback = reason == 'remove' and actor.removed or actor.lost
	if callback then callback() end
end
