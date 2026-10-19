# SI course lesson 22 — Combining lexical scopes with table relations

## Learning objectives
Explain lexical immutable bindings, AST representation, static type inference across value/table scopes, row-local evaluation, and the limits of independently implemented conformance subsets.

## Lab tasks
1. Run `python -m axiomflow.unified examples/mixed_table.af --csv data/landed_cost.csv`. Identify where `min_price` (USD) and `multiplier` (scalar) enter the table filter and derived column.
2. Replace `min_price` with an EUR or scalar value. Explain the static rejection and distinguish source parsing from runtime.
3. Move a `let` below the table declaration, duplicate a name, shadow a column, exceed eight bindings and attempt `use os`. Verify each negative test.
4. Compare 220 seeded mixed programs to source programs containing the same inline constants, then 160 seeded inputs against Node's independent BigInt restricted reference.
5. Run `benchmarks/unified_relational.py` and explain why matching full-process inputs/outputs do not prove runtime speed superiority for an entire programming language.

Assessment (/10 educational only): AST/types 3, source semantics 3, adversarial testing 2, benchmark rigor 2. Scores from this course are not automatically SI project points.
