"""India grid EWIF v2 - CEA PRIMARY source.
Source: CEA, Executive Summary on Power Sector, March 2025, p.22,
        "Electricity Generation (MU) Targets and Achievements for 2024-25 from
         Conventional sources", Apr-24 to Mar-25 Achievement column, plus the
         Renewable Energy Generation table on the same page.
"""
G = 3.78541/1000                      # gal/MWh -> L/kWh

BU = dict(thermal=1363.89, hydro=148.63, nuclear=56.68, bhutan=5.48, res=255.01)
TOT = sum(BU.values())
sh  = {k: v/TOT for k, v in BU.items()}

# Macknick et al. 2011 (NREL/TP-6A20-50900) median CONSUMPTION factors.
# Checked against Macknick et al. 2012 (ERL 7 045802): coal tower 687, nuclear tower 672,
# hydro 4491, biopower steam tower 553 match; NGCC tower is 205 in 2012 (198 here), <0.002 L/kWh effect.
# F["solar"] is not used (RES_LO is set directly); 26 gal/MWh is the CSP dry-tower value, PV is 1.
F = dict(coal_tower=687*G, gas_ccgt=198*G, nuclear_tower=672*G,
         hydro=4491*G, solar=26*G, wind=0.0, biopower=553*G)

# CEA reports thermal as one block (coal + lignite + gas + diesel).
# Gas is ~32 BU and diesel negligible, so gas is ~2.3% of the thermal block;
# lignite behaves like coal on water.
GAS_FRAC = 0.023
# RES composition: solar ~148 BU + wind ~83 BU = ~90% of the 255 BU block,
# biomass and small hydro the remaining ~10%.
RES_LO, RES_HI = 0.05, 0.90*0.05 + 0.10*F["biopower"]

COAL = {"S1 best practice (NREL tower median 2.60)": F["coal_tower"],
        "S2 MoEFCC post-2017 limit (3.0)":            3.00,
        "S3 MoEFCC legacy cap (3.5)":                 3.50,
        "S4 non-compliant / CEA 2012 obs. (5.0)":     5.00}

def ewif(coal_f, hydro_on, res_f):
    thermal_f = (1-GAS_FRAC)*coal_f + GAS_FRAC*F["gas_ccgt"]
    h = F["hydro"] if hydro_on else 0.0
    return (sh["thermal"]*thermal_f + sh["nuclear"]*F["nuclear_tower"]
            + (sh["hydro"]+sh["bhutan"])*h + sh["res"]*res_f)

print("CEA FY2024-25 shares:", {k: f"{v:.2%}" for k, v in sh.items()},
      f"  total {TOT:.2f} BU\n")
print(f"{'coal scenario':<42}{'hydro excl.':>13}{'hydro incl.':>14}")
print("-"*70)
res = {}
for name, c in COAL.items():
    lo, hi   = ewif(c, False, RES_LO), ewif(c, False, RES_HI)
    lo_h, hi_h = ewif(c, True, RES_LO), ewif(c, True, RES_HI)
    res[name] = (lo, hi, lo_h, hi_h)
    print(f"{name:<42}{lo:6.2f}-{hi:5.2f}{'':>2}{lo_h:6.2f}-{hi_h:5.2f}")
print("-"*70)
c2 = res["S2 MoEFCC post-2017 limit (3.0)"]
central = (c2[0]+c2[1])/2
band_lo = res["S1 best practice (NREL tower median 2.60)"][0]
band_hi = res["S4 non-compliant / CEA 2012 obs. (5.0)"][1]
print(f"\nHEADLINE central (S2, hydro excl.) : {central:.2f} L/kWh   [was 2.34]")
print(f"BAND S1lo - S4hi   (hydro excl.)   : {band_lo:.2f} - {band_hi:.2f}   [was 1.97 - 3.88]")
print(f"BAND with hydro included           : {res['S1 best practice (NREL tower median 2.60)'][2]:.2f}"
      f" - {res['S4 non-compliant / CEA 2012 obs. (5.0)'][3]:.2f}   [was 2.50 - 4.41]")
s2h = res["S2 MoEFCC post-2017 limit (3.0)"]
print(f"\nLi et al. (CACM 2025) US average EWIF 3.14 L/kWh INCLUDES hydropower.")
print(f"Like-for-like, India S2 hydro-included {s2h[2]:.2f}-{s2h[3]:.2f} L/kWh -> "
      f"{s2h[2]/3.14:.2f}-{s2h[3]/3.14:.2f}x the US figure")
print(f"\nGas-split sensitivity: treating the whole thermal block as coal raises S2 by "
      f"{ewif(3.00,False,RES_LO)-((1-0)*0+0):.0f}", end="")
alt = sh["thermal"]*3.00 + sh["nuclear"]*F["nuclear_tower"] + sh["res"]*RES_LO
print(f" -> {alt:.3f} vs {ewif(3.00,False,RES_LO):.3f}, i.e. +{alt-ewif(3.00,False,RES_LO):.3f} L/kWh")
print("\nBreak-even check, warm-humid A3 vs A1: EWIF* = 1.80/0.45 = 4.00")
print(f"  inside hydro-excluded band ({band_lo:.2f}-{band_hi:.2f})? "
      f"{'YES' if band_lo <= 4.00 <= band_hi else 'NO'}")
hlo = res['S1 best practice (NREL tower median 2.60)'][2]; hhi = res['S4 non-compliant / CEA 2012 obs. (5.0)'][3]
print(f"  inside hydro-included band ({hlo:.2f}-{hhi:.2f})? {'YES' if hlo <= 4.00 <= hhi else 'NO'}")
