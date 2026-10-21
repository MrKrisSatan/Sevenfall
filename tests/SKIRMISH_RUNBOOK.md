# Sevenfall 0.2: first playable skirmish runbook

**Status: awaiting manual OpenRA runtime verification.** Static tests and a
successful menu launch are not a substitute for the runs in this document.
Use [BUILDING.md](../BUILDING.md) to install, build, and launch the pinned engine.

## Prerequisites and reproducibility

1. Record the Sevenfall commit SHA, OpenRA/SDK pins in `BUILDING.md`, Windows
   version, GPU, .NET version, player count, and whether Red Alert test
   content was installed locally.
2. Run `py -3 -m unittest discover -s tests`, then
   `py -3 scripts/build.py build` and `py -3 scripts/build.py launch`.
   Linux uses `python3` instead of `py -3`. Record failures and logs.
3. Select **Singleplayer → Skirmish → Broken Choir - Proving Ground**.
   Use **MCV only**, **5,000 starting credits**, and normal game speed.
   Disable the opponent AI for the economy-only pass where possible;
   use the **Sevenfall AI (prototype)** for the later opponent pass.
4. Record outcomes separately for each faction. A static check's success
   must not be marked as an in-game PASS.

## Economy, production, combat and victory procedure

For **each of the nine lobby selections**:

- [ ] Spawn and deploy the correct side's MCV into a Construction Yard.
- [ ] Build that side's power building; observe positive available power.
- [ ] Build that side's Veilworks. Record credits before and after building.
- [ ] Confirm that the refinery spawns the correct faction harvester, not a
      Red Alert default. Watch it drive to Veilglass and return **twice**.
- [ ] Observe resource tiles disappearing/declining and credits **rising
      after unloading**. Distinguish unloading income from build refunds.
- [ ] Build the faction's infantry structure and produce one basic troop.
- [ ] Build the faction's vehicle factory and produce one combat vehicle.
- [ ] Verify the other major factions' buildings/units are **not** in the
      production sidebar. Verify the two other subfactions' exclusives are
      unavailable.
- [ ] Verify the selected subfaction's exclusive troop is available when
      its tech prerequisites are met.
- [ ] Move troops and armour over the map, attack an enemy, confirm damage,
      casualties and structure destruction.
- [ ] Destroy the last enemy base and confirm a clean victory result.
      On a second run, lose your last base and confirm defeat.

## Nine-faction acceptance matrix

Use **PASS**, **FAIL** or **NOT RUN** for every column. Leave unfinished
cases as **NOT RUN**, never inferred from another faction.

| Faction | Deploy and power | Two harvest cycles | Infantry and armour | Exclusivity | Combat and victory | AI opponent |
|---|---|---|---|---|---|---|
| Seraphic Synod | NOT RUN | NOT RUN | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| Order of the Gate | NOT RUN | NOT RUN | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| The Unshackled | NOT RUN | NOT RUN | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| Bastion Directorate | NOT RUN | NOT RUN | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| Free Earth Union | NOT RUN | NOT RUN | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| Ashen Covenant | NOT RUN | NOT RUN | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| Iron Legions | NOT RUN | NOT RUN | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| Blood Brood | NOT RUN | NOT RUN | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| Court of Whispers | NOT RUN | NOT RUN | NOT RUN | NOT RUN | NOT RUN | NOT RUN |

## AI and multiplayer follow-up

Run each parent faction against **Sevenfall AI (prototype)** for **20 minutes**
without manually aiding the bot. Record whether the AI builds a refinery and
power, uses the correct harvester, produces legal troops, attacks, and recovers
after losing production buildings. Repeat at least one **full AI-versus-AI**
match and one **two-human** match. Inspect OpenRA logs for crashes, missing
actor IDs, stalls and replay/desync warnings.

## Record a result

Copy this block for every test run:

```text
Date/time:
Sevenfall commit:
SDK commit / engine commit:
OS / GPU / .NET version:
Skirmish map / starting credits / opponent:
Player faction:
Steps passed:
Steps failed (exact observed behavior):
Duration / number of full unload cycles:
Credits before / after unload:
Victory/defeat result:
OpenRA logs / screenshot / replay references:
Issue URL for reproduction:
Retest commit and outcome:
```

Open or update [GitHub Issues](https://github.com/MrKrisSatan/Sevenfall/issues)
for each reproducible failure. Keep the first playable milestone open until
the economic and combat loops are verified in the real engine.
