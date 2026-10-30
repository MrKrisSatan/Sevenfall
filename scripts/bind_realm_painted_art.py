"""Bind all new realm renderers, including inherited harvesters and generic MCVs."""
import json
from pathlib import Path
from build_new_realms import FACTIONS,UNITS
ROOT=Path(__file__).resolve().parents[1];MOD=ROOT/'mods/sevenfall'
plan=json.loads((ROOT/'art/new-realms/painted-prompts.json').read_text())
exclusive={u[1] for u in UNITS}
rules=['# Generated painted asset bindings; gameplay values are unchanged.']
for p in plan:
 id=p['id']
 if id.endswith(('_mcv','_yard')):continue
 block=f'{id.upper()}:\n\tRenderSprites:\n\t\tImage: {id}\n'
 if p['kind']=='unit':
  block+=f'\tSpawnActorOnDeath@SF_ANIMATION:\n\t\tActor: {id}.death\n'
  if id.endswith('_engineer'):block+='\t-SpawnActorOnDeath:\n'
  if id in ('i_harvester','f_gatherer'):block+=f'\tWithHarvesterSpriteBody:\n\t\tImageByFullness: {id}\n'
  if id not in exclusive:rules.append(f'{id.upper()}.DEATH:\n\tInherits: ^SF_ANIMATED_DEATH\n\tRenderSprites:\n\t\tImage: {id}_death\n')
 rules.append(block)
for actor,suffix in [('FACT','yard'),('MCV','mcv'),('MCV.Husk','mcv'),('MCV.SFDEATH','mcv_death'),('HARV.EmptyHusk','collector_death'),('HARV.FullHusk','collector_death')]:
 block=actor+':\n\tRenderSprites:\n\t\tFactionImages:\n'
 for fid,*_ in FACTIONS:
  image=fid[0]+'_'+suffix
  if suffix=='collector_death':image='i_harvester' if fid[0]=='i' else 'f_gatherer'
  block+=f'\t\t\t{fid}: {image}\n'
 rules.append(block)
(MOD/'rules/70-painted-realms.yaml').write_text('\n'.join(rules),encoding='utf-8')
