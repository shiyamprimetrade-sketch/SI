# SI v0.9 — Research Notebook: Small-Step Semantics and Conformance

**Category:** doctoral-level research *preparation* (not a completed, examined PhD thesis). **Date:** 2026-10-16. **Project:** SI training and future language invention.

## Research question and falsifiable claims

**RQ1.** Can the current educational SI language's execution be described precisely enough that an independently written small-step evaluator agrees with two existing engines on reproducible bounded programs?

**RQ2.** What host-level assumptions and corner cases prevent a straightforward mathematical model from faithfully describing Python-based SI, and how should they be recorded?

**Hypothesis H1 (finite):** For a fixed documented domain of valid bounded SI programs, all three implementations agree on printed output, final stack, and executed-instruction count.

**Hypothesis H2 (finite):** For selected malformed programs and resource-limit conditions, model and production engines produce the appropriate `SIError` class without leaking unrelated Python exceptions.

**Hypothesis H3 (specific):** The rational-number model, corrected for signed zero and supplemented with host semantics for float inputs, reproduces selected observable binary64 results. This is narrower than full floating-point equivalence.

## Source-level baseline

The SI v0.8 source and PR #4 provide: `run()` reference interpreter, bytecode `compile_source()/execute()`, `si.limits.apply_binary`, and strict structural preflight. Earlier GitHub Actions run 38899036262 reported 130 passing test methods each on Python 3.11, 3.12 and 3.13. Successful tests are a baseline, not proof that the v0.8 system is mathematically correct.

## Methods, reproducibility, and independence

- Working operational rules and error categories: `docs/operational_semantics.md`.
- Independently implemented source lexer/prevalidation and execution: `si/reference.py`. It does **not** import SI core, compiler, bytecode VM, or common `apply_binary`.
- Shared unavoidable host/policy components: Python `shlex`, `int`, `str`, float runtime, `SIError`, and fixed limit constants. The evaluator is logically separate, but not a separate programming-language runtime.
- Conformance program corpus: `tests/test_semantics_v09.py`, including exhaustive small-integer cases, seeded arithmetic and control-flow, loops, negative zero, malformations, and budget boundaries.
- Fixed seeds: 20261017 (arithmetic), 72207 (branching), 406 (comment metamorphism). Use the full GitHub commit SHA and Python version for reproduction.
- GitHub CI on Python 3.11/3.12/3.13; never infer success before inspecting each job.

## Early counterexample and correction

A naïve `Fraction(0, -3)` oracle converts to `0.0`, whereas the existing interpreter's integer true division produces `-0.0`. This difference matters when `PRINT` renders the value and violates a literal output conformance claim. The independent evaluator retains negative zero for integer-only true division of zero by a negative divisor. For mixed float operations it uses direct host operators to keep the sign and rounding behavior, explicitly limiting the oracle's independence.

## Anticipated limitations

1. Finite tests cannot prove universal conformance. Formal induction over all SI instructions would still need verified premises about arithmetic and stack/resources.
2. Operational semantics are partly host-defined: `shlex`, decimal-int parsing, Unicode line splitting, float rounding, `str(float)`, and errors. A future portable language should specify these completely and implement independent conformance engines in different languages.
3. The immutable reference evaluator is a simple specification, not an optimized implementation. Its performance is not evidence for superior language design.
4. Resource budgets are policy constraints, not OS-level memory/time isolation.
5. A technical research notebook and course lesson do not amount to an invented programming language, scientific proof of outperforming all other languages, a doctoral defense, or a new terminal.

## Long-term staged invention agenda

- v1: recoverable grammar, typed intermediate representation, explicitly testable runtime semantics, diagnostics, property-based testing and proof obligations.
- Comparative research: sample representative programming-language paradigms and real application tasks; report negative outcomes and benchmarks in reproducible environments.
- Invention phase: give a *new, distinct language* a name and define measurable application-specific goals before implementing its compiler, runtime, package/developer tooling and tests.
- Education phase: complete full courses with projects, solutions, assessment and documented prerequisites; independent learner evaluation.
- Research phase: prepare a thesis-length technical manuscript with literature review, original claims, formal results where possible, experiments, baselines, threats to validity and reproducibility artifacts.
- Final engineering phase: design and implement a terminal with practical workflows and user testing.

## Result accounting

New SI mission score: **0/1,000,000**, awards **0** pending an approved rubric. Historical simulation ledger: **996,667/1,000,000** preserved separately. All experimental observations must be recorded before conclusions are updated.