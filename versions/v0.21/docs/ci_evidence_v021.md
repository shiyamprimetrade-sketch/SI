# SI v0.21 — Verified GitHub data/ML interoperability evidence

## Baseline
v0.20 draft PR #16, final commit `6525f7a56526fe6cd020b9f205a03096b0c1382d`, verified 335/335 tests on each Python 3.11/3.12/3.13 with Node.js 22. v0.21 stacked on that unmerged branch. Main remains untouched.

## Tested code
GitHub commit `98d5c8c0614706f9b3d9191403b777f21361141e`.
[GitHub Actions push run 39242469581](https://github.com/shiyamprimetrade-sketch/SI/actions/runs/39242469581):
| Runtime | Job | Tests | Outcome |
|---|---:|---:|---|
| Python 3.11 + Node.js 22 | 118026339374 | 348/348 | PASS |
| Python 3.12 + Node.js 22 | 118026338727 | 348/348 | PASS |
| Python 3.13 + Node.js 22 | 118026339207 | 348/348 | PASS |

**1,044 successful test executions** (13 more test methods/version than v0.20); no failed unittest methods or GitHub warning annotations in inspected job logs. Existing bounded source lexing digest `9997585eb832c9a59660a7ff3873c1e53a087a975b17a79198512aa36a30bd4d` reproduced across all jobs.

## Concrete data/ML example
CLI: `python -m axiomflow.data data/landed_cost.csv`.
- 9 synthetic rows, ordered train/test split **6 / 3**.
- AxiomFlow's *existing statically checked typed monetary function* provides the cent-rounded `landed_cost` feature.
- Independent `decimal.Decimal` oracle checks the feature, including **400 seeded examples** in tests.
- Decimal one-feature OLS fit: slope **2**, intercept **5.00**, test MAE **0.00** on the synthetic known-linear dataset.
- CSV SHA256: `22c3acffb92bcd05d567bbb6933a08181432dd1b2e99af30989c15d6eba00fef`.
- This is a deliberately constructed demonstration, **not real predictive performance**, general ML training or a native AxiomFlow ML runtime.

## Reproducible limited source packaging
`python -m tools.package_source --output /tmp/axiomflow-v021.zip` created a deterministic 13-file source bundle with canonical SHA manifest. Run digest: `486959d13fb12818c50882701653e70b3b592f64216f814a46244de22b5b7ebd`. Automated tests build twice and check identical ZIP bytes, manifest digests and no traversal in archive paths. No signed binary, pip wheel or complete package registry is claimed.

## Benchmark finding — NOT cost-equivalent
`python benchmarks/compare_features.py --iterations 100 --repeats 3` verifies the same outputs on four price/rate values then reports illustrative medians. Python 3.11 GitHub runner:
- Reparse/typecheck/evaluate AxiomFlow: **58,104.97 ns/call**.
- Direct Python Decimal reference: **1,954.15 ns/call**.

This shows **considerable current AxiomFlow overhead**, not superiority. Direct Decimal does not perform AxiomFlow parsing or typechecking. Three repeats, small artificial inputs and runner noise cannot sustain broad speed or productivity conclusions.

## Scientific and engineering limitations
No actual GPU/trained general ML model, TensorFlow/PyTorch bridge, held-out external dataset, production inference API, independently written ML engine, general AxiomFlow dataframe types, security sandbox or fair comparison with Python, C, C++, Java and JavaScript. The HTTP/frontend from v0.20 remain local-only.

Self-assessed project +650 points is provisionally awarded only for new scoped work. Cumulative new SI project **3950 / 1000000**; conditional 100k checkpoint requires **96050** more evidence-based points. Historical archive **996667 / 1000000** unchanged; no increase in underlying model intelligence is claimed.
