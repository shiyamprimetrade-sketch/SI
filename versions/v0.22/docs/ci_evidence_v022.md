# SI v0.22 — Final CI, failed first experiment and measured implementation change

## Baseline
Draft v0.21 PR #17 head `5d818b357a36310a2360dadcfcf7071e199fb097`: previously verified Python 3.11/3.12/3.13 with Node.js 22, 348 tests per Python version. Main `573cf6ea850fe72698ea2a45c6bd854b329c7357` not modified.

## Failed initial v0.22 CI experiment
Source commit `a3946d5070f4d3490eec89551f4daa6a7f46e9d9` triggered [specialized GitHub Actions run 39244247653](https://github.com/shiyamprimetrade-sketch/SI/actions/runs/39244247653), which **FAILED** in all three matrix jobs **after all 365 tests passed**. The final benchmark step, invoked as a standalone script, could not resolve `axiomflow` and raised `ModuleNotFoundError: No module named 'axiomflow'`. This is a real packaging/import-path integration failure, not a numerical conformance failure. The test step alone passing is not counted as overall CI success.

Corrective commit `03a02f9ef5a3eff8bf2084a0128ecbe9382f5877` adds the local project path to `benchmarks/compare_precompiled.py` before imports.

## Verified passing complete retest
[GitHub Actions run 39244404827](https://github.com/shiyamprimetrade-sketch/SI/actions/runs/39244404827):

| Python | GitHub job | Passed unit methods | Job |
|---|---:|---:|---|
| 3.11 + Node.js 22 | `118032706408` | 365/365 | SUCCESS |
| 3.12 + Node.js 22 | `118032706014` | 365/365 | SUCCESS |
| 3.13 + Node.js 22 | `118032705763` | 365/365 | SUCCESS |

**1,095 passing test-method executions** across the matrix, **17 newly added methods/version** above v0.21. Zero unittest failures and zero GitHub warning annotations in inspected logs. The inherited bounded-lexer corpus SHA256 `9997585eb832c9a59660a7ff3873c1e53a087a975b17a79198512aa36a30bd4d` reproduced. Data/ML CLI, source-only ZIP packaging, pinned project CLI, legacy SI obligations and the completed exploratory benchmark succeeded in this workflow.

## Benchmarks: three pathways (200 iterations × 3 samples; median ns per call)
| Python | Parse/typecheck+execute | Cached AST execute | Direct Python Decimal |
|---|---:|---:|---:|
| 3.11 | 57046.08 | 7136.42 | 1921.48 |
| 3.12 | 60179.81 | 8519.00 | 2377.99 |
| 3.13 | 68045.09 | 8987.76 | 2765.68 |

The cached-AST path was approximately **7–8 times faster than reparsing within AxiomFlow** for this limited workload on these runners. **Direct Python Decimal remained faster in every job**; it bypasses AxiomFlow parsing/typechecking and AST execution, so the baseline is not cost-equivalent. Runner variation, tiny sample counts and data-dependent behavior preclude general performance dominance claims. No C/C++/Java competitive performance measurements were made.

## Newly exercised engineering properties
- Immutable `Record`/`Table` Python host representation with aligned schema/types and bounded Decimal records, stable sorting, projection, aggregation and deterministic typed landed-cost augmentation. Not original language table syntax.
- A parsed and statically checked function is held at module scope; each evaluation uses fresh monetary and scalar `Value` inputs, without reparsing. The old v0.21 full evaluation remains as a parity oracle.
- New tests cover 400 seeded comparisons across compiled AxiomFlow, old AxiomFlow and independent Python Decimal.
- Separate Node.js BigInt cents arithmetic compared on 250 seeded cases, ties-even examples and rejection samples. This is not an independent JS AxiomFlow table implementation.
- Reproducible source ZIP includes the new table module; deterministic archive test paths updated for v0.22.

## Scientific limitations
Finite tests are not formal type soundness or cross-language performance proof. Table operations are Python APIs, not grammar constructs executable entirely in AxiomFlow. No secure sandbox, production terminal, public app deployment, complete original language, ML ecosystem, external benchmark study or complete defended thesis. No universal superiority claim. The self-assessed SI project score is not model retraining or an intelligence measurement.
