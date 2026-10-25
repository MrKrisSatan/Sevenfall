# GitHub issue review — 25 October 2026

Reviewed all **11 existing issues** (10 open, 1 closed) against current main
`7d44998`, released [alpha.2](https://github.com/MrKrisSatan/Sevenfall/releases/tag/v0.3.0-alpha.2),
[exact-package acceptance](https://github.com/MrKrisSatan/Sevenfall/actions/runs/40243071020),
committed native transcripts, implementation sources and documented alpha limits.
Pull requests were excluded from issue-state edits. This review inspected existing
results; it did not rerun gameplay or competitive balance tests.

## Existing issues

| Issue | Result | Basis / remaining work |
|---|---|---|
| [#1](https://github.com/MrKrisSatan/Sevenfall/issues/1) Starter source | Closed completed | Historical integration report records the starter import; current tagged sources and scripts are distributed. Original-ZIP parity was not repeated; the historical archive comparison was explicitly superseded. |
| [#2](https://github.com/MrKrisSatan/Sevenfall/issues/2) Pinned SDK boot | Closed completed | Pinned build provenance, Windows/Linux engine checks and repeated native package launches. |
| [#3](https://github.com/MrKrisSatan/Sevenfall/issues/3) Nine selectors | Closed completed | Expanded to twelve; native MCV starts, original/additional paid production transcripts and prerequisite contracts. Advanced paid progression remains #22. |
| [#4](https://github.com/MrKrisSatan/Sevenfall/issues/4) Physical harvesting | Closed completed | Real collectors, deliveries/income, deposit consumption and standard search/loss/idle behavior are implemented. Comprehensive edge-case acceptance remains #23. |
| [#5](https://github.com/MrKrisSatan/Sevenfall/issues/5) Combat/victory | Kept open; narrowed | Core loop and controlled two-client tests exist. Complete player-controlled PvP conquest/result/replay acceptance remains. |
| [#6](https://github.com/MrKrisSatan/Sevenfall/issues/6) AI | Kept open; updated | Basic economy, production, attacks, AI conquest and prepared power use have evidence. Ordinary expansion/recovery and broader human-vs-AI/full-match acceptance remain. |
| [#7](https://github.com/MrKrisSatan/Sevenfall/issues/7) Parent asymmetry | Kept open; updated | Land identities and counters are implemented; actual gateways and advanced domains remain. |
| [#8](https://github.com/MrKrisSatan/Sevenfall/issues/8) Unique technologies | Closed completed | All twelve choices have mechanics, two exclusives and a unique power. Component impact/counterplay is verified; competitive tuning and paid late-game progression remain #22. |
| [#9](https://github.com/MrKrisSatan/Sevenfall/issues/9) Original presentation | Kept open; updated | Distribution/source inventory gates are complete. Audio, emblems, bespoke variant art and presentation polish remain. |
| [#10](https://github.com/MrKrisSatan/Sevenfall/issues/10) Campaigns/full release | Kept open; updated | Windows skirmish release is complete; three developer previews await native acceptance, 72 further missions and full campaign progression remain. Linux separated into #27. |
| [#11](https://github.com/MrKrisSatan/Sevenfall/issues/11) GitHub Pages | Remains closed | Website and current release/field-guide pages are live; no status edit needed. |

Each newly closed issue has a completion comment with direct evidence and linked
follow-ups. Open issue bodies now distinguish implemented work from outstanding
acceptance. Campaign status, twelve-choice scope and the published Windows release
replace obsolete statements; the campaign issue's broken links/encoding were fixed.

## New, concrete follow-ups

| Issue | Work |
|---|---|
| [#22](https://github.com/MrKrisSatan/Sevenfall/issues/22) | Twelve-faction full-match balance and normally paid advanced progression. |
| [#23](https://github.com/MrKrisSatan/Sevenfall/issues/23) | Exhausted deposits, destroyed collectors/refineries and route/recovery accounting. |
| [#24](https://github.com/MrKrisSatan/Sevenfall/issues/24) | Real Internet/NAT/latency, disconnect and supported reconnect behavior. |
| [#25](https://github.com/MrKrisSatan/Sevenfall/issues/25) | Sustained twelve-player performance, long-session stability and GPU compatibility. |
| [#26](https://github.com/MrKrisSatan/Sevenfall/issues/26) | Native H03/A03/D02 win/fail/economy/save acceptance before campaign expansion. |
| [#27](https://github.com/MrKrisSatan/Sevenfall/issues/27) | A genuinely standalone, tested Linux x64 distribution. |
| [#28](https://github.com/MrKrisSatan/Sevenfall/issues/28) | Aircraft, naval and beast gameplay/production/AI acceptance beyond the land alpha. |

Every new issue includes acceptance criteria, scope boundaries and evidence or
parent-issue links. Untested areas were recorded as QA work, rather than labelled
as reproduced bugs. Result: **5 completed issues closed, 5 unfinished issues
updated, 7 new issues created; 12 open and 6 closed issues total**.

The [roadmap](../ROADMAP.md) now follows these issue states. Historical test/runbook
reports remain historical; unrecorded human/full-match/campaign results were not
inferred from native component checks.
