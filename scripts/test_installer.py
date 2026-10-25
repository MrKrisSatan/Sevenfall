"""CI-only installer lifecycle test, in an explicitly isolated writable directory."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

def run(executable,*args):subprocess.run([str(executable),*map(str,args)],check=True,timeout=180)
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--installer',type=Path,required=True);p.add_argument('--package',type=Path,required=True);p.add_argument('--install-dir',type=Path,required=True);p.add_argument('--report',type=Path,required=True);a=p.parse_args()
 target=a.install_dir.resolve()
 if target.exists():p.error('Installer test requires a new empty destination, preserving existing data')
 if len(target.parts)<4:p.error('Installer destination is too broad')
 target.parent.mkdir(parents=True,exist_ok=True)
 args=['/VERYSILENT','/SUPPRESSMSGBOXES','/NORESTART','/SP-',f'/DIR={target}','/NOICONS']
 run(a.installer.resolve(),*args)
 inventory=json.loads((a.package/'FILES.sha256.json').read_text(encoding='utf-8'));verified=0
 for name,expected in inventory.items():
  file=(target/name).resolve()
  if not file.is_relative_to(target):raise ValueError('Unsafe inventory path')
  if hashlib.sha256(file.read_bytes()).hexdigest()!=expected:raise RuntimeError('Installed hash mismatch: '+name)
  verified+=1
 settings=target/'Support/settings.yaml';settings.write_text('Game:\n\tPlayerName: Preserve Me\n',encoding='utf-8')
 save=target/'Support/Saves/lifecycle-sentinel.txt';save.parent.mkdir(parents=True,exist_ok=True);save.write_text('Keep this save',encoding='utf-8')
 run(a.installer.resolve(),*args)
 assert settings.read_text(encoding='utf-8')=='Game:\n\tPlayerName: Preserve Me\n'
 assert save.read_text(encoding='utf-8')=='Keep this save'
 uninstaller=target/'unins000.exe'
 if not uninstaller.is_file():raise RuntimeError('Uninstaller missing')
 run(uninstaller,'/VERYSILENT','/SUPPRESSMSGBOXES','/NORESTART')
 assert not (target/'Sevenfall.exe').exists(),'Uninstall left executable behind'
 assert settings.is_file() and save.is_file(),'Uninstall removed settings or saves'
 a.report.parent.mkdir(parents=True,exist_ok=True)
 a.report.write_text(json.dumps({'installed_file_hashes_verified':verified,'reinstall_preserves_settings':True,'reinstall_preserves_saves':True,'uninstall_preserves_user_data':True,'gameplay_or_clean_machine_acceptance':False},indent=2)+'\n',encoding='utf-8')
 print('Installer lifecycle passed; game launch and clean-machine acceptance remain separate.')
if __name__=='__main__':main()
