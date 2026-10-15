"""Fig. 2 - Heat-rejection viability and source WUE by climate zone."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import *
from matplotlib.colors import LinearSegmentedColormap

EWIF = 2.30
CLASSES = [
    ("A1", "Chilled water +\nopen cooling tower",      1.80, (1.45, 1.42, 1.38), "high", "low"),
    ("A2", "Direct / indirect\nevaporative",           2.20, (1.40, 1.35, 1.30), "high", "low"),
    ("A3", "Air-cooled chiller,\nfully dry",           0.00, (1.90, 1.75, 1.60), "zero", "high"),
    ("A4", "Dry cooler +\nadiabatic assist",           0.70, (1.62, 1.52, 1.44), "seas", "med"),
    ("A5", "Warm-water DTC +\ndry cooler",             0.05, (1.45, 1.35, 1.25), "zero", "lmed"),
    ("A6", "Immersion +\ndry cooler",                  0.03, (1.38, 1.30, 1.20), "zero", "low"),
]
ZONES = [("Warm & humid", "Chennai · Mumbai · Vizag", "≈70% of capacity"),
         ("Composite",    "Delhi–NCR · Gr. Noida",    "fastest growing"),
         ("Temperate",    "Bengaluru · Pune",         "mature market")]
VIAB = {  # per class per zone: 2 = viable, 1 = marginal, 0 = poor
 "A1": (2,2,2), "A2": (0,1,2), "A3": (1,2,2), "A4": (1,2,2), "A5": (2,2,2), "A6": (2,2,2)}
GLYPH = {2: "●", 1: "◐", 0: "○"}

cmap = LinearSegmentedColormap.from_list("wue", ["#79C67A", "#DCE87C", "#F5C86B", "#E8836B"])
vmin, vmax = 2.7, 5.6

W, H = 14.3, 9.55
fig, ax = plt.subplots(figsize=(W, H))
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off"); ax.set_aspect("equal")
panel(ax, 0.12, 0.12, W-0.24, H-0.24, C["bg"], lw=1.9, r=0.18, z=0)

x0, cw = 5.00, 2.05          # first column left edge, column width
y_top, rh = 7.58, 0.94       # first row top, row height
lab_w = 3.36

ax.text(W/2, 9.12, "Heat-rejection viability and source water use by Indian climate zone",
        ha="center", fontsize=13.0, fontweight="bold", zorder=8)
ax.text(W/2, 8.76, "cell value = WUE$_{source}$ in L/kWh at grid EWIF = 2.30   ·   "
        "● viable   ◐ marginal   ○ poor",
        ha="center", fontsize=9.2, zorder=8)

# ---- zone headers
for j, (zn, cities, note) in enumerate(ZONES):
    cxj = x0 + j*cw + cw/2
    ax.add_patch(FancyBboxPatch((x0+j*cw+0.05, y_top+0.10), cw-0.10, 0.86,
        boxstyle="round,pad=0,rounding_size=0.08", fc=C["panelB"], ec="black", lw=1.3, zorder=3))
    ax.text(cxj, y_top+0.78, zn, ha="center", va="center", fontsize=10.0, fontweight="bold", zorder=5)
    ax.text(cxj, y_top+0.55, cities, ha="center", va="center", fontsize=7.6, zorder=5)
    ax.text(cxj, y_top+0.34, note, ha="center", va="center", fontsize=7.4, style="italic", zorder=5)
    ax.text(cxj, y_top+0.20, "PUE band from Table II", ha="center", va="center",
            fontsize=6.8, style="italic", color="#555", zorder=5)

# ---- rows
for i, (code, desc, ws, pues, sw, sp) in enumerate(CLASSES):
    yr = y_top - (i+1)*rh
    hi = code in ("A5", "A6")
    # label block
    ax.add_patch(FancyBboxPatch((0.60, yr+0.05), lab_w, rh-0.10,
        boxstyle="round,pad=0,rounding_size=0.08",
        fc=C["mint"] if hi else C["white"], ec="black", lw=1.6 if hi else 1.2, zorder=3))
    ax.text(0.90, yr+rh/2+0.05, code, ha="left", va="center", fontsize=11.5, fontweight="bold", zorder=5)
    ax.text(1.58, yr+rh/2+0.14, desc, ha="left", va="center", fontsize=8.5, zorder=5, linespacing=1.22)
    tag = {"high":"site water HIGH","zero":"site water ≈ 0","seas":"site water seasonal"}[sw]
    tc  = C["red"] if sw=="high" else (C["dblue"] if sw=="zero" else "#8A5A00")
    ax.text(1.58, yr+0.19, tag, ha="left", va="center", fontsize=7.6,
            color=tc, fontweight="bold", zorder=5)
    # cells
    for j in range(3):
        val = ws + pues[j]*EWIF
        f = np.clip((val-vmin)/(vmax-vmin), 0, 1)
        xc = x0 + j*cw
        ax.add_patch(Rectangle((xc+0.05, yr+0.05), cw-0.10, rh-0.10,
                     fc=cmap(f), ec="black", lw=1.6 if hi else 1.1, zorder=3))
        ax.text(xc+cw/2+0.22, yr+rh/2, f"{val:.2f}", ha="center", va="center",
                fontsize=13.0, fontweight="bold", zorder=5,
                color="black")
        ax.text(xc+0.34, yr+rh/2, GLYPH[VIAB[code][j]], ha="center", va="center",
                fontsize=13.5, zorder=5)

# ---- best-in-column markers
for j in range(3):
    vals = [ws + p[j]*EWIF for _,_,ws,p,_,_ in CLASSES]
    b = int(np.argmin(vals))
    yr = y_top - (b+1)*rh
    ax.add_patch(Rectangle((x0+j*cw+0.05, yr+0.05), cw-0.10, rh-0.10,
                 fc="none", ec=C["dblue"], lw=3.0, zorder=7))

# ---- annotations
ann = dict(fontsize=8.6, fontweight="bold", zorder=9)
yA3 = y_top - 3*rh + rh/2
ax.annotate("described by all four\nIndian colocation\ngroups for new or\nretrofitted capacity",
            xy=(x0+3*cw+0.06, yA3), xytext=(x0+3*cw+0.42, yA3+0.62),
            arrowprops=dict(arrowstyle="-|>", lw=1.5, color=C["red"]),
            color=C["red"], va="center", **ann)
yA5 = y_top - 5*rh + rh/2
ax.annotate("also sold as\n“water-free”; with A6\nthe lowest source\nWUE in every zone",
            xy=(x0+3*cw+0.06, yA5), xytext=(x0+3*cw+0.42, yA5-0.48),
            arrowprops=dict(arrowstyle="-|>", lw=1.5, color=C["dblue"]),
            color=C["dblue"], va="center", **ann)

# gap callout between A3 and A5, warm-humid column
xg = x0 - 0.34
y3 = y_top - 3*rh + rh/2
y5 = y_top - 5*rh + rh/2
ax.annotate("", xy=(xg, y3), xytext=(xg, y5),
            arrowprops=dict(arrowstyle="<|-|>", lw=2.2, color=C["red"]), zorder=9)
ax.text(xg-0.17, (y3+y5)/2, "Δ 0.99 L/kWh",
        ha="center", va="center", fontsize=8.4, color=C["red"], fontweight="bold",
        rotation=90, zorder=10,
        bbox=dict(boxstyle="round,pad=0.18", fc="white", ec=C["red"], lw=1.2))

# ---- colourbar
cb_x, cb_y, cb_w, cb_h = 8.10, 1.02, 3.00, 0.26
grad = np.linspace(0, 1, 256).reshape(1, -1)
ax.imshow(grad, extent=[cb_x, cb_x+cb_w, cb_y, cb_y+cb_h], aspect="auto",
          cmap=cmap, zorder=5)
ax.add_patch(Rectangle((cb_x, cb_y), cb_w, cb_h, fc="none", ec="black", lw=1.1, zorder=6))
for frac, lab in ((0.0, f"{vmin:.1f}"), (0.5, f"{(vmin+vmax)/2:.1f}"), (1.0, f"{vmax:.1f}")):
    ax.text(cb_x+frac*cb_w, cb_y-0.10, lab, ha="center", va="top", fontsize=8.0, zorder=6)
ax.text(cb_x-0.14, cb_y+cb_h/2, "WUE$_{source}$\nL/kWh", ha="right", va="center",
        fontsize=8.2, fontweight="bold", zorder=6)
ax.text(cb_x+cb_w+0.22, cb_y+cb_h/2, "worse →", ha="left", va="center",
        fontsize=8.0, style="italic", zorder=6)

ax.text(0.66, 1.32, "blue outline = best class in that zone", ha="left", va="center",
        fontsize=8.6, color=C["dblue"], fontweight="bold", zorder=8)
ax.text(0.66, 0.86, "hot & dry zone omitted: evaporative performs well thermally there but water stress\n"
                    "is worst, and its PUE parameters are not derived in this study",
        ha="left", va="center", fontsize=7.8, style="italic", zorder=8)

save(fig, "fig2_matrix")
print("ok")
