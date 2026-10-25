// Original vector UI symbols, exported as an RGBA cursor atlas. GPL-3.0-or-later.
const fs = require('node:fs/promises');
const path = require('node:path');
const sharp = require('sharp');
const root = path.resolve(__dirname, '..');
const directions = ['t', 'tr', 'r', 'br', 'b', 'bl', 'l', 'tl'];
const p = d => `<path d="${d}"/>`;
const circle = '<circle cx="16" cy="16" r="9"/>';
function glyph(name) {
  let color = '#f2e9d7', shape;
  const pointer = name.startsWith('default') || name === 'joystick-all';
  if (pointer) shape = p('M3 3 L25 15 L16 18 L12 27 Z');
  else if (name.startsWith('scroll-') || name.startsWith('joystick-')) {
    const dir = directions.indexOf(name.split('-')[1]);
    shape = `<g transform="rotate(${dir * 45} 16 16)">${p('M16 4 L25 15 L20 15 L20 27 L12 27 L12 15 L7 15 Z')}</g>`;
  } else if (name.startsWith('harvest')) {
    color = '#d699ff'; shape = p('M16 3 L24 12 L22 24 L16 29 L9 23 L8 12 Z M8 12 L24 12 M16 3 L16 29');
  } else if (/^(attack|assault|c4|nuke)/.test(name)) {
    color = '#ff7f79'; shape = circle + p('M16 2 V11 M16 21 V30 M2 16 H11 M21 16 H30');
    if (name.startsWith('attackmove') || name.startsWith('assaultmove')) shape += p('M12 18 L16 12 L20 18');
    if (name.startsWith('c4') || name.startsWith('nuke')) shape += p('M12 12 L20 20 M20 12 L12 20');
  } else if (/^(repair|goldwrench)/.test(name)) {
    color = '#f4cf76'; shape = p('M8 4 L8 11 L13 14 L18 10 L17 3 L23 9 L22 16 L13 25 L8 28 L4 24 L8 19 L16 12');
  } else if (name.startsWith('heal')) {
    color = '#9ce9bd'; shape = p('M12 4 H20 V12 H28 V20 H20 V28 H12 V20 H4 V12 H12 Z');
  } else if (name.startsWith('sell')) {
    color = '#f4cf76'; shape = circle + p('M20 10 H13 L10 14 L21 18 L18 22 H11 M16 6 V26');
  } else if (name.startsWith('guard')) {
    color = '#83d8f5'; shape = p('M5 7 L16 3 L27 7 L25 21 L16 29 L7 21 Z M16 7 V24');
  } else if (name.startsWith('capture')) {
    shape = p('M8 29 V4 L26 6 L20 13 L26 19 L8 17');
  } else if (name.startsWith('enter')) {
    color = '#83d8f5'; shape = p('M19 4 H28 V28 H19 M3 16 H23 M16 9 L23 16 L16 23');
  } else if (name.startsWith('deploy')) {
    color = '#83d8f5'; shape = p('M4 14 L16 4 L28 14 V28 H4 Z M16 10 V24 M10 18 L16 24 L22 18');
  } else if (name.startsWith('powerdown')) {
    color = '#f4cf76'; shape = p('M18 2 L7 18 H15 L12 30 L26 12 H18 Z');
  } else if (name.startsWith('ability') || name.startsWith('chrono')) {
    color = '#d699ff'; shape = p('M16 3 L20 12 L29 16 L20 20 L16 29 L12 20 L3 16 L12 12 Z');
  } else if (name.startsWith('select')) {
    shape = p('M4 11 V4 H11 M21 4 H28 V11 M28 21 V28 H21 M11 28 H4 V21');
  } else if (name.startsWith('move')) {
    color = '#9ce9bd'; shape = p('M4 12 L16 24 L28 12 M8 7 L16 15 L24 7');
  } else shape = circle;
  let svg = `<g fill="none" stroke-linejoin="round" stroke-linecap="round"><g stroke="#16131f" stroke-width="5">${shape}</g><g stroke="${color}" stroke-width="2">${shape}</g></g>`;
  if (name.includes('blocked')) svg += '<g fill="none" stroke-linecap="round"><path d="M6 26 L26 6" stroke="#16131f" stroke-width="7"/><path d="M6 26 L26 6" stroke="#ff747a" stroke-width="3"/></g>';
  return {svg, pointer};
}
function chunk(key, value) {
  const data = Buffer.from(key + '\0' + value);
  const body = Buffer.concat([Buffer.from('tEXt'), data]);
  let crc = 0xffffffff;
  for (const byte of body) { crc ^= byte; for (let i=0;i<8;i++) crc = (crc >>> 1) ^ ((crc & 1) ? 0xedb88320 : 0); }
  const size = Buffer.alloc(4), sum = Buffer.alloc(4);
  size.writeUInt32BE(data.length); sum.writeUInt32BE((crc ^ 0xffffffff) >>> 0);
  return Buffer.concat([size, body, sum]);
}
(async () => {
  const names = JSON.parse(await fs.readFile(path.join(root, 'art/cursors/names.json')));
  const width = 352, height = Math.ceil(names.length / 11) * 32;
  const groups = names.map((name, i) => `<g transform="translate(${(i % 11) * 32} ${Math.floor(i / 11) * 32})">${glyph(name).svg}</g>`);
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}">${groups.join('')}</svg>`;
  await fs.writeFile(path.join(root, 'art/cursors/cursors.svg'), svg);
  const png = await sharp(Buffer.from(svg)).ensureAlpha().png().toBuffer();
  const output = Buffer.concat([png.subarray(0, -12), chunk('FrameSize', '32,32'), chunk('FrameAmount', String(names.length)), png.subarray(-12)]);
  await fs.writeFile(path.join(root, 'mods/sevenfall/art/cursors.png'), output);
  let yaml = '# Original RGBA vector cursors; no external palette or SHP files.\nCursors:\n\tsevenfall|art/cursors.png:\n';
  names.forEach((name, i) => { yaml += `\t\t${name}:\n\t\t\tStart: ${i}\n`; if (glyph(name).pointer) yaml += '\t\t\tX: -13\n\t\t\tY: -13\n'; });
  await fs.writeFile(path.join(root, 'mods/sevenfall/cursors.yaml'), yaml);
  console.log(`Exported ${names.length} original cursor states.`);
})();
