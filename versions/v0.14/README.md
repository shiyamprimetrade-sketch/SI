# SI v0.14 — Raw binary64 vectors and reproducible numeric counterexamples

Expands the experimental SI language laboratory with a separate Node.js numerical probe, exact expected binary64 bits from a Python Fraction/struct oracle, adversarial boundaries, deterministic seeds and a greedy counterexample reducer.

Files:
- `js/numeric_probe.js` — ratio, raw binary64 hex, integer/float comparison operations.
- `tests/test_binary64_vectors.py` — independently expected bit, decimal and comparison vectors; seeded experiments and minimizer tests.
- `docs/binary64_vector_protocol.md` — machine-checkable finite obligations and explicit scientific limits.
- `docs/research_v014.md` — research hypotheses, failure evidence and next experiments.
- `courses/lesson10_ieee_vectors_and_minimization.md` — course module with assessment.
- `docs/scoring_rubric_v014.md` — new SI **self-assessment** scoring method; historical archive remains separate.

## Run from `versions/v0.14`
```sh
node --version
python -W error -m unittest discover -s tests -v
python -W error -m si.obligations
python -m si examples.si
```
GitHub Actions `.github/workflows/ci-v014.yml` runs Python 3.11/3.12/3.13 with Node.js 22. Do not infer real CI success from the presence of code or tests.

Passing this finite suite is not full IEEE correctness proof, language superiority, a doctoral thesis, invented language graduation or terminal completion. Points in the new self-assessment ledger require verified evidence.
