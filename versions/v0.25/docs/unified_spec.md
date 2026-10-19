# AxiomFlow v0.25 — Strict unified source classification and supported subset

## Source mode classifier
Given ASCII text of at most 10,000 characters and at most 100 lines, remove comments/blank lines. Empty input rejects. A complete `table <identifier> = input` line causes **table mode**. In table mode, no scalar `let` or `use` lines are allowed; remaining input uses the v0.24 `compile_table` grammar and static schema checker. Without a table declaration, any reserved table keyword causes an error; valid input must pass the prior `parse_script` and `static_check` typed scalar grammar, and `use` is restricted to the existing separately pinned project loader.

## Evaluation
- Table programs require bounded CSV bytes, use `load_rows`, execute an immutable `CompiledTable` plan, and produce structured summary/row outputs.
- Scalar programs forbid CSV bytes and use the previous typed function interpreter; they emit a list of scalar/money texts.
- Resource budgets inherit table row/source constraints, function/type limits, and the explicit classifier limits.
- Unsupported mixed-mode language features **reject**, rather than pretending v0.25 implements one fully integrated AST or bytecode. A later milestone must unify scopes and types formally.

## JS-independent implementation subset
Node.js source evaluator supports only `table t = input`, `filter t where price_usd >= <money> USD`, `derive t adjusted_usd = price_usd * 1.10`, `sort t by price_usd`, `sum t.adjusted_usd`, `select t (price_usd,adjusted_usd)`, and `emit t`; unsupported lines reject. Fixed-point arithmetic uses BigInt cents with half-even rounding. Source batches are strictly bounded.

## Verification obligations
The same 200 seeded source and rows must yield exactly equal JSON output in Python and Node on Python 3.11, 3.12, 3.13/Node 22 runners. Negative/ambiguous input must reject. The benchmark must abort if output differs. This validates a bounded subset, not full semantic equivalence.
