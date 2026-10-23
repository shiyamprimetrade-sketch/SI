# SI v0.18 — Learning outcome and benchmark discipline

## What changed from v0.17
The previous v0.17 language parsed source on every evaluation call. v0.18 exposes `compile_source` (immutable top-level AST tuple) and `evaluate_compiled` (new execution environment for each run), with the existing `evaluate` as the backward-compatible parse+run function. This is an optimization of repeated evaluation workflow, not a compiler producing machine code.

## Evidence requested
- New repeat execution and no-reparse tests, including 800 seeded comparisons, plus all earlier SI and AxiomFlow suites on Python 3.11/3.12/3.13 and Node 22.
- Three-path benchmark: source parse+execute, pre-parsed AST execute and direct Python Decimal. Check identical output before timing.
- Rerun baseline under identical hardware/versions and report median values; direct Decimal is still **not cost-equivalent**.
- Report errors and regressions rather than hiding them.

## Limitations and next engineering questions
- The AST is a Python tuple but its children are not a cross-runtime serialized ABI, nor a cryptographically validated module.
- Interpreter speed is expected to lag direct arithmetic; no universal language advantage is claimed.
- Current language lacks functions, modules, static typing, full IO/effects, backend API and web apps; the 100k gate sheet names them explicitly.
- Neither project milestones nor point changes constitute an increase in neural-network knowledge or intelligence: they measure software artifacts and test evidence only.
