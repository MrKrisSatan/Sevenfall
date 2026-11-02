"""Install authored non-player encounters in the three existing preview missions."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ENCLAVES=[('h03-glass-fields','u_unwritten','u','The Unwritten',False),('a03-glass-wrath','n_remnant','n','Nephilim Remnant',False),('d02-seeds-ruin','o_silence','o','The Outer Silence',True)]
for folder,faction,prefix,label,hostile in ENCLAVES:
 path=ROOT/'mods/sevenfall/maps'/folder
 m=(path/'map.yaml').read_text()
 if 'PlayerReference@Enclave:' not in m:
  players=''
  for name,relation in [('Enclave','neutral'),('EnclaveHostile','enemy'),('EnclaveFriendly','ally')]:
   players+=f'\tPlayerReference@{name}:\n\t\tName: {name}\n\t\tFaction: {faction}\n\t\tNonCombatant: True\n'
   if relation=='enemy':players+='\t\tEnemies: Commander, Enemy\n'
   elif relation=='ally':players+='\t\tAllies: Commander\n\t\tEnemies: Enemy\n'
  m=m.replace('Actors:\n',players+'Actors:\n',1)
  m=m.replace('\t\tEnemies: Enemy\n','\t\tAllies: EnclaveFriendly\n\t\tEnemies: Enemy, EnclaveHostile\n',1)
  m=m.replace('\t\tEnemies: Commander\n','\t\tEnemies: Commander, EnclaveHostile, EnclaveFriendly\n',1)
  m=m.replace('Scripts: mission.lua','Scripts: mission.lua, enclave.lua')
  (path/'map.yaml').write_text(m)
 lua='''-- Local enclave diplomacy: owner changes only this community, never its whole people.
local startMission=WorldLoaded
WorldLoaded=function()
 startMission()
 local commander=Player.GetPlayer('Commander')
 local neutral=Player.GetPlayer('Enclave')
 local hostile=Player.GetPlayer('EnclaveHostile')
 local friendly=Player.GetPlayer('EnclaveFriendly')
 local owner=INITIAL_OWNER
 local angered=INITIAL_HOSTILITY
 local helped=false
 local enclave={}
 for i,kind in ipairs({'PREFIX_rifleman','PREFIX_special','PREFIX_bulwark'}) do
  enclave[i]=Actor.Create(kind,true,{Owner=owner,Location=CPos.New(44+i*2,28)})
  enclave[i].Stance='Defend'
 end
 local function Anger(self,attacker,damage)
  if angered or not attacker or attacker.Owner~=commander or damage<=0 then return end
  angered=true
  Media.DisplayMessage('LABEL: you attacked our enclave. This community now treats your forces as hostile.','Enclave')
  for _,a in ipairs(enclave) do if not a.IsDead then a.Owner=hostile;a.Stance='AttackAnything' end end
 end
 for _,a in ipairs(enclave) do Trigger.OnDamaged(a,Anger) end
 Media.DisplayMessage(INITIAL_MESSAGE,'Enclave')
 if not angered then
  local aid=commander.AddSecondaryObjective('Help the LABEL enclave: bring an engineer to its camp without attacking it.')
  local function PollAid()
   if angered then commander.MarkFailedObjective(aid);return end
   if helped then return end
   local engineers=commander.GetActorsByType('ENGINEER')
   for _,e in ipairs(engineers) do
    local d=e.Location-CPos.New(48,28)
    if math.abs(d.X)<=3 and math.abs(d.Y)<=3 then
     helped=true;commander.MarkCompletedObjective(aid)
     for _,a in ipairs(enclave) do if not a.IsDead then a.Owner=friendly;a.Stance='Defend' end end
     Media.DisplayMessage('LABEL: your aid is remembered. Our survivors will defend this camp alongside you.','Enclave')
     return
    end
   end
   Trigger.AfterDelay(25,PollAid)
  end
  Trigger.AfterDelay(25,PollAid)
 end
end
'''.replace('PREFIX',prefix).replace('LABEL',label).replace('ENGINEER',{'h03-glass-fields':'h_engineer','a03-glass-wrath':'a_engineer','d02-seeds-ruin':'d_engineer'}[folder])
 lua=lua.replace('INITIAL_OWNER','hostile' if hostile else 'neutral').replace('INITIAL_HOSTILITY','true' if hostile else 'false').replace('INITIAL_MESSAGE',repr(f'{label}: '+('this breach is hostile. Keep clear of its patrol.' if hostile else 'this camp is neutral. Do not fire on it. An engineer can offer aid.')))
 (path/'enclave.lua').write_text(lua)
print('Three campaign-preview encounters installed: two neutral/helpable, one hostile.')
