# SI Course lesson 20 — Typed relational filtering and derived functions

**Objectives:** understand compilation against a changing table schema, type-checked relational predicates, stable row filtering, immutable record transformations, and independent reference evaluation.

**Lab:** Run `examples/filtered_table.af` with the included CSV. Trace `price_usd >= 120.00 USD`, the pure `uplift` function, sorting, aggregation and projected output. Write invalid USD-vs-scalar predicates and verify early static rejection. Change filter threshold, then predict the output from a separate Decimal calculation. Verify the JS BigInt fixed-point comparator over seeded datasets.

**Performance discipline:** time equivalent outputs, report whether benchmark paths include parsing/Node process startup, and never infer universal superiority from non-matched workloads.

**Assessment:** syntax and typing (3), deterministic data semantics (3), independent conformance (2), benchmark limitations (2). This grade does not grant SI project points without the separate evidence rubric.
