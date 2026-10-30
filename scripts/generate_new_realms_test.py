"""Paid deployment/production acceptance for all eight new selections."""
from pathlib import Path
import re
from build_new_realms import FACTIONS, UNITS
ROOT=Path(__file__).resolve().parents[1]
source=ROOT/'mods/sevenfall/maps/production-test'
dest=ROOT/'mods/sevenfall/maps/newrealms-test'
dest.mkdir(exist_ok=True)
s=(source/'map.yaml').read_text()
s=s.replace('Sevenfall Production Diagnostic','Sevenfall New Realms Diagnostic').replace('production-test.lua','newrealms-test.lua')
s=re.sub(r'\tPlayerReference@P8:.*?(?=Actors:)', '', s, flags=re.S)
for i,f in enumerate(FACTIONS):
 s=re.sub(r'(PlayerReference@P'+str(i)+r':\n\t\tName: P'+str(i)+r'\n\t\tFaction: )\w+',r'\g<1>'+f[0],s)
# The local human is an observer, so ordinary clicks cannot alter diagnostic armies.
s=s.replace('\t\tPlayable: True\n\t\tLockFaction: True\n','')
s=s.replace('Actors:\n','\tPlayerReference@Observer:\n\t\tName: Observer\n\t\tFaction: h_bastion\n\t\tNonCombatant: True\n\t\tPlayable: True\nActors:\n')
(dest/'map.yaml').write_text(s)
(dest/'map.bin').write_bytes((source/'map.bin').read_bytes())
s=(source/'production-test.lua').read_text().replace('PRODUCTION_TEST','NEWREALMS_TEST').replace('0,8','0,7').replace('0, 8','0, 7')
s=s.replace("local power = { 'a_spire', 'h_generator', 'd_heart' }","local power = { 'i_generator', 'f_spire' }")
s=s.replace("local barracks = { 'a_chapel', 'h_barracks', 'd_pit' }","local barracks = { 'i_barracks', 'f_chapel' }")
s=s.replace("local factory = { 'a_armory', 'h_motorpool', 'd_forge' }","local factory = { 'i_motorpool', 'f_armory' }")
s=s.replace("math.floor(i / 3) + 1","math.floor(i / 4) + 1").replace("({'a', 'h', 'd'})","({'i', 'f'})")
s=re.sub(r'local infantry = .*',"local infantry = { 'i_rifleman', 'f_watcher' }",s)
s=re.sub(r'local armor = .*',"local armor = { 'i_bulwark', 'f_aegis' }",s)
s=re.sub(r'local special = .*',"local special = { "+', '.join("{'"+UNITS[i*2][1]+"', '"+UNITS[i*2+1][1]+"'}" for i in range(8))+' }',s)
s=s.replace('s.units == 3','s.units == 4').replace('s.units ~= 3','s.units ~= 4').replace('special[i+1]','special[i+1][1], special[i+1][2]').replace('three unit roles','shared infantry/armor and both exclusive units')
s=s.replace('DateTime.Seconds(420)','DateTime.Seconds(550)')
(dest/'newrealms-test.lua').write_text(s)
