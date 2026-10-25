"""Compile a per-user setup EXE from an already-hashed skirmish candidate."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
ROOT=Path(__file__).resolve().parents[1]
def validate_package(package):
 info=json.loads((package/'BUILD_INFO.json').read_text(encoding='utf-8'))
 if info.get('profile')!='skirmish':raise ValueError('Installer requires the skirmish distribution profile')
 inventory=json.loads((package/'FILES.sha256.json').read_text(encoding='utf-8'))
 for name,expected in inventory.items():
  path=(package/name).resolve()
  if not path.is_relative_to(package.resolve()):raise ValueError('Unsafe inventory path: '+name)
  if hashlib.sha256(path.read_bytes()).hexdigest()!=expected:raise ValueError('Candidate hash mismatch: '+name)
 if not (package/'Sevenfall.exe').is_file():raise ValueError('Self-contained Sevenfall.exe missing')
 return info

def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('package',type=Path);parser.add_argument('--iscc',default=shutil.which('ISCC.exe'));parser.add_argument('--output-dir',type=Path,default=ROOT/'dist');args=parser.parse_args()
 package=args.package.resolve();info=validate_package(package)
 if not args.iscc:parser.error('Use a preinstalled Inno Setup 6.7+ compiler via --iscc')
 version=info['version'];output=args.output_dir.resolve();output.mkdir(parents=True,exist_ok=True)
 target=output/f'Sevenfall-{version}-Setup-windows-x64.exe'
 if target.exists():parser.error('Installer already exists; preserving prior evidence')
 subprocess.run([args.iscc,'/Qp','/DSourceDir='+str(package),'/DVersion='+version,'/DOutputDir='+str(output),str(ROOT/'packaging/windows/Sevenfall.iss')],check=True,cwd=ROOT)
 if not target.is_file():raise RuntimeError('Compiler returned without producing the expected setup executable')
 target.with_suffix('.exe.sha256').write_text(hashlib.sha256(target.read_bytes()).hexdigest()+'  '+target.name+'\n',encoding='utf-8')
 print('Test candidate only; publication gates remain:',target)
if __name__=='__main__':main()
