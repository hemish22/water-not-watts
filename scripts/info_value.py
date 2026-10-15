"""Feasible-set interval estimator and marginal information value per disclosure attribute.

Corrected version (15 Oct 2026). Differences from audit/info_value.py:

1. Operator inputs re-coded against the source documents (see verification_2026-10.md, section B):
   - Microsoft: A4 removed (no support in the report); fleet is A2, new AI designs closed-loop DTC.
   - Sify: A5 was not supported; the report describes water-cooled condensers (A1), closed-loop
     air-cooled chillers (A3) and adiabatic cooling (A4). India PUE 1.7554 and ~38 % RE share.
   - ST Telemedia GDC: A1 and A3 both stated for India (cooling-tower reuse; air-cooled chillers).
   - Bharti Airtel (Nxtra): A1 and A3 stated (cooling towers; air-based chillers); 49 % RE share.
   - CtrlS: A1 and A3 stated (cooling towers; air-cooled PAC / air-based chillers);
     India PUE 1.466 (FY2023-24); RE share 0.23 % stated.
   - ST Telemedia GDC India: Renewable Energy Factor 59.6 %.
   Rule applied: a fleet-wide architecture statement counts (design standard); PUE and renewable
   share count only when India-scoped, because a global average does not bound Indian facilities.
2. An operator may now state several classes without per-facility allocation. Its interval is the
   hull of those classes, and the information value of per-facility architecture is the mean
   narrowing to each stated class (previously any stated class earned zero further value).
3. The +-50 % sensitivity loop now recomputes the baseline U_j under the rescaled widths and also
   rescales the unknown-architecture hull for PUE (previously it compared against unscaled
   baselines and left the PUE hull unscaled).
4. BRSR status of renewable share corrected to "yes": BRSR Principle 6 Essential Indicator 1
   requires energy consumed from renewable and non-renewable sources.

Run with ORIGINAL=1 to reproduce the published (uncorrected) numbers.
"""
import json
import os
import sys

EWIF_FULL = (1.99, 3.77)          # CEA primary, hydro excluded

# architecture class -> (WUE_site interval, PUE interval across zones)
CLS0 = {
    "A1": ((1.40, 2.20), (1.34, 1.52)), "A2": ((1.80, 2.60), (1.26, 1.48)),
    "A3": ((0.00, 0.05), (1.52, 2.02)), "A4": ((0.40, 1.00), (1.38, 1.70)),
    "A5": ((0.00, 0.15), (1.20, 1.52)), "A6": ((0.00, 0.10), (1.14, 1.45)),
}
CLS = dict(CLS0)


def hull(classes):
    w = (min(CLS[c][0][0] for c in classes), max(CLS[c][0][1] for c in classes))
    p = (min(CLS[c][1][0] for c in classes), max(CLS[c][1][1] for c in classes))
    return w, p


def U(w, p, e):
    lo, hi = w[0] + p[0] * e[0], w[1] + p[1] * e[1]
    return (hi - lo) / (0.5 * (hi + lo)), lo, hi


# arch: tuple of stated classes, or () if none | pue: India PUE value disclosed
# wue_bnd: WUE with stated boundary + denominator | zone: facility locations resolvable
# ppa: India-scoped renewable share of supply disclosed
OPS_ORIGINAL = {
    "Adani (AdaniConneX)":   dict(arch=(),     pue=False, wue_bnd=False, zone=False, ppa=False),
    "Amazon (AWS)":          dict(arch=("A2",), pue=False, wue_bnd=False, zone=False, ppa=False),
    "Bharti Airtel (Nxtra)": dict(arch=(),     pue=False, wue_bnd=False, zone=True,  ppa=False),
    "CtrlS":                 dict(arch=(),     pue=False, wue_bnd=False, zone=True,  ppa=False),
    "Google":                dict(arch=(),     pue=False, wue_bnd=False, zone=False, ppa=False),
    "Microsoft":             dict(arch=("A4",), pue=False, wue_bnd=False, zone=False, ppa=False),
    "NTT DATA":              dict(arch=(),     pue=False, wue_bnd=False, zone=False, ppa=False),
    "Sify":                  dict(arch=("A5",), pue=True,  wue_bnd=False, zone=True,  ppa=False),
    "ST Telemedia GDC":      dict(arch=("A3",), pue=False, wue_bnd=False, zone=True,  ppa=False),
}
OPS_CORRECTED = {
    "Adani (AdaniConneX)":   dict(arch=(),                pue=False, wue_bnd=False, zone=False, ppa=False),
    "Amazon (AWS)":          dict(arch=("A2",),           pue=False, wue_bnd=False, zone=False, ppa=False),
    "Bharti Airtel (Nxtra)": dict(arch=("A1", "A3"),      pue=False, wue_bnd=False, zone=True,  ppa=True),
    "CtrlS":                 dict(arch=("A1", "A3"),      pue=True,  wue_bnd=False, zone=True,  ppa=True),
    "Google":                dict(arch=(),                pue=False, wue_bnd=False, zone=False, ppa=False),
    "Microsoft":             dict(arch=("A2", "A5"),      pue=False, wue_bnd=False, zone=False, ppa=False),
    "NTT DATA":              dict(arch=(),                pue=False, wue_bnd=False, zone=False, ppa=False),
    "Sify":                  dict(arch=("A1", "A3", "A4"), pue=True, wue_bnd=False, zone=True,  ppa=True),
    "ST Telemedia GDC":      dict(arch=("A1", "A3"),      pue=False, wue_bnd=False, zone=True,  ppa=True),
}
ORIGINAL = os.environ.get("ORIGINAL") == "1"
OPS = OPS_ORIGINAL if ORIGINAL else OPS_CORRECTED

ATTRS = ["arch", "pue", "wue_bnd", "zone", "ppa"]
LABEL = {"arch": "Heat-rejection architecture, per facility (A1-A6)",
         "pue": "PUE (India portfolio or facility)",
         "wue_bnd": "WUE-site with stated boundary + denominator",
         "zone": "Facility location / climate zone",
         "ppa": "Renewable share of electricity supply"}
MANDATED = {"arch": False, "pue": False, "wue_bnd": False, "zone": True,
            "ppa": False if ORIGINAL else True}


def intervals(d):
    w, p = hull(d["arch"] if d["arch"] else tuple(CLS))
    if d["wue_bnd"]:
        w = (sum(w) / 2,) * 2
    if d["pue"]:
        p = (sum(p) / 2,) * 2
    elif d["zone"] and d["arch"]:
        p = (p[0] + 0.25 * (p[1] - p[0]), p[1] - 0.25 * (p[1] - p[0]))
    if d["ppa"]:
        mid = 0.5 * (EWIF_FULL[0] + EWIF_FULL[1]); half = 0.20 * (EWIF_FULL[1] - EWIF_FULL[0])
        e = (mid - half, mid + half)
    else:
        e = EWIF_FULL
    return w, p, e


def baseline():
    return {n: U(*intervals(d)) for n, d in OPS.items()}


def gain(n, d, a, base_u):
    """Reduction in U_j if attribute a were disclosed by operator n."""
    if a == "arch":
        if len(d["arch"]) == 1:
            return 0.0                                  # single class already known
        cand = d["arch"] if d["arch"] else tuple(CLS)   # narrow to one stated / plausible class
        return sum(base_u - U(*intervals({**d, "arch": (c,)}))[0] for c in cand) / len(cand)
    if d[a]:
        return 0.0
    return base_u - U(*intervals({**d, a: True}))[0]


def info_values():
    b = baseline()
    return {a: sum(gain(n, d, a, b[n][0]) for n, d in OPS.items()) / len(OPS) for a in ATTRS}


if __name__ == "__main__":
    print("INPUTS:", "ORIGINAL (published)" if ORIGINAL else "CORRECTED")
    print(f"{'operator group':<24}{'WUEsrc lower':>13}{'upper':>8}{'U_j':>8}")
    print("-" * 55)
    base = baseline()
    for n, (u, lo, hi) in sorted(base.items(), key=lambda x: x[1][0]):
        print(f"{n:<24}{lo:13.2f}{hi:8.2f}{u:8.3f}")
    print("-" * 55)
    mean_u = sum(v[0] for v in base.values()) / len(base)
    print(f"{'MEAN':<24}{'':13}{'':8}{mean_u:8.3f}\n")

    iv = info_values()
    tot = sum(iv.values())
    print("MARGINAL INFORMATION VALUE  (mean reduction in U if the attribute were required)")
    print("-" * 78)
    print(f"{'attribute':<46}{'IV (dU)':>9}{'share':>8}{'BRSR?':>8}")
    for a, v in sorted(iv.items(), key=lambda x: -x[1]):
        print(f"{LABEL[a]:<46}{v:9.3f}{v / tot:8.1%}{'yes' if MANDATED[a] else 'NO':>8}")
    print("-" * 78)

    print("\nSENSITIVITY (+-50% on all class interval widths) - does the grouping hold?")
    sens = {}
    for scale in (0.5, 1.0, 1.5):
        CLS.clear()
        CLS.update({k: ((v[0][0], v[0][0] + scale * (v[0][1] - v[0][0])),
                        (v[1][0], v[1][0] + scale * (v[1][1] - v[1][0]))) for k, v in CLS0.items()})
        r = info_values(); t = sum(r.values())
        order = sorted(r.items(), key=lambda x: -x[1])
        sens[scale] = {a: round(v / t, 4) for a, v in r.items()}
        print(f"  scale {scale:4.1f}: " + ", ".join(f"{a} {v / t:.1%}" for a, v in order))
    CLS.clear(); CLS.update(CLS0)

    out = os.environ.get("OUT")
    if out:
        json.dump({"ops": {n: dict(lo=round(lo, 2), hi=round(hi, 2), u=round(u, 3))
                           for n, (u, lo, hi) in base.items()},
                   "mean_u": round(mean_u, 3),
                   "iv": {a: dict(iv=round(v, 3), share=round(100 * v / tot, 1),
                                  mandated=MANDATED[a], label=LABEL[a]) for a, v in iv.items()},
                   "sensitivity": sens}, open(out, "w"), indent=1)
