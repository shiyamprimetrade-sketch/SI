# SI v0.15 evidence-based self-assessment ledger

| Ledger | Score |
|---|---:|
| Historical archived simulation (unchanged) | **996667 / 1000000** |
| New SI research project before v0.15 | 500 / 1000000 |
| v0.15 new nonduplicative award | **+250** |
| **New SI research project cumulative** | **750 / 1000000** |

This user-authorized self-assessment is an engineering progress index, not a measurement of neural-model intelligence. v0.14's 500 points remain assigned to its already audited criteria; v0.15 does not award a second set of points for the same Python+Node CI matrix, previous numeric bit vectors or prior coursework.

## Incremental v0.15 assessment — 250 / 250
| New v0.15 requirement | Points | Evidence |
|---|---:|---|
| Exact-rational nearest-neighbor and ties-even obligation checker, not present in v0.14 | 100 | `tests/test_rounding_invariants.py`, successful live CI |
| Negative control proves obligation rejects an intentionally wrong result | 50 | `test_proof_checker_catches_wrong_neighbor` |
| Improved deterministic, monotone, attempt-bounded counterexample reducer | 50 | `deterministic_shrink` and 3 dedicated tests |
| New course lesson on invariants and reduction | 25 | `courses/lesson11_ieee_invariants.md` |
| Reproducible v0.15 research protocol and honest limitations | 25 | `docs/rounding_obligations_v015.md`, `docs/research_v015.md`, `docs/ci_evidence_v015.md` |
| **Total** | **250** | All criteria verified or inspectable |

## Verified CI
[GitHub Actions run 39232601260](https://github.com/shiyamprimetrade-sketch/SI/actions/runs/39232601260), tested commit `f44e945bb1e821cfd8ba06227625feda214959eb`.

- Python 3.11, Node.js 22: 265/265 tests passed (job `117993904713`).
- Python 3.12, Node.js 22: 265/265 tests passed (job `117993904374`).
- Python 3.13, Node.js 22: 265/265 tests passed (job `117993904211`).
- **795 passing test executions**; no Python unittest failures or workflow warning annotations in inspected job logs.
- Original SI lexical obligation SHA digest reproduced on all three versions.

## Explicit deductions and limits
- **0 points** for simply rerunning the existing CI matrix.
- **0 points** for the inherited bit vectors and v0.14's earlier minimizer implementation.
- **0 points** for unattempted original language invention, general-purpose benchmarks, defended thesis or terminal.
- No new production floating-point bug was found in these tests; the negative control was deliberately injected.
- This is a provisional, self-scored project index; finite tests do not prove a universal theorem or independently certified general intelligence.
