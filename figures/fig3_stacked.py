"""Fig. 3 - Site vs source WUE by heat-rejection class, warm-humid zone."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import *

E_LO, E_MID, E_HI = 1.99, 2.30, 3.77
CLS = [("A6", "Immersion + dry cooler",        0.03, 1.38),
       ("A5", "Warm-water DTC + dry cooler",   0.05, 1.45),
       ("A3", "Air-cooled chiller, fully dry", 0.00, 1.90),
       ("A4", "Dry cooler + adiabatic assist", 0.70, 1.62),
       ("A1", "Chilled water + open tower",    1.80, 1.45),
       ("A2", "Direct / indirect evaporative", 2.20, 1.40)]

fig, ax = plt.subplots(figsize=(12.4, 6.4))
fig.patch.set_facecolor("white")
ax.set_facecolor("#FAFCFA")

ys = np.arange(len(CLS)); bh = 0.60
for i, (code, name, ws, pue) in enumerate(CLS):
    src = pue*E_MID; tot = ws + src
    ax.barh(i, src, height=bh, left=0, color=C["purple"], edgecolor="black", lw=1.3, zorder=3)
    ax.barh(i, ws,  height=bh, left=src, color=C["cyan"], edgecolor="black", lw=1.3, zorder=3)
    # EWIF-band whisker on the total
    lo, hi = ws + pue*E_LO, ws + pue*E_HI
    ax.plot([lo, hi], [i-0.42, i-0.42], color=C["ink"], lw=1.6, zorder=6)
    for xx in (lo, hi):
        ax.plot([xx, xx], [i-0.50, i-0.34], color=C["ink"], lw=1.6, zorder=6)
    ax.plot(tot, i-0.42, "o", ms=5.0, color=C["ink"], zorder=7)
    # labels
    if src > 0.8:
        ax.text(src/2, i+0.08, f"{src:.2f}", ha="center", va="center",
                fontsize=9.4, fontweight="bold", zorder=8)
    if ws > 0.35:
        ax.text(src+ws/2, i+0.08, f"{ws:.2f}", ha="center", va="center",
                fontsize=9.4, fontweight="bold", zorder=8)
    ax.text(tot+0.14, i+0.08, f"{tot:.2f}", ha="left", va="center",
            fontsize=11.0, fontweight="bold", color=C["dblue"], zorder=8)
    ax.text(lo-0.10, i-0.42, f"{lo:.1f}", ha="right", va="center", fontsize=7.2, color="#555", zorder=8)
    ax.text(hi+0.10, i-0.42, f"{hi:.1f}", ha="left", va="center", fontsize=7.2, color="#555", zorder=8)

ax.set_yticks(ys)
ax.set_yticklabels([f"$\\bf{{{c}}}$   {n}" for c, n, _, _ in CLS], fontsize=10.2)
ax.set_xlabel("water use effectiveness   (L / kWh$_{IT}$)", fontsize=11, fontweight="bold")
ax.set_xlim(0, 11.0); ax.set_ylim(-0.95, len(CLS)-0.20)
ax.grid(axis="x", color="#C9D6C9", lw=0.7, zorder=0)
ax.set_axisbelow(True)
for s in ("top", "right"): ax.spines[s].set_visible(False)

# evaporative baseline
base = 1.80 + 1.45*E_MID
ax.axvline(base, color=C["red"], lw=1.7, ls="--", zorder=5)
ax.text(base+0.06, len(CLS)-0.42, "evaporative baseline  5.13",
        color=C["red"], fontsize=8.8, fontweight="bold", va="center", zorder=9)

# "water-free" bracket over A5 and A3
i5, i3 = 1, 2
xb = 7.85                                   # clear of the A3 whisker (to 7.16)
ax.plot([xb, xb+0.16, xb+0.16, xb], [i5, i5, i3, i3], color=C["ink"], lw=1.5, zorder=8)
ax.annotate("both marketed as\n“water-free cooling”\nΔ = 0.99 L/kWh at source",
            xy=(xb+0.16, (i5+i3)/2), xytext=(xb+0.45, (i5+i3)/2),
            fontsize=9.2, fontweight="bold", va="center", zorder=9,
            bbox=dict(boxstyle="round,pad=0.34", fc=C["yellow"], ec="black", lw=1.2),
            arrowprops=dict(arrowstyle="-", lw=0))

lg = [mpatches.Patch(fc=C["purple"], ec="black", label="PUE $\\times$ EWIF   grid-mediated"),
      mpatches.Patch(fc=C["cyan"],   ec="black", label="WUE$_{\\mathrm{site}}$   on-site evaporation"),
      plt.Line2D([0],[0], color=C["ink"], lw=1.6, marker="|", ms=9,
                 label="total across EWIF band 1.99–3.77")]
ax.legend(handles=lg, loc="lower right", fontsize=9.0, frameon=True,
          edgecolor="black", framealpha=1.0)

ax.set_title("Site and source water use by heat-rejection class — warm-humid zone, EWIF = 2.30 L/kWh",
             fontsize=12.6, fontweight="bold", pad=14)
plt.tight_layout()
save(fig, "fig3_stacked")
print("ok")
