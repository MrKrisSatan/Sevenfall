"""Shared aircraft, beasts and cataclysms for all five parent realms."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; MOD=ROOT/'mods/sevenfall'
REALMS={
 'h':('humans','h_barracks','Bastion Gunship','Ironjaw Warhound','Strategic Missile Silo','Nuclear',6),
 'a':('angels','a_chapel','Sky Warden','Covenant Gryphon','Throne of Witness','Petrification',4),
 'd':('demons','d_pit','Ash Wyvern','Cinder Hound','Hellmouth Crucible','Hellrift',5),
 'i':('machine','i_barracks','Vector Interceptor','Logic Stalker','Extinction Array','Extinction',5),
 'f':('fallen','f_chapel','Mourning Kite','Carrion Chimera','Sepulchral Crown','Rapture',5)}
AIR={'h':('gunship',22000,145,1600,3600,40),'a':('skywarden',30000,115,1900,6500,70),'d':('wyvern',24000,135,1400,4200,48),'i':('interceptor',18000,190,1700,3000,25),'f':('bonekite',28000,125,1800,5800,65)}
BEAST={'h':('warhound',7500,140,250,1800,20),'a':('gryphon',24000,95,650,4800,45),'d':('hellhound',13000,125,400,3000,28),'i':('stalker',16000,135,550,2500,25),'f':('carrion',30000,85,750,6000,50)}
def main():
 rules=[];weapons=[];ftl=[]
 def text(key,name,desc):ftl.extend([f'{key}-name = {name}',f'{key}-description = {desc}'])
 for p,(family,barracks,airname,beastname,powername,power,radius) in REALMS.items():
  if p in 'if':
   for suffix,parent,name,prereq in [('helipad','H_HELIPAD' if p=='i' else 'A_HELIPAD','Vector Launch Deck' if p=='i' else 'Mourning Roost',p+'_radar'),('kennel','H_KENNEL' if p=='i' else 'A_KENNEL','Quadruped Assembly' if p=='i' else 'Carrion Cradle',barracks)]:
    id=p+'_'+suffix;key='sf-completion-'+id.replace('_','-');text(key,name,'Produces shared '+('aircraft.' if suffix=='helipad' else 'beasts.'))
    rules.append(f'''{id.upper()}:
	Inherits: {parent}
	RenderSprites:
		Image: {id}
	Buildable:
		Prerequisites: {prereq}, ~sf.{family}, ~techlevel.medium
		Description: {key}-description
	Tooltip:
		Name: {key}-name
	ProvidesPrerequisite@buildingname:
		Prerequisite: {id}
''')
  for kind,values,name in [('air',AIR[p],airname),('beast',BEAST[p],beastname)]:
   suffix,hp,speed,cost,damage,reload=values;id=p+'_'+suffix;key='sf-completion-'+id.replace('_','-')
   desc=('Armed hovering aircraft; vulnerable to dedicated anti-air.' if kind=='air' else 'Ground beast trained at the faction kennel; melee combat and scouting.')
   text(key,name,desc)
   common=f'''	RenderSprites:
		Image: {id}
		Palette: sf_rgba
	Buildable:
		Queue: {'Aircraft' if kind=='air' else 'Infantry'}
		BuildAtProductionType: {'Helicopter' if kind=='air' else 'Dog'}
		BuildPaletteOrder: 110
		Prerequisites: {p}_{'helipad' if kind=='air' else 'kennel'}, ~sf.{family}, ~techlevel.medium
		Description: {key}-description
	Tooltip:
		Name: {key}-name
	Valued:
		Cost: {cost}
	Health:
		HP: {hp}
	SpawnActorOnDeath@SF_ANIMATION:
		Actor: {id}.death
'''
   if kind=='air':
    rules.append(f'''{id.upper()}:
	Inherits: ^Helicopter
	Inherits@AUTOTARGET: ^AutoTargetAllAssaultMove
{common}	-SpawnActorOnDeath:
	-EjectOnDeath:
	Aircraft:
		Speed: {speed}
		TurnSpeed: 24
		CruiseAltitude: 1c512
		Crushes: crate
		PauseOnCondition: sf-petrified
	RevealsShroud:
		Range: 8c0
		Type: GroundPosition
	Armament:
		Weapon: SF_{id}
	WithFacingSpriteBody:
		Sequence: move
	WithAttackAnimation:
		Sequence: shoot
		RequiresCondition: !sf-petrified
	AttackAircraft:
		AttackType: Hover
		FacingTolerance: 80
		PauseOnCondition: sf-petrified
	AutoTarget:
		InitialStance: AttackAnything
		InitialStanceAI: AttackAnything
	Repairable:
		RepairActors: {p}_service
''')
    weapons.append(f'''SF_{id}:
	Inherits: HellfireAA
	ReloadDelay: {reload}
	Range: {'7c0' if p=='i' else '5c0'}
	Burst: 1
	ValidTargets: GroundActor, WaterActor, AirborneActor
	Warhead@1Dam: SpreadDamage
		ValidTargets: GroundActor, WaterActor, AirborneActor
		Damage: {damage}
''')
   else:
    rules.append(f'''{id.upper()}:
	Inherits: H_RIFLEMAN
{common}	-Passenger:
	-GainsExperienceMultiplier:
	Mobile:
		Speed: {speed}
	Armament@PRIMARY:
		Weapon: SF_{id}
	Armament@GARRISONED:
		Weapon: SF_{id}
''')
    weapons.append(f'''SF_{id}:
	Inherits: SF_HellClaw
	ReloadDelay: {reload}
	Warhead@1Dam: SpreadDamage
		Damage: {damage}
		Versus:
			Light: {100 if p in 'aif' else 45}
			Heavy: {85 if p in 'af' else 20}
''')
   rules.append(f'{id.upper()}.DEATH:\n\tInherits: ^SF_ANIMATED_DEATH\n\tRenderSprites:\n\t\tImage: {id}_death\n')
  id=p+'_cataclysm';key='sf-completion-'+id.replace('_','-')
  desc={'h':'Launches a nuclear missile. Five-second warning; damages all units and structures in six cells, including allies.',
   'a':'A six-winged Witness unfolds above the target. After five seconds, all units and buildings in four cells become immobile salt statues and crumble four seconds later, including allies.',
   'd':'Opens a Hellrift after five seconds, burning enemy units and structures in five cells.',
   'i':'An orbital Extinction strike pulses three times against enemies in five cells, disrupting their combat systems.',
   'f':'The Sepulchral Rapture tears at enemy armies and suppresses their miracles for thirty seconds.'}[p]
  text(key,powername,desc);text('sf-shared-'+p,power if p!='a' else 'Witness of Salt',desc)
  rules.append(f'''{id.upper()}:
	Inherits: {p.upper()}_TECH
	Inherits@POWER: ^DisableOnLowPowerOrPowerDown
	RenderSprites:
		Image: {"h_tech" if p=="h" else id}
	Buildable:
		Queue: Building
		BuildPaletteOrder: 125
		BuildLimit: 1
		Prerequisites: {p}_tech, ~sf.{family}, ~techlevel.high
		Description: {key}-description
	Tooltip:
		Name: {key}-name
	Valued:
		Cost: 6000
	Health:
		HP: 80000
	Power:
		Amount: -250
	SupportPowerChargeBar:
	SFFactionPower:
		Kind: {power}
		Radius: {radius}
		WarningTicks: 125
		OrderName: SFShared{power}Order
		ChargeInterval: 7500
		IconImage: {"h_tech" if p=="h" else id}
		Icon: icon
		IconPalette: sf_rgba
		Name: sf-shared-{p}-name
		Description: sf-shared-{p}-description
		PauseOnCondition: disabled || build-incomplete || sf-petrified
		DisplayTimerRelationships: Ally, Enemy
		DisplayRadarPing: True
''')
 # Give all health-bearing base families petrification, including future content.
 for parent in ['^Infantry','^Vehicle','^Ship','^Building','^NeutralPlane','^SF_TREE','^SF_BRIDGE']:
  rules.append(f'''{parent}:
	SFPetrifiable:
	ExternalCondition@PETRIFIED:
		Condition: sf-petrified
		SourceCap: 1
		TotalCap: 1
	WithColoredOverlay@PETRIFIED:
		Color: E8E5DFFF
		RequiresCondition: sf-petrified
	DamageMultiplier@PETRIFIED:
		Modifier: 0
		RequiresCondition: sf-petrified
	FirepowerMultiplier@PETRIFIED:
		Modifier: 0
		RequiresCondition: sf-petrified
''')
 for parent in ['^Infantry','^Vehicle','^Ship']:
  rules.append(f'{parent}:\n\tMobile:\n\t\tPauseOnCondition: '+('being-captured || ' if parent=='^Vehicle' else '')+'sf-petrified\n')
 rules.append('^NeutralPlane:\n\tAircraft:\n\t\tPauseOnCondition: sf-petrified\n')
 rules.append('^Building:\n\tPowerMultiplier@PETRIFIED:\n\t\tModifier: 0\n\t\tRequiresCondition: sf-petrified\n')
 producers=['FACT','A_CHAPEL','H_BARRACKS','D_PIT','I_BARRACKS','F_CHAPEL','A_ARMORY','H_MOTORPOOL','D_FORGE','I_MOTORPOOL','F_ARMORY']
 producers += [p.upper()+'_'+suffix for p in REALMS for suffix in ['HELIPAD','KENNEL']]
 producers += [p.upper()+'_'+suffix for p in 'ahd' for suffix in ['AIRFIELD','NAVAL']]
 for actor in producers:rules.append(actor+':\n\tProduction:\n\t\tPauseOnCondition: sf-petrified\n')
 bot='Player:\n\tUnitBuilderBotModule:\n\t\tUnitsToBuild:\n'
 for p in REALMS:
  bot+=f'\t\t\t{p}_{AIR[p][0]}: 12\n\t\t\t{p}_{BEAST[p][0]}: 18\n'
 bot+='\tBaseBuilderBotModule:\n\t\tBuildingFractions:\n'
 for p in REALMS:
  for suffix,weight in [('helipad',8),('kennel',5),('tech',5),('cataclysm',2)]:bot+=f'\t\t\t{p}_{suffix}: {weight}\n'
 bot+='\t\tBuildingLimits:\n'
 for p in REALMS:
  for suffix in ['helipad','kennel','cataclysm']:bot+=f'\t\t\t{p}_{suffix}: 1\n'
 bot+='\tSupportPowerBotModule@SHARED:\n\t\tRequiresCondition: sevenfall-ai\n\t\tDecisions:\n'
 for p,(_,_,_,_,_,power,radius) in REALMS.items():
  bot+=f'\t\t\t{power}:\n\t\t\t\tOrderName: SFShared{power}Order\n\t\t\t\tMinimumAttractiveness: 300\n\t\t\t\tConsideration@targets:\n\t\t\t\t\tAgainst: Enemy\n\t\t\t\t\tTypes: GroundActor, Structure, AirborneActor\n\t\t\t\t\tAttractiveness: 100\n\t\t\t\t\tCheckRadius: {radius}c0\n'
 rules.append(bot)
 # Merge overlay blocks deterministically rather than duplicate actor keys.
 merged={}
 for block in rules:
  head,body=block.split(':\n',1);merged[head]=merged.get(head,'')+body
 (MOD/'rules/75-realm-completion.yaml').write_text('\n'.join(k+':\n'+v for k,v in merged.items()))
 (MOD/'weapons/realm-completion.yaml').write_text('\n'.join(weapons))
 (MOD/'fluent/realm-completion.ftl').write_text('\n'.join(ftl)+'\n')
if __name__=='__main__':main()
