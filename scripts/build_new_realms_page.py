"""Publish the development roster separately from alpha.2's shipped field guide."""
from pathlib import Path
from html import escape
import shutil
from build_new_realms import FACTIONS,UNITS
ROOT=Path(__file__).resolve().parents[1]
dest=ROOT/'docs/assets/new-realms';dest.mkdir(exist_ok=True)
cards=[]
for fid,name,realm,description in FACTIONS:
 units=[]
 for u in (u for u in UNITS if u[0]==fid):
  shutil.copy2(ROOT/'art/new-realms'/(u[1]+'.svg'),dest/(u[1]+'.svg'))
  units.append(f'<article class="unit"><img src="assets/new-realms/{u[1]}.svg" alt="{escape(u[2])} prototype silhouette"><div><h3>{escape(u[2])}</h3><p>{escape(u[11])}</p><small>Cost {u[4]} · HP {u[5]} · Speed {u[6]} · Base damage {u[8]} · Range {u[9]} · Reload {u[10]} ticks</small></div></article>')
 cards.append(f'<section class="{fid[0]}"><p class="realm">{realm}</p><h2>{name}</h2><p>{escape(description)}</p>'+''.join(units)+'</section>')
page='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Sevenfall — New Realms</title><style>
body{margin:0;background:#11141b;color:#e8e8ed;font:17px/1.6 system-ui,sans-serif}main{max-width:1100px;margin:auto;padding:36px 24px}a{color:#9de4e9}h1{font-size:clamp(32px,5vw,60px);line-height:1.1}h2{margin:0}h3{margin:0 0 8px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,450px),1fr));gap:24px}section{background:#1b222d;border-top:3px solid #6ce8ed;padding:24px;border-radius:6px}section.f{background:#2b2230;border-color:#d4aad6}.realm{font-size:12px;letter-spacing:2px;text-transform:uppercase;color:#b8c5d5}.unit{display:flex;gap:16px;margin:28px 0}.unit img{width:96px;height:96px;flex-shrink:0;image-rendering:pixelated}small{color:#b7bac3}.note{border-left:3px solid #9cabc1;padding:16px;background:#1d2530;margin:28px 0}p{margin:12px 0}</style></head><body><main><nav><a href="index.html">Sevenfall home</a> · <a href="forces.html">Released field guide</a> · <a href="https://github.com/MrKrisSatan/Sevenfall/blob/main/docs/NEW_REALMS.md">Mechanics and lore</a></nav><h1>The mind awakens.<br>The heavens decay.</h1><p>The Noetic Assembly and the Forsaken Host: two new realms, eight subfactions and sixteen exclusive units.</p><div class="note">Development expansion — not included in the published alpha.2 download. Five parent realms and twenty choices in development. These original vector silhouettes are prototype art; shared buildings still use existing Sevenfall bodies. Damage values are before armor, doctrine and target modifiers. Competitive balance and expanded multiplayer acceptance remain pending.</div><div class="grid">'''+''.join(cards)+'''</div><p>Each realm has its own economy, production prerequisites, engineer, defenses and themed HUD. Harvesters remain safe from contact-triggered Veilglass blasts. No new superweapon or flying unit is claimed in this pass.</p></main></body></html>'''
(ROOT/'docs/new-realms.html').write_text(page,encoding='utf-8')
