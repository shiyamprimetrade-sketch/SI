# SI v0.23 — Research notebook: from host APIs to executable table source

## Hypothesis
The bounded typed-table API introduced in v0.22 can be exposed as a declarative source language with independently testable static schema constraints and deterministic operational semantics without permitting arbitrary code execution.

## New falsifiable tests
- Executable `.af` source, source compiler and CLI: schema-correct transform, stable sort, typed Decimal sum, reproducible JSON.
- Invalid source syntax and unsafe operations (file path inside source, implicit `eval`, undeclared table, unknown/projected-away columns, over-budget script) rejected *before* any table operation.
- 250 deterministic seed 23023 table-input datasets checked against **independent Decimal landed-cost oracle**; full inherited AxiomFlow/SI tests and independent Node cents corpus also run.
- Source archive reproducibility checks include the new table program and module. Multi-version Python 3.11–3.13 + Node.js 22 CI is authoritative.

## Critical scope and negative findings
The new table language is a **separate restricted entrypoint**, not a grammar merge into the scalar/program function language. Table runtime and input pipeline remain Python-hosted; no independent Node parser or table executor. Parsing/source validation is separate from secure process isolation. Benchmarks inherited from v0.22 compare unequal execution paths and cannot demonstrate cross-language performance superiority. No large-scale SQL/Pandas/Java/C++ baseline, independent timing error bars, full terminal, package registry, defended doctoral thesis, or 100k score milestone is established.

## Next testable steps
Integrate language grammars with explicit type/effect annotations and a shared bytecode IR; add an independent table interpreter; formalize relational type preservation; test joins, filtering, and resource budgets; design fair matching table baseline experiments against Python Pandas/SQL/JS. Publish failures and counterexamples with seeds. Award no points for repeated inherited tests.
