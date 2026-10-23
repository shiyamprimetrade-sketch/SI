# AxiomFlow v0.23 restricted executable table grammar

Syntax (ASCII identifiers and case-sensitive keywords):
```
program := (declaration | row | derive | sort | select | sum | comment | blank)*
declaration := "table" identifier "(" field ("," field)* ")"
field := identifier ":" ("USD" | "scalar")
row := "row" identifier "(" typed_literal ("," typed_literal)* ")"
typed_literal := fixed_2_cent_decimal "USD" | scalar_decimal
derive := "derive" identifier identifier ":" "USD" "="
          "landed(" price_USD_column "," rate_scalar_column ")"
sort := "sort" identifier "by" existing_column
select := "select" identifier existing_column ("," existing_column)*
sum := "sum" identifier existing_column
```

Static checker verifies field uniqueness and types, existing table and columns, exact row arity, USD literals to 2 places, bounded scalar literals, derived operation requiring USD price and scalar rate, no post-derive `row` statements and all commands prior to any execution. Execution creates fresh immutable Table/Record snapshots, never mutates prior versions. Sorting is stable; output is JSON with ordered rows/columns and string-form Decimal values. Derivation uses cached, statically checked `feature_precompiled` from the existing AxiomFlow typed-function engine.

Limitations: only one hardcoded derived pure function `landed`, no language-level arbitrary functions, no joins, aggregations beyond sum, no external file/network effects or unbounded loops. This is **language syntax plus interpreter**, but not a shared AST/parser with the original scalar/function grammar.
