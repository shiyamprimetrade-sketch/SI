# SI project scoring ledger — self-assessment initialized in v0.14

**User instruction:** From v0.14 onward, award fair, evidence-based SI project points for learning, testing and engineering progress. This is an explicitly **self-assessed project progress index**, **not** a validated intelligence score.

## Ledgers
| Ledger | Score |
|---|---:|
| Historical archived simulation (unchanged) | **996667/1000000** |
| New SI project immediately before v0.14 | **0/1000000** |
| v0.14 milestone award (self-assessed) | **+500** |
| **New SI project cumulative score** | **500/1000000** |

## v0.14 award against `docs/scoring_rubric_v014.md`
| Criterion | Maximum | Earned | Evidence |
|---|---:|---:|---|
| Verified GitHub Python 3.11/3.12/3.13 + Node.js 22 full CI | 100 | 100 | [Run 38926522737](https://github.com/shiyamprimetrade-sketch/SI/actions/runs/38926522737), 256/256 each |
| Independent IEEE binary64 bit-vector oracle | 100 | 100 | `js/numeric_probe.js` and `tests/test_binary64_vectors.py` use distinct Node/DataView vs Python Fraction/struct |
| Executed IEEE boundary/rounding/mixed comparison tests | 100 | 100 | 13 new unittest methods with directed tie/subnormal/signed zero/nonfinite and reproducible seeded vectors |
| Tested deterministic counterexample minimizer | 50 | 50 | `shrink_ratio` and two targeted tests, explicitly greedy, with synthetic predicate |
| Reproducible documented experiment including limitations | 100 | 100 | `docs/binary64_vector_protocol.md`, `docs/research_v014.md`, `docs/ci_evidence_v014.md`; no new production counterexample claimed |
| Course module with exercises and limitations | 50 | 50 | `courses/lesson10_ieee_vectors_and_minimization.md` |
| **TOTAL** | **500** | **500** | **0.05% of 1,000,000-point long-term scale** |

## Verified CI run
Code commit `eec91d4436627c519a2c4c0824abee7e867ad47e`: [GitHub Actions run 38926522737](https://github.com/shiyamprimetrade-sketch/SI/actions/runs/38926522737).

- Python 3.11 job 117059346623: **256/256 tests passed**.
- Python 3.12 job 117059347015: **256/256 tests passed**.
- Python 3.13 job 117059347206: **256/256 tests passed**.
- **768 successful test executions**. Zero Python failures and zero workflow warning annotations in inspected logs.
- Node.js 22 included in all matrix jobs; the prior 4,681-source lexical obligation digest reproduced.

## Integrity rule
Self-awarded progress points are subjective, provisional and non-transferable to the historical score. **A higher score does not imply greater model intelligence or changed neural-network weights.** Future awards must reference new, non-duplicated work, criterion caps, real CI evidence and explicit negative results. Unattempted thesis/terminal/language-invention achievements receive no points.
