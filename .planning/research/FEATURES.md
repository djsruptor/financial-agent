# Feature Research

**Domain:** Buy or Wait? challenge submission
**Researched:** 2026-09-13
**Confidence:** HIGH for required features; MEDIUM for implementation effort

## Feature Landscape

The challenge contract defines scope more directly than a competitor survey. All specified capabilities belong in v1; feature prioritization below determines build order, not whether required behavior may be omitted.

| Required capability | Why it matters | Complexity | Observed evidence |
|---|---|---|---|
| Cash-state reconstruction | Current balance alone is insufficient | High | Linked purchases/refunds, pending debits, scheduled salary, non-cash valuations |
| Supported recurrence and essential reserves | Future commitments determine safe capacity | High | Repeated rent, groceries, transport, salary, subscriptions, and debt payments |
| Multilingual financial amendments | Structured amounts and dates can be superseded | High | English and Indonesian employer/provider messages, including user-level updates without an event link |
| Image interpretation | Some required amounts are absent from CSV | Medium | 16 blank event amounts and 16 PNGs; inspected payslip and utility receipt contain distinct financial fields |
| Dated currency conversion | Users and events may use different currencies | Medium | 134 supplied rates; profiles cover five home currencies |
| 90-day capacity and plan verification | Prevent recommendations that break reserve requirements | High | Explicit minimum balance and deadline rules |
| Full, partial, installment, wait, fallback decisions | Personalized payment options are the required output | High | 790 offers, accepted-method preferences, 25 examples spanning all four statuses |
| Permitted expense adjustments | Some safe plans require flexible spending changes | High | `stoppable`, `reducible`, and `reducible_or_stoppable` events; samples include combined changes |
| Deterministic ranking and explanations | Safety alone does not determine the correct winner | Medium | Six ordered ranking rules and evidence-based explanations |
| Evaluation and submission artifacts | Predictions must be runnable, measurable, and complete | Medium | 250 evaluation requests, usage report, ZIP, transcript |

## Useful Improvements Within v1

- Retain a compact provenance trail so wrong sample predictions can be traced to evidence, forecast, or ranking.
- Reuse extracted evidence with content-based invalidation to avoid repeated model calls.
- Report sample mismatches by output field and financial invariant; do not treat a plausible explanation as a correct decision.

## Anti-Features and Deferrals

| Feature | Reason to defer or exclude |
|---|---|
| Chat UI, accounts, hosting | No requirement beyond a terminal solution |
| Live financial integrations | Supplied records and rates are the authorized inputs |
| Asset-price predictions | Investment questions are affordability questions |
| Multiple models voting on every prediction | Added calls do not replace deterministic safety checks |
| Fine-tuning or fitting sample labels | Twenty-five examples are a public evaluation reference, not permission to hardcode outcomes |

## Feature Dependencies

Input validation → cash reconstruction → baseline forecast → safe capacity → candidate plans → verified selection → output.

Messages/images amend facts before reconstruction. Spending changes create a separate scenario; they must never alter baseline `amount_safe_to_pay` or the baseline full-payment date. Evaluation must exercise the same engine that generates final predictions.

## MVP Definition

Build four executable increments: structured-data decisions; decisions informed by all supplied evidence; complete alternative-payment and adjustment selection; validated full-dataset submission. Early increments must explicitly report unsupported evidence or methods rather than represent incomplete analysis as final advice.

No additional v2 features are committed. Optional OCR, concurrency, and richer diagnostics may be added only if measured needs justify them.

## Sources

Local primary sources: `problem_statement.md`, `README.md`, `AGENTS.md`, all CSV schemas, all 25 sample output summaries, representative messages, `image_01.png`, and `image_09.png`. No evaluation labels were inferred or generated during this research.
