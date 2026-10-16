# SI v0.13 — Verified numeric CI evidence

## Baseline review
Draft PR #8 at `0a551e4f27052ec48ae258ca7d614bbc99940573` passed v0.12 CI (235 tests on each Python 3.11, 3.12, 3.13 with Node.js 22).

Source-level numeric counterexamples motivating v0.13:
1. Integer ratio `10**400 / 10**400` is finite 1.0 in Python. v0.12 Node VM converts both operands to `Number` before division, causing overflow.
2. The division `1 / 10**6` produces Python string `1e-06`, while JavaScript `Number.toString()` prints `0.000001`. Likewise Python uses exponent form at 1e16 while JavaScript does not.
3. Python mixed comparison of integer `9007199254740993` and float `9007199254740992.0` distinguishes them, while converting the integer to JS `Number` loses the least significant unit.

## Implementation
- `js/vm.js`: direct BigInt quotient/remainder rounding of exact integer ratio to IEEE-754 binary64 (round-to-nearest, ties-even, including subnormal and signed zero).
- `js/vm.js`: exact rational comparison of BigInt integers against binary64 operands.
- `js/vm.js`: normalize JS shortest-decimal floats to CPython-like scientific/fixed thresholds.
- `tests/test_cross_runtime_vm.py`: 8 additional test methods, including seeded balanced huge integer ratios and decimal formatting threshold cases.
- `docs/numeric_semantics.md`, `docs/research_v013.md` and `courses/lesson09_binary64_and_exact_rationals.md`.

## Verified GitHub CI — code commit e3fb61bbe392935de9bf548e417df58e08c4eee7

[GitHub Actions run 38915571416](https://github.com/shiyamprimetrade-sketch/SI/actions/runs/38915571416), workflow `.github/workflows/ci-v013.yml`:

| Python | Job ID | Unittest tests | Job outcome |
|---|---:|---:|---|
| 3.11 | 117022034938 | 243/243 | SUCCESS |
| 3.12 | 117022035431 | 243/243 | SUCCESS |
| 3.13 | 117022035541 | 243/243 | SUCCESS |

**729 successful test executions**, zero failed unittest methods and **zero GitHub warning annotations** in inspected logs. Node.js 22 used throughout matrix. Python compileall, JS syntax, inherited language CLI smoke and bounded lexical corpus succeeded as steps of the completed workflow. The lexical corpus SHA256 was identical across all three jobs:

`9997585eb832c9a59660a7ff3873c1e53a087a975b17a79198512aa36a30bd4d`

## Scientific qualifications and future research
- This is finite cross-runtime behavioral evidence, not a machine-checked proof of correct rounding for all ratios or of cross-runtime output equivalence.
- Decimal formatting uses JavaScript shortest-decimal output as its starting point. Rare cases may still differ from Python; a formal shortest-roundtrip decimal specification and external conformance corpus are needed.
- Comparison model is a tested implementation, not an independent formally validated theorem prover.
- No performance benchmarks versus other languages, complete doctoral-level thesis, novel complete programming language, terminal prototype or superintelligence claim.

**Score ledgers:** new SI mission **0/1,000,000**, awarded points **0**; historical archive **996,667/1,000,000**, unchanged. Draft stacked on unmerged v0.12; `main` not touched.
