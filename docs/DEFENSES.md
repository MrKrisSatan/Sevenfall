# Faction defenses

All nine subfactions can build their parent faction's five defenses from the Defense tab. These are prototype balance values at normal game speed.

| Faction | Defense | Purpose and counterplay |
| --- | --- | --- |
| Angels | Wall of Dawn | Allies cross its light curtain safely. Hostile ground units crossing the powered field are incinerated. Cut power or destroy it from range. |
| Angels | Sanctuary Beacon | Heals nearby allied infantry and clears/prevents the dread caused by flesh walls. Requires power. |
| Angels | Watchfire Bastion | Powered anti-infantry fire, weak against heavy armor. |
| Angels | Judgment Lance | Powerful, slow, long-range anti-armor emplacement. |
| Angels | Skyward Choir | Powered anti-air defense; cannot shoot ground targets. |
| Humans | Blast Wall | Solid reinforced concrete blocks ordinary vehicles and projectiles. Artillery and demolition can breach it. |
| Humans | Razorwire | Passable wire slows and injures enemy infantry. Hostile vehicles crush it; allies pass freely. |
| Humans | Entrenchment | An initially empty position for three infantry. Occupants supply its firepower; evacuate to preserve them. |
| Humans | Autocannon | General ground defense with a mechanical backup that works without grid power. |
| Humans | Skyguard Missile Nest | Independent anti-air missiles; does not engage ground troops. |
| Demons | Mourning Flesh | Regenerating walls moan and build dread in enemy infantry within three cells. Twelve seconds of exposure changes their owner to the wall's owner. |
| Demons | Living Thornfield | Passable, damaging thorns slow hostile infantry more strongly than wire. Vehicles crush them. |
| Demons | Spine Nest | Powered anti-infantry organic turret. |
| Demons | Cinder Maw | Powered short-range anti-armor emplacement. |
| Demons | Skyhook Spire | Powered anti-air organic defense. |

Mourning Flesh does not stack its conversion rate. A purple selection bar shows rising dread. Leaving its radius drains exposure twice as fast as it accumulates. Vehicles are immune. Sanctuary protection clears dread, destroying the wall stops its influence, and loss of demonic power silences it. Converted infantry receive 30 seconds of immunity against immediate conversion back. All ownership changes use deterministic engine logic and cancel the unit's current orders.

Light walls are passable energy fields rather than physical blockers. Their lethal radius covers the crossing cell; it does not pursue enemies. Their offline frame makes a power failure visible. Normal hostile diplomacy determines affected units, so allies are safe.

## Art and implementation

The 15 original six-state atlases include healthy, damaged, critical and firing/pulse frames, with an offline frame for the light wall. Sources and generation prompts are in `art/defenses/catalogue.json`; SHA-256 provenance and frame hashes are in `art/defenses/manifest.json`. The mourning sound is an original synthesized waveform, with no sampled voice.

`code/OpenRA.Mods.Sevenfall` implements power-conditioned fields and dread on every gameplay map. The source is built by `scripts/build.py` and loaded by the staged mod. YAML supplies construction, faction prerequisites, line building, garrison behavior, weapons, AI preferences and damage states. This is an initial defense pass; large-match performance and competitive balance still need playtesting.

## Reproduce validation

Run Python unit discovery, `dotnet run --project tests/Sevenfall.DefenseTests -c Release`, and `python scripts/build.py test`. With legally installed Red Alert content, run `python scripts/run_defense_test.py --support-dir PATH`. Its developer map exercises live conversion, immunity, sanctuary, power loss, vehicle crushing, movement penalties, light crossings, garrison fire and air/ground targeting. The runner requires the completion marker and reports failures with a native transcript.
