"""Generate native cliff/pathing and autonomous twelve-player soak diagnostics."""
from pathlib import Path
import re
from generate_twelvefold import ROOT,STARTS
FACTIONS=['a_seraph','a_warden','a_exile','a_desolation','h_bastion','h_union','h_covenant','h_area52','d_legion','d_brood','d_court','d_contempt']
def main():
 source=ROOT/'mods/sevenfall/maps/twelvefold-scar'
 text=(source/'map.yaml').read_text(encoding='utf-8')
 for mode in ['terrain','twelve']:
  folder=ROOT/f'mods/sevenfall/maps/{mode}-test';folder.mkdir(exist_ok=True)
  body=text.replace('Title: The Twelvefold Scar','Title: Sevenfall '+('Cliff Terrain Diagnostic' if mode=='terrain' else 'Twelve-Player AI Soak')).replace('Categories: Conquest','Categories: Test')
  if mode=='terrain':
   a=body.index('\tPlayerReference@Multi0:');b=body.index('Actors:',a)
   body=body[:a]+'\tPlayerReference@Tester:\n\t\tName: Tester\n\t\tPlayable: True\n\t\tNonCombatant: True\n\t\tFaction: h_bastion\n'+body[b:]
   body+='Rules:\n\tPlayer:\n\t\t-ConquestVictoryConditions:\n'
  else:
   for i,faction in enumerate(FACTIONS):
    old=f'\tPlayerReference@Multi{i}:\n\t\tName: Multi{i}\n\t\tPlayable: True\n\t\tFaction: Random'
    enemies=', '.join(f'Multi{j}' for j in range(12) if j!=i)
    body=body.replace(old,f'\tPlayerReference@Multi{i}:\n\t\tName: Multi{i}\n\t\tFaction: {faction}\n\t\tBot: sevenfall\n\t\tEnemies: {enemies}')
   body=body.replace('Actors:','\tPlayerReference@Observer:\n\t\tName: Observer\n\t\tPlayable: True\n\t\tNonCombatant: True\n\t\tFaction: h_bastion\nActors:',1)
   for i,(x,y) in enumerate(STARTS):body+=f'\tBotMCV{i}: mcv\n\t\tOwner: Multi{i}\n\t\tLocation: {x},{y}\n'
   body+='Rules:\n'
  if mode=='terrain':
   body+='\tsf_late_shooter:\n\t\tInherits: H_RIFLEMAN\n\t\t-Buildable:\n\t\tRenderSprites:\n\t\t\tImage: h_rifleman\n\t\tArmament@PRIMARY:\n\t\t\tWeapon: SF_LateProjectile\n\t\tAutoTarget:\n\t\t\tInitialStance: HoldFire\n\t\t\tInitialStanceAI: HoldFire\n\tsf_late_target:\n\t\tInherits: H_BULWARK\n\t\t-Buildable:\n\t\tRenderSprites:\n\t\t\tImage: h_bulwark\n\t\tHealth:\n\t\t\tHP: 1000000\n\t\tAutoTarget:\n\t\t\tInitialStance: HoldFire\n\t\t\tInitialStanceAI: HoldFire\n'
  body+=f'\tWorld:\n\t\t-SpawnStartingUnits:\n\t\tLuaScript:\n\t\t\tScripts: {mode}-test.lua\n'
  if mode=='terrain':body+='Weapons:\n\tSF_LateProjectile:\n\t\tInherits: SF_PulseRifle\n\t\tReloadDelay: 1000\n\t\tProjectile: Bullet\n\t\t\tSpeed: 16\n\t\tWarhead@1Dam: SpreadDamage\n\t\t\tDamage: 1000\n\t\t\tValidRelationships: Ally, Enemy, Neutral\n'
  (folder/'map.yaml').write_text(body,encoding='utf-8');(folder/'map.bin').write_bytes((source/'map.bin').read_bytes())
if __name__=='__main__':main()
