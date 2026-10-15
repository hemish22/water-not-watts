# Water, Not Watts — data and code

Replication material for **"Water, Not Watts: Re-examining the Water Footprint of
Liquid-Cooled AI Data Centres in India"** and its short version, **"Water, Not Watts: What
Indian Data Centre Disclosure Cannot Say About Water."**

The material has three parts:

- a disclosure audit of 18 public sustainability, ESG and BRSR documents from nine Indian and hyperscale data centre operator groups;
- the Indian grid water-intensity derivation;
- an interval estimator that turns incomplete disclosure into a range of possible water use, in litres per kWh.

This repository holds everything needed to regenerate every number, table and figure in the paper.

> **October 2026: source verification.** Every coded cell was re-checked against its source
> page in a second, complete pass, and the corrected audit table now feeds all results. The full
> list of corrections and the evidence for each is in [`verification_2026-10.md`](verification_2026-10.md).
>
> Headline changes:
> - **Document tiers** are now T1×4, T2×11, T3×3 (were T1×5, T2×10, T3×3).
> - **Mean uncertainty ratio** is now 0.906 (was 1.021).
> - **Disclosure fields that matter most:** a WUE with a stated boundary (35.5%) and per-facility heat-rejection architecture (33.7%). Before, four fields at 22–28% each.
> - **Consistency failures:** Nxtra FY25, Sify Infinit FY25 and ST Telemedia CY2023.
> - **Withdrawn:** the Sify Technologies "dimensionally invalid WUE" finding. That figure is a year-on-year change, not a WUE value.

---

## Quick start

```bash
python3 scripts/ewif_india.py                 # grid EWIF: 2.30 L/kWh, band 1.99–3.77
python3 scripts/breakeven.py                  # source WUE by class and zone, break-even EWIF*
python3 scripts/build_corrected_audit.py      # archive table + verified corrections -> master_audit.csv, tiers
OUT=data/info_value_results.json python3 scripts/info_value.py   # intervals, U_j, information value
ORIGINAL=1 python3 scripts/info_value.py      # reproduces the September 2026 (pre-verification) numbers
python3 scripts/build_verified_details.py     # coded-source/ -> data/coded_details_verified.csv
cd figures && for f in fig*_*.py; do python3 $f; done              # every figure -> figures/out/
```

The scripts in `scripts/` need only Python 3.8+ and its standard library. The figure scripts in `figures/` also need `matplotlib` and `numpy`.

## Contents

| Path | What it is |
|---|---|
| `master_audit.csv` | The verified coded audit. One row per document: 18 in sample and 1 excluded. Each row holds withdrawal, consumption and discharge volumes; WUE and PUE; India PUE and renewable share where disclosed; cooling architecture; water source class; whether the volumes are attributable to data centres; and both the rule-derived and first-pass tier. The `notes` column gives the page evidence for every corrected row. |
| `verification_2026-10.md` | The October 2026 verification. It lists every correction with the source page, the corrected inputs to the uncertainty model, and the external sources checked. |
| `corrections_log.md` | The September 2026 corrections log, kept for the record. Its header notes which sections were later superseded. |
| `archive/master_audit_2026-09.csv` | The audit table as it stood before verification. |
| `coded-source/` | First-pass coding output, one summary and one details file per document, so each correction can be checked against what it corrected. Ten rows in the `*_details.txt` files contain unquoted commas inside fields (for example Indian digit grouping). They are kept as the first-pass record; use `data/coded_details_verified.csv` for analysis. |
| `data/coded_details_verified.csv` | Every first-pass detail row in one clean CSV: the 10 malformed rows rebuilt, wrong codes corrected, missed disclosures added. A `verification` column (`verified` / `corrected` / `added`) and a note give what changed and the source page. 168 rows: 119 verified, 29 corrected, 20 added. Built by `scripts/build_verified_details.py`. |
| `data/info_value_results.json` | Output of `info_value.py`, read by the Fig. 4 script so the figure cannot drift from the tables. |
| `scripts/ewif_india.py` | Grid electricity water intensity factor from the CEA generation record × NREL consumption factors, across four coal-fleet scenarios. |
| `scripts/breakeven.py` | Source WUE per heat-rejection class per climate zone, and the break-even grid intensity at which dry cooling stops saving water. |
| `scripts/build_corrected_audit.py` | Applies the verified corrections and recomputes document- and group-level tiers with the deterministic rule. |
| `scripts/build_verified_details.py` | Rebuilds `data/coded_details_verified.csv` from `coded-source/`. |
| `scripts/info_value.py` | Feasible-set interval estimator, uncertainty ratio U_j, and the marginal information value of each disclosure attribute. |
| `figures/` | Plotting scripts for every figure; output goes to `figures/out/`. |

## Which script makes which table or figure (full-length paper numbering)

| Paper object | Script |
|---|---|
| Table II — class parameters and estimator intervals | `breakeven.py`, `info_value.py` |
| Table VI — operator-group tiers | `build_corrected_audit.py` |
| Table VII — EWIF by scenario | `ewif_india.py` |
| Table VIII — feasible intervals and U_j | `info_value.py` |
| Table IX — information value | `info_value.py` |
| Table X — break-even by zone | `breakeven.py` |
| Fig. 1 — water pathway | `figures/fig1_pathway.py` |
| Fig. 2 — class × zone matrix | `figures/fig2_matrix.py` |
| Fig. 3 — audit at a glance | `figures/fig6_audit.py` |
| Fig. 4 — intervals and information value | `figures/fig5_infovalue.py` |
| Fig. 5 — site and source water by class | `figures/fig3_stacked.py` |
| Fig. 6 — break-even | `figures/fig4_breakeven.py` |

In the 5-page version, Fig. 1 is `fig1_pathway.py` and Fig. 2 is `fig5_infovalue.py`.

## Provenance

`master_audit.csv` names the source document for every row. The matching
`coded-source/*_details.txt` file carries the verbatim quotation and page for each extracted
field, and `verification_2026-10.md` gives the page for every corrected value. Every figure in the
paper therefore traces to a page in a named public document.

The 19 source disclosures are public operator publications and are not redistributed here.
Each is cited individually in the paper and can be retrieved from the operator's own site.

## External data

- **Generation mix** — Central Electricity Authority, *Executive Summary on Power Sector,
  March 2025*, p. 22, Table 1, April 2024 to March 2025 achievement column, plus the Renewable
  Energy Generation table on the same page. All-India achieved generation is 1,829,697.94 MU.
  - Thermal, hydro and nuclear agree with the CEA *Growth Book 2025*.
  - Bhutan import (5,484.18 GWh) and the conventional total are confirmed in CEA Sub-Report 4 for March 2025; renewables (255,009.19 GWh) in the CEA Annual Report series. Conventional plus renewables gives the total exactly.
- **Water consumption factors** — Macknick, Newmark, Heath and Hallett, *A Review of
  Operational Water Consumption and Withdrawal Factors for Electricity Generating
  Technologies*, NREL/TP-6A20-50900 (2011), median values.
  - The coal, nuclear, hydro and biopower medians match the 2012 *Environmental Research Letters* version.
- **Regulatory limits** — MoEFCC notification S.O. 3305(E), 7 December 2015, as substituted by
  G.S.R. 593(E), 28 June 2018.
  - The 3.0 m³/MWh limit for plants installed after 1 January 2017 comes from the 2018 amendment; the 2015 text set 2.5.
- **US comparison** — Li et al. (*Communications of the ACM*, 2025) use 3.14 L/kWh for the
  United States, including hydropower. On that basis, India's hydro-included central scenario is about 1.2× higher.

## Known limitations

- **Class parameters.** The class-level WUE_site and PUE values and their intervals are literature-derived representative values, not measurements from Indian facilities. No such measurements are public, which is one of the paper's findings.
- **Coal–gas split.** CEA reports thermal generation as a single block, so the split is assumed at about 2% gas.
- **Hydropower.** Reservoir evaporation is excluded from the headline EWIF and reported separately; including it moves the band from 1.99–3.77 to 3.42–5.20 L/kWh.
- **Renewable share.** The estimator narrows the EWIF band around its national midpoint rather than shifting it toward an operator's actual supply mix.

## Citation

If you use this material, please cite the paper. A BibTeX entry will be added here once the
paper has a DOI or preprint identifier.
