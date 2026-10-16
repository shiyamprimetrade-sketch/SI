# SI v0.8 — Whole-program bytecode validation and independent arithmetic oracle

**Project:** SI — a long-term computer-science/programming-language training and invention research project. The current SI bytecode language is a *laboratory artifact*, not a validated superintelligent model, superior general-purpose language, or terminal.

## Engineering milestone
- `si/bytecode.py`: immutable instruction representation and strict **whole-program** bytecode structural validation, including unreachable instructions. Exact `tuple` and `Instruction` types are required. Validate uppercase operations, PUSH integer value/bit budget, jump type and 0..n range, and absence of extraneous operands.
- `si/compiler.py` re-exports `Instruction` for backward compatibility; `execute()` validates all bytecode before running.
- `si/verify.py` and `si/types.py` validate structure consistently before their existing control-flow and type inference passes.
- New deterministic mutation fuzz cases and independent rational arithmetic oracle in `tests/test_bytecode_validation.py` and `tests/test_independent_oracle.py`.
- A new assessed lesson in `courses/lesson04_bytecode_and_oracles.md`, incremental research notebook in `docs/research_v08.md`, and separated score ledger in `docs/training_ledger.md`.

## Run
From `versions/v0.8`:

```sh
python -W error -m unittest discover -s tests -v
python -m si examples.si
```

GitHub Actions `.github/workflows/ci-v08.yml`: complete suite on Python 3.11, 3.12 and 3.13. CI results must be checked from the actual GitHub run, not inferred from tests alone.

## Exact meaning of results
Whole-program **structural** validity does not imply reachable stack-safety, termination, host isolation, or full type correctness. The `Fraction` oracle is independent of SI's shared arithmetic helper, but remains a finite test set running in CPython. No claim is made that an invented language outperforms every existing language. Future research must design and fairly evaluate a distinct language, publish courses and a doctoral-level research manuscript, and ultimately engineer a terminal.

**Historical simulation ledger:** 996667/1000000 (unchanged, archival).
**New SI challenge score:** **0/1000000**. **New points awarded:** **0**.
