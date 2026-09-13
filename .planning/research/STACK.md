# Stack Research

**Domain:** Dataset-driven financial affordability agent
**Researched:** 2026-09-13
**Confidence:** HIGH for local runtime and standard-library capabilities; MEDIUM for the proposed model boundary

## Recommended Stack

| Technology | Version | Purpose | Rationale |
|---|---|---|---|
| Python | 3.13.3 observed locally | Terminal entry point and evaluation | Reuses the supplied Python entry points; no application framework is needed |
| `csv`, `pathlib`, `collections` | Bundled with Python | Input loading and identifier indexes | The supplied workload is 25,342 events and 275 users, suitable for a straightforward in-memory design |
| `decimal.Decimal` | Bundled with Python | Amounts, exchange rates, fees, balances | Parse numeric strings directly; binary floating point is unsuitable for exact monetary comparisons |
| `datetime.date`, `timedelta`, `calendar` | Bundled with Python | Forecast dates and recurrence | Day-based payment intervals must remain distinct from calendar-month recurrence |
| `json`, `hashlib` | Bundled with Python | Validated evidence artifacts and cache identity | Local files are sufficient; include evidence content, prompt version, and model identity in cache keys |
| One vision-capable model and its supported API client | Select during Phase 2 | Multilingual message and image interpretation | Extract facts with provenance; do not delegate balance arithmetic or candidate ranking |
| `unittest`, `zipfile` | Bundled with Python | Focused financial regression checks and packaging | No new test or packaging framework is justified by this scope |

`csv.DictReader`/`DictWriter` provide named-column access; use `newline=''` when opening CSV files. [Python CSV documentation](https://docs.python.org/3/library/csv.html)

`Decimal` represents decimal strings exactly and offers explicit precision and rounding control. Reject non-finite values and define serialization precision separately from intermediate arithmetic. [Python decimal documentation](https://docs.python.org/3/library/decimal.html)

Python date arithmetic supports explicit day offsets. A 30-day installment interval must not silently become a calendar-month increment. [Python datetime documentation](https://docs.python.org/3/library/datetime.html)

## Model Integration

Use a single provider initially, selected by access and measured extraction quality on supplied evidence. Claude's official documentation confirms PNG input and schema-constrained structured outputs as one available implementation route; this is a capability reference, not a provider selection or paid-call authorization. [Vision](https://platform.claude.com/docs/en/build-with-claude/vision), [structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)

Extract only relevant financial fields: source ID, target event or supported user-level scope, operation, amount/currency, effective date, recurrence scope, and uncertainty. Schema conformity is not proof that a financial claim is correct. Keep request policy outside model-editable facts and validate identifiers and values in code.

Record provider-reported usage from the first integration call. Resolve model IDs, SDK versions, and current pricing when the integration is chosen; no model pricing is assumed here. Planning's `model_profile: inherit` does not configure the submitted program's model.

## Installation and Compatibility

Phase 1 needs no third-party package. Use the available Python 3.13 runtime and document the tested minimum version when code exists. If a model SDK is selected in Phase 2, pin its tested version then. No dependencies were installed during initialization.

## Alternatives Considered

| Alternative | When justified | Current choice |
|---|---|---|
| Pandas or a database | Measured data-processing bottlenecks or larger workloads | Standard-library CSV and dictionaries |
| OCR before vision | Reliable local OCR substantially reduces measured extraction cost | Evaluate only if needed; `tesseract` was not on PATH during inspection |
| Local vision model / Hugging Face hosting | Offline or provider constraints require it | No model download, server, or Hub dependency yet |
| Agent orchestration framework | Multiple independent tool-using workflows become necessary | A direct pipeline with one extraction boundary |
| Optimization solver | Exact permitted spending-change search is demonstrably impractical | Enumerate finite method/offer combinations; derive legal reduction candidates from cash-flow constraints |

## Sources

- Local: `README.md`, `problem_statement.md`, `AGENTS.md`, CSV schemas and counts, Python version check.
- Primary technical documentation linked above, checked 2026-09-13. Architecture recommendations are project-specific inferences, not externally validated performance claims.
