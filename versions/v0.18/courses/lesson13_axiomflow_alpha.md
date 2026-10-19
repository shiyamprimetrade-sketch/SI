# SI Course Lesson 13 — AxiomFlow alpha from grammar to interpreter

**Objectives:** create an AST lexer/parser, evaluate immutable variables, distinguish Decimal scalars from money types, implement deterministic half-even rounding, and benchmark with scientifically valid baselines.

## Exercises
1. Run `python -m axiomflow example.af` and trace each `let`.
2. Use interactive `python -m axiomflow`, then type `emit 2.00 USD + 3.00 USD`.
3. Show why `emit 1.00 USD + 1.00 EUR` must fail. Discuss why no implied FX conversion is permitted.
4. Compute `(125.50 USD + 18.25 USD) * 1.075` and prove rounding order.
5. Propose three invalid inputs; check `AxiomError` rather than raw exceptions.
6. Re-run `benchmarks/compare_decimal.py`, explain why reparsing overhead prevents an apples-to-apples speed conclusion, and propose a fairer benchmark.

**Assessment /10:** 3 grammar, 3 exact-decimal math, 2 adversarial tests, 2 limitations/benchmark rigor. Course scores do not automatically count toward SI progress points.
