// Original sources are generated separately. This script only sizes and packs.
const sharp=require('sharp'), fs=require('node:fs/promises'),path=require('node:path');
const root=path.resolve(__dirname,'..'), out=path.join(root,'mods/sevenfall/art');
const transparent={r:0,g:0,b:0,alpha:0};
async function main(){
 const catalog=JSON.parse(await fs.readFile(path.join(root,'art/building-catalog.json'),'utf8'));
 const groups=new Map();
 let prepared=0;
 for(const item of catalog){
  const source=path.join(root,'art/source',item.name+'.png');
  if(process.argv.includes('--available')){
   try{await fs.access(source);}catch{continue;}
  }
  const meta=await sharp(source).metadata();
  if(!meta.hasAlpha)throw Error(item.name+' must have alpha');
  const sprite=await sharp(source).trim().resize(item.width,item.height,{fit:'inside'}).ensureAlpha().png().toBuffer({resolveWithObject:true});
  const file=path.join(out,item.name+'.png');
  await sharp({create:{width:128,height:128,channels:4,background:transparent}})
   .composite([{input:sprite.data,left:Math.floor((128-sprite.info.width)/2),
     top:item.anchor==='center'?Math.floor((128-sprite.info.height)/2):112-sprite.info.height}]).png().toFile(file);
  await sharp(source).trim().resize(56,42,{fit:'contain',background:'#171b22'}).flatten({background:'#171b22'}).png().toFile(path.join(out,item.name+'-icon.png'));
  if(!groups.has(item.role))groups.set(item.role,[]);
  const row=groups.get(item.role);
  row.push({input:await sharp(file).resize(384,384,{kernel:'nearest'}).toBuffer(),left:row.length*400+8,top:0});
  prepared++;
 }
 for(const [role,images] of groups){
  await sharp({create:{width:1200,height:384,channels:4,background:'#202a29'}}).composite(images).png().toFile(path.join(root,'art',role+'-buildings-preview.png'));
 }
 console.log('Prepared '+prepared+' of '+catalog.length+' original building sprites and icons.');
}
main().catch(e=>{console.error(e);process.exitCode=1;});
