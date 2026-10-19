# SI v0.17 — User-authorized, self-assessed incremental project score

| Ledger | Score |
|---|---:|
| Historical archived simulation | **996667 / 1000000** unchanged |
| New SI project before v0.17 | 950 / 1000000 |
| v0.17 incremental award | **+450** |
| **New SI project cumulative** | **1400 / 1000000** |

This is a subjective, provisional project progress index, not a measure of intelligence or a superiority ranking over existing programming languages.

## v0.17 award
| Criterion — new work only | Points | Evidence |
|---|---:|---|
| First working AxiomFlow parser/interpreter, typed money/scalar rules | 200 | `axiomflow/language.py`, evaluated example |
| New AxiomFlow tests and 500-case seeded independent Decimal reference check | 100 | `tests/test_axiomflow.py`; GitHub matrix all green |
| Usable basic file/one-shot/interactive terminal prototype | 50 | `axiomflow/__main__.py`, CLI smoke test |
| Dated 10-day sprint plus thesis-style research outline, limitations | 50 | `docs/ten_day_sprint.md`, `docs/research_v017.md`, `docs/thesis_outline_v017.md` |
| New tutorial/course lesson 13 | 25 | `courses/lesson13_axiomflow_alpha.md` |
| Transparent exploratory benchmark with observed negative outcome | 25 | `benchmarks/compare_decimal.py` and GitHub CI log |
| **Total** | **450** | No points for inherited SI regression suite or unimplemented functionality |

## Verified GitHub CI
[Run 39236516788](https://github.com/shiyamprimetrade-sketch/SI/actions/runs/39236516788), code commit `5b17c9d93bb53751218bc40412683475dddd2a66`:

- Python 3.11 + Node 22: 287/287 tests passed, job 118006785330.
- Python 3.12 + Node 22: 287/287 tests passed, job 118006784850.
- Python 3.13 + Node 22: 287/287 tests passed, job 118006785051.
- **861 passing test executions**, zero test failures or workflow warning annotations; inherited lexical digest reproduced.

## Benchmark negative result
The exploratory benchmark intentionally includes source re-parsing in the AxiomFlow path but not in the direct Python Decimal path. Observed median nanoseconds/call from CI:
| Python | AxiomFlow | Direct Decimal |
|---|---:|---:|
| 3.11 | 14341.11 | 935.19 |
| 3.12 | 19471.43 | 1295.71 |
| 3.13 | 24935.41 | 1914.89 |

These values are **not apples-to-apples**; do not compute or claim a statistically valid language speed ranking. No performance-superiority points have been awarded.

No credit for unimplemented C/C++/Java superiority, frontend, API/backend, ML framework, dependency compiler, full security sandbox, new standalone terminal or completed PhD.
