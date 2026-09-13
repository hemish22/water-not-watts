"""Layer 2/3: feasible-set interval estimator and marginal information value per attribute."""
from itertools import product

EWIF_FULL = (1.99, 3.77)          # CEA primary, hydro excluded
EWIF_PPA  = (2.35, 3.50)          # disclosing contracted supply mix NARROWS the band to the
                                  # operator's actual mix (60% of full width), not the national range

# architecture class -> (WUE_site interval, PUE interval across zones)
CLS = {
 "A1": ((1.40,2.20),(1.34,1.52)), "A2": ((1.80,2.60),(1.26,1.48)),
 "A3": ((0.00,0.05),(1.52,2.02)), "A4": ((0.40,1.00),(1.38,1.70)),
 "A5": ((0.00,0.15),(1.20,1.52)), "A6": ((0.00,0.10),(1.14,1.45)),
}
def span(iv): return iv
UNKNOWN_W = (min(c[0][0] for c in CLS.values()), max(c[0][1] for c in CLS.values()))
UNKNOWN_P = (min(c[1][0] for c in CLS.values()), max(c[1][1] for c in CLS.values()))

def U(w, p, e):
    lo, hi = w[0]+p[0]*e[0], w[1]+p[1]*e[1]
    return (hi-lo)/(0.5*(hi+lo)), lo, hi

# What each operator group currently discloses.
# arch: class if specified else None | pue: True/False | wue_bnd: WUE with stated boundary
# zone: True if facility locations resolvable | ppa: True if contracted renewable share given
OPS = {
 "Adani (AdaniConneX)":   dict(arch=None,pue=False,wue_bnd=False,zone=False,ppa=False),
 "Amazon (AWS)":          dict(arch="A2",pue=False,wue_bnd=False,zone=False,ppa=False),
 "Bharti Airtel (Nxtra)": dict(arch=None,pue=False,wue_bnd=False,zone=True ,ppa=False),
 "CtrlS":                 dict(arch=None,pue=False,wue_bnd=False,zone=True ,ppa=False),
 "Google":                dict(arch=None,pue=False,wue_bnd=False,zone=False,ppa=False),
 "Microsoft":             dict(arch="A4",pue=False,wue_bnd=False,zone=False,ppa=False),
 "NTT DATA":              dict(arch=None,pue=False,wue_bnd=False,zone=False,ppa=False),
 "Sify":                  dict(arch="A5",pue=True ,wue_bnd=False,zone=True ,ppa=False),
 "ST Telemedia GDC":      dict(arch="A3",pue=False,wue_bnd=False,zone=True ,ppa=False),
}
ATTRS = ["arch","pue","wue_bnd","zone","ppa"]
LABEL = {"arch":"Heat-rejection architecture, per facility (A1-A6)",
         "pue":"Facility PUE",
         "wue_bnd":"WUE-site with stated boundary + denominator",
         "zone":"Facility location / climate zone",
         "ppa":"Contracted renewable share of supply"}
MANDATED = {"arch":False,"pue":False,"wue_bnd":False,"zone":True,"ppa":False}  # BRSR P6 status

def intervals(d):
    if d["arch"]:
        w,p = CLS[d["arch"]]
    else:
        w,p = UNKNOWN_W, UNKNOWN_P
    if d["wue_bnd"]: w = (sum(w)/2,)*2
    if d["pue"]:     p = (sum(p)/2,)*2
    elif d["zone"] and d["arch"]:   p = (p[0]+0.25*(p[1]-p[0]), p[1]-0.25*(p[1]-p[0]))
    if d["ppa"]:
        mid=0.5*(EWIF_FULL[0]+EWIF_FULL[1]); half=0.20*(EWIF_FULL[1]-EWIF_FULL[0])
        e=(mid-half, mid+half)
    else:
        e = EWIF_FULL
    return w,p,e

print(f"{'operator group':<24}{'WUEsrc lower':>13}{'upper':>8}{'U_j':>8}")
print("-"*55)
base={}
for n,d in OPS.items():
    u,lo,hi = U(*intervals(d)); base[n]=u
    print(f"{n:<24}{lo:13.2f}{hi:8.2f}{u:8.3f}")
print("-"*55)
print(f"{'MEAN':<24}{'':13}{'':8}{sum(base.values())/len(base):8.3f}\n")

print("MARGINAL INFORMATION VALUE  (mean reduction in U if the attribute were required)")
print("-"*78)
iv={}
for a in ATTRS:
    tot=0
    for n,d in OPS.items():
        if d[a]: continue                       # already disclosed -> no gain
        d2=dict(d); d2[a]=("A3" if a=="arch" else True)
        # architecture unknown: credit the mean narrowing across plausible classes
        if a=="arch":
            gains=[]
            for c in CLS:
                d3=dict(d); d3["arch"]=c
                gains.append(base[n]-U(*intervals(d3))[0])
            tot += sum(gains)/len(gains)
        else:
            tot += base[n]-U(*intervals(d2))[0]
    iv[a]=tot/len(OPS)
tot_iv=sum(iv.values())
print(f"{'attribute':<46}{'IV (dU)':>9}{'share':>8}{'BRSR?':>8}")
for a,v in sorted(iv.items(), key=lambda x:-x[1]):
    print(f"{LABEL[a]:<46}{v:9.3f}{v/tot_iv:8.1%}{'yes' if MANDATED[a] else 'NO':>8}")
print("-"*78)
print("DCI weights w_i = IV_i / sum(IV):", {a:round(v/tot_iv,3) for a,v in iv.items()})

# sensitivity: +-50% interval widths
print("\nSENSITIVITY (+-50% on all interval widths) - does the ranking hold?")
for scale in (0.5,1.0,1.5):
    g={k:((v[0][0],v[0][0]+scale*(v[0][1]-v[0][0])),(v[1][0],v[1][0]+scale*(v[1][1]-v[1][0]))) for k,v in CLS.items()}
    old=dict(CLS); CLS.clear(); CLS.update(g)
    UNKNOWN_W=(min(c[0][0] for c in CLS.values()),max(c[0][1] for c in CLS.values()))
    r={}
    for a in ATTRS:
        t=0
        for n,d in OPS.items():
            if d[a]: continue
            if a=="arch":
                t+=sum(U(*intervals({**d,"arch":c}))[0] for c in CLS)/len(CLS)*-1+base[n]
            else:
                t+=base[n]-U(*intervals({**d,a:True}))[0]
        r[a]=t/len(OPS)
    print(f"  scale {scale:4.1f}: ranking = {[a for a,_ in sorted(r.items(),key=lambda x:-x[1])]}")
    CLS.clear(); CLS.update(old)
