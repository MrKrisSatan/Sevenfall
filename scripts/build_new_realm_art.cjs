// Original code-native prototype silhouettes, GPL-3.0-or-later.
const fs=require('node:fs/promises'),path=require('node:path'),sharp=require('sharp'),crypto=require('node:crypto');
const root=path.resolve(__dirname,'..');
if(require('node:fs').existsSync(path.join(root,'art/new-realms/painted-manifest.json')))throw Error('Prototype generator retired: use prepare_realm_painted_art.cjs to preserve painted artwork.');
function chunk(k,v){const d=Buffer.from(k+'\0'+v),b=Buffer.concat([Buffer.from('tEXt'),d]);let c=0xffffffff;for(const x of b){c^=x;for(let i=0;i<8;i++)c=(c>>>1)^((c&1)?0xedb88320:0);}const n=Buffer.alloc(4),s=Buffer.alloc(4);n.writeUInt32BE(d.length);s.writeUInt32BE((c^0xffffffff)>>>0);return Buffer.concat([n,b,s]);}
function pose(index,facing,phase,vehicle,machine){
 const angle=facing*Math.PI/4,dx=Math.sin(angle),dy=-Math.cos(angle)*.55;
 const accent=(machine?['#6ce8ed','#e5a767','#85e3b4','#e9d26f']:['#ceb2e4','#e16ca1','#ce6b55','#b4d3db'])[Math.floor(index/2)%4];
 const stride=phase===1?3:phase===2?-3:0,dead=phase>=5,scale=vehicle?1.15:.8;
 let body=machine?`<path d="M-10 -12 L7 -16 L14 -5 L10 9 L-8 13 L-14 1Z" fill="#3c5261" stroke="#9aaebb"/><rect x="-8" y="-16" width="16" height="8" rx="2" fill="#243441"/><path d="M-6 -12 H6" stroke="${accent}" stroke-width="3"/>`:`<path d="M0 -20 Q19 -17 12 0 Q19 12 2 16 Q-18 11 -10 -3 Q-18 -17 0 -20Z" fill="#614455" stroke="#c7afa1"/><path d="M-7 -11 Q0 -6 8 -13 M-8 -4 Q0 2 9 -4 M-7 3 Q0 9 8 3" fill="none" stroke="#cdbca4" stroke-width="2"/><circle cx="2" cy="-14" r="3" fill="${accent}"/>`;
 if(vehicle){body+=machine?`<path d="M-20 -4 V16 M18 -8 V12" stroke="#25313b" stroke-width="8"/><path d="M-20 -4 V16 M18 -8 V12" stroke="#71818a" stroke-width="2"/>`:`<path d="M-9 3 L-23 13 L-25 21 M8 5 L23 12 L26 20 M-5 -4 L-24 0 L-30 9 M7 -5 L23 -1 L30 8" fill="none" stroke="#b6a08f" stroke-width="4"/>`;}
 else body+=`<path d="M-5 10 L${-8+stride} 24 M5 10 L${8-stride} 23" stroke="${machine?'#71818f':'#bca994'}" stroke-width="5"/>`;
 if(!machine)body+=`<path d="M-7 -10 L-24 -27 L-20 -4 L-30 -12 M8 -10 L25 -26 L20 -3 L30 -10" fill="none" stroke="#a78c94" stroke-width="${2+index%3}"/>`;
 const reach=vehicle?24:19;
 body+=`<path d="M2 -4 L${dx*reach} ${dy*reach-4}" stroke="${accent}" stroke-width="${3+index%3}"/><circle cx="${dx*reach}" cy="${dy*reach-4}" r="${phase===3?5:2}" fill="${phase===3?'#fff3c3':accent}"/>`;
 if(index%2===1)body+=`<path d="M-4 -23 L0 -${28+index%4} L4 -23" fill="${accent}"/>`;
 return `<svg xmlns="http://www.w3.org/2000/svg" width="72" height="72"><ellipse cx="36" cy="59" rx="24" ry="8" fill="#000" opacity=".3"/><g transform="translate(36 ${dead?57:36}) scale(${scale} ${dead?.3:scale})" opacity="${phase===7?.45:1}">${body}</g></svg>`;
}
(async()=>{
 const data=JSON.parse(await fs.readFile(path.join(root,'design/NEW_REALMS_ROSTER.json'),'utf8'));
 const dest=path.join(root,'mods/sevenfall/art/new-realms'),src=path.join(root,'art/new-realms');await fs.mkdir(dest,{recursive:true});await fs.mkdir(src,{recursive:true});let seq='',manifest=[];
 for(const [index,u] of data.units.entries()){
  const id=u[1],vehicle=['H_BULWARK','A_AEGIS','D_RAVAGER'].includes(u[3]),machine=id[0]==='i';
  const order=[];for(let f=0;f<8;f++)order.push([f,0]);for(const phases of [[1,2],[3,4],[5,6,7]])for(let f=0;f<8;f++)for(const phase of phases)order.push([f,phase]);
  const frames=await Promise.all(order.map(async([f,p],i)=>({input:await sharp(Buffer.from(pose(index,f,p,vehicle,machine))).png().toBuffer(),left:(i%8)*72,top:Math.floor(i/8)*72})));
  const png=await sharp({create:{width:576,height:576,channels:4,background:'#00000000'}}).composite(frames).png().toBuffer();const packed=Buffer.concat([png.subarray(0,-12),chunk('FrameSize','72,72'),chunk('FrameAmount','64'),png.subarray(-12)]);
  await fs.writeFile(path.join(dest,id+'.png'),packed);await fs.writeFile(path.join(src,id+'.svg'),pose(index,1,0,vehicle,machine));await sharp(frames[1].input).resize(64,48,{fit:'contain'}).png().toFile(path.join(dest,id+'-icon.png'));
  seq+=id+':\n';for(const [name,start,len,stride] of [['idle',0,1,1],['stand',0,1,1],['run',8,2,2],['move',8,2,2],['shoot',24,2,2],['prone-stand',0,1,1],['prone-run',8,2,2],['prone-shoot',24,2,2],['parachute',0,1,1],['damaged-idle',0,1,1],['critical-idle',0,1,1]])seq+=`\t${name}:\n\t\tFilename: sevenfall|art/new-realms/${id}.png\n\t\tStart: ${start}\n\t\tLength: ${len}\n\t\tFacings: -8\n\t\tStride: ${stride}\n\t\tTick: 120\n`;
  seq+=`\ticon:\n\t\tFilename: sevenfall|art/new-realms/${id}-icon.png\n${id}_death:\n\tdie:\n\t\tFilename: sevenfall|art/new-realms/${id}.png\n\t\tStart: 40\n\t\tLength: 3\n\t\tFacings: -8\n\t\tTick: 120\n\tcorpse:\n\t\tFilename: sevenfall|art/new-realms/${id}.png\n\t\tStart: 42\n\t\tLength: 1\n\t\tFacings: -8\n\t\tStride: 3\n`;
  manifest.push({id,sha256:crypto.createHash('sha256').update(packed).digest('hex'),frames:64,frameSize:72,style:'Original vector prototype; not final painted art'});
 }
 await fs.writeFile(path.join(root,'mods/sevenfall/sequences/new-realms.yaml'),seq);await fs.writeFile(path.join(src,'manifest.json'),JSON.stringify(manifest,null,2)+'\n');
})().catch(e=>{console.error(e);process.exitCode=1;});
