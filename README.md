# Water, Not Watts — data and code

Replication material for **"Water, Not Watts: Re-examining the Water Footprint of
Liquid-Cooled AI Data Centres in India."**

A disclosure audit of 18 public sustainability, ESG and BRSR documents from nine Indian and
hyperscale data centre operator groups, plus an interval estimator that quantifies what
incomplete disclosure costs in litres. Everything needed to regenerate every number, table and
figure in the paper is here. No third-party Python packages required.

---

## Quick start

```bash
python3 scripts/ewif_india.py     # grid EWIF: 2.30 L/kWh, band 1.99–3.77
python3 scripts/breakeven.py      # source WUE by class and zone, break-even EWIF*
python3 scripts/info_value.py     # feasible intervals, U_j, information-value ranking
```

Each script prints the table it generates. Python 3.8+, standard library only.

## Contents

| Path | What it is |
|---|---|
| `master_audit.csv` | The coded audit. One row per document — 18 in sample, 1 excluded — with withdrawal and consumption volumes, WUE, PUE, cooling architecture, water source class, and both the rule-derived and first-pass disclosure tier. |
| `corrections_log.md` | Every departure from the first-pass coding, with justification: two malformed-CSV repairs, a tier miscoded against the wrong standard, a dimensionally invalid WUE figure, an out-of-sample document, and a systematic tier re-derivation that disagreed with the manual pass in 6 of 18 cases. |
| `coded-source/` | Raw first-pass coding output, unmodified — one summary and one details file per document, so the corrections log can be checked against what it corrected. |
| `scripts/ewif_india.py` | Grid electricity water intensity factor from the CEA generation record × NREL consumption factors, across four coal-fleet scenarios. |
| `scripts/breakeven.py` | Source WUE per heat-rejection class per climate zone, and the break-even grid intensity at which dry cooling stops saving water. |
| `scripts/info_value.py` | Feasible-set interval estimator, uncertainty ratio $U_j$, and marginal information value of each disclosure attribute. |

## Which script makes which table or figure

| Paper object | Script |
|---|---|
| Table II — class parameters | `breakeven.py` |
| Table VI — EWIF by scenario | `ewif_india.py` |
| Table VII — feasible intervals and $U_j$ | `info_value.py` |
| Table VIII — information value | `info_value.py` |
| Table IX — break-even by zone | `breakeven.py` |
| Figures 1(c), 2, 3, 4 | `breakeven.py` + `ewif_india.py` |
| Figure 5 | `info_value.py` |

## Provenance

`master_audit.csv` names the source document for every row. The matching
`coded-source/*_details.txt` carries the verbatim quotation, PDF page and printed page for each
extracted field. Every figure in the paper therefore traces to a page in a named public
document.

The 19 source disclosures are public operator publications and are not redistributed here.
Each is cited individually in the paper and retrievable from the operator's own site.

## External data

- **Generation mix** — Central Electricity Authority, *Executive Summary on Power Sector,
  March 2025*, p. 22, Table 1, April 2024 to March 2025 achievement column, plus the Renewable
  Energy Generation table on the same page. All-India achieved generation 1,829,697.94 MU.
- **Water consumption factors** — Macknick, Newmark, Heath and Hallett, *A Review of
  Operational Water Consumption and Withdrawal Factors for Electricity Generating
  Technologies*, NREL/TP-6A20-50900 (2011), median values.
- **Regulatory limits** — MoEFCC notification S.O. 3305(E), 7 December 2015, as substituted by
  G.S.R. 593(E), 28 June 2018.

## Known limitations

The class-level $\mathrm{WUE_{site}}$ and PUE parameters in `breakeven.py` are
literature-derived representative values, not measurements from Indian facilities — no such
measurements are public, which is one of the paper's findings. CEA reports thermal generation
as a single block, so the coal–gas split is assumed at roughly 2 % gas. Hydropower reservoir
evaporation is excluded from the headline EWIF and reported separately; including it moves the
band from 1.99–3.77 to 3.42–5.20 L/kWh.

## Citation

If you use this material, please cite the paper. A BibTeX entry will be added here once the
paper has a DOI or preprint identifier.
