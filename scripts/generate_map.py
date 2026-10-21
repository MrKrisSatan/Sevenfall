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
    # The menu is a clean art showcase, not a resource field.
    binary = bytearray((target / 'map.bin').read_bytes())
    binary[17 + size*size*3:] = bytes(size*size*2)
    (shell / 'map.bin').write_bytes(binary)
    text = (target / 'map.yaml').read_text(encoding='utf-8')
    text = text.replace('Visibility: Lobby', 'Visibility: Shellmap')
    text = text.replace('Title: Broken Choir - Proving Ground', 'Title: Sevenfall Menu')
    text = text[:text.index('\tPlayerReference@Multi0:')]
    text += '''	PlayerReference@Host:
		Name: Host
		NonCombatant: True
		Faction: a_seraph
		Color: E7C76C
	PlayerReference@Dominion:
		Name: Dominion
		NonCombatant: True
		Faction: h_bastion
		Color: 69B4D4
	PlayerReference@Legions:
		Name: Legions
		NonCombatant: True
		Faction: d_legion
		Color: D34B78
Actors:
	MenuCenter: waypoint
		Owner: Neutral
		Location: 48,48
	Spire: a_spire
		Owner: Host
		Location: 41,48
	Generator: h_generator
		Owner: Dominion
		Location: 47,48
	Heart: d_heart
		Owner: Legions
		Location: 53,48
	Refinerya: a_veilworks
		Owner: Host
		Location: 41,54
	Refineryh: h_veilworks
		Owner: Dominion
		Location: 47,54
	Refineryd: d_veilworks
		Owner: Legions
		Location: 53,54
Rules:
	World:
		-StartGameNotification:
		-SpawnStartingUnits:
		-MapStartingLocations:
	A_VEILWORKS:
		-FreeActor:
	H_VEILWORKS:
		-FreeActor:
	D_VEILWORKS:
		-FreeActor:
	Player:
		Shroud:
			FogCheckboxEnabled: False
			ExploredMapCheckboxEnabled: True
'''
    (shell / 'map.yaml').write_text(text, encoding='utf-8')

if __name__ == '__main__':
    main()
