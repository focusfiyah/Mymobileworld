"""Adds the S1 Flow kit card (Save + Copy buttons, downloads capability) to review/index.html. Run after build_review.py."""
import html
from pathlib import Path
new = Path("flow/S1_flow_new.txt").read_text().strip(); edit = Path("flow/S1_flow_edit.txt").read_text().strip()
e = html.escape
card = f"""<section id="flowkit"><h2>Flow kit: S1 (palm right under the nozzle)</h2>
<p class="muted">Two ways. <b>A, new take:</b> Flow &gt; new project &gt; Video &gt; Gemini Omni Flash &gt; 9:16 &gt; 4 s. Upload as Ingredients in this order: 1 the S1 still (as the start frame if Flow offers one), 2 the label close-up. Paste prompt A. <b>B, edit the clip we have:</b> save the Kling clip, open it in Flow's edit, paste prompt B. Download at 1080 and send it back here.</p>
<div class="refs">
<figure><img src="img/flow_1.jpg" alt="Image 1, S1 still"><figcaption>1. S1 still (first frame)</figcaption><button class="save" data-src="flow/1_S1_still.png" data-name="1_S1_still.png">Save image 1</button></figure>
<figure><img src="img/flow_2.jpg" alt="Image 2, cleanser label"><figcaption>2. Real label close-up</figcaption><button class="save" data-src="flow/2_cleanser_label.png" data-name="2_cleanser_label.png">Save image 2</button></figure>
<figure><video controls playsinline muted preload="metadata" src="flow/S1_kling_clip_to_edit.mp4" style="width:100%;border-radius:8px;background:#000"></video><figcaption>Clip to edit (Kling S1)</figcaption><button class="save" data-src="flow/S1_kling_clip_to_edit.mp4" data-name="S1_clip_to_edit.mp4">Save clip</button></figure>
</div>
<div class="prompt"><h3>Prompt A (new take)</h3><p class="pr" id="pA">{e(new)}</p><button class="copy" data-for="pA">Copy prompt A</button></div>
<div class="prompt"><h3>Prompt B (edit the clip)</h3><p class="pr" id="pB">{e(edit)}</p><button class="copy" data-for="pB">Copy prompt B</button></div>
<p class="muted" id="kitmsg" aria-live="polite"></p>
</section>
<style>
#flowkit button{{font:600 .9rem var(--body);padding:8px 12px;border-radius:8px;border:1px solid var(--blue);background:var(--card);color:var(--blue);cursor:pointer;justify-self:start}}
#flowkit button:focus-visible{{outline:2px solid var(--blue);outline-offset:2px}}
#flowkit .prompt{{display:grid;gap:8px;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px}} #flowkit h3{{margin:0;font-size:1rem}}
#flowkit .pr{{color:var(--fg);font-size:.92rem}}
</style>
<script>
(function(){{
  var msg=document.getElementById('kitmsg');
  document.querySelectorAll('#flowkit .copy').forEach(function(b){{
    b.addEventListener('click',function(){{
      var el=document.getElementById(b.dataset.for), t=el.textContent;
      function sel(){{var r=document.createRange();r.selectNodeContents(el);var s=getSelection();s.removeAllRanges();s.addRange(r);msg.textContent='Selected: tap Copy in the menu.';}}
      try{{navigator.clipboard.writeText(t).then(function(){{msg.textContent='Prompt copied.';}},sel);}}catch(x){{sel();}}
    }});
  }});
  var saves=document.querySelectorAll('#flowkit .save');
  var dl=null;
  if(window.claude&&claude.use){{claude.use('downloads').then(function(d){{dl=d;if(!d)saves.forEach(function(b){{b.hidden=true;}});}});}} else saves.forEach(function(b){{b.hidden=true;}});
  saves.forEach(function(b){{
    b.addEventListener('click',function(){{
      if(!dl){{msg.textContent='Saving is not available in this view.';return;}}
      fetch(b.dataset.src).then(function(r){{return r.blob();}}).then(function(blob){{
        return dl.save({{filename:b.dataset.name,data:blob}});
      }}).then(function(){{msg.textContent='Saved '+b.dataset.name+'.';}},function(err){{
        msg.textContent=(err&&err.code==='declined')?'Save cancelled.':'Could not save '+b.dataset.name+'.';
      }});
    }});
  }});
}})();
</script>
"""
p = Path("review/index.html"); s = p.read_text()
anchor = "<section><h2>Cut v3 vs v2"
assert anchor in s
s = s.replace(anchor, card + anchor, 1); p.write_text(s); print("kit ok")
