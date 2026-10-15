"""Build coded_details_verified.csv: the first-pass *_details.txt coding, repaired and corrected.

The raw first-pass files are left untouched. This script reads them and writes one clean,
RFC-4180 CSV in which every row has been checked against its source page (October 2026):

  verification = verified   value, quote and page confirmed as coded
               = corrected  something in the row was wrong; verification_note says what
               = added      a disclosure the first pass missed

Fixes applied to every row:
  - the 10 rows with unquoted commas (Indian digit grouping, a heading, a curly quote) are rebuilt
  - "[cite: N]" artefacts and wrapping quote marks are removed from quotes
  - "_2" suffixes are removed from filenames so they match the source PDFs
  - the mislabelled pdf_page column is dropped; printed_page holds the printed page number

Paths: reads ../coded-source/ (repository) or ../../combined codes/ (working folder);
writes ../data/coded_details_verified.csv.  Override with SRC= and OUT=.
"""
import csv, glob, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.environ.get("SRC") or next(
    p for p in (os.path.join(HERE, "..", "coded-source"), os.path.join(HERE, "..", "..", "combined codes"))
    if os.path.isdir(p))
OUT = os.environ.get("OUT") or os.path.join(HERE, "..", "data", "coded_details_verified.csv")

COLS = ["operator", "document_filename", "field_name", "question_asked", "extracted_answer",
        "verbatim_quote", "printed_page", "section_heading", "verification", "verification_note",
        "source_row"]

# --- 1. The 10 malformed rows, rebuilt field by field (operator and filename come from the file) --
# key: (file stem, line number) -> [field, question, answer, quote, printed_page, heading]
REPAIR = {
 ("microsoft_2025", 12): ["additional_claim", "Are there qualitative claims regarding water savings?",
    "Saving over 125,000 cubic meters", "saving over 125,000 cubic meters of water annually per datacenter",
    "35", "Eliminating water for cooling in new datacenters"],
 ("nttdata_2024", 6): ["additional_claim", "Are there limitations to the water data?", "Yes, limited to Japan",
    "For water resources, it pertains to 14 domestic facilities owned by NTT DATA Japan Corporation.",
    "22", "Summary of Third-Party Certified Data in Fiscal 2023"],
 ("nttdata_2025_cb", 2): ["cooling_architecture", "What cooling technologies are mentioned?",
    "Mentions air cooling and liquid cooling technologies like immersion cooling.",
    "traditional air cooling systems, making the need for liquid cooling technologies such as direct "
    "liquid cooling and immersion cooling more acute.", "6", "Business need"],
 ("nxtra_2025", 8): ["cooling_architecture", "What cooling architecture is used?", "MENTIONED_NO_DETAIL",
    "Proven concepts tested with multiple OEMs for direct-to-chip and single/dual-phase liquid immersion cooling",
    "26", "FUTURE-FIRST INFRASTRUCTURE, BUILT TODAY"],
 ("sify-infinit-spaces-limited_2025", 2): ["water_withdrawal_value",
    "What is the total water withdrawal value for FY 2024-25?", "2,96,279 kL",
    "2,96,279 kL Total Water Withdrawal", "52", "Water Management"],
 ("sify-infinit-spaces-limited_2025", 3): ["water_consumption_value",
    "What is the total water consumption value for FY 2024-25?", "1,34,639.5 kL",
    "1,34,639.5 kL Water Consumption", "52", "Water Management"],
 ("sify-infinit-spaces-limited_2025", 6): ["total_energy_consumption",
    "What is the total energy consumption for FY 2024-25?", "65,39,17,445 kWh",
    "65,39,17,445 kWh Total energy consumption", "6", "Highlights"],
 ("sify-infinit-spaces-limited_2025", 8): ["scope_1_2_emissions",
    "What are the total Scope 1 and Scope 2 GHG emissions?", "3,00,835.73 metric tons",
    "Total Carbon Emissions 3,00,835.73 metric tons", "51", "Environment"],
 ("sify-infinit-spaces-limited_2025", 9): ["waste_generated", "What is the total waste generated and disposed?",
    "444,094.38 kg", "Total Waste Generated # 444,094.38 kg", "55", "Waste Management"],
 ("sify-technologies_2025", 2): ["water_withdrawal_value", "How much water did the company withdraw?",
    "3,06,915.60", "Water withdrawal (kl) 3,06,915.60", "2", "Environment"],
}
REPAIR_NOTE = "row rebuilt: unquoted comma split it into extra columns"

# --- 2. Corrections and notes on well-formed rows ------------------------------------------------
# key: (file stem, line) -> dict of column overrides; "status" defaults to corrected if any value
# column changes, else verified.  "note" is appended to verification_note.
FIX = {
 ("adani_2025", 6): {"note": "boundary is consolidated Adani Enterprises (mining, airports, roads, copper, "
                     "solar, defence, data centres; p.349), so this is not data-centre water"},
 ("adani_2025", 7): {"note": "same consolidated boundary as withdrawal; not data-centre water"},
 ("adani_2025", 8): {"extracted_answer": "S2;S4;third-party;surface",
                     "note": "third-party 17,35,795 kL (30% of withdrawal) and surface 59,108 kL were omitted"},
 ("adani_2025", 9): {"verbatim_quote": "Aiming to become a Net Water Positive by 2035, in businesses wherever "
                     "feasible.", "note": "quote restored to source wording ('a' had been dropped)"},
 ("bal_2025", 2): {"note": "reporting boundary is 'Standalone basis - Bharti Airtel Limited' (Q13), so Nxtra "
                   "Data is excluded; not data-centre water. Unit: million litres"},
 ("bal_2025", 3): {"note": "standalone boundary, excludes Nxtra; unit: million litres"},
 ("bal_2025", 5): {"note": "third-party water coded as S1 is an interpretation; the report does not say municipal"},
 ("ctrls_2022", 3): {"note": "blow-down implies evaporative towers, but no class is stated; the corrected audit "
                     "does not credit an architecture for this document"},
 ("ctrls_2023", 4): {"extracted_answer": "A1", "note": "cooling towers named: coded A1, consistent with STT and Nxtra"},
 ("ctrls_2023", 7): {"note": "source is OCR'd (image-only PDF); 'policies' sits on a line break"},
 ("ctrls_2023", 8): {"printed_page": "34", "note": "page corrected 33 -> 34"},
 ("ctrls_2024", 3): {"extracted_answer": "A3", "note": "water-cooled to air-cooled PAC: coded A3"},
 ("ctrls_2024", 4): {"extracted_answer": "A1", "note": "cooling-tower fills: coded A1"},
 ("ctrls_2024", 5): {"extracted_answer": "A3", "note": "air-based chillers: coded A3, consistent with Nxtra FY25"},
 ("ctrls_2024", 10): {"extracted_answer": "Quantified claim: water footprint down 119,662 KL per year",
                      "note": "was coded 'T1 qualitative claim', but the claim is quantified"},
 ("google_2025", 2): {"verbatim_quote": "In 2024, we consumed a total of approximately 8.1 billion gallons (31 "
                      "billion liters or 31 million cubic meters) of water across our data centers (excluding "
                      "those operated by third parties) and offices.",
                      "note": "quote completed: the figure covers data centres and offices; the data-centre-only "
                      "figure (7,787 Mgal, p.110) is in the added rows"},
 ("microsoft_2025", 7): {"printed_page": "36", "note": "page corrected 35 -> 36"},
 ("microsoft_2025", 9): {"extracted_answer": "withdrawal",
                         "note": "the quote itself says 'withdrawal water usage effectiveness'"},
 ("microsoft_2025", 10): {"extracted_answer": "A2;A5",
                          "note": "A4 (dry cooler + adiabatic) has no support in the report. A5 is approximate: "
                          "closed-loop direct-to-chip rejecting to chillers"},
 ("nttdata_2024", 4): {"note": "Japan only (14 domestic facilities); the global figure is in the added rows"},
 ("nttdata_2024", 5): {"note": "Japan only (14 domestic facilities); the global figure is in the added rows"},
 ("nttdata_2024", 6): {"note": "the limitation applies to this table only; global direct-operations volumes "
                       "are reported on p.41"},
 ("nttdata_2024", 7): {"note": "quote omits the footnote markers *1 and *2 after DCLC and LIC"},
 ("nttdata_2024", 8): {"note": "quote omits the footnote markers *1 and *2 after DCLC and LIC"},
 ("nttdata_2025_db", 3): {"note": "quote joins a line-break hyphen ('consump-tion')"},
 ("nttdata_2025_cb", 4): {"note": "context is a client case study (MeetZero water-credit product), not an NTT "
                          "DATA commitment"},
 ("nttdata_2025_db", 5): {"extracted_answer": "consumption",
                          "note": "consumption per unit of IT power; boundary stated in footnote *7 (p.99); quote joins a "
                          "line-break hyphen ('consump-tion')"},
 ("nxtra_2024", 6): {"extracted_answer": "A1;A3",
                     "note": "air-based chillers = A3, cooling-tower blowdown = A1; consistent with Nxtra FY25"},
 ("nxtra_2025", 4): {"note": "equals withdrawal 201,028 + recycled 15,329 exactly: gross use, not GRI 303-5 "
                     "consumption"},
 ("seas-sgtech_2025", 6): {"printed_page": "2", "note": "page corrected 5 -> 2 (also pp.26-28); out of sample"},
 ("sify-infinit-spaces-limited_2025", 2): {"note": "metered sites plus headcount-based estimates for unmetered "
                                           "DC sites (p.52)"},
 ("sify-infinit-spaces-limited_2025", 3): {"note": "equals discharge exactly; W - C - D leaves 27,000 kL"},
 ("sify-infinit-spaces-limited_2025", 4): {"note": "printed without a unit"},
 ("sify-infinit-spaces-limited_2025", 5): {"extracted_answer": "300+ MW",
                                           "verbatim_quote": "300+ MW Green power contracted",
                                           "printed_page": "7", "note": "source says 300+ MW on p.7"},
 ("sify-infinit-spaces-limited_2025", 8): {"note": "source-side: Scope 1 13,422.22 + Scope 2 2,94,493.50 = "
                                           "3,07,915.72, not the reported total"},
 ("sify-technologies_2025", 2): {"note": "company-wide; FY24 was 61,32,323 kl, a 95% fall not explained in "
                                 "the report"},
 ("sify-technologies_2025", 4): {"extracted_answer": "NO",
                                 "note": "only a year-on-year change in WUE is given; the WUE itself is not "
                                 "disclosed"},
 ("sify-technologies_2025", 5): {"extracted_answer": "NOT DISCLOSED",
                                 "note": "'1%' is a year-on-year change (with a down arrow) in a KPI panel of "
                                 "changes, not a WUE value"},
 ("sify-technologies_2025", 6): {"extracted_answer": "96% (year-on-year change)",
                                 "note": "a year-on-year change, like every figure in this KPI panel"},
 ("stt_2023", 3): {"note": "read from chart labels; also in the CY2024 report's data table"},
 ("stt_2023", 10): {"note": "India table, CY2023 column (CY2022: 419,204 m3); quote rebuilt from table cells"},
 ("stt_2023", 11): {"note": "SASB table: data centres 1,030,852 + offices 1,444 = 1,032,296 m3, 26,715 m3 below "
                    "the assured withdrawal 1,059,011 (p.61)"},
 ("stt-gdc_2024", 3): {"note": "read from chart labels; same value in the data table on p.63"},
 ("stt-gdc_2024", 10): {"note": "formula retypeset onto one line; ISO 30134 consumption-based WUE"},
 ("stt-gdc-india_2025", 9): {"note": "read from chart labels"},
}

# --- 3. Disclosures the first pass missed --------------------------------------------------------
# [stem, field, question, answer, quote, printed_page, heading, note]
ADD = [
 ["google_2025", "water_withdrawal_value", "What is the total water withdrawal?", "11,011 million gallons",
  "Water withdrawal 5,689 6,297 7,600 8,653 11,011", "110", "Appendix: Water",
  "2024 is the last column; the coding had 'NOT REPORTED'"],
 ["google_2025", "water_withdrawal_value", "What is the data-centre-only water withdrawal?",
  "9,866 million gallons (data centres only)", "Data centers 9,866 2,079 7,787", "110", "Appendix: Water",
  "withdrawal / discharge / consumption for data centres only; per-site table for 36 locations on pp.110-111, "
  "none in India"],
 ["google_2025", "water_consumption_value", "What is the data-centre-only water consumption?",
  "7,787 million gallons (data centres only)", "Data centers 9,866 2,079 7,787", "110", "Appendix: Water", ""],
 ["google_2025", "water_source", "What are the water sources?",
  "S1 potable 7,699; non-potable 1,289; S3 reclaimed wastewater 877 (million gallons, data centres)",
  "Potable water 7,699 Non-potable water 1,289 Reclaimed wastewater 877", "111", "Appendix: Water", ""],
 ["nttdata_2024", "water_withdrawal_value", "What is the global water withdrawal?",
  "2,098 thousand m3 (global direct operations)",
  "Water withdrawal (total volume) 2,098", "41", "TNFD",
  "unit 1,000 m3; the coding used the Japan-only 413,779 m3"],
 ["nttdata_2024", "water_consumption_value", "What is the global water consumption?",
  "1,371 thousand m3 (global direct operations)", "Water consumption (total volume) 1,371", "41", "TNFD", ""],
 ["nttdata_2024", "water_source", "What are the water sources?",
  "surface and rain 820; groundwater 21; third-party 1,257 (thousand m3)",
  "Surface water and rainwater 820", "41", "TNFD", "coding had 'NOT SPECIFIED'"],
 ["nttdata_2025_db", "water_withdrawal_value", "What is the water withdrawal?",
  "3.84 million m3 (data centres only)", "Water intake ... million m3 ... 3.84", "99", "Appendix: Waste and Water",
  "footnote *3: 'Aggregated for data centers only'; coding had 'NOT REPORTED'"],
 ["nttdata_2025_db", "water_consumption_value", "What is the water consumption?",
  "1.12 million m3 (data centres only)", "Water consumption ... million m3 ... 1.12", "99",
  "Appendix: Waste and Water", "TNFD table (p.43): withdrawal 3,840, discharge 2,724, consumption 1,116 thousand m3"],
 ["nttdata_2025_db", "water_source", "What are the water sources?",
  "groundwater 2,425; third-party 1,402; fresh surface incl. rain 13 (thousand m3)",
  "Groundwater 2,425", "43", "TNFD", "141 sites in 16 countries"],
 ["nttdata_2025_db", "pue_ratio", "What is the PUE?", "1.38", "PUE*5 ... 1.38", "98", "Appendix: Environment",
  "FY2024 column"],
 ["nttdata_2025_db", "wue_boundary", "Is the WUE boundary stated?", "YES",
  "WUE is calculated for data centers within the Global Technology Services Unit's data center business that "
  "have continuous electricity consumption for 24 consecutive months and an IT utilization rate of 20% or more.",
  "99", "Appendix: footnote *7", ""],
 ["nxtra_2025", "water_recycled", "How much water was recycled?", "15,329 kl", "Water Recycled (kl) 15,329",
  "39", "Water Management", "withdrawal + recycled = 216,357 = reported consumption"],
 ["nxtra_2025", "water_discharge_value", "What is the water discharge?", "9,306 kl",
  "Water Discharge (kl) 9,306", "39", "Water Management", "disagrees with 91,306 kl on p.110"],
 ["nxtra_2025", "water_discharge_value", "What is the water discharge (GRI 303-4)?", "91,306 kl",
  "Third-party water kl 91,306 Total kl 91,306", "110", "GRI factsheet: Water discharge (GRI 303-4)",
  "disagrees with 9,306 kl on p.39"],
 ["sify-infinit-spaces-limited_2025", "water_source", "What are the water sources?",
  "S3 STP-recycled 12,699 kL; S5 rainwater harvesting",
  "12,699 kL Recycled water used (STP - Sewage Treatment Plant)", "52", "Water Management",
  "coding had 'NOT REPORTED'"],
 ["sify-infinit-spaces-limited_2025", "estimation_method", "How were unmetered volumes obtained?",
  "Headcount-based estimate for unmetered DC sites",
  "For DC locations without direct water measurement, withdrawal and consumption have been estimated using "
  "the CGWA guideline of 45 litres per person per working day, based on the number of employees at each site.",
  "52", "Water Management", "also assumes 50% consumed / 50% discharged where discharge is unmetered"],
 ["sify-infinit-spaces-limited_2025", "cooling_architecture", "What cooling architecture is used?", "A1",
  "uses soft cleaning ball technology to maintain condenser tube efficiency", "52", "Water Management",
  "water-cooled condensers"],
 ["sify-infinit-spaces-limited_2025", "cooling_architecture", "What cooling architecture is used?", "A3",
  "Deployment of closed-loop air-cooled chillers and thermal storage tanks in place of conventional "
  "water-cooled systems.", "53", "Water Management", ""],
 ["sify-infinit-spaces-limited_2025", "cooling_architecture", "What cooling architecture is used?", "A4",
  "air-cooled chillers, closed-loop systems, and adiabatic cooling solutions", "93", "Upcoming campuses",
  "new campuses"],
]

FILENAME_FIX = {"_2.pdf": ".pdf"}


def clean_quote(q):
    q = re.sub(r"\[cite:[^\]]*\]", "", q).strip()
    q = q.strip('"“”').strip()
    return q


def clean_file(name):
    for a, b in FILENAME_FIX.items():
        name = name.replace(a, b)
    return name


def main():
    out, docmeta = [], {}
    for path in sorted(glob.glob(os.path.join(SRC, "*_details.txt"))):
        stem = os.path.basename(path)[:-len("_details.txt")]
        with open(path, encoding="utf-8") as fh:
            lines = fh.read().splitlines()
        for ln, raw in enumerate(lines, 1):
            if ln == 1 or not raw.strip():
                continue
            r = next(csv.reader([raw]))
            notes = []
            if (stem, ln) in REPAIR:
                fld, q, ans, quote, page, head = REPAIR[(stem, ln)]
                r = [r[0], r[1], fld, q, ans, quote, page, page, head]
                notes.append(REPAIR_NOTE)
            elif len(r) != 9:
                raise SystemExit(f"unrepaired malformed row: {stem} line {ln}")
            op, fn, fld, q, ans, quote, _pdf, printed, head = r
            row = {"operator": op, "document_filename": clean_file(fn), "field_name": fld,
                   "question_asked": q, "extracted_answer": ans, "verbatim_quote": clean_quote(quote),
                   "printed_page": printed.lstrip("0") or printed, "section_heading": head,
                   "source_row": f"{stem}_details.txt:{ln}"}
            docmeta.setdefault(stem, (op, row["document_filename"]))
            changed = bool(notes)
            fix = FIX.get((stem, ln), {})
            for k, v in fix.items():
                if k == "note":
                    continue
                if row[k] != v:
                    row[k] = v
                    changed = True
            if fix.get("note"):
                notes.append(fix["note"])
            row["verification"] = "corrected" if changed else "verified"
            row["verification_note"] = "; ".join(notes)
            out.append(row)
    for stem, fld, q, ans, quote, page, head, note in ADD:
        op, fn = docmeta[stem]
        out.append({"operator": op, "document_filename": fn, "field_name": fld, "question_asked": q,
                    "extracted_answer": ans, "verbatim_quote": quote, "printed_page": page,
                    "section_heading": head, "verification": "added", "verification_note": note,
                    "source_row": ""})
    order = {s: i for i, s in enumerate(sorted(docmeta))}
    inv = {v[1]: k for k, v in docmeta.items()}
    out.sort(key=lambda r: order[inv[r["document_filename"]]])
    os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS, quoting=csv.QUOTE_MINIMAL)
        w.writeheader()
        w.writerows(out)
    n = {k: sum(r["verification"] == k for r in out) for k in ("verified", "corrected", "added")}
    print(f"wrote {os.path.relpath(OUT)}: {len(out)} rows "
          f"({n['verified']} verified, {n['corrected']} corrected, {n['added']} added)")


if __name__ == "__main__":
    main()
