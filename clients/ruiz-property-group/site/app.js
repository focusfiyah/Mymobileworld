(function(){
  var form=document.getElementById('lead'),st=document.getElementById('status');
  form.addEventListener('submit',function(e){
    e.preventDefault();
    var bad=[].filter.call(form.querySelectorAll('[required]'),function(f){var v=f.value.trim();return !v||(f.type==='email'&&!/^\S+@\S+\.\S+$/.test(v));});
    [].forEach.call(form.elements,function(f){f.removeAttribute&&f.removeAttribute('aria-invalid');});
    if(bad.length){bad.forEach(function(f){f.setAttribute('aria-invalid','true')});st.className='status err';st.textContent='Please add your name and a valid email so we can reply.';bad[0].focus();return;}
    st.className='status ok';st.textContent='Thank you. This is a preview, so nothing was sent. When the site is live, this reaches Luigi directly.';
    form.reset();
  });
  /* the one scroll moment: the selling steps draw their line as you scroll */
  var fill=document.createElement('span');fill.className='fill';var steps=document.getElementById('steps');steps.appendChild(fill);
  if(window.gsap&&window.ScrollTrigger&&!window.matchMedia('(prefers-reduced-motion: reduce)').matches){
    gsap.registerPlugin(ScrollTrigger);
    gsap.fromTo(fill,{scaleY:0},{scaleY:1,ease:'none',scrollTrigger:{trigger:steps,start:'top 75%',end:'bottom 60%',scrub:true}});
  }
})();
