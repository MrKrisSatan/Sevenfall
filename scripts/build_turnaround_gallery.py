"""Build the static directional-art gallery from the artwork roster."""
from pathlib import Path
import html
import json

ROOT = Path(__file__).resolve().parents[1]


def main():
    units = json.loads((ROOT / 'art/unit-turnarounds/roster.json').read_text(encoding='utf-8'))
    current = {r['id']:r for r in json.loads((ROOT/'docs/roster.json').read_text(encoding='utf-8')) if r['kind']=='units'}
    for u in units:
        if u['id'] not in current:
            u['availability']='Future concept — not buildable in alpha.3'
        else:
            u['availability']=current[u['id']]['availability']
            u['description']=current[u['id']]['description']
            u['status']='Legacy directional reference for a current unit; see the field guide for current sprite artwork.'
    units += json.loads((ROOT/'docs/turnarounds-expansion.json').read_text(encoding='utf-8'))
    e = html.escape
    cards = []
    for u in units:
        cards.append(f'''<article class="turn-card" id="{u['id']}" data-faction="{u['faction']}" data-category="{u['category']}">
<button type="button" class="turn-open" aria-label="Inspect {e(u['name'])} directions" data-name="{e(u['name'])}" data-source="{e(u['source'])}"><img src="{u.get('preview', 'assets/turnarounds/'+u['id']+'.webp')}" width="1024" height="512" loading="lazy" alt="{e(u['name'])}: north, northeast, east, southeast, south, southwest, west and northwest views"><span>Inspect eight directions ↗</span></button>
<div class="turn-copy"><p class="card-kicker">{u['faction'].title()} / {e(u['category'])}</p><h2>{e(u['name'])}</h2><p>{e(u['description'])}</p><p class="availability">{e(u['availability'])}</p><p class="turn-status">{e(u['status'])}</p><a href="https://github.com/MrKrisSatan/Sevenfall/blob/main/{u['source']}">Source sheet ↗</a></div>
</article>''')
    template = (ROOT / 'docs/turnarounds.template.html').read_text(encoding='utf-8')
    (ROOT / 'docs/turnarounds.html').write_text(template.replace('<!-- TURNAROUND_CARDS -->', '\n'.join(cards)).replace('{{UNIT_COUNT}}',str(len(units))).replace('{{VIEW_COUNT}}',str(len(units)*8)), encoding='utf-8')
    print(f'Built gallery for {len(units)} units and {len(units)*8} directions.')


if __name__ == '__main__':
    main()
