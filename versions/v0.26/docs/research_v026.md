# SI v0.26 — Doctoral research notebook: shared AST boundary

## Question
Can a small immutable scalar binding environment be safely and reproducibly shared by AxiomFlow typed scalar expressions and relational/table instructions without silently weakening table schema checks?

## New experiment
A single v0.26 `UnifiedProgram` can represent typed `let` AST nodes and an immutable table plan. The new mixed compiler does not dynamically execute Python source: it parses typed expression ASTs, infers types, evaluates immutable pre-table bindings and passes their typed values into both static table inference and per-record evaluation. The control limits include eight variables and capped source/CSV sizes.

For a separate oracle, compare each seeded mixed program with a legacy table source containing exactly the corresponding inline literals. A second independent Node implementation tests the documented literal-binding relational subset using integer cents and four-place fixed-point factors. Record any difference and reduce it to a small input. This is **finite differential testing**, not an exhaustive proof.

## Risk register
- Prefix expression evaluation currently occurs during compilation; although pure and bounded by source and existing integer/Decimal checks, further explicit per-expression evaluation budgets and exception normalization are required.
- The parent architecture still dispatches scalar-only and table-only programs; AxiomFlow is not yet one fully unified parser/typechecker/runtime.
- Node only covers a constrained relational/mixed program shape.
- Measured whole-process Python/Node runtime includes interpreter launch, JSON serialization, parsing and computation; controlled output equivalence does not imply equal implementation maturity.
- The 100k goal remains gated; source lines, model outputs and successive runs do not themselves constitute model self-training or general performance superiority.
- No independently reviewed thesis, public deployment security audit, full terminal or global language superiority benchmark has been completed.

## Next steps
Integrate module calls into statically verified mixed scopes, define typed table values as first-class function parameters, formalize evaluation/error semantics, add fuzz-driven shrinking for real counterexamples, and compare with production-grade baselines on identical semantic workload.
