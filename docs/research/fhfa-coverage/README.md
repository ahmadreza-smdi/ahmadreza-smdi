# FHFA metro endpoint coverage reproduction

By [Ahmadreza Samadi](https://a-samadi.com/about.html).

This companion to my [working price and rent methods note](../price-and-rent-study-methods.md) reproduces a coverage diagnostic from frozen public source files: 386 whole-metro FHFA series, 79,516 observations and 186 same-quarter pairs exactly five calendar years apart within 1975Q1–2026Q2.

**This product uses FHFA data but is neither endorsed nor certified by FHFA.**

The output counts which metros have an index at both endpoints. It does not select the price-versus-rent study window, establish HUD matches or calculate price or rent growth.

## Run the reproduction

Use Python 3 and its standard library. From this directory:

```sh
python fhfa_coverage.py > rebuilt-coverage.csv
python -m unittest discover -p test_fhfa_coverage.py -v
```

The command reads the bundled `raw/` snapshots, checks their SHA-256 hashes in `SOURCES.json`, and writes CSV to standard output. It does not download newer data or change the source files. The tests compare the full result with `expected-coverage.csv`.

The source parser separates whole metros from metropolitan divisions using the bundled Census 2023 delineations. It combines 373 whole-metro series from the main FHFA CSV with 13 whole-metro series from the supplement, without averaging division indices. Those geography definitions do not establish historical HUD comparability.

## Read the counts

Each row contains the start and end quarters, the count observed at both, the count not observed at both, the cohort size and nine paired status counts. A status is `observed`, `missing_index` for an existing row with a blank index, or `absent_row`.

The column `observed__missing_index`, for example, counts metros with an observed start value and a blank end value. The nine status counts sum to 386 in every row. These are availability labels, not estimates of index precision.

The smaller separate endpoint count can exceed the paired count:

| Start | End | Observed at start | Observed at end | Observed at both |
| --- | --- | ---: | ---: | ---: |
| 1976Q4 | 1981Q4 | 40 | 140 | 39 |
| 1979Q3 | 1984Q3 | 136 | 201 | 135 |
| 1990Q1 | 1995Q1 | 339 | 382 | 338 |

For the first row, one metro has an observed start index but a blank end index. Another 101 have the reverse pattern. Those records cannot be combined into complete pairs.

## Sources and reuse

Source credit: **FHFA House Price Index® — All-Transactions, not seasonally adjusted, nominal**. FHFA values may revise. The bundled FHFA files were acquired on 17 October 2026; the Census file is an earlier saved snapshot reused in that preparation. `SOURCES.json` identifies each exact file, source URL and hash. The live source URLs may subsequently serve different bytes.

The agency inputs retain their source status and notices. They are separate from the MIT licence for this directory's original Python code. The reuse basis is FHFA's [copyright and agency-name policy](https://www.fhfa.gov/about/fhfa-policies/website-privacy-policy), the [HPI FAQ](https://www.fhfa.gov/faqs/hpi) and the Census Bureau's [public access policy](https://www2.census.gov/foia/ds_policies/ds027.pdf). Federal employee-created works generally have a public-domain basis in the United States; this is not a worldwide CC0 grant or a licence for third-party material, agency seals or logos.

The two helper modules retain the parsing and whole-metro merge functions used in the existing research preparation. The paired-count implementation is checked against every row of the previously reviewed diagnostic. Reproducing these counts does not independently validate all parsing assumptions or the geographic and temporal eligibility of a future comparison.

Educational research, not financial advice. AI-assisted code and documentation; no company or customer result is claimed.
