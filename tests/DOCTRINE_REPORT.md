# Additional subfaction verification — 25 October 2026

- Python regression suite: **79 passed**.
- Pure C# assertions: **7 dread + 104 Veilglass checks passed**.
- Native doctrine acceptance: **34 passed** in a fresh content-free support folder.
- Native paid construction/production: **39 passed** for the three new choices.
- Native existing-defense regression: **33 passed**, including conversion immunity.
- Pinned engine and extension build: passed; existing unused-upstream-text Fluent
  warnings remain. No new rule/sequence/condition errors or warnings were introduced.
- All **208 chrome collections** pass bounds checks at 1x/2x/3x.
- Standalone missing-sprite check: TEMPERAT passed; external RA references: zero.
- Subfaction generator: idempotence verified across faction registration, death
  images, rules, sequences and localization. Source/export hashes verified by tests.

The doctrine scenario checks actual Last Hymn firepower, enemy/self-kill attribution,
stacking and expiration, conviction/dread resistance, shrine reach, null-field effects
and power loss, physical wire remaining active, SERAPH/ABYSS switching and actual
weapon damage, condemnation ownership/Throne bonus, execution damage, Ascendancy,
retarget delay, Magistrate death and resumed angel healing.

The paid-production scenario deploys MCVs for Choir of Desolation, Area Fifty Two
and Circle of Contempt, pays for and places seven structures per player, produces
exactly one of each exclusive unit, and verifies accepted refinery income and
spending. It preserves normal production timing/prerequisites/placement rules.
One earlier run reported an extra Congregant; the full rerun logged each produced
count as exactly one. No underlying production defect was established from that
single observation. Its failed run is not counted as acceptance.

Development-test issues corrected during iteration included a duplicate armament
name, null-field queries on non-spatial actors, an unrevealed martyr target, a
Lua inspection of a dead actor, and the deployment scripting adapter. The final
logs below contain completion markers without failure markers:

- `native-evidence/subfactions-doctrines.txt`
- `native-evidence/subfactions-paid-production.txt`
- `native-evidence/subfactions-defense-regression.txt`

Initial art has original eight-view standing/movement/firing/destruction frames for
six units, six-state art for three defenses, and Janus damaged/critical idle art.
Facing/animation polish, faction-specific lobby emblems, full skirmish balance,
multiplayer synchronization and clean-machine release acceptance remain pending.
No complete-match or release approval is inferred from these component tests.
