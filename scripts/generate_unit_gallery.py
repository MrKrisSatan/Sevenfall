"""Generate a reproducible inspection map for every implemented unit design."""
from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]


def main():
    target = ROOT / 'mods/sevenfall/maps/unit-gallery'
    target.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ROOT / 'mods/sevenfall/maps/broken-choir/map.bin', target / 'map.bin')
    units = re.findall(r'^([A-Z][A-Z0-9_]+):$',
                       (ROOT / 'mods/sevenfall/rules/30-units.yaml').read_text(encoding='utf-8'), re.M)
    text = '''MapFormat: 12
RequiresMod: sevenfall
Title: Sevenfall Unit Gallery
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
	PlayerReference@Multi0:
		Name: Multi0
		Playable: True
		Faction: h_bastion
		LockFaction: True
		LockSpawn: True
		Spawn: 1
	PlayerReference@HostA:
		Name: HostA
		NonCombatant: True
		Faction: a_seraph
		Color: E7C76C
	PlayerReference@HostD:
		Name: HostD
		NonCombatant: True
		Faction: d_legion
		Color: D34B78
Actors:
	Spawn0: mpspawn
		Owner: Neutral
		Location: 48,47
'''
    for side, x, owner in [('a', 34, 'HostA'), ('h', 48, 'Multi0'), ('d', 62, 'HostD')]:
        roster = ['mcv'] + [u.lower() for u in units if u.startswith(side.upper() + '_')]
        for i, actor in enumerate(roster):
            text += (f'\tUnit{side}{i}: {actor}\n\t\tOwner: {owner}\n'
                     f'\t\tLocation: {x},{36 + i * 3}\n\t\tFacing: 384\n')
    text += '''Rules:
	World:
		-SpawnStartingUnits:
	Player:
		-ConquestVictoryConditions:
		Shroud:
			FogCheckboxEnabled: False
			FogCheckboxLocked: True
			ExploredMapCheckboxEnabled: True
			ExploredMapCheckboxLocked: True
'''
    (target / 'map.yaml').write_text(text, encoding='utf-8')


if __name__ == '__main__':
    main()
