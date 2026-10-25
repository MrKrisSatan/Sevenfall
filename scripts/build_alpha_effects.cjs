// Original code-native vector effects and UI symbols for the standalone alpha.
const fs=require('node:fs/promises'),path=require('node:path'),sharp=require('sharp');
const root=path.resolve(__dirname,'..');
function chunk(k,v){const d=Buffer.from(k+'\0'+v),b=Buffer.concat([Buffer.from('tEXt'),d]);let c=0xffffffff;for(const x of b){c^=x;for(let i=0;i<8;i++)c=(c>>>1)^((c&1)?0xedb88320:0);}const n=Buffer.alloc(4),s=Buffer.alloc(4);n.writeUInt32BE(d.length);s.writeUInt32BE((c^0xffffffff)>>>0);return Buffer.concat([n,b,s]);}
const svg=(w,h,b)=>Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}">${b}</svg>`);
async function sheet(name,size,frames){const png=await sharp({create:{width:size*frames.length,height:size,channels:4,background:'#00000000'}}).composite(await Promise.all(frames.map(async(b,i)=>({input:await sharp(svg(size,size,b)).png().toBuffer(),left:i*size,top:0})))).png().toBuffer();await fs.writeFile(path.join(root,'mods/sevenfall/art/effects',name+'.png'),Buffer.concat([png.subarray(0,-12),chunk('FrameSize',`${size},${size}`),chunk('FrameAmount',String(frames.length)),png.subarray(-12)]));}
(async()=>{
 await fs.mkdir(path.join(root,'mods/sevenfall/art/effects'),{recursive:true});
 await sheet('blank',24,['']);
 await sheet('projectile',24,['<path d="M5 12 H19" stroke="#ffe3a1" stroke-width="3"/><circle cx="17" cy="12" r="2" fill="#fff7dd"/>']);
 await sheet('indicator',24,['<path d="M12 2 V8 M12 16 V22 M2 12 H8 M16 12 H22" stroke="#dbe7e6" stroke-width="2"/><circle cx="12" cy="12" r="6" fill="none" stroke="#78c7bd"/>']);
 await sheet('blast',48,Array.from({length:8},(_,i)=>`<circle cx="24" cy="24" r="${3+i*2.7}" fill="#f3a657" opacity="${(8-i)/12}"/><circle cx="24" cy="24" r="${2+i*2.5}" fill="none" stroke="#ffe5b1" stroke-width="${3-i*.3}" opacity="${(8-i)/8}"/>`));
 await sheet('smoke',48,Array.from({length:8},(_,i)=>`<circle cx="24" cy="${29-i*1.6}" r="${5+i*1.8}" fill="#78787e" opacity="${(8-i)/15}"/>`));
 await sheet('clock',48,Array.from({length:32},(_,i)=>{const a=(i+1)/32*Math.PI*2,x=24+23*Math.sin(a),y=24-23*Math.cos(a);return i===31?'<circle cx="24" cy="24" r="23" fill="#000" opacity=".55"/>':`<path d="M24 24 L24 1 A23 23 0 ${i>=16?1:0} 1 ${x} ${y} Z" fill="#000" opacity=".55"/>`;}));
 for(const name of ['shroud','fog']) await sheet(name,24,Array.from({length:16},(_,mask)=>{let b='';[[0,0],[12,0],[12,12],[0,12]].forEach(([x,y],i)=>{if(mask&(1<<i))b+=`<rect x="${x}" y="${y}" width="12" height="12" fill="#000" opacity="${name==='fog'?.58:1}"/>`;});return b;}));
 // Match the open-source layout's functional glyph rectangles with original symbols.
 const chrome=await fs.readFile(path.join(root,'.sdk/engine/mods/ra/chrome.yaml'),'utf8');
 let body='',seen=new Set();
 for(const block of chrome.split(/(?=^[^\s#][^\n]*:\r?$)/m)){
  if(!block.includes('Inherits: ^Glyphs'))continue;
  for(const m of block.matchAll(/^\t\t([^:]+): (\d+), (\d+), (\d+), (\d+)/gm)){
   const [name,x,y,w,h]=[m[1],...m.slice(2).map(Number)],key=[x,y,w,h].join(',');if(seen.has(key)||!w||!h)continue;seen.add(key);
   let d='M4 4 H20 V20 H4 Z M8 8 H16 V16 H8 Z';
   if(/attack|enemy/.test(name))d='M12 2 V22 M2 12 H22 M6 6 L18 18 M18 6 L6 18';
   else if(/stop|hold/.test(name))d='M6 6 H18 V18 H6 Z';
   else if(/repair|tools/.test(name))d='M8 3 V9 L13 12 L18 8 V3 L22 9 L20 14 L7 22 L3 18 L14 9';
   else if(/power/.test(name))d='M14 2 L5 14 H11 L9 22 L20 10 H13 Z';
   else if(/cash|cost|sell/.test(name))d='M12 2 V22 M19 6 H8 L5 9 L8 12 H16 L19 15 L16 18 H5';
   else if(/infantry|player|actor/.test(name))d='M9 3 H15 V9 H9 Z M5 22 V14 L9 11 H15 L19 14 V22 M12 14 V22';
   else if(/vehicle|ship/.test(name))d='M3 8 H21 V17 H3 Z M6 17 V21 M18 17 V21 M10 8 V4 H17';
   else if(/building|defense/.test(name))d='M4 22 V8 H10 V3 H16 V8 H21 V22 Z M10 22 V16 H15 V22';
   else if(/aircraft/.test(name))d='M12 2 L15 10 L22 14 V17 L14 14 V20 L17 22 H7 L10 20 V14 L2 17 V14 L9 10 Z';
   else if(/left|prev/.test(name))d='M17 3 L7 12 L17 21';
   else if(/up/.test(name))d='M3 17 L12 7 L21 17';
   else if(/down|marker/.test(name))d='M3 7 L12 17 L21 7';
   else if(/right|next|play|move/.test(name))d='M7 3 L17 12 L7 21';
   else if(/checked/.test(name))d='M3 12 L9 19 L21 4';
   else if(/pause/.test(name))d='M7 3 V21 M17 3 V21';
   else if(/time|reload/.test(name))d='M12 2 L20 6 L22 14 L16 22 L6 20 L2 12 L5 4 Z M12 5 V12 H18';
   body+=`<g transform="translate(${x} ${y}) scale(${w/24} ${h/24})" stroke="${/disabled/.test(name)?'#656c75':'#dde4e9'}" fill="none" stroke-width="2" stroke-linejoin="round"><path d="${d}"/></g>`;
  }
 }
 for(const scale of [1,2,3])await sharp(svg(256,256,body)).resize(256*scale,256*scale).png().toFile(path.join(root,'mods/sevenfall/art/ui',`alpha-glyphs${scale===1?'':`-${scale}x`}.png`));
 await fs.writeFile(path.join(root,'art/ui/alpha-glyphs.svg'),svg(256,256,body));
})();
