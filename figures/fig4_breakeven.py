"""Fig. 4 - Break-even surface: when does dry cooling stop winning on source water?"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import *

dW = 1.80                       # site-water saved, A1 -> A3
XLO, XHI, YLO, YHI = 0.15, 0.70, 1.5, 5.2

fig, ax = plt.subplots(figsize=(11.2, 7.0))
fig.patch.set_facecolor("white")

x = np.linspace(XLO, XHI, 600)
y = dW/x

# shade regions
ax.fill_between(x, np.clip(y, YLO, YHI), YHI, color="#F0A79A", alpha=0.85, zorder=1)
ax.fill_between(x, YLO, np.clip(y, YLO, YHI), color="#BCE5C3", alpha=0.85, zorder=1)
ax.plot(x, y, color=C["ink"], lw=2.6, zorder=6)

ax.text(0.615, 4.72, "DRY COOLING IS WORSE\non source water",
        ha="center", va="center", fontsize=11.5, fontweight="bold", color="#8C2A1A", zorder=8)
ax.text(0.268, 1.70, "DRY COOLING IS BETTER\non source water",
        ha="center", va="center", fontsize=11.5, fontweight="bold", color="#1E6B33", zorder=8)
ax.text(0.632, 2.98, "EWIF* = $\\Delta$WUE$_{site}$ / $\\Delta$PUE",
        rotation=-19, fontsize=10.0, fontweight="bold", zorder=8, ha="center",
        bbox=dict(boxstyle="round,pad=0.22", fc="white", ec="none", alpha=0.92))

# India EWIF band
ax.axhspan(1.99, 3.77, color=C["blue"], alpha=0.30, zorder=2)
ax.axhline(1.99, color=C["dblue"], lw=1.2, ls=":", zorder=4)
ax.axhline(3.77, color=C["dblue"], lw=1.2, ls=":", zorder=4)
for val, lab in ((1.99, "S1  best-practice coal  1.99"), (2.30, "S2  MoEFCC 3.0 · central  2.30"),
                 (2.67, "S3  MoEFCC 3.5 cap  2.67"),     (3.77, "S4  non-compliant fleet  3.77")):
    ls = "-" if val == 2.30 else "--"
    lw = 2.0 if val == 2.30 else 1.1
    ax.axhline(val, color=C["dblue"], lw=lw, ls=ls, zorder=5, alpha=0.9)
    ax.text(XLO+0.006, val+0.045, lab, fontsize=8.0, color=C["dblue"],
            fontweight="bold" if val == 2.30 else "normal", zorder=9)
ax.text(XHI-0.008, 2.98+0.62, "India grid\nEWIF band", ha="right", va="center",
        fontsize=9.0, color=C["dblue"], fontweight="bold", zorder=9,
        bbox=dict(boxstyle="round,pad=0.26", fc="white", ec=C["dblue"], lw=1.2, alpha=0.95))

# climate-zone bands
zones = [(0.22, "Temperate\nBengaluru · Pune"), (0.33, "Composite\nDelhi–NCR"),
         (0.45, "Warm-humid\nChennai · Mumbai")]
for xv, lab in zones:
    ax.axvline(xv, color="#5C4033", lw=1.5, ls="-.", zorder=4, alpha=0.85)
    ax.text(xv, YHI+0.06, lab, ha="center", va="bottom", fontsize=8.6,
            fontweight="bold", color="#5C4033", zorder=9)
    ev = dW/xv
    if ev <= YHI:
        ax.plot(xv, ev, "o", ms=9, mfc="white", mec=C["ink"], mew=2.0, zorder=10)
        ax.text(xv-0.012, ev+0.13, f"EWIF* = {ev:.2f}", fontsize=8.8, fontweight="bold",
                zorder=10, ha="right",
                bbox=dict(boxstyle="round,pad=0.20", fc="white", ec="black", lw=1.0))
    else:
        ax.text(xv-0.014, YHI-0.30, f"EWIF* = {ev:.2f}\n(off scale)",
                fontsize=8.6, fontweight="bold", zorder=10, ha="right", va="top")

# the critical threshold
xc = dW/3.77
ax.plot(xc, 3.77, "*", ms=22, mfc=C["yellow"], mec=C["ink"], mew=1.6, zorder=12)
ax.annotate("reversal becomes possible only here\n"
            "$\\Delta$PUE $\\geq$ 0.478  AND  non-compliant fleet\n"
            "— and no disclosure resolves either",
            xy=(xc, 3.77), xytext=(0.556, 2.35),
            fontsize=9.2, fontweight="bold", zorder=12,
            bbox=dict(boxstyle="round,pad=0.34", fc=C["yellow"], ec="black", lw=1.3),
            arrowprops=dict(arrowstyle="-|>", lw=1.8, color="black",
                            connectionstyle="arc3,rad=0.0"))

ax.set_xlim(XLO, XHI); ax.set_ylim(YLO, YHI)
ax.set_xlabel("$\\Delta$PUE   energy penalty of dry vs evaporative rejection",
              fontsize=11.5, fontweight="bold")
ax.set_ylabel("grid EWIF   (L / kWh)", fontsize=11.5, fontweight="bold")
ax.set_title("When does replacing evaporative with dry cooling stop saving water at source?",
             fontsize=12.8, fontweight="bold", pad=30)
ax.grid(color="#FFFFFF", lw=0.6, alpha=0.55, zorder=3)
ax.set_axisbelow(False)
for s in ("top", "right"): ax.spines[s].set_visible(False)
plt.tight_layout()
save(fig, "fig4_breakeven")
print("ok")
