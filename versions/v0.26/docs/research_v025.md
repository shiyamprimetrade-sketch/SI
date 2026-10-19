# SI doctoral research notebook v0.25 — Unified dispatch and restricted independent source semantics

## Baseline
Review PR #20 v0.24 and its final actual GitHub Actions run. It implements statically checked typed table relational operators, scalar function calls in derived expressions, and a Node independent data comparator on a narrower fixed operation. The central missing piece is a documented common entrypoint and an independent subset interpreter of the actual **source text**.

## New hypothesis and falsifiable checks
H1: Source classification can provide one strict CLI for table programs and existing typed scalar/function programs without ambiguous silent fallthrough, even if the grammars have not yet been merged. A table declaration selects the existing compiled table plan; unsupported cross-mode operations reject before output.

H2: A separately written Node.js evaluator can parse and execute a restricted AxiomFlow relational source subset directly (table, price filter, 1.10-derived USD, sort, sum, select, emit) while matching Python's statically checked table interpreter on 200 fixed-seed generated source programs and data tables. BigInt cents prevent float rounding discrepancies for this subset.

H3: Full-process Python vs Node benchmark fairness improves when **both processes** accept the same batch of source programs and data, produce the same structured JSON and include interpreter launch, source parsing and JSON handling in each sample. Even then their implementations, optimization effort, startup behavior, hardware scheduling and runtime semantics differ; performance findings support only this precise workload.

## Method and limits
- `axiomflow/unified.py`: bounded source classifier; scalar calls existing `parse_script`, `static_check`, then existing scalar evaluator. Table calls existing `compile_table` and immutable table evaluator. CSV is required for table mode and forbidden for scalar mode. Foreign syntax and cross-mode mixing reject.
- `js/relational_runtime.js`: one independent source interpreter on an intentionally limited grammar and 500-row bounds; not a complete AxiomFlow implementation.
- `tests/test_unified_runtime.py`: 14 methods, 200 reproducibly seeded differential examples and errors; previous conformance suites retained.
- `benchmarks/unified_relational.py`: forty deterministic 18-row programs, Python and Node subprocess output equality before timing, five repeated wall-clock process launches.
- Deterministic source ZIP updated and run under real CI.

## Failure and negative findings discipline
Record all failing initial actions and fixes, including packager path mismatches. Report performance even when Python/Node timings run counter to hypotheses. No proof of universal programming-language superiority, global static type soundness, secure sandbox, complete independent runtime, finished PhD dissertation or all-purpose terminal. The user requested a rapid 100k milestone, but **points only accrue from independently verified artifact gates**.
