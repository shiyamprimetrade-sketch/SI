# AxiomFlow v0.23 — Executable typed table sublanguage v1

The table program is line-oriented ASCII, max 10,000 source characters, max 100 lines. Trailing `#` comments and blank lines allowed; all other syntax rejected. Syntax:

```ebnf
program = "table" name "=" "input" { statement } ;
statement = "augment" name "landed_cost_usd"
          | "select" name "(" column { "," column } ")"
          | "sort" name "by" column
          | "sum" name "." column
          | "emit" name ;
name,column = /[a-z_][a-z0-9_]*/ ;
```

The compiled plan is a frozen dataclass holding a tuple of operations and final schema/type tuple. Exactly one initial declaration, and at least one `sum` or `emit`, are required. Only the declared table variable is valid. Column names and order are checked at parse/compile time. `augment` adds the USD landed-cost column only when the table currently has the original fixed schema `price_usd:USD, rate:scalar, observed_cost_usd:USD`. `select` permits nonempty unique existing names; `sort` uses a stable numeric ascending order. `sum` emits a typed value; `emit` returns column/type labels and up to 500 bounded records. Decimal finite checks and strict CSV validation originate in existing `axiomflow.data` and `axiomflow.table`.

`table t=input` receives an explicit host validated CSV table, **never an implicit filesystem path**. The CLI accepts only the source path and `--csv` path. No dynamic script import, arbitrary expression evaluation, networking, loops, SQL joins, data mutation, variable rebinding or unbounded record creation. Existing mathematical rounding is inherited from the v0.22 compiled AxiomFlow function and independently checked with Decimal/Node limited fixed-point oracle.

**Scope:** This is *real parsed and executable AxiomFlow table source syntax* implemented in a new entrypoint. It is **not integrated** into the original AxiomFlow monetary-expression parser, and it remains hosted in Python. No production security isolation or formal soundness proof is claimed.
