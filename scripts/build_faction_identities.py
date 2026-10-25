"""Generate the twelve faction identity overlays from explicit, reviewable data.

Specialist units reuse Sevenfall's authored animated bodies, with visible role
labels/overlays. They do not introduce external-game sprites or claim new artwork.
"""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MOD=ROOT/'mods/sevenfall'
FACTIONS=[
 ('a_seraph','Seraphic Synod','Dawn','Spear of First Light','Charged precision volleys after standing still for three seconds.', 'a_seraphim','a_luminary','Luminary','A_JUDICATOR',800,11000,'SF_Luminary','SF_HaloLance','Infantry','a_chapel', 'a_tech',240),
 ('a_warden','Order of the Gate','Sanctuary','The Unbroken Gate','Gatekeepers and Wardbearers protect nearby allies; formation trades speed for armor.', 'a_gatekeeper','a_wardbearer','Wardbearer','A_WATCHER',600,18000,'SF_WardBolt','SF_HaloLance','Infantry','a_chapel','a_tech',210),
 ('a_exile','The Unshackled','Rebellion','Heaven in Revolt','Below half health, outcasts gain firepower and speed; exposed survivors reward aggressive retreats.', 'a_penitent','a_outrider','Exile Outrider','A_AEGIS',1000,35000,'SF_Outrider','SF_Sanction','Vehicle','a_armory','a_tech',180),
 ('a_desolation','Choir of Desolation','Requiem','Requiem for the Living','Human Congregant deaths empower angels inside Cantor and Shrine hymn networks.', 'a_congregant','a_cantor',None,None,0,0,None,None,None,None,'a_tech',240),
 ('h_bastion','Bastion Directorate','Barrage','Rolling Thunder','After four seconds stationary, troops entrench for armor and range; moving breaks the position.', 'h_siegegun','h_sapper','Bastion Sapper','H_ROCKETEER',300,5500,'SF_BreachCharge','SF_RocketeerAG','Infantry','h_barracks','h_tech',240),
 ('h_union','Free Earth Union','Relief','Emergency Airlift','Harvesters and Pathfinders project mobile supply corridors: faster movement and reloads.', 'h_ranger','h_pathfinder','Pathfinder','H_BULWARK',700,24000,'SF_Pathfinder','SF_PulseRifle','Vehicle','h_motorpool','h_tech',150),
 ('h_covenant','Ashen Covenant','Covenant','Ashes to Ashes','Templars and Confessors heal nearby infantry and harden their resolve.', 'h_templar','h_confessor','Ash Confessor','H_RIFLEMAN',450,8500,'SF_Confessor','SF_PulseRifle','Infantry','h_barracks','h_tech',210),
 ('h_area52','Area Fifty Two','Singularity','Project Event Horizon','Powered containment switches Janus weapons between SERAPH and ABYSS; null fields suppress supernatural abilities.', 'h_retrieval','h_janus',None,None,0,0,None,None,None,None,'h_tech',270),
 ('d_legion','Iron Legions','Furnace','The Ninth Furnace','Hellreavers and Taskmasters bind nearby troops into slow, armored siege formations.', 'd_hellreaver','d_taskmaster','Iron Taskmaster','D_CINDERLING',650,15000,'SF_Taskmaster','SF_Cinder','Infantry','d_pit','d_tech',270),
 ('d_brood','Blood Brood','Bloodtide','The Red Deluge','Enemy mobile-unit kills feed the killer: healing and six seconds of faster strikes; buildings grant no feeding.', 'd_skitter','d_goremaw','Goremaw','D_RAVAGER',800,38000,'SF_Goremaw','SF_RavagerClaw','Vehicle','d_forge','d_tech',180),
 ('d_court','Court of Whispers','Silence','The Nameless Silence','Hexers and Silencers curse enemies with slow movement and weakened damage for four seconds.', 'd_hexer','d_silencer','Silencer','D_CINDERLING',550,6500,'SF_Silencer','SF_Cinder','Infantry','d_pit','d_tech',240),
 ('d_contempt','Circle of Contempt','Verdict','The Final Verdict','Magistrates condemn priority targets; Contemptors punish wounded enemies and executions grant Ascendancy.', 'd_magistrate','d_contemptor',None,None,0,0,None,None,None,None,'d_tech',240),
]
POWER_DESCRIPTIONS={
 'Dawn':'After 3s, deals 15000 damage to enemy units and 25000 to buildings within 4 cells.',
 'Sanctuary':'After 3s, allies within 6 cells take 65% less damage and regenerate 2% HP per second for 15s.',
 'Rebellion':'After 3s, allied units within 6 cells gain 40% firepower and 50% speed for 20s, but take 20% more damage.',
 'Requiem':'After 3s, allied troops within 6 cells gain 45% firepower for 20s; enemy infantry are weakened and slowed for 12s.',
 'Barrage':'After 3s, three eastward-moving impacts at 1s intervals deal 9000 unit / 18000 building damage in 3-cell circles.',
 'Relief':'After 3s, repairs allied units by 30% maximum HP and grants 30% speed for 20s within 7 cells.',
 'Covenant':'After 3s, fully heals allied infantry and reduces incoming damage by 80% for 12s within 6 cells.',
 'Singularity':'After 3s, deals 12000 damage to enemies, locks all nearby troops for 6s, and nullifies supernatural abilities for 30s. Affects friendly troops too. Radius 5.',
 'Furnace':'After 3s, deals 65000 damage to enemy buildings and 10000 to troops within 4 cells; survivors move at 40% speed for 10s.',
 'Bloodtide':'After 3s, allied infantry within 7 cells heal 25% HP, regenerate 2% HP/sec and attack 35% faster for 30s.',
 'Silence':'After 3s, enemy units and defenses within 5 cells deal no weapon damage and troops cannot move for 12s. Does not disable superweapon charging.',
 'Verdict':'After 3s, enemy units below half HP suffer 25000 damage; others take 8000, buildings 15000. Nearby allies gain 45% firepower for 12s. Radius 5.',
}
MODIFIERS={
 'focus':[('Firepower',130),('Range',115)], 'aegis':[('Damage',75),('Speed',90)],
 'defiance':[('Firepower',135),('Speed',120)],'entrenched':[('Damage',80),('Range',115)],
 'logistics':[('Speed',115),('ReloadDelay',85)],'oath':[('Damage',90)],
 'iron':[('Damage',75),('Speed',85)],'fed':[('ReloadDelay',75),('Speed',115)],
 'whisper':[('Speed',65),('Firepower',75)],'sanctum':[('Damage',35)],
 'rebellion':[('Firepower',140),('Speed',150),('Damage',120)],'requiem':[('Firepower',145)],
 'relief':[('Speed',130)],'martyrguard':[('Damage',20)],'lockdown':[('Speed',0),('Firepower',0)],
 'scorched':[('Speed',40)],'bloodtide':[('ReloadDelay',65)],
}
SPECIALIST_ROLES={
 'a_luminary':'Long-range seven-cell light artillery in an infantry body; needs a screen and three seconds stationary for focused volleys.',
 'a_wardbearer':'Infantry shield relay. Projects the same four-cell non-stacking formation protection as a Gatekeeper.',
 'a_outrider':'Fast, lightly protected attack chassis. At low health Defiance improves speed and damage; kite rather than trade with heavy armor.',
 'h_sapper':'Short-range breaching rocket specialist. Strong against concrete; fragile during the approach.',
 'h_pathfinder':'Fast reconnaissance vehicle and six-cell mobile supply relay. Nearby allies move and reload faster.',
 'h_confessor':'Lightly armed battlefield medic. Projects a four-cell healing and protection oath for infantry.',
 'd_taskmaster':'Armored command infantry. Projects a four-cell siege formation that trades movement speed for protection.',
 'd_goremaw':'Heavy melee predator. Enemy troop kills restore health and accelerate its next hunt; vulnerable to kiting.',
 'd_silencer':'Fragile seven-cell curse specialist. Its attacks slow and weaken a victim, enabling the rest of the army to close.',
}
SPECIALIST_SPEEDS={'a_luminary':62,'a_wardbearer':58,'a_outrider':105,'h_sapper':82,'h_pathfinder':115,'h_confessor':82,'d_taskmaster':62,'d_goremaw':90,'d_silencer':92}
def main():
 out=['# Generated by scripts/build_faction_identities.py. Original faction identities.',
      'World:\n\tSFFactionPowerManager:']
 for base in ('^Infantry','^Vehicle','^Building'):
  block=[base+':']
  block+=['\tSFSuppressionState:', '\t\tRequiresCondition: sf-null', '\tExternalCondition@sf-null:', '\t\tTotalCap: 2', '\t\tSourceCap: 1']
  if base!='^Building':block+=['\tSFFactionIdentity:']
  for cond, modifiers in MODIFIERS.items():
   if base=='^Building' and cond not in ('whisper','lockdown'):continue
   block += [f'\tExternalCondition@IDENTITY_{cond}:',f'\t\tCondition: sf-{cond}','\t\tTotalCap: 1','\t\tSourceCap: 1']
   for trait,value in modifiers:
    if base=='^Building' and trait in ('Speed','Range','ReloadDelay'):continue
    block += [f'\t{trait}Multiplier@IDENTITY_{cond}:',f'\t\tModifier: {value}',f'\t\tRequiresCondition: sf-{cond}'+(' && !sf-null' if cond in ('focus','aegis','defiance','oath','fed','iron','sanctum','requiem','bloodtide') else '')]
   if base!='^Building':
    block += [f'\tWithTextDecoration@IDENTITY_{cond}:',f'\t\tText: {cond.upper()}','\t\tPosition: Top','\t\tRequiresSelection: True','\t\tValidRelationships: Ally',f'\t\tRequiresCondition: sf-{cond}']
  if base!='^Building':
   for cond in ('sanctum','bloodtide'):
    block += [f'\tChangesHealth@IDENTITY_{cond}:','\t\tStep: 0','\t\tPercentageStep: 2','\t\tDelay: 25','\t\tStartIfBelow: 100','\t\tDamageCooldown: 0',f'\t\tRequiresCondition: sf-{cond} && !sf-null']
  out.append('\n'.join(block))
 weapons=['# Generated original specialist weapons.']
 fluent=[]
 ai=['Player:\n\tBaseBuilderBotModule:\n\t\tBuildingLimits:']
 ai += [f'\t\t\t{p}_{kind}: 1' for p in ('a','h','d') for kind in ('radar','tech')]
 ai += [f'\t\t\tsf_{f[0]}_ultimate: 1' for f in FACTIONS]
 ai += ['\t\tBuildingFractions:']+[f'\t\t\t{p}_{kind}: {weight}' for p in ('a','h','d') for kind,weight in (('radar',5),('tech',3))]+[f'\t\t\tsf_{f[0]}_ultimate: 4' for f in FACTIONS]
 ai += ['\tUnitBuilderBotModule:\n\t\tUnitsToBuild:']
 ai += [f'\t\t\t{f[6]}: 20' for f in FACTIONS if f[7]]
 ai += ['\tSupportPowerBotModule@IDENTITIES:\n\t\tRequiresCondition: sevenfall-ai\n\t\tDecisions:']
 for f in FACTIONS:
  faction,name,kind,power,mechanic,first,unit,title,parent,cost,hp,weapon,weaponparent,queue,production,tech,seconds=f
  textkey=faction.replace('_','-')
  fluent += [f'sf-power-{textkey}-name = {power}',f'sf-power-{textkey}-description = {POWER_DESCRIPTIONS[kind]} Requires explored terrain; losing the installation, power or ownership during the warning cancels the strike. Recharge: {seconds}s.',f'sf-ultimate-{textkey}-name = {power} Array',f'sf-ultimate-{textkey}-description = {name} superweapon installation. Requires power; visible charge timer. One per player.']
  building=f'SF_{faction.upper()}_ULTIMATE'
  radius={'Dawn':4,'Sanctuary':6,'Rebellion':6,'Requiem':6,'Barrage':3,'Relief':7,'Covenant':6,'Furnace':4,'Bloodtide':7}.get(kind,5)
  out += [f'{building}:\n\tInherits: {tech.upper()}\n\tBuildable:\n\t\tQueue: Building\n\t\tBuildPaletteOrder: 120\n\t\tBuildLimit: 1\n\t\tPrerequisites: {tech}, ~sf.{faction}, ~techlevel.high\n\t\tDescription: sf-ultimate-{textkey}-description\n\tTooltip:\n\t\tName: sf-ultimate-{textkey}-name\n\tValued:\n\t\tCost: 4500\n\tHealth:\n\t\tHP: 65000\n\tPower:\n\t\tAmount: -150\n\tInherits@IDENTITY_POWER: ^DisableOnLowPowerOrPowerDown\n\tSupportPowerChargeBar:\n\tWithTextDecoration@IDENTITY:\n\t\tText: {power.upper()}\n\t\tPosition: Top\n\t\tRequiresSelection: True\n\t\tValidRelationships: Ally\n\tSFFactionPower:\n\t\tKind: {kind}\n\t\tRadius: {radius}\n\t\tOrderName: SF{kind}Order\n\t\tChargeInterval: {seconds*25}\n\t\tIconImage: {tech}\n\t\tIcon: icon\n\t\tIconPalette: sf_rgba\n\t\tName: sf-power-{textkey}-name\n\t\tDescription: sf-power-{textkey}-description\n\t\tPauseOnCondition: disabled || build-incomplete\n\t\tDisplayTimerRelationships: Ally, Enemy\n\t\tDisplayRadarPing: True']
  if title:
   damage={'a_luminary':6500,'a_wardbearer':2200,'a_outrider':4200,'h_sapper':5500,'h_pathfinder':1000,'h_confessor':1000,'d_taskmaster':3600,'d_goremaw':7500,'d_silencer':1600}[unit]
   ranges={'a_luminary':'7c0','a_wardbearer':'4c0','a_outrider':'5c0','h_sapper':'3c0','h_pathfinder':'5c0','h_confessor':'5c0','d_taskmaster':'4c0','d_goremaw':'1c512','d_silencer':'7c0'}
   # Inherit ground weapon primitives already authored for Sevenfall.
   weapons += [f'{weapon}:\n\tInherits: {weaponparent}\n\tRange: {ranges[unit]}\n\tReloadDelay: 45\n\tWarhead@1Dam: SpreadDamage\n\t\tDamage: {damage}']
   if unit=='h_sapper':weapons[-1]+='\n\t\tVersus:\n\t\t\tConcrete: 140\n\t\t\tWood: 100'
   slot='Armament@PRIMARY' if queue=='Infantry' else 'Armament'
   out += [f'{unit.upper()}:\n\tInherits: {parent}\n\tBuildable:\n\t\tQueue: {queue}\n\t\tBuildPaletteOrder: 88\n\t\tPrerequisites: {production}, ~sf.{faction}, ~techlevel.medium\n\t\tDescription: sf-{unit.replace("_","-")}-description\n\tTooltip:\n\t\tName: sf-{unit.replace("_","-")}-name\n\tValued:\n\t\tCost: {cost}\n\tHealth:\n\t\tHP: {hp}\n\t{slot}:\n\t\tWeapon: {weapon}\n\tWithTextDecoration@SPECIALIST:\n\t\tText: {title.upper()}\n\t\tPosition: Bottom\n\t\tRequiresSelection: False\n\t\tValidRelationships: Ally']
   # Rocket infantry expose separate ground/air armaments; match both field and garrison ground slots.
   if parent in ('A_JUDICATOR','H_ROCKETEER'):
    out[-1]=out[-1].replace(f'\t{slot}:\n\t\tWeapon: {weapon}',f'\tArmament@SECONDARY:\n\t\tWeapon: {weapon}\n\tArmament@GARRISONEDSECONDARY:\n\t\tWeapon: {weapon}')
   elif queue=='Infantry':out[-1]+=f'\n\tArmament@GARRISONED:\n\t\tWeapon: {weapon}'
   out[-1]+=f'\n\tMobile:\n\t\tSpeed: {SPECIALIST_SPEEDS[unit]}'
   if unit=='h_pathfinder':out[-1]+='\n\tRevealsShroud:\n\t\tRange: 9c0'
   fluent += [f'sf-{unit.replace("_","-")}-name = {title}',f'sf-{unit.replace("_","-")}-description = {SPECIALIST_ROLES[unit]}']
  friendly=kind in ('Sanctuary','Rebellion','Relief','Covenant','Bloodtide')
  targets='Infantry' if kind in ('Covenant','Bloodtide') else 'Infantry, Vehicle' if friendly else 'GroundActor, Structure'
  ai += [f'\t\t\t{kind}:\n\t\t\t\tOrderName: SF{kind}Order\n\t\t\t\tMinimumAttractiveness: 200\n\t\t\t\tConsideration@targets:\n\t\t\t\t\tAgainst: {"Ally" if friendly else "Enemy"}\n\t\t\t\t\tTypes: {targets}\n\t\t\t\t\tAttractiveness: 100\n\t\t\t\t\tCheckRadius: {radius}c0']
 out+=['\n'.join(ai)]
 (MOD/'rules/60-identities.yaml').write_text('\n\n'.join(out)+'\n',encoding='utf-8')
 (MOD/'weapons/identities.yaml').write_text('\n\n'.join(weapons)+'\n',encoding='utf-8')
 (MOD/'fluent/identities.ftl').write_text('\n'.join(fluent)+'\n',encoding='utf-8')
 # The faction picker describes the actual differentiator instead of repeating its parent bonus.
 source=(MOD/'fluent/sevenfall.ftl').read_text(encoding='utf-8')
 for faction,name,kind,power,mechanic,*_ in FACTIONS:
  key=f'sf-faction-{faction.replace("_","-")}-description = '
  source='\n'.join(key+mechanic+' Superweapon: '+power+'.' if line.startswith(key) else line for line in source.splitlines())+'\n'
 source=source.replace('Choose one of the nine playable hosts at random.','Choose one of the twelve playable hosts at random.')
 (MOD/'fluent/sevenfall.ftl').write_text(source,encoding='utf-8')
if __name__=='__main__':main()

