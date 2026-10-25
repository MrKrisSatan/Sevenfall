"""Collect exact restored NuGet metadata and available licence texts for review.

This is an inventory, not a substitute for corresponding-source verification.
"""
import json
from pathlib import Path
import shutil
import xml.etree.ElementTree as ET

def collect(engine, destination):
    destination.mkdir(parents=True, exist_ok=True)
    packages = {}
    folders = set()
    runtimes = set()
    for project in engine.glob('OpenRA.*/obj/project.assets.json'):
        assets = json.loads(project.read_text())
        project_folders = [Path(p) for p in assets.get('packageFolders', {})]
        folders.update(project_folders)
        for framework in assets.get('project', {}).get('frameworks', {}).values():
            for dependency in framework.get('downloadDependencies', []):
                name = dependency['name']
                if name.lower().startswith('microsoft.netcore.app.runtime.win-x64'):
                    # NuGet records resolved runtime downloads as exact ranges.
                    version = dependency['version'].strip('[]').split(',')[0].strip()
                    runtimes.add((name, version))
        for name, value in assets.get('libraries', {}).items():
            if value.get('type') != 'package':
                continue
            path = next((p / value['path'] for p in project_folders if (p/value['path']).exists()), None)
            if path is None:
                raise RuntimeError('Restored dependency missing: ' + name)
            packages[name] = path
    # Runtime pack is resolved by the SDK rather than an ordinary PackageReference.
    for name, version in sorted(runtimes):
        runtime = next((folder/name.lower()/version for folder in sorted(folders)
                        if (folder/name.lower()/version).exists()), None)
        if runtime is None:
            raise RuntimeError(f'Restored runtime dependency missing: {name}/{version}')
        packages[f'{name}/{version}'] = runtime
    inventory = []
    for name, path in sorted(packages.items()):
        out = destination/name.replace('/', '-')
        out.mkdir(exist_ok=True)
        metadata = next(path.glob('*.nuspec'))
        shutil.copy2(metadata, out/metadata.name)
        root = ET.parse(metadata).getroot()
        fields = {node.tag.split('}')[-1]: node for node in root.iter()}
        copied = []
        for file in path.rglob('*'):
            if file.is_file() and any(word in file.name.lower() for word in ('license', 'licence', 'notice', 'copying', 'copyright')):
                target = out/file.relative_to(path)
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(file, target)
                copied.append(str(file.relative_to(path)))
        inventory.append({'package': name, 'licence': fields['license'].text if 'license' in fields else None,
                          'project': fields['projectUrl'].text if 'projectUrl' in fields else None,
                          'licence_url': fields['licenseUrl'].text if 'licenseUrl' in fields else None,
                          'included_texts': copied})
    (destination/'dependencies.json').write_text(json.dumps(inventory, indent=2)+'\n')
    return inventory

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('engine', type=Path)
    parser.add_argument('destination', type=Path)
    args = parser.parse_args()
    collect(args.engine, args.destination)
