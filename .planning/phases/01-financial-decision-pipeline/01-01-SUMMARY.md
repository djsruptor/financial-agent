---
phase: 01-financial-decision-pipeline
plan: "01"
subsystem: financial forecasting
tags: [python, decimal, csv, cash-flow, forecasting]
requires: []
provides:
  - Validated request-scoped cash context and supplied-FX conversion
  - Reusable 90-day schedule checker and baseline forecast
  - Independent input, forecast, and structured-sample checks
affects: [01-02-PLAN.md, payment-selection]
tech-stack:
  added: []
  patterns: [stdlib CSV loading, Decimal money, host-owned schedule checks]
key-files:
  created: []
  modified: [code/main.py, code/evaluation/main.py]
key-decisions:
  - "Use the profile as the current balance snapshot and reserve pending debits once."
  - "Treat a named next salary plus prior settled salary as supported ongoing employment evidence."
patterns-established:
  - "All capacity calculations call check_schedule across the complete 90-day horizon."
requirements-completed: [DATA-01, DATA-03, CASH-01, CASH-03, CASH-04, FORE-01, FORE-02, FORE-03, EVAL-02]
duration: 16min
completed: 2026-09-13
---

# Phase 01 Plan 01: Deterministic financial tools and numerical oracles Summary

**Validated CSV financial state, deterministic 90-day cash safety, and a passing stripped public request baseline.**

## Performance

- **Duration:** 16 min
- **Started:** 2026-09-13T20:55:51Z
- **Completed:** 2026-09-13T21:11:00Z
- **Tasks:** 3/3
- **Files modified:** 2

## Accomplishments

- Loads authorized request records with finite `Decimal` money, supplied settlement-date FX, snapshot semantics, pending-debit reserves, and explicit unresolved evidence.
- Replays every date in the 90-day horizon in debit, credit, payment order to calculate safe-today capacity and earliest full-payment date.
- Runs isolated input/forecast checks and evaluates `request_01` after stripping all sample answer fields.

## Task Commits

1. **Task 1: Load a request into validated cash state** — `d20c464` (`feat`)
2. **Task 2: Implement supported recurrence and whole-horizon capacity** — `13836d6` (`feat`)
3. **Task 3: Close the structured slice with a public numerical oracle** — `b589fe2` (`feat`)

## Files Created/Modified

- `code/main.py` — deterministic loader, cash-state reconstruction, recurrence inference, safety checker, and baseline CLI.
- `code/evaluation/main.py` — direct numerical regressions and stripped public-sample assertion.

## Decisions Made

- The current profile balance is authoritative for settled history; only known future cash and pending reserves alter the forecast.
- A scheduled salary repeats only when prior settled salary evidence supports continuing employment. This general correction makes the published `request_01` result pass without request-specific handling.

## Verification

- `python3 code/evaluation/main.py --checks core` — passed.
- `python3 code/evaluation/main.py --samples request_01 --structured-only` — passed: safe amount `25256`, earliest date `2024-03-03`.
- `python3 code/main.py --request-id request_26 --baseline --structured-only` — passed with a concise host-owned baseline result.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Repeated a supported salary schedule only with evidence of ongoing employment**
- **Found during:** Task 3
- **Issue:** Treating only the one explicitly scheduled salary as future income produced an incorrect public baseline despite a prior settled salary and a named next-salary record.
- **Fix:** Added a general salary schedule rule requiring both the future named schedule and historic settled salary evidence.
- **Files modified:** `code/main.py`, `code/evaluation/main.py`
- **Verification:** `request_01` passes through stripped production inputs.
- **Committed in:** `b589fe2`

## Known Stubs

None.

## Next Phase Readiness

Plan 01-02 can bind the model-driven orchestrator to these deterministic, host-owned tools. Live model credentials and evidence resolution remain its responsibility.

## Self-Check: PASSED

- `code/main.py`, `code/evaluation/main.py`, and this summary exist.
- Task commits `d20c464`, `13836d6`, and `b589fe2` exist in git history.
