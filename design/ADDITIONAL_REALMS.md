# The Veilborn and the three non-aligned peoples

This is the implementation specification for four additional original Sevenfall realms. Each receives a complete skirmish economy, construction/production, radar/technology, repair, engineers, air, beasts, defenses and a building-bound power. They are separate parent factions, not skins for existing subfactions. Existing five realms retain their twenty choices; these additions have one identity each and no subfactions. The three non-aligned peoples are selectable in development skirmish; Veilborn remains hidden pending genuine campaign progression. The released alpha.3 does not contain this expansion.

## Veilborn — a living mineral, not a machine infection

**Campaign:** sixth and final perspective, The World That Wakes. Its intended unlock requires completing all five preceding campaigns. **Identity:** a community emerging from pure Veilglass; physical crystalline bodies linked by voluntary resonance. **Visual language:** turquoise/violet facets, gold internal veins, branching mineral roots, visibly fractured damage states. **Voice:** plural voices learning when they may speak for one another.

**Economy:** Root Carriers collect ordinary Veilglass and unload at Assimilation Wells. A living seed is a marked campaign actor, not every normal resource tile. Growth never creates free credits. **Doctrine:** combat troops within six cells of a powered Heartroot or Resonator gain protection and recovery; isolated troops retain agency and basic combat but lose those advantages. Network sources do not stack. Destroying/depowering nodes and forcing fights away from their coverage are primary counters.

**Army:** Shardlings screen, Prism Lancers fight armor, Cathedral Walkers anchor the line, Facet Seers provide mobile support, Crystal Mantas provide air pressure and Glassmaws pursue raiders. Facet Menders handle engineering. Powerful cores are expensive and susceptible to focused attacks; the army needs several connected positions rather than one invulnerable deathball.

**Buildings:** Heartroot construction yard, Lumen Growth, Assimilation Well, Seed Nursery, Cathedral Foundry, Pure Spire, Mending Pool, Listening Prism, Memory Lattice, Manta Aerie, Glassmaw Cradle, Shard Battery, Sky Prism, Resonator and Heart Prism.

**Superweapon — Resonant Bloom:** supplied by the Heart Prism. After a visible warning, a bounded temporary bloom supports nearby allied troops with protection/recovery and slows hostile ground movement. It does not paint permanent free resources, overwrite map terrain or automatically win the mission. Source destruction removes the sidebar power; rebuilding starts a fresh charge. Low power pauses it.

## The Unwritten — existence on borrowed time

**Campaign:** never player-controlled; mostly neutral archives, occasional negotiated allies or hostile local defenders. **Skirmish:** fully selectable. **Identity:** distinct people erased from history whose surviving records are trapped in pure Veilglass. They are not Veilborn crystals and not copies of living opponents. **Visual language:** pale spectral silhouettes, ink-black gaps, parchment/silver facets and broken outlines.

**Doctrine:** inexpensive fragile echoes and deception; survivors can recover through support but lose direct trades. Real Unwritten combat deaths leave short-lived memory remnants. Restoration can consume a limited number to reconstruct temporary combat echoes. Echoes cannot recursively create remnants, harvest, build, capture, grant sale refunds or form an infinite resurrection economy. Decoys are weak targetable actors, not hidden alterations of enemy UI.

**Army:** Memory Infantry, Errata Lancers, Palimpsest Walkers, Decoy Echoes, Lantern Shades and Mnemonic Hounds. Namekeepers repair/capture; Remembrance Carriers harvest.

**Buildings:** Refuge of Names, Mnemonic Lamp, Remembrance Mill, Echo Hall, Palimpsest Foundry, Memory Beacon, Recollection Pool, Witness Lens, Index of Lives, Lantern Loft, Memory Den, Script Battery, Sky Quill and Archive of Names.

**Superweapon — Restoration:** supplied by the Archive of Names. Consume up to six nearby own memory remnants, each at most once, to create temporary Memory Echoes. No enemy reconstruction and no permanent free army. Deny the location or disengage until echoes expire.

## The Outer Silence — the spaces between signals

**Campaign:** territorial enclaves are usually neutral; named annihilationist splinters can be hostile, and threatened enclaves can accept limited cooperation. **Skirmish:** fully selectable. **Identity:** an alien presence beyond the known realms. Its factions disagree over withdrawal versus extinction. **Visual language:** dark negative-space bodies, dim indigo rims, broken circular geometry and minimal central light.

**Doctrine:** concealed scouts/ambushers, isolation bonuses and short-lived suppression. Attacking or taking damage reveals cloaked units; detectors remain effective. Suppression does not become permanent mind control or a global instant shutdown. Low durability and short attack ranges make prepared defenses, screens and overlapping detection effective counters.

**Army:** Hush Stalkers, Dissonance Lances, Null Leviathans, Stillness Seers, Eclipse Rays and Quiet Predators. Void Tenders engineer; Hollow Gatherers harvest physical deposits normally.

**Buildings:** Quiet Threshold, Dark Pulse, Hollow Siphon, Hush Chamber, Null Foundry, Deep Pulse, Stillwater Basin, Absence Lens, Boundary Archive, Eclipse Nest, Quiet Den, Hush Battery, Sky Void and Null Cathedral.

**Superweapon — Absolute Silence:** supplied by the Null Cathedral. A warned, local field suppresses enemy weapon output and supernatural effects for a limited duration. Movement remains possible so opponents can retreat; no map-wide disable and no automatic cancellation of charged enemy powers.

## Nephilim Remnant — giants with people to protect

**Campaign:** usually neutral sanctuaries and caravans; earned aid or localized hostility follows mission actions. **Skirmish:** fully selectable. **Identity:** an original fictional remnant drawing on the idea of ancient mortal/celestial ancestry, not a claim that a real-world group is monstrous. **Visual language:** weathered bronze, stone armor, cloth standards, towering proportions and small human attendants.

**Doctrine:** very expensive, slow giants supported by vulnerable attendants. Nearby attendants provide bounded protection/recovery; multiple copies do not stack. Giants remain powerful alone but lack economical replacement and cannot cover every raid. Focus support, kite slow attackers and attack their economy.

**Army:** Remnant Wardens, Cairn Slingers, Oathbound Giants, Mountain Bearers, Dawn Kites and Stonehorn Beasts. Human Attendants support; Cairnkeepers engineer; Burden Carriers harvest.

**Buildings:** Ancestral Seat, Hearth Tower, Burden Mill, Attendant Lodge, Giant Hall, Sun Hearth, Resting Court, Horizon Watch, Ancestral Chronicle, Dawn Roost, Stonehorn Pen, Cairn Battery, Sky Spear and Ancestral Cairn.

**Superweapon — Earthbreaker:** supplied by the Ancestral Cairn. A visible warned ground shock damages structures and grounded troops in a bounded radius; aircraft escape it. It does not permanently deform terrain or destroy every bridge on the map. Spread out, leave the warned area, or destroy/depower the source.

## Common implementation rules

All four powers use the established Defences sidebar and installation lifecycle. Initial shared settings: 6000 credits, 250 power, five-minute recharge, five-second warning; tune with recorded tests. Units must have explicit faction-specific HP, cost, movement, damage and reload values. All rosters need source artwork, directional sprites, damage/death states, icons, legal build prerequisites, bot lists and repair/harvesting paths.

The new factions' campaign roles are authored per mission in CAMPAIGN_PLAN.json. Neutrality is the default narrative relationship, not a skirmish restriction. In skirmish, normal player/team diplomacy applies. Full-match balance, local multiplayer/save-load, source/lifecycle cancellation and normal paid production are required acceptance categories.
