# AxiomFlow v0.26 — Bounded mixed-scope AST and semantics

## Grammar fragment
```
program := binding* function* table_decl table_operation+
binding := "let" identifier "=" pure_typed_expression
table_decl := "table" identifier "=" "input"
table_operation := filter | derive | select | sort | augment | sum | emit
```

Bindings may appear prior to table declaration, interleaved only with already supported function definitions in the remaining table grammar; the v0.26 compiler strips and statically checks `let` bindings before passing the remaining source to the table compiler. No module imports are permitted. The compiled `UnifiedProgram` holds an immutable tuple of AST binding nodes and table steps. **The parser paths are partially shared, not yet one grammar parser for all constructs.**

## Static and execution rules
- At most eight pre-table bindings, at most 100 input source lines and 10,000 characters; input CSV limited to 100 KB and 500 rows under existing parser.
- Each bound expression is parsed using `typed.Expression`, statically inferred using `typed.infer`, and evaluated once in lexical binding order under 50-digit Decimal, half-even rounding; no I/O.
- Duplicate names, binding/column shadowing, invalid types, nonexistent variables, late `let` statements, `use` imports and unsupported effects are rejected before the table emits output.
- Constants are attached to the compiled table plan and are available when inferring/evaluating `filter` and `derive` expressions. Column values retain precedence at runtime but collision is disallowed statically.
- Scalar-only source still dispatches to the prior typed scalar compiler/executor. Table-only source follows the old table evaluator. Earlier version directories are never altered.

## Independent JS subset
The bounded Node reference accepts `let min_price = <money-literal>`, `let multiplier = <nonnegative scalar literal with <=4 decimals>`, the existing table input and the constrained `filter t where price_usd >= min_price` / `derive t adjusted_usd = price_usd * multiplier` benchmark workflow. BigInt money cents and 1/10000 scalar arithmetic remain independent. Other AxiomFlow effects, arbitrary function bodies, general relational predicates and full mixed AST are **not** yet implemented in JS.

## Evidence obligations and negative results
- New mixed programs must agree with their corresponding literal-inlined forms for deterministic bounded seeded cases.
- Matching Node programs must produce structurally identical output, including sorting, sum values, rows, types and original input stability.
- Existing scalar-only and table-only test suites must remain green.
- No general static soundness theorem, shell isolation, general JS runtime equivalence or overall superiority is claimed.
