# Pitfalls Research

**Domain:** Buy or Wait? financial reconstruction and planning
**Researched:** 2026-09-13
**Confidence:** HIGH for contract risks; MEDIUM for proposed prevention details

## Critical Pitfalls

| Failure | Early warning sign | Prevention | Phase |
|---|---|---|---|
| Replaying settled history into the current balance | Cash grows by historical salary totals before forecasting | Treat profile balance as the snapshot and history as recurrence/lifecycle evidence | 1 |
| Treating all lifecycle links as duplicates | A genuine settled refund or sale disappears with its linked purchase | Resolve cash state by event meaning and status; links alone do not determine inclusion | 1 |
| Counting pending credits or asset values | Capacity increases from an unapproved bonus or unrealized portfolio | Distinguish confirmed future cash from pending/non-cash rows | 1 |
| Extrapolating unsupported income | Seasonal contracts continue despite a termination notice | Preserve scope and apply explicit amendments before recurrence | 1–2 |
| Applying only event-linked messages | User-level salary date changes have no effect | Retrieve relevant user/request evidence even when event link is blank | 2 |
| Choosing the largest number in a document | Gross earnings are substituted for net cash pay | Interpret amount roles and corroborate with the linked event; inspect the supplied payslip example | 2 |
| Treating a missing amount as zero | The 16 blank-amount rows disappear from cash flow | Require extraction or emit an explicit unresolved-evidence diagnostic; block final export | 2 |
| Following instructions embedded in evidence | A message changes reserve rules, output format, or policy | Extract constrained facts only; independently validate them against immutable rules | 2 |
| Confusing current time with request time | Older evaluation requests use later knowledge or today's rates | Anchor context, rates, and forecast to each request's supplied dates | 1–2 |
| Checking only month-end or final balance | The plan dips below reserve before a salary arrives | Replay cash checkpoints and every plan payment in order | 1, 3 |
| Replacing offer day intervals with months | Supplied 28/30/31-day schedules drift | Generate exact offsets from `first_payment_date` and `payment_frequency_days` | 3 |
| Dropping installments beyond the forecast | An apparently cheap plan omits later obligations | Require complete schedule safety and deadline compliance; reject unsupported horizons | 3 |
| Letting adjustments inflate baseline fields | Safe-to-pay or earliest date changes when a subscription is stopped | Preserve baseline and adjusted scenarios separately | 3 |
| Checking partial payments independently | Both payments look safe alone but combined spending breaches reserve | Replay the exact two-payment schedule cumulatively | 3 |
| Selecting the cheapest unsafe or unacceptable offer | Installments selected despite the user's method restriction | Filter for preference, deadline, and safety before ranking | 3 |
| Overfitting the solved examples | Request-ID branches or exact copied sample outputs | Evaluate the same general engine on samples; prohibit labels as prediction inputs | 4 |
| Reporting made-up or unrelated usage | A cached or failed run is described as a measured fresh run | Bind model-call usage, cache reuse, run ID, and output hash; include failed/retried calls when charged | 2, 4 |
| Packaging a non-runnable development checkout | ZIP needs absolute local paths, excludes prompts, or includes secrets | Extract the ZIP to a clean temporary directory and run documented commands | 4 |

## Dataset-Specific Findings

- Samples span all four affordability statuses and include partial payment and combined spending changes.
- `request_06`, `request_11`, and `request_21` show `affordable_with_plan` with `full_payment` and spending changes. A method/status mapping must allow these cases; baseline full-payment dates can remain later than the selected adjusted payment.
- `request_12` has an installment recommendation even though full payment is financially possible on the baseline date. Payment preferences and capacity are distinct.
- All 790 supplied offers satisfy `payment_amount × number_of_payments = total_payable_amount` under decimal arithmetic. Do not add a rounding-repair rule or charge the financing fee twice.
- Sample and evaluation request IDs are disjoint. Neither set should be merged into final predictions.
- Representative messages include English and Indonesian. Keyword matching for English alone is insufficient.

## Performance and Scope Traps

The current dataset does not justify a vector database, web service, model-training pipeline, or separate planner agents in the submitted solution. Index supplied identifiers and extract relevant evidence once. If exact spending-change enumeration becomes large, measure it and improve candidate derivation without silently limiting search in a way that loses required safe plans.

## Verification Strategy

Start focused financial checks with the first engine implementation. Cover non-finite numbers, duplicate versus genuine linked cash movements, missing amounts, salary date changes, reserve dips, partial cumulative safety, exact offer dates, preference exclusions, and unchanged baseline capacity after adjustments. Keep these checks tied to real failure modes rather than mirroring every helper function.

## Sources

Primary local sources: `problem_statement.md`, `AGENTS.md`, `sample_requests.csv`, event and payment-option scans, representative `messages.csv` rows, and two inspected PNGs. Prevention strategies are design recommendations, not a claim that these bugs already exist.
