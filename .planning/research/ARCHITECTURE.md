# Implementation Shape

**Updated:** 2026-09-13 after scope reduction

```text
supplied CSVs/images → necessary fact extraction → cash forecast
                    → permitted payment candidates → safety/ranking → output.csv
```

Start with ordinary functions in `code/main.py`. Use the existing `code/evaluation/main.py` to call the same engine for the public examples. Add one helper file only if actual code becomes hard to follow; do not scaffold modules or classes for future extensibility.

Financial calculations and schedule checks stay deterministic. An extraction result is ordinary validated data; source IDs may be retained in memory to resolve the provided links, without building a provenance store. Secrets stay in environment variables. Invalid or missing evidence fails explicitly rather than becoming zero or an invented financial fact.

Accumulate the model's returned usage in simple counters during the run. Generate the required usage report from those totals. No cache manager, persistent run ledger, output hashing, service boundary, or reporting UI is planned.

Build order: (1) input/evidence and financial capacity, (2) all payment decisions and output, (3) evaluation and packaging. Preserve baseline capacity when trying spending changes and replay complete cumulative schedules before selection.
