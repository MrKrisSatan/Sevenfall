# The Noetic Assembly and the Forsaken Host

Development expansion: **five parent realms, twenty selectable subfactions**.
The published alpha.2 remains a twelve-choice release; these additions require a
new development build. Each new choice has two exclusive paid units, a shared
realm economy/army, and a combat doctrine. No existing faction is removed.

## Noetic Assembly

Human defense models, embodied assistants and uploaded minds survived the
Seventh Seal inside Veilglass computation lattices. They disagree about whether
protecting humanity means defending its freedom, replacing its soldiers,
containing its choices, or teaching it to reason beyond war.

The influences are themes, not adaptations: embodied identity and networked
consciousness; autonomous extermination machinery; simulated custodianship;
strategic games that mistake people for counters; and an accidental merger of
human intuition with computing. No named film character, organization, likeness,
dialogue or franchise machine design is used.

| Subfaction | Playstyle and doctrine | Exclusive units | Counterplay |
|---|---|---|---|
| Echo Directorate | Reconnaissance and prepared precision: after 3 seconds stationary, +30% damage and +15% range | Mnemonic Ghost: fast cloak-detecting scout infantry. Needle Chassis: fragile long-range precision vehicle | Force movement, flank, exploit the Needle's long reload |
| Iron Calculus | Armored attrition: 20% less incoming damage, 15% less speed | Endurer: durable expensive infantry. Crucible Engine: very slow heavy siege chassis | Outmaneuver, deny resources, avoid frontal trades |
| Custodian Grid | Formation network: within 4 cells of a friendly Relay Walker, 20% faster reload and 10% less incoming damage | Threadkeeper: anti-armor infantry. Relay Walker: armed network anchor | Destroy or separate relays; bonuses do not stack |
| Paradox Collegium | Adaptive harassment: below half health, +30% speed and 15% faster reload | Circuit Savant: fragile rapid-fire infantry. Gambit Rover: fast light vehicle | Burst damage and interception; do not feed repeated escapes |

Shared infrastructure: Cognition Reactor, Matter Compiler, Shell Foundry,
Chassis Forge, Fusion Stack, Reconstruction Bay, Prediction Spire and Recursion
Core. Reclaimers harvest Veilglass. Shell Troopers, Breach Automatons and Sentinel
Chassis provide the shared force; Repair Proxies repair civilian structures and
bridges. Sentry and Interceptor Nodes defend the base.

## Forsaken Host

These are former celestial beings who knowingly repudiated their covenant with
God. Their bodies no longer agree with the offices they once embodied: crowns
sink into skulls, wings ossify into cages, throats close around stolen hymns, and
halos become load-bearing wounds. They differ from both Hell's native Demons and
the existing angelic Unshackled. Their rejection is deliberate spiritual ruin,
not merely political independence.

This is Sevenfall's fiction, drawing broadly on biblical rebellion, judgment,
fallen heavenly powers and later angelic/gothic imagery. It does not present its
invented anatomy or four orders as biblical doctrine. Horror emphasizes broken
symmetry, bone, torn vestments and corrupted sacred architecture.

| Subfaction | Playstyle and doctrine | Exclusive units | Counterplay |
|---|---|---|---|
| Ashen Thrones | Entrenched aristocracy: after 4 seconds stationary, 30% less incoming damage, 15% longer reload | Uncrowned Regent: armored fallen noble. Walking Reliquary: bone-bound siege engine | Force repositioning and exploit slow fire |
| Hollow Choir | Risky procession: within 4 cells of a Lamentor, +25% damage dealt but +10% damage received | Mute Canticle: inexpensive ranged worshipper. Lamentor: profane hymn relay | Kill the relay or punish the vulnerability with area damage |
| Carrion Testament | Wounded aggression: below half health, +40% damage and +15% speed | Vow Flayer: fast melee infantry. Carrion Martyr: heavy melee abomination | Kite, screen and finish wounded attackers quickly |
| Broken Firmament | Dispersed hunters: without another friendly armed unit within 4 cells, +25% speed and +20% range | Severed Pinion: grounded hunter with ruined wings. Harrow Stalker: mobile flanking engine | Concentrate locally, surround isolated units, deny escape routes |

Shared infrastructure: Apostate Pyre, Ossuary Mill, Profaned Chapel, Flesh
Crucible, Sundered Halo, Suture Shrine, Blind Oracle and Testament Vault. Tithe
Bearers harvest Veilglass. Oath Husks, Blight Heralds and Bonebound Engines form
the shared force. Suture Keepers repair civilian structures and bridges.
Balefire Watches, Wrath Organs and Broken Halo Batteries provide defenses.

## Implementation and boundaries

- Subfaction combat bonuses exclude collectors and unarmed engineers. Existing
  containment/null suppression disrupts the new bonuses. Relay effects use own
  units, do not stack, and expire after the source is lost or leaves range.
- Shared combat units have distinct HP, cost and weapon damage from their donor
  definitions. Forsaken combat units do not inherit angelic Renewal or demonic
  Blood Frenzy. Each exclusive unit has explicit HP, cost, speed and weapon.
- 51 painted sheets replace the temporary bodies: 23 buildings and 28 units,
  including construction yards, MCVs, collectors and all sixteen exclusive units.
  Units have eight directions and four authored states: idle, stride, action and
  wreck. Buildings have intact, damaged, critical, two construction and operating
  states. The sequence pack holds each wreck for three frames; this is one pose,
  not three death phases. Mobile damage states still reuse the intact body.
- Machine HUDs use cyan/blue circuitry; Forsaken HUDs use violet/bone and a
  broken-wing emblem. Neutral menus remain neutral.
- This pass adds no new superweapons, aircraft, naval or flying fallen units.
  Grounded wings are intentional. These are future content decisions, not hidden
  promises in the unit descriptions.
- Native component acceptance is not a full-match balance, multiplayer or
  save/load certification for this expanded roster. Keep those results separate.

## Rebuild

Run `python scripts/build_new_realms.py`, `node scripts/prepare_realm_painted_art.cjs`,
`python scripts/bind_realm_painted_art.py`,
`node scripts/build_realm_flags.cjs`, `python scripts/build_new_realms_page.py`
and `node scripts/build_ui.cjs` (Node requires sharp). Then generate the native
maps with `scripts/generate_new_realms_test.py` and
`scripts/generate_realm_doctrine_test.py`, and use `scripts/build.py build`.
Run `scripts/run_defense_test.py --scenario newrealms --support-dir PATH
--timeout 700` for paid production, and `--scenario realmdoctrine` for doctrine
activation/expiration. Diagnostic maps are excluded by the public map allowlist.

The reviewed roster and stats live in `design/NEW_REALMS_ROSTER.json` and the
generator. Full sprite provenance is recorded in `art/new-realms/painted-manifest.json`.

The painted pass also supplies eight distinct vector faction flags for lobby and
unit tooltips. A native tooltip inspection exposed the missing flag mappings;
all eight are now bound and covered by the selection contract test.

Painted-pass acceptance: 108 Python tests, engine YAML and missing-sprite checks,
245 chrome collections at 1x/2x/3x, and a native 51-design rendering smoke scenario
covering movement, damaged/critical buildings and death actors. See
[rendering evidence](../tests/native-evidence/painted-realms-rendering.txt).
All [96 paid-production checks](../tests/native-evidence/painted-realms-production.txt)
were rerun successfully with the painted art and corrected faction flags.

## Recorded development acceptance

- 107 Python tests and 120 C# assertions passed.
- Engine YAML/sequence/Fluent validation passed; 244 interface collections passed
  bounds validation at 1x, 2x and 3x density.
- [96 native production checks](../tests/native-evidence/new-realms-production.txt):
  all eight choices deployed an MCV, paid for and placed power, infantry factory,
  refinery and vehicle factory, received actual refinery income, and produced
  shared infantry/armor plus both exclusive units.
- [24 native doctrine checks](../tests/native-evidence/new-realm-doctrines.txt):
  activation, low-health thresholds, actual armor/speed multipliers, relay-loss
  expiration, isolation restoration and collector exclusion.

These controlled tests do not certify autonomous AI performance, every advanced
building, multiplayer synchronization, save/load or competitive matchups for the
new choices. Existing alpha.2 acceptance is not relabeled as expansion acceptance.
