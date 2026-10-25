"""Build the static, no-JavaScript-required website roster from Sevenfall rules."""
from pathlib import Path
import re, json, html

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / 'mods/sevenfall'
FACTIONS = {'a': ('angels','Angels'), 'h': ('humans','Humans'), 'd': ('demons','Demons')}
SUBFACTIONS = {'a_seraph':'Seraphic Synod','a_warden':'Order of the Gate','a_exile':'The Unshackled',
 'h_bastion':'Bastion Directorate','h_union':'Free Earth Union','h_covenant':'Ashen Covenant',
 'd_legion':'Iron Legions','d_brood':'Blood Brood','d_court':'Court of Whispers'}
ROLES = {'advpower':'Advanced power','service':'Vehicle repair','radar':'Radar','naval':'Naval production',
 'helipad':'Vertical aircraft','airfield':'Fixed-wing aircraft','kennel':'Beast training','tech':'Technology',
 'chapel':'Infantry production','barracks':'Infantry production','pit':'Infantry production',
 'armory':'Vehicle production','motorpool':'Vehicle production','forge':'Vehicle production',
 'spire':'Power','generator':'Power','heart':'Power','veilworks':'Veilglass refinery'}

def build_records():
    strings = dict(re.findall(r'^(sf-[\w-]+) = (.*)$', (MOD/'fluent/sevenfall.ftl').read_text(encoding='utf-8'), re.M))
    records=[]
    for f,(faction,label) in FACTIONS.items():
        records.append(dict(id=f+'-yard',actor='FACT',faction=faction,kind='buildings',name=label[:-1]+' Construction Yard',
          role='Base construction',description='The heart of the '+label[:-1]+' base. Deploy an MCV to establish this yard and construct faction buildings.',
          source='art/source/'+f+'-yard.png',status='Original game art',availability='Shared by all three subfactions',subfaction='shared'))
        records.append(dict(id=f+'-mcv',actor='MCV',faction=faction,kind='units',name=label[:-1]+' MCV',role='Mobile construction',
          description='Deploys into a faction Construction Yard to establish a base. Available as a starting unit; replacement MCV production is not enabled yet.',
          source='art/source/'+f+'-mcv.png',sprite=True,status='Original game art',availability='Shared by all three subfactions',subfaction='shared'))
    for filename,kind in [('20-structures.yaml','buildings'),('25-support-structures.yaml','buildings'),('30-units.yaml','units')]:
        text=(MOD/'rules'/filename).read_text(encoding='utf-8')
        for match in re.finditer(r'^([A-Z][A-Z_]+):\n(.*?)(?=^[A-Z][A-Z_]+:\n|\Z)',text,re.M|re.S):
            actor,body=match.groups(); key=actor.lower().replace('_','-');f=key[0]
            title=strings['sf-'+key+'-name'];description=strings['sf-'+key+'-description']
            suffix=key[2:]; sub=re.search(r'~sf\.([ahd]_\w+)',body)
            subid=sub[1] if sub else 'shared'
            collector=suffix in ['gatherer','harvester','devourer']
            concept=kind=='units' and not collector
            source=('art/source/website/'+key+'.png') if concept else ('art/source/'+f+'-harvester.png') if collector else ('art/source/'+key+'.png')
            role=ROLES.get(suffix) if kind=='buildings' else 'Veilglass collector' if collector else 'Combat vehicle' if '\t\tQueue: Vehicle' in body else 'Infantry'
            if key == 'd-ravager': role='Shock beast'
            if key == 'd-hellreaver': role='Siege beast'
            records.append(dict(id=key,actor=actor,faction=FACTIONS[f][0],kind=kind,name=title,role=role,
              description=description,source=source,sprite=collector,status='Concept illustration' if concept else 'Original game art',
              availability=SUBFACTIONS[subid]+' exclusive' if sub else 'Shared by all three subfactions',subfaction=subid))
    for defense in json.loads((ROOT/'art/defenses/catalogue.json').read_text(encoding='utf-8')):
        actor=defense['id']; key=actor.replace('_','-')
        records.append(dict(id=key,actor=actor.upper(),faction=FACTIONS[actor[0]][0],kind='buildings',
          name=defense['name'],role='Defense / '+defense['role'],description=defense['description'],
          source=defense['source'],sprite=True,status='Original game art',
          availability='Shared by all three subfactions',subfaction='shared'))
    records.sort(key=lambda r:(list(v[0] for v in FACTIONS.values()).index(r['faction']),r['kind']=='units',r['actor'] not in ['FACT','MCV'],r['name']))
    return records

def render_card(r):
    e=html.escape
    note='Original animated game sprite integrated; concept art shown.' if r['status']=='Concept illustration' else 'Current original artwork.'
    return f'''<article class="roster-card {r['faction']}" id="{r['id']}" data-faction="{r['faction']}" data-kind="{r['kind']}" data-subfaction="{r['subfaction']}">
  <button class="art-button" type="button" aria-label="Enlarge {e(r['name'])} artwork" data-art="assets/roster/full/{r['id']}.webp"><img src="assets/roster/{r['id']}.webp" width="512" height="384" loading="lazy" decoding="async" alt="{e(r['name'])} — {e(r['status'].lower())}"></button>
  <div class="roster-card-copy"><p class="card-kicker">{r['faction'].title()} / {e(r['role'])}</p><h3>{e(r['name'])}</h3><p>{e(r['description'])}</p><p class="availability">{e(r['availability'])}</p><p class="art-status"><span>{r['status']}</span> {note}</p></div>
</article>'''

def main():
    records=build_records()
    (ROOT/'docs/roster.json').write_text(json.dumps(records,indent=2)+'\n',encoding='utf-8')
    cards='\n'.join(map(render_card,records))
    template=(ROOT/'docs/catalogue.template.html').read_text(encoding='utf-8')
    (ROOT/'docs/forces.html').write_text(template.replace('<!-- ROSTER_CARDS -->',cards),encoding='utf-8')
    print(f'Built {len(records)} roster cards: {sum(r["kind"]=="buildings" for r in records)} buildings and {sum(r["kind"]=="units" for r in records)} units.')

if __name__=='__main__':main()
