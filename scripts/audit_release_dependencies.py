"""Inventory external references in the installed manifest; not a rights clearance.

Run after build.py. --require-independent fails while RA package references or
content installer dependencies remain. Never treats absent staging as success.
"""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def inspect(manifest):
    source = manifest.read_text(encoding='utf-8-sig')
    references = []
    section = ''
    for number, raw in enumerate(source.splitlines(), 1):
        if not raw.strip() or raw.lstrip().startswith('#'):
            continue
        if not raw.startswith(('\t', ' ')):
            section = raw.split(':', 1)[0]
        if any(token in raw for token in ('ra|', '$ra:', 'Content/ra/', 'content|', 'ra-content')):
            references.append({'section': section, 'line': number, 'reference': raw.strip()})
    return {
        'schema': 1,
        'manifest_sha256': hashlib.sha256(manifest.read_bytes()).hexdigest(),
        'external_ra_references': references,
        'independent_manifest': not references,
        'limitations': 'Manifest-level architecture check only. Does not prove asset licensing, '
                      'transitive asset completeness, native playability or clean-machine installation.',
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, default=ROOT / '.sdk/mods/sevenfall/mod.yaml')
    parser.add_argument('--output', type=Path, default=ROOT / 'artifacts/release-dependencies.json')
    parser.add_argument('--require-independent', action='store_true')
    args = parser.parse_args()
    if not args.manifest.is_file():
        parser.error('Installed manifest missing; run scripts/build.py first.')
    report = inspect(args.manifest)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(f"External RA manifest references: {len(report['external_ra_references'])}")
    print(f'Report: {args.output}')
    if args.require_independent and not report['independent_manifest']:
        raise SystemExit('Standalone packaging blocked: external RA dependencies remain.')


if __name__ == '__main__':
    main()
