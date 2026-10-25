"""Generate the three additive subfaction prototypes and their original-art bindings."""
import json
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MOD=ROOT/'mods/sevenfall'
FACTIONS=[('a_desolation','Choir of Desolation','Angels','a_exile'),('h_area52','Area Fifty Two','Humans','h_covenant'),('d_contempt','Circle of Contempt','Demons','d_court')]
ENTRIES=[
 dict(id='a_congregant',name='Ashbound Congregant',faction='a_desolation',kind='unit',parent='A_WATCHER',cost=40,hp=2400,speed=85,role='Follower',weapon='SF_Congregant',description='Cheap human worshipper. Within five cells of a Cantor or Processional Shrine, Conviction reduces damage and prevents dread. Enemy-caused deaths charge nearby Choir angels: three stacks maximum, six seconds.'),
 dict(id='a_cantor',name='Cantor of Desolation',faction='a_desolation',kind='unit',parent='A_WATCHER',cost=750,hp=14000,speed=62,role='Cantor',weapon='SF_HaloLance',description='Angelic overseer. Grants Conviction to nearby worshippers and enables Last Hymn martyrdom within five cells. Kill or isolate the Cantor to break the formation.'),
 dict(id='h_retrieval',name='Retrieval Team',faction='h_area52',kind='unit',parent='H_RIFLEMAN',cost=200,hp=5000,speed=92,role='Retrieval',weapon='SF_PulseRifle',description='Black-site reconnaissance infantry with eight-cell sight and short-range cloak detection. Screens expensive experimental vehicles. Sample recovery remains future research.'),
 dict(id='h_janus',name='Janus Tank',faction='h_area52',kind='unit',parent='H_BULWARK',cost=1500,hp=55000,speed=65,role='Janus',weapon='SF_JanusSeraph',description='Experimental containment tank. SERAPH fires long-range precision shots; ABYSS delivers short-range infernal fire. A powered Containment Pylon is required. Protocol changes disable firing for three seconds.'),
 dict(id='d_magistrate',name='Magistrate of Ash',faction='d_contempt',kind='unit',parent='D_CINDERLING',cost=900,hp=15000,speed=70,role='Magistrate',weapon='SF_Magistrate',description='Attacking pronounces Contempt: one visible target per player, ten-second mark, eight-second retarget cooldown. Circle attacks deal 15% extra damage; killing the condemned enemy grants six seconds of Ascendancy. Killing the Magistrate cancels the mark.'),
 dict(id='d_contemptor',name='Contemptor',faction='d_contempt',kind='unit',parent='D_RAVAGER',cost=1350,hp=65000,speed=68,role='Contemptor',weapon='SF_Contemptor',description='Armored close-range execution beast. Strong against damaged heavy targets; weak against cheap infantry screens. Gains 30% execution damage against targets below half health.'),
 dict(id='a_processional',name='Processional Shrine',faction='a_desolation',kind='building',parent='H_ENTRENCHMENT',cost=650,hp=50000,power=25,role='Shrine',description='Powered four-person garrison and hymn relay. Extends Conviction and enables martyrdom within five cells. Empty shrines cannot shoot.'),
 dict(id='h_containment',name='Containment Pylon',faction='h_area52',kind='building',parent='A_SANCTUARY',cost=900,hp=35000,power=60,role='Pylon',description='Powered null field suppresses Renewal, Blood Frenzy, dread and doctrine buffs within four cells, including friendly supernatural abilities. Select and Deploy (F) to switch SERAPH/ABYSS; oldest powered pylon controls your Janus tanks. Switching takes three seconds.'),
 dict(id='d_throne',name='Throne of Scorn',faction='d_contempt',kind='building',parent='D_SPINENEST',cost=1000,hp=45000,power=55,role='Throne',description='Powered organic defense and command monument. If both attacker and its living Magistrate stand within five cells, condemnation damage rises from 15% to 30%.')]

def main():
    art=ROOT/'art/subfactions';art.mkdir(exist_ok=True)
    (art/'catalogue.json').write_text(json.dumps(ENTRIES,indent=2)+'\n',encoding='utf-8')
    f=MOD/'rules/10-factions.yaml';s=f.read_text(encoding='utf-8')
    for sub,name,side,old in FACTIONS:
        if f'Faction@{sub}:' not in s:
            s=s.replace('\tFaction@sf_random:',f'\tFaction@{sub}:\n\t\tName: sf-faction-{sub.replace("_","-")}-name\n\t\tInternalName: {sub}\n\t\tSide: {side}\n\t\tDescription: sf-faction-{sub.replace("_","-")}-description\n\tFaction@sf_random:')
        # Expand each faction list without touching singleton exclusive gates.
        s=re.sub(r'(?m)^(\t+(?:Factions|RandomFactionMembers): )([^\n]+)$',
            lambda m:m[1]+m[2]+(', '+sub if old in m[2].split(', ') and len(m[2].split(', '))>1 and sub not in m[2].split(', ') else ''),s)
        s=re.sub(r'(?m)^(\t\t\t'+old+r': ([^\n]+))$',lambda m:m[0]+'\n\t\t\t'+sub+': '+m[2],s)
        if f'ProvidesPrerequisite@sf_{sub}:' not in s:
            s=s.replace('\nMCV:\n',f'\n\tProvidesPrerequisite@sf_{sub}:\n\t\tFactions: {sub}\n\t\tPrerequisite: sf.{sub}\n\nMCV:\n',1)
    if '\tSFDoctrineManager:' not in s:s=s.replace('World:\n\tBridgeLayer:', 'World:\n\tSFDoctrineManager:\n\tBridgeLayer:')
    s='\n'.join(line for i,line in enumerate(s.splitlines()) if i==0 or line!=s.splitlines()[i-1] or not line.strip())+'\n'
    f.write_text(s,encoding='utf-8')
    # Parent actor lists elsewhere use the new selection's proper art and HUD.
    for file in [MOD/'metrics.yaml',MOD/'rules/35-animations.yaml']:
        s=file.read_text(encoding='utf-8')
        for sub,name,side,old in FACTIONS:
            if file.name=='metrics.yaml':
                if 'FactionSuffix-'+sub not in s:s=re.sub(r'(?m)^(\tFactionSuffix-'+old+r': [^\n]+)$',lambda m:m[0]+'\n'+m[0].replace(old,sub),s)
            else:s=re.sub(r'(?m)^(\t\t\t'+old+r': ([^\n]+))$',lambda m:m[0]+'\n\t\t\t'+sub+': '+m[2] if '\t\t\t'+sub+': '+m[2] not in s else m[0],s)
        file.write_text(s,encoding='utf-8')
    rules='# Generated by scripts/build_subfactions.py. Initial additive doctrines.\n'
    for base in ['^Infantry','^Vehicle','^Building']:
        rules+=base+':\n\tSFDoctrineTarget:\n'
        for cond,cap in [('sf-null',1),('sf-resonance',3),('sf-ascendancy',1),('sf-condemned',1)]:
            rules+=f'\tExternalCondition@{cond}:\n\t\tCondition: {cond}\n\t\tTotalCap: {cap}\n\t\tSourceCap: {cap}\n'
        for i,mod in [(1,115),(2,130),(3,145)]:rules+=f'\tFirepowerMultiplier@SF_RESONANCE{i}:\n\t\tModifier: {mod}\n\t\tRequiresCondition: sf-resonance == {i} && !sf-null\n'
        rules+='\tFirepowerMultiplier@SF_ASCENDANCY:\n\t\tModifier: 120\n\t\tRequiresCondition: sf-ascendancy && !sf-null\n\tWithColoredOverlay@SF_CONDEMNED:\n\t\tColor: B044E078\n\t\tRequiresCondition: sf-condemned\n\tWithColoredOverlay@SF_NULL:\n\t\tColor: 80B0D040\n\t\tRequiresCondition: sf-null\n\n'
    for base in ['^Wall','^TechBuilding']:
        rules+=base+':\n\tSFDoctrineTarget:\n\tExternalCondition@SF_CONDEMNED:\n\t\tCondition: sf-condemned\n\t\tTotalCap: 1\n\tWithColoredOverlay@SF_CONDEMNED:\n\t\tColor: B044E078\n\t\tRequiresCondition: sf-condemned\n\n'
    seq='';messages=[]
    for e in ENTRIES:
        a=e['id'];key=a.replace('_','-');unit=e['kind']=='unit';vehicle=e['role'] in ['Janus','Contemptor']; parent=e['parent']; family={'a':'angels','h':'humans','d':'demons'}[a[0]]
        pre={'a':'a_armory' if vehicle else 'a_chapel','h':'h_motorpool' if vehicle else 'h_barracks','d':'d_forge' if vehicle else 'd_pit'}[a[0]]
        if not unit:pre={'a':'a_chapel','h':'h_radar','d':'d_forge'}[a[0]]
        rules+=f'{a.upper()}:\n\tInherits: {parent}\n\tRenderSprites:\n\t\tImage: {a}\n\tBuildable:\n\t\tQueue: '+('Vehicle' if vehicle else 'Infantry' if unit else 'Defense')+f'\n\t\tPrerequisites: {pre}, ~sf.{e["faction"]}, ~techlevel.'+('medium' if vehicle or not unit else 'infonly')+f'\n\t\tBuildPaletteOrder: 85\n\t\tDescription: sf-{key}-description\n\tTooltip:\n\t\tName: sf-{key}-name\n\tValued:\n\t\tCost: {e["cost"]}\n\tHealth:\n\t\tHP: {e["hp"]}\n\tSFDoctrineMember:\n\t\tRole: {e["role"]}\n'
        if unit:
            rules+=f'\tMobile:\n\t\tSpeed: {e["speed"]}\n\tSpawnActorOnDeath@SF_ANIMATION:\n\t\tActor: {a}.death\n\t'+('Armament' if vehicle else 'Armament@PRIMARY')+f':\n\t\tWeapon: {e["weapon"]}\n'
            if not vehicle:rules+=f'\tArmament@GARRISONED:\n\t\tWeapon: {e["weapon"]}\n'
            if a=='a_congregant':rules+='\tExternalCondition@SF_CONVICTION:\n\t\tCondition: sf-conviction\n\t\tTotalCap: 1\n\t-ChangesHealth@SF_RENEWAL:\n\tDamageMultiplier@SF_CONVICTION:\n\t\tModifier: 85\n\t\tRequiresCondition: sf-conviction && !sf-null\n'
            if a=='h_retrieval':rules+='\tRevealsShroud:\n\t\tRange: 8c0\n\tDetectCloaked:\n\t\tRange: 3c0\n'
            if a=='h_janus':rules+='\tExternalCondition@SF_ABYSS:\n\t\tCondition: sf-abyss\n\t\tTotalCap: 1\n\tExternalCondition@SF_PROTOCOL:\n\t\tCondition: sf-protocol-offline\n\t\tTotalCap: 1\n\tArmament:\n\t\tRequiresCondition: !sf-abyss\n\tArmament@ABYSS:\n\t\tName: abyss\n\t\tWeapon: SF_JanusAbyss\n\t\tRequiresCondition: sf-abyss\n\tAttackFrontal:\n\t\tArmaments: primary, abyss\n\t\tPauseOnCondition: sf-protocol-offline\n'
            rules+=f'{a.upper()}.DEATH:\n\tInherits: ^SF_ANIMATED_DEATH\n\tRenderSprites:\n\t\tImage: {a}_death\n\n'
            for name,start,length,stride in [('stand',0,1,1),('run',8,2,2),('move',8,2,2),('shoot',24,2,2),('prone-stand',0,1,1),('prone-run',8,2,2),('prone-shoot',24,2,2),('parachute',0,1,1)]:
                seq+=('' if seq.endswith(a+':\n') else a+':\n') if name=='stand' else ''
                seq+=f'\t{name}:\n\t\tFilename: sevenfall|art/subfactions/{a}.png\n\t\tStart: {start}\n\t\tLength: {length}\n\t\tFacings: -8\n\t\tStride: {stride}\n\t\tTick: 120\n'
            # Vehicle damage uses authored late damage/death phases, never blank legacy frames.
            seq+=f'\tidle:\n\t\tFilename: sevenfall|art/subfactions/{a}.png\n\t\tStart: 0\n\t\tFacings: -8\n\ticon:\n\t\tFilename: sevenfall|art/subfactions/{a}-icon.png\n'
            if a=='h_janus':
                for label,start in [('damaged-idle',40),('critical-idle',41)]:
                    seq+=f'\t{label}:\n\t\tFilename: sevenfall|art/subfactions/{a}.png\n\t\tStart: {start}\n\t\tLength: 1\n\t\tFacings: -8\n\t\tStride: 3\n'
            seq+=f'{a}_death:\n\tdie:\n\t\tFilename: sevenfall|art/subfactions/{a}.png\n\t\tStart: 40\n\t\tLength: 3\n\t\tFacings: -8\n\t\tTick: 120\n\tcorpse:\n\t\tFilename: sevenfall|art/subfactions/{a}.png\n\t\tStart: 42\n\t\tLength: 1\n\t\tFacings: -8\n\t\tStride: 3\n'
        else:
            rules+=f'\tPower:\n\t\tAmount: {-e["power"]}\n\tSFDoctrineMember:\n\t\tRequiresCondition: !disabled && !build-incomplete\n'
            if a=='a_processional':rules+='\tInherits@SF_POWER: ^DisableOnLowPowerOrPowerDown\n\tCargo:\n\t\tMaxWeight: 4\n'
            if a=='h_containment':rules+='\t-SFDefenseSource:\n\tGrantConditionOnDeploy:\n\t\tDeployedCondition: sf-pylon-abyss\n\t\tRequiresCondition: !disabled && !build-incomplete\n\tWithTextDecoration@PROTOCOL:\n\t\tText: ABYSS\n\t\tPosition: Top\n\t\tRequiresCondition: sf-pylon-abyss\n\t\tValidRelationships: Ally\n'
            seq+=a+':\n'
            for n,start,length in [('idle',0,1),('make',0,1),('damaged-idle',1,1),('critical-idle',2,1),('shoot',3,3)]:seq+=f'\t{n}:\n\t\tFilename: sevenfall|art/subfactions/{a}.png\n\t\tStart: {start}\n\t\tLength: {length}\n\t\tTick: 100\n'
            seq+=f'\ticon:\n\t\tFilename: sevenfall|art/subfactions/{a}-icon.png\n'
        rules+='\n';seq+='\n';messages.extend([f'sf-{key}-name = {e["name"]}',f'sf-{key}-description = {e["description"]}'])
    for sub,name,side,old in FACTIONS:
        messages.extend([f'sf-faction-{sub.replace("_","-")}-name = {name}',f'sf-faction-{sub.replace("_","-")}-description = {side} - '+{'a_desolation':'Worshipper screens, martyrdom and angelic overseers.','h_area52':'Secret containment experiments and switchable supernatural weapon protocols.','d_contempt':'Condemned targets, execution beasts and infernal command monuments.'}[sub]])
    # Coalesce multiple additions to a trait into one MiniYaml node.
    output=[]; actor=[]
    def flush(lines):
        if not lines:return []
        head=lines[0]; traits={}; current=None
        for line in lines[1:]:
            if line.startswith('\t') and not line.startswith('\t\t'):
                current=line
                traits.setdefault(current,[])
            elif current is not None and line.strip():traits[current].append(line)
        return [head]+[line for key,values in traits.items() for line in [key,*values]]+['']
    for line in rules.splitlines():
        if line and not line.startswith(('\t','#')):
            output.extend(flush(actor));actor=[line]
        elif actor:actor.append(line)
        elif line.startswith('#'):output.append(line)
    output.extend(flush(actor));rules='\n'.join(output)
    (MOD/'rules/55-subfactions.yaml').write_text(rules.rstrip()+'\n',encoding='utf-8')
    (MOD/'sequences/subfactions.yaml').write_text(seq.rstrip()+'\n',encoding='utf-8')
    f=MOD/'fluent/sevenfall.ftl';s=f.read_text(encoding='utf-8').split('\n# Additional subfaction doctrines')[0];f.write_text(s.rstrip()+'\n\n# Additional subfaction doctrines\n'+'\n'.join(messages)+'\n',encoding='utf-8')
    # Null fields disable supernatural passives as well as custom fields.
    f=MOD/'rules/30-units.yaml';s=f.read_text(encoding='utf-8');s=s.replace('RequiresCondition: sf-frenzy\n','RequiresCondition: sf-frenzy && !sf-null\n');s=re.sub(r'(\tChangesHealth@SF_RENEWAL:\n)(?!\t\tRequiresCondition)',r'\1\t\tRequiresCondition: !sf-null\n',s);f.write_text(s,encoding='utf-8')
    weapons=''
    for name,parent,damage,range_,reload in [('Congregant','SF_PulseRifle',350,'4c0',28),('JanusSeraph','SF_Judgment',9500,'7c0',80),('JanusAbyss','SF_CinderMaw',11500,'4c0',55),('Magistrate','SF_Cinder',1200,'6c0',50),('Contemptor','SF_HellClaw',6500,'1c512',45)]:
        weapons+=f'SF_{name}:\n\tInherits: {parent}\n\tRange: {range_}\n\tReloadDelay: {reload}\n\tWarhead@1Dam: SpreadDamage\n\t\tDamage: {damage}\n\t\tValidRelationships: Enemy\n'
        if name=='Contemptor':weapons+='\t\tVersus:\n\t\t\tNone: 20\n\t\t\tLight: 100\n\t\t\tHeavy: 130\n'
    (MOD/'weapons/subfactions.yaml').write_text(weapons,encoding='utf-8')
    print('Generated three additive factions, six units and three defenses.')
if __name__=='__main__':main()
