"""Does dry cooling flip sign on source WUE in India?  WUE_source = WUE_site + PUE x EWIF"""
EWIF = {"S1 best-practice coal":1.99,"S2 MoEFCC 3.0 (central)":2.30,
        "S3 MoEFCC 3.5 cap":2.67,"S4 non-compliant fleet":3.77,"S4+ incl. hydro":5.20}

# Site WUE by heat-rejection class (L/kWh_IT) and typical PUE by class x climate zone
CLASS = {  # name: (WUE_site, PUE warm-humid, PUE composite, PUE temperate)
 "A1 chilled water + open tower":   (1.80, 1.45, 1.42, 1.38),
 "A2 direct/indirect evaporative":  (2.20, 1.40, 1.35, 1.30),
 "A3 air-cooled chiller (dry)":     (0.00, 1.90, 1.75, 1.60),
 "A4 dry cooler + adiabatic assist":(0.70, 1.62, 1.52, 1.44),
 "A5 warm-water DTC + dry cooler":  (0.05, 1.45, 1.35, 1.25),
 "A6 immersion + dry cooler":       (0.03, 1.38, 1.30, 1.20),
}
ZONES = [("warm-humid (Chennai, Mumbai)",1),("composite (Delhi-NCR)",2),("temperate (Bengaluru, Pune)",3)]

for zname, zi in ZONES:
    print("="*88); print(f"ZONE: {zname}"); print("="*88)
    print(f"{'class':<34}{'WUEsite':>8}{'PUE':>6}", end="")
    for e in EWIF: print(f"{e.split()[0]:>9}", end="")
    print()
    for cname,(w,*pues) in CLASS.items():
        p = pues[zi-1]
        print(f"{cname:<34}{w:8.2f}{p:6.2f}", end="")
        for e,ev in EWIF.items(): print(f"{w+p*ev:9.2f}", end="")
        print()
    print()

print("="*88); print("BREAK-EVEN: at what EWIF does A3 (dry) stop beating A1 (evaporative)?"); print("="*88)
print(f"{'zone':<32}{'dWUEsite':>10}{'dPUE':>7}{'EWIF* (L/kWh)':>16}  verdict at India EWIF 1.99-3.77")
for zname, zi in ZONES:
    w1,p1 = CLASS["A1 chilled water + open tower"][0], CLASS["A1 chilled water + open tower"][zi]
    w3,p3 = CLASS["A3 air-cooled chiller (dry)"][0],   CLASS["A3 air-cooled chiller (dry)"][zi]
    dW, dP = w1-w3, p3-p1
    ev = dW/dP
    v = "SIGN FLIPS - dry is worse" if ev<=3.77 else "no flip - dry still wins"
    if ev<=1.99: v="SIGN FLIPS under ALL scenarios"
    print(f"{zname:<32}{dW:10.2f}{dP:7.2f}{ev:16.2f}  {v}")

print()
print("A5 (warm-water DTC + dry cooler) vs A1, warm-humid:")
w1,p1 = 1.80,1.45; w5,p5 = 0.05,1.45
print(f"  dWUEsite={w1-w5:.2f}  dPUE={p5-p1:+.2f}  -> A5 saves site water at NO PUE penalty:")
for e,ev in EWIF.items():
    print(f"    EWIF {ev:4.2f}: A1 source={w1+p1*ev:5.2f}  A5 source={w5+p5*ev:5.2f}  saving={(w1+p1*ev)-(w5+p5*ev):5.2f} L/kWh")
