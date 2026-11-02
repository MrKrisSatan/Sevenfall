"""Export website direction previews from existing authored unit atlases (Pillow)."""
import json
from pathlib import Path
from PIL import Image
from build_site_catalogue import build_records
ROOT=Path(__file__).resolve().parents[1]
legacy=json.loads((ROOT/'art/unit-turnarounds/roster.json').read_text(encoding='utf-8'))
old={r['id']:r for r in legacy}
painted={}
for group in ['new-realms','realm-completion','additional-realms']:
 for row in json.loads((ROOT/'art'/group/'painted-manifest.json').read_text(encoding='utf-8')):
  if row['kind']=='unit':painted[row['id'].replace('_','-')]=row
for row in json.loads((ROOT/'art/subfactions/manifest.json').read_text(encoding='utf-8'))['assets']:
 if row['frames']==64:painted[row['id'].replace('_','-')]=row
out=[]
for row in build_records():
 if row['kind']!='units' or row['id'] in old:continue
 base=row.get('variant_of',row['id'])
 if base in old:
  preview='assets/turnarounds/'+base+'.webp';source=old[base]['source'];status='Current unit; existing parent directional reference artwork.'
 else:
  art=painted[base];source=art['file'];size=art['frameSize'];sheet=Image.open(ROOT/source).convert('RGBA')
  preview='assets/turnarounds/'+row['id']+'.webp'
  grid=Image.new('RGBA',(1024,512))
  for i in range(8):
   frame=sheet.crop((i*size,0,(i+1)*size,size)).resize((256,256),Image.Resampling.NEAREST)
   grid.paste(frame,((i%4)*256,(i//4)*256))
  grid.save(ROOT/'docs'/preview,quality=94)
  status='Current integrated eight-direction idle sprites, enlarged from the game atlas. Further animation polish remains planned.'
 category='aircraft' if row['role']=='Aircraft' else 'beasts' if row['role']=='Beast' else 'logistics' if row['id'].endswith(('-mcv','-harvester','-gatherer')) else 'vehicles' if any(w in row['role'].lower() for w in ['vehicle','chassis']) else old[base]['category'] if base in old else 'infantry' if painted[base]['frameSize']<=48 else 'vehicles'
 out.append({**row,'category':category,'preview':preview,'source':source,'status':status})
(ROOT/'docs/turnarounds-expansion.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print('Exported',len(out),'additional current unit entries.')
