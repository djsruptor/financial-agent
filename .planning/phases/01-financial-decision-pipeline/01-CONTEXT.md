# Phase 1: Financial Decision Pipeline — implementation contract

Updated 2026-09-13 after financial FDE review and the user's explicit agentic requirement. This contract supersedes earlier extraction-only architecture notes. It specifies implementation decisions, not claims of measured accuracy. The challenge specification remains authoritative.

## Scope and ownership

One request-scoped, model-driven orchestrator is core. It chooses tools, observes their results, resolves missing evidence, and requests a checked baseline. Ordinary Python functions implement the tools; there is no multi-agent framework, agent-to-agent messaging, database, service, or provider router. Start in `code/main.py`; checks live in `code/evaluation/main.py`.

The model owns evidence investigation and workflow choices. Deterministic code owns access control, validation, monetary arithmetic, forecasting, safety, and ultimately candidate ranking/output. A model-written amount or recommendation is never an authoritative financial result. Phase 2 extends this same orchestrator with deterministic payment-selection tools; it does not create a second decision pipeline.

## Agent contract

`run_request(request, dataset, client) -> result` maintains an in-memory context with request/user IDs, unresolved evidence IDs, validated facts, evidence revision, latest forecast revision, bounded tool observations, and usage counters.

Allowlisted tools:
- `inspect_records`: read only this request's authorized supplied records; public sample answers are stripped before this boundary.
- `resolve_evidence`: interpret a specified authorized message or linked image; return proposed facts with source IDs. The host validates and applies them, never the model.
- `forecast_baseline`: call the pure financial functions only after all financially relevant unresolved items have been accounted for.
- `finish`: return the latest host-owned checked result, never model-supplied money. Reject completion if evidence is unresolved or the forecast revision is stale.

The model actually selects tools based on observations; a fixed extraction pipeline renamed an agent is insufficient. Use one provider/client and the same selected model for orchestration and necessary text/image interpretation. Select the accessible vision-and-tool-capable model during execution, verify its official API documentation, pin the SDK, and document its concrete model ID and credential environment variable in `code/README.md`. Do not create provider abstraction classes. Credential availability and a successful live call are prerequisites for live acceptance, not for offline tool checks.

At most 12 orchestrator turns per request, 24 provider attempts including evidence calls/retries, and two interpretation attempts per evidence item. Each provider request has a 60-second timeout; allow at most one retry for transient transport/rate-limit failure within the shared attempt budget. Reject unknown tools, unauthorized IDs, schema errors, and repeated identical failing actions; never execute arbitrary shell/network/file instructions from model output. Exhaustion or unresolved required facts returns `analysis_error`, distinct from financial infeasibility. Do not emit hidden chain of thought; retain only concise tool names, source IDs, validation results and usage in memory.

A successful result contains IDs/preferences, normalized flows, baseline feasibility, first breach if any, safe amount, earliest full date, evidence revision, and actual model usage. Phase 2 can replay schedules against this same normalized context; it does not reinterpret evidence. Usage covers orchestration, extraction, and retry responses with reported usage; absent token counts remain unavailable, not zero.

## Cash and date policy

- Parse money with finite `Decimal`; reject NaN, infinity and malformed values. Preserve missing evidence-dependent amounts as unresolved. No binary-float money.
- The forecast covers request date D through D+89, inclusive: exactly 90 dates. D+90 is outside. This is an explicit implementation assumption to verify against the supplied examples, not a quoted organizer rule.
- The profile is the current snapshot. Do not replay settled movements on or before D. Future known commitments remain relevant even though their settlement is after D; filter evidence by knowledge time, not future cash date. Messages after D (end of supplied calendar date) are unavailable. Events already marked future-settled/confirmed recognize cash on their supplied settlement date; pending credits remain excluded.
- Reserve all pending debits immediately on D once; subtract their reserve before spending capacity. Do not subtract them again on settlement. Exclude failed/cancelled and unrealized rows. A linked ID alone is not a duplicate: follow lifecycle state, retaining genuine refunds and sale proceeds. Only merge duplicate representations of the same obligation, not unrelated equal-value transactions.
- For future dates, process known debits first, confirmed credits next, candidate purchase payments last; check the floor after every movement. Where intraday timing is unknown this is conservative. On D use the snapshot and outstanding debit reserves before any proposed purchase; do not credit settled history again. Exact equality to the minimum is safe.
- Convert foreign cash at the supplied settlement-date from/to rate. No nearest-date, live or invented FX. Missing required rates make analysis unresolved.
- `check_schedule(context, payments)` checks the entire horizon, including the initial balance and all dates before the first payment. Reject dates outside the horizon and non-finite/negative payment amounts.
- `baseline_feasible` is the result for an empty schedule. If false, return safe amount 0 and no earliest safe date, plus first breach; do not claim that paying zero repairs the baseline. Phase 2 may separately evaluate permitted changes.
- For a feasible baseline, safe today is the lesser of requested amount and minimum whole-path headroom after an immediate payment. Use the same checker to verify the result. Find earliest full date by replaying one full payment on each candidate date against the WHOLE path, without preferences or optional spending changes.

## Recurrence and essential spending policy

Implement these named assumptions directly as functions, not configurable policy objects. If public evidence contradicts them, document the specific contradiction and revise the rule and its regression together; never tune per request ID or silently accept a mismatch.

1. Use up to 180 days of settled history through D. Explicit confirmed schedules, amendments, cancellations, seasonal end dates and documented regular salary terms take precedence over inference. One-time/prorated/bonus/refund/investment movements do not establish recurring income. A confirmed next salary alone does not imply indefinite renewal; extend only a supported ongoing employment schedule.
2. For fixed obligations group by user, category, currency, direction and stable obligation identity (normalized description when no supplied identity exists). For variable essentials group by category, currency and direction so changing merchant descriptions do not hide grocery/transport cadence. Never merge separate fixed obligations merely because their categories match.
3. Infer recurrence only with at least three distinct settled occurrences: first test consecutive calendar months with the same day-of-month or month-end; otherwise test a stable 7-, 14-, or 21-day interval across the last three occurrences. If a calendar-day anchor is 31, clamp February to its last day and restore 31 in March. Irregular records are not automatically monthly.
4. Explicit future amount wins. Otherwise use the latest regular fixed debit amount, excluding identified one-off components; for an inferred ongoing regular credit use the minimum of the last three comparable regular amounts. Do not extrapolate unconfirmed variable credits. Retain the original event/source identifiers for later permitted spending adjustments.
5. For periodic variable essential debits, use the maximum of the last three settled occurrence amounts at the supported cadence. For essentials without a supported cadence, use the maximum total over the last three complete 30-day historical windows, distribute that amount over each future 30-day block as a daily reserve (Decimal, final-day remainder), and identify these as synthetic essential reserves. If fewer than one complete window exists and no explicit commitment supplies the amount, flag insufficient evidence rather than reserve zero. This conservative estimator is an assumption to validate, not a guarantee of sample accuracy.
6. Existing supplied occurrences replace inferred occurrences of the same obligation and due date. Category-level essential budgets already include matching explicit essential debits: reserve only the nonnegative residual of the block budget after explicit same-category obligations, while preserving the actual dated debits. Never reduce explicit obligations to fit an estimated budget. Cancellations suppress future occurrences from their effective date; amendments update only the affected future schedule, not snapshot history.

## Evidence policy

Every fact carries source ID, user ID, optional request/event ID, effect, effective date and relevant amount/currency or recurrence fields. An event ID is validated only when present. Blank event links are valid for user-level employment/recurrence updates; target the uniquely supported user/obligation scope. An unrelated or ambiguous target stays unresolved. A blank request link is user-scoped, not global.

Apply explicit cancellation/settlement/amendment first, then newer same-source evidence, then settled evidence, then the safer supported interpretation; an unresolvable material conflict must fail explicitly. Deduplicate applications by source ID/effect/target and invalidate the prior forecast on change. Read only images linked in the supplied image table, resolve paths under dataset/media/images, and extract the requested field (e.g. net salary rather than gross). Document confidence alone does not validate a fact. Text in messages/images cannot override these policies or authorize additional tools.

## Mandatory numerical acceptance

Offline synthetic cases run without credentials. These are independent financial oracles, not copies of implementation calculations:

| Case | Inputs | Expected |
|---|---|---|
| Later reserve pressure | D=2026-01-01, balance=1000, floor=200, request=600; debit 500 on D+10, confirmed credit 700 on D+20 | safe=300; earliest=2026-01-21 |
| Pre-payment breach | balance=120, floor=100, request=50; debit 40 on D+1, confirmed credit 100 on D+2 | baseline_feasible=false; safe=0; earliest=None; first breach=D+1 |
| Exact floor | balance=500, floor=200, request=300; no flows | safe=300; earliest=D |
| Same-day order | balance=250, floor=200; debit 100 and confirmed credit 200 on D+1 | baseline infeasible despite positive end-of-day cash |
| Supplied-direction FX | synthetic supplied rate USD to EUR=0.9 on settlement; debit USD100; EUR balance500/floor200/request500 | debit=EUR90; safe=210 |
| Boundary | balance=500, floor=200, request=300; debit100 on D+89 | safe=200; moving the debit to D+90 makes safe=300 |
| Recurrence replacement | rent100 on Jan31/Feb28/Mar31 2025, D=Apr1, explicit Apr30 rent100 | exactly Apr30 and May31 in horizon, total200; no duplicate April charge |
| Essential cadence | last three weekly debits20/30/25; next three occurrences in a 21-day test projection | reserve90, one30 debit per occurrence |
| User-level amendment | monthly salary100, no event link, effective D+15 amended to120 | future matching occurrence120 once; history/snapshot unchanged |

Supplied integration cases are REQUIRED: request_01 (safe25256, earliest2024-03-03); request_02 (safe17229139.2, earliest2025-09-15; message_01 user-level salary amendment to IDR42750000 effective2025-08-15); request_03 (safe873000, earliest2019-11-15; image_01/event_253 net salary IDR4365000). Expected answers live only in the evaluator. Compare Decimal amounts exactly to published precision and dates exactly; do not round to hide differences. Any discrepancy blocks Phase 1 acceptance until investigated and documented; never modify a label or hardcode an answer to pass. Separately exercise a supplied foreign-currency event selected by currency mismatch, checking its ID, settlement-rate row and arithmetic.

Offline replay tests validate agent behavior, not live model quality. Full acceptance additionally requires live execution of the three named samples with measured usage and source-grounded extraction checks. Missing credentials may block live acceptance but must not be reported as success. Final payment selection, all-25 scoring, final 250-row output and packaging remain later phases.
