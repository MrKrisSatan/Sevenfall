"""Native repair/garrison diagnostic; requires a working game content installation."""
from generate_ashen_crossing import main, ROOT

main()
source = ROOT / 'mods/sevenfall/maps/ashen-crossing'
dest = ROOT / 'mods/sevenfall/maps/environment-test'
dest.mkdir(parents=True, exist_ok=True)
(dest / 'map.bin').write_bytes((source / 'map.bin').read_bytes())
text = (source / 'map.yaml').read_text(encoding='utf-8').replace('Title: Ashen Crossing', 'Title: Sevenfall Environment Diagnostic').replace('Categories: Conquest', 'Categories: Test')
text += '''Rules:
	World:
		-SpawnStartingUnits:
		LuaScript:
			Scripts: environment-test.lua
	Player:
		-ConquestVictoryConditions:
		Shroud:
			FogCheckboxEnabled: False
			FogCheckboxLocked: True
			ExploredMapCheckboxEnabled: True
			ExploredMapCheckboxLocked: True
'''
(dest / 'map.yaml').write_text(text, encoding='utf-8')
