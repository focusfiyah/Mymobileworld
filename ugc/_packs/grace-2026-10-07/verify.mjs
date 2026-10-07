// Checks for the 2026-10-07 Grace 5-product script pack. Usage: node verify.mjs <scripts|banned|readability|gate|readme>
import fs from 'node:fs'; import path from 'node:path'; import {execFileSync} from 'node:child_process';
const UGC = path.resolve(path.dirname(new URL(import.meta.url).pathname), '../..');
const JOBS = ['skin1004-centella-kit','ilso-blackhead-bundle','emerald-tennis-necklace','seamless-bras-4pack','shapewear-pants-4pack'];
const spoken = () => JOBS.flatMap(j => [1,2,3].map(n => [j+'/s'+n, fs.readFileSync(path.join(UGC,j,'spoken',`s${n}.txt`),'utf8').trim()]));
const fail = m => { console.log('FAIL ' + m); process.exit(1); };
const mode = process.argv[2];
if (mode === 'scripts') {
  const s = spoken(); if (s.length !== 15) fail('count ' + s.length);
  for (const [k,t] of s) if (!t.endsWith("It's in the orange cart.")) fail(k + ' closer');
  console.log('SCRIPTS_OK 15');
} else if (mode === 'banned') {
  const bad = [/[–—]/, / - /, /heads up/i, /obsessed/i, /so cute/i, /you need this/i, /order it now/i, /\$\s?\d/];
  // positive control: the checker must catch a planted phrase
  if (!bad.some(r => r.test('just order it now'))) fail('control');
  const files = JOBS.flatMap(j => [path.join(j,'scripts.md'), ...[1,2,3].map(n => path.join(j,'spoken',`s${n}.txt`))]);
  for (const f of files) { const t = fs.readFileSync(path.join(UGC,f),'utf8'); for (const r of bad) if (r.test(t)) fail(f + ' ' + r); }
  console.log('BANNED_CLEAN ' + files.length);
} else if (mode === 'readability') {
  for (const j of JOBS) { const t = fs.readFileSync(path.join(UGC,j,'readability.txt'),'utf8');
    const g = [...t.matchAll(/Grade level \(Flesch-Kincaid\): ([\d.]+)/g)].map(m => +m[1]);
    if (g.length !== 3 || g.some(x => x > 6)) fail(j + ' grades ' + g); }
  for (const [k,t] of spoken()) { const w = t.split(/\s+/).length; if (w > 115) fail(k + ' words ' + w); }
  console.log('READABILITY_OK');
} else if (mode === 'gate') {
  for (const j of JOBS) { let out = '';
    try { out = execFileSync('python3', ['grace/gate.py', 'ugc/'+j], {cwd: path.join(UGC,'..'), encoding:'utf8', stdio:['ignore','pipe','pipe']}); }
    catch (e) { out = (e.stdout||'') + (e.stderr||''); }
    const lines = out.split('\n').filter(l => l.trim().startsWith('- '));
    if (lines.length !== 1 || !/viral_board/.test(lines[0])) fail(j + ' gate: ' + out.trim()); }
  console.log('GATE_8_OF_9_ALL (only viral_board open)');
} else if (mode === 'readme') {
  for (const j of JOBS) { const t = fs.readFileSync(path.join(UGC,j,'README.md'),'utf8');
    if (!/^Status: DONE \(\$0\)/m.test(t) || !/drive\.google\.com\/drive\/folders\//.test(t)) fail(j); }
  console.log('README_OK 5');
} else fail('mode');
