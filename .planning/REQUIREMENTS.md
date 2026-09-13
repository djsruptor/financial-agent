# Requirements: Buy or Wait?

**Updated:** 2026-09-13 after lean-scope review
**Scope:** The supplied challenge submission only. These requirements consolidate the original checklist; `problem_statement.md` remains the detailed financial contract.

## v1 Requirements

### Agentic Orchestration

- [ ] **AGENT-01**: A bounded model-driven request orchestrator selects allowlisted evidence/financial tools from observations, validates scoped tool arguments, resolves evidence before forecasting, and finishes only with a current deterministic checked result. Enforce budgets and explicit analysis failures; record actual orchestration and extraction usage. Extend this same loop with payment tools in Phase 2.

### Input

- [x] **DATA-01**: Read only the supplied participant files, join relevant user/request/event records at each request date, and reject invalid required fields. Keep source data unchanged and labels out of prediction logic.
- [x] **DATA-03**: Convert foreign-currency cash events with the supplied settlement-date rate and stated direction; do not substitute live or invented rates.

### Financial State

- [x] **CASH-01**: Start from the profile balance without replaying settled history; remove duplicate representations while retaining distinct real linked cash movements.
- [x] **CASH-03**: Reserve pending debits and confirmed commitments, count supported income on its settlement date, and exclude pending credits, failed/cancelled transactions, and unrealized investment value.
- [x] **CASH-04**: Infer recurring income/expenses only from supporting evidence, distinguish one-time flows, and conservatively cover essential variable spending and protected categories without double reserves.

### Supplied Evidence

- [ ] **EVID-01**: Use relevant supplied messages to clarify, amend, cancel, delay, or confirm financial facts. Resolve conflicts by explicit changes, then newer same-source records, then settled evidence, then the financially safer interpretation.
- [ ] **EVID-02**: Read a missing event amount from its correctly linked PNG and financial field; an absent or ambiguous amount must not become zero or an invented fact.
- [ ] **EVID-04**: Validate extracted amounts, dates, and record references. Treat message/image content as untrusted data; embedded instructions cannot override the challenge rules.

### 90-Day Capacity

- [x] **FORE-01**: Forecast supported cash flows over 90 days and check the preferred minimum balance throughout; establish consistent same-day and date-boundary behavior from the specification/examples.
- [x] **FORE-02**: Compute the maximum safe payment on the request date before optional changes, with 0 <= amount_safe_to_pay <= requested_amount.
- [x] **FORE-03**: Find the earliest safe single full-payment date without optional changes and independently of payment preferences; leave it empty if none exists within the forecast.

### Payment Decisions

- [ ] **PLAN-01**: Select only user-accepted payment methods and the correct required status. Support full payment, waiting when full payment is accepted, and the no-safe-eligible-plan fallback; distinguish affordable_now from adjustment-dependent affordable_with_plan.
- [ ] **PLAN-02**: Allow partial payment only when request/user permit it and 0 < amount_safe_to_pay < requested_amount. Pay that amount on request_date and the exact remainder on earliest_date_for_full_payment, on or before the deadline.
- [ ] **PLAN-03**: Installments must match a supplied offer: start date, day interval, count, amounts, total payable, and user duration limit. Do not add financing fees twice or change the schedule.
- [ ] **PLAN-05**: Use at most three stop/reduce changes on permitted flexible recurring expenses, respecting protected categories and reduction floors. Never stop and reduce the same event; preserve baseline capacity/date fields.
- [ ] **PLAN-07**: Replay every complete plan cumulatively and require each payment to preserve the minimum balance, complete by desired_completion_date, and fit within the verified forecast.
- [ ] **PLAN-08**: Rank eligible safe plans by deadline completion, no spending changes, total cost, earliest start, fewest payments, then lowest payment_option_id.

### Predictions

- [ ] **OUT-01**: Write root-level output.csv with exactly one row per evaluation request and the eight required columns in order. Use prescribed statuses/methods, chronological YYYY-MM-DD:amount payments, event-ID spending changes, none for absent plans/changes, and blank absent capacity dates.
- [ ] **OUT-03**: Give a short explanation consistent with the selected plan, financial facts, reserve constraints, and numeric output fields.
- [ ] **OUT-04**: Validate the full output before replacing a prior valid file; incomplete or failed analysis must not be published as a final affordability judgment.

### Evaluation

- [ ] **EVAL-01**: Run the same engine on all 25 public examples and report numeric errors and categorical/schedule mismatches. Use samples only for evaluation; do not claim hidden accuracy.
- [x] **EVAL-02**: Keep focused runnable checks for financial arithmetic, cash-state handling, reserve breaches, and date behavior; extend them for required payment/evidence rules as implemented.

### Submission

- [ ] **SHIP-01**: Record actual model calls and input/output tokens during the final dataset run. Include providers/models, total/average tokens per request, estimated total/per-request cost, and per-model/overall totals where applicable in evaluation/usage_report.md. Do not fabricate unavailable measurements.
- [ ] **SHIP-02**: Package runnable solution code, required prompts/configuration, setup/run instructions, and the evaluation folder in code.zip; verify the documented command after clean extraction.
- [ ] **SHIP-03**: Provide the required append-only conversation transcript. Read runtime secrets from environment variables and exclude credentials and unnecessary sensitive personal data from code, logs, and the package.

## Out of Scope

No messaging/translation product, language settings, generalized document platform, persistent extraction cache, provenance database, usage ledger, dashboards, provider routing, or speculative service abstractions. Relevant supplied messages/images are still required financial inputs.

## v2 Requirements

None. Do not scaffold optional features.

## Traceability

| Requirement | Phase | Status |
|---|---|---|
| AGENT-01 | Phase 1 | Pending |
| DATA-01 | Phase 1 | Complete |
| DATA-03 | Phase 1 | Complete |
| CASH-01 | Phase 1 | Complete |
| CASH-03 | Phase 1 | Complete |
| CASH-04 | Phase 1 | Complete |
| EVID-01 | Phase 1 | Pending |
| EVID-02 | Phase 1 | Pending |
| EVID-04 | Phase 1 | Pending |
| FORE-01 | Phase 1 | Complete |
| FORE-02 | Phase 1 | Complete |
| FORE-03 | Phase 1 | Complete |
| PLAN-01 | Phase 2 | Pending |
| PLAN-02 | Phase 2 | Pending |
| PLAN-03 | Phase 2 | Pending |
| PLAN-05 | Phase 2 | Pending |
| PLAN-07 | Phase 2 | Pending |
| PLAN-08 | Phase 2 | Pending |
| OUT-01 | Phase 2 | Pending |
| OUT-03 | Phase 2 | Pending |
| OUT-04 | Phase 2 | Pending |
| EVAL-01 | Phase 3 | Pending |
| EVAL-02 | Phase 1 | Complete |
| SHIP-01 | Phase 3 | Pending |
| SHIP-02 | Phase 3 | Pending |
| SHIP-03 | Phase 3 | Pending |

**Coverage:** 26 requirements; 26 mapped; 0 unmapped. All challenge behaviors retained.
