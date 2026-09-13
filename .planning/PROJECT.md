# Buy or Wait?

## What This Is

A terminal agentic solution for the supplied HackerRank challenge. A bounded model-driven orchestrator chooses evidence and financial tools for each request. It reads `dataset/`, decides how each requested expense can safely be paid, and produces `output.csv`, `code.zip`, and the required transcript.

## Core Value

Complete each recommended payment plan by its deadline while protecting essential spending and the user's minimum balance throughout the 90-day forecast.

## Requirements

### Validated

None. Implementation files are still empty.

### Active

- [ ] Read the supplied profiles, transactions, rates, offers, messages, and images.
- [ ] Reconstruct cash and commitments without inventing facts or double-counting settled history.
- [ ] Calculate safe capacity and select the best permitted payment plan under the challenge rules.
- [ ] Evaluate the public samples and produce the complete submission with actual model usage/cost reporting.

The checkable contract is in `REQUIREMENTS.md`; detailed financial rules remain in `problem_statement.md` and the original `AGENTS.md`.

### Out of Scope

Messaging interfaces, translation/localization features, language settings, a generalized document platform, persistent extraction caches, provenance databases, run-ledger infrastructure, dashboards, live financial feeds, multi-agent frameworks, provider routing, and model training. Do not add them as optional future scaffolding.

## Context

The supplied data has 250 evaluation requests, 25 solved examples, 275 profiles, 25,342 financial events, 790 offers, 215 messages, and 16 linked images. Sixteen event amounts are blank and require reading their linked images. All dates and exchange rates come from the supplied files.

The program must interpret relevant supplied message/image content to satisfy the challenge; this is input processing, not a messaging or translation product. No extra language feature or separate language-support workstream is planned.

`code/main.py`, `code/evaluation/main.py`, and `code/evaluation/usage_report.md` are empty starter files. Final predictions belong at root-level `output.csv`; `dataset/output.csv` is the unchanged template.

## Implementation Constraints

- Use ordinary Python functions, `csv`, `Decimal`, and date utilities. Start in the existing entry points; split a helper file only when the actual implementation needs it.
- Use one model-driven orchestrator with allowlisted evidence and financial tools. The model chooses actions from observations; host code validates facts, enforces budgets and owns all financial results. Use one provider/client, ordinary functions and in-memory request state; no orchestration framework or separate service.
- Keep monetary calculations, schedule generation, ranking, and validation deterministic. Preserve input validation, prompt-injection boundaries, and checks that prevent incorrect financial decisions or output loss.
- Record model-call counts and token totals when calls occur; write the required cost report for the final dataset run. Ordinary counters suffice; no persistent usage ledger or output hashing subsystem.
- Keep supplied data immutable; do not use hidden labels or hardcoded predictions. Secrets come from environment variables and stay out of the package and transcript.
- Use one sample-evaluation script and focused regression checks for money and schedule rules. No generic testing platform.
- Automatic sequential execution remains enabled. Keep plan checks and verification; skip routine research, UI/AI design contracts, and pattern mapping. Read documentation only to resolve a concrete implementation question.

## Key Decisions

| Decision | Rationale | Status |
|---|---|---|
| Lean agentic orchestrator | User explicitly requires agentic structure as core; financial authority stays deterministic | Adopted |
| Challenge requirements and requested agentic workflow | User explicitly requested removal of all implementation excess | Adopted |
| Three phases: decisions, payment selection, submission | Removes the standalone evidence subsystem phase | Phase 1 planned |
| No language-specific feature requirement | Process the actual supplied evidence without expanding product scope | Adopted |
| No mandatory cache, provenance store, or run ledger | Not required to produce correct predictions and the usage report | Adopted |
| Python standard library plus one necessary model client | Reuses starter files and keeps the solution small | Pending implementation |

## Open Questions

Phase 1 date, recurrence, evidence, orchestration and numerical acceptance policies are specified in `.planning/phases/01-financial-decision-pipeline/01-CONTEXT.md`. Validate these explicit assumptions against supplied evidence; do not silently tune rules to labels. Select and document one accessible vision/tool-capable model during execution; live acceptance requires credentials and actual measured calls. Installment-duration interpretation remains Phase 2 work.

The repository's September 13, 2026 18:00 IST deadline has passed; submission availability is unverified. Development continues.

## Evolution

After each phase, record verified requirements and necessary decisions. Add scope only when the user requests it or the challenge contract requires it.

---
*Updated: 2026-09-13 after the user's lean-scope review.*
