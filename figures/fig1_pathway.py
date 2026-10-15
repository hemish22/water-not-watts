"""Fig. 1 - Where water actually leaves a liquid-cooled data centre."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import *

W, H = 16.6, 8.1
fig, ax = plt.subplots(figsize=(W, H))
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off"); ax.set_aspect("equal")
panel(ax, 0.12, 0.12, W-0.24, H-0.24, C["bg"], lw=1.9, r=0.18, z=0)

# ============================ PANEL (a) : FACILITY ==========================
PA = dict(x=0.52, y=4.00, w=11.10, h=3.66)
panel(ax, PA["x"], PA["y"], PA["w"], PA["h"], C["panelA"], z=1)
ax.text(PA["x"]+PA["w"]/2, PA["y"]+PA["h"]-0.25,
        "(a)  FACILITY  —  three thermally coupled loops, one water boundary",
        ha="center", va="center", fontsize=11.5, fontweight="bold", zorder=6)

yb, hb = 5.06, 1.46

box(ax, 0.78, yb, 1.16, hb, "AI\nIT load\n\nGPU racks", C["pink"], fs=9.0, bold=True)

# loop 1
box(ax, 2.30, yb, 1.96, hb, "", C["blue"])
ax.text(3.28, yb+hb-0.27, "①  IT LOOP", ha="center", va="center", fontsize=9.6, fontweight="bold", zorder=5)
ax.text(3.28, yb+0.80, "cold plate / immersion", ha="center", va="center", fontsize=8.0, zorder=5)
ax.text(3.28, yb+0.58, "sealed · CLOSED", ha="center", va="center", fontsize=7.8,
        style="italic", color=C["dblue"], zorder=5)
nodrop(ax, 3.28, yb+0.29, s=0.38)

# loop 2
box(ax, 4.60, yb, 2.14, hb, "", C["blue"])
ax.text(5.67, yb+hb-0.27, "②  FACILITY LOOP", ha="center", va="center", fontsize=9.6, fontweight="bold", zorder=5)
ax.text(5.67, yb+0.80, "CDU → chilled water", ha="center", va="center", fontsize=8.0, zorder=5)
ax.text(5.67, yb+0.58, "CLOSED", ha="center", va="center", fontsize=7.8,
        style="italic", color=C["dblue"], zorder=5)
nodrop(ax, 5.67, yb+0.29, s=0.38)

# loop 3 : heat rejection
hx, hw = 7.08, 3.18
ax.add_patch(FancyBboxPatch((hx, 4.34), hw, 2.94,
    boxstyle="round,pad=0,rounding_size=0.10", fc="#FFFFFF", ec="black", lw=1.5, zorder=2.5))
ax.text(hx+hw/2, 7.05, "③  HEAT REJECTION", ha="center", va="center",
        fontsize=9.6, fontweight="bold", zorder=6)
ax.text(hx+hw/2, 6.82, "the only site-water boundary", ha="center", va="center",
        fontsize=7.8, style="italic", color=C["red"], zorder=6)

box(ax, hx+0.15, 5.80, hw-0.30, 0.90, "", C["cyan"], z=4)
ax.text(hx+hw/2-0.26, 6.46, "EVAPORATIVE   A1 · A2 · A4", ha="center", va="center", fontsize=8.3, fontweight="bold", zorder=6)
ax.text(hx+hw/2-0.26, 6.24, "open tower · DEC/IDEC · adiabatic", ha="center", va="center", fontsize=7.2, zorder=6)
ax.text(hx+hw/2-0.26, 6.01, "site water consumed as vapour", ha="center", va="center", fontsize=7.2,
        color=C["red"], fontweight="bold", zorder=6)
droplet(ax, hx+hw-0.44, 6.25, s=0.45, z=9)

box(ax, hx+0.15, 4.52, hw-0.30, 0.90, "", C["mint"], z=4)
ax.text(hx+hw/2-0.26, 5.18, "DRY   A3 · A5 · A6", ha="center", va="center", fontsize=8.3, fontweight="bold", zorder=6)
ax.text(hx+hw/2-0.26, 4.96, "air-cooled chiller · dry cooler", ha="center", va="center", fontsize=7.2, zorder=6)
ax.text(hx+hw/2-0.26, 4.73, "no site water, higher PUE", ha="center", va="center", fontsize=7.2,
        color=C["dblue"], fontweight="bold", zorder=6)
nodrop(ax, hx+hw-0.44, 4.98, s=0.40)   # aligned with the blue droplet above

box(ax, 10.52, yb+0.14, 0.94, hb-0.28, "heat to\natmosphere", C["grey"], fs=8.0)

arrow(ax, (1.94, yb+hb/2), (2.28, yb+hb/2))
arrow(ax, (4.26, yb+hb/2), (4.58, yb+hb/2))
arrow(ax, (6.74, yb+hb/2), (7.06, yb+hb/2))
arrow(ax, (hx+hw, 6.25), (10.50, 6.05), rad=-0.10)
arrow(ax, (hx+hw, 4.98), (10.50, 5.35), rad=0.10)
ax.text(3.27, yb+hb+0.15, "heat", ha="center", fontsize=7.4, style="italic", zorder=6)

# electricity bus feeding all three loops
bus_y = 4.62
ax.plot([2.32, 6.72], [bus_y, bus_y], color=C["dblue"], lw=2.2, zorder=5, solid_capstyle="round")
for bx in (3.28, 5.67):
    arrow(ax, (bx, bus_y), (bx, yb-0.02), lw=1.8, ms=9, color=C["dblue"])
arrow(ax, (6.72, bus_y), (7.06, bus_y), lw=1.8, ms=9, color=C["dblue"])
ax.text(2.32, bus_y-0.24, "electricity", fontsize=7.8, color=C["dblue"],
        fontweight="bold", ha="left", va="center", zorder=6)

# ============================ PANEL (b) : GRID ==============================
PB = dict(x=0.52, y=0.55, w=11.10, h=2.72)
panel(ax, PB["x"], PB["y"], PB["w"], PB["h"], C["panelB"], z=1)
ax.text(PB["x"]+PB["w"]/2, PB["y"]+PB["h"]-0.25,
        "(b)  GRID  —  the second water boundary, invisible to site metrics",
        ha="center", va="center", fontsize=11.5, fontweight="bold", zorder=6)

gy, gh = 0.98, 1.42
box(ax, 0.78, gy, 2.56, gh, "", C["yellow"])
ax.text(2.06, gy+gh-0.25, "INDIA GRID MIX", ha="center", fontsize=8.8, fontweight="bold", zorder=5)
ax.text(2.06, gy+0.85, "CEA Exec. Summary Mar-2025", ha="center", fontsize=7.4, zorder=5)
ax.text(2.06, gy+0.62, "1,829.7 BU generated FY2024–25", ha="center", fontsize=7.2, zorder=5)
ax.text(2.06, gy+0.41, "thermal 74.5% · RES 13.9%", ha="center", fontsize=7.2, zorder=5)
ax.text(2.06, gy+0.20, "hydro 8.1% · nuclear 3.1%", ha="center", fontsize=7.2, zorder=5)

box(ax, 3.72, gy, 2.42, gh, "", C["salmon"])
ax.text(4.93, gy+gh-0.25, "THERMOELECTRIC COOLING", ha="center", fontsize=8.0, fontweight="bold", zorder=5)
ax.text(4.93, gy+0.86, "at the generating station", ha="center", fontsize=7.4, zorder=5)
ax.text(4.93, gy+0.62, "NREL median factors × mix", ha="center", fontsize=7.2, zorder=5)
ax.text(4.93, gy+0.40, "MoEFCC cap 3.0–3.5 m³/MWh", ha="center", fontsize=7.2, zorder=5)
ax.text(4.93, gy+0.19, "≈51% shown compliant (2019)", ha="center", fontsize=7.0,
        style="italic", color=C["red"], zorder=5)

droplet(ax, 6.52, gy+gh/2+0.06, s=0.66, z=9)
ax.text(6.58, gy+0.20, "source water", ha="center", fontsize=5.8, color=C["red"],
        fontweight="bold", zorder=9)

box(ax, 7.02, gy, 2.18, gh, "", C["purple"])
ax.text(8.11, gy+gh-0.27, "EWIF", ha="center", fontsize=9.8, fontweight="bold", zorder=5)
ax.text(8.11, gy+0.76, "2.30 L/kWh", ha="center", fontsize=12.5, fontweight="bold", color=C["dblue"], zorder=5)
ax.text(8.11, gy+0.44, "band 1.99 – 3.77", ha="center", fontsize=7.8, zorder=5)
ax.text(8.11, gy+0.22, "hydro incl.: ≈1.2× US average", ha="center", fontsize=7.0, style="italic", zorder=5)

box(ax, 9.58, gy+0.18, 1.72, gh-0.36, "electricity\nsupplied\n\nPUE × E$_{IT}$", C["green"], fs=8.2)

arrow(ax, (3.34, gy+gh/2), (3.70, gy+gh/2))
arrow(ax, (6.14, gy+gh/2), (6.22, gy+gh/2))
arrow(ax, (6.86, gy+gh/2), (7.00, gy+gh/2))
arrow(ax, (9.20, gy+gh/2), (9.56, gy+gh/2))

# grid -> facility bus
arrow(ax, (10.44, gy+gh-0.18+0.36), (10.44, 3.55), lw=2.6, ms=0, color=C["dblue"], style="-")
ax.plot([10.44, 10.44], [3.55, 3.90], color=C["dblue"], lw=2.6, zorder=6)
ax.plot([10.44, 6.90], [3.90, 3.90], color=C["dblue"], lw=2.6, zorder=6)
arrow(ax, (6.90, 3.90), (6.90, bus_y-0.02), lw=2.6, ms=13, color=C["dblue"])
ax.text(8.70, 3.70, "powers all three loops", fontsize=8.0, color=C["dblue"],
        fontweight="bold", ha="center", va="center", zorder=9)

# ============================ PANEL (c) : IDENTITY ==========================
PC = dict(x=11.86, y=0.55, w=4.28, h=7.11)
panel(ax, PC["x"], PC["y"], PC["w"], PC["h"], C["panelC"], z=1)
cx = PC["x"] + PC["w"]/2
ax.text(cx, PC["y"]+PC["h"]-0.30, "(c)  THE IDENTITY",
        ha="center", va="center", fontsize=11.5, fontweight="bold", zorder=6)

box(ax, PC["x"]+0.22, 6.32, PC["w"]-0.44, 0.76, "", C["white"], z=4)
ax.text(cx, 6.70, r"WUE$_{\mathrm{source}}$ = WUE$_{\mathrm{site}}$ + PUE $\times$ EWIF",
        ha="center", va="center", fontsize=11.0, zorder=6)

for xa, lab in ((PC["x"]+1.18, "from  ③\nevaporative\nonly"),
                (PC["x"]+3.02, "from  (b)\nalways\npresent")):
    ax.annotate("", xy=(xa, 6.30), xytext=(xa, 5.86),
                arrowprops=dict(arrowstyle="-|>", lw=1.5, color="black"), zorder=8)
    ax.text(xa, 5.76, lab, ha="center", va="top", fontsize=7.8, zorder=8)

ax.text(cx, 5.06, "typical magnitudes, warm-humid zone   (L/kWh)",
        ha="center", fontsize=8.4, fontweight="bold", zorder=8)

base_y, scale, bw = 1.94, 0.50, 0.66
classes = [("A1\nopen tower", 1.80, 1.45), ("A3\ndry chiller", 0.00, 1.90),
           ("A5\nwarm DTC", 0.05, 1.45)]
bx0 = PC["x"] + 0.72
for i, (lab, ws, pue) in enumerate(classes):
    x = bx0 + i*1.10
    src = pue*2.30
    ax.add_patch(Rectangle((x, base_y), bw, src*scale, fc=C["purple"], ec="black", lw=1.2, zorder=6))
    ax.add_patch(Rectangle((x, base_y+src*scale), bw, ws*scale, fc=C["cyan"], ec="black", lw=1.2, zorder=6))
    ax.text(x+bw/2, base_y+(src*scale)/2, f"{src:.2f}", ha="center", va="center",
            fontsize=8.0, fontweight="bold", zorder=8)
    if ws > 0.2:
        ax.text(x+bw/2, base_y+src*scale+(ws*scale)/2, f"{ws:.2f}", ha="center", va="center",
                fontsize=8.0, fontweight="bold", zorder=8)
    ax.text(x+bw/2, base_y+(src+ws)*scale+0.11, f"{src+ws:.2f}", ha="center",
            fontsize=9.2, fontweight="bold", color=C["dblue"], zorder=8)
    ax.text(x+bw/2, base_y-0.12, lab, ha="center", va="top", fontsize=7.8, zorder=8)
ax.plot([bx0-0.18, bx0+2.98], [base_y, base_y], color="black", lw=1.3, zorder=7)

lg = [mpatches.Patch(fc=C["cyan"], ec="black", label="WUE$_{\\mathrm{site}}$  (facility)"),
      mpatches.Patch(fc=C["purple"], ec="black", label="PUE $\\times$ EWIF  (grid)")]
leg = ax.legend(handles=lg, loc="center", bbox_to_anchor=(cx/W, 1.25/H),
                fontsize=7.0, frameon=True, edgecolor="black", framealpha=1.0,
                ncol=2, columnspacing=0.6, handlelength=1.0, handletextpad=0.35)
leg.set_zorder(20)

ax.text(cx, 0.76, "the grid term dominates every class,\nincluding those sold as “water-free”",
        ha="center", va="center", fontsize=8.2, style="italic", color=C["red"],
        fontweight="bold", zorder=8)

save(fig, "fig1_pathway")
print("ok")
