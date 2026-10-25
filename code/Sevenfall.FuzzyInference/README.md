# Sevenfall squad inference

Original GPL-3.0-or-later implementation of the small Mamdani API used by OpenRA's
AttackOrFleeFuzzy squad decision class. It supplies trapezoid membership functions,
parenthesized AND/OR rule parsing, max-min aggregation and centroid integration.
The existing OpenRA squad rules and their attack/retreat threshold are retained.

This replaces the binary-only OpenRA-FuzzyLogicLibrary NuGet dependency, whose
listed source fork was unavailable during the release audit. No code from that
fork or the separate upstream fuzzynet project is included here. Namespace and
assembly names preserve the engine's existing reference API.

Numerical integration uses 256 intervals; full-match and multiplayer checks must
be rerun when this implementation changes. Tests cover shoulder endpoints,
centroids, nested rule aggregation, unmatched rules and invalid input rejection.
