"""Bundle committed Sevenfall and pinned OpenRA/SDK source for a candidate.

Dependency source compliance remains a separate publication gate.
"""
import argparse
import hashlib
from pathlib import Path
import subprocess
import zipfile
from build import ENGINE_COMMIT, SDK_COMMIT

ROOT = Path(__file__).resolve().parents[1]
def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--version', required=True)
    args = parser.parse_args()
    if subprocess.check_output(['git', 'status', '--porcelain'], cwd=ROOT).strip():
        raise SystemExit('Commit the candidate first: source bundle requires a clean working tree.')
    target = ROOT/'dist'/f'Sevenfall-{args.version}-source.zip'
    if target.exists():
        raise SystemExit('Source archive already exists; preserving it.')
    target.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as bundle:
        for name, path, expected in [('Sevenfall', ROOT, None), ('OpenRA', ROOT/'.sdk/engine', ENGINE_COMMIT),
                                     ('OpenRAModSDK', ROOT/'.sdk', SDK_COMMIT)]:
            sha = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=path, text=True).strip()
            if expected and sha != expected:
                raise SystemExit(f'{name}: unexpected source revision {sha}')
            archive = subprocess.check_output(['git', 'archive', '--format=tar', sha], cwd=path)
            bundle.writestr(name+'.tar', archive)
            bundle.writestr(name+'.commit', sha+'\n')
        bundle.writestr('README.txt', 'Extract the three source tar files. Sevenfall/BUILDING.md contains build instructions.\n'
                        'Sevenfall/scripts/build.py applies the reviewed, hash-pinned engine overlay automatically.\n'
                        'The companion dependencies-source.zip supplies native/audio library and font source.\n')
    target.with_suffix('.zip.sha256').write_text(hashlib.sha256(target.read_bytes()).hexdigest()+'  '+target.name+'\n')
    print(target)
    from release_dependencies import bundle as bundle_dependencies
    print(bundle_dependencies(args.version))
if __name__ == '__main__':
    main()
