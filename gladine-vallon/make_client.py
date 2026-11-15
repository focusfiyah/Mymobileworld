"""Two-pass build of the professional client docx: placeholder contents, render, read heading pages, rebuild with page numbers."""
import re, subprocess, os, shutil
SRC='plan/business_plan_client.md'; TMP='plan/_client_build.md'
OUT='plan/Glad Personal Care Home - Business Plan.docx'
md=open(SRC).read()
heads=[h for h in re.findall(r'^## (.+)$', md, re.M) if h not in ('Confidentiality Statement','Contents')]
def build(pages):
    rows='| Section | Page |\n|---|---|\n'+'\n'.join(f'| {h} | {pages.get(h,"00")} |' for h in heads)
    open(TMP,'w').write(md.replace('[[TOC]]', rows))
    subprocess.run(['python3','build_client_docx.py',TMP],check=True,capture_output=True)
def render():
    d='/tmp/claude-0/-home-user/cf13e01e-92e0-50f2-be26-26de58a321fc/scratchpad/clientrender'; shutil.rmtree(d,ignore_errors=True); os.makedirs(d)
    shutil.copy(OUT,d+'/plan.docx'); subprocess.run(['soffice','--headless','--convert-to','pdf','--outdir',d,d+'/plan.docx'],capture_output=True,timeout=180)
    return d+'/plan.pdf'
build({}); pdf=render()
n=int(re.search(r'Pages:\s+(\d+)',subprocess.run(['pdfinfo',pdf],capture_output=True,text=True).stdout).group(1))
pages={}
for p in range(2,n+1):
    t=subprocess.run(['pdftotext','-f',str(p),'-l',str(p),'-layout',pdf,'-'],capture_output=True,text=True).stdout
    for h in heads:
        if h not in pages and re.search(r'^\s*'+re.escape(h)+r'\s*$', t, re.M): pages[h]=p
missing=[h for h in heads if h not in pages]; assert not missing, missing
build(pages); pdf=render()
print('pages',n,pages); os.remove(TMP)
