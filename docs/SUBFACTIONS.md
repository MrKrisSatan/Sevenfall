# Three additional subfaction doctrines

These are additive playable prototypes: the original nine choices remain, and the
lobby/random pool now contains twelve. Each addition has two exclusive units and
one exclusive defense, while retaining its parent's economy and shared army.

## Choir of Desolation — "You were promised purpose."

Funeral angels lead human worshippers who believe suffering earns salvation.
Ash-grey human robes, funeral ivory, tarnished gold and folded angelic wings make
the overseers and their expendable congregation visually distinct.

- **Ashbound Congregant:** 40 credits, 2,400 HP. A cheap human rifle screen with
  weak damage and no Angel Renewal. Within five cells of a living Cantor or a
  powered Processional Shrine, Conviction reduces incoming damage by 15% and
  clears/prevents flesh-wall dread.
- **Cantor of Desolation:** 750 credits, 14,000 HP. An armed angelic overseer and
  mobile hymn source. The formation needs its living presence.
- **Processional Shrine:** 650 credits, 25 power, 50,000 HP. A four-person garrison
  and stationary hymn relay. Empty shrines have no firepower; power loss disables
  the relay. Occupants supply their own weapons.

**The Last Hymn:** an enemy-caused Congregant death within the hymn network gives
that player's nearby Choir angels one Resonance stack: +15%, +30%, then +45%
firepower. Three stacks is the cap; six seconds without another eligible death
clears them. Angels must remain inside an active hymn network to receive the buff.
Self-kills and friendly kills give no stacks. Charges are shared by the player's
hymn network; they are not a spendable currency. Null fields suppress the effect.

Counterplay: kill the overseer, cut shrine power, flank the formation, or withdraw
until Resonance expires. Area Fifty Two's null field also breaks Conviction.

## Area Fifty Two — "Contain. Replicate. Deploy."

A government black-site force fields conventional human scouts and a restrained
hybrid weapons platform. Charcoal armor, unmarked vehicles, hazard braces and
cyan/crimson containment cores distinguish its equipment.

- **Retrieval Team:** 200 credits, 5,000 HP. Rifle-armed reconnaissance infantry,
  eight-cell sight and three-cell cloak detection. Sample-recovery research is
  not implemented in this initial scope.
- **Janus Tank:** 1,500 credits, 55,000 HP. SERAPH gives a slow seven-cell precision
  weapon; ABYSS gives a four-cell infernal weapon. It needs a powered friendly
  Containment Pylon to fire. Damage/critical idle art uses its authored smoking
  chassis variants; movement, firing and destruction have original frames.
- **Containment Pylon:** 900 credits, 60 power, 35,000 HP. Its four-cell null field
  suppresses Angel Renewal, Demon Blood Frenzy, flesh/light/sanctuary fields and
  the new doctrine buffs. Friendly supernatural abilities are affected too;
  conventional gunfire and harvesting continue normally.

**Containment Protocols:** select a powered Pylon and use **Deploy (F)** to toggle
SERAPH/ABYSS. The oldest active owned pylon controls the army. Each change pauses
Janus firing for three seconds, including when control falls back to another
pylon. Losing all powered pylons disables Janus weapons. The deployed pylon shows
an ABYSS label; undeployed is SERAPH. The prototype AI uses default SERAPH.

Counterplay: disrupt power, destroy the controlling pylon, rush before the radar/
experimental investment pays off, or keep conventional forces inside the null
field. There are no random containment failures. Bound Seraphs, Hellhound Platforms,
research samples and a larger experimental roster remain future additions.

## Circle of Contempt — "Even damnation is wasted on you."

An infernal aristocracy directs deliberate executions. Obsidian armor, iron
judicial masks, polished bone and cold violet fire replace the usual swarm imagery.

- **Magistrate of Ash:** 900 credits, 15,000 HP. Its attack condemns an enemy unit
  or building. One mark per player lasts ten seconds; retargeting has an eight-second
  cooldown. Killing or converting the issuing Magistrate cancels the mark.
- **Contemptor:** 1,350 credits, 65,000 HP. A close-range armored execution beast
  with poor anti-infantry damage. It deals 30% extra damage against targets below
  half health, independent of condemnation.
- **Throne of Scorn:** 1,000 credits, 55 power, 45,000 HP. An organic defensive gun
  and command monument. If the attacker and the living issuing Magistrate are both
  within five cells, the condemnation bonus rises from 15% to 30%.

**Pronouncement of Contempt:** purple overlay identifies the condemned target when it is visible.
Only attacks by the marking player's units receive the bonus. A kill credited to
that player grants **Ascendancy**: six seconds of +20% firepower to troops within
six cells of its active Magistrates or Thrones. Null fields suppress condemnation and Ascendancy; physical execution remains.
Execution and condemnation multiply (up to 169% before other existing
weapon modifiers); damage is not an instant execution or loss of control.

Counterplay: withdraw the marked target, sacrifice cheap screens, attack on multiple
fronts and assassinate the Magistrate. Circle units retain the parent's shared
Blood Frenzy where inherited; a full competitive balance pass remains outstanding.

## Validation and reproduction

The new native doctrine diagnostic passes 34 checks covering actual Resonance
firepower, attribution/cap/expiry, Conviction, suppression and resumed Renewal,
protocol switching/firing/power loss, condemnation bonuses, execution, Ascendancy
and Magistrate death. Paid-production acceptance passes 39 checks for the three
new choices: MCV deployment, normal paid structures, an exclusive defense, both
exclusive units, real refinery deliveries and spending. This is component and
production acceptance, not complete-match or multiplayer balance acceptance.

```
python scripts/build.py build
python scripts/run_defense_test.py --scenario doctrine --support-dir artifacts/doctrine
python scripts/run_defense_test.py --scenario subproduction --support-dir artifacts/subproduction --timeout 650
```

Original source sheets and prompts: `art/subfactions/`. Technical packing:
`npm run art:subfactions`. After regenerating older defense or animation sources,
run `python scripts/build_subfactions.py` and then rebuild the site catalogue.
All nine new assets use built-in image generation, with source/export hashes in
the manifest. Animation/facing polish, unique lobby emblems and full-match tuning
remain pending. The game continues toward the skirmish alpha; this change does
not publish or approve a standalone release.
