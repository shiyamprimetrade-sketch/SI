# SI v0.15 — Nearest-even rounding invariants and bounded failure reduction

Experimental SI stack language: an engineering research training artifact, not validated artificial superintelligence.

## Delta from v0.14
- Retains the v0.14 interpreter/compiler, Node VM, and previous tests.
- New `tests/test_rounding_invariants.py`: independently checks binary64 candidate outputs against exact rational distances to adjacent representable floats and ties-to-even significand parity. Covers zero/subnormal ties, subnormal-normal boundary, large balanced ratios and seeded rational tests.
- Deterministic `deterministic_shrink` reduces counterexamples with a monotone rank and attempt bound, demonstrated on **synthetic** failures.
- New research note, machine-executable obligations and course lesson 11.

Run `python -W error -m unittest discover -s tests -v` in this directory. GitHub Actions `.github/workflows/ci-v015.yml` runs Python 3.11–3.13 with Node.js 22. Finite checks are not a universal proof.

**Score before v0.15:** new SI self-assessed 500/1,000,000. Historical archive 996,667/1,000,000 unchanged.
