# Twelve hosts, twelve ways to wage war

All twelve faction choices now have an active gameplay identity, two exclusive
units and an exclusive late-game superweapon. The parent faction's economy and
core units remain available, so recognizable armies can develop different plans.
These are implemented alpha mechanics; competitive balance remains playtest work.

| Faction | Mechanic and play style | Exclusive units | Superweapon |
|---|---|---|---|
| Seraphic Synod | Stand still 3s for +30% firepower and +15% range. Prepare deliberate volleys; movement interrupts focus. | Seraphim, Luminary (long-range light infantry artillery) | **Spear of First Light:** 4-cell strike; 15,000 troop / 25,000 building damage. 240s recharge. |
| Order of the Gate | Within 4 cells of a Gatekeeper or Wardbearer: 25% less incoming damage, 10% slower movement. Relays never stack. | Gatekeeper, Wardbearer (infantry shield relay) | **The Unbroken Gate:** allies in 6 cells take 65% less damage and regenerate 2% HP/sec for 15s. 210s. |
| The Unshackled | Below half HP: +35% firepower and +20% speed. Fast, dangerous survivors reward kiting and timely retreats. | Penitent, Exile Outrider (fast attack chassis) | **Heaven in Revolt:** allies in 6 cells gain +40% firepower and +50% speed for 20s, but take 20% more damage. 180s. |
| Choir of Desolation | Expendable human deaths inside a live hymn network build capped, expiring Resonance for its angels. | Ashbound Congregant, Cantor of Desolation | **Requiem for the Living:** allies in 6 cells gain +45% firepower for 20s; enemy infantry lose 25% firepower and 35% speed for 12s. 240s. |
| Bastion Directorate | Stand still 4s for 20% less damage and +15% range; moving breaks entrenchment. Prepare firing lines and protect artillery. | Siege Cannon, Bastion Sapper (short-range anti-building rockets) | **Rolling Thunder:** three eastward 3-cell impacts one second apart; each deals 9,000 troop / 18,000 building damage. 240s. |
| Free Earth Union | Friendly Harvesters and Pathfinders project 6-cell supply corridors: +15% speed and 15% shorter reloads. Escort logistics and reposition together. | Ranger, Pathfinder (fast scout/supply vehicle) | **Emergency Airlift:** allied troops in 7 cells recover 30% max HP and gain +30% speed for 20s. 150s. |
| Ashen Covenant | Within 4 cells of a Templar or Confessor: 10% less damage; infantry also recover 200 HP/sec. One aura per troop. | Templar, Ash Confessor (armed field medic) | **Ashes to Ashes:** fully heals allied infantry in 6 cells and reduces their incoming damage by 80% for 12s. 210s. |
| Area Fifty Two | Powered pylons switch Janus SERAPH/ABYSS weapons and suppress supernatural effects locally, including friendly effects. | Retrieval Team, Janus Tank | **Project Event Horizon:** 5-cell implosion deals 12,000 enemy damage; all nearby troops, including friendly troops, lose movement and weapon damage for 6s and are nullified for 30s. 270s. |
| Iron Legions | Hellreavers and Taskmasters project a 4-cell siege formation: 25% less incoming damage, 15% slower movement. | Hellreaver, Iron Taskmaster (command infantry) | **The Ninth Furnace:** 4-cell strike deals 65,000 building / 10,000 troop damage; enemy survivors move at 40% speed for 10s. 270s. |
| Blood Brood | Killing an enemy mobile unit heals its killer by 10% max HP (cap 5,000), then grants 25% shorter reloads and +15% speed for 6s. Friendly kills/buildings grant nothing. | Skitter, Goremaw (heavy melee predator) | **The Red Deluge:** allied infantry in 7 cells recover 25% max HP, regenerate 2% HP/sec and reload 35% faster for 30s. 180s. |
| Court of Whispers | Hexer/Silencer attacks curse an enemy for 4s: 35% slower movement and 25% less weapon damage. Repeated attacks refresh rather than stack. | Hexer, Silencer (fragile long-range curse caster) | **The Nameless Silence:** enemies in 5 cells deal no weapon damage for 12s; mobile enemies also cannot move. Does not halt superweapon charge or passive wall damage. 240s. |
| Circle of Contempt | Magistrates condemn a priority target; Contemptors punish wounded enemies. Credited executions grant nearby troops timed Ascendancy. | Magistrate of Ash, Contemptor | **The Final Verdict:** 5-cell strike deals 25,000 damage to enemy units below half HP, 8,000 to other units, 15,000 to buildings; nearby allies gain +45% firepower for 12s. 240s. |

## Controls, limits and counterplay

Build your radar and advanced technology building, then the faction's named
**Array** in the building tab. Each costs 4,500 credits, consumes 150 power and
has 65,000 HP. One array of that type can be built per player. Its sidebar icon
charges normally; select the power and click explored terrain. A radius preview
shows the affected ground, including all three Rolling Thunder circles.

All powers have a **three-second warning**, visible rings and a public enemy
charge timer. Move out, spread an army, or destroy, capture or depower the array.
The array must survive with the same owner and adequate power until impact;
cancellation spends the charge. Rolling Thunder needs the array for each pulse.
There is no instant map-wide annihilation or forced permanent conversion in these
new superweapons. Existing flesh-wall dread conversion remains unchanged.

Support auras use the current owner and cannot stack with another copy of the
same aura. Different bonuses multiply; an Order shield inside The Unbroken Gate
takes about 26% of ordinary incoming damage. Parent Renewal/Blood Frenzy and the
three earlier doctrines remain. Null fields interrupt supernatural passives and
supernatural protection/regeneration; conventional Bastion entrenchment and Union
logistics continue. Suppression from a pylon cannot shorten Event Horizon's timer.

Passives update within five ticks. Stationary preparation resets when crossing a
cell; turning inside that cell preserves a prepared firing position. Feeding
requires an attributed enemy mobile-unit kill; it is neither free income nor free
production. Damage values are engine HP units before active damage modifiers.

The nine added specialists reuse Sevenfall's original animated infantry/vehicle
bodies and death cycles with distinct role labels, names, stats and weapon/ability
bindings. They are authored roster variants, not nine new illustrations. Arrays
likewise use existing faction technology-building art. The twelve telegraphs are
original animated code-drawn effects with different colors and ring patterns.

## AI and acceptance

The AI can build radar, technology, its exclusive specialists and its array.
Support decisions target hostile groups for strikes and allied groups for buffs;
the infantry-only Covenant/Brood powers prefer infantry. Native AI acceptance
uses prepared armies and arrays and issues no scripted support-power orders.
It verifies actual independently launched powers, not just configuration entries.

The native `identity-test` covers all twelve real powers, passive damage/firepower/
movement effects, regeneration above half health, non-stacking formation armor,
warning delay, recharge, friendly-kill rejection, expiry, and cancellation by
destruction, power loss and capture. Existing doctrine, two-client synchronization
and real save/load acceptance remain separate regression gates. Diagnostic maps
are excluded from public skirmish packages.

```
python scripts/build_faction_identities.py
python scripts/generate_identity_test.py
python scripts/build.py test
python scripts/run_defense_test.py --scenario identity --support-dir artifacts/identity --timeout 180
python scripts/run_defense_test.py --scenario identityai --support-dir artifacts/identityai --timeout 180
```
