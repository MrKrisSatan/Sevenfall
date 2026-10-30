"""Reviewable prompts for original, image-generated realm artwork."""
import json
from pathlib import Path
from build_new_realms import FAMILIES,UNITS
ROOT=Path(__file__).resolve().parents[1]
DESIGNS={
'i_ghost':'Mnemonic Ghost: slender white ceramic synthetic humanoid, carbon joints, hoodlike optical shroud, cyan sensor slit, long precision rifle',
'i_lance':'Needle Chassis: narrow four-legged robotic precision gun platform, off-white ceramic plates, slender central rail lance, cyan optical lens',
'i_endurer':'Endurer: massive bipedal industrial combat automaton, dark gunmetal layered armor, amber core, broad shoulders, heavy integrated arm rifle, no human skull',
'i_crucible':'Crucible Engine: huge slow six-tread siege machine, iron armor and copper heat sinks, heavy fixed forward siege cannon, amber furnace core',
'i_thread':'Threadkeeper: angular black-and-white humanoid missile automaton, mint network lights, shoulder launcher rack, antenna crown',
'i_relay':'Relay Walker: squat quadrupedal white-and-black robotic command vehicle, tall segmented mint holographic relay mast, small forward pulse gun',
'i_savant':'Circuit Savant: small agile asymmetrical humanoid robot, cream ceramic shells and yellow circuits, exposed computational backpack, compact rapid-fire gun',
'i_gambit':'Gambit Rover: fast low three-wheel autonomous rover, asymmetrical cream armor, yellow circuit fins, fixed compact energy cannon',
'f_regent':'Uncrowned Regent: grotesque fallen celestial aristocrat, immense tarnished silver armor enclosing an elongated skeletal body, crown embedded into faceless head, twisted bone wing stumps, violet judgment spear',
'f_reliquary':'Walking Reliquary: huge six-legged bone-bound living cathedral engine, ribbed ivory cage, tarnished silver reliquary shrine, twisted wing buttresses, forward violet judgment organ',
'f_canticle':'Mute Canticle: gaunt fallen humanoid worshipper, stitched closed mouth, charcoal funeral robes, exposed ivory ribs, pink-violet throat crystal, crooked ranged prayer staff',
'f_lamentor':'Lamentor: heavy ground-walking grotesque fallen angel with a ribcage like a pipe organ, long bony legs, torn violet funeral vestments, luminous magenta throat chambers, shredded wing frame',
'f_flayer':'Vow Flayer: fast hunched fallen angel, bone hooks for hands, ruined wing stumps, scarlet wax seals and torn bandages, pale sinewy body, no weapon gun, melee claws',
'f_martyr':'Carrion Martyr: huge four-legged skeletal abomination, open rib arch and charred wings fused into armor, red wounds glowing without graphic gore, enormous melee foreclaws',
'f_pinions':'Severed Pinion: lean grounded fallen hunter, backward-jointed legs, long broken wing bones folded like a cloak, pale blue eyes, long silver ranged hunting spear',
'f_harrow':'Harrow Stalker: fast low four-legged fallen hunting beast with swept-back shattered bone wing blades, ivory and charcoal body, icy blue spectral forward lance',
'i_generator':'Cognition Reactor: compact hexagonal steel generator, concentric cyan coolant rings and ceramic server stacks',
'i_veilworks':'Matter Compiler: broad automated refinery, low front docking apron, three ore processing cylinders, cyan crystal hopper and industrial robot arms',
'i_barracks':'Shell Foundry: compact rectangular robot infantry assembly plant, open dark front assembly exit and two white skeletal gantries',
'i_motorpool':'Chassis Forge: wide heavy robot vehicle factory, large front vehicle door, overhead robotic assembly cranes, blue-white industrial armor',
'i_advpower':'Fusion Stack: tall clustered reactors, three luminous cyan containment rings, heavy steel cooling fins',
'i_service':'Reconstruction Bay: open low vehicle service platform, robotic repair arms around clear central pad, cyan repair arcs',
'i_radar':'Prediction Spire: tapered white ceramic computation tower with a rotating geometric sensor crown and cyan lenses',
'i_tech':'Recursion Core: large black-glass computing citadel inside interlocking white polygonal supports, brilliant cyan contained central lattice',
'i_autocannon':'Sentry Node: compact autonomous armored twin-barrel turret on squat hexagonal bunker base, cyan targeting eye',
'i_missilenest':'Interceptor Node: armored vertical missile battery on low hexagonal base, angled launcher pods and cyan targeting dish',
'f_spire':'Apostate Pyre: crooked ivory bone spire enclosing a violet sacrificial flame, charred stone base and broken halo rings',
'f_veilworks':'Ossuary Mill: broad grotesque bone refinery, ribbed vault, low front collector docking mouth, purple Veilglass crucibles, no detached characters',
'f_chapel':'Profaned Chapel: compact distorted gothic chapel, twisted bone buttresses, mouthlike front infantry doorway, ripped violet banners and fractured halo',
'f_armory':'Flesh Crucible: broad living bone vehicle forge, huge rib-arch exit, tendonlike supports and violet furnace chambers, gothic ruin architecture',
'f_advpower':'Sundered Halo: tall broken halo energy plant, three cracked hovering bone rings chained to violet-flame ossuary pylons',
'f_service':'Suture Shrine: low open repair courtyard framed by bent angel wing bones, hanging spectral sutures and violet energy above central pad',
'f_radar':'Blind Oracle: twisted eyeless giant angel statue fused into a gothic sensor tower, crown of small violet lenses and cracked wings',
'f_tech':'Testament Vault: imposing bone-and-black-stone library fortress, sealed violet booklike central monolith, crooked wing buttresses and broken silver halo',
'f_watchfire':'Balefire Watch: squat bone watchtower with a violet flame brazier and small skeletal gun aperture',
'f_judgment':'Wrath Organ: heavy gothic defensive organ, clustered long bone energy barrels over a squat armored ossuary base',
'f_skyward':'Broken Halo Battery: anti-air tower of crooked ivory prongs enclosing a fractured silver halo, violet targeting crystal',
'i_rifleman':'Shell Trooper: standardized autonomous biped robot, slate armored torso, white shoulder plates, cyan face strip, practical pulse rifle',
'i_rocketeer':'Breach Automaton: broad-shouldered armored robot carrying a twin-tube missile launcher, cyan sensor head, white and charcoal armor',
'i_bulwark':'Sentinel Chassis: robust low four-track autonomous tank, white angular glacis, fixed forward cyan energy cannon, no human crew or markings',
'i_engineer':'Repair Proxy: small slender utility biped robot, white ceramic body, cyan repair backpack, manipulator tool hands, no gun',
'i_harvester':'Reclaimer: heavy six-wheel autonomous mineral collector, low front articulated harvesting jaws, cyan ore container, white armored hull, no gun',
'f_watcher':'Oath Husk: skeletal fallen infantry with twisted ivory armor, closed cracked face, torn purple vestment and crooked energy spear',
'f_judicator':'Blight Herald: tall hunched fallen ranged soldier, ribbed shoulders, broken small wing bones, black vestment and violet heavy judgment staff',
'f_aegis':'Bonebound Engine: low heavy four-legged abomination with ivory rib armor, twisted wing stump shields, forward violet energy maw',
'f_engineer':'Suture Keeper: gaunt robed fallen repair priest, ivory mask, long delicate tool fingers, spectral violet thread spool, no gun',
'f_gatherer':'Tithe Bearer: enormous squat six-legged bone-armored mineral beast, front crystal-scooping mandibles, swollen violet ore cage on back, no weapon',
'i_yard':'Assembly Nexus construction yard: broad modular automated construction command complex, two articulated cranes, cyan planning lattice, white ceramic command bunker and dark steel footprint',
'f_yard':'Exile Seat construction yard: sprawling ruined celestial throne-workshop, bone cranes, twisted gothic arches, violet creation well and broken enormous halo',
'i_mcv':'Seed Carrier mobile construction vehicle: huge folded six-wheel autonomous construction machine, collapsed white gantries, cyan core and heavy steel chassis',
'f_mcv':'Pilgrim Ossuary mobile construction vehicle: huge lumbering six-legged walking shrine, tightly folded bone cranes and wing arches, violet core, remains a ground vehicle',
}
BUILDINGS={p+'_'+suffix for p,(_,_,_,names) in FAMILIES.items() for suffix in names if suffix not in ('harvester','gatherer','rifleman','rocketeer','bulwark','watcher','judicator','aegis','engineer')}|{'i_yard','f_yard'}
plan=[]
for id,subject in DESIGNS.items():
 building=id in BUILDINGS
 layout=('EXACTLY 3 columns and 2 rows, 6 equal cells, landscape sheet. Fixed elevated isometric camera facing southeast; the SAME building and footprint in EVERY cell. Reading order: intact; visibly damaged with cracked surfaces; critical damage with collapsed sections; early construction scaffold; half-built structure; operating/weapon firing energy pulse.' if building else 'EXACTLY 8 columns and 4 rows, 32 equal cells, wide landscape sheet. Eight views in each row, clockwise: north (back to viewer), northeast, east, southeast, south (front), southwest, west, northwest. Row 1 standing/idle; row 2 walking/rolling active stride; row 3 firing/using tools/harvesting; row 4 destroyed corpse or wreck lying flat. Same complete subject and scale in every cell, fixed elevated isometric camera, each facing must show a different angle. NO duplicate rows.')
 prompt=f'Original production sprite atlas for Sevenfall dark apocalyptic science-fiction RTS. Subject: {subject}. Painterly realistic miniature game art, strongly readable silhouette, detailed muted materials. {layout} Keep generous transparent gutters between cells, each entire subject inside its own cell with no overlap. Actual alpha transparency, NO background, checkerboard, text, labels, gridlines, scenery, franchise symbols or watermark. All sprites aligned to a consistent ground anchor. Render small miniatures with empty space, not oversized portraits.'
 plan.append(dict(id=id,kind='building' if building else 'unit',subject=subject,prompt=prompt,source=f'art/new-realms/painted-source/{id}.png'))
(ROOT/'art/new-realms/painted-source').mkdir(exist_ok=True)
(ROOT/'art/new-realms/painted-prompts.json').write_text(json.dumps(plan,indent=2)+'\n',encoding='utf-8')
print(len(plan),'assets planned')
