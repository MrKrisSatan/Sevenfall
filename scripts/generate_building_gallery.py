"""Deterministic developer map for inspecting all faction building silhouettes."""
from pathlib import Path
import struct

ROOT = Path(__file__).resolve().parents[1]

def main():
    target = ROOT / 'mods/sevenfall/maps/building-gallery'
    target.mkdir(parents=True, exist_ok=True)
    size = 96
    tiles = bytearray()
    for x in range(size):
        for y in range(size):
            tiles.extend(struct.pack('<HB', 1 if y >= 72 else 255, 0 if y >= 72 else (x*7+y*3)%16))
    (target/'map.bin').write_bytes(struct.pack('<BHHIII',2,size,size,17,0,17+size*size*3)+tiles+bytes(size*size*2))
    text = '''MapFormat: 12
RequiresMod: sevenfall
Title: Sevenfall Building Gallery
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
    for i, faction in enumerate(['a_seraph','h_bastion','d_legion']):
        text += f'\tPlayerReference@Multi{i}:\n\t\tName: Multi{i}\n\t\tPlayable: True\n\t\tFaction: {faction}\n\t\tLockFaction: True\n\t\tLockSpawn: True\n\t\tSpawn: {i+1}\n'
    text += 'Actors:\n'
    for i,(f,power,barracks,factory) in enumerate([('a','spire','chapel','armory'),('h','generator','barracks','motorpool'),('d','heart','pit','forge')]):
        x=9+i*30
        text += f'\tSpawn{i}: mpspawn\n\t\tOwner: Neutral\n\t\tLocation: {x},12\n'
        actors=['fact',f+'_'+power,f+'_veilworks',f+'_'+barracks,f+'_'+factory]+[f+'_'+r for r in ['advpower','service','radar','helipad','airfield','kennel','tech','naval']]
        for j,actor in enumerate(actors):
            ax,ay=(x,74) if j==12 else (x+(j%2)*10,18+(j//2)*8)
            text += f'\tBuilding{i}_{j}: {actor}\n\t\tOwner: Multi{i}\n\t\tLocation: {ax},{ay}\n'
    text += '''Rules:
	World:
		-SpawnStartingUnits:
	Player:
		Shroud:
			FogCheckboxEnabled: False
			FogCheckboxLocked: True
			ExploredMapCheckboxEnabled: True
			ExploredMapCheckboxLocked: True
	A_VEILWORKS:
		-FreeActor:
	H_VEILWORKS:
		-FreeActor:
	D_VEILWORKS:
		-FreeActor:
	A_ADVPOWER:
		Power:
			Amount: 2000
	H_ADVPOWER:
		Power:
			Amount: 2000
	D_ADVPOWER:
		Power:
			Amount: 2000
'''
    (target/'map.yaml').write_text(text,encoding='utf-8')

if __name__ == '__main__':
    main()
