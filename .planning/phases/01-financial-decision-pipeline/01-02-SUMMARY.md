---
phase: 01-financial-decision-pipeline
plan: "02"
subsystem: financial agent orchestration
tags: [python, openai, responses-api, decimal, evidence-validation]
requires:
  - phase: 01-01
    provides: deterministic 90-day financial forecast and schedule checker
provides:
  - bounded request-scoped agent loop with host-owned financial results
  - validated message/image evidence updates and forecast revision checks
  - offline agent acceptance suite plus a live Responses API acceptance command
affects: [phase-02-payment-selection, evaluation]
tech-stack:
  added: [openai==1.109.0]
  patterns: [literal tool allowlist, Decimal host validation, injected scripted client]
key-files:
  created: [code/README.md, code/requirements.txt]
  modified: [code/main.py, code/evaluation/main.py]
key-decisions:
  - "Use one direct Responses API client and keep provider calls injectable for no-cost offline checks."
  - "Allow only source-scoped validated facts to update cash context; never accept model financial outputs."
patterns-established:
  - "A forecast is valid only for its evidence revision and finish returns host-owned fields."
requirements-completed: [AGENT-01, EVID-01, EVID-02, EVID-04, DATA-01, CASH-04, FORE-01, FORE-02, FORE-03, EVAL-02]
duration: 109min
completed: 2026-09-13
---

# Phase 1 Plan 2: Bounded model-driven financial orchestration Summary

**A bounded model-selected tool loop validates evidence and returns only deterministic 90-day financial baselines.**

## Performance

- **Duration:** 109 min
- **Started:** 2026-09-13T21:05:01Z
- **Completed:** 2026-09-13T22:54:11Z
- **Tasks:** 3/3
- **Files modified:** 4

## Accomplishments

- Added a 12-turn, 24-attempt request loop with a literal financial-tool allowlist, per-request scope checks, bounded failures, and measured provider usage.
- Added finite `Decimal` evidence validation for user-level salary amendments and linked image net amounts, including revision invalidation and safe image-path handling.
- Added combined offline acceptance checks and an opt-in real Responses API runner that reports token usage and blocks explicitly on provider/credential failure.

## Task Commits

1. **Task 1: Build the bounded orchestrator around the financial tools** — `42ae141` (`feat`)
2. **Task 2: Resolve authorized evidence and invalidate stale forecasts** — `24287a4` (`feat`)
3. **Task 3: Prove the agentic path against exact sample results** — `0dfaa64` (`feat`)

## Files Created/Modified

- `code/main.py` — scoped orchestrator, evidence validation, revision-safe forecast dispatch, and direct tool allowlist.
- `code/evaluation/main.py` — scripted agent/evidence regressions, aggregate phase checks, and real provider acceptance runner.
- `code/requirements.txt` — pinned OpenAI SDK.
- `code/README.md` — offline and live commands plus credential guidance.

## Verification

- `python3 code/evaluation/main.py --checks phase1` — passed.
- `python3 code/evaluation/main.py --samples request_01,request_02,request_03 --live` — blocked before a completed model action; it returned `live_acceptance_blocked` with two failed provider attempts and no fabricated usage or financial result.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Missing Critical] Material-evidence filtering and supported user-level salary target**
- **Found during:** Task 2
- **Issue:** Treating every text message as required left an amount-free salary confirmation unresolved; a valid user-level salary amendment also had no explicit future event to target.
- **Fix:** Indexed messages only when they contain a currency amount, and created a scheduled salary fact only when three prior settled salaries support that recurring scope.
- **Files modified:** `code/main.py`, `code/evaluation/main.py`
- **Verification:** `python3 code/evaluation/main.py --checks evidence`
- **Committed in:** `24287a4`

**Total deviations:** 1 auto-fixed (1 missing critical functionality).

## Authentication Gates

Live acceptance remains blocked: the configured OpenAI environment could not complete the first provider action. Supply a working `OPENAI_API_KEY`, then rerun the documented `--live` command; it will assert the three exact sample amount/date pairs and print measured usage.

## Known Stubs

None.

## Next Phase Readiness

Phase 2 can reuse `run_request`, `forecast_baseline`, and `check_schedule` for deterministic payment selection. Do not treat Phase 1 as live-accepted until the provider blocker is resolved and the three required sample results pass.

## Self-Check: PASSED

- `code/main.py`, `code/evaluation/main.py`, `code/README.md`, `code/requirements.txt`, and this summary exist.
- Task commits `42ae141`, `24287a4`, and `0dfaa64` exist in git history.
