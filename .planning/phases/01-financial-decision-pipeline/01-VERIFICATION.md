---
phase: 01-financial-decision-pipeline
verified: 2026-09-13T23:07:05Z
status: gaps_found
score: 5/11 must-haves verified
overrides_applied: 0
gaps:
  - truth: "The three named public requests match exact baseline amount/date oracles through the real agent path."
    status: failed
    reason: "The required live acceptance exits 2 before a completed model action. Independent replay shows request_02 returns 18671640.83 rather than 17229139.2 and request_03 returns 1153856.95/2019-10-15 rather than 873000/2019-11-15 when supplied source-shaped facts are applied."
    artifacts:
      - path: "code/evaluation/main.py"
        issue: "Only request_01 is asserted in offline sample_check; request_02 and request_03 are checked only by the unavailable live path."
    missing:
      - "Make all three exact sample baseline oracles pass through the production run_request path and obtain a successful measured live-provider run."
  - truth: "Necessary linked image evidence is source-grounded and cannot silently invent a financial amount."
    status: failed
    reason: "_apply_evidence checks only the linked path and model-provided field metadata. It accepts both IDR 1 and IDR 4365000 for actual image_01/event_253 without inspecting or validating image content."
    artifacts:
      - path: "code/main.py"
        issue: "_apply_evidence at lines 351-401 has no image extraction or source-value verification."
    missing:
      - "Validate the net amount extracted from the linked PNG before applying it, and reject incorrect or ambiguous extraction."
  - truth: "Forecasts conservatively include protected essential spending and supported recurring commitments."
    status: failed
    reason: "Production code never reads expense_categories_to_protect or implements the required unsupported-cadence essential reserve/residual budget policy; no conflict-precedence implementation was found."
    artifacts:
      - path: "code/main.py"
        issue: "No references to protected-category profile fields or essential 30-day reserve/conflict logic."
    missing:
      - "Implement and test protected essential and irregular-essential reserves plus evidence conflict precedence."
---

# Phase 1: Financial Decision Pipeline Verification Report

**Phase Goal:** Run a supplied request through a model-driven tool loop that resolves evidence and obtains a deterministic checked baseline forecast and safe-to-pay/full-payment date.
**Verified:** 2026-09-13T23:07:05Z
**Status:** gaps_found
**Re-verification:** No — initial verification

## Goal Achievement

The phase is marked MVP in the roadmap, but its goal is not a valid User Story (it does not begin `As a …, I want …, so that …`). Therefore a MVP user-flow coverage table cannot be constructed from the roadmap metadata. The code audit below applies the normal goal-backward contract and does not treat that metadata defect as evidence of implementation success.

### Observable Truths

| # | Truth | Status | Evidence |
| --- | --- | --- | --- |
| 1 | Terminal program loads relevant supplied records and safely interprets necessary message/image facts. | ✗ FAILED | CSV loading, finite-money rejection, and injection tests exist, but actual image_01 accepts arbitrary net values without checking image contents. |
| 2 | Forecast begins from snapshot balance, handles cash movements/FX, and includes supported commitments with protected essentials. | ✗ FAILED | Snapshot and supplied-FX paths work, but `code/main.py` never reads `expense_categories_to_protect` or implements irregular essential reserves/conflict precedence. |
| 3 | 90-day capacity and earliest full date match all three named oracles; unresolved facts are reported. | ✗ FAILED | request_01 matches. request_02 is `18671640.83` versus `17229139.2`; request_03 is unresolved without evidence and `1153856.95`/`2019-10-15` after source-shaped evidence, versus `873000`/`2019-11-15`. |
| 4 | Focused runnable checks cover financial basics and usage is counted from the first provider response. | ✓ VERIFIED | `--checks phase1` exits 0; checks cover malformed money, FX, reserve breach/date ordering, and scripted usage totals. `_usage` increments each dict response attempt. |
| 5 | A structured request produces checked baseline capacity without replaying settled history. | ✓ VERIFIED | `reconstruct_cash_state` skips settlements on/before request date (lines 108-123); request_01 stripped sample produces `25256`, `2024-03-03`. |
| 6 | Every schedule is checked across the full 90-day horizon, including before its first payment. | ✓ VERIFIED | `check_schedule` initializes balance/floor before payments and loops offsets 0–89 (lines 253-282); later-pressure and early-breach checks pass. |
| 7 | Unresolved evidence and baseline infeasibility are distinct outcomes. | ✓ VERIFIED | `forecast_baseline` returns `analysis_error` for unresolved evidence and `ok` with `baseline_feasible=False`/zero capacity for a breach (lines 285-303). |
| 8 | A bounded model-driven orchestrator selects allowed tools and completes a checked baseline. | ✗ FAILED | Host loop and injected-client replay exist, but the required real provider acceptance exits 2 with two failed attempts and no tool action. |
| 9 | User-level messages and linked images update only validated authorized facts. | ✗ FAILED | Scope/path/type checks exist, but the host accepts a model-supplied amount for a real PNG without validating it against the image. |
| 10 | Model cannot bypass money checks, finish stale, or invent output amounts. | ✓ VERIFIED | Literal dispatcher owns forecast/finish; finish ignores model money and requires current revision. Agent checks exercise early finish, unknown tool, and stale forecast. |
| 11 | All three named public requests match exact baseline oracles and live calls report actual usage. | ✗ FAILED | Live command exits non-zero, and the evaluator has no offline exact assertion for request_02/request_03. Independent production-loop replay disproves their expected outputs. |

**Score:** 5/11 truths verified

### Required Artifacts

| Artifact | Expected | Status | Details |
| --- | --- | --- | --- |
| `code/main.py` | Financial tools, evidence validation, orchestrator, counters | ⚠️ HOLLOW | Exists (527 lines), substantive, imported/used, and reads supplied CSV data. Image-value validation and protected-essential forecasting are absent. |
| `code/evaluation/main.py` | Offline replays, evidence checks, live acceptance | ⚠️ PARTIAL | Exists (230 lines), substantive, and invokes production functions. Its offline public-sample oracle covers only request_01; live acceptance is blocked. |
| `code/requirements.txt` | One pinned model SDK | ✓ VERIFIED | Contains `openai==1.109.0`; used only by the live client. |
| `code/README.md` | Model/environment/offline/live commands | ✓ VERIFIED | Specifies model ID, `OPENAI_API_KEY`, pinned install command, and acceptance command. |

### Key Link Verification

| From | To | Via | Status | Details |
| --- | --- | --- | --- | --- |
| `code/main.py` | deterministic forecast and schedule checker | allowlisted `_dispatch` | ✓ WIRED | `forecast_baseline` dispatches to host `forecast_baseline`; forecast uses `check_schedule`. |
| `code/evaluation/main.py` | `code/main.py` | scripted/live client through `run_request` | ✓ WIRED | Imports production functions at line 15; `live_samples` calls `run_request` at line 188. Live behavior is nevertheless blocked. |

### Data-Flow Trace (Level 4)

| Artifact | Data Variable | Source | Produces Real Data | Status |
| --- | --- | --- | --- | --- |
| `code/main.py` | `context.events`, `flows`, `rates` | Supplied CSVs via `load_dataset` | Yes for profile/event/FX data | ✓ FLOWING |
| `code/main.py` | evidence fact amount | Model action argument | No source-grounded validation of image amount | ✗ HOLLOW |
| `code/evaluation/main.py` | public sample result | `run_request` / deterministic functions | request_01 yes; request_02/03 lack passing oracle coverage | ⚠️ PARTIAL |

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
| --- | --- | --- | --- |
| Offline core/agent/evidence regressions | `python3 code/evaluation/main.py --checks phase1` | `checks passed` (exit 0) | ✓ PASS |
| request_01 stripped baseline | `--samples request_01 --structured-only` | `25256`, `2024-03-03` | ✓ PASS |
| request_02 stripped baseline | `--samples request_02 --structured-only` | `18671640.83`, `2025-09-15`; expected `17229139.2`, `2025-09-15` | ✗ FAIL |
| request_03 stripped baseline | `--samples request_03 --structured-only` | `analysis_error`; expected source-resolved baseline | ✗ FAIL |
| Production loop with source-shaped request_02/request_03 facts | injected `run_request` replay | `18671640.83`/`2025-09-15`; `1153856.95`/`2019-10-15` | ✗ FAIL |
| Required live acceptance | `python3 code/evaluation/main.py --samples request_01,request_02,request_03 --live` | exits 2: `live_acceptance_blocked`, two provider attempts, no action | ✗ FAIL |
| Linked-PNG amount validation | `_apply_evidence(image_01, amount=1)` | accepted and changed `event_253` to `1` | ✗ FAIL |

### Probe Execution

Step 7c: SKIPPED — no declared or conventional `scripts/**/tests/probe-*.sh` probes found.

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
| --- | --- | --- | --- | --- |
| AGENT-01 | 01-02 | Bounded model-driven checked result | ✗ BLOCKED | Real provider path did not complete. |
| DATA-01 | 01-01/01-02 | Supplied data, scoped joins, label exclusion | ✓ SATISFIED | CSV loader and `_request` strip output-label fields. |
| DATA-03 | 01-01 | Supplied dated FX | ✓ SATISFIED | `_converted_amount` requires exact dated direction; synthetic and supplied-row checks pass. |
| CASH-01 | 01-01 | Snapshot and duplicate lifecycle handling | ⚠️ PARTIAL | Snapshot behavior is verified; duplicate detection is limited to cancelled linked rows and has no direct duplicate test. |
| CASH-03 | 01-01 | Pending debits/commitments and excluded credits | ✓ SATISFIED | Pending debit reserve and excluded pending credits/failed/cancelled/unrealized rows are exercised. |
| CASH-04 | 01-01/01-02 | Supported recurrence and conservative protected essentials | ✗ BLOCKED | No protected-category or irregular-essential-reserve implementation. |
| EVID-01 | 01-02 | Relevant message changes/conflict precedence | ✗ BLOCKED | Salary amendment path exists; required conflict-precedence rules are not implemented. |
| EVID-02 | 01-02 | Correct linked-PNG missing amount | ✗ BLOCKED | Arbitrary finite amount for actual linked image is accepted. |
| EVID-04 | 01-02 | Validate evidence and reject embedded instructions | ✗ BLOCKED | Injection/scope checks pass, but extracted amount correctness is not validated. |
| FORE-01 | 01-01/01-02 | 90-day forecast/date ordering | ✓ SATISFIED | Whole-horizon loop and same-day/boundary checks pass. |
| FORE-02 | 01-01/01-02 | Maximum safe current payment | ✓ SATISFIED | Deterministic whole-path headroom and later-pressure oracle pass. |
| FORE-03 | 01-01/01-02 | Earliest safe full-payment date | ✓ SATISFIED | Replays full payment per candidate date; generic/request_01 checks pass. |
| EVAL-02 | 01-01/01-02 | Focused runnable financial checks | ✓ SATISFIED | `--checks phase1` covers money, states, FX, dates, reserve, agent boundaries. |

No Phase 1 requirements are orphaned: all roadmap-mapped IDs appear in at least one Phase 1 plan.

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
| --- | --- | --- | --- | --- |
| `code/main.py` | 351-401 | Accepts any finite model-provided linked-image net amount | 🛑 Blocker | Untrusted model can change financial evidence without source validation. |
| `code/main.py` | 1-527 | No protected-category/irregular-essential/conflict-precedence logic | 🛑 Blocker | Forecast may omit required conservative commitments. |
| `code/evaluation/main.py` | 64-75 | Public exact oracle assertion only for request_01 | 🛑 Blocker | Offline suite can pass while required request_02/03 outcomes are wrong. |
| `.planning/ROADMAP.md` | Phase 1 | `mode: mvp` with a non-User-Story goal | ℹ️ Info | MVP-specific flow verification cannot be applied until roadmap metadata is corrected. |

No `TBD`, `FIXME`, or `XXX` debt markers were found in phase-modified code.

### Human Verification Required

None. The blocking failures are observable programmatically. A working provider credential/service is required to close the live acceptance gate after the code gaps are fixed.

### Gaps Summary

This is an **Escalation Gate**: Phase 1 cannot advance on the current evidence. The deterministic skeleton and its basic regressions are real, but the phase contract requires source-grounded image evidence, protected/essential conservative forecasting, and all three exact source-resolved samples through a successful model run. The offline suite is insufficient because it does not assert request_02/request_03 and passes while those production outcomes are wrong.

---

_Verified: 2026-09-13T23:07:05Z_
_Verifier: the agent (gsd-verifier)_
