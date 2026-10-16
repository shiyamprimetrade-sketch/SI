# SI v0.12 — GitHub CI evidence and recovered defect

## Baseline and changed code

- Parent draft [PR #7](https://github.com/shiyamprimetrade-sketch/SI/pull/7) passed the v0.11 parser conformance suite.
- New draft [PR #8](https://github.com/shiyamprimetrade-sketch/SI/pull/8) stacks on the v0.11 branch, not `main`.
- Initial v0.12 code commit `23ca87ffe7595e3fb3ede45146fb50b309c8bbb3` introduced an independent Node.js VM and 18 Python-to-Node execution conformance tests.
- Corrected code commit `2609c74da17bd544633be46b058a9630166a76c6` fixes error classification for rejected bare-CR source text.

## Failed experiment (retained)

[GitHub Actions run 38905581699](https://github.com/shiyamprimetrade-sketch/SI/actions/runs/38905581699) **FAILED** on Python 3.11, 3.12 and 3.13. One test in `test_cross_runtime_vm.py`, `test_rejected_malformed_source`, failed because input `'PUSH 1\\rADD'` received JavaScript category `other error`, but Python classified it as `parse error`. This demonstrates an actual error-taxonomy inconsistency, not a successful initial run. No other test failure was observed in the inspected Python 3.11 log.

A focused code change in `js/vm.js` now classifies `bare CR` and `character at offset` rejections as `parse error`.

## Successful full retest

[GitHub Actions run 38905711938](https://github.com/shiyamprimetrade-sketch/SI/actions/runs/38905711938), tested commit `2609c74da17bd544633be46b058a9630166a76c6`:

| Python | GitHub job ID | Tests | Result |
|---|---:|---:|---|
| 3.11 | 116988636817 | 235/235 | PASSED |
| 3.12 | 116988637143 | 235/235 | PASSED |
| 3.13 | 116988637243 | 235/235 | PASSED |

**705 successful unittest executions.** There were **0 GitHub warning annotations** in the inspected logs. The workflow uses Node.js 22 and the inherited Python 3.11/3.12/3.13 matrix, runs Python source compilation, JavaScript syntax checks, full Python-and-Node tests, SI CLI smoke and the prior bounded lexical proof obligations.

The source-obligation digest remains unchanged across the three versions:

`9997585eb832c9a59660a7ff3873c1e53a087a975b17a79198512aa36a30bd4d`

## New v0.12 test scope

Eighteen test methods include a combined **360 seeded arithmetic programs, 240 seeded branching programs and 150 seeded budget configurations**, plus directed stack, step, output, signed-zero, underflow, division-by-zero, numeric overflow, integer-bit-budget, nonfinite results, rejection, and more-than-53-bit integer tests. The inherited v0.11 test suite remains.

All cross-runtime comparisons run Python source and compiled VM plus an independent Python small-step reference evaluator, then compare with an independently authored Node.js execution engine.

## Caveats and future scientific obligations

- JavaScript `BigInt` vs Python `int` agree in tested cases, not necessarily on all operations or float conversions.
- JavaScript `Number` and Python `float` are both binary64 but may differ in exact string rendering and rounding on edge cases. The current conformance domain is finite and does not prove full equivalence.
- Error categories are intentionally coarser than exception messages.
- No process sandbox or non-Linux CI has been established.
- A genuine formal semantics proof, controlled language benchmark, original-language invention, full curriculum, doctoral thesis and new terminal remain future milestones.

**New SI challenge score: 0/1,000,000; new points 0. Historical archive 996667/1,000,000 unchanged.**
