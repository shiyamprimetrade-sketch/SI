# SI v0.25 — Nonduplicative self-assessed project score

| Ledger | Score |
|---|---:|
| Historical simulation archive — unchanged | **996667 / 1000000** |
| New SI engineering project at v0.25 entry | **6250 / 1000000** |
| Evidence-based provisional v0.25 award | **+850** |
| **New SI cumulative score** | **7100 / 1000000** |
| Remaining to conditional 100000-point milestone | **92900** |

## Only new auditable work credited
| Deliverable, distinct from v0.24 | Points | Evidence |
|---|---:|---|
| Strict unified scalar/function/table CLI and compile-time mode checks | 250 | `axiomflow/unified.py`, scalar/table CLI examples and rejection tests |
| Independently written JavaScript source-level relational subset evaluator | 200 | `js/relational_runtime.js`, Node 22 tests |
| Fourteen new tests including 200 deterministic seeded cross-language source-program comparisons | 200 | `tests/test_unified_runtime.py`; [CI 39248411993](https://github.com/shiyamprimetrade-sketch/SI/actions/runs/39248411993) |
| Output-equivalent process-level benchmark: equal JSON workload, five repeats, negative qualifiers | 100 | `tools/table_batch.py`, `benchmarks/unified_relational.py` and runner logs |
| Updated reproducible release archive with expanded runtime/adapters | 50 | `tools/package_source.py` and inherited packaging-integrity tests on new files |
| Versioned lesson 21, source semantics, doctoral research record and failure limitations | 50 | `courses/lesson21_unified_source.md`, `docs/unified_spec.md`, `docs/research_v025.md`, CI audit |
| **Total** | **850** | No re-crediting inherited tests or earlier grammar/features |

## Verification
Python 3.11/3.12/3.13 with Node.js 22 passed **402 test methods per runtime**, **1,206 successful executions**, no failed tests/warnings, real source CLI and package checks. The project score measures **self-assessed software deliverable progress**; it is not an objective intelligence metric or evidence of changes to the assistant's neural weights.

Zero points are awarded for the unimplemented unified type system, full JS runtime, production terminal, full ML framework, security proof, benchmark supremacy, peer-reviewed thesis or 100k target completion. Historical archive remains completely separate.
