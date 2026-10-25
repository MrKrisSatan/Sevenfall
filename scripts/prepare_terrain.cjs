// Technical slicing/resizing of authored textures; no generated painting.
const fs = require('node:fs/promises');
const path = require('node:path');
const sharp = require('sharp');
const crypto = require('node:crypto');
const root = path.resolve(__dirname, '..');
function chunk(key, value) {
  const data = Buffer.from(key + '\0' + value), body = Buffer.concat([Buffer.from('tEXt'), data]);
  let crc = 0xffffffff;
  for (const byte of body) { crc ^= byte; for (let i=0;i<8;i++) crc = (crc >>> 1) ^ ((crc & 1) ? 0xedb88320 : 0); }
  const size = Buffer.alloc(4), sum = Buffer.alloc(4);
  size.writeUInt32BE(data.length); sum.writeUInt32BE((crc ^ 0xffffffff) >>> 0);
  return Buffer.concat([size, body, sum]);
}
const hash = data => crypto.createHash('sha256').update(data).digest('hex');
(async () => {
  const assets = [];
  for (const kind of ['ground', 'water']) {
    const source = `art/terrain/source/${kind}.png`;
    const data = await fs.readFile(path.join(root, source));
    const metadata = await sharp(data).metadata();
    const cols = kind === 'ground' ? 4 : 1, rows = cols;
    const tileW = Math.floor(metadata.width / cols), tileH = Math.floor(metadata.height / rows);
    const layers = [];
    for (let y=0;y<rows;y++) for (let x=0;x<cols;x++) layers.push({
      input: await sharp(data).extract({left:x*tileW,top:y*tileH,width:tileW,height:tileH}).resize(24,24).ensureAlpha().png().toBuffer(),
      left:x*24,top:y*24
    });
    const png = await sharp({create:{width:cols*24,height:rows*24,channels:4,background:{r:0,g:0,b:0,alpha:0}}}).composite(layers).png().toBuffer();
    const output = Buffer.concat([png.subarray(0,-12),chunk('FrameSize','24,24'),chunk('FrameAmount',String(cols*rows)),png.subarray(-12)]);
    const file = `mods/sevenfall/art/terrain/${kind}.png`;
    await fs.writeFile(path.join(root,file),output);
    assets.push({source,sourceSha256:hash(data),file,sha256:hash(output),frames:cols*rows});
  }
  await fs.writeFile(path.join(root,'art/terrain/manifest.json'),JSON.stringify({generator:'Built-in imagegen; original ground/water textures, 2026-10-25',assets},null,2)+'\n');
})();
