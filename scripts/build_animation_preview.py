"""Build a portable offline HTML viewer for the authored game exports."""
import argparse
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / '.tools/animation-preview')
    output = parser.parse_args().output.resolve()
    assets_folder = output / 'assets'
    assets_folder.mkdir(parents=True, exist_ok=True)
    assets = json.loads((ROOT / 'art/animations/manifest.json').read_text(encoding='utf-8'))['assets']
    catalogue = {r['id']: r for r in json.loads((ROOT / 'docs/roster.json').read_text(encoding='utf-8'))}
    records = []
    for asset in assets:
        file = Path(asset['file'])
        shutil.copyfile(ROOT / file, assets_folder / file.name)
        record = {k: asset[k] for k in ('id', 'kind', 'frames', 'frameSize')}
        record.update(name=catalogue[asset['id']]['name'], file='assets/' + file.name)
        if asset['kind'] == 'building':
            intact = asset['id'] + '-intact.png'
            shutil.copyfile(ROOT / 'mods/sevenfall/art' / (asset['id'] + '.png'), assets_folder / intact)
            record['intact'] = 'assets/' + intact
        records.append(record)
    html = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sevenfall animation and damage preview</title><style>
:root{color-scheme:dark;font:16px system-ui;background:#10151b;color:#edf1f5}body{margin:0}header{padding:24px;background:#19232f}h1{margin:0 0 8px;font-size:26px}p{color:#bfcbd7;max-width:85ch}.controls{position:sticky;top:0;z-index:2;display:flex;flex-wrap:wrap;gap:14px;padding:16px;background:#243344}label{display:flex;align-items:center;gap:8px}select,button{font:inherit;color:inherit;background:#17212c;border:1px solid #66809a;border-radius:5px;padding:7px}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(256px,1fr));gap:16px;padding:20px}article{border:1px solid #34465a;border-radius:8px;background:#18222d;text-align:center;overflow:hidden}h2{font-size:16px;padding:0 12px}canvas{width:256px;height:256px;background:radial-gradient(#304237,#1b282b)}small{display:block;color:#bfcbd7;padding:8px}.hidden{display:none}</style>
<header><h1>Sevenfall: animation and damage preview</h1><p>24 implemented faction unit designs and 39 buildings. This viewer reads the actual packed game exports. Movement and attack/work use four timing frames per facing; death cycles finish in a corpse or wreck. Unarmed collectors and MCVs have work-action art, without gaining weapons. This is an initial art pass; visual polish and full gameplay acceptance remain.</p></header>
<div class="controls"><label>Show <select id="kind"><option value="all">All 63 designs</option><option value="unit">Units</option><option value="building">Buildings</option></select></label><label>Faction <select id="faction"><option value="all">All</option><option value="a">Angels</option><option value="h">Humans</option><option value="d">Demons</option></select></label><label>Unit action <select id="action"><option value="0">Move</option><option value="32">Attack / work</option><option value="64">Death</option></select></label><label>Facing <select id="facing"><option value="0">N</option><option value="1">NE</option><option value="2">E</option><option value="3">SE</option><option value="4" selected>S</option><option value="5">SW</option><option value="6">W</option><option value="7">NW</option></select></label><label><input type="checkbox" id="damage">Damaged units</label><label>Buildings <select id="building"><option value="-1">Healthy</option><option value="0">Heavy damage</option><option value="1">Critical damage</option><option value="2">Rubble</option></select></label><button id="pause">Pause</button></div><main id="cards"></main>
<script>const records=RECORDS;
const $=id=>document.getElementById(id);let paused=false,clock=0,last=performance.now();const cards=[];
for(const record of records){const article=document.createElement('article');const title=document.createElement('h2');title.textContent=record.name;article.append(title);const canvas=document.createElement('canvas');canvas.width=canvas.height=256;article.append(canvas);const info=document.createElement('small');info.textContent=record.kind==='unit'?(record.frames===192?'Movement · attack/work · death · damaged variants':'Movement · attack · death'):'Healthy · heavy damage · critical damage · rubble';article.append(info);$('cards').append(article);const image=new Image();image.src=record.file;const intact=new Image();if(record.intact)intact.src=record.intact;cards.push({record,article,canvas,image,intact});}
function filter(){for(const c of cards)c.article.classList.toggle('hidden',($('kind').value!=='all'&&$('kind').value!==c.record.kind)||($('faction').value!=='all'&&$('faction').value!==c.record.id[0]));}
$('kind').onchange=$('faction').onchange=filter;$('pause').onclick=()=>{paused=!paused;$('pause').textContent=paused?'Play':'Pause';};
function draw(now){if(!paused)clock+=now-last;last=now;const tick=Math.floor(clock/100)%4;for(const c of cards){if(c.article.classList.contains('hidden'))continue;const ctx=c.canvas.getContext('2d');ctx.clearRect(0,0,256,256);let index=0,image=c.image;const [w,h]=c.record.frameSize;if(c.record.kind==='unit'){index=Number($('action').value)+Number($('facing').value)*4+tick;if($('damage').checked&&c.record.frames===192)index+=96;}else{index=Number($('building').value);if(index<0){image=c.intact;index=0;}}if(!image.complete||!image.naturalWidth)continue;const cols=Math.floor(image.naturalWidth/w);const scale=Math.min(256/w,256/h);ctx.drawImage(image,(index%cols)*w,Math.floor(index/cols)*h,w,h,(256-w*scale)/2,(256-h*scale)/2,w*scale,h*scale);}requestAnimationFrame(draw);}requestAnimationFrame(draw);
</script></html>'''.replace('RECORDS', json.dumps(records))
    (output / 'preview.html').write_text(html, encoding='utf-8')
    print(output / 'preview.html')


if __name__ == '__main__':
    main()
