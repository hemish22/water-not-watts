"""Shared drawing primitives and palette for the paper's figures."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Polygon, Rectangle
from matplotlib.path import Path
import matplotlib.patches as mpatches
import numpy as np
import os

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "pdf.fonttype": 42, "ps.fonttype": 42,
    "svg.fonttype": "none",
})

# pastel palette matching the reference figures
C = dict(
    bg      = "#EAF7EC",   # outer light-green canvas
    panelA  = "#FBDCB8",   # orange sub-panel
    panelB  = "#CFE3F7",   # blue sub-panel
    panelC  = "#EDE0F7",   # violet sub-panel
    pink    = "#F9BFD4",
    blue    = "#A7C9EE",
    green   = "#BCE5C3",
    mint    = "#D3F2DC",
    yellow  = "#FDF2B4",
    cyan    = "#B7E7F7",
    purple  = "#D5B3EC",
    salmon  = "#F2A79A",
    grey    = "#DCDCDC",
    white   = "#FFFFFF",
    ink     = "#111111",
    red     = "#C62828",
    dblue   = "#14456F",
)

def panel(ax, x, y, w, h, fc, label=None, lw=1.6, r=0.14, label_size=11, z=1, ls="-"):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
        boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec="black", lw=lw, zorder=z, linestyle=ls))
    if label:
        ax.text(x + w/2, y - 0.26, label, ha="center", va="top",
                fontsize=label_size, fontweight="bold", zorder=z+5)

def box(ax, x, y, w, h, text, fc="#FFFFFF", fs=9, bold=False, r=0.10, lw=1.3,
        z=3, tc="black", ec="black", va="center", pad_top=0.0):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
        boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=ec, lw=lw, zorder=z))
    ax.text(x + w/2, y + h/2 + pad_top, text, ha="center", va=va, fontsize=fs,
            fontweight="bold" if bold else "normal", zorder=z+1, color=tc,
            linespacing=1.35)

def arrow(ax, p0, p1, lw=1.7, z=6, color="black", style="-|>", ms=9, rad=0.0, ls="-"):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle=style, mutation_scale=ms,
        lw=lw, color=color, zorder=z, shrinkA=0, shrinkB=0,
        connectionstyle=f"arc3,rad={rad}", linestyle=ls))

def op(ax, x, y, sym, r=0.155, fc="#C9EFD3", fs=11, z=7):
    ax.add_patch(Circle((x, y), r, fc=fc, ec="black", lw=1.3, zorder=z))
    ax.text(x, y + 0.005, sym, ha="center", va="center", fontsize=fs,
            fontweight="bold", zorder=z+1)

def droplet(ax, x, y, s=1.0, fc="#3B9BD6", ec="black", z=8, lw=1.1):
    """Teardrop pointing up, centred on (x,y)."""
    t = np.linspace(0, 2*np.pi, 240)
    # classic droplet parametrisation
    px = 0.30 * np.sin(t) * (1 - np.cos(t)) / 1.30
    py = 0.52 * np.cos(t) - 0.02
    pts = np.column_stack([x + s*px, y + s*py])
    ax.add_patch(Polygon(pts, closed=True, fc=fc, ec=ec, lw=lw, zorder=z))
    # highlight
    ax.add_patch(Circle((x - 0.08*s, y - 0.14*s), 0.075*s, fc="white", ec="none",
                        alpha=0.7, zorder=z+1))

def nodrop(ax, x, y, s=1.0, z=8):
    """Droplet with a slash through it = no water consumed here."""
    droplet(ax, x, y, s=s, fc="#E4E4E4", ec="#8A8A8A", z=z, lw=1.0)
    d = 0.34*s
    ax.plot([x-d, x+d], [y-d, y+d], color=C["red"], lw=2.1, zorder=z+3,
            solid_capstyle="round")

def save(fig, name, outdir=os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")):
    import os
    os.makedirs(outdir, exist_ok=True)
    for ext in ("pdf", "png"):
        fig.savefig(f"{outdir}/{name}.{ext}", dpi=260 if ext == "png" else None,
                    bbox_inches="tight", pad_inches=0.06,
                    facecolor="white")
    plt.close(fig)
    return f"{outdir}/{name}.png"
