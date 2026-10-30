# Shared realm arsenal

All twenty subfactions inherit the buildings, defenses, aircraft, beast and shared
superweapon of their parent realm. The twelve existing subfaction powers remain.
All five realms already have power, economy, infantry/vehicle production, service,
radar, technology and defensive buildings. This pass fills their air/beast and
shared-power gaps; it does not claim a complete naval roster or campaign.

| Realm | Aircraft | Beast | Shared power |
|---|---|---|---|
| Humans | Bastion Gunship | Ironjaw Warhound | Nuclear missile |
| Angels | Sky Warden | Covenant Gryphon | Witness of Salt |
| Hell | Ash Wyvern | Cinder Hound | Hellrift |
| Noetic Assembly | Vector Interceptor | Logic Stalker | Extinction |
| Forsaken Host | Mourning Kite | Carrion Chimera | Sepulchral Rapture |

Aircraft are built from faction helipads/roosts; beasts use the infantry queue
but emerge from faction kennels/cradles. Each has distinct HP, speed, cost,
damage and reload values in `scripts/build_realm_completion.py`. The machine
interceptor is fastest and longest-ranged, the angel flyer is durable and slow,
and the fallen beast is strongest but slowest. Humans have the cheapest scout
beast; hell has cheaper assault aircraft.

Each shared installation requires its faction technology building, costs 6000,
consumes 250 power, has a five-minute recharge at normal speed and a limit of one.
Their power icons appear automatically at the top of the Defences tab and charge
without a purchase or queue click. Click a ready icon to target. Losing the last
supplying installation removes its icon and firing access; rebuilding starts a
fresh charge cycle. Losing electricity pauses charging. A surviving duplicate
installation keeps its shared power available. The Defences tab remains usable
without a Construction Yard if a power installation survives. These rules also
apply to all twelve subfaction powers.

All powers use normal support-power orders, explored-area targeting and a visible
five-second warning. Source destruction, ownership loss or power loss during the
warning cancels the strike. Existing faction-specific powers remain separate.

The nuclear missile damages everyone within six cells (60000 unit / 120000
building base damage). The Witness unfolds three pairs of wings above the target,
then flashes: units, buildings, trees and bridges within four cells become
salt-white, immobile, invulnerable statues with zero weapon damage. Buildings
lose power and production pauses. Four seconds later they crumble, regardless
of subsequent source destruction. Friendly and neutral actors are affected.
Terrain tiles, roads, cliffs and resource deposits are not transformed.

Hellrift burns enemies within five cells. Extinction delivers three pulses,
one second apart, with short combat-system disruption. Rapture damages enemies
and suppresses supernatural bonuses for thirty seconds. AI construction/unit
preferences and support-power decisions include the shared arsenal.

## Artwork and validation

Twenty original sheets were generated with the built-in image tool. Exact
prompts, source PNGs and hashes live in `art/realm-completion/`. The human missile
installation reuses existing human tech artwork because its generated sheet was
rejected by the image service. Initial animation uses authored idle/stride/action/
wreck poses; this is not a final animation or audio pass.

Rebuild with `python scripts/build_realm_completion.py`,
`node scripts/prepare_realm_painted_art.cjs realm-completion`, and
`python scripts/build_realm_arsenal_page.py`. Generate native acceptance using
`python scripts/generate_realm_completion_test.py`; run with
`python scripts/run_defense_test.py --scenario realmcompletion --support-dir PATH`.

Native checks cover paid production, aircraft ground attacks, all five powers,
friendly/neutral damage, warning cancellation and delayed salt destruction.
Recorded acceptance: 111 Python tests, 120 C# assertions, engine YAML/sprite/chrome
validation and [53 native checks](../tests/native-evidence/shared-arsenal.txt).
The existing subfaction powers also passed [78 native regression checks](../tests/native-evidence/shared-arsenal-regression.txt).
Full multiplayer/save-load, autonomous AI full matches, audio and competitive
balance remain separate acceptance work. Published alpha.2 is unchanged.

Building lifecycle and sidebar acceptance: 113 Python tests, engine validation,
and [173 lifecycle + 9 UI checks](../tests/native-evidence/power-lifecycle.txt).
Verified the grid at 1600×900 and 1280×720; a direct sidebar click selected and launched Nuclear.
