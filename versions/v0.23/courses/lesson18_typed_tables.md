# SI course lesson 18 — Immutable typed tables and compile-once execution

## Outcomes
Describe table schema and record invariants, stable sorting, column projection, exact Decimal aggregation, half-even monetary feature creation and the distinction between source compilation and host API operations.

## Lab
1. Load the nine-row CSV fixture via `load_rows` then `from_validated_csv_rows`. Inspect schema `(USD,scalar,USD)`, immutability and bounded size.
2. Project `rate` and `price_usd` in different order, then stably sort by price. Explain why input records remain untouched.
3. Augment records with `landed_cost_usd`. Verify each value against the independent Decimal oracle.
4. Test a currency/schema mismatch, malformed record, nonfinite decimal, and duplicate column name and document the rejection.
5. Execute 400 seeded price/rate examples with both old parse/typecheck and compiled function execution, and compare with Node BigInt cents on 250 seeded inputs.
6. Benchmark the three pathways with the same outputs. Explain why direct Python Decimal avoids interpreter overhead and therefore is *not* a matched execution-cost comparison.

Assessment (/10): schema and invariants 3, numerical parity 3, reproducibility 2, honest benchmark limitations 2. Course points not automatically credited as SI project points.
