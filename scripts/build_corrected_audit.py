"""Apply the October 2026 source re-verification to audit/master_audit.csv.

Every change below was checked against the cited page of the source PDF (see verification_2026-10.md).
Reads archive/master_audit_2026-09.csv, writes master_audit.csv, then
recomputes document- and group-level tiers with the deterministic rule.
"""
import csv
import os
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "archive", "master_audit_2026-09.csv")
OUT = os.path.join(HERE, "..", "master_audit.csv")

rows = list(csv.DictReader(open(SRC, encoding="utf-8")))
by_doc = {r["document"]: r for r in rows}


def fix(doc_prefix, **kv):
    hits = [d for d in by_doc if d.startswith(doc_prefix)]
    assert len(hits) == 1, (doc_prefix, hits)
    r = by_doc[hits[0]]
    for k, v in kv.items():
        r[k] = v
    r["corrected_2026_10"] = "YES"


for r in rows:
    r["corrected_2026_10"] = "NO"
    r["dc_attributable"] = "YES"
    r["D_m3_reported"] = ""
    r["re_share_india"] = ""
    r["pue_india"] = ""

# --- source fixes ---------------------------------------------------------------------------
fix("adani_2025", dc_attributable="NO", D_m3_reported="1509232",
    water_source_coded="S2;S4;third-party;surface",
    notes="Consolidated AEL boundary (mining, airports, roads, copper, solar mfg, defence, data "
          "centres; BRSR p.349). Volumes are conglomerate water, not AdaniConneX. W-C=D exact.")
fix("BAL_24-25", dc_attributable="NO", D_m3_reported="56000",
    notes="Standalone Bharti Airtel Limited boundary (BRSR Q13): Nxtra Data Ltd is a subsidiary "
          "and is excluded. Volumes are telecom water, not data-centre water.")
fix("ctrls_2023", cooling_arch_coded="A1 (cooling towers, p.34)", flag_arch_specified="PARTIAL",
    notes="India only. Consumption 4,68,330 m3 (p.33); withdrawal not reported although the GRI "
          "index lists 303-3 at pp.33-34.")
fix("ctrls_2024", cooling_arch_coded="A1;A3 (cooling-tower fills p.33; air-cooled PAC and "
                                     "air-based chillers pp.14,36)",
    flag_arch_specified="PARTIAL", pue_value="1.466", pue_india="1.466", re_share_india="0.23%",
    notes="India only. Consumption 4,09,037 m3; PUE 1.490 (FY23) and 1.466 (FY24), p.34; "
          "renewable 0.23% of energy, p.32.")
fix("google_2025", W_m3_reported="41681150", C_m3_reported="30794310", D_m3_reported="10886845",
    water_source_coded="S1 potable 7,699 Mgal; non-potable 1,289; S3 reclaimed 877 (DC total)",
    notes="Appendix p.110-111: total W 11,011 / D 2,876 / C 8,135 Mgal; data centres only "
          "W 9,866 / D 2,079 / C 7,787 Mgal; per-site W/D/C for ~33 named locations, none in "
          "India. W-C=D exact.")
fix("Microsoft_2025", cooling_arch_coded="A2 (evaporative fleet, p.35); closed-loop DTC to "
                                         "chillers in new AI designs (p.35)",
    flag_arch_specified="PARTIAL",
    notes="FY24 W 10,377,000 / C 5,807,000 m3 (Water Table 5, p.37; new estimation method from "
          "FY24). WUE 0.30 L/kWh is withdrawal-based (p.35). A4 removed: no support in report.")
fix("nttdata_2024", scope="global", W_m3_reported="2098000", C_m3_reported="1371000",
    D_m3_reported="728000", flag_source_specified="YES",
    water_source_coded="surface/rain 820k; ground 21k; third-party 1,257k m3",
    notes="Global direct operations, TNFD table p.41 (W 2,098 / D 728 / C 1,371 thousand m3). "
          "The assured 413,779 / 203,297 m3 cover 14 Japanese facilities only (p.22).")
fix("nttdata_2025_sustainability-report-cb", notes="Case Book. Water-positivity text describes "
    "the MeetZero client product (p.11), not an NTT commitment; T1 rests on the Jal Sanjivani "
    "India community water project (p.12).")
fix("nttdata_2025_sustainability-report-db", W_m3_reported="3840000", C_m3_reported="1116000",
    D_m3_reported="2724000", tier="T2", disagree="YES", flag_source_specified="YES",
    pue_value="1.38", water_source_coded="ground 2,425k; third-party 1,402k; surface 13k m3",
    notes="Data centres only, 141 sites / 16 countries: W 3.84 / C 1.12 million m3 (p.99, p.43). "
          "WUE 0.72 L/kWh = consumption per IT energy, site boundary in footnote 7. PUE 1.38 "
          "global. Previously coded NOT REPORTED.")
fix("Nxtra_2024", cooling_arch_coded="A1;A3 (cooling-tower blowdown; air-based chillers, p.51)",
    flag_arch_specified="PARTIAL")
fix("Nxtra_2025", D_m3_reported="9306", re_share_india="49%",
    cooling_arch_coded="A1;A3 (cooling towers p.40; air-based chillers majority of core p.41)",
    flag_arch_specified="PARTIAL",
    notes="C (216,357, p.39 and p.110) > W (201,028). C = W + recycled (15,329) exactly, i.e. gross use, not GRI "
          "consumption. Discharge 9,306 kL (p.39) vs 91,306 kL (GRI 303-4 factsheet p.110).")
fix("Sify-Infinit", D_m3_reported="134639.5", flag_source_specified="YES", pue_india="1.7554",
    re_share_india="~38%", water_source_coded="S3 STP-recycled 12,699 kL; S5 rainwater",
    cooling_arch_coded="A1 (water-cooled condensers p.52); A3 (closed-loop air-cooled chillers "
                       "p.53); A4 (adiabatic, new campuses p.93); rack-level RDHx/DTC/immersion",
    flag_arch_specified="PARTIAL",
    notes="W 2,96,279 / C 1,34,639.5 / D 1,34,639.5 kL (p.52): W-C != D by 27,000 kL. Unmetered DC "
          "sites estimated at 45 L/person/working day (CGWA) with 50/50 C/D split (p.52). WUE "
          "1.805 printed without unit. Report states TIA-942 Rated-4, not Tier 3.")
fix("Sify_Techonologies", wue_value="",
    notes="W 3,06,915.60 kL (p.02; FY24 61,32,323 kL). The p.19 KPI panel gives year-on-year "
          "changes with arrows ('WUE ... 1% down', 'per-employee consumption 96% down'): no WUE "
          "value is disclosed.")
fix("STT_2023", notes="Assured total W 1,059,011 m3 (p.61) vs SASB data centres 1,030,852 + "
                      "offices 1,444 = 1,032,296 m3 at 100% coverage (p.71): 26,715 m3 gap. "
                      "India W 357,429 m3 (p.58). WUE = consumption / IT energy (ISO 30134).")
fix("stt_gdc_2024", notes="W 1,149,020 m3 (p.63) = SASB 1,146,979 + 2,041 exactly (p.76). "
                          "WUE 0.73 = consumption / IT energy per ISO 30134 (p.64).")
fix("STT-GDC-India", re_share_india="59.6%",
    notes="India W 298,595 m3 for data centres (SASB p.46). WUE 0.58 L/kWh. Renewable energy "
          "factor 59.6% (p.8). PUE given only as design <1.5 and 2% change.")

# --- deterministic tier rule ----------------------------------------------------------------
def rule(r):
    W, C = r["W_m3_reported"], r["C_m3_reported"]
    Wi, Ci = r["W_m3_india"], r["C_m3_india"]
    if r["in_sample"] != "YES":
        return "N/A"
    if Wi and Ci:
        return "T3"
    if W or C or Wi or Ci:
        return "T2"
    return "T1"


for r in rows:
    if r["in_sample"] == "YES":
        t = rule(r)
        assert t == r["tier"] or r["document"].startswith("nttdata_2025_sustainability-report-db"), r["document"]
        r["tier"] = t
        manual = r["tier_coder_original"]
        if manual not in ("T0", "T1", "T2", "T3", "T4", "T5"):
            r["disagree"] = "N/A"   # manual value was not a rubric tier (Sify Infinit: TIA-942 label)
        else:
            r["disagree"] = "YES" if t != manual else "NO"

fields = list(rows[0].keys())
with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader(); w.writerows(rows)

ins = [r for r in rows if r["in_sample"] == "YES"]
print("documents in sample:", len(ins))
print("document tiers:", dict(sorted(Counter(r["tier"] for r in ins).items())))
grp = {}
for r in ins:
    grp[r["operator_group"]] = max(grp.get(r["operator_group"], "T0"), r["tier"])
print("group tiers:", dict(sorted(Counter(grp.values()).items())))
print("rule vs manual disagreements:", sum(r["disagree"] == "YES" for r in ins))
for r in ins:
    if r["disagree"] == "YES":
        print("   ", r["document"][:45], r["tier_coder_original"], "->", r["tier"])
print("wrote", os.path.relpath(OUT))
