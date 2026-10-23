# SI v0.23 doctoral research notebook — table syntax and bounded static semantics

Hypothesis: an explicitly restricted typed table syntax can provide deterministic, reject-before-execute record operations while reusing the existing AxiomFlow pure monetary function engine.

Falsifiable acceptance criteria: parse and typecheck complete source before execution; 500-row and 16-column limits; deterministic sorting/projecting/summing; 400 seeded source-program landed-cost outputs agreeing with an independently written integer-cent nearest-even model; all older tests remain green; source ZIP bundles tablelang.py.

Method: direct source programs with row declarations and a single typed `landed` derivation, independent model oracle, parser negative/adversarial source tests, CLI subprocess, full Python 3.11/3.12/3.13 + Node.js 22 CI. The older independent Node.js money comparator remains an inherited regression, not new v0.23 credit.

Important limitations: the interpreter is in Python and uses the host Table API, not a fully independent language runtime; resource budgets are implementation limits, not a security sandbox; only `landed` has grammar-level derivation; no controlled workload-equivalent Python/C/C++/Java benchmark result yet. Any CI regressions must remain visible. No formal type soundness theorem, complete thesis or universal superiority claim.

Next: unify table syntax with user-defined scalar/functions, implement independent Node table evaluator and measurable feature-level reproducibility, then integrate terminal and package distribution.
