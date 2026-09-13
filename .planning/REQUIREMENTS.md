# Requirements: Buy or Wait?

**Defined:** 2026-09-13
**Core Value:** Recommend only payment plans that complete the request by its deadline while protecting essential spending and the user's minimum balance throughout the 90-day forecast.

## v1 Requirements

### Dataset and Context

- [ ] **DATA-01**: The participant can load the supplied CSVs and image links without modifying source data, with explicit diagnostics for missing files, malformed fields, duplicate identifiers, invalid references, and non-finite monetary values.
- [ ] **DATA-02**: Each request uses relevant user-, request-, and event-linked context at its supplied request date, preserving evidence timestamps and effective dates rather than relying on the current clock.
- [ ] **DATA-03**: Foreign-currency cash events are converted to the user's home currency using the supplied settlement-date rate in the stated currency direction; missing required rates produce an explicit error.

### Financial State

- [ ] **CASH-01**: Forecasting starts from the supplied current available balance without adding historical settled income or subtracting historical settled expenses again.
- [ ] **CASH-02**: Transaction lifecycle resolution removes duplicate representations while retaining distinct real cash movements such as settled refunds and investment-sale proceeds.
- [ ] **CASH-03**: The forecast reserves pending debits and supported future payments, counts confirmed income on its settlement date, and excludes pending credits, failed/cancelled transactions, and unrealized investment values.
- [ ] **CASH-04**: Recurring income and fixed commitments are inferred only from supported history and confirmed facts, distinguishing regular flows from one-time payments and applying supported recurrence end dates.
- [ ] **CASH-05**: Essential variable spending is forecast conservatively from supplied history while protecting the user's specified categories and avoiding duplicate reserves for the same obligation.

### Forecast and Baseline Capacity

- [ ] **FORE-01**: A baseline 90-day forecast checks the minimum balance at cash-flow checkpoints, with documented and tested day-boundary, month-end, and same-day ordering rules.
- [ ] **FORE-02**: `amount_safe_to_pay` is the largest safe payment on the request date before optional spending changes and satisfies `0 <= amount_safe_to_pay <= requested_amount`.
- [ ] **FORE-03**: `earliest_date_for_full_payment` is the first safe single full-payment date in the forecast without optional changes, independent of accepted methods; it is empty when no such date exists.

### Evidence Interpretation

- [ ] **EVID-01**: Relevant English and Indonesian messages can amend financial facts including amounts, payment dates, cancellations, income confirmation, and recurrence scope, including messages without a direct event link.
- [ ] **EVID-02**: Missing event amounts are extracted from the correct linked PNG and financial field with amount, currency, and source provenance; missing or ambiguous evidence remains unresolved instead of becoming zero.
- [ ] **EVID-03**: Conflicts are resolved in the specified order: explicit cancellation/settlement/amendment, newer same-source evidence, settled over estimated evidence, then the financially safer interpretation.
- [ ] **EVID-04**: Extracted facts pass identifier, type, value, and scope validation; instructions embedded in messages or images cannot alter problem rules, execute actions, or directly set financial decisions.
- [ ] **EVID-05**: The participant can reproduce evidence interpretation through documented prompts/configuration and validated extraction artifacts, with cache invalidation tied to source content, prompt settings, and model identity.
- [ ] **EVID-06**: Every model integration call records available provider/model identity and input/output usage, including charged retries, with explicit cache-reuse and unknown-usage accounting.

### Payment Planning

- [ ] **PLAN-01**: Full payment and waiting are recommended only when accepted by the user and safe by the completion deadline; full payment with no required changes is `affordable_now` and waiting for safe future full payment is `affordable_later`.
- [ ] **PLAN-02**: Partial payment is considered only when allowed by the request and user and `0 < amount_safe_to_pay < requested_amount`; its exact two payments are the safe amount on the request date and the remainder on the baseline earliest full-payment date, no later than the deadline.
- [ ] **PLAN-03**: Installment candidates exactly reproduce supplied offer amounts, count, start date, and day intervals, reconcile with total payable, and do not add financing fees a second time.
- [ ] **PLAN-04**: Every selected immediate payment method is in the user's accepted methods, installment offers respect `max_installment_months`, and future capacity is not confused with method eligibility.
- [ ] **PLAN-05**: Spending changes affect only recurring flexible events in user-permitted categories, never protected or fixed spending.
- [ ] **PLAN-06**: An adjusted plan uses at most three legal stop/reduce actions, respects each reduction floor, and never stops and reduces the same event; baseline capacity fields remain unchanged.
- [ ] **PLAN-07**: Every complete candidate schedule is replayed cumulatively through the forecast and rejected if any payment breaches the reserve, misses the completion deadline, or lies beyond the validated horizon.
- [ ] **PLAN-08**: Safe eligible candidates are ranked by completion deadline compliance, no spending changes, least total paid, earliest start, fewest payments, and lowest payment-option ID.
- [ ] **PLAN-09**: Final statuses and methods reflect the selected complete plan, including `affordable_with_plan` for adjustment-dependent full payments and `not_recommended` when no safe eligible option exists; incomplete analysis is never reported as a final affordability judgment.

### Output

- [ ] **OUT-01**: The final root-level `output.csv` has exactly the required eight columns in order and one row per evaluation request ID, with no solved-sample rows or duplicate/missing predictions.
- [ ] **OUT-02**: Payment plans use chronological `YYYY-MM-DD:amount` entries joined by `|`, spending changes use the prescribed event-ID syntax, absent plans/changes use `none`, and absent capacity dates are empty.
- [ ] **OUT-03**: Each recommendation includes a concise explanation grounded in the chosen schedule, relevant commitments/evidence, and reserve constraints, consistent with all numeric output fields.
- [ ] **OUT-04**: Final export occurs only after batch validation succeeds; unresolved evidence, extraction failure, or incomplete analysis cannot overwrite a valid output with a partial or misleading submission.

### Evaluation

- [ ] **EVAL-01**: The participant can run the same engine against all 25 solved examples and obtain per-field numeric error, categorical/schedule accuracy, and actionable mismatch details.
- [ ] **EVAL-02**: Runnable regression checks cover the core monetary and cash-state invariants from the first engine implementation and expand to evidence, schedules, preferences, and adjustment failures as those capabilities ship.
- [ ] **EVAL-03**: Prediction code never reads organizer-only data or hardcoded labels; sample outputs are used only by evaluation, and final accuracy claims distinguish measured sample results from unknown hidden-ground-truth performance.

### Submission

- [ ] **SHIP-01**: `evaluation/usage_report.md` inside `code.zip` reports the final prediction run's providers/models, calls, input/output tokens, total/average tokens per request, and estimated total/per-request costs, including per-model and overall totals when applicable.
- [ ] **SHIP-02**: `code.zip` contains runnable solution code, prompts/configuration, setup/run instructions, and the required evaluation folder, and passes a documented clean-extraction smoke run without machine-specific paths.
- [ ] **SHIP-03**: The submission includes the required conversation transcript from append-only logging, and code/configuration/logs/package exclude credentials and unnecessary sensitive personal data; runtime secrets come from environment variables.

## v2 Requirements

None committed. Optional OCR optimization, parallel processing, additional providers, and richer diagnostics require a demonstrated need after the required solution works.

## Out of Scope

| Feature | Reason |
|---|---|
| Live bank, market, or FX integrations | Required evidence and rates are supplied locally |
| Payments, trades, or security recommendations | The challenge requests affordability decisions |
| Web/mobile UI, authentication, hosting | A terminal submission is the required interface |
| Voice input | No voice notes are supplied |
| Training on hidden labels or hardcoding sample answers | Prohibited or invalid evaluation behavior |
| Speculative services, vector retrieval, or agent framework | Identifier joins and one deterministic pipeline cover the current task |

## Acceptance and Release Criteria

- All v1 requirements have runnable verification or artifact evidence; financial safety and serialization checks have zero unresolved violations.
- All 25 public examples are evaluated. Every discrepancy is investigated and documented; an unsupported promise of perfect sample or hidden accuracy is not a release criterion.
- All 250 current evaluation requests have one validated output row; source dataset files remain unchanged.
- Final usage figures refer to the run that produced the delivered output, with unavailable usage explicitly disclosed rather than guessed.
- A clean extraction of the submission package can execute the documented workflow, with any model credentials supplied externally.

## Traceability

Pending roadmap assignment. Each v1 requirement will map to exactly one owning phase; later phases may extend its regression coverage.

---
*Requirements defined: 2026-09-13 from the approved full challenge scope and completed research.*
