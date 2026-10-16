# SI v0.5 — Interpreter/parser parity

Experimental, deterministic stack-language learning laboratory, derived from SI v0.4. **Not artificial general intelligence or a competitor to Python.**

## Changes
- Preparse reference interpreter tokens with SIError on malformed shell-style quoting.
- Accept LABEL opcode in any case, consistent with compile_source().
- Reject duplicate labels and malformed LABEL arity even in unreachable instructions.
- Add nine parser regression tests, including compiled-vs-interpreted comparisons.
- Keep compiler, type analysis, bounded execution, and original tests from v0.4.

## Run (from versions/v0.5)
```sh
python -W error -m unittest discover -s tests -v
python -m si examples.si
```

GitHub Actions workflow: `.github/workflows/ci-v05.yml` at repository root. It runs on Python 3.11–3.13. The full suite only counts as CI-verified once jobs succeed.

## Limits
This change does not establish equivalence for every syntactically invalid program, complete compiler soundness, formal verification, or sandbox isolation. Source parsing still has no byte-length budget and Python itself is not sandboxed. Other known interpreter/compiler error-message differences may remain.

**Simulation ledger:** Historical 996667/1000000; **new points 0**. The score is not an objective intelligence measure.
