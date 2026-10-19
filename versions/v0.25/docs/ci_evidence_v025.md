# SI v0.25 — Verified CI, source-level conformance, and cross-runtime timing

## Parent review
Prior draft [PR #20](https://github.com/shiyamprimetrade-sketch/SI/pull/20) at `0df82d216c72ce57c4b65d43a789db7600dcee43` remained unmerged and its latest three-runtime specialized workflow [39247227589](https://github.com/shiyamprimetrade-sketch/SI/actions/runs/39247227589) completed successfully. New v0.25 is stacked on actual parent branch `si-v0.24-relational-functions-20261019`, not main.

## Tested v0.25 source
Code commit `ccd0e9e22a3d3b8ca32b002cea1e7ff385962f50`.
[GitHub Actions run 39248411993](https://github.com/shiyamprimetrade-sketch/SI/actions/runs/39248411993), workflow `.github/workflows/ci-v025.yml`:

| Runtime | GitHub job | Unittest result | Conclusion |
|---|---:|---:|---|
| Python 3.11 + Node.js 22 | 118045922927 | 402 / 402 | SUCCESS |
| Python 3.12 + Node.js 22 | 118045922505 | 402 / 402 | SUCCESS |
| Python 3.13 + Node.js 22 | 118045923074 | 402 / 402 | SUCCESS |

**1,206 passing test executions**, zero failed unittest methods and zero workflow warning annotations in the three inspected logs. Original bounded lexical obligation SHA `9997585eb832c9a59660a7ff3873c1e53a087a975b17a79198512aa36a30bd4d` reproduced across all three jobs. Both unified CLI examples, reproducible ZIP, inherited SI and pinned AxiomFlow CLI, and process-comparison benchmark ran successfully.

## What has been independently checked
- A strict unified *entrypoint* distinguishes typed scalar/function source and table source; cross-mode expressions, unbound module imports and invalid table input are rejected. This is not yet one fully merged grammar or shared type system.
- The Node.js reference parses a constrained relational source vocabulary independently and evaluates using BigInt cents. Python and JS structured outputs agree for **200 deterministically seeded source programs** and data collections (plus directed empty-filter and half-even checks). This is a finite supported subset, **not complete dual-runtime equivalence**.
- The Python batch adapter and Node evaluator consume the same JSON source/data workload. The benchmark aborts if outputs differ. The source packager includes the new CLI, JS evaluator, adapter and SHA manifest; two-build archive equality is tested.

## Output-equivalent, exploratory process wall time
40 datasets × 18 rows, 5 samples per language on each runner; results show median elapsed milliseconds for the **entire subprocess**, including interpreter startup, JSON parsing, source parsing and output serialization.

| Python CI matrix job | Python subprocess ms | Node.js subprocess ms |
|---|---:|---:|
| Python 3.11 | 75.123 | 35.041 |
| Python 3.12 | 84.191 | 36.574 |
| Python 3.13 | 50.794 | 21.351 |

**Negative/scientific qualifications:** These are **not matched engine implementations**: Node's restricted BigInt interpreter and Python's more general typed table interpreter have different functionality, startup time and optimization maturity. Five measurements and runner noise cannot prove Node/AxiomFlow superiority, let alone outperformance versus Python, Java, C or C++ across workloads. Node was faster in these precise whole-process samples; no universal comparison is warranted.

## Failure and limits
The initial PR creation request returned HTTP 422 because an incorrect parent branch name was supplied. The actual PR #20 head was independently resolved via GitHub and [PR #21](https://github.com/shiyamprimetrade-sketch/SI/pull/21) was created correctly stacked. There was no v0.25 failed specialized CI job in the inspected implementation run.

Not implemented: native scalar/table mixed-scoped AST semantics, independent full-language Node interpreter, independently proved type soundness, production shell, public hardened deployment, broad benchmarks, dissertation defense or full 100k target.
