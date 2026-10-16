# SI v0.8 reproducible CI evidence

**Repository:** `shiyamprimetrade-sketch/SI`
**Feature branch:** `si-v0.8-bytecode-oracle-20261016`
**Code commit tested:** `8b359ea5559fd5b1bfc7a8a9631331a505cf33c2`
**Run:** https://github.com/shiyamprimetrade-sketch/SI/actions/runs/38898831534
**Workflow:** `.github/workflows/ci-v08.yml`
**Command:** `python -W error -m unittest discover -s tests -v` from `versions/v0.8`.

## Observed job results (GitHub Actions logs, 2026-10-16 UTC)

| Python runtime | GitHub job ID | Tests | Result | Wall time (test runner) |
|---|---:|---:|---|---:|
| 3.11 | 116965770018 | 130/130 | PASSED | 1.869 s |
| 3.12 | 116965770061 | 130/130 | PASSED | 2.202 s |
| 3.13 | 116965769994 | 130/130 | PASSED | 1.904 s |

**Summary:** 390 successful test executions across three runtimes. No Python unittest failures in the inspected logs. All three jobs concluded `success`.

## Newly added coverage
- 24 new `test_bytecode_validation.py` tests including 600 deterministic mutated invalid-bytecode cases.
- 6 new `test_independent_oracle.py` tests including 2,400 deterministic rational-oracle arithmetic samples and 400 conditional-program samples.
- 100 inherited v0.7 tests.
- Random seeds: 20261016 (bytecode fuzz), 18102026 (integer oracle), 808 (control flow).

## Warnings
GitHub runner emitted a Node.js deprecation warning: `actions/checkout@v4` and `actions/setup-python@v5` use deprecated Node.js 20 compatibility. GitHub forced Node.js 24. This warning was nonfatal and is separate from Python test success. Updating to GitHub-supported newer major versions of these actions is recommended in a later maintenance cycle after compatibility checks.

## Methodological caveats
This result is **not** proof of universal bytecode safety, sandbox isolation, formal equivalence, superior performance, peer-reviewed language invention, or a terminal implementation. The independent Fraction oracle does not invoke SI's `apply_binary`, but uses the CPython standard library. The suite tests finite cases.

**Historical archive:** 996667/1000000; **new SI mission score:** 0/1000000; **awarded points:** 0.
