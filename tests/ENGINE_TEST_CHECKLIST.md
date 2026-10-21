# OpenRA integration acceptance checklist

All checkboxes remain unchecked until verified in a real OpenRA SDK environment.

- [ ] Starter overlay loads in OpenRA without missing rules/traits/actor exceptions.
- [ ] All nine lobby subfactions appear and load appropriate prerequisites.
- [ ] Angel, Human and Demon MCVs deploy construction yards.
- [ ] Each side builds power, refinery and infantry production.
- [ ] Three faction-specific harvesters navigate to Veilglass, collect it and unload.
- [ ] Deposits deplete and the player's resources increase by the correct amount.
- [ ] At least one infantry and one vehicle type per major faction can be produced.
- [ ] Combat weapons hit intended target classes and damage is applied.
- [ ] Base destruction triggers correctly and victory/defeat terminates the match.
- [ ] Each AI builds, harvests and attacks without referencing removed RA actor IDs.
- [ ] A full skirmish can run to completion without crashes or infinite pathfinding.
- [ ] Release archive installs and launches on a second clean test machine.

Record SDK commit, engine commit, OS and complete logs next to results.