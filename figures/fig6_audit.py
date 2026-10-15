"""Fig. 6 - Disclosure audit at a glance: what each of the 18 in-sample documents discloses.

Every cell was checked against the source PDF in the October 2026 re-verification; the page
behind each non-empty cell is given in the comment on its row (printed page numbers).
2 = disclosed at the scope the audit needs (India data centres, or per facility for architecture)
1 = disclosed, but at a wider or non-data-centre boundary, without per-facility allocation,
    as an absolute without its denominator, or without a stated unit/boundary
0 = not disclosed
"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import *

COLS = ["With-\ndrawal", "Consump-\ntion", "WUE", "PUE", "Heat-\nrejection\nclass",
        "Water\nsource", "Renew-\nable\nshare"]
#      group,            document,             W  C  WUE PUE Arch Src RE  tier  consistency
DOCS = [
 ("Adani",            "BRSR FY25",           1, 1, 0, 0, 0, 2, 1, "T2", "pass"),  # p.381 conglomerate; RE 24% AEL p.360
 ("Amazon (AWS)",     "Sust. Report CY24",   0, 0, 1, 1, 1, 1, 1, "T1", "n.t."),  # WUE 0.15 p.24; PUE 1.15 p.7; A2 p.24
 ("Bharti Airtel",    "BRSR FY25",           1, 1, 0, 0, 0, 2, 1, "T3", "pass"),  # standalone, excludes Nxtra; p.213
 ("Bharti Airtel",    "Nxtra FY24",          0, 0, 0, 0, 1, 1, 1, "T1", "n.t."),  # A1/A3 p.51; RE 220,541 MWh p.29
 ("Bharti Airtel",    "Nxtra FY25",          2, 2, 0, 0, 1, 2, 2, "T3", "fail"),  # p.39, p.110; RE 49% p.13
 ("CtrlS",            "ESG FY21",            0, 0, 0, 0, 0, 1, 0, "T1", "n.t."),  # p.11
 ("CtrlS",            "Sust. Report FY23",   0, 2, 0, 2, 1, 1, 0, "T2", "n.t."),  # C p.33; PUE 1.490 p.29
 ("CtrlS",            "Sust. Report FY24",   0, 2, 0, 2, 1, 1, 2, "T2", "n.t."),  # C p.36; PUE 1.466 p.34; RE 0.23% p.32
 ("Google",           "Env. Report 2025",    1, 1, 0, 1, 0, 2, 1, "T2", "pass"),  # p.110-111 per site, none in India
 ("Microsoft",        "Env. Report FY24",    1, 1, 1, 0, 1, 1, 0, "T2", "pass"),  # p.37; WUE 0.30 withdrawal p.35
 ("NTT DATA",         "Sust. Report 2024",   1, 1, 0, 1, 0, 2, 1, "T2", "pass"),  # global p.41; Mumbai PUE p.15
 ("NTT DATA",         "Case Book 2025",      0, 0, 0, 0, 0, 0, 0, "T1", "n.t."),
 ("NTT DATA",         "Sust. Report 2025",   1, 1, 1, 1, 1, 2, 1, "T2", "pass"),  # p.99, p.43; 3 of 141 evaporative
 ("Sify",             "Sify Tech. AR FY25",  1, 0, 0, 0, 0, 0, 1, "T2", "n.t."),  # W p.02 company-wide; RE 38.36%
 ("Sify",             "Sify Infinit FY25",   2, 2, 1, 2, 1, 1, 2, "T3", "fail"),  # p.52; PUE p.7; RE ~38% p.30
 ("ST Telemedia GDC", "ESG CY23",            2, 0, 1, 1, 1, 1, 2, "T2", "fail"),  # India W p.58; REF India 49% p.58
 ("ST Telemedia GDC", "ESG CY24",            1, 0, 1, 1, 1, 1, 1, "T2", "pass"),  # p.63, p.76 reconcile
 ("ST Telemedia GDC", "India ESG FY25",      2, 0, 1, 0, 1, 1, 2, "T2", "pass"),  # p.46; WUE p.23; REF p.8
]
FAIL_NOTE = {4: "C1, C3", 14: "C1, C2", 15: "C3"}

FILL = {2: C["dblue"], 1: "#9DBBD8", 0: "white"}
TIERC = {"T1": "#F2A79A", "T2": "#FDF2B4", "T3": "#BCE5C3"}

nr, nc = len(DOCS), len(COLS)
CW = 1.32                                   # column pitch
XT = nc * CW                                # x where the tier column starts
fig, ax = plt.subplots(figsize=(12.4, 9.8))
ax.set_xlim(-5.2, XT + 3.3); ax.set_ylim(-2.6, nr + 2.25); ax.axis("off")

for j, lab in enumerate(COLS):
    ax.text(j * CW + CW / 2, nr + 0.16, lab, ha="center", va="bottom", fontsize=8.6,
            fontweight="bold", linespacing=1.12)
ax.text(XT + 0.55, nr + 0.16, "Tier", ha="center", va="bottom", fontsize=8.6, fontweight="bold")
ax.text(XT + 2.05, nr + 0.16, "Consistency", ha="center", va="bottom", fontsize=8.6,
        fontweight="bold")

prev = None
for i, (grp, doc, *cells, tier, cons) in enumerate(DOCS):
    y = nr - 1 - i
    if grp != prev:
        ax.text(-5.05, y + 0.5, grp, ha="left", va="center", fontsize=9.0, fontweight="bold")
        if prev is not None:
            ax.plot([-5.1, XT + 3.2], [y + 1, y + 1], color="#7A7A7A", lw=0.9, zorder=1)
        prev = grp
    ax.text(-0.15, y + 0.5, doc, ha="right", va="center", fontsize=8.4)
    for j, v in enumerate(cells):
        ax.add_patch(Rectangle((j * CW + 0.10, y + 0.10), CW - 0.20, 0.80, fc=FILL[v], ec="#333",
                               lw=0.8, zorder=3))
    ax.add_patch(FancyBboxPatch((XT + 0.15, y + 0.12), 0.80, 0.76,
                                boxstyle="round,pad=0,rounding_size=0.12", fc=TIERC[tier],
                                ec="black", lw=0.9, zorder=3))
    ax.text(XT + 0.55, y + 0.5, tier, ha="center", va="center", fontsize=8.6, fontweight="bold",
            zorder=4)
    if cons == "fail":
        txt, col = "fail " + FAIL_NOTE[i], C["red"]
    elif cons == "pass":
        txt, col = "pass", "#2E7D32"
    else:
        txt, col = "not testable", "#777"
    ax.text(XT + 1.20, y + 0.5, txt, ha="left", va="center", fontsize=8.2,
            fontweight="bold" if cons == "fail" else "normal", color=col)

# legend (two rows)
items = [(2, "disclosed at the scope the audit needs (India data centres; per facility for class)"),
         (1, "disclosed at a wider or non-data-centre boundary, without allocation, or without unit"),
         (0, "not disclosed")]
for k, (v, lab) in enumerate(items):
    ly = -0.75 - 0.52 * k
    ax.add_patch(Rectangle((-5.0, ly), 0.40, 0.36, fc=FILL[v], ec="#333", lw=0.8))
    ax.text(-4.45, ly + 0.18, lab, ha="left", va="center", fontsize=8.0)
ax.text(-5.0, -2.35, "Consistency tests:   C1  C ≤ W and D = W − C     C2  WUE × energy ≈ volume     "
        "C3  a quantity reported twice in one document agrees",
        ha="left", va="center", fontsize=7.9, style="italic")
ax.text((XT + 3.3 - 5.2) / 2, nr + 1.95,
        "Disclosure audit at a glance: 18 documents, 9 operator groups",
        ha="center", va="center", fontsize=12.4, fontweight="bold")

save(fig, "fig6_audit")
print("ok")
