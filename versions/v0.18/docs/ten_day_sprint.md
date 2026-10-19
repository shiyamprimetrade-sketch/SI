# SI — 10-day delivery sprint (19–29 October 2026)

## Contract
Produce a working documented AxiomFlow **alpha**, runnable terminal/CLI, a sample application and accessible integration demonstrations, reproducible comparisons, tests, a course and a **thesis-style technical research report**. A real PhD and a proof that a new language is better than **every other language at every task** are not realistically certifiable on this timeline; do not make such claims.

| Day | Date | Target and independent exit criterion |
|---|---|---|
| 1 | Oct 19 | AxiomFlow subset lexer/parser/interpreter, typed Decimal/money, CLI, tests, GitHub CI |
| 2 | Oct 20 | Normative grammar, error taxonomy, fuzzing and static type-checking prototype |
| 3 | Oct 21 | Terminal usability: interactive help, history, debugger and exit codes |
| 4 | Oct 22 | Function/module support and an explicit dependency manifest with deterministic resolution |
| 5 | Oct 23 | Narrow API/backend integration + JSON interchange with tests |
| 6 | Oct 24 | Frontend and a working browser-accessible example |
| 7 | Oct 25 | Numeric/ML *data pipeline interoperability* example, not a new competitive ML framework |
| 8 | Oct 26 | Reproducible Python/JS/C/C++/Java baselines on **semantically equivalent** workloads, with versions, repeats, variance, memory |
| 9 | Oct 27 | Course modules and reproducible thesis-style manuscript |
| 10 | Oct 28–29 | Packaging, installation, terminal demonstration, release candidate, full CI and known-issues register |

**Prioritize vertical-slice completion over unsupported universal superiority.** Individual gates require runnable artifacts and independently inspectable evidence. Mark incomplete gates incomplete. Earlier SI versions and `main` remain untouched; stack new draft PRs without merging.

## Benchmarks and scientific claims
Correctness, typing, ease of use, compile/startup time, execution speed, memory, dependency setup, API integration and deployment are different dimensions. Compare like-for-like implementations, list hardware, OS, CPU, runtime flags, toolchain versions, warmups, repeats, confidence intervals and negative results. AxiomFlow prototype is hosted on CPython, so outperforming optimized native C/C++ *in every aspect* is not an evidence-backed claim.

## Scoring
Carry forward new SI project's subjective score **950/1,000,000** and historical archive **996667/1000000** separately. Award incremental progress points only after code and GitHub CI are verified; do not double count inherited regression work.
