// Script checks for the Your Wish book job: node check.mjs <what>
import fs from 'fs';
const what=process.argv[2];const s=fs.existsSync('scripts.md')?fs.readFileSync('scripts.md','utf8'):'';
const fail=m=>{console.log('FAIL '+m);process.exit(1)};
const vids=s.split(/^## Script /m).slice(1);
if(what==='structure'){
  if(vids.length!==3) fail('expected 3 scripts, got '+vids.length);
  for(const v of vids){for(const k of ['HOOK','BODY','CTA']) if(!new RegExp('\\*\\*'+k).test(v)) fail('missing '+k);
    if(!/It's in the orange cart\./.test(v)) fail('no orange cart close');}
  console.log('STRUCTURE OK');}
if(what==='hooks'){
  let lib=JSON.parse(fs.readFileSync('../../grace/hooks/hooks.json','utf8'));lib=Array.isArray(lib)?lib:lib.hooks;const ids=new Set();
  for(const v of vids){const m=v.match(/\(H(\d{3})\)/g)||[];if(m.length<3) fail('need main + 2 alt hook ids per script');
    for(const t of m){const id=t.slice(1,5);if(ids.has(id)) fail('hook reused '+id);ids.add(id);
      const h=lib.find(x=>x.id===id);if(!h) fail('unknown '+id);
      const re=new RegExp('^'+h.hook.replace(/[.*+?^${}()|[\]\\]/g,'\\$&').replace(/__/g,'.+?')+'[.?!]?$','i');
      const line=(v.split('\n').find(l=>l.includes(t))||'').replace(/^.*?"/,'').replace(/".*$/,'');
      if(!re.test(line.trim())) fail(id+' not word for word: '+line);}}
  console.log('HOOKS VERBATIM OK '+ids.size);}
if(what==='banned'){
  const spoken=s.toLowerCase();
  for(const b of [/\$\s?\d/,/\b\d+\s?(%|percent|dollars?)\b/,/reviewer/,/the label says/,/order (it )?now/,/heads up/,/obsessed/,/game.?changer/,/you need this/,/miracle/,/[–—]/,/selling out/,/guarantee/]) if(b.test(spoken)) fail('banned '+b);
  console.log('BANNED CLEAN');}
