# OpenRA integration acceptance checklist

Reusable checklist for a new candidate. Record results independently; see [current release evidence](../docs/TESTER_ALPHA_ACCEPTANCE.md) for completed checks.

- [ ] Starter overlay loads in OpenRA without missing rules/traits/actor exceptions.
- [ ] All twenty lobby subfactions appear and load appropriate prerequisites.
- [ ] Angel, Human, Demon, Noetic and Forsaken MCVs deploy construction yards.
- [ ] Each side builds power, refinery and infantry production.
- [ ] Five faction-specific collectors navigate to Veilglass, collect it and unload.
- [ ] Deposits deplete and the player's resources increase by the correct amount.
- [ ] At least one infantry and one vehicle type per major faction can be produced.
- [ ] All five realms can normally build aircraft, beasts and supplying superweapon installations.
- [ ] All seventeen powers charge in Defences, disappear on last-source loss and restart after rebuilding.
- [ ] Combat weapons hit intended target classes and damage is applied.
- [ ] Base destruction triggers correctly and victory/defeat terminates the match.
- [ ] Each AI builds, harvests and attacks without referencing removed RA actor IDs.
- [ ] A full skirmish can run to completion without crashes or infinite pathfinding.
- [ ] Release archive installs and launches on a second clean test machine.

Record SDK commit, engine commit, OS and complete logs next to results.