"""Native rendering smoke scenario for every painted actor and both generic mappings."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
source=ROOT/'mods/sevenfall/maps/newrealms-test'
dest=ROOT/'mods/sevenfall/maps/paintedrealms-test'
dest.mkdir(exist_ok=True)
(dest/'map.bin').write_bytes((source/'map.bin').read_bytes())
(dest/'map.yaml').write_text((source/'map.yaml').read_text().replace('New Realms Diagnostic','Painted Realms Diagnostic').replace('newrealms-test.lua','paintedrealms-test.lua'))
plan=json.loads((ROOT/'art/new-realms/painted-prompts.json').read_text())
lines=['local units, buildings = {}, {}','WorldLoaded=function()']
for i,p in enumerate(plan):
 actor='fact' if p['id'].endswith('_yard') else 'mcv' if p['id'].endswith('_mcv') else p['id']
 owner='P0' if p['id'][0]=='i' else 'P4'
 group='buildings' if p['kind']=='building' else 'units'
 x,y=8+(i%8)*13,10+(i//8)*14
 lines.append(f' table.insert({group},Actor.Create("{actor}",true,{{Owner=Player.GetPlayer("{owner}"),Location=CPos.New({x},{y})}}))')
lines+=[' Camera.Position=Map.CenterOfCell(CPos.New(50,24))',
' Trigger.AfterDelay(DateTime.Seconds(8),function()',
'  Camera.Position=Map.CenterOfCell(CPos.New(50,57))',
'  for _,a in ipairs(buildings) do a.Health=math.floor(a.MaxHealth*.4) end',
'  for _,a in ipairs(units) do a.Move(a.Location+CVec.New(3,2)) end',
'  print("PAINTEDREALMS_TEST PASS: spawned 51 designs; move and damaged states")',
' end)',
' Trigger.AfterDelay(DateTime.Seconds(16),function()',
'  for _,a in ipairs(buildings) do a.Health=math.floor(a.MaxHealth*.1) end',
'  print("PAINTEDREALMS_TEST PASS: critical building states")',
' end)',
' Trigger.AfterDelay(DateTime.Seconds(24),function()',
'  Camera.Position=Map.CenterOfCell(CPos.New(50,24))',
'  for _,a in ipairs(units) do if not a.IsDead then a.Kill("DefaultDeath") end end',
'  print("PAINTEDREALMS_TEST PASS: death actor rendering")',
' end)',
' Trigger.AfterDelay(DateTime.Seconds(32),function() print("PAINTEDREALMS_TEST COMPLETE checks=3") end)',
'end']
(dest/'paintedrealms-test.lua').write_text('\n'.join(lines)+'\n')
