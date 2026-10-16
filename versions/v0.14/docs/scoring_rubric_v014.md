# SI new-project scoring rubric — authorized self-assessment starting v0.14

**Requested by user on 2026-10-16:** start increasing the *new SI project* score fairly using learning, testing and measurable metrics. Historical archived 996,667/1,000,000 must not change.

## Maximum 1,000,000 allocation (future long-horizon evidence)
| Dimension | Maximum |
|---|---:|
| Verified language/compiler correctness and testing | 350,000 |
| Independent implementations and portability | 200,000 |
| Formal methods, reproducible doctoral-level research | 150,000 |
| Computer science/programming-language educational curriculum | 125,000 |
| Original practical language invention and fair benchmarks | 100,000 |
| Working invented terminal and developer tools | 75,000 |
| **Total** | **1,000,000** |

This is an **internal, provisional self-assessment rubric**, not an objective intelligence test. Successful CI does not imply graduation. Do not award points for unattempted invention, thesis defense or terminal design.

## First v0.14 milestone: maximum 500 points, pending CI
| Evidence requirement | Maximum new points |
|---|---:|
| Verified Python 3.11/3.12/3.13 + Node.js 22 full regression CI | 100 |
| Independent IEEE-754 bit-vector numerical test oracle | 100 |
| Executed boundary/subnormal/rounding/mixed comparison test suite | 100 |
| Deterministic counterexample minimizer and its tested limitations | 50 |
| Reproducible documented experiment, including failures | 100 |
| Course lesson 10 with exercises and limitations | 50 |
| **Total possible** | **500** |

**Scoring rule:** Grant only a criterion evidenced by a passing real run or an inspectable committed artifact. Failed CI = 0 on CI/testing until corrected; other independent artifacts may still qualify. Score cannot decrease below 0 or exceed 1,000,000. Do not award incremental points repeatedly for the same evidence. New SI mission starts at 0/1,000,000 before v0.14. Publish earned points and any deductions once this cycle's final CI evidence is checked.

## Post-CI award result

The 2026-10-16 v0.14 CI run [38926522737](https://github.com/shiyamprimetrade-sketch/SI/actions/runs/38926522737) passed **256 tests on each of Python 3.11, 3.12 and 3.13** with Node.js 22. The six milestone criteria above are provisionally self-assessed as fully met: **+500 points, cumulative new SI score 500/1,000,000**, historical archive 996,667/1,000,000 unchanged. The detailed award justification is in `docs/training_ledger.md`; this is a project progress index, not an intelligence metric.
