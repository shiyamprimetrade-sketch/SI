# SI v0.9 — Operational semantics and independently implemented reference evaluator

**Status:** experimental stage of the new comprehensive SI programming-language, computer-science training and future invention mission. The existing SI stack language remains a learning laboratory, not a validated superintelligent system or newly proven superior language.

## Deliverables

- `docs/operational_semantics.md` — bounded, explicit small-step state machine and error rules, including `LABEL`, jumps, step budgets, signed zero and runtime limits.
- `si/reference.py` — independently implemented source parser and immutable transition-machine evaluator, using `fractions.Fraction` for integer arithmetic without importing the SI compiler, interpreter or `apply_binary` helper.
- `tests/test_semantics_v09.py` — 42 conformance test methods comparing **reference, interpreter and VM**: arithmetic, branches, loops, malformed source, resource limits, negative zero, immutable transitions, exhaustive small values, seeded random samples, and metamorphic comments.
- `courses/lesson05_operational_semantics.md` — computer-science course lesson, labs and grading rubric.
- `docs/research_v09.md` — PhD-level research *preparation*, hypotheses, evidence criteria, negative findings, threats to validity and staged language/terminal invention agenda.
- `docs/training_ledger.md` — separate historical score and reset new SI challenge score.

## Run

From `versions/v0.9`:

```sh
python -W error -m unittest discover -s tests -v
python -m si examples.si
```

GitHub Actions `.github/workflows/ci-v09.yml` runs on Python 3.11, 3.12 and 3.13. Its results must be checked separately; no run is deemed passing from the presence of tests alone.

## Evidence boundaries

The finite conformance suite is **not a formal proof** or secure execution sandbox. `Fraction` independently implements integer arithmetic but relies on CPython and uses host operators for floating values. Step semantics model the existing implementation; they do not yet define an independently portable language specification. No peer-reviewed thesis, universal cross-language superiority claim, terminal product or SI graduation is asserted.

**New SI challenge: 0/1,000,000, 0 new awarded points. Historical archive: 996,667/1,000,000, unchanged.**