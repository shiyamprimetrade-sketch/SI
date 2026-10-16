# SI v0.13 — Precise binary64 semantics and deterministic output conventions

This version addresses a real cross-runtime discrepancy between SI's CPython execution engines and the independent Node.js engine.

## Work
- Improved `js/vm.js`: direct correct-rounding BigInt ratio to binary64, integer/float exact comparisons, Python-like numeric display thresholds and preserved signed zero.
- Extended the cross-runtime test suite with targeted and reproducibly seeded precision, overflow, scientific-notation and subnormal cases.
- Added `docs/numeric_semantics.md`, `docs/research_v013.md` and `courses/lesson09_binary64_and_exact_rationals.md`.
- Preserves previous SI versions and the experimental legacy language behavior; no `main` changes.

## Run from versions/v0.13
```sh
python -W error -m unittest discover -s tests -v
python -W error -m si.obligations
python -m si examples.si
```

The GitHub CI file `.github/workflows/ci-v013.yml` runs Python 3.11–3.13 and Node.js 22, including JS syntax, full conformance and the bounded lexical obligations.

**Limitations:** finite behavioral conformance is not a universal proof of CPython/ECMAScript float equivalence or host safety, and it is not evidence of language speed advantages, PhD completion, terminal invention or SI graduation.

**New SI project score: 0/1000000, awarded points 0. Historical simulation archive: 996667/1000000.**
