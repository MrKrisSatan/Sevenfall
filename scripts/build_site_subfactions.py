"""Publish accessible, deep-linkable playstyle profiles from the current roster."""
from pathlib import Path
import html
import json
from build_faction_identities import FACTIONS, POWER_DESCRIPTIONS
from build_new_realms import FACTIONS as NEW_FACTIONS
from build_site_catalogue import build_records

ROOT = Path(__file__).resolve().parents[1]
E = html.escape
PARENTS = {'a': ('angels', 'Angels'), 'h': ('humans', 'Humans'), 'd': ('demons', 'Demons'), 'i': ('machine', 'Noetic Assembly'), 'f': ('fallen', 'Forsaken Host')}
# Tactical advice inferred from the implemented doctrines, not additional abilities.
TACTICS = {
'a_seraph': ('Prepared precision', 'Screen your Luminaries, settle into a firing position and let focus build before the enemy arrives.', 'Flanking and forced movement interrupt focus. Expensive elites cannot replace a broad screen.'),
'a_warden': ('Shield formations', 'Keep your army within four cells of a Gatekeeper or Wardbearer. Advance as a protected group and use the Unbroken Gate to hold a contested area.', 'Relays do not stack. Separate or eliminate the shield carriers; the protected formation moves more slowly.'),
'a_exile': ('Wounded skirmishers', 'Use Penitents and Outriders to pressure a flank. Retreat injured survivors and use their speed to choose the next engagement.', 'The bonus requires low health. Burst damage can finish units before they escape; avoid sustained frontal trades.'),
'a_desolation': ('Martyrdom formations', 'Screen Cantors with inexpensive Congregants and fight inside the hymn network. Enemy-caused worshipper losses create a brief window for empowered angels.', 'Destroy or isolate Cantors and shrines. Resonance is capped and expires, so separated fights waste its timing.'),
'h_bastion': ('Entrenched artillery', 'Prepare firing lines before contact. Protect Siege Cannons with infantry and use Sappers to breach buildings once the approach is safe.', 'Moving resets entrenchment. Flanks and attacks on multiple fronts make a static line reposition.'),
'h_union': ('Mobile logistics', 'Escort Harvesters and Pathfinders, then move your army along their supply corridors. Rangers help scout where to strike next.', 'Destroying or isolating logistics units removes the local advantage. Protect your economy while raiding.'),
'h_covenant': ('Sustained infantry', 'Keep Templars and Confessors close to infantry. Rotate wounded troops through their protective healing aura and time Ashes to Ashes around a decisive fight.', 'Focus fire can overwhelm healing. Eliminate the support units or split the infantry formation.'),
'h_area52': ('Containment warfare', 'Scout with Retrieval Teams and choose Janus protocols for the range of the fight. Position powered pylons where their null fields disrupt enemy supernatural bonuses.', 'Pylons need power; protocol switches temporarily stop firing. Null fields also suppress friendly supernatural effects.'),
'd_legion': ('Armored siege', 'Advance Hellreavers with Taskmasters and a screen. Keep the formation together while breaking a defended position.', 'The protective formation sacrifices speed. Kite it or threaten a second front outside its coverage.'),
'd_brood': ('Kill-driven momentum', 'Use Skitters to pressure and Goremaws to finish enemy troops. Chain successful fights while the killer’s healing and attack bonuses are active.', 'Buildings and friendly kills provide no feeding. Deny easy troop kills and kite melee predators.'),
'd_court': ('Debuff control', 'Tag priority enemies with Hexers and Silencers, then let the rest of the army exploit slowed movement and weakened return fire.', 'Curse specialists are fragile. Break line of fire, flank them and wait out the short curse before re-engaging.'),
'd_contempt': ('Priority executions', 'Condemn one important target with a Magistrate, focus it down and send Contemptors after wounded heavy enemies. Use the resulting Ascendancy window.', 'Kill the Magistrate to cancel its mark. Cheap screens and healthy targets frustrate execution beasts.'),
'i_echo': ('Reconnaissance and precision', 'Scout with Mnemonic Ghosts, screen Needle Chassis and prepare stationary firing positions before committing.', 'Force movement, flank and exploit the Needle’s long reload. Precision units are fragile under focused fire.'),
'i_iron': ('Armored attrition', 'Use Endurers to support Crucible Engines in a steady push. Spend the armor advantage on sustained exchanges you can afford.', 'Slow movement and costly replacements invite flanking and resource denial. Avoid chasing fast raiders.'),
'i_grid': ('Network formations', 'Escort Relay Walkers with Threadkeepers and shared combat units. Keep your fighting force inside the four-cell network.', 'Destroy or separate the relays. Multiple relays do not stack their bonus, and isolated units lose the formation advantage.'),
'i_paradox': ('Adaptive harassment', 'Pressure exposed targets with Savants and Gambit Rovers. Pull damaged survivors out, reposition and strike somewhere else.', 'The bonus only activates below half health. Burst damage and interception punish repeated escape attempts.'),
'f_thrones': ('Entrenched aristocracy', 'Establish a position with Regents and Walking Reliquaries, then let the stationary protection build before trading fire.', 'Force repositioning and exploit the slower attack cadence. Holding armor comes at the cost of damage output.'),
'f_choir': ('Risky procession', 'Keep Canticles and the wider army near a Lamentor. Commit together while the hymn amplifies their damage.', 'The hymn also increases incoming damage. Kill the relay or punish tightly packed formations with area attacks.'),
'f_scars': ('Wounded aggression', 'Screen the advance of Vow Flayers and Carrion Martyrs. Their wounded-state bonus can turn a close-range fight if they survive the approach.', 'Kite and screen melee attackers. Finish injured units quickly instead of leaving empowered survivors.'),
'f_wings': ('Dispersed hunters', 'Split Pinions and Harrow Stalkers into separate attack lanes. Maintain spacing to preserve their isolation bonus and attack exposed targets.', 'Concentrate force against isolated hunters and block escape routes. Nearby friendly combat units switch off the isolation bonus.')}
SHARED = {'a': 'Witness of Salt', 'h': 'Nuclear', 'd': 'Hellrift', 'i': 'Extinction', 'f': 'Sepulchral Rapture'}

def render():
    records = build_records()
    # The original identity guide records exact implemented mechanics.
    mechanics = {line.split('|')[1].strip(): line.split('|')[2].strip() for line in (ROOT/'docs/FACTION_IDENTITIES.md').read_text(encoding='utf-8').splitlines() if line.startswith('| ') and len(line.split('|')) == 6}
    profiles = [(f[0], f[1], mechanics[f[1]], (f[3], POWER_DESCRIPTIONS[f[2]])) for f in FACTIONS]
    profiles += [(f[0], f[1], f[3], None) for f in NEW_FACTIONS]
    nav = ''.join(f'<a href="#{sid}">{E(name)}</a>' for sid,name,_,_ in profiles)
    cards = []
    for sid,name,mechanic,power in profiles:
        family,label = PARENTS[sid[0]]
        style,plan,counter = TACTICS[sid]
        units = [r for r in records if r['subfaction']==sid and r['kind']=='units']
        assert len(units)==2, sid
        unit_html = ''
        for unit in units:
            image = unit.get('image', 'assets/roster/'+unit.get('art_id',unit['id'])+'.webp')
            unit_html += f'<article class="profile-unit"><img src="{E(image)}" width="112" height="112" loading="lazy" alt="{E(unit["name"])}"><div><h4>{E(unit["name"])}</h4><p>{E(unit["description"])}</p><small>{E(unit["status"])}</small></div></article>'
        power_html = f'<h3>Exclusive superweapon: {E(power[0])}</h3><p>{E(power[1])}</p>' if power else '<p>This subfaction uses its realm’s shared superweapon; it has no separate exclusive superweapon in this alpha.</p>'
        cards.append(f'''<section class="subfaction-profile {family}" id="{sid}" aria-labelledby="{sid}-title"><p class="eyebrow">{E(label)} / {E(style)}</p><h2 id="{sid}-title">{E(name)}</h2><p class="doctrine">{E(mechanic)}</p><div class="profile-tactics"><div><h3>How to play</h3><p>{E(plan)}</p></div><div><h3>Weaknesses and counterplay</h3><p>{E(counter)}</p></div></div><h3>Exclusive units</h3><div class="profile-units">{unit_html}</div>{power_html}<p><strong>Shared realm power:</strong> {E(SHARED[sid[0]])}. Powers charge automatically in Defences while their supplying installation is present and powered. Losing the last supplying building removes the power; rebuilding starts a fresh charge.</p><div class="profile-links"><a href="forces.html?faction={family}&amp;subfaction={sid}">Explore this subfaction’s units and buildings ↗</a><a href="#choose">Choose another subfaction ↑</a></div></section>''')
    return '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Sevenfall — Subfaction playstyles</title><meta name="description" content="Choose between twenty Sevenfall subfactions: doctrines, tactical advice, counters, exclusive units and superweapons."><link rel="stylesheet" href="site.css"><link rel="stylesheet" href="subfactions.css"></head><body><main class="profile-main"><nav aria-label="Main navigation"><a href="index.html#factions">← Original five factions</a><a href="forces.html">Illustrated field guide</a><a href="additional-realms.html">Four independent factions</a><a href="arsenal.html">Shared arsenal</a></nav><header id="choose"><p class="eyebrow">TWENTY DOCTRINES / FIVE REALMS</p><h1>Choose how<br>you wage war.</h1><p>Every subfaction keeps its realm’s shared base and army, adds two exclusive units and changes the way you fight. These profiles describe implemented alpha mechanics; tactical advice is a starting point for playtesting, not a claim of competitive balance.</p></header><nav class="profile-picker" aria-label="Choose a subfaction">'''+nav+'</nav>'+''.join(cards)+'</main></body></html>\n'

def main():
    (ROOT/'docs/subfactions.html').write_text(render(),encoding='utf-8')
    path=ROOT/'docs/index.html'
    text=path.read_text(encoding='utf-8')
    for sid,name in [(f[0],f[1]) for f in FACTIONS+NEW_FACTIONS]:
        text=text.replace(f'<li>{name}</li>',f'<li><a class="subfaction-link" href="subfactions.html#{sid}">{name}<span aria-hidden="true"> ↗</span></a></li>')
    path.write_text(text,encoding='utf-8')
    print('Built twenty linked subfaction playstyle profiles.')

if __name__=='__main__':main()
