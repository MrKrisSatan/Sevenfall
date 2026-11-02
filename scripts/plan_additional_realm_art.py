"""Reproducible painted-art briefs, one generated atlas per original asset."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'design/ADDITIONAL_REALMS_ROSTER.json').read_text())
styles={
'v':'Veilborn living mineral organism, luminous turquoise and amethyst crystal facets with subtle antique gold veins, organic crystalline growth, dark stone roots; not robotic, no angel wings',
'u':'Unwritten erased people reconstructed from memories, weathered silver and blue-grey armor or architecture, parchment ribbons and incomplete translucent edges, soft pearl glow; substantial readable silhouette, not invisible',
'o':'Outer Silence alien absence, obsidian and charcoal-violet surfaces, impossible curved carapaces framing dark hollow centers, restrained lavender seams, unsettling asymmetry; no conventional human technology',
'n':'Nephilim Remnant ancient mortal-celestial heritage, weathered limestone, bronze and ochre cloth, monumental masonry and carved oath motifs; living giants with human anatomy and vulnerable ordinary human attendants, no angel wings'}
roles={
'generator':'compact energy generator with a single glowing core and two buttresses',
'advpower':'tall advanced energy plant with three large coupled cores and heavy supports',
'veilworks':'resource refinery with a clearly open vehicle unloading bay, processing vats and mineral storage',
'barracks':'infantry training hall with a broad doorway, courtyard and faction banner without lettering',
'motorpool':'large vehicle or giant production hall with high open arch and industrial assembly floor',
'service':'repair depot with low open maintenance platform and articulated repair tools',
'radar':'reconnaissance tower with elevated lens or receiving crown',
'tech':'advanced research archive with layered upper chambers and enclosed central relic',
'helipad':'aircraft landing and production structure with a broad open landing ring',
'kennel':'beast nursery with fenced entrance and sheltered creature pen',
'autocannon':'low anti-ground defensive turret with a prominent directed weapon',
'missilenest':'tall anti-air defense with upward aiming paired launchers',
'cataclysm':'unique monumental superweapon installation, impressive crown and charged central relic',
'yard':'large construction headquarters with multiple connected sections, commanding central tower and work bays',
'mcv':'mobile construction vehicle carrying folded architectural components, clearly drivable tracked or walking chassis',
'harvester':'heavy resource collection vehicle with scooping front appendages, cargo vessel and reinforced mobile undercarriage',
'rifleman':'basic armed infantry, single complete figure carrying a faction ranged weapon',
'rocketeer':'anti-armor infantry carrying a large shoulder or arm mounted lance launcher',
'bulwark':'heavy armored combat walker with prominent main weapon',
'special':'specialist combat support unit with distinct long staff, optics or heavy weapon',
'air':'armed airborne creature or aircraft, broad wings, visibly airborne silhouette',
'beast':'powerful quadrupedal combat beast, complete body and four clearly visible limbs',
'engineer':'unarmed engineering specialist with repair tools and a compact supply pack',
'attendant':'ordinary small human attendant in ochre robes carrying a lantern, medical satchel and short defensive weapon'}
special={
'n_bulwark':'Oathbound Giant: towering muscular living humanoid giant in battered bronze and stone armor, immense two-handed stone maul, no wheels or vehicle chassis',
'n_special':'Mountain Bearer: enormous stooped living giant carrying a carved boulder siege cradle on its shoulders, stone armor and bronze straps, no wheels',
'n_air':'Dawn Kite: giant bronze-feathered raptor with an ancient armored harness, living flying beast',
'n_beast':'Stonehorn Beast: enormous muscular rhinoceros-like animal with a basalt horn and bronze flank armor',
'n_harvester':'Burden Carrier: massive slow stone-plated quadruped carrying a mineral hopper and collection tusks',
'u_special':'Decoy Echo: deliberately incomplete ghostly armored infantry apparition with a broken mirror chest and imitation rifle, pale translucent silhouette',
'u_bulwark':'Palimpsest Walker: slender articulated four-legged war machine reconstructed from layered fragments of silver armor and parchment memory ribbons, long ranged cannon',
'u_air':'Lantern Shade: floating spectral manta-like flying war construct with a luminous pearl lantern at its heart and trailing memory ribbons',
'u_beast':'Mnemonic Hound: spectral lean hunting hound built from pale layered memories, silver bone-like armor, soft pearl eyes',
'o_rifleman':'Hush Stalker: slender cloaked alien biped, obsidian carapace, hollow oval face, short integrated ambush weapon, no human face',
'o_bulwark':'Null Leviathan: hulking many-legged alien siege organism with obsidian segmented carapace and a dark central maw, ground based not a ship',
'o_air':'Eclipse Ray: alien flying ray with crescent obsidian wings and a hollow violet-edged central eye',
'o_beast':'Quiet Predator: six-limbed obsidian hunting beast with a low head and hooked claws',
'v_air':'Crystal Manta: living flying manta formed from turquoise and amethyst crystal membranes, gold-veined central seed',
'v_beast':'Glassmaw: muscular crystalline quadruped predator with angular mineral jaws and a long faceted tail',
'v_bulwark':'Cathedral Walker: tall four-legged living crystal siege organism with a cathedral-like cluster of mineral spires and a directed prism weapon',
'v_special':'Facet Seer: slender floating crystalline humanoid oracle with a lens-shaped halo of mineral fragments and a long prism staff',
'u_cataclysm':'Archive of Names: monumental silver-grey archival sanctuary with open book-shaped roof wings, shelves of glowing memory tablets and a pearl-lit central vault; no legible writing',
'o_cataclysm':'Null Cathedral: enormous alien obsidian cathedral of inward-curving black spires around a perfectly dark circular void, restrained violet edge light',
'n_cataclysm':'Ancestral Cairn: monumental stack of weathered standing stones with bronze oath rings surrounding a glowing subterranean fault, no modern technology',
'v_cataclysm':'Heart Prism: enormous living turquoise crystal heart suspended among six amethyst growth spires rooted in dark stone'}
plan=[]
assets=data['assets']+[dict(id='v_resonator',name='Resonator',prefix='v',kind='building',role='radar')]
for a in assets:
 building=a['kind']=='building'
 subject=special.get(a['id'],a['name']+': '+roles[a['role']])+'. '+styles[a['prefix']]
 layout=('EXACTLY 3 columns and 2 rows, six equal cells. Row 1: intact operational, heavily damaged with cracks and broken components, critically damaged partial ruin. Row 2: early construction foundation, half-built structure, fully operational active charged state. Same fixed elevated isometric camera angle and footprint in every cell.' if building else 'EXACTLY 8 columns and 4 rows, 32 equal cells, wide landscape sheet. Eight views in each row, clockwise: north (back to viewer), northeast, east, southeast, south (front), southwest, west, northwest. Row 1 standing/idle; row 2 walking or flying active stride; row 3 firing or using tools or harvesting; row 4 destroyed corpse or wreck lying flat. Each facing shows a different angle. Same elevated isometric camera. NO duplicate rows.')
 prompt='Original production sprite atlas for Sevenfall dark apocalyptic fantasy science-fiction RTS. Subject: '+subject+'. Painterly realistic miniature game art, detailed muted materials, shaded dimensional form, crisp readable silhouette, matching premium painted strategy sprites; NOT flat vector art. '+layout+' Same complete subject and scale in every cell. Generous transparent gutters, entire subject inside its cell, no overlap or clipping, consistent ground anchor. Actual alpha transparency, NO background, checkerboard, text, labels, gridlines, scenery, franchise symbols or watermark. Render small miniatures with empty space, not oversized portraits.'
 plan.append(dict(id=a['id'],kind='building' if building else 'unit',subject=subject,prompt=prompt,source='art/additional-realms/painted-source/'+a['id']+'.png',frameSize=128 if building else 48 if a['kind'] in ('infantry','rocket','engineer','beast') else 80))
folder=ROOT/'art/additional-realms';(folder/'painted-source').mkdir(exist_ok=True)
(folder/'painted-prompts.json').write_text(json.dumps(plan,indent=2)+'\n')
print(f'{len(plan)} painted atlas briefs ready.')
