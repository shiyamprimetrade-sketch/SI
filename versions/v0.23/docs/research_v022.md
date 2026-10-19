# SI v0.22 research notebook — Immutable tables, partial evaluation and numerical portability

## Hypotheses
H1. Pre-parsing and typechecking a pure AxiomFlow money function once can reduce repeated feature construction overhead relative to parsing the same function source for every CSV row.
H2. A strict immutable, bounded, typed host Table API can offer deterministic projection, stable sort, aggregate and feature augmentation, with early rejection of invalid records.
H3. Independent integer-cent arithmetic in Node.js can reproduce typed AxiomFlow half-even monetary output on bounded cases.

## Methods
- `feature_precompiled` uses `parse_function` and `static_check` at module import, followed by per-request fresh typed values and `execute_expression` without reparsing. Existing v0.21 `feature_axiomflow` retained as differential reference.
- `Table`/`Record` frozen dataclasses with column name/type alignment, bounded finite Decimal rows, deterministic projection/sorting/aggregation, and typed landed-cost column augmentation. **Python host API only**, not original grammar syntax.
- 400 seeded comparisons of old AxiomFlow vs compiled AxiomFlow vs independent Decimal, plus 250 cases compared against separately written Node BigInt cent arithmetic.
- Microbenchmark medians repeat on Python 3.11, 3.12 and 3.13 runners: same output controls, but not cost-equivalent to direct Python Decimal because interpreted AST and type checks remain.
- Reproducible deterministic source archive includes new table module, inheriting SHA pins and ZIP reproducibility checks.

## Evidence and negative observations
Only real completed GitHub CI logs can establish pass/fail and measured overhead. No globally proven type-system soundness, host-independent table runtime, native compiled execution, real browser E2E automation, controlled Java/C/C++ application baselines or universal language advantage exists here. An independent Node BigInt fixed-point comparator is limited to monetary arithmetic, not a JS AxiomFlow interpreter.

## Next thesis and course work
Specify table schemas as grammar constructs, implement a second table runtime, compare against SQL/Pandas/Java collections on identical tasks, harden sources/serialization, and prepare thesis-style experiments with negative results and real release validation.
