# SI v0.16 — Reproducible GitHub CI and decimal research evidence

## Baseline
Draft v0.15 PR #11 at `69d78c22bf078d093fb9d800f45052aa8b608d57` passed Python 3.11–3.13 + Node.js 22, 265 tests/version. Main remained untouched at `573cf6ea850fe72698ea2a45c6bd854b329c7357`.

## v0.16 tested source
Commit `6e61f4a8c7097877454545c13b3d6ff7ab7ffc83` adds `tests/test_decimal_roundtrip.py`, `docs/language_proposal.md`, `courses/lesson12_decimal_and_language_design.md`, `docs/research_v016.md` and `.github/workflows/ci-v016.yml`.

[GitHub Actions run 39233483078](https://github.com/shiyamprimetrade-sketch/SI/actions/runs/39233483078):

| Runtime | Job ID | Tests | Outcome |
|---|---:|---:|---|
| Python 3.11 + Node 22 | 117996839869 | 272/272 | SUCCESS |
| Python 3.12 + Node 22 | 117996840331 | 272/272 | SUCCESS |
| Python 3.13 + Node 22 | 117996840198 | 272/272 | SUCCESS |

**816 passed executions**, zero test failures and zero workflow warnings in inspected CI logs. `python -W error -m unittest discover -s tests -v` was executed from `versions/v0.16`, alongside Node syntax checks, bounded lexical properties and CLI smoke test. Inherited lexical digest `9997585eb832c9a59660a7ff3873c1e53a087a975b17a79198512aa36a30bd4d` reproduced across all three jobs.

## What is and is not checked
- The new test module checks 800 seeded finite binary64 bit strings and additional exponent-neighbor cases against Node's decimal rendering, Python `str(float)`, Python binary64 `struct` bytes and `float(text)` roundtrip.
- Correctly tests negative-zero preservation at the bit level.
- Shows that a shorter spelling such as `1e-6` parses equivalently to `1e-06` and therefore character deletion alone is not a sufficient test for Python-compatible canonical output.
- The optional character-removal exploration is **not an asserted shortest-decimal proof obligation**. No globally shortest representation theorem follows.
- The AxiomFlow design document is a **proposal only**, with intended niche and preregistered comparisons to established languages; no implementation or benchmark results are asserted.
- No numerical production bug was identified in these cases. No machine-checked formal proof, doctoral dissertation defense or terminal was completed.

## Self-scored ledger
v0.15 carried 750/1,000,000 new SI project points. v0.16 provisions **+200** for new tested roundtrip criteria, scoped language design proposal, learning module and reproducible research, for cumulative **950/1,000,000**. The historical archived **996667/1000000** is preserved unchanged. Project points are not a validated AI intelligence measure.
