"""Generate four original tech trees. GPL-3.0-or-later.

Veilborn is authored but hidden from the normal lobby until campaign progression
is available. The other three realms are unrestricted skirmish choices.
"""
import json
import re
from pathlib import Path
from additional_realms_data import REALMS, STRUCTURES, UNITS, YARDS, MCVS, DOCTRINES
from build_new_realms import blocks, traits

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / 'mods/sevenfall'

def main():
    source = {}
    for path in sorted((MOD/'rules').glob('*.yaml')):
        if path.name in ('80-additional-realms.yaml', '90-alpha.yaml'): continue
        for key, body in blocks(path.read_text(encoding='utf-8')).items():
            source[key] = source.get(key, '') + body
    out, weapons, fluent, records = [], [], [], []
    def text(actor, name, description):
        key='sf-extra-'+actor.replace('_','-')
        fluent.extend([f'{key}-name = {name}', f'{key}-description = {description}'])
        return f'\tTooltip:\n\t\tName: {key}-name\n', key
    for p, realm in REALMS.items():
        family, faction = realm['family'], realm['faction']
        def remap(s):
            return re.sub(r'\bh_(\w+)', lambda m:p+'_'+m[1], s, flags=re.I).replace('sf.humans','sf.'+family)
        for suffix, name in zip(STRUCTURES, realm['buildings']):
            actor=p+'_'+suffix; parent='H_'+suffix.upper(); ts=traits(source[parent])
            tip,key=text(actor,name, f'{realm["name"]} {suffix}.')
            b=f'{actor.upper()}:\n\tInherits: {parent}\n'+tip
            for trait in ('Buildable','ProvidesPrerequisite@buildingname','FreeActor'):
                if trait in ts:
                    values=remap(ts[trait]).rstrip()+'\n'
                    values=re.sub(r'(Description:) .*',r'\1 '+key+'-description',values)
                    b+='\t'+trait+':\n'+values
            b+=f'\tRenderSprites:\n\t\tImage: {actor}\n\t\tPalette: sf_rgba\n'
            if suffix=='cataclysm':
                # Do not inherit the human tech prerequisite from H_TECH.
                b+=f'\tProvidesPrerequisite@buildingname:\n\t\tPrerequisite: {actor}\n'
                powerkey='sf-extra-power-'+p
                fluent.extend([f'{powerkey}-name = '+{'Bloom':'Bloom','Restoration':'Restoration','AbsoluteSilence':'Absolute Silence','Earthbreaker':'Earthbreaker'}[realm['power']],
                    f'{powerkey}-description = '+{'v':'Temporarily protects allied combat units and slows enemies inside the target area.', 'u':'Consumes up to six own memory remnants in the target area to restore temporary infantry for thirty seconds.', 'o':'Suppresses enemy weapons and faction abilities for twelve seconds; movement remains possible.', 'n':'Deals heavy damage to enemy buildings and ground troops. Aircraft are immune.'}[p]])
                b+=f'\tSFFactionPower:\n\t\tKind: {realm["power"]}\n\t\tOrderName: SFExtra{realm["power"]}Order\n\t\tRadius: 5\n\t\tIconImage: {actor}\n\t\tName: {powerkey}-name\n\t\tDescription: {powerkey}-description\n'
            out.append(b)
            records.append(dict(id=actor,name=name,kind='building',realm=family,prefix=p,role=suffix))
        for suffix,name,kind,cost,hp,speed,damage,range_,reload,description in UNITS[p]:
            actor=p+'_'+suffix
            parent={'infantry':'H_RIFLEMAN','rocket':'H_ROCKETEER','vehicle':'H_BULWARK','air':'H_GUNSHIP','beast':'H_WARHOUND','engineer':'H_ENGINEER','harvester':'H_HARVESTER'}[kind]
            tip,key=text(actor,name,description)
            factory={'infantry':'barracks','rocket':'barracks','vehicle':'motorpool','air':'helipad','beast':'kennel','engineer':'barracks','harvester':'motorpool'}[kind]
            queue={'air':'Aircraft','vehicle':'Vehicle','harvester':'Vehicle'}.get(kind,'Infantry')
            b=f'{actor.upper()}:\n\tInherits: {parent}\n'+tip+f'\tBuildable:\n\t\tQueue: {queue}\n\t\tPrerequisites: {p}_{factory}, ~sf.{family}, ~techlevel.low\n\t\tDescription: {key}-description\n\tValued:\n\t\tCost: {cost}\n\tHealth:\n\t\tHP: {hp}\n\t'+('Aircraft' if kind=='air' else 'Mobile')+f':\n\t\tSpeed: {speed}\n\tRenderSprites:\n\t\tImage: {actor}\n\t\tPalette: sf_rgba\n\tSpawnActorOnDeath@SF_ANIMATION:\n\t\tActor: {actor}.death\n'
            if kind=='engineer': b+='\t-SpawnActorOnDeath:\n'
            if kind=='air': b+='\tSFFactionIdentity:\n\tSFSuppressionState:\n\t\tRequiresCondition: sf-null\n\tExternalCondition@sf-null:\n\t\tCondition: sf-null\n\t\tTotalCap: 2\n\t\tSourceCap: 1\n'
            if kind=='harvester':b+=f'\tWithHarvesterSpriteBody:\n\t\tImageByFullness: {actor}\n'
            if kind in ('vehicle','harvester','air'):b+=f'\tRepairable:\n\t\tRepairActors: {p}_service\n'
            if kind not in ('engineer','harvester'):
                if kind=='rocket': pairs=[('PRIMARY','SF_RocketeerAA'),('SECONDARY','SF_RocketeerAG'),('GARRISONED','SF_RocketeerAA'),('GARRISONEDSECONDARY','SF_RocketeerAG')]
                elif kind in ('vehicle','air'):pairs=[('', 'SF_h_gunship' if kind=='air' else 'SF_Judgment')]
                else:pairs=[('PRIMARY','SF_HellClaw' if kind=='beast' else 'SF_PulseRifle'),('GARRISONED','SF_HellClaw' if kind=='beast' else 'SF_PulseRifle')]
                generated=set()
                for slot, donor in pairs:
                    w='SF_'+actor+('_AA' if donor.endswith('AA') else '')
                    b+='\tArmament'+('@'+slot if slot else '')+f':\n\t\tWeapon: {w}\n'
                    if w not in generated:
                        weapons.append(f'{w}:\n\tInherits: {donor}\n\tRange: {range_}\n\tReloadDelay: {reload}\n\tWarhead@1Dam: SpreadDamage\n\t\tDamage: {damage}\n')
                        generated.add(w)
                if p=='u' and suffix!='special':b+='\tSpawnActorOnDeath@MEMORY:\n\t\tActor: u_remnant\n\t\tOwnerType: Victim\n\t\tSpawnAfterDefeat: False\n'
            if (p,suffix) in [('v','special'),('o','special')]:b+='\tDetectCloaked:\n\t\tRange: 5c0\n\tRevealsShroud:\n\t\tRange: 8c0\n'
            if (p,suffix)==('o','rifleman'):b+='\tCloak:\n\t\tInitialDelay: 75\n\t\tCloakDelay: 75\n\t\tUncloakOn: Attack, Damage\n\t\tCloakStyle: Alpha\n\t\tRequiresCondition: !sf-null && !sf-petrified\n'
            out.extend([b,f'{actor.upper()}.DEATH:\n\tInherits: ^SF_ANIMATED_DEATH\n\tRenderSprites:\n\t\tImage: {actor}_death\n'])
            records.append(dict(id=actor,name=name,kind=kind,realm=family,prefix=p,role=suffix,description=description,cost=cost,hp=hp,damage=damage))
        for suffix,names in [('yard',YARDS),('mcv',MCVS)]:
            records.append(dict(id=p+'_'+suffix,name=names[p],kind='building' if suffix=='yard' else 'vehicle',realm=family,prefix=p,role=suffix))
    # A powered network node uses the same low-power lifecycle as support installations.
    out.append('V_RESONATOR:\n\tInherits: V_RADAR\n\tInherits@DISABLE: ^DisableOnLowPowerOrPowerDown\n\tBuildable:\n\t\tPrerequisites: v_radar, ~sf.veilborn, ~techlevel.medium\n\tTooltip:\n\t\tName: sf-extra-resonator-name\n\tValued:\n\t\tCost: 800\n\tPower:\n\t\tAmount: -40\n\tProvidesPrerequisite@buildingname:\n\t\tPrerequisite: v_resonator\n\tSFResonanceSource:\n\t\tRequiresCondition: !disabled && !build-incomplete && !sf-petrified\n')
    fluent.append('sf-extra-resonator-name = Resonator')
    out.append('V_RESONATOR:\n\tRenderSprites:\n\t\tImage: v_resonator\n')
    out.append('U_REMNANT:\n\tInherits: ^SF_ANIMATED_DEATH\n\tRenderSprites:\n\t\tImage: u_rifleman_death\n\tKillsSelf:\n\t\tDelay: 500\n\t\tRemoveInstead: True\n')
    out.append('U_MEMORY_ECHO:\n\tInherits: U_RIFLEMAN\n\t-Buildable:\n\t-SpawnActorOnDeath@MEMORY:\n\t-Passenger:\n\t-GainsExperienceMultiplier:\n\tValued:\n\t\tCost: 0\n\tTooltip:\n\t\tName: sf-extra-memory-echo-name\n\tKillsSelf:\n\t\tDelay: 750\n\t\tRemoveInstead: True\n')
    fluent.append('sf-extra-memory-echo-name = Restored Memory (temporary)')
    # Metadata is authored as an overlay, leaving the existing twenty choices intact.
    world='^BaseWorld:\n'
    for p,r in REALMS.items():
        fid=r['faction'];key='sf-extra-faction-'+p
        world+=f'\tFaction@{fid}:\n\t\tName: {key}-name\n\t\tInternalName: {fid}\n\t\tSide: {r["name"]}\n\t\tDescription: {key}-description\n'
        if p=='v':world+='\t\tSelectable: False\n'
        fluent.extend([f'{key}-name = {r["name"]}',f'{key}-description = {DOCTRINES[p]}'])
    base=(MOD/'rules/10-factions.yaml').read_text(encoding='utf-8')
    start=re.search(r'StartingUnits@mcvonly:\n\t\tFactions: ([^\n]+)',base)[1]
    pool=re.search(r'RandomFactionMembers: ([^\n]+)',base)[1]
    out.append('World:\n\tStartingUnits@mcvonly:\n\t\tFactions: '+start+', '+', '.join(r['faction'] for r in REALMS.values())+'\n')
    world+='\tFaction@sf_random:\n\t\tRandomFactionMembers: '+pool+', '+', '.join(r['faction'] for p,r in REALMS.items() if p!='v')+'\n'
    out.append(world)
    fact='FACT:\n\tSFResonanceSource:\n\t\tRequiresCondition: !build-incomplete && !sf-petrified\n'
    for r in REALMS.values():fact+=f'\tProvidesPrerequisite@sf_{r["family"]}:\n\t\tFactions: {r["faction"]}\n\t\tPrerequisite: sf.{r["family"]}\n'
    out.append(fact)
    for actor,suffix in [('FACT','yard'),('MCV','mcv'),('MCV.Husk','mcv'),('MCV.SFDEATH','mcv_death'),('HARV.EmptyHusk','harvester'),('HARV.FullHusk','harvester')]:
        out.append(actor+':\n\tRenderSprites:\n\t\tFactionImages:\n'+''.join(f'\t\t\t{r["faction"]}: {p}_{suffix}\n' for p,r in REALMS.items()))
    # All providers participate in bot construction and normal paid production.
    ai='Player:\n'
    oldtraits=traits(blocks((MOD/'rules/65-new-realms.yaml').read_text(encoding='utf-8'))['Player'])
    for t in ('McvManagerBotModule','HarvesterBotModule','BaseBuilderBotModule','UnitBuilderBotModule'):
        body=oldtraits[t]
        def extend(m):
            values=m[2].split(', ');extra=[p+'_'+v[2:] for v in values if v.startswith('h_') and v[2:] in STRUCTURES+['harvester'] for p in REALMS]
            return m[1]+', '.join(dict.fromkeys(values+extra))
        body=re.sub(r'(?m)^(\t\t\w+Types: )([^\n]+)',extend,body)
        body=re.sub(r'(?m)^(\t\t\t)h_(\w+): (\d+)$',lambda m:m[0]+''.join(f'\n{m[1]}{p}_{m[2]}: {m[3]}' for p in REALMS) if m[2] in STRUCTURES+['harvester','rifleman','rocketeer','bulwark'] else m[0],body)
        if t=='UnitBuilderBotModule':body=body.replace('\t\tUnitsToBuild:\n','\t\tUnitsToBuild:\n'+''.join(f'\t\t\t{p}_{s}: 15\n' for p in REALMS for s in ['special','air','beast'])+'\t\t\tn_attendant: 25\n')
        if t=='BaseBuilderBotModule':
            body=body.replace('\t\tBuildingFractions:\n','\t\tBuildingFractions:\n'+''.join(f'\t\t\t{p}_{s}: {w}\n' for p in REALMS for s,w in [('helipad',8),('kennel',5),('tech',5),('cataclysm',2)]))
            body=body.replace('\t\tBuildingLimits:\n','\t\tBuildingLimits:\n'+''.join(f'\t\t\t{p}_{s}: 1\n' for p in REALMS for s in ['helipad','kennel','cataclysm']))
        ai+='\t'+t+':\n'+body.rstrip()+'\n'
    out.append(ai)
    decisions='Player:\n\tSupportPowerBotModule@INDEPENDENT:\n\t\tRequiresCondition: sevenfall-ai\n\t\tDecisions:\n'
    for power,relation,targets,minimum in [('Bloom','Ally','GroundActor, AirborneActor',300),('Restoration','Ally','SFMemory',100),('AbsoluteSilence','Enemy','GroundActor, Structure, AirborneActor',300),('Earthbreaker','Enemy','GroundActor, Structure',300)]:
        decisions+=f'\t\t\t{power}:\n\t\t\t\tOrderName: SFExtra{power}Order\n\t\t\t\tMinimumAttractiveness: {minimum}\n\t\t\t\tConsideration@targets:\n\t\t\t\t\tAgainst: {relation}\n\t\t\t\t\tTypes: {targets}\n\t\t\t\t\tAttractiveness: 100\n\t\t\t\t\tCheckRadius: 5c0\n'
    out.append(decisions)
    out.append('U_REMNANT:\n\tHealth:\n\t\tHP: 3000\n\tTargetable:\n\t\tTargetTypes: Ground, SFMemory\n')
    out.append('^Building:\n\tExternalCondition@EXTRA_quiet:\n\t\tCondition: sf-quiet\n\t\tTotalCap: 1\n\t\tSourceCap: 1\n\tFirepowerMultiplier@EXTRA_quiet:\n\t\tModifier: 30\n\t\tRequiresCondition: sf-quiet\n')
    for base in ('^Infantry','^Vehicle','^Aircraft'):
        b=base+':\n'
        for condition,mods in {'growth':[('Damage',80)],'attended':[('Damage',85)],'isolation':[('Speed',125)],'bloom':[('Damage',65)],'quiet':[('Firepower',30)],'bloom-slow':[('Speed',65)]}.items():
            b+=f'\tExternalCondition@EXTRA_{condition}:\n\t\tCondition: sf-{condition}\n\t\tTotalCap: 1\n\t\tSourceCap: 1\n'
            for trait,value in mods:b+=f'\t{trait}Multiplier@EXTRA_{condition}:\n\t\tModifier: {value}\n\t\tRequiresCondition: sf-{condition}'+(' && !sf-null' if condition in ('growth','attended','isolation','bloom') else '')+'\n'
        out.append(b)
    merged={}
    for entry in out:
        for actor,body in blocks(entry).items(): merged[actor]=merged.get(actor,'')+body
    (MOD/'rules/80-additional-realms.yaml').write_text('\n'.join(actor+':\n'+body for actor,body in merged.items()),encoding='utf-8')
    (MOD/'weapons/additional-realms.yaml').write_text('\n'.join(weapons),encoding='utf-8')
    (MOD/'fluent/additional-realms.ftl').write_text('\n'.join(fluent)+'\n',encoding='utf-8')
    (ROOT/'design/ADDITIONAL_REALMS_ROSTER.json').write_text(json.dumps(dict(realms=REALMS,assets=records),indent=2)+'\n',encoding='utf-8')
    print(f'Generated {len(records)} original roster entries across four realms.')

if __name__=='__main__':main()
