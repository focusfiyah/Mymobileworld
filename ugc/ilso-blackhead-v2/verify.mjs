// Checks for ilso blackhead v2 scripts (2026-10-19). Usage: node verify.mjs <scripts|banned|readability|hooks|gate|readme>
import fs from 'node:fs'; import path from 'node:path'; import {execFileSync} from 'node:child_process';
const JOB = path.dirname(new URL(import.meta.url).pathname); const ROOT = path.resolve(JOB, '../..');
const fail = m => { console.log('FAIL ' + m); process.exit(1); };
const spoken = () => [1,2,3].map(n => [`s${n}`, fs.readFileSync(path.join(JOB,'spoken',`s${n}.txt`),'utf8').trim()]);
const mode = process.argv[2];
if (mode === 'scripts') {
  for (const [k,t] of spoken()) if (!t.endsWith("It's in the orange cart.")) fail(k + ' closer');
  console.log('SCRIPTS_OK 3');
} else if (mode === 'banned') {
  const bad = [/[–—]/, / - /, /heads up/i, /obsessed/i, /so cute/i, /you need this/i, /order (it )?now/i, /\$\s?\d/, /\d+\s?(dollars|bucks|cents)/i,
    /\b(on sale|% off|percent off)\b/i, /label says/i, /reviewers?/i, /game.?changer/i, /miracle/i, /selling out/i, /\b(cures?|kills?|fixes)\b/i];
  if (!bad.some(r => r.test('just order it now')) || !bad.some(r => r.test('the label says'))) fail('control');
  const files = ['scripts.md', ...[1,2,3].map(n => `spoken/s${n}.txt`)];
  for (const f of files) { const t = fs.readFileSync(path.join(JOB,f),'utf8'); for (const r of bad) if (r.test(t)) fail(f + ' ' + r); }
  console.log('BANNED_CLEAN ' + files.length);
} else if (mode === 'readability') {
  const t = fs.readFileSync(path.join(JOB,'readability.txt'),'utf8');
  const g = [...t.matchAll(/Grade level \(Flesch-Kincaid\):\s*([\d.]+)/g)].map(m => +m[1]);
  if (g.length !== 3 || g.some(x => x > 6)) fail('grades ' + g);
  for (const [k,t2] of spoken()) { const w = t2.split(/\s+/).length; if (w < 70 || w > 115) fail(k + ' words ' + w); }
  console.log('READABILITY_OK ' + g.join(','));
} else if (mode === 'hooks') {
  const lib = JSON.parse(fs.readFileSync(path.join(ROOT,'grace/hooks/hooks.json'),'utf8')).hooks;
  const byId = Object.fromEntries(lib.map(h => [h.id, h.hook]));
  const v1 = ['H094','H096','H095','H018','H011','H077','H025','H029','H024'];
  const used = JSON.parse(fs.readFileSync(path.join(JOB,'hooks.json'),'utf8')); // [{script, id, said}]
  const norm = s => s.toLowerCase().replace(/[’']/g,"'").replace(/[^a-z0-9' ]/g,'').replace(/\s+/g,' ').trim();
  const ids = used.map(u => u.id); if (new Set(ids).size !== ids.length) fail('id repeated');
  if (used.length !== 9) fail('need 9 hooks, got ' + used.length);
  for (const u of used) {
    if (v1.includes(u.id)) fail(u.id + ' used in v1');
    if (!byId[u.id]) fail(u.id + ' not in library');
    const pat = norm(byId[u.id]).split(/_+|\[[^\]]*\]/).map(s => s.trim()).filter(Boolean);
    let s = norm(u.said); for (const p of pat) { const i = s.indexOf(p); if (i < 0) fail(u.id + ' not word for word: ' + p); s = s.slice(i + p.length); }
  }
  const sp = spoken(); for (const u of used.filter(u => u.main)) { const t = norm(sp[u.script-1][1]); if (!t.startsWith(norm(u.said))) fail('s'+u.script+' does not open with ' + u.id); }
  console.log('HOOKS_OK 9');
} else if (mode === 'gate') {
  let out = '', code = 0;
  try { out = execFileSync('python3', ['grace/gate.py', 'ugc/ilso-blackhead-v2'], {cwd: ROOT, encoding:'utf8', stdio:['ignore','pipe','pipe']}); }
  catch (e) { code = 1; out = (e.stdout||'') + (e.stderr||''); }
  if (code) fail(out.trim()); console.log('GATE_PASS ' + out.trim().split('\n').pop());
} else if (mode === 'readme') {
  const t = fs.readFileSync(path.join(JOB,'README.md'),'utf8');
  if (!/^Status: DONE \(\$0\)/m.test(t) || !/drive\.google\.com\/drive\/folders\//.test(t) || !/claude\.ai\//.test(t)) fail('readme');
  console.log('README_OK');
} else fail('mode');
