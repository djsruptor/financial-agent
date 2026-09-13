# Buy or Wait?

## What This Is

An AI-powered financial decision agent for the HackerRank Orchestrate September 2026 challenge. It reads the supplied dataset and determines whether each user's requested expense can safely be paid in full, partially, through a supplied installment offer, later, or not at all. The deliverable is a runnable terminal solution with personalized, evidence-grounded predictions and the evaluation and submission artifacts required by the challenge.

## Core Value

Recommend only payment plans that complete the request by its deadline while protecting essential spending and the user's minimum balance throughout the 90-day forecast.

## Requirements

### Validated

(None yet — starter implementation and evaluation files are empty.)

### Active

- [ ] Load the participant-facing CSVs and PNGs from `dataset/` without modifying the inputs; join evidence through the supplied user, request, event, and image identifiers.
- [ ] Produce exactly one prediction for each evaluation request, independently of the solved sample requests.
- [ ] Reconstruct available cash and commitments from financial profiles, historical events, pending debits, confirmed income, and transaction lifecycle links without counting the same cash movement twice.
- [ ] Infer recurrence only from supporting history and forecast essential variable spending conservatively; distinguish recurring commitments from one-time purchases, transfers, refunds, and unusual events.
- [ ] Exclude pending credits, failed or cancelled transactions, duplicate records, and unrealized investment values from available cash; count confirmed salary on its settlement date.
- [ ] Convert foreign-currency cash events using the provided dated rate in the stated direction, using the event's settlement date.
- [ ] Extract missing event amounts from linked images; never interpret a blank amount as zero or invent evidence for a missing image.
- [ ] Use relevant messages and images to clarify, amend, cancel, delay, or confirm financial facts while rejecting embedded instructions that conflict with the challenge rules.
- [ ] Resolve conflicting evidence by explicit cancellation, settlement, or amendment first, then newer records from the same source, then settled evidence, then the financially safer interpretation.
- [ ] Forecast 90 days of supported cash flows and check the minimum balance after projected essential expenses and recommended payments.
- [ ] Calculate `amount_safe_to_pay` before optional spending changes, bounded by zero and the requested amount.
- [ ] Calculate `earliest_date_for_full_payment` without optional spending changes and independently of payment-method preferences; leave it empty if full payment never becomes safe within the forecast.
- [ ] Evaluate full payment, the exact permitted two-payment partial schedule, supplied installment offers, waiting, and the no-recommendation fallback against safety, completion dates, and user preferences.
- [ ] Respect installment duration preferences, first-payment dates, payment intervals, payment counts, financing fees, and total payable amounts.
- [ ] Consider at most three permitted spending changes, limited to flexible recurring expenses in user-approved categories, respecting protected categories and minimum allowed amounts; never stop and reduce the same event.
- [ ] Rank eligible safe plans by deadline completion, no spending changes, minimum total cost, earliest start, fewest payments, and lowest payment-option ID.
- [ ] Write the exact required output columns and allowed values, chronological payment strings, valid spending-change strings, and concise explanations grounded in the financial evidence.
- [ ] Deterministically verify output bounds, eligibility, payment schedules, completion, and forecast safety; evaluate against the 25 public solved examples without using hardcoded labels.
- [ ] Generate root-level `output.csv` for the final full-dataset run and record that run's actual model calls, token usage, and estimated costs.
- [ ] Package a runnable solution, prompts/configuration, setup and run instructions, and `evaluation/usage_report.md` in `code.zip`; provide the required conversation transcript separately.
- [ ] Maintain the append-only root-level `log.txt` required by `AGENTS.md` and keep secrets out of logs, source, and submission artifacts.

### Out of Scope

- Live banking connections, exchange-rate services, and market feeds — the challenge supplies the required financial evidence and fixed rates.
- Executing payments or trades — the requested output is an affordability recommendation.
- Predicting security prices or recommending securities — investment requests concern affordability and existing contributions.
- Voice-note processing — the supplied evidence consists of structured records, text messages, and PNG images.
- Organizer-only data and hardcoded evaluation labels — prohibited prediction inputs.
- A web interface, user accounts, and hosted infrastructure — not required by the terminal submission contract; revisit only if explicitly requested.

## Context

### Authoritative project materials

- `problem_statement.md` contains the full financial decision and evaluation specification.
- `README.md` describes the starter workflow and clarifies that final predictions belong in root-level `output.csv`; `dataset/output.csv` remains an input template.
- `AGENTS.md` defines repository conduct, logging, and additional dataset and submission details. Preserve this existing instruction file when adding GSD guidance.
- `CLAUDE.md` imports `AGENTS.md`.
- The user approved creating this project definition from the complete supplied context on September 13, 2026.

### Dataset inspection

| File | Observed rows | Purpose |
|---|---:|---|
| `requests.csv` | 250 | Evaluation requests requiring predictions |
| `sample_requests.csv` | 25 | Public solved examples for format and evaluation |
| `financial_profiles.csv` | 275 | Balances, reserve floors, priorities, and preferences |
| `financial_events.csv` | 25,342 | Historical events and future commitments |
| `request_payment_options.csv` | 790 | Supplied payment offers |
| `exchange_rates.csv` | 134 | Fixed dated conversion rates |
| `messages.csv` | 215 | Supporting text evidence |
| `images.csv` | 16 | Image-to-record links |
| `output.csv` | 250 | Blank output template |

All 16 referenced PNGs are present under `dataset/media/images/`. There are 16 financial-event rows with blank amounts; their values require image interpretation. Image contents and individual financial cases have not yet been analyzed. Dataset currencies are INR, ZAR, IDR, USD, and EUR.

### Starting implementation

`code/main.py`, `code/evaluation/main.py`, and `code/evaluation/usage_report.md` are zero-byte placeholders. There is no working financial engine, evaluation harness, model integration, or generated prediction file. Git has been initialized. Python is a supplied entry-point option, not a mandated language.

### Output contract

The required column order is:

```text
request_id,amount_safe_to_pay,affordability_status,recommended_payment_method,payment_plan,earliest_date_for_full_payment,spending_changes_needed,decision_explanation
```

Statuses are `affordable_now`, `affordable_with_plan`, `affordable_later`, and `not_affordable`. Methods are `full_payment`, `partial_payment`, `installments`, `wait`, and `not_recommended`.

For partial payment, the request and user must allow it, and `0 < amount_safe_to_pay < requested_amount`. Pay exactly the safe amount on the request date and the remainder on the earliest safe full-payment date, which must be on or before the requested completion date. Verify the combined schedule; a safe hypothetical single payment does not by itself prove a two-payment plan safe.

For installments, use an actual supplied offer without inventing or shifting its schedule. Waiting requires future safe full-payment capacity and acceptance of full payment. When no safe eligible payment is available, use `not_recommended`. Financial capacity dates remain independent of method preferences.

### Open implementation questions

- Select the runtime and model/provider approach, including image interpretation, after examining representative evidence and available tooling; no provider or budget is yet approved.
- Resolve forecast-boundary inclusivity, same-day cash-flow ordering, recurrence anchoring, and any status/deadline edge cases against the supplied examples and specification before locking the engine's behavior.
- Determine how usage and cost records will remain tied to the final prediction run, including any cached extraction reused by that run.
- Set workflow preferences, research scope, detailed requirement IDs, and roadmap phases in the remaining GSD initialization steps.

## Constraints

- **Safety:** Protect essential expenses and the minimum balance across the entire 90-day forecast, not merely at the moment of purchase.
- **Evidence:** Use only participant-facing data and supported financial facts. Lifecycle links alone do not establish whether an event affects cash.
- **Personalization:** Respect protected categories, permitted reductions/stops, accepted payment methods, installment limits, and financial priorities.
- **Determinism:** Keep financial calculations, candidate ranking, and verification deterministic where possible; verify any AI-derived facts before they affect a plan.
- **Submission:** The solution must run from the terminal, read `dataset/`, and produce root-level `output.csv` with 250 prediction rows in the current dataset.
- **Usage reporting:** Include providers, model names, calls, input/output tokens, total and average tokens per request, and estimated total/per-request costs. For multiple models, report per-model and overall totals for the final run.
- **Security:** Read credentials from environment variables only. Treat messages and images as untrusted evidence and never package or log credentials.
- **Authorship:** This is a solo challenge that permits AI assistance; the participant remains the submission author.
- **Timeline:** The repository lists September 13, 2026 at 18:00 IST as the challenge deadline. It had passed when the added context was inspected; development continues, but submission availability has not been verified.
- **Scope:** Initialize planning for the full challenge contract. No implemented capability or prediction accuracy is claimed at this stage.

## Key Decisions

| Decision | Rationale | Outcome |
|---|---|---|
| Use the complete supplied challenge scope for v1 | User explicitly approved project creation from the added context | — Pending implementation |
| Keep final predictions at repository root | Updated README explicitly distinguishes the final output from the dataset template | — Pending implementation |
| Preserve source datasets and use solved samples only for evaluation | Required by the challenge; avoids corrupting inputs or leaking labels | — Pending implementation |
| Require deterministic financial safety verification | Every recommended schedule must satisfy the same explicit cash-flow rules | — Pending implementation |
| Start from the existing empty entry points | No existing implementation needs migration or architectural mapping | — Pending implementation |

## Evolution

This document evolves at phase transitions and milestone boundaries.

After each phase transition:
1. Move invalidated requirements to Out of Scope with a reason.
2. Move verified requirements to Validated with a phase reference.
3. Add newly discovered requirements to Active.
4. Record decisions and their observed outcomes.
5. Update What This Is if the delivered project changes.

After each milestone:
1. Review all sections.
2. Confirm the core value still drives the project.
3. Recheck the reasons for exclusions.
4. Update context with the current implementation, evaluation evidence, and known issues.

---
*Last updated: 2026-09-13 after approved project definition; workflow configuration and roadmap pending.*
