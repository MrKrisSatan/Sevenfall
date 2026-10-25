"""Generate the deterministic, developer-only defense proving-ground scenarios."""
from pathlib import Path
import json
import struct

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / 'mods/sevenfall'


def main():
    folder = MOD / 'maps/defense-test'
    folder.mkdir(parents=True, exist_ok=True)
    binary = bytearray(struct.pack('<BHHIII', 2, 96, 96, 17, 0, 17 + 96 * 96 * 3) + struct.pack('<HB', 255, 0) * (96 * 96) + bytes(96 * 96 * 2))
    binary[17 + 96 * 96 * 3:] = bytes(96 * 96 * 2)
    (folder / 'map.bin').write_bytes(binary)
    text = '''MapFormat: 12
RequiresMod: sevenfall
Title: Sevenfall Defense Proving Ground
Author: Sevenfall contributors
Tileset: TEMPERAT
MapSize: 96,96
Bounds: 1,1,94,94
Visibility: Lobby
Categories: Test
Players:
	PlayerReference@Neutral:
		Name: Neutral
		OwnsWorld: True
		NonCombatant: True
		Faction: h_bastion
'''
    players = [('Humans','h_bastion','Angels','Demons, Victims, SilentBrood, DarkAngels'),
               ('Angels','a_warden','Humans','Demons, Victims, SilentBrood'),
               ('Demons','d_brood','','Humans, Angels, Victims'),
               ('Victims','h_union','','Demons, Angels, Humans, SilentBrood, DarkAngels'),
               ('SilentBrood','d_court','','Victims, Humans, Angels'),
               ('DarkAngels','a_seraph','','Victims')]
    for name, faction, allies, enemies in players:
        text += f'\tPlayerReference@{name}:\n\t\tName: {name}\n\t\tFaction: {faction}\n\t\tEnemies: {enemies}\n'
        if allies:
            text += f'\t\tAllies: {allies}\n'
        if name == 'Humans':
            text += '\t\tPlayable: True\n\t\tLockFaction: True\n\t\tLockSpawn: True\n\t\tSpawn: 1\n'
    text += 'Actors:\n\tSpawn0: mpspawn\n\t\tOwner: Neutral\n\t\tLocation: 35,25\n'
    actors = []
    def actor(name, type, owner, x, y):
        actors.append(type)
        return f'\t{name}: {type}\n\t\tOwner: {owner}\n\t\tLocation: {x},{y}\n'
    for index, x in enumerate((5,10,15,20)):
        text += actor(f'AngelPower{index}', 'a_spire', 'Angels', x, 59)
    for index, x in enumerate((5,10)):
        text += actor(f'DemonPower{index}', 'd_heart', 'Demons', x, 30)
    for row in [('HumanYard','fact','Humans',5,5),('HumanPower','h_generator','Humans',10,5),
                ('VictimPower','h_generator','Victims',80,5),('SilentPower','d_heart','SilentBrood',31,31),
                ('DarkPower','a_spire','DarkAngels',70,31),
                ('ConvertWall','d_mourningwall','Demons',15,15),('OverlapWall','d_mourningwall','Demons',15,16),
                ('OpposingWall','d_mourningwall','Victims',17,15),('ConvertVictim','h_rifleman','Victims',16,15),
                ('WardWall','d_mourningwall','Demons',35,15),('Ward','a_sanctuary','Angels',38,15),('WardVictim','h_rifleman','Humans',36,15),
                ('RetreatWall','d_mourningwall','Demons',55,15),('RetreatVictim','h_rifleman','Victims',56,15),
                ('VehicleWall','d_mourningwall','Demons',75,15),('VehicleVictim','h_bulwark','Victims',76,15),
                ('DestroyedWall','d_mourningwall','Demons',15,35),('DestroyedVictim','h_rifleman','Victims',16,35),
                ('SilentWall','d_mourningwall','SilentBrood',35,35),('SilentVictim','h_rifleman','Victims',36,35),
                ('LightWall','a_dawnwall','Angels',55,35),('LightVictim','h_rifleman','Victims',53,35),
                ('LightTankWall','a_dawnwall','Angels',55,38),('LightTank','h_bulwark','Victims',53,38),
                ('DarkWall','a_dawnwall','DarkAngels',75,35),('DarkVictim','h_rifleman','Victims',73,35),
                ('WireWalker','h_rifleman','Victims',8,50),('WireControl','h_rifleman','Victims',8,53),
                ('CrushWire','h_razorwire','Humans',9,55),('Crusher','h_bulwark','Victims',7,55),
                ('BlastWall','h_blastwall','Humans',29,55),('BlockedTank','h_bulwark','Victims',27,55),
                ('ThornWalker','h_rifleman','Victims',38,50),('ThornControl','h_rifleman','Victims',38,53),
                ('HumanGun','h_autocannon','Humans',55,55),('GunTarget','sf_defense_dummy','Victims',59,55),
                ('Bunker','h_entrenchment','Humans',75,55),('BunkerTarget','sf_defense_dummy','Victims',79,55),
                ('AngelGun','a_watchfire','Angels',12,65),('AngelGunTarget','sf_defense_dummy','Victims',16,65),
                ('AngelLance','a_judgment','Angels',26,65),('LanceTarget','sf_defense_dummy','Victims',30,65),
                ('Spines','d_spinenest','Demons',40,65),('SpineTarget','sf_defense_dummy','Victims',44,65),
                ('Maw','d_cindermaw','Demons',54,65),('MawTarget','sf_defense_dummy','Victims',57,65),
                ('AngelAA','a_skyward','Angels',15,80),('HumanAA','h_missilenest','Humans',40,80),('DemonAA','d_skyhook','Demons',70,80),
                ('AAGroundTarget','sf_defense_dummy','Victims',43,83)]:
        text += actor(*row)
    for i in range(9):
        text += actor('Wire'+str(i),'h_razorwire','Humans',8+i,50)
        text += actor('Thorn'+str(i),'d_thornfield','Demons',38+i,50)
    text += '''Rules:
	World:
		-SpawnStartingUnits:
		LuaScript:
			Scripts: defense-test.lua
	Player:
		-ConquestVictoryConditions:
		Shroud:
			FogCheckboxEnabled: False
			FogCheckboxLocked: True
			ExploredMapCheckboxEnabled: True
			ExploredMapCheckboxLocked: True
	H_RIFLEMAN:
		AutoTarget:
			InitialStance: HoldFire
			InitialStanceAI: HoldFire
	H_BULWARK:
		AutoTarget:
			InitialStance: HoldFire
			InitialStanceAI: HoldFire
	sf_defense_dummy:
		Inherits: H_BULWARK
		-Buildable:
		Health:
			HP: 1000000
		AutoTarget:
			InitialStance: HoldFire
			InitialStanceAI: HoldFire
	sf_defense_airtarget:
		Inherits: HELI
		-Buildable:
		RenderSprites:
			Image: heli
		Health:
			HP: 1000000
'''
    (folder / 'map.yaml').write_text(text, encoding='utf-8')
    (folder / 'defense-test.lua').write_text(LUA, encoding='utf-8')
    print('Defense proving ground generated with all 15 defenses and live counterplay cases.')


LUA = '''-- Native defense-extension acceptance. Uses real actors, ownership, power and cargo.
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
'''


if __name__ == '__main__':
    main()
