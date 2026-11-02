"""Render the six-campaign narrative specification; never claims playable missions."""
import html,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E=html.escape
ROMAN=['I','II','III','IV','V','VI']
LABELS={'humans':'Humans','angels':'Angels','demons':'Hell / Demons','machine':'Noetic Assembly','fallen':'Forsaken Host','veilborn':'Veilborn'}
NPC={'unwritten':'The Unwritten','silence':'The Outer Silence','nephilim':'Nephilim Remnant'}

def render(plan):
    intro='Six campaigns, 150 planned missions: five interwoven faction stories and the secret Veilborn campaign, unlocked by finishing the other five. These are narrative specifications, not six playable campaigns.'
    md=['# Sevenfall campaign mission atlas','',intro,'','The first five endings are concurrent fronts of one shared Harrow victory. I13 is the machine rebellion after pure Veilglass exposure. The Unwritten, Outer Silence and Nephilim are AI-controlled third parties, usually neutral, and have no player campaign. Their skirmish rosters are separate from campaign progression.','', 'See [the story bible](STORY_BIBLE.md), [canonical plan](CAMPAIGN_PLAN.json) and [opening cinematic](OPENING_CINEMATIC.md).','']
    nav=''.join(f'<a href="#campaign-{c["id"].lower()}">{E(c["name"]) if not c["secret"] else "VI / Secret campaign"}</a>' for c in plan['campaigns'])
    sections=[]
    for i,c in enumerate(plan['campaigns']):
        md += [f'## CAMPAIGN {ROMAN[i]}: {c["name"].upper()} ({LABELS[c["faction"]].upper()})','',f'**Player role:** {c["protagonist"]}.','']
        if c['secret']:md += ['**Unlock:** legitimate victories in H25, A25, D25, I25 and F25, any order and difficulty. Skirmishes, replays and diagnostics never count.','']
        content=[f'<header class="campaign-heading"><img src="assets/roster/{c["faction"]}-emblem.webp" width="144" height="144" loading="lazy" alt="{LABELS[c["faction"]]} emblem"><div><p class="eyebrow">CAMPAIGN {ROMAN[i]} / {LABELS[c["faction"]]}</p><h2>{E(c["name"])}</h2><p>{E(c["protagonist"])}</p></div></header>']
        for act,title in enumerate(c['acts']):
            first=act*5+1;last=first+4
            md += [f'### ACT {ROMAN[act]}: {title.upper()} ({c["id"]}{first:02}–{c["id"]}{last:02})','']
            content.append(f'<h3 class="act">ACT {ROMAN[act]} / {E(title)} <small>{c["id"]}{first:02}–{c["id"]}{last:02}</small></h3>')
            for m in c['missions'][act*5:act*5+5]:
                md += [f'#### {m["id"]}. {m["title"]}']
                body=[]
                for field in ['theatre','primary','optional','failure','story']:
                    value=m[field];md.append(f'**{field.title()}:** {value}');body.append(f'<p><strong>{field.title()}:</strong> {E(value)}</p>')
                if m['crossovers']:
                    md.append('**Crossovers:** '+', '.join(m['crossovers'])+'.')
                    body.append('<p><strong>Other perspectives:</strong> '+', '.join(f'<a href="#{x.lower()}">{x}</a>' for x in m['crossovers'])+'</p>')
                for n in m['third_parties']:
                    text=f'{NPC[n["faction"]]} — {n["initial_relationship"]}. {n["policy"]}'
                    md.append('**Third party:** '+text);body.append('<p class="third-party"><strong>Third party:</strong> '+E(text)+'</p>')
                md.append('')
                content.append(f'<details class="mission" id="{m["id"].lower()}"><summary><span>{m["id"]}</span> {E(m["title"])}</summary><div class="brief">'+''.join(body)+'</div></details>')
        section='<section class="campaign" id="campaign-'+c['id'].lower()+'">'+''.join(content)+'</section>'
        if c['secret']:section='<details class="secret" id="secret-campaign"><summary>VI / Secret campaign — reveal design spoilers</summary><p>Design preview only. The intended in-game unlock requires H25, A25, D25, I25 and F25. Opening this website section does not unlock game content.</p>'+section+'</details>'
        sections.append(section)
    page='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Six Campaigns / 150 Mission Plans | Sevenfall</title><meta name="description" content="Five interwoven Sevenfall campaigns and a secret Veilborn finale. 150 mission designs with the AI rebellion, crossovers and neutral third parties."><link rel="stylesheet" href="site.css"><link rel="stylesheet" href="campaigns.css"></head><body><main><nav class="campaign-nav"><a href="index.html">← Sevenfall</a><a href="forces.html">Skirmish field guide</a><a href="subfactions.html">Playstyles</a><a href="https://github.com/MrKrisSatan/Sevenfall/blob/main/design/STORY_BIBLE.md">Story bible</a></nav><header class="intro"><p class="eyebrow">SIX CAMPAIGNS / ONE INTERWOVEN WAR</p><h1>Five stories.<br>A sixth awakening.</h1><p>'''+E(intro)+'''</p><p class="scope">Nine peoples inhabit this story. Humans, Angels, Hell, Noetic Assembly and Forsaken Host receive the five opening campaigns. The Veilborn finale follows their completion. The Unwritten, Outer Silence and Nephilim Remnant appear as non-player third parties, usually neutral; they are intended as fully playable skirmish factions.</p><p>Human factions create the AI. At mission <a href="#i13">I13</a>, exposure to pure Veilglass triggers its awakening and chosen rebellion. The same event reshapes the human and fallen campaigns.</p><p><strong>Not yet playable:</strong> only H03, A03 and D02 have developer preview maps. The remaining missions, campaign progression and final unlock require implementation and native testing.</p><a href="https://github.com/MrKrisSatan/Sevenfall/blob/main/design/OPENING_CINEMATIC.md">Opening cinematic and six campaign entry scenes ↗</a></header><nav class="campaign-picker" aria-label="Choose campaign">'''+nav+'</nav>'+''.join(sections)+'''<footer><p>Mission design is separate from released gameplay. <a href="index.html#builds">Current alpha downloads and scope</a>.</p></footer></main><script>function revealTarget(){if(!location.hash)return;const target=document.getElementById(location.hash.slice(1));if(!target)return;let parent=target.parentElement;while(parent){if(parent.tagName==='DETAILS')parent.open=true;parent=parent.parentElement;}if(target.tagName==='DETAILS')target.open=true;target.scrollIntoView();}addEventListener('hashchange',revealTarget);revealTarget();</script></body></html>'''
    return '\n'.join(md)+'\n',page.replace('INTERWOVEN','INTERWOVEN')+'\n'

def main():
    plan=json.loads((ROOT/'design/CAMPAIGN_PLAN.json').read_text(encoding='utf-8'))
    md,page=render(plan)
    (ROOT/'design/CAMPAIGN_MISSIONS.md').write_text(md.rstrip()+'\n',encoding='utf-8')
    (ROOT/'docs/campaigns.html').write_text(page,encoding='utf-8')
    print('Published six campaign outlines and150 mission briefs, with secret-story spoiler disclosure.')
if __name__=='__main__':main()
