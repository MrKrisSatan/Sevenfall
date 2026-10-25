"""Generate an explicit developer-only animation and damage exercise map.

This is an engine/rendering diagnostic, not a campaign playability test.
"""
from pathlib import Path
import json
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / 'mods/sevenfall'


def main():
    target = MOD / 'maps/animation-test'
    target.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(MOD / 'maps/building-gallery/map.bin', target / 'map.bin')
    base = (MOD / 'maps/unit-gallery/map.yaml').read_text(encoding='utf-8')
    header = base.split('Actors:\n', 1)[0].replace('Title: Sevenfall Unit Gallery', 'Title: Sevenfall Animation Diagnostic')
    units = re.findall(r'^\tUnit([ahd])(\d+): (\w+)$', base, re.M)
    buildings = json.loads((ROOT / 'art/building-catalog.json').read_text(encoding='utf-8'))
    names = []
    text = header + 'Actors:\n\tSpawn0: mpspawn\n\t\tOwner: Neutral\n\t\tLocation: 48,35\n'
    for side, x, owner in [('a', 14, 'HostA'), ('h', 44, 'Multi0'), ('d', 74, 'HostD')]:
        for faction, index, actor in units:
            if faction != side:
                continue
            name = 'Unit' + side + index
            names.append(name)
            text += f'\t{name}: {actor}\n\t\tOwner: {owner}\n\t\tLocation: {x},{10 + int(index)*3}\n\t\tFacing: 384\n'
            text += f'\tTarget{side}{index}: sf_animation_target\n\t\tOwner: Neutral\n\t\tLocation: {x+7},{10 + int(index)*3}\n'
        roster = [f'{side}_yard', f'{side}_' + {'a': 'spire', 'h': 'generator', 'd': 'heart'}[side], f'{side}_veilworks']
        roster += [b['name'].replace('-', '_') for b in buildings if b['name'].startswith(side + '-')]
        for index, image in enumerate(roster):
            actor = 'fact' if image.endswith('_yard') else image
            y = 77 if image.endswith('_naval') else 42 + (index // 2)*5
            x2 = x - 5 + (index % 2)*10
            text += f'\tBuilding{side}{index}: {actor}\n\t\tOwner: {owner}\n\t\tLocation: {x2},{y}\n'
    text += '''Rules:
	World:
		-SpawnStartingUnits:
		LuaScript:
			Scripts: animation-test.lua
	Player:
		-ConquestVictoryConditions:
		Shroud:
			FogCheckboxEnabled: False
			FogCheckboxLocked: True
			ExploredMapCheckboxEnabled: True
			ExploredMapCheckboxLocked: True
	sf_animation_target:
		Inherits: H_GENERATOR
		-Buildable:
		-Selectable:
		-Targetable:
		Interactable:
		Health:
			HP: 100000000
		Targetable@ANIMATION:
			TargetTypes: GroundActor, Structure
	A_VEILWORKS:
		-FreeActor:
	H_VEILWORKS:
		-FreeActor:
	D_VEILWORKS:
		-FreeActor:
'''
    (target / 'map.yaml').write_text(text, encoding='utf-8')
    lua = '''-- Developer diagnostic: commands exercise engine traits; they do not prove
-- visual quality, campaign victories, harvesting throughput or gameplay balance.
local units = {}
local buildings = {}
local targets = {}
WorldLoaded = function()
	Camera.Position = Map.CenterOfCell(CPos.New(48, 24))
'''
    for name in names:
        lua += f'\ttable.insert(units, Map.NamedActor("{name}"))\n'
        lua += f'\ttable.insert(targets, Map.NamedActor("Target{name[4:]}"))\n'
    for side in 'ahd':
        for index in range(13):
            lua += f'\ttable.insert(buildings, Map.NamedActor("Building{side}{index}"))\n'
    lua += '''
	print("ANIMATION_DIAGNOSTIC START units=" .. #units .. " buildings=" .. #buildings)
	Trigger.AfterDelay(DateTime.Seconds(2), function()
		for _, actor in ipairs(units) do actor.Move(actor.Location + CVec.New(2, 0)) end
		print("ANIMATION_DIAGNOSTIC MOVE")
	end)
	Trigger.AfterDelay(DateTime.Seconds(6), function()
		for i, actor in ipairs(units) do
			if actor.HasProperty("Attack") then actor.Attack(targets[i], true, true) end
		end
		print("ANIMATION_DIAGNOSTIC ATTACK")
	end)
	Trigger.AfterDelay(DateTime.Seconds(12), function()
		Camera.Position = Map.CenterOfCell(CPos.New(48, 64))
		for _, actor in ipairs(units) do if not actor.IsDead then actor.Health = math.floor(actor.MaxHealth * 0.4) end end
		for _, actor in ipairs(buildings) do actor.Health = math.floor(actor.MaxHealth * 0.4) end
		print("ANIMATION_DIAGNOSTIC HEAVY_DAMAGE")
	end)
	Trigger.AfterDelay(DateTime.Seconds(18), function()
		for _, actor in ipairs(buildings) do actor.Health = math.floor(actor.MaxHealth * 0.1) end
		print("ANIMATION_DIAGNOSTIC CRITICAL_DAMAGE")
	end)
	Trigger.AfterDelay(DateTime.Seconds(24), function()
		Camera.Position = Map.CenterOfCell(CPos.New(48, 24))
		for _, actor in ipairs(buildings) do actor.Health = actor.MaxHealth end
		for _, actor in ipairs(units) do if not actor.IsDead then actor.Kill("DefaultDeath") end end
		print("ANIMATION_DIAGNOSTIC REPAIR_AND_DEATH")
	end)
	Trigger.AfterDelay(DateTime.Seconds(25), function()
		local corpses = 0
		for _, owner in ipairs({"Neutral", "Multi0", "HostA", "HostD"}) do
			for _, actor in ipairs(Player.GetPlayer(owner).GetActors()) do
				if string.find(actor.Type, "death") then corpses = corpses + 1 end
			end
		end
		print("ANIMATION_DIAGNOSTIC DEATH_ACTORS=" .. corpses)
		if corpses ~= 24 then error("Expected 24 facing-preserving death actors") end
		print("ANIMATION_DIAGNOSTIC PASS")
	end)
end
'''
    (target / 'animation-test.lua').write_text(lua, encoding='utf-8')


if __name__ == '__main__':
    main()
