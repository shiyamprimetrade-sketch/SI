# SI v0.16 — Evidence-based project scoring ledger

| Ledger | Score |
|---|---:|
| Historical simulated archive | **996667 / 1000000** (unchanged) |
| New SI project at start of v0.16 | **750 / 1000000** |
| New v0.16 evidence-based self-assessed award | **+200** |
| **New SI project cumulative** | **950 / 1000000** |

## Nonduplicative +200 v0.16 award

| Incremental work | Points | Status/evidence |
|---|---:|---|
| Binary64 decimal roundtrip, bitwise preservation and signed-zero conformance tests | 100 | Seven new unittest methods in `tests/test_decimal_roundtrip.py`, 800 seeded raw patterns, exact outputs checked; [CI 39233483078](https://github.com/shiyamprimetrade-sketch/SI/actions/runs/39233483078) passed |
| Precisely scoped **AxiomFlow language proposal** with falsifiable hypotheses and fair evaluation baselines | 50 | `docs/language_proposal.md`; proposal only, no compiler/runtime achievement claimed |
| Learning module 12 | 25 | `courses/lesson12_decimal_and_language_design.md` |
| Scientific research note and reproducible negative findings | 25 | `docs/research_v016.md` and `docs/ci_evidence_v016.md` |
| **Total newly credited** | **200** | Other inherited CI/IEEE tests get 0 new points |

## Verified CI
Code commit `6e61f4a8c7097877454545c13b3d6ff7ab7ffc83`.
- Python 3.11 with Node 22: **272/272** tests, job 117996839869.
- Python 3.12 with Node 22: **272/272**, job 117996840331.
- Python 3.13 with Node 22: **272/272**, job 117996840198.
- **816 passing unittest executions**, zero workflow warnings in examined job logs. Inherited lexical digest was identical across jobs.

## Deductions, cautions and interpretation
- **0 new points** for rerunning inherited CI, existing binary64 checks or v0.15 rounding checker.
- **0 points** for constructing an AxiomFlow compiler, benchmarking AxiomFlow, or creating an AxiomFlow terminal: none has been built in this cycle.
- The lexical character-deletion check in v0.16 is exploratory and does **not assert a globally shortest-decimal property**. Passing test count must not be advertised as proving shortest representation.
- Shortest-decimal tests compare against CPython's numeric output and may share runtime-level behavior; no all-input theorem was verified.
- The +200 award is a **subjective, provisional self-assessed project progress score** under the user's stated rubric, not a measurement of assistant intelligence or weights, and not external peer review.
