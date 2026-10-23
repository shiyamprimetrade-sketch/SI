# AxiomFlow Lesson 14 — Parse once, execute repeatedly

The difference between an interpreter that parses every invocation and a reusable parsed expression tree matters for developer workflows and benchmark fairness.

**Exercise 1:** Trace the v0.17 `evaluate` source path and list repeated steps.

**Exercise 2:** Use `program = compile_source("emit (1.00 USD+2.00 USD)*2")`; then call `evaluate_compiled(program)` repeatedly. Show how fresh environments prevent binding leaks.

**Exercise 3:** Compare source evaluation and compiled-AST execution against direct Python Decimal arithmetic. Explain why only the first two implement the *same AxiomFlow semantics*, and why direct Decimal is not cost-equivalent.

**Exercise 4:** Add a seeded differential corpus and a negative syntax case that must be rejected before execution.

**Assessment /10:** semantics 3, reproducibility 3, benchmark fairness 3, scientific limitations 1. Educational course points are not SI project score.
