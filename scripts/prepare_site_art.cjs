// Technical export of original artwork only; no proprietary game assets.
const sharp=require('sharp'),fs=require('node:fs/promises'),path=require('node:path');
const root=path.resolve(__dirname,'..');
async function vehicleFacing(source) {
  const {data,info}=await sharp(source).ensureAlpha().raw().toBuffer({resolveWithObject:true});
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
  if(boxes.length!==8)throw Error(source+' must contain eight separated vehicles, found '+boxes.length);
  boxes.sort((a,b)=>(a.top+a.bottom)-(b.top+b.bottom));
  const ordered=[];
  for(let row=0;row<2;row++)ordered.push(...boxes.slice(row*4,(row+1)*4).sort((a,b)=>a.left-b.left));
  const b=ordered[3];
  return sharp(await sharp(source).extract({left:b.left,top:b.top,width:b.right-b.left,height:b.bottom-b.top}).png().toBuffer());
}
async function main(){
 const records=JSON.parse(await fs.readFile(path.join(root,'docs/roster.json'),'utf8'));
 const out=path.join(root,'docs/assets/roster');await fs.mkdir(path.join(out,'full'),{recursive:true});
 let count=0;
 for(const record of records){
  const source=path.join(root,record.source);
  if(process.argv.includes('--available')){try{await fs.access(source);}catch{continue;}}
  let art=sharp(source);
  if(record.sprite) art=await vehicleFacing(source);
  await art.clone().trim().resize(1024,768,{fit:'contain',background:{r:0,g:0,b:0,alpha:0},kernel:'lanczos3'}).webp({quality:90,alphaQuality:100}).toFile(path.join(out,'full',record.id+'.webp'));
  await art.trim().resize(512,384,{fit:'contain',background:{r:0,g:0,b:0,alpha:0},kernel:'lanczos3'}).webp({quality:88,alphaQuality:100}).toFile(path.join(out,record.id+'.webp'));
  count++;
 }
 for(const faction of ['angels','humans','demons']) await sharp(path.join(root,'art/source',faction+'-emblem.png')).trim().resize(256,256,{fit:'contain',background:{r:0,g:0,b:0,alpha:0}}).webp({quality:90}).toFile(path.join(out,faction+'-emblem.webp'));
 console.log(`Exported ${count}/${records.length} roster images and three emblems.`);
}
main().catch(e=>{console.error(e);process.exitCode=1;});
