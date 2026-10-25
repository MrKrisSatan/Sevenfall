"""Generate the deterministic three-doctrine native acceptance map."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MOD=ROOT/'mods/sevenfall'
def main():
 folder=MOD/'maps/doctrine-test';folder.mkdir(exist_ok=True)
 text='''MapFormat: 12
RequiresMod: sevenfall
Title: Sevenfall Doctrine Diagnostic
Author: Sevenfall contributors
Tileset: TEMPERAT
MapSize: 96,96
Bounds: 1,1,94,94
Visibility: Lobby
Categories: Test
Players:
	PlayerReference@Neutral:
		Name: Neutral
		OwnsWorld: True
		NonCombatant: True
		Faction: h_bastion
	PlayerReference@Observer:
		Name: Observer
		Playable: True
		NonCombatant: True
		Faction: h_bastion
'''
 for name,faction in [('Choir','a_desolation'),('Area','h_area52'),('Circle','d_contempt'),('Enemy','h_bastion')]:
  enemies='Choir, Area, Circle' if name=='Enemy' else 'Enemy'
  text+=f'\tPlayerReference@{name}:\n\t\tName: {name}\n\t\tFaction: {faction}\n\t\tEnemies: {enemies}\n'
 text+='Actors:\n\tSpawn: mpspawn\n\t\tOwner: Neutral\n\t\tLocation: 45,45\n'
 rows=[('ChoirPower','a_spire','Choir',5,5),('AreaPower','h_generator','Area',25,25),('CirclePower','d_heart','Circle',55,5),('EnemyPower','d_heart','Enemy',18,5),('Cantor','a_cantor','Choir',10,10),('SelfMartyr','a_congregant','Choir',10,11),('Martyr1','a_congregant','Choir',11,10),('Martyr2','a_congregant','Choir',11,11),('Martyr3','a_congregant','Choir',12,11),('Martyr4','a_congregant','Choir',12,10),('Protected','a_congregant','Choir',11,9),('Dread','d_mourningwall','Enemy',13,8),('Executor','h_rifleman','Enemy',14,10),('Pylon','h_containment','Area',30,30),('Janus','h_janus','Area',32,30),('LongTarget','sf_doctrine_dummy','Enemy',37,30),('NearTarget','sf_doctrine_dummy','Enemy',34,30),('NullAngel','a_watcher','Choir',32,32),('Retrieval','h_retrieval','Area',28,34),('Magistrate','d_magistrate','Circle',60,10),('Beast','d_contemptor','Circle',61,10),('MarkedTarget','sf_doctrine_dummy','Enemy',63,10),('SecondTarget','sf_doctrine_dummy','Enemy',63,12),('Shrine','a_processional','Choir',10,20),('ShrineFollower','a_congregant','Choir',13,20)]
 rows += [('NullWire','h_razorwire','Area',33,29),('WireWalker','h_rifleman','Enemy',32,29)]
 for name,kind,owner,x,y in rows:text+=f'\t{name}: {kind}\n\t\tOwner: {owner}\n\t\tLocation: {x},{y}\n'
 text+='''Rules:
	World:
		-SpawnStartingUnits:
		LuaScript:
			Scripts: doctrine-test.lua
	Player:
		-ConquestVictoryConditions:
	sf_doctrine_dummy:
		Inherits: H_BULWARK
		-Buildable:
		RenderSprites:
			Image: h_bulwark
		Health:
			HP: 1000000
		AutoTarget:
			InitialStance: HoldFire
			InitialStanceAI: HoldFire
Weapons:
	SF_PulseRifle:
		Warhead@1Dam:
			Damage: 999999
'''
 for actor in ['A_CONGREGANT','A_CANTOR','H_RETRIEVAL','H_JANUS','D_MAGISTRATE','D_CONTEMPTOR','A_WATCHER','H_RIFLEMAN','H_BULWARK']:
  text=text.replace('Weapons:\n',f'\t{actor}:\n\t\tAutoTarget:\n\t\t\tInitialStance: HoldFire\n\t\t\tInitialStanceAI: HoldFire\nWeapons:\n')
 (folder/'map.yaml').write_text(text,encoding='utf-8')
 (folder/'map.bin').write_bytes((MOD/'maps/defense-test/map.bin').read_bytes())
if __name__=='__main__':main()
