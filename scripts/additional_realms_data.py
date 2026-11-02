"""Original additional realm roster. Values are explicit initial playtest tuning."""
# prefix: internal family, lobby ID, display name, power kind, colors, structure names
REALMS={
 'v':dict(family='veilborn',faction='v_veilborn',name='Veilborn',power='Bloom',colors=['72e8d9','8266d9','e3c572'],buildings=['Lumen Growth','Assimilation Well','Seed Nursery','Cathedral Foundry','Pure Spire','Mending Pool','Listening Prism','Memory Lattice','Manta Aerie','Glassmaw Cradle','Shard Battery','Sky Prism','Heart Prism']),
 'u':dict(family='unwritten',faction='u_unwritten',name='The Unwritten',power='Restoration',colors=['dce8ef','657991','adcad4'],buildings=['Mnemonic Lamp','Remembrance Mill','Echo Hall','Palimpsest Foundry','Memory Beacon','Recollection Pool','Witness Lens','Index of Lives','Lantern Loft','Memory Den','Script Battery','Sky Quill','Archive of Names']),
 'o':dict(family='silence',faction='o_silence',name='The Outer Silence',power='AbsoluteSilence',colors=['34314e','9b8ad5','171621'],buildings=['Dark Pulse','Hollow Siphon','Hush Chamber','Null Foundry','Deep Pulse','Stillwater Basin','Absence Lens','Boundary Archive','Eclipse Nest','Quiet Den','Hush Battery','Sky Void','Null Cathedral']),
 'n':dict(family='nephilim',faction='n_remnant',name='Nephilim Remnant',power='Earthbreaker',colors=['b99b64','7b8275','e0c99a'],buildings=['Hearth Tower','Burden Mill','Attendant Lodge','Giant Hall','Sun Hearth','Resting Court','Horizon Watch','Ancestral Chronicle','Dawn Roost','Stonehorn Pen','Cairn Battery','Sky Spear','Ancestral Cairn'])}
STRUCTURES=['generator','veilworks','barracks','motorpool','advpower','service','radar','tech','helipad','kennel','autocannon','missilenest','cataclysm']
YARDS={'v':'Heartroot','u':'Refuge of Names','o':'Quiet Threshold','n':'Ancestral Seat'}
MCVS={'v':'Seed Pilgrim','u':'Wandering Archive','o':'Threshold Carrier','n':'Ancestral Caravan'}
DOCTRINES={
'v':'Crystalline growth network. Combat units near a powered Heartroot or Resonator take 20% less damage and recover 1% health per second; isolated units lose these benefits.',
'u':'Fragile echoes and decoys. Combat deaths leave short-lived memory remnants; Restoration consumes up to six to reconstruct temporary infantry. No recursive resurrection.',
'o':'Short-range ambush and suppression. Hush Stalkers cloak between attacks; isolated combat units gain speed. Detection, screens and focus fire counter them.',
'n':'Slow, expensive giants supported by vulnerable human attendants. Nearby attendants grant non-stacking protection and recovery; raid the support and economy.'}
# suffix, label, kind, cost, HP, speed, damage, range, reload, description
UNITS={
'v':[
 ('rifleman','Shardling','infantry',180,7000,84,1200,'4c0',32,'Crystalline screening infantry; gains protection and recovery inside the growth network.'),
 ('rocketeer','Prism Lancer','rocket',420,9500,66,4800,'6c0',75,'Deliberate anti-armor and anti-air fire; weak when swarmed.'),
 ('bulwark','Cathedral Walker','vehicle',1700,65000,52,8200,'6c0',85,'Expensive heavy anchor. Protect its slow advance with resonators and screens.'),
 ('special','Facet Seer','infantry',650,10000,78,1500,'6c0',45,'Long-sight detector and ranged support; cannot replace a powered network node.'),
 ('air','Crystal Manta','air',1750,26000,130,4700,'5c0',55,'Hovering crystalline attacker; vulnerable to anti-air concentration.'),
 ('beast','Glassmaw','beast',520,18000,115,3700,'1c512',34,'Fast mineral predator for intercepting raids; needs support against heavy armor.'),
 ('engineer','Facet Mender','engineer',450,6000,76,0,'0c0',1,'Repairs civilian structures and bridges; captures eligible buildings.'),
 ('harvester','Root Carrier','harvester',1450,64000,66,0,'0c0',1,'Physical Veilglass collector; no free-resource generation and safe from contact blasts.')],
'u':[
 ('rifleman','Memory Infantry','infantry',90,3200,105,1050,'5c0',30,'Fast fragile echo infantry. Real deaths leave a short-lived memory remnant.'),
 ('rocketeer','Errata Lancer','rocket',260,3900,94,2800,'5c0',56,'Fragile armor/air counter; screens and decoys must protect it.'),
 ('bulwark','Palimpsest Walker','vehicle',1000,28500,90,5600,'6c0',70,'Mobile ranged chassis with poor durability; leaves a recoverable memory remnant.'),
 ('special','Decoy Echo','infantry',60,1400,115,0,'4c0',45,'Targetable distraction with no damaging weapon; cannot generate memory remnants.'),
 ('air','Lantern Shade','air',1150,12000,175,2400,'5c0',34,'Fast fragile aerial raider; loses direct trades with dedicated anti-air.'),
 ('beast','Mnemonic Hound','beast',220,5500,155,1600,'1c512',20,'Swift spectral scout and melee pursuer; cannot sustain a frontal attack.'),
 ('engineer','Namekeeper','engineer',350,3500,100,0,'0c0',1,'Engineering and capture specialist, not a free resurrection source.'),
 ('harvester','Remembrance Carrier','harvester',1250,38000,90,0,'0c0',1,'Fast vulnerable physical collector. Escort it; destruction never creates a replacement.')],
'o':[
 ('rifleman','Hush Stalker','infantry',260,5600,110,2400,'3c512',38,'Cloaks after three quiet seconds. Attacking or taking damage reveals it; detectors counter concealment.'),
 ('rocketeer','Dissonance Lance','rocket',430,6500,88,5200,'4c512',80,'Short-range armor/air ambusher; exposed while firing.'),
 ('bulwark','Null Leviathan','vehicle',1900,56000,61,10500,'4c0',85,'Heavy close-range attacker; cannot safely siege long-range defenses alone.'),
 ('special','Stillness Seer','infantry',700,7000,92,900,'5c0',50,'Detector whose attacks briefly slow and weaken the target; suppression refreshes instead of stacking.'),
 ('air','Eclipse Ray','air',1500,17000,170,3900,'4c0',45,'Fast short-range airborne ambusher; retreat after a strike.'),
 ('beast','Quiet Predator','beast',600,15500,145,4400,'1c512',40,'Rapid melee pursuit beast; vulnerable to screens and focused fire.'),
 ('engineer','Void Tender','engineer',500,5000,98,0,'0c0',1,'Repairs and captures; has no combat isolation or cloak bonus.'),
 ('harvester','Hollow Gatherer','harvester',1500,42000,85,0,'0c0',1,'Visible physical resource collector; normal refinery unloading is required.')],
'n':[
 ('rifleman','Remnant Warden','infantry',300,13500,65,2000,'5c0',42,'Costly durable human guardian. Protect attendants and giant approaches.'),
 ('rocketeer','Cairn Slinger','rocket',550,15000,55,6600,'6c0',95,'Slow heavy anti-armor and anti-air support; punish its long reload.'),
 ('bulwark','Oathbound Giant','vehicle',2400,100000,43,16000,'1c768',65,'Towering melee combatant. Extremely costly and slow; kite it or isolate its attendants.'),
 ('special','Mountain Bearer','vehicle',2600,85000,39,12500,'7c0',110,'Slow ranged siege giant. Needs screening and cannot cover multiple fronts.'),
 ('air','Dawn Kite','air',2100,36000,95,7800,'6c0',90,'Durable slow aircraft with heavy volleys; expensive to replace.'),
 ('beast','Stonehorn Beast','beast',950,45000,75,7800,'1c512',60,'Heavy ground beast; strong in sustained close combat and vulnerable to kiting.'),
 ('attendant','Human Attendant','infantry',180,3200,75,300,'3c0',45,'Vulnerable support. Within four cells, allied Remnant combatants gain protection and recover health.'),
 ('engineer','Cairnkeeper','engineer',400,6000,68,0,'0c0',1,'Repair/capture specialist; not a giant and not an attendant aura source.'),
 ('harvester','Burden Carrier','harvester',1750,85000,50,0,'0c0',1,'Very durable slow collector. Its long travel cycle makes route defense essential.')]
}
