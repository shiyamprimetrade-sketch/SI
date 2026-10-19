# AxiomFlow v0.24 — Bounded relational tables with scalar/function integration

## Grammar delta
Before `table t = input`, a program may declare pure scalar or money functions using the existing `fn name(x: USD) -> USD = expression` syntax. The table schema is `price_usd: USD`, `rate: scalar`, `observed_cost_usd: USD`.

- `filter t where column >= expression` (operators `== != < <= > >=`): the column must exist and the expression's inferred type must match its declared type. A pure expression may refer to row columns and previously declared functions.
- `derive t new_column = expression`: adds one new statically inferred typed column. Existing names cannot be replaced, and the column budget is 16.
- Existing `select`, `sort`, `augment`, `sum`, and `emit` continue as in v0.23, with the schema updated after each operation.

All code is completely parsed and statically checked before table row execution; unknown names/functions, incompatible money/scalar operations, malformed syntax and recursive functions are rejected. The v0.24 interpreter evaluates expression syntax with the existing typed AxiomFlow `Expression`, `infer` and `execute_expression` machinery. This is integration, not a new independent optimizing compiler.

## Semantics
Filtering retains input rows in their original order, unless `sort` is requested. Derived expressions are evaluated per row against fresh typed records and pure function environments; no file access or Python `eval`. Monetary operations retain half-even cent rounding and `Decimal` arithmetic. A derived money result is rendered with two fractional digits and its declared currency.

Bounded resource limits: ASCII source up to 10,000 chars, 100 source lines and statement steps, 30 functions, 16 typed columns, 500 table input/output rows and existing 100 KB CSV input. Compile first, then validated data execution. Table operations still use Python host records; the new source grammar calls those host APIs.

## Positive demonstration
```text
fn uplift(x: USD) -> USD = x * 1.10
table t = input
filter t where price_usd >= 120.00 USD
derive t adjusted_usd = uplift(price_usd)
sort t by adjusted_usd
sum t.adjusted_usd
select t (price_usd,adjusted_usd)
emit t
```
Run from `versions/v0.24`:
`python -m axiomflow.table_language examples/filtered_table.af --csv data/landed_cost.csv`.

## Scientific limits
Node.js reference `js/table_reference.js` implements independently bounded **filtering and uplift fixed-point cents** rather than all of AxiomFlow syntax or full static typing. Table operations are not yet an independently compiled machine-native language. Passing finite tests is not a formal proof of equivalence or language speed superiority.
