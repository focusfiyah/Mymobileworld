"""Styled client docx from plan/business_plan_clean.md: cover page, brand colours, styled tables, page numbers."""
import subprocess, copy
from docx import Document
from docx.shared import Pt, RGBColor, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
TEAL=RGBColor(0x1F,0x5F,0x56); INK=RGBColor(0x22,0x2B,0x28); MUTED=RGBColor(0x5B,0x67,0x62)
import sys,re
OUT='plan/CLEAN - Glad Personal Care Home Business Plan.docx'
SRC=sys.argv[1] if len(sys.argv)>1 else 'plan/_client_build.md'
ref='plan/_ref.docx'
open(ref,'wb').write(subprocess.run(['pandoc','--print-default-data-file','reference.docx'],capture_output=True,check=True).stdout)
d=Document(ref)
S={st.name:st for st in d.styles}
def font(st,name,size,color=INK,bold=None):
    st.font.name=name; st.font.size=Pt(size); st.font.color.rgb=color
    if bold is not None: st.font.bold=bold
    rpr=st.element.get_or_add_rPr(); rf=rpr.find(qn('w:rFonts'))
    if rf is None: rf=OxmlElement('w:rFonts'); rpr.append(rf)
    for k in ('w:ascii','w:hAnsi','w:cs','w:eastAsia'): rf.set(qn(k),name)
for n in ('Normal','Body Text','First Paragraph','Compact'):
    if n in [s.name for s in d.styles]:
        st=S[n]; font(st,'Calibri',11); st.paragraph_format.space_after=Pt(6); st.paragraph_format.line_spacing=1.15
font(S['Heading 1'],'Georgia',20,TEAL,True); S['Heading 1'].paragraph_format.space_before=Pt(18); S['Heading 1'].paragraph_format.space_after=Pt(8)
font(S['Heading 2'],'Georgia',17,TEAL,True); S['Heading 2'].paragraph_format.space_before=Pt(20); S['Heading 2'].paragraph_format.space_after=Pt(6)
S['Heading 2'].paragraph_format.page_break_before=False
font(S['Heading 3'],'Calibri',12.5,INK,True); S['Heading 3'].paragraph_format.space_before=Pt(12)
d.save(ref)
subprocess.run(['pandoc',SRC,'-o',OUT,'--reference-doc',ref],check=True)
d=Document(OUT)
sec=d.sections[0]; sec.left_margin=sec.right_margin=Inches(1); sec.top_margin=sec.bottom_margin=Inches(0.9)
def shade(cell,hexc):
    tcPr=cell._tc.get_or_add_tcPr(); sh=OxmlElement('w:shd'); sh.set(qn('w:val'),'clear'); sh.set(qn('w:color'),'auto'); sh.set(qn('w:fill'),hexc); tcPr.append(sh)
def borders(tbl):
    tblPr=tbl._tbl.tblPr; b=OxmlElement('w:tblBorders')
    for e in ('top','bottom','insideH'):
        x=OxmlElement(f'w:{e}'); x.set(qn('w:val'),'single'); x.set(qn('w:sz'),'4'); x.set(qn('w:color'),'C9D3CF'); b.append(x)
    for e in ('left','right','insideV'):
        x=OxmlElement(f'w:{e}'); x.set(qn('w:val'),'nil'); b.append(x)
    tblPr.append(b)
for t in d.tables:
    for k,row in enumerate(t.rows):
        trPr=row._tr.get_or_add_trPr(); cs=OxmlElement('w:cantSplit'); trPr.append(cs)
        if k==0: th=OxmlElement('w:tblHeader'); trPr.append(th)
    borders(t); t.alignment=WD_TABLE_ALIGNMENT.CENTER
    hdr=t.rows[0]; empty=all(not c.text.strip() for c in hdr.cells)
    if t.rows[0].cells[0].text.strip()=='Section':
        for row in t.rows:
            for c in row.cells:
                for p in c.paragraphs:
                    p.paragraph_format.space_after=Pt(4); p.paragraph_format.space_before=Pt(4)
                    for r in p.runs: r.font.size=Pt(11); r.font.color.rgb=INK
            for p in row.cells[1].paragraphs: p.alignment=WD_ALIGN_PARAGRAPH.RIGHT
        t.rows[0]._tr.getparent().remove(t.rows[0]._tr)
        continue
    if t.rows[0].cells[0].text.strip() in ('Business Name','Startup budget'):
        for row in t.rows:
            shade(row.cells[0],'E4EEEA')
            for p in row.cells[0].paragraphs:
                for r in p.runs: r.font.color.rgb=TEAL
            for c in row.cells:
                for p in c.paragraphs:
                    p.paragraph_format.space_after=Pt(3); p.paragraph_format.space_before=Pt(3)
                    for r in p.runs: r.font.size=Pt(10.5)
        continue
    for i,row in enumerate(t.rows):
        for c in row.cells:
            for p in c.paragraphs:
                p.paragraph_format.space_after=Pt(2); p.paragraph_format.space_before=Pt(2)
                for r in p.runs: r.font.size=Pt(10)
            if i==0 and not empty:
                shade(c,'1F5F56')
                for p in c.paragraphs:
                    for r in p.runs: r.font.color.rgb=RGBColor(0xFF,0xFF,0xFF); r.font.bold=True
            elif i%2==0: shade(c,'F1F5F3')
    if empty: hdr._tr.getparent().remove(hdr._tr)
for p in d.paragraphs:
    if p.style.name.startswith('Heading') and p.text.strip() in ('Contents','1. Executive Summary'):
        p.paragraph_format.page_break_before=True
# cover page
body=d.element.body; first=d.paragraphs[0]
def para_before(text,size,color,bold=False,font_name='Georgia',space_after=6,align=WD_ALIGN_PARAGRAPH.LEFT):
    p=first.insert_paragraph_before(); p.alignment=align
    r=p.add_run(text); r.font.size=Pt(size); r.font.color.rgb=color; r.font.bold=bold; r.font.name=font_name
    r._element.rPr.rFonts.set(qn('w:eastAsia'),font_name); p.paragraph_format.space_after=Pt(space_after); return p
for _ in range(6): para_before('',12,INK)
para_before('BUSINESS PLAN',11,TEAL,True,'Calibri',4)
tp=para_before('Glad Personal Care Home',34,INK,True,'Georgia',14)
pPr=tp._p.get_or_add_pPr(); bd=OxmlElement('w:pBdr'); bt=OxmlElement('w:bottom'); bt.set(qn('w:val'),'single'); bt.set(qn('w:sz'),'18'); bt.set(qn('w:space'),'10'); bt.set(qn('w:color'),'1F5F56'); bd.append(bt); pPr.append(bd)
para_before('A small, private-room personal care home for seniors in Pennsylvania',14,MUTED,False,'Georgia',36)
para_before('Prepared by Gladine Vallon, Owner',11,INK,False,'Calibri',2)
para_before('[Company Name] LLC  ·  [City], Pennsylvania',11,INK,False,'Calibri',2)
pb=para_before('November 2026',11,MUTED,False,'Calibri',2)
pb.add_run().add_break(WD_BREAK.PAGE)
# footer page numbers
fp=sec.footer.paragraphs[0]; fp.alignment=WD_ALIGN_PARAGRAPH.CENTER
r=fp.add_run('Glad Personal Care Home  ·  Business Plan  ·  Confidential  ·  Page '); r.font.size=Pt(9); r.font.color.rgb=MUTED
r2=fp.add_run(); 
for tag,txt in (('begin',None),(None,'PAGE'),('end',None)):
    if tag: e=OxmlElement('w:fldChar'); e.set(qn('w:fldCharType'),tag); r2._r.append(e)
    else: e=OxmlElement('w:instrText'); e.set(qn('xml:space'),'preserve'); e.text=txt; r2._r.append(e)
r2.font.size=Pt(9); r2.font.color.rgb=MUTED
sec.different_first_page_header_footer=True
d.save(OUT); import os; os.remove(ref); print('saved', OUT)
