# SI v0.9 — Verified GitHub CI and research evidence

**Date checked:** 2026-10-16 (UTC)  
**Repository:** `shiyamprimetrade-sketch/SI`  
**Base branch:** `si-v0.8-bytecode-oracle-20261016` (stacked; still unmerged)  
**Feature branch:** `si-v0.9-operational-semantics-20261016`  
**Code commit tested:** `71db381c11c5f7538150d00c51eede25fe93ef0a`  
**Workflow:** `.github/workflows/ci-v09.yml`  
**GitHub Actions run:** https://github.com/shiyamprimetrade-sketch/SI/actions/runs/38901097045

## Inspected CI job results

| Python | Job ID | Unit tests | Result | Unit-test runner duration |
|---|---:|---:|---|---:|
| 3.11 | 116973256301 | 172/172 | PASS | 1.817 s |
| 3.12 | 116973256721 | 172/172 | PASS | 3.006 s |
| 3.13 | 116973256592 | 172/172 | PASS | 1.490 s |

**Aggregate across runtimes:** 516 successful Python unit-test executions; no failed/error tests in the inspected logs. All three GitHub jobs concluded `success`. Runner workflow additionally executed a Python compileall syntax check and `python -m si examples.si` to test the command-line entry point; it printed the expected countdown `3`, `2`, `1`. No GitHub Actions warning annotations were observed for these three jobs; new action versions `actions/checkout@v7` and `actions/setup-python@v7` ran successfully.

## Executed test command

From `versions/v0.9`:

```sh
python -m compileall -q si tests
python -W error -m unittest discover -s tests -v
python -m si examples.si
```

**New v0.9 tests:** 42 new methods in `tests/test_semantics_v09.py`, added to the inherited 130. Included:
- 715 exhaustively enumerated small integer arithmetic programs over operands -5..5 and six operations, excluding 11 zero-divisor cases.
- 2,000 seeded mixed arithmetic programs (`Random(20261017)`).
- 700 seeded conditional programs (`Random(72207)`).
- 250 seeded source-comment metamorphism cases (`Random(406)`).
- Boundary and negative tests for signed zero, stack/output/step limits, compilation, source errors, immutable state transitions, countdown loops and termination.

The local reference implementation also passed five standalone smoke tests before publishing; these smoke tests were not used as a substitute for remote CI and are **not** counted in the 172 GitHub unit-test methods.

## Counterexample recorded

An early exact-Fraction model produced observable `0.0` for `0 / -3`; current SI/CPython division produces `-0.0`. The executable reference model was corrected to maintain signed-zero behavior, and new regression tests verify it. This is an **evaluator-model refinement**, not a demonstrated bug in the prior SI executor.

## What the result does *not* prove

The runs are finite tests and do not certify a machine-checked semantics, complete correctness for all inputs, general-purpose language superiority, security isolation, a doctoral dissertation, mastery of every programming language, an invented terminal, or artificial superintelligence. The independent evaluator still relies on CPython for tokenization, float operations, and display; mathematical independence is limited. The documented language version remains a rigorous *training artifact*.

**New SI mission score:** 0/1,000,000; **new points awarded:** 0. **Historical simulation ledger:** 996,667/1,000,000 (archival and unchanged). No automatic score from passing tests.