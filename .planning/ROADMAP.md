# Roadmap: Buy or Wait?

## Overview

Three sequential phases deliver the required terminal submission. Evidence handling is part of reading the provided inputs. Do not create messaging features, a document platform, cache/provenance infrastructure, or additional product surfaces.

## Phases

- [ ] **Phase 1: Financial Decision Pipeline** - Read the supplied evidence and produce a checked 90-day forecast with baseline payment capacity.
- [ ] **Phase 2: Payment Selection and Output** - Complete all required payment methods, spending adjustments, and CSV output.
- [ ] **Phase 3: Evaluation and Submission** - Check the samples, run the dataset, and package the required artifacts.

## Phase Details

### Phase 1: Financial Decision Pipeline
**Goal:** Run a supplied request from input files through financial reconstruction to a baseline forecast and safe-to-pay/full-payment date.
**Mode:** mvp
**Depends on:** Nothing (first phase)
**Requirements:** DATA-01, DATA-03, CASH-01, CASH-03, CASH-04, EVID-01, EVID-02, EVID-04, FORE-01, FORE-02, FORE-03, EVAL-02
**UI hint:** no
**Success Criteria:**
1. The terminal program loads relevant supplied records and interprets necessary message/image facts; missing amounts, invalid facts, and embedded instructions cannot silently change the financial rules.
2. Forecasts start from the profile balance, resolve real versus duplicate cash movements, use supplied dated FX, and include only supported income and commitments with protected essential spending.
3. A 90-day calculation produces baseline safe capacity and the earliest safe full-payment date; a representative supplied sample exercises the path and unresolved facts are reported rather than guessed.
4. Focused runnable checks cover snapshot double-counting, invalid money, date/FX handling, and reserve breaches. Model-call usage is counted from the first call for the eventual required report.
**Plans:** TBD (target 1–2 plans)

Implement with functions in the existing Python entry point. One extraction function/client is sufficient; no language detection, translation interface, persistent cache, or generalized evidence subsystem. Resolve financial date/recurrence assumptions against the supplied rules and examples.

### Phase 2: Payment Selection and Output
**Goal:** Produce one complete, safe, personalized recommendation per request in the required CSV format.
**Mode:** mvp
**Depends on:** Phase 1
**Requirements:** PLAN-01, PLAN-02, PLAN-03, PLAN-05, PLAN-07, PLAN-08, OUT-01, OUT-03, OUT-04
**UI hint:** no
**Success Criteria:**
1. Full, partial, installment, wait, and fallback decisions respect user preferences, deadlines, and the exact permitted schedules; partial payments are checked cumulatively.
2. Spending changes use at most three permitted flexible recurring events/actions, preserve protected categories and reduction floors, and never change the baseline capacity fields.
3. Every complete candidate is checked against the reserve and deadline, then ranked in the specified order; status, payment method, and explanation agree with the selected plan.
4. The command writes root-level `output.csv` with all evaluation IDs and the exact required columns/formats after validation; a failed run preserves prior valid output.
**Plans:** TBD (target 1–2 plans)

Use the same forecast checker for every candidate. Add focused cases to the existing checks; no separate planner service, optimization platform, or reporting interface.

### Phase 3: Evaluation and Submission
**Goal:** Deliver evaluated predictions and the runnable submission package with the required usage report and transcript.
**Mode:** mvp
**Depends on:** Phase 2
**Requirements:** EVAL-01, SHIP-01, SHIP-02, SHIP-03
**UI hint:** no
**Success Criteria:**
1. The existing evaluation entry point compares the same engine against all 25 public examples, reporting errors and mismatches without feeding labels into predictions.
2. The final run produces 250 validated prediction rows without modifying input data; sample results are measured and hidden accuracy is not claimed.
3. The required usage report includes actual final-run model calls, token totals/averages, and estimated costs with per-model and overall totals when applicable; no fabricated usage values.
4. `code.zip` includes runnable code, prompts/configuration, instructions, and `evaluation/usage_report.md`; a clean extraction runs as documented, and the separate transcript/package contain no credentials.
**Plans:** TBD (target 1–2 plans)

Use a straightforward evaluation script, usage counters, and standard ZIP packaging. No dashboard, tracking service, benchmark platform, or automatic external submission.

## Progress

| Phase | Plans Complete | Status | Completed |
|---|---|---|---|
| 1. Financial Decision Pipeline | 0/TBD | Not started | - |
| 2. Payment Selection and Output | 0/TBD | Not started | - |
| 3. Evaluation and Submission | 0/TBD | Not started | - |

Execution order: 1 → 2 → 3, sequential and automatic. Plan checks and financial verification remain enabled.

---
*Updated: 2026-09-13. Replaces the original four-phase roadmap; implementation has not started.*
