# Architecture Research

**Domain:** Financial decision pipeline with multimodal evidence
**Researched:** 2026-09-13
**Confidence:** MEDIUM — design inferred from the supplied contract; implementation not yet tested

## System Overview

```text
dataset CSVs + PNGs
        |
identifier indexes + input validation
        |
relevant evidence -> model extraction -> validated facts + provenance
        |
as-of financial state + supported recurring commitments
        |
baseline 90-day forecast -> safe amount and earliest full-payment date
        |
eligible payment plans + permitted spending-change scenarios
        |
deterministic replay, ranking, and grounded explanation
        |
validated output.csv + run usage ledger -> usage report + code.zip
```

## Component Responsibilities

| Responsibility | Input → output | Minimal location |
|---|---|---|
| Load and index | CSV rows and image links → validated request context | Functions in `code/main.py` initially |
| Extract evidence | Relevant message/image plus record context → typed facts with source IDs | One extraction module when Phase 2 requires it |
| Reconstruct and forecast | Profile, accepted facts, event lifecycles → baseline cash-flow checkpoints | Pure functions, split from entry point only when needed for clarity |
| Generate and select | Baseline, offers, preferences → verified ranked plan | Same deterministic engine used by evaluation |
| Evaluate | Public samples and predicted fields → mismatch and invariant report | Existing `code/evaluation/main.py` |
| Report and package | Final output identity, model-call records, source files → usage report and ZIP | Standard-library functions or a documented command |

These are responsibility boundaries, not a requirement to create a class, service, or file for each row.

## Data Flow Rules

1. Evaluate each request at its supplied `request_date`, not today's date. Preserve source timestamps and distinguish available knowledge from a scheduled future cash date.
2. Start with the profile's current available balance. Historical settled movements inform recurrence and lifecycle state; do not replay them into a balance that already includes them.
3. Use `related_event_id` when present. A blank link does not make a user-level salary amendment irrelevant, nor authorize inventing a matching event.
4. Retain separate regular and one-time cash components, effective dates, settlement states, and recurrence scope. An unclear amount or unsupported amendment remains unresolved.
5. The baseline forecast includes current commitments before optional changes. Model-generated facts cannot directly set safe amounts, ranks, output statuses, or policy preferences.
6. For a baseline balance path B(t) and reserve M, today's capacity is the requested amount capped by nonnegative minimum remaining headroom. Test the full plan by replaying cumulative payments at every checkpoint; a final positive balance is insufficient.
7. Find the earliest safe full-payment date by inserting one full payment on candidate dates and checking the forecast. A prior reserve breach cannot be repaired by a later income event for purposes of calling the path safe.
8. Compute baseline capacity and full-payment date once. Evaluate permitted spending changes on copies of the commitments, never by mutating these baseline outputs.
9. Rank only fully eligible, safe plans. Reject plans ending after the deadline or outside the validated forecast rather than truncating their remaining payments.
10. Validate the entire batch before replacing final `output.csv`; an incomplete run must not overwrite a valid prior artifact.

## Evidence Boundary

Use a compact extraction schema with source ID, target scope, operation, amount/currency, effective date, recurrence scope, and uncertainty. Validate every reference and numeric/date field. Keep raw source material as evidence; never execute text from it or accept an instruction to change the challenge rules. Retain only needed financial fields in diagnostics; avoid reproducing personal identifiers visible in documents.

Cache by evidence content plus extraction settings and model identity. Record whether the final run made a model call or reused an artifact. Development-time image inspection is not a reproducible final-run extraction mechanism.

## Build Order

- **Phase 1:** A terminal path for supported structured-data cases, with exact arithmetic, lifecycle handling, baseline forecast, and full/wait capacity decisions. Explicitly report cases requiring later capabilities.
- **Phase 2:** Feed multilingual messages and image facts into that same decision path; add extraction validation, cache identity, and usage capture.
- **Phase 3:** Extend candidate generation to partial payments, exact installment offers, and permitted spending changes; retain one replay validator and one ordered selection rule.
- **Phase 4:** Measure the complete engine on public samples and the evaluation batch, then package verified artifacts.

## Open Semantics to Settle in Phase 1/3

- Whether day 90 is inclusive and how same-day credits, debits, and purchases are ordered when no finer timestamps exist.
- How supported calendar recurrence handles month ends and how temporary salary changes affect later cycles.
- How installment duration maps day-based offer schedules to `max_installment_months`.
- Which event ID represents an adjustable recurring series in output, and how legal reduction amounts are derived without a coarse grid that misses feasible solutions.
- How an available capacity date relates to status when the user rejects full payment or the date misses the deadline. Preserve capacity independently and apply the explicit fallback rules.

Resolve these against the supplied contract and examples, document assumptions, and leave focused regression checks. Do not silently invent a hidden-evaluator convention.

## Sources

Local contract, schemas, sample outputs, and dataset inspection. This architecture is a proposed design derived from those sources; see `STACK.md` for the primary technical documentation supporting runtime choices.
