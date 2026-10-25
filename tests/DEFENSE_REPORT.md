# Faction defense verification — 2026-10-25

Environment: Windows, pinned OpenRA release-20250330 engine, .NET 6 runtime,
legally installed Red Alert support content. No proprietary support assets are
included in the commit.

- Python unit discovery: 47 tests pass.
- Pure C# dread rules: seven timing/counterplay assertions pass.
- Native defense proving ground: 33 gameplay assertions pass, ending with
  `DEFENSE_TEST COMPLETE checks=33` after 58 simulated seconds.
- Full engine and extension build: zero warnings/errors. YAML and Fluent checks
  pass for nine maps and four tilesets. Missing-sprite checks pass for SNOW,
  INTERIOR, TEMPERAT and DESERT.

Native coverage includes wire/thorn movement penalties and damage; vehicle wire
crushing; concrete blocking; overlapping flesh walls not accelerating conversion;
sustained conversion and ownership changes; sanctuary healing/protection; retreat;
vehicle immunity; destruction and power loss stopping influence; flesh regeneration;
powered light killing infantry/armor, allied crossings and offline hostile crossings;
unpowered human gunfire; empty and occupied three-person entrenchments; all four
other ground turrets; all three AA defenses hitting aircraft and ignoring ground;
recent-convert immunity and subsequent reconversion after immunity expires.

The native harness uses flat terrain, caches references before actor destruction,
and explicitly sets both human and AI target stances to HoldFire. Synthetic target
actors are diagnostic-only and cannot be built. The runner closes its own game
process and fails on Lua errors, failure markers or a missing completion marker.

Visual inspection confirmed the original flesh wall renders in the native game.
Source and packed atlas inspection verified authored damage/pulse variants and
transparent game exports. This is an initial implementation; competitive balance,
large-match performance, visual polish and a full multiplayer soak remain pending.
