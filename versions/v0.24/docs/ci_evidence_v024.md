# SI v0.24 — Reproducible GitHub CI, table-language experiments and performance evidence

## Baseline
Reviewed draft SI v0.23 PR #19 at `4173cd03719f596064542c2309dbbeaaeec3f429` (unmerged). Its specialized final CI [run 39245898170](https://github.com/shiyamprimetrade-sketch/SI/actions/runs/39245898170) passed all Python 3.11, 3.12, 3.13 jobs with Node.js 22. v0.23 contained 376 unittest methods per Python version, and a separate executable typed table grammar. New SI project score at start of v0.24: 5450/1000000; historical archive: 996667/1000000.

## Implemented in v0.24
- Actual AxiomFlow `filter t where column OP expression` source syntax, where `OP` is one of `== != < <= > >=`, with static schema/type checks.
- Actual `derive t new_column = expression` syntax, with type inference and a 16-column cap.
- Pure typed `fn name(args) -> type = expression` declarations before table input. Uses the existing AxiomFlow scalar/function expression parser, static type checker, and pure row-local evaluator.
- Previous v0.23 select, sort, augment, sum and emit statements retained. Source length, line count, input rows and dataset size remain bounded.
- CLI example `examples/filtered_table.af`, package archive includes the example and separately authored JavaScript reference evaluator.
- Twelve new Python unittest methods across two files: 250 seeded Decimal-calculated filter/derive cases and 200 seeded independent Node.js BigInt fixed-point table comparisons, plus negative source/type/schema/unsupported-expression tests.
- Lesson 20, precise grammar/semantics note, research notebook and clearly labeled output-equivalent (but non-cost-equivalent) Python/Node benchmark.

## Actual completed GitHub CI on implementation commit
[GitHub Actions run 39246868940](https://github.com/shiyamprimetrade-sketch/SI/actions/runs/39246868940) tested code commit `b5a72a18e26df9c13d19ba2f5d734ef61ebd280d`.

| Python | GitHub job ID | Unit tests | Result |
|---|---:|---:|---|
| 3.11 + Node 22 | 118040803145 | 388/388 | SUCCESS |
| 3.12 + Node 22 | 118040803271 | 388/388 | SUCCESS |
| 3.13 + Node 22 | 118040802956 | 388/388 | SUCCESS |

**1,164 passing test-method executions**, 12 additional methods per Python version over v0.23; zero unittest failures and zero GitHub warning annotations in inspected job logs. Existing legacy lexical obligation digest `9997585eb832c9a59660a7ff3873c1e53a087a975b17a79198512aa36a30bd4d` reproduced. The new table CLI, source packaging, previous typed/local SI CLIs and benchmark steps completed as part of the successful workflow.

## Performance — NOT a fair language superiority benchmark
`python benchmarks/table_workload.py` verifies bit/string-equivalent outputs on 100 seeded datasets of 15 rows each, then times a Python in-process precompiled AxiomFlow table engine against a custom Node BigInt fixed-point evaluator **including Node subprocess startup**. Median nanoseconds per dataset (three repeats):

| Python runner | Python precompiled AxiomFlow | Node subprocess-included fixed-point reference |
|---|---:|---:|
| 3.11 | 390,688.22 | 321,336.60 |
| 3.12 | 295,333.31 | 351,985.07 |
| 3.13 | 324,288.83 | 343,411.34 |

These are different implementation paths and the runner timing varies. Node implements only a particular filter/uplift cents operation and does not parse/check the AxiomFlow language; Python executes typed AxiomFlow statements. **No conclusion of general Python/JavaScript speed superiority, let alone C/C++/Java superiority, is supported.**

## Limits and future research
The table DSL now reuses scalar/function grammar components, but it is not yet a single unified general-purpose language grammar or an independently compiled cross-runtime table engine. No real browser automation, secure full production deployment, general package registry, formal all-input correctness proof or defended doctoral thesis is demonstrated.

No numerical production counterexample or performance superiority was discovered. The new SI project score and 100000 milestone status must be based on independently verified distinct software deliverables, not repeated tests.
