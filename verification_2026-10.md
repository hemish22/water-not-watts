# Source verification, October 2026

**Date:** 15 October 2026
**Basis:** a second, complete verification pass in October 2026. Every coded cell in `coded-source/` was checked against its source PDF page; quotations were searched programmatically, every number was located in its source table, and charts were rendered and read where text extraction was ambiguous. Two image-only PDFs were OCR'd.
Page numbers below are the **printed** page numbers in each source report.

The previous audit table is kept as `archive/master_audit_2026-09.csv`; `scripts/build_corrected_audit.py` applies every correction below to it and regenerates `master_audit.csv`. The first-pass coding in `coded-source/` is unchanged.

---

## A. Errors in the audit data (fed the tiers, the consistency section and Fig. 6)

| # | Document | Was | Source says | Effect on paper |
|---|---|---|---|---|
| A1 | NTT DATA 2025 (FY2024) | Withdrawal and consumption "not reported"; tier T1 | Data-centre withdrawal 3.84 M m³ and consumption 1.12 M m³ (p.99; TNFD table p.43); source split; PUE 1.38; WUE boundary in footnote 7 | Tier T1→**T2**. Document tiers **T1×4, T2×11, T3×3** (were ×5, ×10, ×3) |
| A2 | Google 2025 | Withdrawal "not reported"; consumption "ambiguous, DCs + offices" | p.110–111: withdrawal 11,011 Mgal; data-centre-only W/D/C; per-site W/D/C for 36 named locations, none in India; potable / non-potable / reclaimed split | Text now says Google is the most granular hyperscaler but has no Indian site. Tier unchanged (T2) |
| A3 | NTT DATA 2024 | Japan-only 413,779 / 203,297 m³ treated as the only volumes | Global direct operations: W 2,098k, C 1,371k m³ (p.41) | Corrected in data. Tier unchanged |
| A4 | Sify Technologies FY25 | "WUE 1%" was called a dimensionally invalid WUE (old finding C3) | p.19 is a KPI panel of **year-on-year changes with ▲/▼ arrows** ("WUE … 1% ▼", "per-employee consumption 96% ▼") | **Old C3 withdrawn.** Now reported as "WUE never disclosed, only its change" |
| A5 | Nxtra FY25 | C > W called "physically impossible" | Same page: recycled 15,329 kL; 201,028 + 15,329 = 216,357 **exactly** → gross use. Discharge also given as both 9,306 kL (p.39) and 91,306 kL (GRI factsheet, p.110) | C1 kept, now with the mechanism; adds a C3 failure (repeated quantity disagrees) |
| A6 | Sify Infinit FY25 | "Only operator disclosing W, C, WUE, PUE, energy"; "reader cannot determine which boundary" | p.52: unmetered DC sites were **estimated from headcount** at 45 L/person/day with a 50/50 C/D split. Consumption = discharge exactly; W − C − D = 27,000 kL. WUE printed without a unit. NTT DATA 2025 also discloses all five metrics, but globally | C2 rewritten with the stated mechanism; C1 failure added; "only" now says "only India-scoped" |
| A7 | ST Telemedia GDC CY2023 | not tested | Assured W 1,059,011 m³ (p.61) vs SASB 1,030,852 + 1,444 = 1,032,296 m³ at 100% coverage (p.71). CY2024 reconciles exactly (p.63 vs p.76) | **New C3 failure.** Groups failing are still three of nine (Nxtra, Sify, STT), but a different three |
| A8 | Adani BRSR | treated as AdaniConneX water | Boundary is consolidated Adani Enterprises: mining, airports, roads, copper, solar, defence and DCs (p.349) | Boundary caveat added. Tier unchanged |
| A9 | Bharti Airtel BRSR | grouped as Nxtra water | "Standalone basis – Bharti Airtel Limited" (Q13), so the Nxtra Data subsidiary is excluded | Boundary caveat added. Group tier unchanged (Nxtra FY25 is T3 on its own) |
| A10 | Tier-rule disagreements | "6 of 18" | The original CSV already had a 7th (STT CY2024, T1→T2) that the log omitted; NTT 2025 adds an 8th. All are upward | Now **"8 of 18"** |
| A11 | Architecture column (Table VI) | Microsoft "Yes", STT "Yes", CtrlS "No"; "four of nine name no class" | No group allocates classes per facility. 3 name none, 5 name several, Amazon names one (A2) | Column relabelled one / several / none; text says three of nine |
| A12 | CtrlS FY2022–23 | — | GRI index cites 303-3 withdrawal at pp.33–34, but those pages show consumption only | New observation added |

## B. Errors in the uncertainty-model inputs (changed U_j, the IV ranking and Fig. 5)

`scripts/info_value.py` keeps the model of the September version. Run it with `ORIGINAL=1` and it reproduces the old numbers exactly. Only the inputs are corrected:

| Group | Old input | Corrected input | Evidence |
|---|---|---|---|
| Microsoft | A4 | A2 + A5 (several) | A4 has no support in the report. Evaporative fleet and closed-loop DTC are both on p.35 |
| Sify | A5, PUE | A1 + A3 + A4, PUE, India renewable share | Water-cooled condensers (p.52); closed-loop air-cooled chillers (p.53); adiabatic (p.93); ~38% renewable (p.30). A5 is not stated anywhere |
| ST Telemedia GDC | A3 | A1 + A3, India renewable share | Cooling-tower reuse and air-cooled chillers (India p.23); India REF 59.6% (p.8) and 49% (CY23 p.58) |
| Bharti Airtel (Nxtra) | none | A1 + A3, India renewable share | Cooling towers (p.40); air-based chillers (p.41); 49% renewable (p.13) |
| CtrlS | none | A1 + A3, India PUE, India renewable share | Cooling-tower fills (p.33); air-cooled PAC and chillers (pp.14, 36); PUE 1.490 / 1.466 (FY23 p.29; FY24 p.34); renewable 0.23% (p.32) |

Rules that are now stated in the paper:

- Several named classes give the hull of their intervals.
- PUE and renewable share count only when India-scoped.

Two bugs in the old ±50% sensitivity loop were also fixed:

- It did not recompute the baseline U_j at each scale.
- It did not rescale the PUE hull.

**Result**

| | Old | Corrected |
|---|---|---|
| Mean U_j | 1.021 | **0.906** |
| Groups at the full 2.27–10.22 interval | 5 | **3** (Adani, Google, NTT DATA) |
| Best constrained | Sify 0.644 | **CtrlS and Sify, 0.572** |
| Top attributes | four at 22–28% each | **WUE-with-boundary 35.5%, architecture 33.7%**, PUE 17.0%, renewable share 12.6%, location 1.3% |
| BRSR status of renewable share | "No" | **Yes**: BRSR Principle 6 EI-1 requires the renewable / non-renewable energy split |
| BRSR status of location | "Yes" | **Count only**: Section A Q18 asks for the number of locations, not the sites |
| Policy headline | 4 unrequired fields; 98.7% bracket | **3 unrequired fields carry 86.2%**; the two BRSR touches carry 14% |

The paper's conclusion stands: the required fields are the least informative ones. The magnitudes and the list of fields changed.

## C. Other fixes

- **Fig. 1:** the label "≈49% of plants non-compliant" overstated its source. The 2019 Down To Earth piece reports 30 of 156 plants/units admitting non-compliance, and "about 51%" shown compliant. The label is now "≈51% shown compliant (2019)" and the text gives the numbers.
- **Bibliography `dte2019noncompliance`:** the analysis was by Manthan Adhyayan Kendra (RTI data), not the Centre for Science and Environment. Authors are now Dharmadhikary and Raheja.
- **Fig. 2:**
  - A5 was annotated "lowest source WUE in every zone". A6 is lowest; the annotation now says so.
  - The A3 note "claimed by most Indian operators as water-free" now reads "described by all four Indian colocation groups for new or retrofitted capacity".
- **Bibliography titles:**
  - NTT DATA 2025 "Corporate Brochure" → **Case Book**.
  - NTT DATA 2024 → **Data Book (FY2023)**.
  - NTT DATA 2025 main report is not a "Data Book".
- **Limitations:** the single-coder paragraph now reports what the second verification pass found. The coarse renewable-share treatment is now stated.

## D. Not changed

Unchanged in the paper:

- The taxonomy, the EWIF derivation (1.99–3.77 L/kWh, central 2.30)
- The class parameters, the break-even analysis (EWIF* 4.00 / 5.45 / 8.18)
- The A3–A5 gap (restated as 0.99 L/kWh in §G) and Figs. 3–4

None of these depend on the coded documents.

## E. New

- **Fig. 6** (full version only): a document-level audit matrix covering all 18 documents, the 7 disclosure fields, the tier and the consistency result. Every cell was checked against its source page; the comments in `figures/fig6_audit.py` give the page for each row.

## F. Second round (15 Oct 2026): external sources checked, reproducibility

| # | Was | Now | Evidence |
|---|---|---|---|
| F1 | "India's 2.30 L/kWh is ≈1.3× the US average used by Li et al." (text and Fig. 1) | Li et al. use **3.14 L/kWh** for the US, and that figure *includes* hydropower. Like-for-like, India's hydro-included S2 (3.72–3.74) is **≈1.2×**. On the hydro-excluded basis the old sentence was backwards: 2.30 is 0.73× of 3.14 | Li et al., arXiv 2304.03271 §3: "average EWIF … 3.14 L/kWh … [8] includes hydropower" |
| F2 | "MoEFCC 2015 notification caps … 3.0 thereafter" | The 3.0 m³/MWh limit for post-2017 plants comes from the **2018 amendment** (G.S.R. 593(E)). The 2015 text set 2.5 | CERC order 66/MP/2021; Lok Sabha AU3728; Manthan comments on the 2017 draft |
| F3 | Full version: "half of data centre capacity is warm-humid"; Fig. 2 "≈50% of capacity" | **≈70%**: Mumbai 53% + Chennai 20% of ~1,530 MW (Jan–Sep 2025). A citation was added (`cbre2025dc`) | CBRE "India's Data Centre Market in a New Era", via W.Media, 13 Nov 2025 |
| F4 | NREL thermosyphon "demonstrated exactly this substitution" (an A5-type result) | It is a dry cooler *ahead of the cooling towers*: a hybrid that **halved** on-site water over 24 months. It does not show elimination, so the text now calls it a partial version | NREL/TP-2C00-72196 and the NREL/LBNL summaries |
| F5 | Bibliography: Sickinger et al., co-author "Chuck Belmont" | **Suzanne Belmont**; the title wording is also corrected | NREL report front matter |
| F6 | Table I (5-page) / Table II (full) gave point values only, yet the paper said every interval could be recomputed by hand | The tables now print the **estimator intervals** (e.g. A1 WUE_site 1.40–2.20, PUE 1.34–1.52). The 5-page version also states the disclosure rules (PUE fixes the term, location halves the PUE range, renewable share narrows EWIF to its central 40%, a bounded WUE fixes the site term) | `scripts/info_value.py` |
| F7 | 5-page: "failed in an earlier draft"; full: "One apparent failure in an earlier draft" | Reworded with no reference to an earlier draft | n/a |
| F8 | 5-page ST Telemedia C3 sentence gave no gap figure | Now gives the 26,715 m³ gap and cites the CY2024 report that reconciles | STT CY2023 pp.61, 71; CY2024 pp.63, 76 |

**Checked and found correct.**

- **Privette et al. 2026:** AGU Advances 7, e2025AV002140; authors Privette, Barros and Cai.
- **CEA FY2024–25:** thermal 1,363.89 BU (coal/lignite 1,331,867 + gas 31,580 + diesel 443 GWh), hydro 148.63 BU, nuclear 56.68 BU, all per the CEA Growth Book 2025. Gas share 2.3% ✓.
- **Macknick medians:** coal tower 687, nuclear tower 672, hydro 4,491 and biopower 553 gal/MWh ✓. The NGCC tower median is 205 in the 2012 ERL version against 198 used here; the effect is under 0.002 L/kWh.

**Confirmed in the third round (16 Oct 2026).** The two figures that could not be checked before are now confirmed:

- **Bhutan import 5.48 BU.** CEA Sub-Report 4, *Energywise performance status, all India*, March 2025 (published on npp.gov.in), row "BHUTAN IMP", April 2024 – March 2025: 5,484.18 GWh. The same table gives thermal 1,363,889.7, nuclear 56,680.83 and hydro 148,633.98 GWh, and a conventional total of 1,574,688.75 GWh.
- **Renewables 255.01 BU.** 255,009.19 GWh for 2024–25, from the CEA Annual Report series (Ministry of Power data, via Dataful).
- **Total.** 1,574,688.75 + 255,009.19 = 1,829,697.94 GWh, exactly the total the paper uses.

## G. Third round (16 Oct 2026): consistency, layout, clean codes

| # | Was | Now | Why |
|---|---|---|---|
| G1 | A3 4.37 vs A5 3.38, "a gap of 0.98 L/kWh" (text ×4, Fig. 2, Fig. 5 in the full paper) | Gap **0.99 L/kWh** | Exact values are 4.370, 3.385 and 0.985. The printed figures subtract to 0.99, so the gap now matches what a reader can check. No other number changes |
| G2 | Fig. 5 (`fig3_stacked`): the "water-free" bracket and label sat over A3's EWIF whisker and hid its upper end (7.2) | Callout moved right of the whisker; x-axis extended to 11 | Layout only |
| G3 | Full paper, Table I (Axis A): 10 pt overfull line | Column spacing tightened to 4 pt | Layout only |
| G4 | CEA renewables (255.01 BU) and Bhutan import (5.48 BU) not independently confirmed | Both confirmed; see the note under §F | CEA Sub-Report 4, March 2025; CEA Annual Report data |
| G5 | The first-pass `*_details.txt` files have 10 malformed rows and some wrong codes | New file `data/coded_details_verified.csv`, built by `scripts/build_verified_details.py`: 168 rows, 119 verified, 29 corrected, 20 added. Every quote was matched against the source text. The raw files are unchanged | October 2026 verification |
