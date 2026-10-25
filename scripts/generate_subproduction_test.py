"""Paid production acceptance for the three additional subfactions."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
def main():
 source=ROOT/'mods/sevenfall/maps/production-test';dest=ROOT/'mods/sevenfall/maps/subproduction-test';dest.mkdir(exist_ok=True)
 text=(source/'map.yaml').read_text(encoding='utf-8').replace('Production Diagnostic','Additional Subfaction Production Diagnostic').replace('production-test.lua','subproduction-test.lua')
 text=re.sub(r'\tPlayerReference@P[3-8]:\n(?:\t\t[^\n]*\n)+','',text)
 for old,new in [('a_seraph','a_desolation'),('a_warden','h_area52'),('a_exile','d_contempt')]:text=text.replace('Faction: '+old+'\n','Faction: '+new+'\n')
 (dest/'map.yaml').write_text(text,encoding='utf-8');(dest/'map.bin').write_bytes((source/'map.bin').read_bytes())
 lua=(source/'production-test.lua').read_text(encoding='utf-8').replace('PRODUCTION_TEST','SUBPRODUCTION_TEST').replace('for i=0,8','for i=0,2').replace('for i = 0, 8','for i = 0, 2')
 lua=lua.replace("{ 'a_watcher', 'h_rifleman', 'd_thrall' }","{ 'a_congregant', 'h_retrieval', 'd_magistrate' }").replace("{ 'a_aegis', 'h_bulwark', 'd_ravager' }","{ 'a_cantor', 'h_janus', 'd_contemptor' }")
 lua=re.sub(r"local special = .*", "local special = { 'a_processional', 'h_containment', 'd_throne' }",lua)
 lua=lua.replace('math.floor(i / 3) + 1','i + 1').replace('s.stage == 6 and s.units == 3','s.stage == 9 and s.units == 2').replace('s.stage ~= 6 or s.units ~= 3','s.stage ~= 9 or s.units ~= 2')
 lua=lua.replace('s.stage <= 4','s.stage <= 7').replace('elseif s.stage == 5 then','elseif s.stage == 8 then').replace('if s.units == 3 then s.stage = 6 end','if s.units == 2 then s.stage = 9 end')
 lua=lua.replace('{ infantry[s.family], armor[s.family], special[i+1] }','{ infantry[s.family], armor[s.family] }')
 lua=lua.replace("prefix .. '_veilworks', factory[family]}","prefix .. '_veilworks', factory[family], prefix .. '_radar', prefix .. '_advpower', special[i+1]}")
 lua=lua.replace('CPos.New(x,y-3)}}','CPos.New(x,y-3), CPos.New(x+8,y+1), CPos.New(x+8,y+5), CPos.New(x+5,y+9)}}')
 lua=lua.replace('DateTime.Seconds(420)','DateTime.Seconds(550)')
 lua=lua.replace("Check(#units == 1, 'produced '","print('SUBPRODUCTION_TEST DETAIL: produced count=' .. #units .. ' type=' .. kind); Check(#units == 1, 'produced '")
 lua=lua.replace('complete paid construction and three unit roles','complete paid construction, two units and exclusive defense')
 (dest/'subproduction-test.lua').write_text(lua,encoding='utf-8')
if __name__=='__main__':main()
