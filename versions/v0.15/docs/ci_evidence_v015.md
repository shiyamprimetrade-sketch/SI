# SI v0.15 — Reproducible CI and rounding-invariant evidence

**Code commit:** `f44e945bb1e821cfd8ba06227625feda214959eb`
**Workflow:** `.github/workflows/ci-v015.yml`
**GitHub Actions:** https://github.com/shiyamprimetrade-sketch/SI/actions/runs/39232601260

| Python | Node | Job ID | Result | Test seconds |
|---|---|---:|---|---:|
| 3.11 | 22 | 117993904713 | 265/265 passed | 6.918 |
| 3.12 | 22 | 117993904374 | 265/265 passed | 3.771 |
| 3.13 | 22 | 117993904211 | 265/265 passed | 5.004 |

**795 successful test executions**, zero unittest failures, zero GitHub warning annotations in the three inspected logs. Workflow includes syntax compilation, complete tests, executable bounded lexical checks and SI CLI smoke.

The inherited lexical SHA256 was reproduced across jobs: `9997585eb832c9a59660a7ff3873c1e53a087a975b17a79198512aa36a30bd4d`.

## v0.15 experiment
Nine additional test methods validate exact rational distance to nearest representable binary64 neighbors, ties-to-even low significand parity, signed zero, subnormal/normal boundary, 250 seeded rational neighborhoods (seed 151501), very large balanced ratios, a deliberately wrong candidate as negative control and a deterministic bounded monotone counterexample reduction on a synthetic predicate.

No new genuine production counterexample was discovered; therefore no source engine repair is claimed. The test suite inherits earlier source parser, VM and numerical behavior checks.

## Scientific limitations
- Executable obligations cover only selected finite candidate/target pairs, not all binary64 possibilities or all SI programs.
- The Python Fraction/math.nextafter checker and JS/Node VM share underlying floating-point hardware conventions; the tests are independent in algorithm, not formal theorem proving.
- The greedy shrinker returns a reduced reproducing input but cannot promise globally minimal counterexamples.
- The shortest-roundtrip decimal problem and portable float semantics remain incompletely specified for all inputs.
- No performance superiority claim, new fully-fledged programming language, completed PhD thesis or terminal is established.

**Historical score**: 996667/1000000 unchanged. **New SI score**: 750/1000000 (500 prior + 250 user-authorized, self-assessed v0.15 points). Score is research/project progress only.
