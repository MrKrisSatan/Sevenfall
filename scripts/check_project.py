#!/usr/bin/env python3
"""Static lint for Sevenfall MiniYaml source. Not an OpenRA runtime test."""
from pathlib import Path
import re

base = Path(__file__).resolve().parent.parent / 'mods' / 'sevenfall'
files = list((base / 'rules').glob('*.yaml')) + list((base / 'weapons').glob('*.yaml'))
assert files, 'No OpenRA YAML found'
ids = {}
for p in files:
    local_ids = set()
    for no, raw in enumerate(p.read_text(encoding='utf8').splitlines(), 1):
        assert not raw.startswith(' '), f'{p}:{no}: MiniYaml indentation must use tabs'
        if raw and not raw.startswith(('\t', '#', ' ')) and raw.endswith(':'):
            key = raw[:-1]
            assert key not in local_ids, f'Duplicate {key} within {p}'
            local_ids.add(key)
            # These overlays intentionally refine actors declared earlier.
            if p.name not in ('10-factions.yaml', '35-animations.yaml', '55-subfactions.yaml', '90-alpha.yaml'):
                assert key not in ids, f'Duplicate {key}: {p} and {ids[key]}'
            ids[key] = f'{p.name}:{no}'
ftl = (base / 'fluent/sevenfall.ftl').read_text(encoding='utf8')
fluent_ids = re.findall(r'^([a-z][a-z0-9-]+)\s*=', ftl, flags=re.MULTILINE)
assert len(set(fluent_ids)) == len(fluent_ids), 'Duplicate ftl name'
referenced = set()
for p in files:
    # Conditions and filenames may also use the sf- prefix. Only text fields
    # refer to Fluent messages; treating every prefixed token as text rejects
    # valid native aura conditions and original sound assets.
    referenced.update(re.findall(r'(?m)^\t+(?:Name|GenericName|Description|Text|Title):[^\n]*?\b(sf-[a-z0-9-]+)\b', p.read_text(encoding='utf8')))
missing = referenced - set(fluent_ids)
assert not missing, f'Missing fluent strings: {sorted(missing)}'
# All intentional new actor identifiers are assigned an image unless they are rule overrides.
actors = {}
for f in ('20-structures.yaml', '25-support-structures.yaml', '30-units.yaml', '45-defenses.yaml', '55-subfactions.yaml'):
    filetext = (base / 'rules' / f).read_text(encoding='utf8')
    for m in re.finditer(r'(?m)^([A-Z][A-Z0-9_]+):\n(.*?)(?=^[A-Z][A-Z0-9_]+:\n|\Z)', filetext, re.S|re.M):
        key, body = m.group(1),m.group(2)
        assert '\tBuildable:' in body and '\tRenderSprites:' in body, (key, f)
        assert '\t\tPrerequisites:' in body, (key, f)
        actors[key] = body
assert len(actors) >= 25, len(actors)
for side, groups in [('A_', 'sf.angels'),('H_', 'sf.humans'),('D_', 'sf.demons')]:
    assert sum(k.startswith(side) for k in actors) >= 7
print(f'Static checks passed: {len(files)} YAML files, {len(actors)} actor definitions, {len(fluent_ids)} text IDs.')
print('OpenRA runtime tests must still be run in a real Mod SDK.')
