-- Local enclave diplomacy: owner changes only this community, never its whole people.
local startMission=WorldLoaded
WorldLoaded=function()
 startMission()
 local commander=Player.GetPlayer('Commander')
 local neutral=Player.GetPlayer('Enclave')
 local hostile=Player.GetPlayer('EnclaveHostile')
 local friendly=Player.GetPlayer('EnclaveFriendly')
 local owner=neutral
 local angered=false
 local helped=false
 local enclave={}
 for i,kind in ipairs({'u_rifleman','u_special','u_bulwark'}) do
  enclave[i]=Actor.Create(kind,true,{Owner=owner,Location=CPos.New(44+i*2,28)})
  enclave[i].Stance='Defend'
 end
 local function Anger(self,attacker,damage)
  if angered or not attacker or attacker.Owner~=commander or damage<=0 then return end
  angered=true
  Media.DisplayMessage('The Unwritten: you attacked our enclave. This community now treats your forces as hostile.','Enclave')
  for _,a in ipairs(enclave) do if not a.IsDead then a.Owner=hostile;a.Stance='AttackAnything' end end
 end
 for _,a in ipairs(enclave) do Trigger.OnDamaged(a,Anger) end
 Media.DisplayMessage('The Unwritten: this camp is neutral. Do not fire on it. An engineer can offer aid.','Enclave')
 if not angered then
  local aid=commander.AddSecondaryObjective('Help the The Unwritten enclave: bring an engineer to its camp without attacking it.')
  local function PollAid()
   if angered then commander.MarkFailedObjective(aid);return end
   if helped then return end
   local engineers=commander.GetActorsByType('h_engineer')
   for _,e in ipairs(engineers) do
    local d=e.Location-CPos.New(48,28)
    if math.abs(d.X)<=3 and math.abs(d.Y)<=3 then
     helped=true;commander.MarkCompletedObjective(aid)
     for _,a in ipairs(enclave) do if not a.IsDead then a.Owner=friendly;a.Stance='Defend' end end
     Media.DisplayMessage('The Unwritten: your aid is remembered. Our survivors will defend this camp alongside you.','Enclave')
     return
    end
   end
   Trigger.AfterDelay(25,PollAid)
  end
  Trigger.AfterDelay(25,PollAid)
 end
end
