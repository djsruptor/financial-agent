# Scope Notes

**Updated:** 2026-09-13 after scope reduction

Only `problem_statement.md`, the original repository instructions, and the user's constraints define scope.

Required: read supplied financial evidence; reconstruct commitments; verify 90-day affordability; choose among the specified payment methods and allowed expense changes; produce evaluated predictions, usage report, runnable ZIP, and transcript.

Reading `messages.csv` is input processing. Do not add messaging, translation, localization, or language settings. Reading the linked PNGs is necessary because 16 supplied event amounts are blank; it does not justify a generalized document-processing product.

Remove optional differentiators from the implementation backlog: dashboards, extraction caches, provenance stores, provider routing, concurrency, and model training. Reconsider only if the user requests them or a measured issue prevents completing the challenge.
