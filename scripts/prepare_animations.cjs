// Technical slicing, scaling and packing only. Pose/damage artwork is authored
// by image generation; this script never synthesizes motion or paints damage.
const sharp = require('sharp');
const fs = require('node:fs/promises');
const path = require('node:path');
const crypto = require('node:crypto');
const root = path.resolve(__dirname, '..');
const folder = path.join(root, 'art/animations');
const available = process.argv.includes('--available');
const hash = b => crypto.createHash('sha256').update(b).digest('hex');
const blank = (width, height) => sharp({create:{width,height,channels:4,background:{r:0,g:0,b:0,alpha:0}}});

function pngText(key, value) {
  const data = Buffer.from(key+'\0'+value, 'latin1');
  const body = Buffer.concat([Buffer.from('tEXt'), data]);
  let crc = 0xffffffff;
  for (const byte of body) { crc ^= byte; for(let i=0;i<8;i++) crc=(crc>>>1)^((crc&1)?0xedb88320:0); }
  const length=Buffer.alloc(4), checksum=Buffer.alloc(4);
  length.writeUInt32BE(data.length); checksum.writeUInt32BE((crc^0xffffffff)>>>0);
  return Buffer.concat([length,body,checksum]);
}

async function bounds(buffer) {
  const {data,info} = await sharp(buffer).ensureAlpha().raw().toBuffer({resolveWithObject:true});
  let left=info.width, top=info.height, right=-1, bottom=-1, transparent=0;
  for(let y=0;y<info.height;y++) for(let x=0;x<info.width;x++) {
    const a=data[(y*info.width+x)*4+3];
    if(a<16) transparent++;
    if(a<32) continue;
    left=Math.min(left,x); top=Math.min(top,y); right=Math.max(right,x); bottom=Math.max(bottom,y);
  }
  if(right<left || bottom<top) throw Error('Empty sprite cell');
  if(transparent/(info.width*info.height)<0.15) throw Error('Sprite cell lacks clear alpha margins');
  return {left,top,width:right-left+1,height:bottom-top+1};
}

async function pack(frames, size, file) {
  const cols=8, rows=Math.ceil(frames.length/cols);
  const png=await blank(cols*size.width,rows*size.height).composite(frames.map((input,i)=>({input,left:(i%cols)*size.width,top:Math.floor(i/cols)*size.height}))).png().toBuffer();
  const result=Buffer.concat([png.subarray(0,-12),pngText('FrameSize',`${size.width},${size.height}`),pngText('FrameAmount',String(frames.length)),png.subarray(-12)]);
  await fs.writeFile(file,result);
  return result;
}

async function unitFrames(requests, unit) {
  const inputs=[], boxes=[], cells=[];
  for(const request of requests) {
    const data=await fs.readFile(request.destination), meta=await sharp(data).metadata();
    if(meta.width%8 || meta.height%12) throw Error(`${request.id}: expected an exact 8x12 atlas`);
    const w=meta.width/8,h=meta.height/12;
    if(w!==h) throw Error(`${request.id}: cells must be square`);
    const decoded=await sharp(data).ensureAlpha().raw().toBuffer();
    // Generated atlases have regular columns, but their rows can have unequal
    // padding. Find the twelve authored bands instead of cutting through feet,
    // turrets or muzzle flashes at nominal 128-pixel boundaries.
    const density=new Uint32Array(meta.height);
    for(let y=0;y<meta.height;y++) for(let x=0;x<meta.width;x++) if(decoded[(y*meta.width+x)*4+3]>=32) density[y]++;
    const threshold=Math.max(...density)*0.15;
    let bands=[];
    for(let y=0;y<meta.height;y++) if(density[y]>threshold) {
      if(!bands.length || y>bands[bands.length-1].end+7) bands.push({start:y,end:y});
      else bands[bands.length-1].end=y;
    }
    bands=bands.filter(b=>b.end-b.start>=10);
    if(bands.length<11 || bands.length>13) throw Error(`${request.id}: expected 11–13 separated authored pose rows, found ${bands.length}`);
    const edges=[0];
    for(let i=1;i<bands.length;i++) edges.push(Math.floor((bands[i-1].end+bands[i].start)/2));
    edges.push(meta.height);
    // Some authored atlases contain three or five death poses. Select four
    // timing frames from those real poses; a three-pose cycle holds its final
    // wreck for one frame. Never replace an empty movement or attack pose.
    const deathRows=bands.length-8;
    const deathMap=deathRows===3?[8,9,10,10]:deathRows===5?[8,9,11,12]:[8,9,10,11];
    const batch=[];
    for(let state=0;state<3;state++) for(let facing=0;facing<8;facing++) for(let frame=0;frame<4;frame++) {
      const row=state===2?deathMap[frame]:state*4+frame, height=edges[row+1]-edges[row], pixels=Buffer.alloc(w*height*4);
      for(let y=0;y<height;y++) {
        const start=((edges[row]+y)*meta.width+facing*w)*4;
        decoded.copy(pixels,y*w*4,start,start+w*4);
      }
      const cell=await sharp(pixels,{raw:{width:w,height,channels:4}}).png().toBuffer();
      let b;
      try { b=await bounds(cell); }
      catch(error) { throw Error(`${request.id} row ${row+1}, facing ${facing}: ${error.message}`); }
      batch.push(cell); boxes.push(b);
    }
    cells.push(...batch);
    inputs.push({id:request.id,source:path.relative(root,request.destination).replaceAll('\\','/'),sha256:hash(data),poseRows:bands.length,deathRowMap:deathMap});
  }
  // One scale for all poses, facings and damage variants prevents per-frame jitter.
  const movement=boxes.filter((b,i)=>i%96<32);
  const scale=Math.min(unit.drawSize/Math.max(...movement.map(b=>Math.max(b.width,b.height))),
    124/Math.max(...boxes.map(b=>Math.max(b.width,b.height))));
  const frames=[];
  for(let i=0;i<cells.length;i++) {
    const width=Math.max(1,Math.round(boxes[i].width*scale)),height=Math.max(1,Math.round(boxes[i].height*scale));
    const input=await sharp(cells[i]).extract(boxes[i]).resize(width,height).png().toBuffer();
    frames.push(await blank(128,128).composite([{input,left:Math.floor((128-width)/2),top:Math.floor((128-height)/2)}]).png().toBuffer());
  }
  return {frames,inputs};
}

async function main() {
  const plan=JSON.parse(await fs.readFile(path.join(folder,'plan.json'),'utf8')).map(p=>({...p,
    reference:path.resolve(root,p.reference),destination:path.resolve(root,p.destination)}));
  const roster=JSON.parse(await fs.readFile(path.join(root,'art/unit-turnarounds/roster.json'),'utf8'));
  const ready=[];
  for(const request of plan) {
    try { await fs.access(request.destination); ready.push(request); }
    catch(error) { if(!available) throw Error(`Missing authored asset ${request.id}`); }
  }
  await fs.mkdir(path.join(folder,'sheets'),{recursive:true});
  let previous=[];
  try { previous=JSON.parse(await fs.readFile(path.join(folder,'manifest.json'),'utf8')).assets; } catch(error) { if(error.code!=='ENOENT') throw error; }
  const manifest=[];
  for(const unit of roster) {
    const requests=ready.filter(p=>p.kind==='unit'&&p.unit===unit.id);
    const required=plan.filter(p=>p.kind==='unit'&&p.unit===unit.id);
    if(!requests.length || requests.length!==required.length) continue;
    const cached=previous.find(a=>a.kind==='unit'&&a.id===unit.id);
    if(cached && cached.packerVersion===2 && cached.inputs.length===requests.length && (await Promise.all(requests.map(p=>fs.readFile(p.destination)))).every((b,i)=>hash(b)===cached.inputs[i].sha256)) {
      const exported=await fs.readFile(path.join(root,cached.file));
      if(hash(exported)!==cached.sha256) throw Error(`${unit.id}: existing export hash mismatch`);
      manifest.push(cached); console.log(`${unit.id}: unchanged validated export`); continue;
    }
    const {frames,inputs}=await unitFrames(requests,unit);
    const file=path.join(folder,'sheets',unit.id+'.png');
    const data=await pack(frames,{width:128,height:128},file);
    manifest.push({id:unit.id,kind:'unit',packerVersion:2,category:unit.category,frameSize:[128,128],frames:frames.length,inputs,
      file:path.relative(root,file).replaceAll('\\','/'),sha256:hash(data),frameHashes:frames.map(hash)});
    console.log(`${unit.id}: ${frames.length} packed frames`);
  }
  for(const request of ready.filter(p=>p.kind==='building')) {
    const source=await fs.readFile(request.destination), meta=await sharp(source).metadata();
    if(meta.width%3) throw Error(`${request.id}: expected three equal-width horizontal damage cells`);
    const cellWidth=meta.width/3;
    const original=await fs.readFile(request.reference), dimensions=await sharp(original).metadata(), originalBounds=await bounds(original);
    const cells=[], boxes=[];
    for(let i=0;i<3;i++) {
      const cell=await sharp(source).extract({left:i*cellWidth,top:0,width:cellWidth,height:meta.height}).png().toBuffer();
      cells.push(cell); boxes.push(await bounds(cell));
    }
    const scale=Math.min(originalBounds.width/boxes[0].width, originalBounds.height/boxes[0].height,
      ...boxes.map(b=>Math.min((dimensions.width-4)/b.width,(dimensions.height-4)/b.height)));
    const frames=[];
    for(let i=0;i<3;i++) {
      const b=boxes[i],width=Math.max(1,Math.round(b.width*scale)),height=Math.max(1,Math.round(b.height*scale));
      const input=await sharp(cells[i]).extract(b).resize(width,height).png().toBuffer();
      frames.push(await blank(dimensions.width,dimensions.height).composite([{input,left:Math.floor((dimensions.width-width)/2),top:Math.max(0,Math.min(dimensions.height-height,originalBounds.top+originalBounds.height-height))}]).png().toBuffer());
    }
    const file=path.join(folder,'sheets',request.id+'-damage.png');
    const data=await pack(frames,dimensions,file);
    manifest.push({id:request.id,kind:'building',frameSize:[dimensions.width,dimensions.height],frames:3,
      inputs:[{source:path.relative(root,request.destination).replaceAll('\\','/'),sha256:hash(source)}],
      file:path.relative(root,file).replaceAll('\\','/'),sha256:hash(data),frameHashes:frames.map(hash)});
    console.log(`${request.id}: damaged, critical and rubble frames packed`);
  }
  await fs.writeFile(path.join(folder,'manifest.json'),JSON.stringify({frameOrder:'state, facing, time',facings:-8,assets:manifest},null,2)+'\n');
  console.log(`${manifest.length} assets packed; ${ready.length}/${plan.length} authored atlases present.`);
}
main().catch(error=>{ console.error(error.stack); process.exitCode=1; });
