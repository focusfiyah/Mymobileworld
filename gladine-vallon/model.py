"""Financial model for Gladine Vallon's PA care home. All inputs below; outputs -> research/model.json.
Sources: wages PA L&I May 2025 OEWS (RN 45.20, LPN 31.70, CNA 21.14); PA assisted living median $6,480 (CareScout 2025).
Everything marked EST is an estimate to replace with her real quotes."""
import json
B = 1.25  # payroll burden (taxes, workers comp, PTO) EST
RN, LPN, CNA, COOK = 45.20, 31.70, 21.14, 18.00  # COOK EST
H = 8760
def staff(lines):  # lines: (label, hours/yr, rate) or (label, salary)
    w = sum(l[1]*l[2] if len(l)==3 else l[1] for l in lines); return w, w*B
SC = {
 "A": dict(name="Plan as written (ALR, 10 beds, 1 LPN + 1 CNA every shift, paid administrator)", beds=10, rate=6480,
   staff=[("LPN 24/7",H,LPN),("CNA 24/7",H,CNA),("Administrator",65000),("Cook/housekeeper full time",2080,COOK)],
   fixed_month=dict(property=6500, utilities=2500, insurance=2000, other=2500)),
 "B": dict(name="Lean personal care home, 10 beds, Gladine is the administrator", beds=10, rate=5500,
   staff=[("Med-trained aide 24/7",H,CNA),("Second aide 8 h/day",2920,CNA),("RN consultant 10 h/week",520,RN),("Cook/housekeeper 20 h/week",1040,COOK)],
   fixed_month=dict(property=6500, utilities=2500, insurance=2000, other=2500)),
 "C": dict(name="Lean, after expansion to 20 beds, paid administrator", beds=20, rate=5500,
   staff=[("Two aides 24/7",2*H,CNA),("Third aide 8 h/day",2920,CNA),("RN 20 h/week",1040,RN),("Administrator",65000),("Cook full time",2080,COOK),("Housekeeper full time",2080,COOK)],
   fixed_month=dict(property=8500, utilities=4000, insurance=3500, other=3500)),
}
VAR = 12*30.4 + 100  # food $12/day + supplies/activities $100 per resident per month EST
out = {}
for k,s in SC.items():
    w, loaded = staff(s["staff"]); fixed = loaded + 12*sum(s["fixed_month"].values())
    margin = s["rate"] - VAR
    full = s["beds"]*12*s["rate"] - fixed - s["beds"]*12*VAR
    at90 = 0.9*s["beds"]*12*s["rate"] - fixed - 0.9*s["beds"]*12*VAR
    out[k] = dict(name=s["name"], beds=s["beds"], rate=s["rate"], wages=round(w), staff_loaded=round(loaded),
       staff_per_res_month=round(loaded/s["beds"]/12), fixed_year=round(fixed), var_per_res_month=round(VAR),
       profit_full=round(full), profit_90=round(at90), breakeven_residents=round(fixed/(12*margin),1),
       breakeven_rate_full=round(fixed/(s["beds"]*12)+VAR), staff=s["staff"], fixed_month=s["fixed_month"])
# 3-year projection: Y1-Y2 scenario B, Y3 scenario C
def year(sk, avg):
    s=out[sk]; rev=avg*12*s["rate"]; cost=s["fixed_year"]+avg*12*s["var_per_res_month"]; return dict(avg_residents=avg, revenue=round(rev), costs=round(cost), net=round(rev-cost))
ramp = [3,4,5,6,7,8,9,9,9,10,10,10]  # residents by month, year 1 EST
out["projection"] = {"Y1": year("B", round(sum(ramp)/12,2)), "Y2": year("B", 9.5), "Y3": year("C", 16)}
out["ramp_y1"] = ramp
y1_loss_months = sum(min(0, r*(out['B']['rate']-out['B']['var_per_res_month']) - out['B']['fixed_year']/12) for r in ramp)
out["y1_ramp_cash_gap"] = round(-y1_loss_months)
su = {"Property purchase (placeholder, depends on city)":650000, "Renovation: fire alarm, sprinklers if required, accessibility, baths":150000,
      "Furniture, beds, kitchen, equipment":40000, "Pre-opening payroll, hiring, training, administrator course":25000,
      "Legal, accounting, licensing, insurance deposits":15000, "Working capital (cash cushion, about 6 months)":150000}
tot = sum(su.values()); out["uses"]=su; out["uses_total"]=tot
out["sources"]={"Owner equity (20%)":round(tot*0.2), "SBA 504 or 7(a) bank loan":round(tot*0.8*0.6), "PIDA Small Business First (if the county says a care home qualifies)":round(tot*0.8*0.4)}
json.dump(out, open("research/model.json","w"), indent=1)
json.dump(dict(lpn_hr=LPN, cna_hr=CNA, burden=B-1, annual_shown=578598, annual_label="$578,598", per_resident_month_shown={"10":4822,"20":2411}), open("research/staffing_math.json","w"))
for k in "ABC": o=out[k]; print(k, o["staff_loaded"], o["staff_per_res_month"], o["fixed_year"], "full", o["profit_full"], "90%", o["profit_90"], "BE res", o["breakeven_residents"], "BE rate", o["breakeven_rate_full"])
print(out["projection"], "ramp gap", out["y1_ramp_cash_gap"], "uses", tot, out["sources"])
