# SI v0.14 — Research note: binary64 boundaries and counterexample minimization

## Question
Can we independently check exact binary64 outcomes of the Node BigInt-rational VM using raw IEEE-754 bit-vector evidence rather than only string agreement of SI programs?

## Falsifiable protocol
`js/numeric_probe.js` provides a narrow JSON/Node interface for exact integer-ratio division (`ratio`), hexadecimal binary64-to-decimal rendering (`bits`), and exact integer/float comparison (`compare`). The independent Python test oracle uses `fractions.Fraction`, `struct.pack('>d')`, and `struct.unpack('>d')`, with explicit signed-zero handling.

Initial directed corpus:
- positive/negative zero, min positive/negative subnormal, max subnormal, min normal, exact 1.0 and neighbors, max finite, nonfinite patterns;
- exactly halfway ratios at the 53-bit significand and 2^-1075 subnormal boundary;
- finite and overflowing ratios of very large integers;
- exact mixed integer/float comparisons beyond 2^53;
- seeded arbitrary finite binary64 bit patterns, large bounded integer ratios, near-subnormal ratios.

The test harness also includes a deterministic greedy decimal digit remover to shrink a reproducible failure; its unit test uses a synthetic failing predicate rather than falsely claiming a real fault was found.

## What would constitute evidence
An exact bit-pattern match supports IEEE rounding for the sampled rational, while a string match supports tested CPython-compatible decimal formatting. Both are distinct from formal all-input equivalence. Failed vectors must be retained and minimized without overclaiming a globally minimal example. Per-version CI must be observed in GitHub logs.

## Threats
The Python oracle and Node VM use the same underlying binary64 hardware environment, despite separately implemented conversion paths. Both might share misunderstood specification requirements. `float(Fraction)` is a CPython behavioral reference, not a proof assistant. Random corpora are not exhaustive. Float shortest round-trip string canonicalization might still differ between JS and Python in rare cases.

No invention of a new complete programming language, independently verified intelligence, completed PhD thesis, terminal or universal performance claim is made.

## Next research
Find an independently specified curated IEEE-754 test corpus with redistribution permissions, create a mathematically stated rounding invariant and explore a mechanically checked proof obligation, investigate known shortest-decimal tie cases, run independent toolchains/architectures, and only then consider a new language specification and benchmark design.
