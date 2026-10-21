// Technical slicing/packing only. Artwork and corrections are authored with image generation.
const sharp = require('sharp');
const fs = require('node:fs/promises');
const path = require('node:path');
const crypto = require('node:crypto');
const root = path.resolve(__dirname, '..');
const output = path.join(root, 'art/unit-turnarounds');
const directions = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw'];
const clear = {r:0,g:0,b:0,alpha:0};
const canvas = (w,h) => sharp({create:{width:w,height:h,channels:4,background:clear}});
const sha = data => crypto.createHash('sha256').update(data).digest('hex');

function pngText(key, value) {
  const data=Buffer.from(key+'\0'+value,'latin1'),body=Buffer.concat([Buffer.from('tEXt'),data]);
  let crc=0xffffffff;
  for(const byte of body){crc^=byte;for(let i=0;i<8;i++)crc=(crc>>>1)^((crc&1)?0xedb88320:0);}
  const length=Buffer.alloc(4),checksum=Buffer.alloc(4);
  length.writeUInt32BE(data.length);checksum.writeUInt32BE((crc^0xffffffff)>>>0);
  return Buffer.concat([length,body,checksum]);
}

async function findViews(source) {
  const {data,info}=await sharp(source).ensureAlpha().raw().toBuffer({resolveWithObject:true});
  const count=info.width*info.height,seen=new Uint8Array(count),queue=new Int32Array(count),components=[];
  let clearPixels=0;
  for(let seed=0;seed<count;seed++) {
    if(data[seed*4+3]===0)clearPixels++;
    if(seen[seed]||data[seed*4+3]<32)continue;
    let read=0,write=1,left=info.width,top=info.height,right=0,bottom=0;
    seen[seed]=1;queue[0]=seed;
    while(read<write){
      const p=queue[read++],x=p%info.width,y=Math.floor(p/info.width);
      left=Math.min(left,x);right=Math.max(right,x);top=Math.min(top,y);bottom=Math.max(bottom,y);
      for(const q of [x>0?p-1:-1,x+1<info.width?p+1:-1,y>0?p-info.width:-1,y+1<info.height?p+info.width:-1]){
        if(q>=0&&!seen[q]&&data[q*4+3]>=32){seen[q]=1;queue[write++]=q;}
      }
    }
    components.push({left,top,right,bottom,pixels:write});
  }
  if(clearPixels/count<0.2)throw Error('Expected a genuinely transparent, separated eight-view sheet');
  const major=components.filter(b=>b.pixels>count/400);
  if(major.length!==8)throw Error(`Expected eight separate silhouettes, found ${major.length}`);
  major.sort((a,b)=>(a.top+a.bottom)-(b.top+b.bottom));
  const ordered=[];
  for(let row=0;row<2;row++)ordered.push(...major.slice(row*4,(row+1)*4).sort((a,b)=>a.left-b.left));
  const centers=ordered.map(b=>[(b.left+b.right)/2,(b.top+b.bottom)/2]);
  // Retain disconnected details belonging to a sprite, without painting or changing alpha.
  for(const b of components){
    if(major.includes(b)||b.pixels<8)continue;
    const x=(b.left+b.right)/2,y=(b.top+b.bottom)/2;
    const nearest=centers.map(([cx,cy],i)=>({i,d:(x-cx)**2+(y-cy)**2})).sort((a,b)=>a.d-b.d)[0].i;
    const target=ordered[nearest];
    target.left=Math.min(target.left,b.left);target.right=Math.max(target.right,b.right);
    target.top=Math.min(target.top,b.top);target.bottom=Math.max(target.bottom,b.bottom);
  }
  return ordered.map(b=>{
    const left=Math.max(0,b.left-3),top=Math.max(0,b.top-3);
    return {left,top,width:Math.min(info.width,b.right+4)-left,height:Math.min(info.height,b.bottom+4)-top};
  });
}

async function framed(crop, size, scale, grounded) {
  const width=Math.max(1,Math.round(crop.info.width*scale)),height=Math.max(1,Math.round(crop.info.height*scale));
  const input=await sharp(crop.data).resize(width,height).png().toBuffer();
  const left=Math.floor((size-width)/2),top=grounded?Math.floor(size*0.84)-height:Math.floor((size-height)/2);
  if(left<0||top<0||left+width>size||top+height>size)throw Error('Frame bounds exceeded');
  return canvas(size,size).composite([{input,left,top}]).png().toBuffer();
}

async function main(){
  const roster=JSON.parse(await fs.readFile(path.join(output,'roster.json'),'utf8'));
  const web=path.join(root,'docs/assets/turnarounds');
  await fs.mkdir(web,{recursive:true});await fs.mkdir(path.join(output,'sheets'),{recursive:true});
  const manifest=[],failures=[];
  for(const unit of roster){
    const source=path.join(root,unit.source);
    try{await fs.access(source);}catch(error){if(process.argv.includes('--available'))continue;throw error;}
    try{
      const sourceData=await fs.readFile(source),boxes=await findViews(sourceData),crops=[];
      for(const box of boxes){const cropped=await sharp(sourceData).extract(box).png().toBuffer();crops.push(await sharp(cropped).trim().png().toBuffer({resolveWithObject:true}));}
      const maxWidth=Math.max(...crops.map(c=>c.info.width)),maxHeight=Math.max(...crops.map(c=>c.info.height));
      const grounded=unit.category==='infantry';
      const displayScale=Math.min(216/maxWidth,(grounded?202:216)/maxHeight);
      const gameScale=Math.min(unit.drawSize/maxWidth,unit.drawSize/maxHeight);
      const frames=[],sprites=[],frameDir=path.join(output,'frames',unit.id),frameHashes=[];
      await fs.mkdir(frameDir,{recursive:true});
      for(let i=0;i<8;i++){
        const frame=await framed(crops[i],256,displayScale,grounded);
        await fs.writeFile(path.join(frameDir,directions[i]+'.png'),frame);
        frameHashes.push(sha(frame));frames.push(frame);
        sprites.push(await framed(crops[i],unit.frameSize,gameScale,false));
      }
      if(new Set(frameHashes).size!==8)throw Error('Duplicate directional images');
      const strip=await canvas(unit.frameSize*8,unit.frameSize).composite(sprites.map((input,i)=>({input,left:i*unit.frameSize,top:0}))).png().toBuffer();
      const packed=Buffer.concat([strip.subarray(0,-12),pngText('FrameSize',`${unit.frameSize},${unit.frameSize}`),pngText('FrameAmount','8'),strip.subarray(-12)]);
      await fs.writeFile(path.join(output,'sheets',unit.id+'.png'),packed);
      await canvas(1024,512).composite(frames.map((input,i)=>({input,left:(i%4)*256,top:Math.floor(i/4)*256}))).webp({quality:90,alphaQuality:100}).toFile(path.join(web,unit.id+'.webp'));
      manifest.push({id:unit.id,source:unit.source,sourceSha256:sha(sourceData),directions,boxes,frameSize:unit.frameSize,drawSize:unit.drawSize,frameHashes,sheetSha256:sha(packed),sheet:`art/unit-turnarounds/sheets/${unit.id}.png`,frames:directions.map(d=>`art/unit-turnarounds/frames/${unit.id}/${d}.png`),preview:`assets/turnarounds/${unit.id}.webp`});
      console.log(unit.id+': eight facings packed');
    }catch(error){failures.push(unit.id+': '+error.message);}
  }
  await fs.writeFile(path.join(output,'manifest.json'),JSON.stringify({directionOrder:directions,openraFacings:-8,assets:manifest},null,2)+'\n');
  console.log(`Packed ${manifest.length}/${roster.length} units (${manifest.length*8} facings).`);
  if(failures.length)throw Error(failures.join('\n'));
}
main().catch(error=>{console.error(error.message);process.exitCode=1;});
