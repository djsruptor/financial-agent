# Roadmap: Buy or Wait?

## Overview

Deliver the complete challenge solution in four sequential, runnable increments: establish structured financial decisions, incorporate message/image evidence, complete payment-method and spending-change selection, then validate and package the full submission. Each phase extends the same terminal pipeline. Early development diagnostics must clearly identify unsupported cases; only the complete validated engine may produce final submission output.

## Phases

- [ ] **Phase 1: Structured Financial Decisions** - Run supported structured-data requests through baseline forecasting and full/wait decisions.
- [ ] **Phase 2: Evidence-Aware Decisions** - Incorporate multilingual messages and image-derived facts reproducibly.
- [ ] **Phase 3: Complete Payment Planning** - Select the safest eligible plan across all required methods and spending changes.
- [ ] **Phase 4: Evaluated Submission** - Validate the full dataset and deliver reproducible submission artifacts with measured usage.

## Phase Details

### Phase 1: Structured Financial Decisions
**Goal:** The participant can run supported structured-data requests from the terminal and inspect correct baseline capacity and full-payment/wait decisions, with explicit diagnostics for unsupported evidence or payment methods.
**Mode:** mvp
**Depends on:** Nothing (first phase)
**Requirements:** DATA-01, DATA-02, DATA-03, CASH-01, CASH-02, CASH-03, CASH-04, CASH-05, FORE-01, FORE-02, FORE-03, PLAN-01, EVAL-02
**UI hint:** no
**Success Criteria:**
1. A documented terminal command loads immutable participant data and runs a supported structured-data case end to end; invalid inputs and requests requiring unimplemented evidence/method handling produce explicit diagnostics rather than fabricated final judgments.
2. The participant can inspect a forecast that starts from the profile balance, preserves genuine linked cash movements, removes duplicates, reserves pending debits, excludes unsupported credits/non-cash values, and uses the correct dated FX rates.
3. The forecast includes supported recurring commitments and conservative essential spending and checks reserve compliance across a documented 90-day horizon, including same-day and month-end behavior.
4. Baseline safe-to-pay and earliest full-payment date are independently testable, and full/wait recommendations respect user acceptance and completion deadlines.
5. A runnable check suite fails for snapshot double-counting, invalid monetary values, a reserve dip, incorrect FX direction/date, and changed forecast boundary semantics; at least one supported supplied sample is exercised without embedding its label into prediction logic.
**Plans:** TBD (target 1–3 plans during phase planning)

**Planning focus:** Resolve as-of evidence eligibility, recurring calendar anchors, variable essential spending, forecast inclusivity, and same-day cash ordering using the specification and public samples. Use Python and its standard library initially.

### Phase 2: Evidence-Aware Decisions
**Goal:** The participant can rerun the decision pipeline with relevant messages and images applied as validated financial facts, with reproducible extraction and usage records.
**Mode:** mvp
**Depends on:** Phase 1
**Requirements:** EVID-01, EVID-02, EVID-03, EVID-04, EVID-05, EVID-06
**UI hint:** no
**Success Criteria:**
1. English and Indonesian amendments update supported salary amounts, payment dates, cancellations, and recurrence scope, including relevant user-level messages without direct event links.
2. All 16 currently missing event amounts are resolved from their linked images with financial-field provenance, or reported explicitly as unresolved; no blank amount is treated as zero and no unresolved case is eligible for final export.
3. Conflict-precedence checks and adversarial evidence checks demonstrate that embedded instructions cannot change policy, run commands, or dictate output decisions.
4. The same terminal decision path reflects accepted evidence changes, and a repeated extraction run can reuse validated artifacts only when source content and extraction settings match.
5. Each actual model call records provider/model identity and available input/output usage, with charged retries, missing usage, and cache reuse distinguishable; no development-session estimates are presented as final-run measurements.
**Plans:** TBD (target 1–3 plans during phase planning)

**Planning focus:** Select one accessible vision-capable provider/model, pin the tested integration, define extraction schema and provenance, and verify the supplied images' financial amount roles. Do not bind the application model to the planning model setting.

### Phase 3: Complete Payment Planning
**Goal:** The participant receives a complete personalized recommendation across all required methods and permitted spending changes, verified against the same baseline financial state.
**Mode:** mvp
**Depends on:** Phase 2
**Requirements:** PLAN-02, PLAN-03, PLAN-04, PLAN-05, PLAN-06, PLAN-07, PLAN-08, PLAN-09, OUT-02, OUT-03
**UI hint:** no
**Success Criteria:**
1. Partial schedules use exactly the two prescribed payments; installment schedules match a supplied offer's exact dates, amounts, count, total cost, and user duration restrictions.
2. Every selected schedule passes cumulative reserve and deadline checks through the forecast; later obligations are never omitted to make an offer appear safe.
3. Spending adjustments use no more than three legal changes to permitted flexible recurring events, preserve protected spending and reduction floors, and leave baseline capacity/date fields unchanged.
4. Controlled candidate comparisons demonstrate the complete ranking order and correct status/method handling, including adjusted full payment, installments chosen by preference, waiting, and no-safe-eligible-plan fallback.
5. Selected plans serialize in the required chronological and event-ID formats and include explanations consistent with the actual forecast, schedule, evidence, and required changes.
**Plans:** TBD (target 1–3 plans during phase planning)

**Planning focus:** Define installment-duration interpretation, adjustment event references, and legal reduction search; replay the combined partial plan rather than validating its payments separately. Extend regression checks at each addition.

### Phase 4: Evaluated Submission
**Goal:** The participant can generate, inspect, and reproduce the complete challenge submission with validated predictions and truthful final-run usage reporting.
**Mode:** mvp
**Depends on:** Phase 3
**Requirements:** OUT-01, OUT-04, EVAL-01, EVAL-03, SHIP-01, SHIP-02, SHIP-03
**UI hint:** no
**Success Criteria:**
1. The public-sample evaluation runs the same engine on all 25 examples and reports per-field numeric errors, categorical/schedule accuracy, and investigated discrepancies without hardcoded labels or hidden data.
2. A complete run produces exactly one validated row for each of the 250 evaluation requests in root-level `output.csv`, with the exact eight columns, no sample rows, and no unresolved safety or output-contract violations.
3. Failed or incomplete runs leave a prior valid output intact; validation covers the whole batch before the final file is replaced, and input datasets remain unchanged.
4. The usage report in the ZIP identifies the final output-producing run and includes providers/models, calls, token totals/averages, costs, per-model/overall totals, and transparent cache or unavailable-usage treatment.
5. The ZIP passes a documented clean-extraction run with required prompts/configuration and evaluation files, and the transcript is ready as a separate artifact; no credentials or unnecessary sensitive personal data are included.
**Plans:** TBD (target 1–3 plans during phase planning)

**Planning focus:** Confirm output/run identity, current provider pricing when applicable, package layout, clean-run instructions, and the distinction between measured sample results and unknown hidden accuracy. Do not submit externally without an explicit submission request.

## Progress

**Execution Order:** 1 → 2 → 3 → 4. Plans execute sequentially using the approved automatic workflow.

| Phase | Plans Complete | Status | Completed |
|---|---|---|---|
| 1. Structured Financial Decisions | 0/TBD | Not started | - |
| 2. Evidence-Aware Decisions | 0/TBD | Not started | - |
| 3. Complete Payment Planning | 0/TBD | Not started | - |
| 4. Evaluated Submission | 0/TBD | Not started | - |

---
*Created: 2026-09-13 under the user's approved automatic initialization preferences. Detailed executable plans are the next workflow step.*
