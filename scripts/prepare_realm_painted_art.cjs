// Technical extraction, resizing, alignment and packing only. No painted content is synthesized.
const fs=require('node:fs/promises'),path=require('node:path'),sharp=require('sharp'),crypto=require('node:crypto');
const root=path.resolve(__dirname,'..'),sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const canvas=(w,h)=>sharp({create:{width:w,height:h,channels:4,background:'#00000000'}});
function chunk(k,v){const d=Buffer.from(k+'\0'+v),b=Buffer.concat([Buffer.from('tEXt'),d]);let c=0xffffffff;for(const x of b){c^=x;for(let i=0;i<8;i++)c=(c>>>1)^((c&1)?0xedb88320:0);}const h=Buffer.alloc(4),t=Buffer.alloc(4);h.writeUInt32BE(d.length);t.writeUInt32BE((c^0xffffffff)>>>0);return Buffer.concat([h,b,t]);}
async function bounds(b){const {data,info}=await sharp(b).ensureAlpha().raw().toBuffer({resolveWithObject:true});let l=info.width,t=info.height,r=-1,z=-1,transparent=0;for(let y=0;y<info.height;y++)for(let x=0;x<info.width;x++){const a=data[(y*info.width+x)*4+3];if(a<16)transparent++;if(a<48)continue;l=Math.min(l,x);r=Math.max(r,x);t=Math.min(t,y);z=Math.max(z,y);}if(r<l||transparent<info.width*info.height*.06)throw Error('Empty/opaque source cell');return{left:l,top:t,width:r-l+1,height:z-t+1};}
async function main(){
 const plan=JSON.parse(await fs.readFile(path.join(root,'art/new-realms/painted-prompts.json'),'utf8'));
 const roster=JSON.parse(await fs.readFile(path.join(root,'design/NEW_REALMS_ROSTER.json'),'utf8'));
 const vehicles=new Set(roster.units.filter(u=>['H_BULWARK','A_AEGIS','D_RAVAGER'].includes(u[3])).map(u=>u[1]));
 for(const id of ['i_mcv','f_mcv','i_harvester','f_gatherer','i_bulwark','f_aegis'])vehicles.add(id);
 const dest=path.join(root,'mods/sevenfall/art/new-realms'),web=path.join(root,'docs/assets/new-realms');await fs.mkdir(dest,{recursive:true});await fs.mkdir(web,{recursive:true});
 const manifest=[],previews=[];let seq='';
 for(const p of plan){
  const source=await fs.readFile(path.join(root,p.source));const m=await sharp(source).metadata();if(!m.hasAlpha)throw Error(p.id+': missing alpha');
  const building=p.kind==='building',cols=building?3:8,rows=building?2:4,cw=m.width/cols,ch=m.height/rows;
  const cells=[],boxes=[];
  for(let i=0;i<cols*rows;i++){const b=await sharp(source).extract({left:Math.floor(i%cols*cw),top:Math.floor(Math.floor(i/cols)*ch),width:Math.floor((i%cols+1)*cw)-Math.floor(i%cols*cw),height:Math.floor((Math.floor(i/cols)+1)*ch)-Math.floor(Math.floor(i/cols)*ch)}).png().toBuffer();cells.push(b);try{boxes.push(await bounds(b));}catch(e){throw Error(p.id+' cell '+i+': '+e.message);}}
  const size=building?128:p.id.endsWith('_mcv')?96:vehicles.has(p.id)?80:48;
  const scale=(size-8)/Math.max(...boxes.map(b=>Math.max(b.width,b.height)));const frames=[];
  for(let i=0;i<cells.length;i++){const b=boxes[i],w=Math.max(1,Math.round(b.width*scale)),h=Math.max(1,Math.round(b.height*scale));frames.push(await canvas(size,size).composite([{input:await sharp(cells[i]).extract(b).resize(w,h).png().toBuffer(),left:Math.floor((size-w)/2),top:size-h-3}]).png().toBuffer());}
  // Two authored locomotion poses (idle/stride), attack/rest, then a held authored wreck.
  // Three repeated wreck frames preserve the prior sequence layout; they are NOT three death poses.
  const order=building?[0,1,2,3,4,5]:[...Array(8).keys(),...Array.from({length:8},(_,f)=>[f,8+f]).flat(),...Array.from({length:8},(_,f)=>[16+f,f]).flat(),...Array.from({length:8},(_,f)=>[24+f,24+f,24+f]).flat()];
  const across=building?6:8,png=await canvas(across*size,Math.ceil(order.length/across)*size).composite(order.map((n,i)=>({input:frames[n],left:i%across*size,top:Math.floor(i/across)*size}))).png().toBuffer();
  const packed=Buffer.concat([png.subarray(0,-12),chunk('FrameSize',size+','+size),chunk('FrameAmount',String(order.length)),png.subarray(-12)]);
  await fs.writeFile(path.join(dest,p.id+'.png'),packed);
  const portrait=frames[building?0:4],icon=await sharp(portrait).trim().resize(50,38,{fit:'inside'}).png().toBuffer(),im=await sharp(icon).metadata();await canvas(56,42).composite([{input:icon,left:Math.floor((56-im.width)/2),top:Math.floor((42-im.height)/2)}]).png().toFile(path.join(dest,p.id+'-icon.png'));
  const pi=building?0:4;await sharp(cells[pi]).extract(boxes[pi]).resize(256,256,{fit:'contain',background:'#00000000'}).webp({quality:90}).toFile(path.join(web,p.id+'.webp'));
  previews.push(await sharp(portrait).resize(128,128).png().toBuffer());
  seq+=p.id+':\n';
  if(building){
   for(const [n,start,len] of [['idle',0,1],['damaged-idle',1,1],['critical-idle',2,1],['make',3,2],['build',5,1],['damaged-build',1,1],['active',5,1],['damaged-active',1,1],['shoot',5,1],['place',0,1],['dead',2,1]])seq+=`\t${n}:\n\t\tFilename: sevenfall|art/new-realms/${p.id}.png\n\t\tStart: ${start}\n\t\tLength: ${len}\n\t\tTick: 160\n\t\tOffset: 0,-24\n`;
  }else{
   for(const [n,start,len,stride] of [['idle',0,1,1],['stand',0,1,1],['run',8,2,2],['move',8,2,2],['shoot',24,2,2],['prone-stand',0,1,1],['prone-run',8,2,2],['prone-shoot',24,2,2],['parachute',0,1,1],['damaged-idle',0,1,1],['critical-idle',0,1,1],['harvest',24,2,2],['dock',24,2,2],['dock-loop',24,2,2]])seq+=`\t${n}:\n\t\tFilename: sevenfall|art/new-realms/${p.id}.png\n\t\tStart: ${start}\n\t\tLength: ${len}\n\t\tFacings: -8\n\t\tStride: ${stride}\n\t\tTick: 120\n`;
  }
  seq+=`\ticon:\n\t\tFilename: sevenfall|art/new-realms/${p.id}-icon.png\n`;
  if(!building)seq+=`${p.id}_death:\n\tdie:\n\t\tFilename: sevenfall|art/new-realms/${p.id}.png\n\t\tStart: 40\n\t\tLength: 3\n\t\tFacings: -8\n\t\tTick: 120\n\tcorpse:\n\t\tFilename: sevenfall|art/new-realms/${p.id}.png\n\t\tStart: 42\n\t\tLength: 1\n\t\tFacings: -8\n\t\tStride: 3\n`;
  manifest.push({id:p.id,kind:p.kind,source:p.source,sourceSha256:sha(source),file:'mods/sevenfall/art/new-realms/'+p.id+'.png',sha256:sha(packed),frames:order.length,frameSize:size,authoredFrames:cells.length,sourceSize:[m.width,m.height],frameHashes:order.map(i=>sha(frames[i])),tool:'built-in image generation; technical packing with sharp'});
  console.log(p.id+': '+cells.length+' authored poses/states');
 }
 await fs.writeFile(path.join(root,'mods/sevenfall/sequences/new-realms.yaml'),seq);
 await fs.writeFile(path.join(root,'art/new-realms/painted-manifest.json'),JSON.stringify(manifest,null,2)+'\n');
 const exclusive=new Set(roster.units.map(u=>u[1]));await fs.writeFile(path.join(root,'art/new-realms/manifest.json'),JSON.stringify(manifest.filter(x=>exclusive.has(x.id)),null,2)+'\n');
 await canvas(8*128,Math.ceil(previews.length/8)*128).composite(previews.map((input,i)=>({input,left:i%8*128,top:Math.floor(i/8)*128}))).png().toFile(path.join(root,'art/new-realms/painted-preview.png'));
}
main().catch(e=>{console.error(e);process.exitCode=1;});
