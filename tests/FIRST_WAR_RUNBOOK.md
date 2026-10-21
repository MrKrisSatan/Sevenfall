# Sevenfall 0.3 / First War gameplay runbook

**Status: not yet run in a live OpenRA match.** This report tracks three
implemented-source **campaign previews**, not the full 75-mission campaign,
not an independently installable Windows release and not nine-faction completion.

## Automated steps

From the project root on Windows:

```powershell
py -3 -m unittest discover -s tests
py -3 scripts/build.py build
py -3 scripts/build.py launch
```

The build command pins engine/SDK revisions, validates MiniYaml, installs the
three mission maps and their Lua scripts, compiles the engine, and runs the
OpenRA Utility YAML check. It does **not** simulate a human match.

## Preview mission acceptance

| Scenario | Menu launch | MCV deploy | Power/refinery | Harvester 2 deliveries | Troop/armour produced | Destroy enemy yard / victory | Own-yard loss / defeat | AI activity |
|---|---|---|---|---|---|---|---|---|
| H03 / The Glass Fields | NOT RUN | NOT RUN | NOT RUN | NOT RUN | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| A03 / A Glass of Wrath | NOT RUN | NOT RUN | NOT RUN | NOT RUN | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| D02 / Seeds of Ruin | NOT RUN | NOT RUN | NOT RUN | NOT RUN | NOT RUN | NOT RUN | NOT RUN | NOT RUN |

Instructions for each preview:

1. From Singleplayer → Missions, select the named Sevenfall campaign and
   its one visible preview. Record if the selector is missing.
2. Deploy the MCV. Build the side's power plant and refinery. Confirm the
   faction-appropriate **original** harvester exits.
3. Escort the harvester on **two visible full runs** from Veilglass deposit
   to the refinery, watching credits increase. The current Lua resource
   objective requires cumulative stored credits to increase by 900 but
   does not directly count physical deliveries.
4. Construct infantry and vehicle factories; **produce** at least one
   starting-side basic infantry and basic combat vehicle after game start.
   Initial guards do not count as produced troops.
5. Destroy the opposing command yard. The game should award victory only
   when economy + production + enemy-yard objectives have all completed.
6. Restart and lose **both** MCV and Construction Yard before the objectives
   complete. Confirm a loss rather than a silent game over.
7. Observe the enemy bot for rebuilding, harvesting, pathfinding, artillery
   and attack behavior. Inspect logs and replays for stalls and crashes.

Do not mark a row PASS from a successful CI build alone. Record hardware,
commit SHA, log path, observed resource delta, whether a real second unload
was seen, victory/defeat message, and any reported game errors.

## Remaining 0.3 milestones

- [ ] Full nine-subfaction skirmish runtime matrix, including parent and individual prerequisites
- [ ] Manual two-harvest-cycle verification on all three mining doctrines
- [ ] Infantry, armour, damage, loss and victory/defeat in all nine matchups
- [ ] Full-match AI attack/build/harvest test in every parent faction
- [ ] Original **animated** combat sprites integrated and rendered in live match
- [ ] All three Lua preview missions launch and resolve victory/failure in OpenRA
- [ ] Clean standalone, legally distributable Windows build and packaging

The three previews are a **vertical slice of design and engine integration**.
They do not replace these acceptance conditions.
