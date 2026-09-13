# Project Research Summary

**Project:** Buy or Wait?
**Domain:** Dataset-driven affordability recommendations
**Researched:** 2026-09-13
**Confidence:** MEDIUM overall; HIGH for the supplied requirements and observed dataset structure

## Executive Summary

Build a small Python terminal pipeline around exact monetary arithmetic and deterministic cash-flow replay. The dataset's identifiers provide retrieval; no external financial feeds, database, agent framework, or user interface is needed. Use AI to extract financial facts from multilingual messages and PNGs, then validate and apply those facts before calculating affordability.

The main risk is reconstructing the wrong cash state, not generating a fluent explanation. History must not be counted again on top of the current balance; missing amounts, salary amendments, lifecycle links, and user preferences all affect the result. Develop the engine through complete, runnable slices and require final-batch validation before producing submission artifacts.

## Key Findings

- **Stack:** Existing Python 3.13.3 with standard-library CSV, decimal arithmetic, dates, JSON, and ZIP support. Add one model SDK only when extraction is implemented. See `STACK.md` and its linked primary documentation.
- **Features:** The full challenge contract is v1. Four statuses, five methods, permitted spending changes, exact offer schedules, evidence handling, evaluation, and cost reporting are all required. See `FEATURES.md`.
- **Architecture:** Indexed context → validated evidence → cash reconstruction → baseline forecast → candidate plans → replay/ranking → output and usage artifacts. See `ARCHITECTURE.md`.
- **Pitfalls:** Snapshot double-counting, unsupported recurrence, incorrect image amount roles, silent evidence omissions, preference/capacity conflation, and unreplayed partial plans. See `PITFALLS.md`.

## Implications for Roadmap

| Phase | Delivered user capability | Why this order |
|---|---|---|
| 1. Structured Financial Decisions | Run supported structured-data requests and inspect baseline capacity and full/wait decisions | Establish the financial invariants and a runnable path first |
| 2. Evidence-Aware Decisions | Incorporate relevant messages and images with reproducible extraction | Resolve the source facts before expanding payment search |
| 3. Complete Payment Planning | Select among all allowed methods and permitted spending adjustments | Reuse one verified cash-flow model for every candidate |
| 4. Evaluated Submission | Generate all predictions, measured usage, and a reproducible submission package | Validate the complete engine and artifact provenance together |

Use vertical MVP mode for each phase. Early development outputs are explicitly incomplete; unresolved evidence or unimplemented candidate types are diagnostics, not a final `not_affordable` judgment. Final export requires the complete contract.

## Confidence Assessment

| Area | Confidence | Evidence or remaining work |
|---|---|---|
| Scope and output rules | High | Explicit local specification and 25 solved examples |
| Core runtime | High | Python available; standard-library behavior verified in official docs |
| Evidence integration | Medium | English/Indonesian messages and two images inspected; provider and schema still need implementation validation |
| Financial semantics | Medium | Recurrence, horizon boundaries, and same-day ordering need focused sample-based checks |
| Performance and accuracy | Unmeasured | No runnable solution or full-dataset model run exists yet |

## Gaps to Address

- **Phase 1:** Document forecast day boundaries, as-of filtering, same-day ordering, and recurrence assumptions against samples; do not invent hidden rules.
- **Phase 2:** Select an accessible model/provider, validate multilingual and image extraction, pin the SDK, and confirm usage accounting. No paid calls were made during research.
- **Phase 3:** Define installment duration checks and legal reduction candidate derivation; verify status versus baseline-date edge cases.
- **Phase 4:** Measure per-field sample accuracy and inspect each unresolved mismatch. Do not claim hidden-ground-truth accuracy or fabricate final-run token/cost totals.

## Sources and Research Method

Primary local sources: README, problem statement, AGENTS instructions, CSV schema/count scans, all sample status summaries, representative event lifecycles and messages, and `image_01.png` / `image_09.png`. Primary external references are linked in `STACK.md`: Python CSV/decimal/datetime documentation and provider vision/structured-output documentation.

Research was performed inline with the current model under the approved sequential workflow. Recommendations are derived from the supplied task, not a market survey or a production benchmark.

---
*Research completed: 2026-09-13. Ready for roadmap: yes.*
