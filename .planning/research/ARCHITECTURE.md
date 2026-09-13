# Implementation Shape

Updated 2026-09-13: the user explicitly requires agentic orchestration as core. This supersedes the earlier extraction-only pipeline.

One model-driven orchestrator per request selects allowlisted inspect/evidence/forecast/finish tools based on observations. It keeps ordinary in-memory request state. Host code scopes access, validates facts, enforces turn/call budgets, invalidates stale forecasts, and returns only deterministic checked money. A fixed extraction pipeline renamed an agent is insufficient.

Use ordinary Python functions in `code/main.py`, one model SDK and the existing evaluator. No multi-agent framework, separate services, persistent caches, provenance database or ledger. Model usage counters include orchestration, evidence and reported retry usage.

Phase 1's concrete policies and acceptance cases live in `../phases/01-financial-decision-pipeline/01-CONTEXT.md`. Phase 2 adds deterministic candidate selection/ranking and output tools to the same loop; Phase 3 measures all samples, runs the dataset and packages the submission. Model output never overrides financial checks.
