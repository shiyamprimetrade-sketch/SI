# SI v0.24 research notebook — Typed relations and independent money arithmetic

## Hypotheses and methodology
H1. Integrating the prior scalar/function parser into the table DSL can preserve type safety for row-level filters and derived expressions. H2. Independent JS BigInt fixed-point comparisons can expose numerical disagreements in bounded table workloads.

The new `filter` and `derive` constructs use type inference against schema columns, declared pure functions and money/scalar values. An existing bounded compile-then-run table engine executes records. Tests include invalid schema/type/operation cases, repeated compiled execution, 250 seeded independent Decimal relational calculations and 200 seeded Node.js BigInt reference comparisons.

## Performance study design
Run `python benchmarks/table_workload.py`, which verifies identical outputs before measuring a 100-dataset × 15-row table batch. Python executes precompiled table plans in-process; JavaScript executes an independent fixed-cents comparator through a Node.js child process. This **is not cost-equivalent**, includes process startup in JS and differing language operations; only a preliminary telemetry baseline is collected. Publish negative findings and do not claim superiority over Python/C/C++/Java/JavaScript.

## Reproducibility and limitations
The CLI demonstrates a language-level user-defined function in a derived table column. Resources are bounded but no secure process sandbox is established. No proof of full language soundness, complete relational algebra, SQL optimizer, general dependency resolution, binary compiler, native frontend/backend, complete doctoral dissertation, or independent all-features runtime is claimed.

The cumulative 100,000-point milestone remains conditional; previous project score 5450/1,000,000 and archive 996667/1,000,000 are distinct. New points require actual CI evidence and nonduplicative tests.
