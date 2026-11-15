"""Build the client-facing clean plan from plan/business_plan.md (no review notes). Rerun after every plan change."""
import re
s = open('plan/business_plan.md').read()
# drop header lines up to first ---
s = s[s.index('\n---\n')+5:]
R = [
 (r'\*\*Business Name:\*\* Glad Personal Care Home \(working name\) \*\*\[UPDATED:[^\]]*\]\*\*', '**Business Name:** Glad Personal Care Home'),
 (r'\*\*Business Type:\*\* Personal Care Home \(55 Pa\. Code Chapter 2600\), licensed by the PA Department of Human Services \*\*\[CHANGE:[^\]]*\]\*\*', '**Business Type:** Personal Care Home (55 Pa. Code Chapter 2600), licensed by the Pennsylvania Department of Human Services'),
 (r'\*\*Owner:\*\* Gladine Vallon, \[company name\] LLC', '**Owner:** Gladine Vallon, [Company Name] LLC'),
 (r'\*\*What we are asking for \[ADDED\]:\*\*', '**Funding needed:**'),
 (r'about \$1\.04 million to buy and prepare the property and open \(section 15\), or as little as about \$297,000 if the building is leased \(section 14\), from Gladine\'s own money \(about 20%\)', "about $1.04 million to buy and prepare the property and open, or about $297,000 if the building is leased (section 14), from the owner's own funds (about 20%)"),
]
for a,b in R:
    n = len(re.findall(a, s)); assert n == 1, (a[:50], n); s = re.sub(a, lambda m: b, s)
# staffing critique paragraph -> neutral explanation
a = s[s.index('**[CHANGE]** Gladine'):s.index('### Staffing model at 10 residents')]
s = s.replace(a, "Pennsylvania requires at least 1 hour of direct care per resident each day for residents who can walk, with at least one staff member 21 or older on site at all times. Our staffing goes well beyond that minimum. Medication-trained aides provide hands-on care around the clock, and a registered nurse oversees medications and resident health. This keeps a nurse involved in every resident's care while keeping the monthly rate affordable for families.\n\n")
# break-even first-plan row, choice line, remaining tags
s = re.sub(r"\| Gladine's first staffing plan[^\n]*\n", '', s)
s = s.replace("**Our choice: a Personal Care Home (chosen 2026-11-15).**", "**Why a Personal Care Home:**")
s = s.replace("it allows every service on Gladine's list,", "it allows every service the home offers,")
s = s.replace("**What Glad Personal Care Home provides (Gladine's list, 2026-11-15):**", "**What Glad Personal Care Home provides:**")
s = s.replace("What this means: a 10-bed home pays for itself only if Gladine runs it herself and keeps it nearly full.", "What this means: the 10-bed home covers its costs once it is close to full, with the owner serving as administrator.")
s = s.replace("Gladine is not paid a salary in years 1 and 2; she earns what the home makes.", "The owner takes no salary in years 1 and 2 and earns what the home makes.")
s = s.replace("when Gladine is away", "when the administrator is away")
s = s.replace("| Gladine's own money (20%) |", "| Owner's own funds (20%) |")
s = s.replace("| Administrator | Gladine |", "| Administrator | Gladine Vallon (owner) |")
s = s.replace("*To fill in once the city is chosen.*", "*To be completed once the location is chosen.*")
s = s.replace("*All estimates until she has the property and real quotes.*", "*Figures are estimates and will be finalized once the property is chosen and quotes are in.*")
s = s.replace("[Add her background: years in care, licenses such as RN, LPN or CNA, and any management experience. Lenders weigh this heavily.]", "[Background: years in care, licenses (RN, LPN or CNA) and management experience.]")
s = re.sub(r' ?\*\*\[(ADDED|UPDATED|CHANGE)[^\]]*\]\*\*', '', s)
s = re.sub(r' \[(ADDED|UPDATED)[^\]]*\]', '', s)
s = s.replace('(*estimate*)', '').replace('*estimate* ', '').replace('*estimates*', 'estimates').replace('*estimated* ', 'estimated ').replace('(*estimate*)', '')
s = s.replace('## Sources', '## References')
s = s.replace('before she buys it', 'before purchase')
s = s.replace('Her accountant should make that call based on her income.', "The owner's accountant will advise on this based on income.")
facts = re.search(r'\*\*Business Name:\*\*.*?\*\*Location:\*\*[^\n]*', s, re.S).group(0)
rows = [l.split(':** ',1) for l in facts.split('\n') if l.strip()]
tbl = '| | |\n|---|---|\n' + '\n'.join(f"| **{k.strip('*')}** | {v} |" for k,v in rows)
s = s.replace(facts, tbl)
s = s.replace('The $1,040,000 above assumes buying a $650,000 property. The property is 63% of the total, so the building decision matters most.', 'The $1,040,000 above assumes buying a $650,000 property. The property is 63% of the total, so the choice of building has the biggest effect on the startup cost.')
s = s.replace('\n---\n', '\n')
assert not re.search(r'\[(ADDED|UPDATED|CHANGE)', s) and 'Gladine\'s' not in s and 'draft' not in s.lower(), 'leftover'
open('plan/business_plan_clean.md','w').write(s)
print(len(s.split()), 'words')
