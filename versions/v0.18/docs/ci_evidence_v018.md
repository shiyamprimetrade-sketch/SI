# SI v0.18 — GitHub CI and benchmark audit

**Code commit:** `65feb3db6b338d2e886c27244c83cc54cd932996`.
**Workflow:** `.github/workflows/ci-v018.yml`.
**GitHub Actions:** https://github.com/shiyamprimetrade-sketch/SI/actions/runs/39238016230

| Python | GitHub job ID | Unit tests | Result |
|---|---:|---:|---|
| 3.11 | 118011729431 | 295/295 | SUCCESS |
| 3.12 | 118011730122 | 295/295 | SUCCESS |
| 3.13 | 118011729702 | 295/295 | SUCCESS |

**885 successful unittest executions** across Python 3.11, 3.12, 3.13 with Node.js 22. The inspected job logs contain no unittest failures or GitHub workflow warnings. The inherited lexical obligation digest `9997585eb832c9a59660a7ff3873c1e53a087a975b17a79198512aa36a30bd4d` reproduced in all jobs. SI CLI and AxiomFlow file example both succeeded in the completed workflow.

## Benchmark result
Measured via `python benchmarks/compare_decimal.py --iterations 200 --repeats 3` on distinct GitHub-hosted Ubuntu runners; data are approximate medians of three repeats, **not controlled independent evidence of performance dominance**.

| Python | Parse+execute ns | Preparsed execute ns | Direct Decimal ns |
|---|---:|---:|---:|
| 3.11.17 | 20215.94 | 8184.40 | 1357.34 |
| 3.12.15 | 18142.33 | 7559.49 | 1175.32 |
| 3.13.16 | 17282.95 | 7621.69 | 1320.61 |

AxiomFlow pre-parsed AST execution is about 2.3–2.5× faster than repeatedly parsing **for this particular script on these runs**. This is a self-comparison, not a claim to beat Python; Python Decimal direct remains significantly faster in the measurements. The baseline has a different semantic and interpretation cost, so no fair cross-language throughput ranking has been established.

## New v0.18 deliverables
- `compile_source` separates source parsing from AST evaluation.
- `evaluate_compiled` uses new bindings and output list each run; checks structural tuple container but does **not** securely deserialize bytecode.
- Eight new tests include no-reparse monkeypatch, repeated execution, invalid statement types, 800 deterministic comparisons, and explicit syntax error checks.
- `docs/milestone_100k.md` defines cumulative, conditional point gates up to 100,000.
- New research and course notes document limits and next milestones.

## Caveats
No typed function or module implementation has been delivered yet, and there is no security sandbox, completed backend/frontend/ML SDK, terminal replacement, standalone dependency compiler, thesis defense, or demonstrated across-the-board language superiority.

**Score:** user-authorized self-assessed +300 new project points, 1,700/1,000,000 total; historical archive 996667/1000000 unchanged.
