"""Civilian-only shellmap: no faction army, base, colour or resource showcase."""
from pathlib import Path
import struct

def main():
    folder = Path(__file__).resolve().parents[1] / 'mods/sevenfall/maps/sevenfall-menu'
    size = 96
    data = bytearray(struct.pack('<BHHIII', 2, size, size, 17, 0, 17+size*size*3))
    for x in range(size):
        for y in range(size):
            tile, frame = 255, (x*7+y*3) % 16
            if y == 50:
                tile, frame = 109, 0
            if x in (39, 57) and 40 <= y <= 60:
                tile, frame = 108, 0
            data.extend(struct.pack('<HB', tile, frame))
    data.extend(bytes(size*size*2))
    (folder/'map.bin').write_bytes(data)
    text = '''MapFormat: 12
RequiresMod: sevenfall
Title: Sevenfall Menu
Author: Sevenfall contributors
Tileset: TEMPERAT
MapSize: 96,96
Bounds: 1,1,94,94
Visibility: Shellmap
Categories: Conquest
Players:
	PlayerReference@Neutral:
		Name: Neutral
		OwnsWorld: True
		NonCombatant: True
		Faction: h_bastion
Actors:
	MenuCenter: waypoint
		Owner: Neutral
		Location: 48,49
'''
    for i,(kind,x,y) in enumerate([('sf_cottage',41,45),('sf_townhouse',53,53),
                                 ('sf_oak',44,54),('sf_pine',55,43),('sf_deadtree',36,48),
                                 ('sf_pine',61,55),('sf_oak',50,40)]):
        text += f'\tScenery{i}: {kind}\n\t\tOwner: Neutral\n\t\tLocation: {x},{y}\n'
    text += '''Rules:
	World:
		-StartGameNotification:
		-SpawnStartingUnits:
		-MapStartingLocations:
	^SF_CIVILIAN_HOUSE:
		-WithTextDecoration@OWNER:
	Player:
		Shroud:
			FogCheckboxEnabled: False
			ExploredMapCheckboxEnabled: True
'''
    (folder/'map.yaml').write_text(text, encoding='utf-8')

if __name__ == '__main__':
    main()
