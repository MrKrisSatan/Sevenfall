"""Apply and verify reviewed, hash-pinned patches to the pinned OpenRA source.

The source bundle includes the unmodified upstream commit and this patch manifest.
Only these exact changes are accepted by the binary packager.
"""
import hashlib
import json
from pathlib import Path

MANIFEST = Path(__file__).resolve().parents[1]/'packaging/engine/patches.json'

def digest(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def specifications():
    return json.loads(MANIFEST.read_text(encoding='utf-8'))['patches']

def apply(engine):
    for patch in specifications():
        path = Path(engine)/patch['path']
        text = path.read_text(encoding='utf-8-sig')
        current = digest(text)
        if current == patch['after_sha256']:
            continue
        if current != patch['before_sha256'] or text.count(patch['before']) != 1:
            raise RuntimeError('Unexpected upstream source; preserving local edits: '+str(path))
        result = text.replace(patch['before'], patch['after'])
        if digest(result) != patch['after_sha256']:
            raise RuntimeError('Invalid patch result: '+str(path))
        path.write_text(result, encoding='utf-8', newline='\n')
    return verify(engine)

def verify(engine):
    hashes = {}
    for patch in specifications():
        path = Path(engine)/patch['path']
        if digest(path.read_text(encoding='utf-8-sig')) != patch['after_sha256']:
            raise RuntimeError('Engine patch not applied or modified: '+str(path))
        hashes[patch['path']] = patch['after_sha256']
    return hashes
