"""Hash-pinned dependency notices and corresponding library/font source bundle."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import tarfile
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT/'packaging/dependencies/sources.json'
CACHE = ROOT/'.tools/release-source-cache'

def sources():
    return json.loads(MANIFEST.read_text(encoding='utf-8'))['sources']

def archive(entry):
    CACHE.mkdir(parents=True, exist_ok=True)
    path = CACHE/entry['filename']
    if not path.exists():
        if not entry['url'].startswith('https://'):
            raise ValueError('Dependency source must use HTTPS')
        temporary = path.with_suffix(path.suffix+'.download')
        with urllib.request.urlopen(entry['url'], timeout=120) as response, temporary.open('wb') as out:
            shutil.copyfileobj(response, out)
        if hashlib.sha256(temporary.read_bytes()).hexdigest() != entry['sha256']:
            raise ValueError('Downloaded source checksum mismatch: '+entry['id'])
        temporary.replace(path)
    if hashlib.sha256(path.read_bytes()).hexdigest() != entry['sha256']:
        raise ValueError('Cached source checksum mismatch: '+entry['id'])
    return path

def members(tar):
    for member in tar.getmembers():
        if not member.isfile():
            continue
        full = PurePosixPath(member.name)
        if full.is_absolute() or '..' in full.parts or len(full.parts) < 2 or '\\' in member.name or ':' in member.name:
            raise ValueError('Unsafe dependency archive path: '+member.name)
        yield member, PurePosixPath(*full.parts[1:])

def shipped_packages(package):
    required = set()
    for dependency_file in package.glob('*.deps.json'):
        data = json.loads(dependency_file.read_text(encoding='utf-8'))
        libraries = data.get('libraries', {})
        for target in data.get('targets', {}).values():
            for name, content in target.items():
                if libraries.get(name, {}).get('type') == 'package' and any(
                    content.get(k) for k in ('runtime', 'native', 'runtimeTargets', 'resources')):
                    required.add(name.lower())
    return required

def collect(package):
    destination = package/'Notices/SourceLicences'
    destination.mkdir(parents=True, exist_ok=True)
    for font in json.loads(MANIFEST.read_text(encoding='utf-8')).get('fonts', []):
        if hashlib.sha256((package/font['file']).read_bytes()).hexdigest() != font['sha256']:
            raise RuntimeError('Unreviewed font binary: '+font['file'])
    coverage = {}
    copied = []
    for entry in sources():
        count = 0
        with tarfile.open(archive(entry)) as tar:
            for member, relative in members(tar):
                if str(relative) not in entry['notice_paths']:
                    continue
                out = destination/entry['id']/str(relative)
                if not out.resolve().is_relative_to(destination.resolve()):
                    raise ValueError('Unsafe source notice destination')
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_bytes(tar.extractfile(member).read())
                count += 1
        if entry['notice_paths'] and count != len(set(entry['notice_paths'])):
            raise RuntimeError('Source licence paths did not all resolve: '+entry['id'])
        if count:
            for name in entry['packages']:
                coverage.setdefault(name.lower(), []).append(entry['id'])
        copied.append({'id':entry['id'], 'texts':count, 'url':entry['url'], 'sha256':entry['sha256']})

    inventory = json.loads((package/'Notices/dependencies.json').read_text(encoding='utf-8'))
    required = shipped_packages(package)
    missing = []
    for entry in inventory:
        key = entry['package'].lower()
        entry['runtime_assets_in_deps_manifest'] = key in required
        entry['source_licence_components'] = coverage.get(key, [])
        if key in required and not entry['included_texts'] and not coverage.get(key):
            missing.append(entry['package'])
    known = {p['package'].lower() for p in inventory}
    missing.extend(sorted(required-known))
    if missing:
        raise RuntimeError('Missing exact distribution notices: '+', '.join(missing))
    (package/'Notices/dependencies.json').write_text(json.dumps(inventory, indent=2)+'\n', encoding='utf-8')
    (destination/'SOURCE_INVENTORY.json').write_text(json.dumps(copied, indent=2)+'\n', encoding='utf-8')
    shutil.copy2(ROOT/'packaging/dependencies/RELINKING.md', package/'Notices/RELINKING.md')
    return {'runtime_packages':len(required), 'unresolved_runtime_notices':missing, 'source_components':len(copied)}

# Samples and precompiled outputs are not required to build the libraries. Their
# omission avoids redistributing unrelated test songs/images from upstream repos.
EXCLUDED_MEDIA = {'.mp3','.mp4','.m4a','.wav','.ogg','.flac','.wma','.asf','.ape',
    '.spx','.aiff','.aif','.tta','.wv','.opus','.jpg','.jpeg','.png','.bmp','.gif',
    '.ico','.tif','.tiff','.ttf','.otf','.woff','.woff2','.dll','.exe','.pdb',
    '.nupkg','.so','.dylib','.a','.lib'}

def bundle(version, destination=None):
    destination = destination or ROOT/'dist'
    destination.mkdir(parents=True, exist_ok=True)
    target = destination/f'Sevenfall-{version}-dependencies-source.zip'
    if target.exists():
        raise RuntimeError('Preserving existing dependency source archive')
    with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as output:
        output.write(MANIFEST, 'SOURCE_MANIFEST.json')
        output.write(ROOT/'packaging/dependencies/RELINKING.md', 'BUILD_AND_RELINK.md')
        for entry in sources():
            with tarfile.open(archive(entry)) as tar:
                for member, relative in members(tar):
                    if relative.suffix.lower() in EXCLUDED_MEDIA:
                        continue
                    output.writestr(entry['id']+'/'+str(relative), tar.extractfile(member).read())
    target.with_suffix('.zip.sha256').write_text(hashlib.sha256(target.read_bytes()).hexdigest()+'  '+target.name+'\n', encoding='utf-8')
    return target

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--version', required=True)
    args = parser.parse_args()
    print(bundle(args.version))
