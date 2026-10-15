# Coded-Data Corrections Log

> **Superseded in part (October 2026).** A complete second verification pass against the source
> PDFs is recorded in [`verification_2026-10.md`](verification_2026-10.md). It withdraws §2.2
> (the Sify Technologies "1%" is a year-on-year change, not a WUE value), revises §2.4 (Nxtra's
> consumption equals withdrawal plus recycled water, a labelling error rather than a physical
> impossibility), corrects §3 (8 of 18 rule-versus-manual disagreements, not 6; NTT DATA 2025
> moves to T2), and corrects §4 (document tiers T1×4, T2×11, T3×3). The September table this log
> describes is kept as `archive/master_audit_2026-09.csv`.

**Paper:** From Cooling Towers to Cold Plates — water footprint of liquid-cooled AI data centres in India
**Date:** 12 September 2026
**Applies to:** `combined codes/*_summary.txt` → `audit/master_audit.csv`

This log exists so the audit is reproducible. Every departure from the raw
first-pass coding is recorded here with its justification. Raw first-pass output is
preserved unmodified in `sources to codes/`.

---

## 1. Structural repairs (malformed CSV)

Two summary files contained unquoted commas inside fields, which shifted every
downstream column and silently corrupted the record on parse.

| File | Fault | Repair |
|---|---|---|
| `nxtra_2025_summary.txt` | `cooling_architecture` contained `"A3 air-cooled chiller, fully dry"` unquoted → 24 fields parsed against a 23-field header | Field quoted |
| `sify-technologies_2025_summary.txt` | withdrawal value `3,06,915.60` (Indian digit grouping) unquoted → 25 fields parsed against a 23-field header | Field quoted; value normalised to 306,915.60 kL |

Both files now parse cleanly. **Anything computed from these two records before
12 Sep is wrong and must be recomputed.**

---

## 2. Content corrections

### 2.1 Sify Infinit Spaces — tier miscoded against the wrong standard
`tier_global` and `tier_india` were recorded as `Tier 3 (ANSI/TIA-942-2017)`.
That is the *facility availability* Tier standard, not this paper's T0–T5
**disclosure** rubric. The two are unrelated axes that share a word.

**Corrected to T3** (India-level withdrawal *and* consumption both reported,
p. 52). It does **not** reach T4: the WUE figure of 1.805 is portfolio-level with
no stated measurement boundary or methodology.

### 2.2 Sify Technologies — WUE figure is dimensionally invalid
Annual Report FY2024-25, p. 19 reports *"Water Usage Efficiency (WUE) in litres) 1%"*,
and on the same page *"Average Water Consumption per employee per month (in liters) 96%"*.
WUE has units L/kWh; a percentage cannot express it.

**The value is retained as verbatim evidence but excluded from all numerical
analysis** (`wue_value` = null, `wue_usable` = NO). This is not a coding error to be
silently dropped — it is a finding, and it is cited in §6.4 as a dimensional-validity
failure.

### 2.3 SEAS / SGTech — out of sample
`sttgdc_2025_clean-energy-adoption-in-data-centres.pdf` is a Singapore industry
position paper on clean-energy adoption, not an operator disclosure. It contains no
water metrics and no Indian facility data.

**Marked `in_sample = NO`.** It may still be cited as background in §2. Sample size
drops from 19 documents to **18**.

### 2.4 Nxtra FY25 — mass-balance violation retained, not repaired
Reported consumption (216,357 kL) exceeds reported withdrawal (201,028 kL), p. 39.
This is physically impossible under the standard definition (consumption is the
non-returned fraction of withdrawal).

**Both figures are retained exactly as published.** The violation is recorded as a
consistency-check failure (§6.4) and is one of the paper's findings. Do not "fix" it
by swapping the values.

---

## 3. Tier re-derivation (systematic, not a one-off correction)

Tier assignment is the paper's headline result, so it was **recomputed
deterministically from the coded fields** rather than taken from the first-pass
manual judgement. The decision rule:

```
T5  if WUE-source or grid water-intensity accounting is reported
T4  if India-level withdrawal AND consumption AND facility-level WUE
    with stated methodology and boundary
T3  if India-level withdrawal AND consumption
T2  if any withdrawal or consumption volume is reported at any
    aggregation level (i.e. volumes exist but not as an India W+C pair)
T1  if only a qualitative water claim and/or a WUE figure, no volumes
T0  if no water disclosure at all
```

The rule disagrees with the first-pass manual tier in **6 of 18 in-sample documents**.
Disagreements are flagged in `master_audit.csv` (`disagree` column) and resolved in
favour of the rule, because the rule is inspectable and the manual judgement is not.

| Document | Manual | Rule | Why the rule wins |
|---|---|---|---|
| Google 2025 | T0 | T2 | A consumption volume *is* reported (8.1 bn gal); it is unallocatable to India, which is exactly what T2 means |
| Microsoft 2025 | T1 | T2 | Global withdrawal and consumption both reported; T1 is reserved for disclosures with no volumes |
| NTT DATA 2024 | T0 | T2 | Volumes reported, but for 14 Japanese facilities only |
| NTT DATA 2025 cb | T0 | T1 | Qualitative water-positivity commitments present |
| Sify Technologies 2025 | T0 | T2 | Withdrawal volume reported (306,915.60 kL) |
| STT GDC India 2025 | T1 | T2 | India-level withdrawal reported (298,595 m³) |

Note that every disagreement moves in the same direction — the manual pass
**under-credited** disclosure. Stating this protects the paper from the obvious
reviewer objection that the audit was tuned to produce a damning result.

---

## 4. Post-correction sample

- **18 documents, 9 operator groups.** Adani (AdaniConneX), Amazon (AWS),
  Bharti Airtel (Nxtra), CtrlS, Google, Microsoft, NTT DATA, Sify,
  ST Telemedia GDC.
- Document-level tiers: **T1 × 5, T2 × 10, T3 × 3.**
- Operator-group tiers (max across that group's documents):
  **T1 × 1, T2 × 6, T3 × 2.**
- **Zero operators reach T4 or T5.** The pre-registered prediction in the plan holds.

Against the plan's Hour-9 checkpoint (12 operators), the realised sample is 9 groups.
This must be stated in Limitations, together with the operators absent from the
sample: Yotta, Web Werks, ESDS, Pi Datacenters, Nxtgen, Equinix, and Digital Realty.
