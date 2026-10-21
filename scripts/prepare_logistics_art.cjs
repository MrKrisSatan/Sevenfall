// Technical slicing, resizing and OpenRA PNG metadata; no generated drawing.
const sharp = require('sharp');
const fs = require('node:fs/promises');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
const source = name => path.join(root, 'art/source', name + '.png');
const out = name => path.join(root, 'mods/sevenfall/art', name + '.png');
const transparent = {r:0,g:0,b:0,alpha:0};
const canvas = (width,height) => sharp({create:{width,height,channels:4,background:transparent}});

// OpenRA PngSheetLoader consumes standard PNG tEXt chunks.
function textChunk(key, value) {
  const data = Buffer.from(key + '\0' + value, 'latin1');
  const body = Buffer.concat([Buffer.from('tEXt'), data]);
  let crc = 0xffffffff;
  for (const byte of body) {
    crc ^= byte;
    for (let i=0;i<8;i++) crc=(crc>>>1)^((crc&1)?0xedb88320:0);
  }
  const length=Buffer.alloc(4), checksum=Buffer.alloc(4);
  length.writeUInt32BE(data.length); checksum.writeUInt32BE((crc^0xffffffff)>>>0);
  return Buffer.concat([length,body,checksum]);
}
async function saveSheet(buffer, name, size, amount) {
  const metadata = [textChunk('FrameSize', size.join(',')), textChunk('FrameAmount', String(amount))];
  await fs.writeFile(out(name), Buffer.concat([buffer.subarray(0,-12),...metadata,buffer.subarray(-12)]));
}
async function cellFrames(name, columns, rows, size, maxWidth, maxHeight) {
  const meta=await sharp(source(name)).metadata();
  if (!meta.hasAlpha) throw Error(name+' needs alpha');
  // Generated turnarounds have uneven margins. Detect each connected vehicle
  // instead of clipping a scoop that crosses a nominal grid-cell boundary.
  const {data,info}=await sharp(source(name)).ensureAlpha().raw().toBuffer({resolveWithObject:true});
  const count=info.width*info.height, seen=new Uint8Array(count), queue=new Int32Array(count), boxes=[];
  for(let seed=0;seed<count;seed++) {
    if(seen[seed] || data[seed*4+3]<32)continue;
    let read=0,write=1,minX=info.width,minY=info.height,maxX=0,maxY=0;
    queue[0]=seed;seen[seed]=1;
    while(read<write) {
      const p=queue[read++], x=p%info.width, y=Math.floor(p/info.width);
      minX=Math.min(minX,x);maxX=Math.max(maxX,x);minY=Math.min(minY,y);maxY=Math.max(maxY,y);
      for(const q of [x>0?p-1:-1,x+1<info.width?p+1:-1,y>0?p-info.width:-1,y+1<info.height?p+info.width:-1]) {
        if(q>=0 && !seen[q] && data[q*4+3]>=32){seen[q]=1;queue[write++]=q;}
      }
    }
    if(write>count/300) boxes.push({left:Math.max(0,minX-3),top:Math.max(0,minY-3),
      right:Math.min(info.width,maxX+4),bottom:Math.min(info.height,maxY+4)});
  }
  if(boxes.length!==columns*rows)throw Error(name+' must contain eight separated vehicles, found '+boxes.length);
  boxes.sort((a,b)=>(a.top+a.bottom)-(b.top+b.bottom));
  const ordered=[];
  for(let row=0;row<rows;row++)ordered.push(...boxes.slice(row*columns,(row+1)*columns).sort((a,b)=>a.left-b.left));
  const frames=[];
  for(let i=0;i<columns*rows;i++) {
    const b=ordered[i];
    const raw=await sharp(source(name)).extract({left:b.left,top:b.top,width:b.right-b.left,height:b.bottom-b.top}).png().toBuffer();
    const sprite=await sharp(raw).trim().resize(maxWidth,maxHeight,{fit:'inside'}).ensureAlpha().png().toBuffer({resolveWithObject:true});
    frames.push(await canvas(size,size).composite([{input:sprite.data,left:Math.floor((size-sprite.info.width)/2),top:Math.floor((size-sprite.info.height)/2)}]).png().toBuffer());
  }
  return frames;
}
async function main() {
  const previews=[];
  for (const [index,faction] of ['a','h','d'].entries()) {
    const name=faction+'-yard';
    const sprite=await sharp(source(name)).trim().resize(96,100,{fit:'inside'}).ensureAlpha().png().toBuffer({resolveWithObject:true});
    await canvas(128,128).composite([{input:sprite.data,left:Math.floor((128-sprite.info.width)/2),top:112-sprite.info.height}]).png().toFile(out(name));
    await sharp(source(name)).trim().resize(56,42,{fit:'contain',background:'#171b22'}).flatten({background:'#171b22'}).png().toFile(out(name+'-icon'));
    previews.push({input:await sharp(out(name)).resize(384,384,{kernel:'nearest'}).toBuffer(),left:index*400+8,top:0});
    for(const [row,kind] of ['mcv','harvester'].entries()) {
      const name=faction+'-'+kind;
      const frames=await cellFrames(name,4,2,64,42,42);
      const sheet=await canvas(512,64).composite(frames.map((input,i)=>({input,left:i*64,top:0}))).png().toBuffer();
      await saveSheet(sheet,name,[64,64],8);
      await sharp(frames[3]).trim().resize(56,42,{fit:'contain',background:'#171b22'}).flatten({background:'#171b22'}).png().toFile(out(name+'-icon'));
      previews.push({input:await sharp(frames[3]).resize(192,192,{kernel:'nearest'}).toBuffer(),left:index*400+104,top:360+row*176});
    }
  }
  for(const [index,grade] of ['rough','enriched'].entries()) {
    const name='veilglass-'+grade;
    // Source cells deliberately retain increasing density, so use one common scale.
    const meta=await sharp(source(name)).metadata();
    if(!meta.hasAlpha || meta.width%4)throw Error(name+' needs a four-cell alpha sheet');
    const {data,info}=await sharp(source(name)).ensureAlpha().raw().toBuffer({resolveWithObject:true});
    const gaps=[];
    let start=-1;
    for(let x=0;x<=info.width;x++) {
      let used=false;
      if(x<info.width)for(let y=0;y<info.height;y++)if(data[(y*info.width+x)*4+3]>32){used=true;break;}
      if(!used && start<0)start=x;
      if((used || x===info.width) && start>=0) {
        if(x-start>12 && start>0 && x<info.width)gaps.push(Math.floor((start+x)/2));
        start=-1;
      }
    }
    const cuts=[0];
    for(let i=1;i<4;i++) {
      const target=i*info.width/4;
      const closest=gaps.toSorted((a,b)=>Math.abs(a-target)-Math.abs(b-target))[0];
      if(closest===undefined || Math.abs(closest-target)>info.width/8 || closest<=cuts.at(-1))
        throw Error(name+' needs four clearly separated density states');
      cuts.push(closest);
    }
    cuts.push(info.width);
    const crops=[];
    for(let i=0;i<4;i++) {
      const input=await sharp(source(name)).extract({left:cuts[i],top:0,width:cuts[i+1]-cuts[i],height:meta.height}).png().toBuffer();
      crops.push(await sharp(input).trim().png().toBuffer({resolveWithObject:true}));
    }
    const scale=Math.min(22/Math.max(...crops.map(c=>c.info.width)),20/Math.max(...crops.map(c=>c.info.height)));
    const frames=[];
    for(const crop of crops) {
      const width=Math.max(1,Math.round(crop.info.width*scale)),height=Math.max(1,Math.round(crop.info.height*scale));
      const input=await sharp(crop.data).resize(width,height).png().toBuffer();
      frames.push(await canvas(24,24).composite([{input,left:Math.floor((24-width)/2),top:22-height}]).png().toBuffer());
    }
    await saveSheet(await canvas(96,24).composite(frames.map((input,i)=>({input,left:i*24,top:0}))).png().toBuffer(),name,[24,24],4);
    previews.push({input:await sharp(out(name)).resize(384,96,{kernel:'nearest'}).toBuffer(),left:200+index*400,top:728});
  }
  await sharp({create:{width:1200,height:840,channels:4,background:'#202a29'}}).composite(previews).png().toFile(path.join(root,'art/logistics-preview.png'));
  console.log('Prepared three yards, six eight-facing vehicles, nine icons and two four-density Veilglass sheets.');
}
main().catch(e=>{console.error(e);process.exitCode=1;});
