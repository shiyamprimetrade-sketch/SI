# SI v0.18 — 100,000-point milestone progress ledger

**Target:** **100,000 / 1,000,000** new SI project self-assessed progress points. The target is conditional on evidence, **not an automatic score grant**. The historical simulation archive remains **996667 / 1000000** and is separate.

| Ledger | Value |
|---|---:|
| New SI project score before v0.18 | **1,400 / 1,000,000** |
| Newly earned, nonduplicated v0.18 project points | **+300** |
| **Current new SI project score** | **1,700 / 1,000,000** |
| Remaining to 100,000 checkpoint | **98,300 points** |
| Historic archival simulation | **996667 / 1000000** (unchanged) |

## v0.18 new evidence and point award
| New and distinctly validated criterion | Maximum | Earned | Evidence |
|---|---:|---:|---|
| Parse-once reusable AxiomFlow AST execution without reparsing | 120 | 120 | `axiomflow/language.py`, `test_no_parsing_during_compiled_execution` |
| 8 regression methods + 800 deterministic source-vs-preparsed examples | 80 | 80 | `tests/test_compile_once.py`, complete CI matrix |
| Three-path measured benchmarks with explicit limitations | 50 | 50 | `benchmarks/compare_decimal.py`, actual CI log medians |
| Versioned 100,000 acceptance-gate plan with no automatic awards | 30 | 30 | `docs/milestone_100k.md` |
| New course lesson and scientific limitations | 20 | 20 | `courses/lesson14_compile_once.md`, `docs/research_v018.md` |
| **Total** | **300** | **300** | No credit for inherited tests or features |

## Verified CI
Code commit `65feb3db6b338d2e886c27244c83cc54cd932996`. [GitHub Actions run 39238016230](https://github.com/shiyamprimetrade-sketch/SI/actions/runs/39238016230), Python 3.11/3.12/3.13 plus Node.js 22, yielded **295/295 tests per version, 885 successful test executions**; no unittest failures or workflow warning annotations.

## New measured numbers (ns per call; exploratory Ubuntu GitHub runners)
| Python | Parse+execute | Preparsed AST execute | Direct Decimal |
|---|---:|---:|---:|
| 3.11 | 20,215.94 | 8,184.40 | 1,357.34 |
| 3.12 | 18,142.33 | 7,559.49 | 1,175.32 |
| 3.13 | 17,282.95 | 7,621.69 | 1,320.61 |

Compile-once is faster **than AxiomFlow reparsing the identical source each invocation** in these short exploratory CI measurements. Direct Python Decimal remains much faster and is **not cost-equivalent**, because it bypasses the interpreted AxiomFlow language, type checks and AST dispatch. Do not claim superiority over Python, Java, C or C++.

## Gate policy
Milestone allocations in `docs/milestone_100k.md` are **cumulative**, not 100k new points on top of the current 1,700; earlier points are included within relevant gates. 100,000 can only be reached by future independently verified functional milestones, integration tests, reproducible benchmarks, course and thesis-style research. Feature evidence must be linked to CI and attributed once. A full million remains a distinct much-longer-horizon ceiling.

The score is provisional engineering-project self-evaluation **not neural-network training, an increase in assistant intelligence, or an externally validated AGI metric**.
