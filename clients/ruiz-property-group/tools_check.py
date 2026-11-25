import re,sys,os,glob
os.chdir('site');bad=[]
need={'we-buy-houses.html':['We Buy Houses. We Renovate. We Transform.','We buy houses','We renovate and restore','We fix and flip houses','Find the opportunity','Transform and resell','Our vision',"Let's make your property our next project",'Buy. Renovate. Transform. Create value.'],
      'property-management.html':['Your Property, Professionally Managed','Residential property management','Tenant placement and leasing','Rent collection and financial management','Maintenance and repairs','Property inspections','Tenant relations','Lease administration','Our mission','Let us manage your property']}
for f in glob.glob('*.html'):
    s=open(f).read()
    for m in re.finditer(r'(?:href|src)="([^"#:]+?)(#[^"]*)?"',s):
        p=m.group(1)
        if p.startswith('http') or p.startswith('//'): continue
        if not os.path.exists(p): bad.append((f,p))
    for t in need.get(f,[]):
        if t.replace("'","&#39;") not in s and t not in s: bad.append((f,'missing: '+t))
print('PAGES_OK' if not bad else bad)
