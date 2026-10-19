# SI v0.26 — CI evidence and mixed-scope conformance audit

**Baseline:** v0.25 [draft PR #21](https://github.com/shiyamprimetrade-sketch/SI/pull/21) latest head `9851d7b077c86150bd3d090d830cde86abbb0428` and GitHub CI [run 39248774086](https://github.com/shiyamprimetrade-sketch/SI/actions/runs/39248774086) passed. v0.25 contained 402 test methods per Python version and separate scalar/table front ends. `main` remained `573cf6ea850fe72698ea2a45c6bd854b329c7357`.

## Newly implemented and tested
- `axiomflow/unified.py`: bound, immutable `let` nodes compiled into a shared `UnifiedProgram.shared_ast` tuple alongside table steps, using existing typed `Expression`/inference machinery. Up to eight pure money/scalar bindings before table input; no modules/effects, no binding/table-column shadows.
- `axiomflow/table_language.py`: typed constants in table filter/derive inference and row-local evaluation, attached to immutable `CompiledTable`. Prior scalar-only and table-only execution preserved.
- `js/relational_runtime.js`: independently implemented limited literal mixed bindings, money-threshold filters and four-place scalar multiplier derived columns. **Not** a general independent JS AxiomFlow evaluator.
- `tests/test_mixed_scopes.py`: 16 new unittest methods, including 220 seeded mixed-vs-inlined comparisons, 160 bounded seeded Python/Node source tests, static rejection, repeated execution and CLI.
- `examples/mixed_table.af`, reproducible source ZIP inclusion, terminal CLI, lesson 22 and versioned research/specification notes.

## Initial failed workflow
The initial specialized [run 39250044175](https://github.com/shiyamprimetrade-sketch/SI/actions/runs/39250044175) and PR workflow [39250095221](https://github.com/shiyamprimetrade-sketch/SI/actions/runs/39250095221) **failed** on all Python versions. In the inspected Python 3.11 log, 417 of 418 tests passed; the one failure was `test_constant_budget`: a ninth binding correctly raised an AxiomError but its diagnostic said `mixed bindings must precede table input and be bounded` rather than explicitly containing `budget`. No implementation-safety bypass was found in that failing test.

Fix commit `9ea18f14d7005c32fe071c4ddef040a1db7f7961` separates the 'binding after table' and 'mixed constant budget exceeded' errors.

## Successful full GitHub retest
[Run 39250206768](https://github.com/shiyamprimetrade-sketch/SI/actions/runs/39250206768) on code commit `9ea18f14d7005c32fe071c4ddef040a1db7f7961`:

| Python + Node 22 | GitHub job ID | Tests | Result |
|---|---:|---:|---|
| Python 3.11 | 118051862440 | 418/418 | PASS |
| Python 3.12 | 118051862664 | 418/418 | PASS |
| Python 3.13 | 118051862624 | 418/418 | PASS |

**1,254 successful test-method executions**, no failed tests or GitHub warning annotations in inspected job logs. Legacy bounded lexical digest `9997585eb832c9a59660a7ff3873c1e53a087a975b17a79198512aa36a30bd4d` reproduced, the mixed/legacy CLI, source archive and complete output-equivalent benchmark steps completed.

## Controlled output-equal bounded workload benchmark
Identical JSON: **40 source programs × 18 rows**, five full subprocess repetitions, median wall milliseconds (startup/JSON/parsing/execution all included):

| Python baseline process | Python median | Node median |
|---|---:|---:|
| Python 3.11 vs Node 22 | 41.485 ms | 20.421 ms |
| Python 3.12 vs Node 22 | 81.652 ms | 33.940 ms |
| Python 3.13 vs Node 22 | 79.968 ms | 30.714 ms |

The JS reference is narrower than the Python language runtime; therefore these are **process-specific measurements and are not cost-equivalent language or compiler performance rankings**. Different runner hardware, startup costs and process maturity materially affect timing. Node finished faster for this bounded example, not in all tasks.

## Scientific limitations
The mixed program supports only immutable pure pre-table `let` bindings, not complete first-class table types, arbitrary functions capturing mixed variables, packages or effects. The table grammar is still partially dispatched. The Node runtime implements a narrow comparator subset. No formal overall type soundness theorem, standalone terminal, general sandbox, claimed universal superiority, completed doctoral thesis or earned 100,000 milestone.
