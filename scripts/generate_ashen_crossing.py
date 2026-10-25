"""Reproducible two-player environment showcase with two destructible crossings."""
from pathlib import Path
import struct

ROOT = Path(__file__).resolve().parents[1]
SIZE = 128


def layout():
    tiles = {(x, y): (255, (x * 7 + y * 11) % 16)
             for x in range(SIZE) for y in range(SIZE)}
    actors = [('Spawn1', 'mpspawn', 18, 64), ('Spawn2', 'mpspawn', 108, 64)]
    for x in range(62, 65):
        for y in range(SIZE):
            tiles[x, y] = (1, 0)
    for cx in (30, 96):
        for cy in (22, 55, 78, 106):
            for x in range(cx - 7, cx + 8):
                for y in range(cy - 6, cy + 7):
                    if (x-cx)**2 + (y-cy)**2 < 42:
                        tiles[x, y] = (100 + (cy // 20) % 4, 0)
    for y in (34, 92):
        for x in range(18, 109):
            if x not in range(62, 65):
                tiles[x, y] = (105, 0)
        actors += [(f'Bridge{y}', 'sf_bridge_ew', 62, y),
                   (f'WestPost{y}', 'sf_bridge_post', 61, y-1),
                   (f'EastPost{y}', 'sf_bridge_post', 65, y+1)]
    for x in (18, 108):
        for y in range(35, 92):
            tiles[x, y] = (104, 0)
    for x in (44, 82):
        for y in range(48, 78):
            tiles[x, y] = (113, 0)
    for x in (52, 72):
        for y in range(25, 102):
            if y not in (34, 92):
                tiles[x, y] = (108, 0)
    for i, (x, y) in enumerate([(54, 29), (69, 29), (54, 97), (69, 97)]):
        actors.append((f'House{i}', 'sf_cottage' if i % 2 else 'sf_townhouse', x, y))
    for cx in (35, 91):
        for cy in (12, 114):
            for i in range(8):
                actors.append((f'Tree{cx}_{cy}_{i}', ['sf_oak', 'sf_pine', 'sf_deadtree', 'sf_burntree'][i % 4],
                               cx + (i % 4) * 2, cy + (i // 4) * 2))
    resources = {}
    for cx in (28, 98):
        for cy in (52, 76):
            for x in range(cx-3, cx+4):
                for y in range(cy-3, cy+4):
                    if (x-cx)**2+(y-cy)**2 <= 10:
                        resources[x, y] = (1, 12)
    return tiles, actors, resources


def main():
    tiles, actors, resources = layout()
    folder = ROOT / 'mods/sevenfall/maps/ashen-crossing'
    folder.mkdir(parents=True, exist_ok=True)
    data = bytearray(struct.pack('<BHHIII', 2, SIZE, SIZE, 17, 0, 17+SIZE*SIZE*3))
    for x in range(SIZE):
        for y in range(SIZE):
            data.extend(struct.pack('<HB', *tiles[x, y]))
    for x in range(SIZE):
        for y in range(SIZE):
            data.extend(bytes(resources.get((x, y), (0, 0))))
    (folder / 'map.bin').write_bytes(data)
    lines = ['MapFormat: 12', 'RequiresMod: sevenfall', 'Title: Ashen Crossing',
             'Author: Sevenfall contributors', 'Tileset: TEMPERAT', 'MapSize: 128,128',
             'Bounds: 1,1,126,126', 'Visibility: Lobby', 'Categories: Conquest', 'Players:',
             '\tPlayerReference@Neutral:', '\t\tName: Neutral', '\t\tOwnsWorld: True',
             '\t\tNonCombatant: True', '\t\tFaction: h_bastion']
    for i in range(2):
        lines += [f'\tPlayerReference@Multi{i}:', f'\t\tName: Multi{i}', '\t\tPlayable: True', '\t\tFaction: Random']
    lines.append('Actors:')
    for name, kind, x, y in actors:
        lines += [f'\t{name}: {kind}', '\t\tOwner: Neutral', f'\t\tLocation: {x},{y}']
    (folder / 'map.yaml').write_text('\n'.join(lines)+'\n', encoding='utf-8')


if __name__ == '__main__':
    main()
