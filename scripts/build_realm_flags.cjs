// Extend Sevenfall's existing code-native UI emblem system; preserve original marks.
const fs=require('node:fs/promises'),path=require('node:path'),sharp=require('sharp');
const root=path.resolve(__dirname,'..');
const marks={
 i_echo:'M-10 0 Q0 -10 10 0 Q0 10 -10 0 M0 -4 V4',
 i_iron:'M-8 -7 H8 V6 L0 10 L-8 6 Z M-4 -3 H4 V4 H-4 Z',
 i_grid:'M-8 -7 H8 V7 H-8 Z M-8 0 H8 M0 -7 V7 M-11 -10 H-5 V-4 H-11 Z M5 4 H11 V10 H5 Z',
 i_paradox:'M-10 -6 H2 L-4 0 L2 6 H10 M-10 6 H-2 L4 0 L-2 -6 H10',
 f_thrones:'M-10 -6 L-5 2 L0 -8 L5 2 L10 -6 L7 7 H-7 Z M-4 10 H4',
 f_choir:'M-9 -5 V6 M-4 -9 V9 M1 -6 V6 M6 -10 V9 M10 -5 V5 M-11 1 H11',
 f_scars:'M-10 8 L-2 -9 M-4 10 L4 -10 M3 9 L10 -8 M-10 -2 L10 2',
 f_wings:'M-1 5 L-4 -8 L-11 -4 L-7 -2 L-11 3 L-5 1 L-7 9 Z M1 5 L4 -8 L11 -4 L7 -2 L11 3 L5 1 L7 9 Z'
};
(async()=>{
 for(const [id,d] of Object.entries(marks))await fs.writeFile(path.join(root,`docs/assets/new-realms/${id}.svg`),`<svg xmlns="http://www.w3.org/2000/svg" viewBox="-16 -16 32 32"><path d="${d}" fill="none" stroke="${id[0]==='i'?'#70f6ee':'#d6b3d3'}" stroke-width="1.5"/></svg>`);
 let content='';Object.entries(marks).forEach(([id,d],i)=>{content+=`<g transform="translate(15 ${i*15+7.5}) scale(.55)" fill="none" stroke="${id[0]==='i'?'#70f6ee':'#d6b3d3'}" stroke-width="2"><path d="${d}"/></g>`;});
 const svg=`<svg xmlns="http://www.w3.org/2000/svg" width="30" height="120" viewBox="0 0 30 120">${content}</svg>`;
 await fs.writeFile(path.join(root,'art/ui/new-realm-flags.svg'),svg);
 for(const scale of [1,2,3]){
  const suffix=scale===1?'':`-${scale}x`;
  const old=await fs.readFile(path.join(root,`mods/sevenfall/art/factions${suffix}.png`));
  await sharp({create:{width:2**Math.ceil(Math.log2(60*scale)),height:2**Math.ceil(Math.log2(120*scale)),channels:4,background:'#00000000'}}).composite([{input:old,left:0,top:0},{input:await sharp(Buffer.from(svg)).resize(30*scale,120*scale).png().toBuffer(),left:30*scale,top:0}]).png().toFile(path.join(root,`mods/sevenfall/art/ui/all-realm-flags${suffix}.png`));
 }
 const file=path.join(root,'mods/sevenfall/chrome.yaml');let yaml=await fs.readFile(file,'utf8');
 yaml=yaml.replaceAll('\r\n','\n').replaceAll('art/factions','art/ui/all-realm-flags');
 Object.entries(marks).forEach(([id],i)=>{yaml=yaml.replace(new RegExp(`\\t\\t${id}:.*\\r?\\n`,'g'),'');});
 yaml=yaml.replace('\tRegions:\n','\tRegions:\n'+Object.keys(marks).map((id,i)=>`\t\t${id}: 30, ${i*15}, 30, 15\n`).join(''));
 await fs.writeFile(file,yaml);
})();
