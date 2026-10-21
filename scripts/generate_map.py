"""Generate our original, symmetric economy test arena (OpenRA binary format 2)."""
from pathlib import Path
import struct

def main():
    target = Path(__file__).resolve().parents[1] / 'mods/sevenfall/maps/broken-choir'
    target.mkdir(parents=True, exist_ok=True)
    size = 96
    tiles = bytearray()
    resources = bytearray()
    for x in range(size):
        for y in range(size):
            tiles.extend(struct.pack('<HB', 255, (x * 7 + y * 3) % 16))
            kind, density = 0, 0
            for cx, cy in [(23, 23), (72, 72), (25, 65), (70, 30)]:
                if (x-cx)**2 + (y-cy)**2 <= 36:
                    kind, density = 1, 12
            if (x-47.5)**2 + (y-47.5)**2 <= 64:
                kind, density = 2, 3
            resources.extend(bytes((kind, density)))
    (target / 'map.bin').write_bytes(struct.pack('<BHHIII', 2, size, size, 17, 0,
                                                17 + size*size*3) + tiles + resources)
    (target / 'map.yaml').write_text('''MapFormat: 12
RequiresMod: sevenfall
Title: Broken Choir - Proving Ground
Author: Sevenfall contributors
Tileset: TEMPERAT
MapSize: 96,96
Bounds: 1,1,94,94
Visibility: Lobby
Categories: Conquest
Players:
	PlayerReference@Neutral:
		Name: Neutral
		OwnsWorld: True
		NonCombatant: True
		Faction: h_bastion
	PlayerReference@Multi0:
		Name: Multi0
		Playable: True
		Faction: Random
	PlayerReference@Multi1:
		Name: Multi1
		Playable: True
		Faction: Random
Actors:
	Spawn0: mpspawn
		Owner: Neutral
		Location: 15,15
	Spawn1: mpspawn
		Owner: Neutral
		Location: 80,80
''', encoding='utf-8')
    shell = target.parent / 'sevenfall-menu'
    shell.mkdir(exist_ok=True)
    (shell / 'map.bin').write_bytes((target / 'map.bin').read_bytes())
    text = (target / 'map.yaml').read_text(encoding='utf-8')
    text = text.replace('Visibility: Lobby', 'Visibility: Shellmap')
    text = text.replace('Title: Broken Choir - Proving Ground', 'Title: Sevenfall Menu')
    text = text[:text.index('\tPlayerReference@Multi0:')]
    text += '''Actors:
	MenuCenter: waypoint
		Owner: Neutral
		Location: 48,48
Rules:
	World:
		-StartGameNotification:
		-SpawnStartingUnits:
		-MapStartingLocations:
	Player:
		Shroud:
			FogCheckboxEnabled: False
			ExploredMapCheckboxEnabled: True
'''
    (shell / 'map.yaml').write_text(text, encoding='utf-8')

if __name__ == '__main__':
    main()
