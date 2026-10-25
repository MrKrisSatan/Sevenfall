# Ashlands environment and repair gameplay

The alpha terrain library contains original grass, dirt, ash and gravel textures,
stone roads, dirt paths and impassable cliff tiles. Four tree designs block ground
movement and can be destroyed. Ashen Crossing is a two-player skirmish map using
these assets, with balanced starting mineral fields and two river crossings.

## Civilian houses

Uncontested nearby infantry claim an empty house. Once claimed, order infantry
inside to garrison it; its occupants fire their faction garrison weapons through
four ports. Cottages hold four infantry, townhouses six. An occupied house cannot
be stolen by nearby enemies. Empty houses return to neutral when no infantry are
nearby. Ownership is shown with a player-colour marker.

Both designs have intact, scratched, heavily damaged and ruined artwork. Force
fire can damage or destroy them, including friendly houses. Destroyed houses eject
their occupants and leave passable rubble. Engineers fully repair surviving
friendly or neutral houses and survive the repair. House rubble cannot currently
be rebuilt. Damage and repairs select the corresponding sprite automatically.

## Bridges

East-west and north-south spans have intact, scratched, damaged and destroyed
frames. Force fire can destroy them. Destruction restores the underlying water
terrain and kills ground units stranded on the span. Engineers repair damaged
or destroyed bridges by entering the adjacent bankside maintenance post; they
survive the repair. The post is an indestructible repair access point. Bridges
must be placed over water with a post adjoining their footprint.

## Faction engineers

| Faction | Unit | Cost | HP | Speed | Specialisation |
|---|---|---:|---:|---:|---|
| Angelic | Restorer | 500 | 7,000 | 70 | Durable; regenerates after combat |
| Human | Field Engineer | 350 | 4,500 | 87 | Balanced cost, speed and durability |
| Infernal | Infernal Mason | 250 | 3,000 | 105 | Cheap, fast and fragile |

Engineers are unarmed, reusable and trained at their faction's infantry building.
They temporarily reuse existing original faction sprites with a visible plus
marker. Dedicated engineer artwork remains a presentation backlog item.

## Validation and known limits

Engine compilation and YAML/sequence/Fluent validation pass. Structural map tests
verify each bridge connects the banks and losing both separates them. These are
not native pathfinding or combat results. The native environment diagnostic is
**NOT RUN** and can be launched after installing development test content:

```
python scripts/run_defense_test.py --scenario environment --support-dir PATH --dotnet .tools/dotnet/dotnet.exe
```

It exercises garrison entry, house repair, forced bridge destruction, restoration,
ground passage, forced house destruction and occupant ejection. Manual acceptance
must additionally cover all three engineers, north-south bridges, damage-frame
alignment at game zoom, enemy/contested ownership, occupied-house firing, blocked
exits, bridge collapse with units on it, replay and multiplayer synchronisation.
No native pass or standalone release readiness is claimed.

Terrain transitions are preliminary: shore edges, cliff junctions and road/path
seams need an in-game visual pass. Existing maps retain compatible terrain IDs.
