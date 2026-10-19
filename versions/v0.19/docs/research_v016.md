# SI v0.16 — Shortest-decimal research and new language scoping

## Reviewed baseline
SI v0.15 draft PR #11 head `69d78c22bf078d093fb9d800f45052aa8b608d57` passed GitHub Python 3.11–3.13 plus Node.js 22, 265 unittest methods per Python runtime; historical archive and self-scored SI ledger kept separate.

## Experiment
New `tests/test_decimal_roundtrip.py` tests Node-generated string rendering for finite IEEE-754 bit patterns and compares with independently obtained Python `str(float)`, `struct` bits, and finite roundtrip `float(text)`. It tests exact negative-zero preservation, exponent thresholds and a fixed-seed set of 800 random binary64 encodings plus neighborhood values. This is a **finite conformance experiment**, not a theorem of globally shortest formatting.

## Negative/limiting examples
- Python's `1e-06` and `1e-6` parse to the same float. Thus byte-length alone cannot define the Python-compatible canonical representation.
- Source-level numeric conversion parity may depend on CPython's formatting choices and JS shortest-roundtrip seed algorithm; agreement on finite test corpora does not make the algorithms independent of those runtimes.
- Parsing back to an identical float is **necessary but not sufficient** for shortest representational optimality.
- This cycle does not implement the proposed new language; `docs/language_proposal.md` states intended use cases and preregistered benchmark criteria.

## Reproducibility
Python `-W error -m unittest discover -s tests -v`, Node.js 22; `python -m si.obligations`, `python -m si examples.si`. Record actual three-version GitHub jobs and failures. Do not transfer points for inherited CI or preexisting vector tests.

## Research honesty
No verified broad cross-language performance superiority, no formally mechanized decimal formatter proof, no completed PhD thesis, no prototype terminal. The SI stack language is an experimental scaffold for the proposed AxiomFlow design.
