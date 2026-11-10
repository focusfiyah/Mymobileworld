// Gate checks for the PA assisted living analysis page. Usage: node tools_check.mjs <check>
import fs from 'fs';
const page = fs.existsSync('review/index.html') ? fs.readFileSync('review/index.html','utf8') : '';
const c = process.argv[2]; let ok = false; const fail = m => { console.log('FAIL: '+m); process.exit(1); };
if (c === 'sections') {
  const need = ['id="verdict"','id="license"','id="staffing"','id="money"','id="gaps"','id="grant"','id="roadmap"','id="client-checklist"','id="questions"'];
  const miss = need.filter(n => !page.includes(n)); if (miss.length) fail('missing '+miss.join(',')); ok = true;
} else if (c === 'sources') {
  const n = new Set((page.match(/href="https?:\/\/[^"]+"/g)||[])).size; if (n < 12) fail('only '+n+' source links'); console.log('links', n); ok = true;
} else if (c === 'math') {
  const m = JSON.parse(fs.readFileSync('research/staffing_math.json','utf8'));
  const annual = (m.lpn_hr + m.cna_hr) * 8760 * (1 + m.burden);
  for (const [beds, shown] of Object.entries(m.per_resident_month_shown)) {
    const calc = annual / Number(beds) / 12; if (Math.abs(calc - shown) > 50) fail(`beds ${beds}: shown ${shown} calc ${calc.toFixed(0)}`);
  }
  if (Math.abs(annual - m.annual_shown) > 500) fail('annual mismatch '+annual.toFixed(0)); if (!page.includes(m.annual_label)) fail('annual label not on page'); ok = true;
} else if (c === 'nobanned') {
  const txt = page.replace(/<[^>]+>/g,' ');
  const bad = ['—','delve','leverage','seamless','robust','In conclusion','not only'].filter(w => txt.includes(w)); if (bad.length) fail('banned: '+bad.join(',')); ok = true;
} else if (c === 'readme') {
  const r = fs.readFileSync('README.md','utf8'); if (!/claude\.ai\/code\/artifact\/|claude\.ai\/artifact\//.test(r)) fail('no artifact link'); ok = true;
}
if (ok) console.log('GATE_PASS '+c); else fail('unknown check');
