# SI v0.21 — New self-assessed score and 100k gates

| Score ledger | Points |
|---|---:|
| Historical archive (unchanged) | **996667 / 1000000** |
| New SI before v0.21 | 3300 / 1000000 |
| v0.21 nonduplicate self-assessed credit | **+650** |
| **New SI cumulative** | **3950 / 1000000** |
| Remaining to cumulative 100000 evidence gate | **96050** |

## Newly evidenced v0.21 work only

| Criterion | Points | Evidence |
|---|---:|---|
| Strict bounded CSV into typed AxiomFlow feature and deterministic Decimal OLS train/test integration | 250 | `axiomflow/data.py`, `data/landed_cost.csv` |
| 13 new tests, 400 seeded independent feature comparisons, negative validation and CLI checks | 150 | `tests/test_data_interop.py`, `tests/test_package_source.py` |
| Reproducible source-only ZIP with fixed metadata and SHA-256 manifest | 100 | `tools/package_source.py`, two-build equality test |
| Transparent matching-output microbenchmark with explicit overhead and caveat | 75 | `benchmarks/compare_features.py` and real GitHub CI |
| New lesson 17, research notebook and gate-status/installation instructions | 75 | `courses/lesson17_data_ml.md`, `docs/research_v021.md`, README |
| **Total** | **650** | [CI run 39242469581](https://github.com/shiyamprimetrade-sketch/SI/actions/runs/39242469581) |

**Verified CI:** 348/348 tests on each Python 3.11, 3.12, 3.13 + Node.js 22, **1,044 passing unittest executions**, no failures/warnings in reviewed logs; the model CLI and source archive build succeeded.

**No points** for inherited SI tests, previous API/frontend/typed functions, public deployment, standalone ML framework, general-purpose language performance wins, formal proof, global package manager, complete thesis or new system terminal. This self-assessed progress record is not a measurement of AI intelligence or altered model weights.

**Negative result:** AxiomFlow's direct feature pathway was slower than direct Python Decimal in the logged microbenchmark, and the two paths are not cost-equivalent. The result is explicitly recorded rather than concealed. The synthetic OLS zero-error result is not evidence of ML generalization.
