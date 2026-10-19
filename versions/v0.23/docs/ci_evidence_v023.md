# SI v0.23 — Actual GitHub CI and executable table-source validation

## Reviewed baseline
v0.22 draft PR #18, head `19260c813b8e4ced81e2381026029567e5edd4dd`, passed its final Python 3.11–3.13 + Node.js 22 GitHub CI with **365 tests/version**. The prior initial benchmark import-path failure remained documented. v0.23 was developed as a new **stacked draft PR #19** based on v0.22 without altering main.

## Verified real CI
**Tested source commit:** `b81f4c8a6a3a9c5ed609ea6aad98e82cad15d08f`
**Workflow:** `.github/workflows/ci-v023.yml`
**GitHub Actions:** https://github.com/shiyamprimetrade-sketch/SI/actions/runs/39245695068

| Runtime | GitHub job | Unit test methods | Job result |
|---|---:|---:|---|
| Python 3.11 + Node.js 22 | 118036929641 | 376/376 | SUCCESS |
| Python 3.12 + Node.js 22 | 118036929283 | 376/376 | SUCCESS |
| Python 3.13 + Node.js 22 | 118036929490 | 376/376 | SUCCESS |

**1,128 successful test executions**, **11 new test methods/version** beyond v0.22, zero test failures and zero warning annotations in inspected logs. The original bounded lexical obligation digest `9997585eb832c9a59660a7ff3873c1e53a087a975b17a79198512aa36a30bd4d` reproduced. The table-source CLI emitted the `landed_cost_usd` output, the v0.23 deterministic source ZIP build succeeded, and previous data/ML, pinned project, SI CLI and benchmark steps passed.

## New experimental claims supported
- Table statements are **real source grammar in a restricted sublanguage**, compiled by `axiomflow.table_language.compile_table` and executed by `execute_table` or `run_table`.
- Before data execution, the compiler verifies table declaration, variable binding, schema/column validity for `select`, `sort`, `augment`, `sum`, and `emit`, source limits, unknown operations and at least one observable output.
- A bounded input is provided explicitly from the CLI `--csv`, never through a filesystem path embedded in the language source. Runtime uses immutable typed host `Table`/`Record` operations inherited from v0.22.
- 11 new unittest methods cover CLI parity, repeatable compiled execution, statically rejected unsupported statements, budgets, independent Decimal aggregates and **250 deterministic seed-23023 table-input comparisons**.
- Deterministic v0.23 source archive bundles the new table program and parser, with byte-equality and content-hash tests retained.

## Negative findings / limitations
- This is **not** table syntax merged into the previously existing scalar/function parser; a separate entrypoint is used. It remains a hosted Python runtime and is not a secure general sandbox.
- There is no new independent JavaScript table language implementation. The earlier Node fixed-cent comparison is inherited, not new v0.23 achievement.
- No new fair cost-equivalent table benchmark against Python Pandas, SQL, JS, C/C++ or Java was built. Existing benchmark telemetry is for the monetary feature pathways and cannot establish superiority of the table DSL.
- Finite conformance tests and generated corpora do not prove universal type soundness or exhaustive parser correctness.
- No public deployment, independent terminal, general dependency installer, complete defended PhD thesis, or universally superior language is claimed.

**Scoring:** new SI project before v0.23 4750/1000000; nonduplicative +700 scoped project-progress points, provisional total **5450/1000000**, leaving **94550** to the conditional 100000 milestone. Historical archive **996667/1000000** unchanged. This is a self-assessed research artifact ledger, not a metric of model intelligence or neural retraining.
