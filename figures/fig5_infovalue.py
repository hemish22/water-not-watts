"""Fig. 5 - Feasible source-WUE interval per operator group, and information value per attribute.

Numbers are read from ../data/info_value_results.json, written by ../scripts/info_value.py
(run with OUT=../data/info_value_results.json), so the figure cannot drift from the tables.
"""
import json
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import *

HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, "..", "data", "info_value_results.json")))

SHORT = {"arch": "Heat-rejection architecture,\nper facility  (A1–A6)",
         "wue_bnd": "WUE-site with stated\nboundary + denominator",
         "pue": "PUE, India portfolio\nor per facility",
         "ppa": "Renewable share of\nelectricity supply",
         "zone": "Facility location /\nclimate zone"}
ATTR = sorted(R["iv"].items(), key=lambda kv: -kv[1]["share"])
OPS = sorted(R["ops"].items(), key=lambda kv: (kv[1]["u"], kv[0]))
n_full = sum(1 for _, v in OPS if v["lo"] == 2.27 and v["hi"] == 10.22)
unmandated = sum(v["share"] for _, v in ATTR if not v["mandated"])

fig, (axL, axR) = plt.subplots(1, 2, figsize=(14.6, 6.6),
                               gridspec_kw=dict(width_ratios=[1.06, 1.0], wspace=0.42))
fig.patch.set_facecolor("white")

# ---------------- LEFT : feasible intervals per operator ----------------
axL.set_facecolor("#FAFCFA")
for i, (name, v) in enumerate(OPS):
    lo, hi, u = v["lo"], v["hi"], v["u"]
    y = len(OPS) - 1 - i
    col = C["salmon"] if u > 1.0 else C["green"]
    axL.plot([lo, hi], [y, y], color=C["ink"], lw=1.4, zorder=4)
    axL.add_patch(Rectangle((lo, y - 0.26), hi - lo, 0.52, fc=col, ec="black", lw=1.2, zorder=5))
    axL.plot([lo, lo], [y - 0.30, y + 0.30], color=C["ink"], lw=2.0, zorder=6)
    axL.plot([hi, hi], [y - 0.30, y + 0.30], color=C["ink"], lw=2.0, zorder=6)
    axL.text((lo + hi) / 2, y, f"$U_j$ = {u:.3f}", ha="center", va="center",
             fontsize=9.0, fontweight="bold", zorder=8)
    axL.text(hi + 0.22, y, f"{lo:.2f}–{hi:.2f}", ha="left", va="center",
             fontsize=7.8, color="#444", zorder=8)
axL.set_yticks(range(len(OPS)))
axL.set_yticklabels([n for n, _ in OPS][::-1], fontsize=9.8)
axL.set_xlim(0, 13.6); axL.set_ylim(-1.30, len(OPS) + 0.05)
axL.set_xlabel("feasible WUE$_{source}$  (L / kWh)", fontsize=10.8, fontweight="bold")
axL.grid(axis="x", color="#C9D6C9", lw=0.7); axL.set_axisbelow(True)
for s in ("top", "right"):
    axL.spines[s].set_visible(False)
axL.set_title("(a)  What each disclosure actually pins down",
              fontsize=12.0, fontweight="bold", pad=12)

words = {2: "two", 3: "three", 4: "four", 5: "five"}
axL.annotate(f"{words.get(n_full, n_full)} operators share one interval:\n"
             "nothing they publish constrains\nthe identity at all",
             xy=(10.22, 1.0), xytext=(11.15, -0.95), fontsize=7.8, fontweight="bold",
             color="#8C2A1A", va="center", zorder=10,
             bbox=dict(boxstyle="round,pad=0.32", fc="#FBE3DE", ec="#8C2A1A", lw=1.2),
             arrowprops=dict(arrowstyle="-|>", lw=1.5, color="#8C2A1A"))
axL.text(0.30, len(OPS) - 0.40,
         f"mean $U_j$ = {R['mean_u']:.3f}   —   the interval is {R['mean_u']:.0%} as wide as its own midpoint",
         fontsize=9.0, fontweight="bold", color=C["dblue"], va="center", zorder=9)

# ---------------- RIGHT : information value ----------------
axR.set_facecolor("#FAFCFA")
ys = np.arange(len(ATTR))[::-1]
for i, (a, v) in enumerate(ATTR):
    y, share, mand = ys[i], v["share"], v["mandated"]
    col = C["dblue"] if mand else C["purple"]
    axR.barh(y, share, height=0.62, color=col, edgecolor="black", lw=1.3, zorder=4)
    axR.text(share + 0.7, y, f"{share:.1f}%", ha="left", va="center",
             fontsize=11.0, fontweight="bold", color=C["dblue"], zorder=8)
    if share > 15:
        axR.text(0.7, y, "required by BRSR" if mand else "not required", ha="left", va="center",
                 fontsize=8.2, color="white" if mand else "#3A2A50", fontweight="bold", zorder=9)
axR.set_yticks(ys)
axR.set_yticklabels([SHORT[a] for a, _ in ATTR], fontsize=9.3, linespacing=1.25)
axR.set_xlim(0, 58); axR.set_ylim(-0.85, len(ATTR) - 0.35)
axR.set_xlabel("mean reduction in source-water uncertainty  (% of achievable)",
               fontsize=10.6, fontweight="bold")
axR.grid(axis="x", color="#C9D6C9", lw=0.7); axR.set_axisbelow(True)
for s in ("top", "right"):
    axR.spines[s].set_visible(False)
axR.set_title("(b)  Which missing field costs the most",
              fontsize=12.0, fontweight="bold", pad=12)

idx = [i for i, (_, v) in enumerate(ATTR) if not v["mandated"]]
top, bot = ys[idx[0]] + 0.34, ys[idx[-1]] - 0.34
xb = 44.5
axR.plot([xb, xb], [top, bot], color="#8C2A1A", lw=2.2, zorder=6)
for yy in (top, bot):
    axR.plot([xb - 0.7, xb], [yy, yy], color="#8C2A1A", lw=2.2, zorder=6)
axR.text(xb + 1.0, (top + bot) / 2,
         f"{unmandated:.1f}% of the\nachievable reduction\nsits in fields BRSR\ndoes not require",
         ha="left", va="center", fontsize=9.0, fontweight="bold", color="#8C2A1A", zorder=10,
         bbox=dict(boxstyle="round,pad=0.32", fc="#FBE3DE", ec="#8C2A1A", lw=1.3))

lg = [mpatches.Patch(fc=C["purple"], ec="black", label="not required by BRSR"),
      mpatches.Patch(fc=C["dblue"], ec="black", label="required by BRSR (location: count only)")]
axR.set_xticks([0, 10, 20, 30, 40])
axR.legend(handles=lg, loc="lower right", fontsize=8.6, frameon=True,
           edgecolor="black", framealpha=1.0)

fig.suptitle("Disclosure incompleteness, measured in litres",
             fontsize=13.6, fontweight="bold", y=0.985)
fig.subplots_adjust(left=0.115, right=0.985, bottom=0.10, top=0.88, wspace=0.42)
save(fig, "fig5_infovalue")
print("ok")
