# SI v0.17 — Day-one CI and exploratory benchmark evidence

**GitHub Actions:** https://github.com/shiyamprimetrade-sketch/SI/actions/runs/39236516788
**Code commit:** `5b17c9d93bb53751218bc40412683475dddd2a66`
**Workflow:** `.github/workflows/ci-v017.yml`

| Python | Node | Job | Unittest result |
|---|---|---:|---|
| 3.11 | 22 | 118006785330 | 287/287 passed |
| 3.12 | 22 | 118006784850 | 287/287 passed |
| 3.13 | 22 | 118006785051 | 287/287 passed |

861 successful executions. Complete suite run with `python -W error -m unittest discover -s tests -v`. No test failures or warning annotations in inspected job logs. Syntax check, AxiomFlow example, exploratory benchmark and inherited SI bounded lexical obligations succeeded in workflow. Original lexical digest `9997585eb832c9a59660a7ff3873c1e53a087a975b17a79198512aa36a30bd4d` reproduced.

## Verified positive claim
Working interpreter for a **restricted** AxiomFlow DSL with money/currency typing, fixed-cent half-even rounding, strict errors, immutable variables and CLI. The new `test_axiomflow.py` adds 15 unittest methods including 500 seeded Decimal-model samples. Source and tests are inspectable.

## Verified negative result
Small exploratory CI benchmark (100 iterations/repeat, 3 repeats) measured AxiomFlow repeatedly parsing source much slower than a direct Python Decimal expression. The paths are not equivalent work units, so this is NOT a valid universal performance ranking. See `docs/training_ledger.md` for raw medians.

## Future proof obligations
Design cost-equivalent tests for numeric correctness, run AxiomFlow parse-once execution, compare real Python/JS/Java/C/C++ algorithms, verify setup/dependency installation cost, record memory and CPU, multiple OS/architectures and usability data. None has been established in v0.17. The proposed web/backend/frontend/ML functionality, complete terminal and doctoral thesis remain future deliverables.

**Ten-day sprint:** Oct 19–29, 2026. A ten-day effort cannot responsibly guarantee global superiority over every existing programming language. Preserve negative results.
