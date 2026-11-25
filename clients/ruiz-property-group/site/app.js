(function(){
  var root=document.documentElement;root.classList.add('js');
  var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  /* mobile menu: Transitions.dev dropdown */
  var mb=document.getElementById('menu-btn'),mn=document.getElementById('menu');
  function setMenu(open){
    if(!mb||!mn)return;
    mb.setAttribute('aria-expanded',open?'true':'false');
    if(open){mn.hidden=false;void mn.offsetWidth;mn.classList.remove('is-closing');mn.classList.add('is-open');}
    else{mn.classList.remove('is-open');mn.classList.add('is-closing');setTimeout(function(){if(mb.getAttribute('aria-expanded')==='false'){mn.hidden=true;mn.classList.remove('is-closing');}},reduce?0:160);}
  }
  if(mb&&mn){
    mb.addEventListener('click',function(){setMenu(mb.getAttribute('aria-expanded')!=='true');});
    document.addEventListener('keydown',function(e){if(e.key==='Escape'&&mb.getAttribute('aria-expanded')==='true'){setMenu(false);mb.focus();}});
    document.addEventListener('click',function(e){if(mb.getAttribute('aria-expanded')==='true'&&!mn.contains(e.target)&&!mb.contains(e.target))setMenu(false);});
    [].forEach.call(mn.querySelectorAll('a'),function(a){a.addEventListener('click',function(){setMenu(false);});});
  }
  /* hero quick form hands over to the contact form */
  var q=document.getElementById('quick');
  if(q)q.addEventListener('submit',function(e){
    e.preventDefault();
    document.getElementById('addr').value=document.getElementById('qaddr').value;
    document.getElementById('phone').value=document.getElementById('qphone').value;
    document.getElementById('need').value='Sell my property';
    document.getElementById('contact').scrollIntoView({behavior:reduce?'auto':'smooth'});
    setTimeout(function(){document.getElementById('name').focus({preventScroll:true})},500);
  });
  /* FAQ: Transitions.dev accordion, one open at a time */
  var accs=[].slice.call(document.querySelectorAll('.t-acc'));
  accs.forEach(function(acc){
    var h=acc.querySelector('.t-acc-head');
    h.addEventListener('click',function(){
      var open=acc.getAttribute('data-open')==='true';
      accs.forEach(function(o){o.setAttribute('data-open','false');o.querySelector('.t-acc-head').setAttribute('aria-expanded','false');});
      if(!open){acc.setAttribute('data-open','true');h.setAttribute('aria-expanded','true');}
    });
  });
  /* lead form with success check */
  var form=document.getElementById('lead'),st=document.getElementById('status');
  if(form)form.addEventListener('submit',function(e){
    e.preventDefault();
    var bad=[].filter.call(form.querySelectorAll('[required]'),function(f){var v=f.value.trim();return !v||(f.type==='email'&&!/^\S+@\S+\.\S+$/.test(v));});
    [].forEach.call(form.elements,function(f){f.removeAttribute&&f.removeAttribute('aria-invalid');});
    if(bad.length){bad.forEach(function(f){f.setAttribute('aria-invalid','true')});st.className='status err';st.textContent='Please add your name and a valid email so we can reply.';bad[0].focus();return;}
    form.reset();form.classList.add('sent');
    var c=document.getElementById('check');if(c){c.removeAttribute('data-state');void c.offsetWidth;c.setAttribute('data-state','in');}
    var d=form.querySelector('.done');if(d)d.focus({preventScroll:true});
  });
  /* the one scroll moment: the steps draw their line as you scroll */
  var steps=document.getElementById('steps');
  if(steps){var fill=document.createElement('span');fill.className='fill';steps.appendChild(fill);
    if(window.gsap&&window.ScrollTrigger&&!reduce){
      gsap.registerPlugin(ScrollTrigger);
      gsap.fromTo(fill,{scaleY:0},{scaleY:1,ease:'none',scrollTrigger:{trigger:steps,start:'top 75%',end:'bottom 60%',scrub:true}});
    }
  }
})();
