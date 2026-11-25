const {chromium}=require('playwright');const path=require('path');
(async()=>{const b=await chromium.launch();const bad=[];
for(const pg of ['index.html','we-buy-houses.html','property-management.html']){
 for(const [w,h] of [[390,844],[1440,900]]){
  const p=await b.newPage({viewport:{width:w,height:h}});const errs=[];
  p.on('console',m=>m.type()=='error'&&errs.push(m.text()));p.on('pageerror',e=>errs.push(e.message));p.on('requestfailed',r=>errs.push('fail '+r.url()));
  await p.goto('file://'+path.resolve('site/'+pg));await p.waitForTimeout(900);
  await p.evaluate(async()=>{for(let y=0;y<document.body.scrollHeight;y+=600){scrollTo(0,y);await new Promise(r=>setTimeout(r,200))}scrollTo(0,0)});await p.waitForTimeout(800);
  const r=await p.evaluate(()=>({sw:document.documentElement.scrollWidth,iw:innerWidth,noalt:[...document.images].filter(i=>!(i.getAttribute('alt')||'').length).length,broken:[...document.images].filter(i=>!(i.complete&&i.naturalWidth>0)).length,nolabel:[...document.querySelectorAll('input,select,textarea')].filter(e=>!document.querySelector('label[for="'+e.id+'"]')).length,h1:document.querySelectorAll('h1').length}));
  if(r.sw>r.iw||r.noalt||r.broken||r.nolabel||r.h1!=1||errs.length) bad.push([pg,w,r,errs]);
  if(w==1440||pg!='index.html') await p.screenshot({path:'/tmp/ruizsite/pg_'+pg.replace('.html','')+'_'+w+'.png',fullPage:true});
  await p.close();}}
console.log(bad.length?JSON.stringify(bad,null,1):'PAGES_BROWSER_OK');await b.close()})()
