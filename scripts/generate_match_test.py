"""Unassisted bot-versus-bot conquest on the original skirmish terrain."""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def main():
    source = ROOT / 'mods/sevenfall/maps/broken-choir'
    dest = ROOT / 'mods/sevenfall/maps/match-test'
    dest.mkdir(exist_ok=True)
    text = (source/'map.yaml').read_text().split('Players:')[0].replace('Broken Choir - Proving Ground', 'Sevenfall AI Match Diagnostic').replace('Categories: Conquest', 'Categories: Test')
    text += '''Players:
	PlayerReference@Neutral:
		Name: Neutral
		OwnsWorld: True
		NonCombatant: True
		Faction: h_bastion
	PlayerReference@Observer:
		Name: Observer
		Playable: True
		NonCombatant: True
		Faction: h_bastion
	PlayerReference@Humans:
		Name: Humans
		Faction: h_bastion
		Bot: sevenfall
		Enemies: Demons
	PlayerReference@Demons:
		Name: Demons
		Faction: d_legion
		Bot: sevenfall
		Enemies: Humans
Actors:
	Spawn: mpspawn
		Owner: Neutral
		Location: 45,45
	HumanMCV: mcv
		Owner: Humans
		Location: 15,15
	DemonMCV: mcv
		Owner: Demons
		Location: 80,80
Rules:
	World:
		SFDiagnosticExit:
		-SpawnStartingUnits:
		LuaScript:
			Scripts: match-test.lua
'''
    (dest/'map.yaml').write_text(text)
    (dest/'map.bin').write_bytes((source/'map.bin').read_bytes())
if __name__ == '__main__':
    main()
