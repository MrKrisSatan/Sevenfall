"""Stage an explicit skirmish-only distribution without deleting development sources."""
from pathlib import Path
import shutil
SKIRMISH_MAPS=frozenset({'broken-choir','ashen-crossing','twelvefold-scar','sevenfall-menu'})

def stage_mod(source,destination,profile):
 source=Path(source);destination=Path(destination)
 def ignore(directory,names):
  if profile=='skirmish' and Path(directory)==source/'maps':return set(names)-SKIRMISH_MAPS
  return set()
 shutil.copytree(source,destination,ignore=ignore)
 if profile=='skirmish':
  for name in SKIRMISH_MAPS:
   if not (destination/'maps'/name/'map.yaml').is_file():raise RuntimeError('Required skirmish map missing: '+name)
  # Keep the manifest entry valid, with an intentionally empty mission list.
  (destination/'missions.yaml').write_text('# Campaign previews are excluded from the skirmish candidate.\n',encoding='utf-8')
 return sorted(p.name for p in (destination/'maps').iterdir() if p.is_dir())
