"""Generate native nine-faction harvesting and Veilglass hazard diagnostics."""
from pathlib import Path
import struct

ROOT = Path(__file__).resolve().parents[1]
FACTIONS = ['a_seraph', 'a_warden', 'a_exile', 'h_bastion', 'h_union',
            'h_covenant', 'd_legion', 'd_brood', 'd_court']


def main():
    folder = ROOT / 'mods/sevenfall/maps/release-test'
    folder.mkdir(parents=True, exist_ok=True)
    size = 128
    resource_offset = 17 + size * size * 3
    data = bytearray(struct.pack('<BHHIII', 2, size, size, 17, 0, resource_offset)
                     + struct.pack('<HB', 255, 0) * size * size + bytes(size * size * 2))

    def field(cx, cy):
        for x in range(cx - 2, cx + 3):
            for y in range(cy - 2, cy + 3):
                offset = resource_offset + (x * size + y) * 2
                data[offset:offset + 2] = bytes((1, 12))

    lines = ['MapFormat: 12', 'RequiresMod: sevenfall', 'Title: Sevenfall Release Diagnostic',
             'Author: Sevenfall contributors', 'Tileset: TEMPERAT', 'MapSize: 128,128',
             'Bounds: 1,1,126,126', 'Visibility: Lobby', 'Categories: Test', 'Players:',
             '\tPlayerReference@Neutral:', '\t\tName: Neutral', '\t\tOwnsWorld: True',
             '\t\tNonCombatant: True', '\t\tFaction: h_bastion']
    for i, faction in enumerate(FACTIONS):
        lines += [f'\tPlayerReference@P{i}:', f'\t\tName: P{i}', f'\t\tFaction: {faction}']
        if i == 0:
            lines += ['\t\tPlayable: True', '\t\tLockFaction: True']
    lines += ['Actors:', '\tSpawn: mpspawn', '\t\tOwner: Neutral', '\t\tLocation: 10,10']
    for i, faction in enumerate(FACTIONS):
        x, y = 5 + (i % 3) * 38, 5 + (i // 3) * 34
        prefix = faction[0]
        power = {'a': 'a_spire', 'h': 'h_generator', 'd': 'd_heart'}[prefix]
        for name, kind, px, py in [('Power', power, x, y),
                                    ('Refinery', prefix + '_veilworks', x + 4, y + 4)]:
            lines += [f'\t{name}{i}: {kind}', f'\t\tOwner: P{i}', f'\t\tLocation: {px},{py}']
        field(x + 12, y + 12)
    # A separate untouched field for controlled contact and spread assertions.
    field(60, 116)
    lines += ['Rules:', '\tWorld:', '\t\t-SpawnStartingUnits:', '\t\tLuaScript:',
              '\t\t\tScripts: release-test.lua', '\tPlayer:', '\t\t-ConquestVictoryConditions:',
              '\t\tShroud:', '\t\t\tFogCheckboxEnabled: False', '\t\t\tFogCheckboxLocked: True',
              '\t\t\tExploredMapCheckboxEnabled: True', '\t\t\tExploredMapCheckboxLocked: True']
    (folder / 'map.yaml').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    (folder / 'map.bin').write_bytes(data)


if __name__ == '__main__':
    main()
