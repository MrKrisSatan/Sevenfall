# Four independent factions — 2 November 2026

Development scope: Veilborn, Unwritten, Outer Silence and Nephilim Remnant, with no subfactions. The original twenty choices are retained. Three new choices are available in skirmish; Veilborn is hidden pending genuine campaign progression. This report does not describe the already published five-faction alpha.3 binary.

## Verification

- **119 Python tests passed**, covering existing content plus four-faction selection boundaries, 94 source/packed art hashes, complete roles, website coverage and NPC-only campaign encounters.
- **120 C# assertions passed** for the existing dread, Veilglass and fuzzy-inference rules.
- Pinned OpenRA build and all map YAML/sprite checks passed. **317 merged chrome collections** validated at 1x, 2x and 3x.
- **126 native additional-realm checks passed:** MCV deployment, all 13 paid production/technology/defense buildings per realm, all 33 paid combat/logistics units, cash deductions and physical Veilglass deliveries; powered crystal protection, attendant recovery, loss of aura source, collector exclusion, isolation speed; Restoration consumes the targeted memory and produces a temporary non-recursive echo; Earthbreaker damages ground/structures and excludes aircraft; suppression expires; Bloom protection; powers disappear when the last supplying installation is destroyed.
- **Seven enclave assertions passed** in disposable copies of the actual H03/A03/D02 scripts: neutral camps, engineer aid, subsequent hostility when attacked, and the initially hostile Outer Silence encounter. No player ownership is granted to the enclave faction.
- Painted contact sheet inspected. Website profile cards, symbols, per-faction filtering and artwork loading inspected in the browser. The current site contains **275 field-guide entries** and **131 directional entries / 1,048 views**, including 14 labelled future concepts. Sources and generation prompts are retained.

The production diagnostic keeps real costs and prerequisites, with accelerated build durations and charge timers. Separate fields remain within the collector's normal resource-search radius, and test troops are moved clear of them. Earlier attempts exposed fixture problems (out-of-range fields and unrelated combat casualties counted as Restoration remnants); the final map checks the target memory specifically and retains real physical collection.

## Reproduce

```text
python scripts/build.py build
python -m unittest discover -s tests
dotnet run --project tests/Sevenfall.DefenseTests
python scripts/run_defense_test.py --scenario additionalrealms --support-dir .tools/acceptance-additional --timeout 280
python scripts/run_campaign_enclave_test.py
```

Art: `node scripts/prepare_realm_painted_art.cjs additional-realms`, then `python scripts/prepare_extended_turnarounds.py`. Site: `build_site_catalogue.py`, `build_additional_realms_page.py`, `build_turnaround_gallery.py`, `build_site_subfactions.py`, `build_campaign_site.py`.

## Remaining limits

Full-match balance, the new bot targeting decisions, extended animation cycles, multiplayer and save/load acceptance for the four additions still need dedicated playtesting before the next expansion release. Restoration currently reconstructs temporary infantry, not the original casualty's exact class. New defensive buildings initially share established weapon baselines. Campaigns comprise 150 designed briefs and three developer previews, not 150 completed missions; Veilborn's earned unlock is not implemented.
