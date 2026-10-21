// Reproducible asset sizing/packing. Artwork is authored separately in art/source.
const sharp = require('sharp');
const fs = require('node:fs/promises');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
const output = path.join(root, 'mods/sevenfall/art');
const source = name => path.join(root, 'art/source', name + '.png');
const transparent = { r: 0, g: 0, b: 0, alpha: 0 };
const textureSize = n => 2 ** Math.ceil(Math.log2(n));

async function main() {
  await fs.mkdir(output, { recursive: true });
  const actors = [['a-spire', 64, 96], ['h-generator', 68, 68], ['d-heart', 68, 76]];
  const previews = [];
  for (const [name, width, height] of actors) {
    const metadata = await sharp(source(name)).metadata();
    if (!metadata.hasAlpha) throw Error(`${name} must have transparency`);
    const sprite = await sharp(source(name)).trim().resize(width, height, { fit: 'inside' })
      .ensureAlpha().png().toBuffer({ resolveWithObject: true });
    const file = path.join(output, name + '.png');
    await sharp({ create: { width: 96, height: 112, channels: 4, background: transparent } })
      .composite([{ input: sprite.data, left: Math.floor((96-sprite.info.width)/2), top: 100-sprite.info.height }])
      .png().toFile(file);
    await sharp(source(name)).trim().resize(56, 42, { fit: 'contain', background: '#171b22' })
      .flatten({ background: '#171b22' }).png().toFile(path.join(output, name + '-icon.png'));
    previews.push({ input: await sharp(file).resize(288, 336, { kernel: 'nearest' }).toBuffer(), left: previews.length*320+16, top: 32 });
  }
  const factions = ['angels', 'humans', 'demons'];
  const refineryPreviews = [];
  for (const name of ['a-veilworks', 'h-veilworks', 'd-veilworks']) {
    const metadata = await sharp(source(name)).metadata();
    if (!metadata.hasAlpha) throw Error(`${name} must have transparency`);
    const sprite = await sharp(source(name)).trim().resize(88, 96, { fit: 'inside' })
      .ensureAlpha().png().toBuffer({ resolveWithObject: true });
    const file = path.join(output, name + '.png');
    await sharp({ create: { width: 128, height: 128, channels: 4, background: transparent } })
      .composite([{ input: sprite.data, left: Math.floor((128-sprite.info.width)/2), top: 112-sprite.info.height }])
      .png().toFile(file);
    await sharp(source(name)).trim().resize(56, 42, { fit: 'contain', background: '#171b22' })
      .flatten({ background: '#171b22' }).png().toFile(path.join(output, name + '-icon.png'));
    refineryPreviews.push({ input: await sharp(file).resize(384, 384, { kernel: 'nearest' }).toBuffer(),
      left: refineryPreviews.length*400+8, top: 8 });
  }
  await sharp({ create: { width: 1200, height: 400, channels: 4, background: '#202a29' } })
    .composite(refineryPreviews).png().toFile(path.join(root, 'art/refinery-buildings-preview.png'));
  // All nine faction IDs share their parent's emblem in this first pass.
  // Separate image scales keep the existing lobby's logical 30x15 regions intact.
  for (const scale of [1, 2, 3]) {
    const badges = [];
    for (const [i, faction] of factions.entries()) {
      const input = await sharp(source(faction + '-emblem')).trim()
        .resize(30*scale, 15*scale, { fit: 'contain', background: transparent }).png().toBuffer();
      badges.push({ input, left: 0, top: i*15*scale });
    }
    const question = Buffer.from(`<svg width="${30*scale}" height="${15*scale}"><text x="50%" y="80%" text-anchor="middle" font-family="sans-serif" font-size="${14*scale}" fill="#ced4df">?</text></svg>`);
    badges.push({ input: await sharp(question).png().toBuffer(), left: 0, top: 45*scale });
    await sharp({ create: { width: textureSize(30*scale), height: textureSize(60*scale), channels: 4, background: transparent } })
      .composite(badges).png().toFile(path.join(output, `factions${scale===1?'':`-${scale}x`}.png`));
    const marks = [];
    for (const [i, faction] of factions.entries()) {
      marks.push({input: await sharp(source(faction+'-emblem')).trim()
        .resize(80*scale, 125*scale, {fit:'contain', background:transparent}).png().toBuffer(),
        left: (8+i*80)*scale, top: 42*scale});
    }
    const title = Buffer.from(`<svg width="${256*scale}" height="${256*scale}" viewBox="0 0 256 256"><text x="128" y="202" text-anchor="middle" font-family="Georgia" font-weight="bold" font-size="29" fill="#e7d6af">SEVENFALL</text><text x="128" y="222" text-anchor="middle" font-family="sans-serif" font-size="11" letter-spacing="1.5" fill="#c3c9d4">THE WAR FOR CREATION</text></svg>`);
    const logo = await sharp({create:{width:256*scale,height:256*scale,channels:4,background:transparent}})
      .composite([...marks,{input:await sharp(title).png().toBuffer(),left:0,top:0}]).png().toBuffer();
    const stripe = Buffer.from(`<svg width="${253*scale}" height="${256*scale}" viewBox="0 0 253 256"><rect y="64" width="253" height="128" fill="#161e29"/><path d="M0 64H253M0 192H253" stroke="#a58b5b" stroke-width="2"/></svg>`);
    await sharp({create:{width:textureSize(512*scale),height:textureSize(256*scale),channels:4,background:transparent}})
      .composite([{input:logo,left:0,top:0},{input:await sharp(stripe).png().toBuffer(),left:258*scale,top:0}])
      .png().toFile(path.join(output, `loadscreen${scale===1?'':`-${scale}x`}.png`));
  }
  await sharp({ create: { width: 960, height: 400, channels: 4, background: '#202a29' } })
    .composite(previews).png().toFile(path.join(root, 'art/power-buildings-preview.png'));
  console.log('Prepared six building sprites, six production icons, and 1x/2x/3x faction atlases.');
}
main().catch(error => { console.error(error); process.exitCode = 1; });
