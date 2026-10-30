"""Original Noetic Assembly and Forsaken Host gameplay. GPL-3.0-or-later.

Uses explicitly identified existing Sevenfall animated bodies for this gameplay pass.
No film characters, designs, dialogue or external game assets are imported.
"""
from pathlib import Path
import re
import json

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT/'mods/sevenfall'
FACTIONS = [
 ('i_echo','Echo Directorate','Noetic Assembly','Patient reconnaissance and precision. After three seconds stationary, combat units gain 30% damage and 15% range.'),
 ('i_iron','Iron Calculus','Noetic Assembly','Armored attrition. Combat units take 20% less damage but move 15% slower.'),
 ('i_grid','Custodian Grid','Noetic Assembly','Network formations. Within four cells of a Relay Walker, combat units reload 20% faster and take 10% less damage.'),
 ('i_paradox','Paradox Collegium','Noetic Assembly','Experimental skirmishers. Below half health, combat units move 30% faster and reload 15% faster; avoid sustained trades.'),
 ('f_thrones','Ashen Thrones','Forsaken Host','Fallen aristocrats. After four seconds stationary, combat units take 30% less damage but attack 15% slower.'),
 ('f_choir','Hollow Choir','Forsaken Host','Corrupted procession. Within four cells of a Lamentor, combat units deal 25% more damage but take 10% more damage.'),
 ('f_scars','Carrion Testament','Forsaken Host','Wounded berserkers. Below half health, combat units deal 40% more damage and move 15% faster.'),
 ('f_wings','Broken Firmament','Forsaken Host','Isolated hunters. With no other friendly combat unit within four cells, gain 25% speed and 20% range.'),
]
# faction, id, name, source body, cost, hp, speed, weapon, damage, range, reload, role
UNITS = [
 ('i_echo','i_ghost','Mnemonic Ghost','H_RANGER',480,6000,110,'SF_PulseRifle',950,'6c0',32,'Reconnaissance infantry; detects cloaked targets within three cells. Fragile under focus fire.'),
 ('i_echo','i_lance','Needle Chassis','H_BULWARK',1350,30000,88,'SF_Judgment',7500,'7c0',85,'Mobile precision gun. Long reload and low armor demand a screen.'),
 ('i_iron','i_endurer','Endurer','H_RIFLEMAN',340,14500,62,'SF_PulseRifle',1200,'4c0',30,'Expensive armored infantry; powerful in sustained exchanges but easily outmaneuvered.'),
 ('i_iron','i_crucible','Crucible Engine','H_BULWARK',1900,82000,48,'SF_Judgment',10000,'5c0',90,'Slow siege chassis with exceptional health and high replacement cost.'),
 ('i_grid','i_thread','Threadkeeper','H_ROCKETEER',400,7000,82,'SF_RocketeerAG',2500,'5c0',50,'Anti-armor network infantry. Escort a relay rather than fighting alone.'),
 ('i_grid','i_relay','Relay Walker','H_BULWARK',1100,39000,72,'SF_PulseRifle',1800,'5c0',25,'Four-cell command relay. Killing it removes the Grid formation advantage.'),
 ('i_paradox','i_savant','Circuit Savant','H_RIFLEMAN',260,5000,115,'SF_PulseRifle',650,'5c0',18,'Fast experimental infantry; fragile but dangerous in short exchanges.'),
 ('i_paradox','i_gambit','Gambit Rover','H_BULWARK',850,23000,125,'SF_Judgment',4200,'5c0',50,'Fast harassment vehicle; withdraw wounded survivors rather than trading with tanks.'),
 ('f_thrones','f_regent','Uncrowned Regent','A_WATCHER',650,22000,52,'SF_HaloLance',2400,'4c0',48,'Armored fallen noble. Slow, costly infantry built to hold a position.'),
 ('f_thrones','f_reliquary','Walking Reliquary','A_AEGIS',1750,78000,45,'SF_Judgment',11500,'6c0',105,'Bone-bound siege abomination; vulnerable while repositioning.'),
 ('f_choir','f_canticle','Mute Canticle','A_WATCHER',240,6500,78,'SF_HaloLance',1000,'4c0',28,'Cheap ranged procession infantry; needs a Lamentor to reach full damage.'),
 ('f_choir','f_lamentor','Lamentor','A_AEGIS',1200,33000,65,'SF_HexBolt',4000,'6c0',60,'Four-cell profane hymn relay. The hymn amplifies damage dealt and received.'),
 ('f_scars','f_flayer','Vow Flayer','D_THRALL',250,10500,110,'SF_HellClaw',2400,'1c512',25,'Fast melee infantry that becomes more dangerous when wounded; kite it.'),
 ('f_scars','f_martyr','Carrion Martyr','D_RAVAGER',1100,55000,95,'SF_RavagerClaw',6500,'1c512',42,'Melee abomination with a lethal wounded phase; lacks a ranged attack.'),
 ('f_wings','f_pinions','Severed Pinion','A_WATCHER',400,7000,105,'SF_HaloLance',1500,'5c0',35,'Grounded hunter with shattered wings; split from the army to gain range and speed.'),
 ('f_wings','f_harrow','Harrow Stalker','A_AEGIS',1050,30000,110,'SF_Judgment',6000,'6c0',70,'Independent flanking hunter. Clumping removes its isolation bonus.'),
]
FAMILIES = {
 'i': ('machine','h','humans',{'generator':'Cognition Reactor','veilworks':'Matter Compiler','barracks':'Shell Foundry','motorpool':'Chassis Forge','advpower':'Fusion Stack','service':'Reconstruction Bay','radar':'Prediction Spire','tech':'Recursion Core','harvester':'Reclaimer','rifleman':'Shell Trooper','rocketeer':'Breach Automaton','bulwark':'Sentinel Chassis','engineer':'Repair Proxy','autocannon':'Sentry Node','missilenest':'Interceptor Node'}),
 'f': ('fallen','a','angels',{'spire':'Apostate Pyre','veilworks':'Ossuary Mill','chapel':'Profaned Chapel','armory':'Flesh Crucible','advpower':'Sundered Halo','service':'Suture Shrine','radar':'Blind Oracle','tech':'Testament Vault','gatherer':'Tithe Bearer','watcher':'Oath Husk','judicator':'Blight Herald','aegis':'Bonebound Engine','engineer':'Suture Keeper','watchfire':'Balefire Watch','judgment':'Wrath Organ','skyward':'Broken Halo Battery'})}
MODIFIERS = {'machine-iron':[('Damage',80),('Speed',85)],'machine-grid':[('ReloadDelay',80),('Damage',90)],'machine-paradox':[('Speed',130),('ReloadDelay',85)],'fallen-throne':[('Damage',70),('ReloadDelay',115)],'fallen-choir':[('Firepower',125),('Damage',110)],'fallen-scars':[('Firepower',140),('Speed',115)],'fallen-wings':[('Speed',125),('Range',120)]}

def blocks(text):
 return dict(re.findall(r'(?ms)^([^\s#][^\n]*):\n(.*?)(?=^[^\s#][^\n]*:\n|\Z)', text))
def traits(body):
 return dict(re.findall(r'(?ms)^\t([^\t\n][^\n]*):[^\n]*\n(.*?)(?=^\t[^\t\n]|\Z)',body))

def main():
 source={}
 for file in ('20-structures.yaml','25-support-structures.yaml','30-units.yaml','45-defenses.yaml','51-engineers.yaml'):
  source.update(blocks((MOD/'rules'/file).read_text(encoding='utf-8')))
 out=[]; fluent=[]; mappings={}; records=[]; weapons=[]
 weapon_source=blocks((MOD/'weapons/sevenfall.yaml').read_text(encoding='utf-8'))
 for prefix,(family,old,oldfamily,names) in FAMILIES.items():
  mapping={old+'_'+suffix:prefix+'_'+suffix for suffix in names}
  mappings.update(mapping)
  def remap(s):
   s=s.replace('sf.'+oldfamily,'sf.'+family)
   for a,b in mapping.items():s=re.sub(r'(?<![\w])'+a+r'(?![\w])',b,s,flags=re.I)
   return s
  for suffix,name in names.items():
   parent=(old+'_'+suffix).upper(); actor=prefix+'_'+suffix; body=source[parent]; ts=traits(body)
   b=f'{actor.upper()}:\n\tInherits: {parent}\n'
   # Rebind tech, free collectors, own building prerequisites and repair paths.
   for t in ('Buildable','ProvidesPrerequisite@buildingname','FreeActor'):
    if t in ts:b+='\t'+t+':\n'+remap(ts[t]).rstrip()+'\n'
   key=actor.replace('_','-')
   b=re.sub(r'(\t\tDescription:) .*',r'\1 sf-'+key+'-description',b)
   b+=f'\tTooltip:\n\t\tName: sf-{key}-name\n\tWithTextDecoration@REALM:\n\t\tText: '+('NOETIC' if prefix=='i' else 'FORSAKEN')+'\n\t\tPosition: Top\n\t\tRequiresSelection: True\n\t\tValidRelationships: Ally\n'
   if suffix in ('watcher','judicator','aegis','engineer') and prefix=='f':b+='\t-ChangesHealth@SF_RENEWAL:\n'
   if suffix=='service':b+='\tProvidesPrerequisite@sf_service:\n\t\tPrerequisite: sf_service\n'
   if suffix in ('rifleman','rocketeer','bulwark','watcher','judicator','aegis'):
    hp=int(re.search(r'\tHealth:\n\t\tHP: (\d+)',body)[1]);cost=int(re.search(r'\tValued:\n\t\tCost: (\d+)',body)[1])
    b+=f'\tHealth:\n\t\tHP: {int(hp*(1.2 if prefix=="i" else 1.1))}\n\tValued:\n\t\tCost: {int(cost*1.15)}\n'
    unique={}
    for trait,values in ts.items():
     if trait.startswith('Armament'):
      match=re.search(r'Weapon: (\w+)',values)
      if match and match[1] in weapon_source:
       original=match[1];new='SF_'+prefix+'_'+original[3:]
       b+=f'\t{trait}:\n\t\tWeapon: {new}\n'
       unique[new]=original
    for new,original in unique.items():
     damage=int(re.search(r'Damage: (\d+)',weapon_source[original])[1])
     weapons.append(f'{new}:\n\tInherits: {original}\n\tWarhead@1Dam: SpreadDamage\n\t\tDamage: {int(damage*(1.1 if prefix=="i" else 1.2))}\n')
   if suffix in ('harvester','gatherer','bulwark','aegis'):
    b+=f'\tRepairable:\n\t\tRepairActors: {prefix}_service\n'
   out.append(b)
   fluent += [f'sf-{key}-name = {name}',f'sf-{key}-description = {name}. '+('Noetic Assembly' if prefix=='i' else 'Forsaken Host')+' infrastructure or shared roster. Uses a temporary existing Sevenfall body.']
   records.append(dict(id=actor,name=name,parent=parent,realm=family))
 for faction,actor,name,parent,cost,hp,speed,weapon,damage,range_,reload,role in UNITS:
  family='machine' if faction[0]=='i' else 'fallen'; vehicle=parent in ('H_BULWARK','A_AEGIS','D_RAVAGER'); factory=('i_motorpool' if faction[0]=='i' else 'f_armory') if vehicle else ('i_barracks' if faction[0]=='i' else 'f_chapel')
  key=actor.replace('_','-'); w='SF_'+actor
  b=f'{actor.upper()}:\n\tInherits: {parent}\n\tBuildable:\n\t\tQueue: '+('Vehicle' if vehicle else 'Infantry')+f'\n\t\tPrerequisites: {factory}, ~sf.{faction}, ~techlevel.low\n\t\tBuildPaletteOrder: 85\n\t\tDescription: sf-{key}-description\n\tTooltip:\n\t\tName: sf-{key}-name\n\tValued:\n\t\tCost: {cost}\n\tHealth:\n\t\tHP: {hp}\n\tMobile:\n\t\tSpeed: {speed}\n\t'+('Armament' if vehicle else 'Armament@PRIMARY')+f':\n\t\tWeapon: {w}\n'
  if not vehicle:b+=f'\tArmament@GARRISONED:\n\t\tWeapon: {w}\n'
  if parent.startswith('A_'):b+='\t-ChangesHealth@SF_RENEWAL:\n'
  if parent.startswith('D_'):b+='\t-GrantConditionOnAttack@SF_FRENZY:\n\t-FirepowerMultiplier@SF_FRENZY:\n\t-SpeedMultiplier@SF_FRENZY:\n\t-WithColoredOverlay@SF_FRENZY:\n'
  if parent=='H_ROCKETEER':
   b+=f'\tArmament@SECONDARY:\n\t\tWeapon: {w}\n\tArmament@GARRISONEDSECONDARY:\n\t\tWeapon: {w}\n'
  b+=f'\tRenderSprites:\n\t\tImage: {actor}\n\tSpawnActorOnDeath@SF_ANIMATION:\n\t\tActor: {actor}.death\n'
  if actor=='i_ghost':b+='\tRevealsShroud:\n\t\tRange: 8c0\n\tDetectCloaked:\n\t\tRange: 3c0\n'
  b+=f'\tWithTextDecoration@REALM:\n\t\tText: {name.upper()}\n\t\tPosition: Top\n\t\tRequiresSelection: True\n\t\tValidRelationships: Ally\n'
  if vehicle:b+=f'\tRepairable:\n\t\tRepairActors: {faction[0]}_service\n'
  out.append(b)
  out.append(f'{actor.upper()}.DEATH:\n\tInherits: ^SF_ANIMATED_DEATH\n\tRenderSprites:\n\t\tImage: {actor}_death\n')
  weapons.append(f'{w}:\n\tInherits: {weapon}\n\tRange: {range_}\n\tReloadDelay: {reload}\n\tWarhead@1Dam: SpreadDamage\n\t\tDamage: {damage}\n')
  fluent += [f'sf-{key}-name = {name}',f'sf-{key}-description = {role} Exclusive to {dict((f[0],f[1]) for f in FACTIONS)[faction]}.']
 for base in ('^Infantry','^Vehicle'):
  b=base+':\n'
  for cond,mods in MODIFIERS.items():
   b+=f'\tExternalCondition@REALM_{cond}:\n\t\tCondition: sf-{cond}\n\t\tTotalCap: 1\n\t\tSourceCap: 1\n'
   for trait,value in mods:b+=f'\t{trait}Multiplier@REALM_{cond}:\n\t\tModifier: {value}\n\t\tRequiresCondition: sf-{cond} && !sf-null\n'
  out.append(b)
 # AI extends the existing bot lists, retaining every original faction.
 ai=(MOD/'rules/40-ai.yaml').read_text(encoding='utf-8')
 ai=ai[ai.index('Player:'):]
 def extend_line(m):
  indent,key,value=m.groups(); values=value.split(', '); extra=[mappings[v] for v in values if v in mappings]
  return indent+key+': '+', '.join(values+extra)
 ai=re.sub(r'(?m)^(\t\t)(\w+Types): (.+)$',extend_line,ai)
 ai=re.sub(r'(?m)^(\t\t\t)([ah]_\w+): (\d+)$',lambda m:m[0]+('\n'+m[1]+mappings[m[2]]+': '+m[3] if m[2] in mappings else ''),ai)
 ai=ai.replace('\t\tUnitsToBuild:\n','\t\tUnitsToBuild:\n'+''.join(f'\t\t\t{u[1]}: 25\n' for u in UNITS))
 out.append(ai)
 (MOD/'rules/65-new-realms.yaml').write_text('\n'.join(out),encoding='utf-8')
 (MOD/'weapons/new-realms.yaml').write_text('\n'.join(weapons),encoding='utf-8')
 f=MOD/'rules/10-factions.yaml';s=f.read_text(encoding='utf-8')
 for fid,name,side,desc in FACTIONS:
  key=fid.replace('_','-')
  if f'Faction@{fid}:' not in s:s=s.replace('\tFaction@sf_random:',f'\tFaction@{fid}:\n\t\tName: sf-faction-{key}-name\n\t\tInternalName: {fid}\n\t\tSide: {side}\n\t\tDescription: sf-faction-{key}-description\n\tFaction@sf_random:')
  fluent += [f'sf-faction-{key}-name = {name}',f'sf-faction-{key}-description = {side}: {desc}']
  if f'ProvidesPrerequisite@sf_{fid}:' not in s:s=s.replace('\nMCV:\n',f'\n\tProvidesPrerequisite@sf_{fid}:\n\t\tFactions: {fid}\n\t\tPrerequisite: sf.{fid}\n\nMCV:\n',1)
 for prefix,(family,old,_,_) in FAMILIES.items():
  ids=[f[0] for f in FACTIONS if f[0].startswith(prefix+'_')]
  if f'ProvidesPrerequisite@sf_{family}:' not in s:s=s.replace('\nMCV:\n',f'\n\tProvidesPrerequisite@sf_{family}:\n\t\tFactions: '+', '.join(ids)+f'\n\t\tPrerequisite: sf.{family}\n\nMCV:\n',1)
  # All start selections and random pool include the new realms.
  s=re.sub(r'(?m)^(\t+(?:Factions|RandomFactionMembers): )(.*)$',lambda m:m[1]+m[2]+''.join(', '+fid for fid in ids if fid not in m[2] and 'a_seraph' in m[2] and 'h_bastion' in m[2]),s)
  # Shared MCV/deployed yard art is explicit for each new choice.
  s=re.sub(r'(?m)^(\t\t\t'+('h_bastion' if prefix=='i' else 'a_seraph')+r': (.+))$',lambda m:m[0]+''.join('\n\t\t\t'+fid+': '+m[2] for fid in ids if '\t\t\t'+fid+':' not in s),s)
 f.write_text(s,encoding='utf-8')
 (MOD/'fluent/new-realms.ftl').write_text('\n'.join(fluent)+'\n',encoding='utf-8')
 (ROOT/'design/NEW_REALMS_ROSTER.json').write_text(json.dumps({'factions':FACTIONS,'units':UNITS,'shared':records},indent=2)+'\n',encoding='utf-8')
 print('Generated eight subfactions, sixteen exclusive units and two independent tech trees.')

if __name__=='__main__':main()
