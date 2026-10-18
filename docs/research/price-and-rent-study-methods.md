# Working methods for comparing house price growth and rent benchmarks

By [Ahmadreza Samadi](https://a-samadi.com/about.html). Prepared 17 October 2026.

I am preparing a descriptive study of how nominal house price index growth compares with changes in a published rent benchmark across comparable US metropolitan areas. The primary duration is five calendar years; exact endpoint dates, eligible metros and comparison results remain unresolved. This working note explains the proposed method and the choices that still need evidence; it is not a registered preregistration.

The question is about changes in two measures. It does not compare a purchase price and rent for the same property, calculate investment yield or identify the best place to invest.

## Choose the measures before interpreting a gap

The prepared price input is the FHFA House Price Index All-Transactions series, not seasonally adjusted. It is a nominal index rather than a median dollar house price. FHFA explains that historical values can revise, so the study will identify its frozen snapshot and distinguish later revisions. [FHFA HPI FAQ](https://www.fhfa.gov/faqs/hpi).

The planned rent input is a HUD Fair Market Rent benchmark, with the two-bedroom measure as the intended starting point. The actual files, rent definition, revisions, local exceptions and reuse conditions remain to be established. HUD's overview describes a benchmark built from source rents, adjustments and trending. A fiscal-year label does not mean that all underlying rents were observed in that year. [HUD FMR overview](https://www.huduser.gov/portal/sites/default/files/pdf/fmr-overviewFY25.pdf).

Both rent endpoints must have a consistent currency, unit and rent-measure basis. The intended comparison remains nominal; it does not imply an inflation-adjusted rate.

## Match whole areas rather than similar names

My proposed inclusion rule requires a complete documented geographic footprint at both endpoints. A matching metropolitan name or area code identifies a candidate, not proof that the underlying areas are the same.

County and county-subdivision units remain distinct. Different geography vintages require supporting official evidence before they can be treated as comparable. I will not average partial HUD subareas into an invented metropolitan rent or reconstruct a whole-metro price series by averaging divisions.

A complete geographic match would still leave timing, the rent measure and source reuse to resolve. Prepared FHFA inputs are not evidence that corresponding HUD matches exist.

### Boundary changes to check at each endpoint

HUD's methodology, updated June 2026, describes concrete reasons to check membership rather than carry today's area definition backward:

- New England FMR geography generally uses towns, equivalent to Census county subdivisions. Connecticut's geography changes start with FY 2026: following its switch to planning-region county equivalents, HUD adopted OMB's 2023 metro definitions there.
- Starting with FY 2025 FMRs, Westchester County became part of the New York HUD Metro FMR Area. The earlier separate rent benchmark cannot simply be treated as unchanged membership.
- HUD describes several area-code constructions and acknowledges possible historical inconsistencies. A familiar code is useful metadata, not a substitute for endpoint-specific boundary evidence.

These are documented geography changes and methodological cautions, not measured price or rent growth. They do not by themselves establish which metros qualify for the proposed window. [HUD, Calculation of Fair Market Rents, Section II, printed pages 2–3](https://www.huduser.gov/portal/datasets/fmr/fmr2027/FY27-Public-FMR-Methodology.pdf).

### A named metro can include a partial-county exception

HUD's June 2026 methodology describes the Sullivan City portion of Crawford County, Missouri as included in its St. Louis HUD Metro FMR Area. HUD notes that Census does not appear to follow this practice in its St. Louis MSA statistics. That qualification matters: this is an attributed statement from HUD, not my independent legal or Census-boundary determination. [HUD methodology, printed page 4](https://www.huduser.gov/portal/datasets/fmr/fmr2027/FY27-Public-FMR-Methodology.pdf#page=4).

A similar name or identifier prefix cannot resolve this partial-area question. I will not discard a source component, truncate an identifier into an assumed whole county, or average subarea benchmarks merely to force matching coverage. The exact selected-vintage membership, boundaries and timing still need evidence; this example establishes no eligible St. Louis comparison or growth result.

## Explain the time alignment explicitly

The primary window decision, recorded on 17 October 2026 before actual price-versus-rent comparisons, is five calendar years. This is an editorial research choice, not an FHFA or HUD recommendation, an optimal horizon or a forecast period.

For a frozen inventory of acquired source files and versions, the selection rule is:

1. Identify comparable two-bedroom metro FMR benchmarks with documented effective dates sharing the same month and day exactly five calendar years apart. Keep base, adjustment or trend, effective and revision dates separate.
2. Map each effective date explicitly to its containing calendar quarter. Both FHFA quarters must have at least one valid metro observation in the prepared source inventory. This is a source-level screen; each metro still needs both usable price endpoints and all other eligibility checks.
3. Choose the latest end date that passes source reuse, documented-date and rent-measure comparability reviews. Retain newer unsupported candidates and their reasons. Do not select a period by its growth direction, gap or ranking.
4. Apply that single window across metros. If no five-year pair qualifies, leave the primary comparison unavailable. There is no shorter-window fallback; any change to this policy must be dated and explained before comparisons under that change.

Pairing a quarterly price index with an effective-date rent benchmark does not align their underlying observation or base periods, or establish that they cover the same housing population.

I will not automatically map a HUD fiscal year to an FHFA quarter or annual average. FHFA's quarterly indexes pool observations within a quarter; they are not quarter-end property prices. A missing requested quarter will not be replaced by the nearest available value. [FHFA HPI FAQ](https://www.fhfa.gov/faqs/hpi).

No annualization or compound annual growth rate is specified at this stage.

## Count the same metros at both endpoints

Endpoint coverage is a paired-data question. If A contains metros with an observed index at the start and B contains metros with an observed index at the end, the usable price-endpoint count is |A ∩ B|. The smaller of |A| and |B| is only an upper bound; the two groups need not contain the same metros.

A diagnostic prepared on 18 October 2026 from my frozen FHFA inventory covers 386 whole-metro series and 186 same-quarter pairs exactly five calendar years apart, within 1975Q1–2026Q2. In three pairs, the smaller separate endpoint count exceeds the count observed at both endpoints:

| Start | End | Observed at start | Observed at end | Smaller separate count | Observed at both |
| --- | --- | ---: | ---: | ---: | ---: |
| 1976Q4 | 1981Q4 | 40 | 140 | 40 | 39 |
| 1979Q3 | 1984Q3 | 136 | 201 | 136 | 135 |
| 1990Q1 | 1995Q1 | 339 | 382 | 339 | 338 |

For example, the first pair has one metro with an observed start index but a blank end index, and 101 with a blank start index but an observed end index. Those records cannot be combined into a complete pair. The diagnostic distinguishes an observed value, an existing row with a missing index, and an absent row.

These are coverage counts in a frozen prepared inventory, not growth results or a newly selected study window. The inventory combines 373 whole-metro series from the main source and 13 whole-metro series from the supplement; metropolitan divisions are excluded. It does not prove that any corresponding HUD benchmark has comparable dates, boundaries or rent measures. Availability must be checked for each metro after selecting an eligible common window under the policy above.

Source: FHFA House Price Index® (All-Transactions, not seasonally adjusted, nominal). The [main CSV](https://www.fhfa.gov/hpi/download/quarterly_datasets/hpi_at_metro.csv) and [supplemental workbook](https://www.fhfa.gov/hpi/download/quarterly_datasets/hpi_at_multid_metro.xlsx) were acquired on 17 October 2026; those download URLs may subsequently serve revised data. The frozen raw CSV SHA-256 is `07e3e98998806df830fd1ec141dbf234e66d66675258ecd705078028aafedee0`; the supplemental workbook SHA-256 is `4d434b9939bae371d2198be89b4426e4e03290b5d71073251cea4c26d6341293`. These counts describe that snapshot, not every FHFA vintage. This product uses FHFA data but is neither endorsed nor certified by FHFA.

## Keep percentage points and relative changes separate

For positive, finite and comparable endpoints, define the price growth factor as **H = HPI end / HPI start**, and the rent growth factor as **R = FMR end / FMR start**.

- House price index growth in percent: **100 × (H − 1)**.
- Rent benchmark change in percent: **100 × (R − 1)**.
- Growth gap in percentage points: **100 × (H − R)**.
- Relative change in the starting price-index-to-rent-benchmark ratio, in percent: **100 × (H / R − 1)**.

A percentage-point gap and a relative ratio change answer different questions. Neither the ratio HPI/FMR nor its relative change is a dollar price-to-rent level or a property yield. The prepared arithmetic keeps exact rational values separate from display rounding, so a tiny nonzero difference may display as zero.

## Preserve exclusions and unknowns

Missing index cells, absent source rows, failed comparisons and unresolved evidence need separate labels and reasons. Missing or nonpositive endpoints cannot become valid growth factors. Unknowns will not be converted to zero or silently presented as successful matches.

The prepared matching and arithmetic components do not yet include a raw HUD file adapter.

## Decisions still open

- The exact HUD files and initial or revised versions at each endpoint.
- Actual complete geographic matches and any necessary official crosswalk.
- The exact effective-date pair, its interpretation and selected FHFA quarters under the five-year policy.
- The final rent-measure definition, local exceptions and source-use evidence.
- The eligible population, exclusion counts and any aggregate summary method.

The completed study is intended to publish its method and limits alongside a CSV, chart with alt text, source checksums, rebuild code and citation metadata. Until those comparisons exist, this note supplies no metro rankings, growth estimates or statistical-significance findings. The existing [rent-burden study](https://github.com/ahmadreza-smdi/metro-rent-burden) answers a different question and remains a separate dataset.

This product uses FHFA data but is neither endorsed nor certified by FHFA.

Educational research, not financial advice. AI-assisted preparation; no company or customer result is claimed. [More research and writing](https://a-samadi.com/topics/ai-real-estate.html).

## Reproduce the FHFA coverage diagnostic

The [frozen source companion](fhfa-coverage/) includes the four official source snapshots, a standard-library Python runner and the expected 186-row CSV. It rebuilds the paired availability counts above; it does not select the study window, match HUD geographies or calculate price and rent growth.
