# SI v0.10 — Portable lexer and bounded semantic conformance

SI is an experimental programming-language training laboratory in a broader computer-science research and invention mission. The v0.10 contribution is **SI-Portable-1**, an optional portable *source syntax profile* and independently written hand-coded parser. Existing v0.9 `shlex` behavior is retained; this version does **not** change runtime semantics, invent a finished new programming language, or establish universal superiority.

## What's new

- `docs/portable_lexical_spec.md`: ASCII-only profile with precise LF/CRLF, token, comment, decimal integer and identifier rules, caps, normal form and portability limitations.
- `si/portable.py`: independent ASCII token scanner, two-pass label resolver, typed immutable parsed operations and canonical source renderer. It does not import `shlex`, `si.compiler`, or `si.reference`.
- `si/obligations.py`: executable **bounded** parse/canonical round-trip and idempotence checks, enumerating all short strings over a declared alphabet and computing a reproducible SHA-256 results digest.
- `tests/test_portable_*.py`: adversarial lexical tests, bounded exhaustive checks, seeded round-trip and conformance across portable parser, compiler, interpreter, VM and v0.9 small-step model.
- `courses/lesson06_lexers_and_conformance.md`: lesson, labs, exercises and assessment rubric.
- `docs/research_v010.md`: hypotheses, methods, falsifiable obligations, negative results and doctoral-level work plan.
- `docs/training_ledger.md`: historical vs. newly reset SI scores.

## Run from `versions/v0.10`

```sh
python -W error -m unittest discover -s tests -v
python -m si.obligations
python -m si examples.si
```

The CI workflow is `.github/workflows/ci-v010.yml` at repository root. It tests Python 3.11, 3.12 and 3.13 using GitHub Actions. Do not assert CI success until the actual runs conclude.

## Explicit limitations

- The portable profile is **narrower** than v0.9: quoted numeric operands and Unicode comments remain legal in the legacy parser but are intentionally excluded here.
- `si/portable.py` checks lexical/syntactic portability, not portable floating-point runtime behavior, type soundness, security isolation, universal equivalence, or execution outside CPython.
- The finite enumeration and seeded test corpus are executable proof **obligations**, not machine-checked universal theorems.
- No complete thesis, language-invention graduation, terminal prototype or across-all-languages benchmark is claimed.

**New SI mission score: 0 / 1,000,000. New awarded points: 0. Historical simulation archive: 996,667 / 1,000,000.**