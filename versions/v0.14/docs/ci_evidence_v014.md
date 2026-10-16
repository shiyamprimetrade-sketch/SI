# SI v0.14 — GitHub CI and numeric-vector research evidence

**Run:** https://github.com/shiyamprimetrade-sketch/SI/actions/runs/38926522737
**Tested code commit:** `eec91d4436627c519a2c4c0824abee7e867ad47e`
**GitHub workflow:** `.github/workflows/ci-v014.yml`
**Command:** `python -W error -m unittest discover -s tests -v` in `versions/v0.14`.

## Observed job results
| Python runtime | GitHub job ID | Passed tests | Runner test duration |
|---|---:|---:|---:|
| 3.11 | 117059346623 | 256/256 | 6.716 seconds |
| 3.12 | 117059347015 | 256/256 | 6.839 seconds |
| 3.13 | 117059347206 | 256/256 | 4.019 seconds |

**768 passed test executions, no failures or GitHub warning annotations in inspected job logs.** All three matrix jobs also used Node.js 22; JS syntax, Python compilation, bounded lexical obligations and existing SI source CLI were in the successful CI workflow.

## Reproducible finite obligations
The inherited v0.10 Python source roundtrip checker still produced SHA256 `9997585eb832c9a59660a7ff3873c1e53a087a975b17a79198512aa36a30bd4d` on all three Python versions. It exhaustively covers 4,681 strings over the chosen eight-character alphabet at length ≤4; this is not an all-input theorem.

The v0.14 vector tester defines independently expected IEEE results using Python Fraction and struct, then compares with Node/DataView BigInt result bits and decimal formatting. Thirteen newly added test methods cover directed IEEE encodings, zeros, subnormals, ties-even, huge integer ratio overflow, mixed integer/float comparisons, 300 seeded raw binary64 patterns, 300 seeded huge integer ratios, 120 near-subnormal ratio samples, and deterministic synthetic failure shrinking. The unit-test count is by methods, not the number of generated cases.

## Negative findings and limits
The prior v0.13 CI passed, and no new failing vector was identified in this v0.14 test corpus. The minimizer is tested on an intentionally synthetic predicate; claiming a discovered real floating-point defect from it would be inaccurate. The new probe currently exercises finite numeric behavior and distinguishes NaN/inf rejection, but no independent formally proved Ryu/Dragonbox formatter or mechanized rounding proof exists.

**Scoring:** user-authorized, provisional self-assessment awards +500 SI project points in this iteration, cumulative **500/1,000,000**. Historical archived score **996667/1000000** unchanged; these are not intelligence metrics.

**Stacked draft** v0.14 is based on unmerged v0.13. Neither `main` nor past version directories were changed.
