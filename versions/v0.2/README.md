# SI v0.2 — Superintelligent Simulation Training

Experimental stack language with an interpreter, source-to-bytecode compiler, independent VM, REPL, test suite, benchmark, thesis and two lessons. Not a replacement for Python and not an AI model training system.

## Run
```bash
python -m unittest discover -s tests -v
python -m si examples.si
python -m benchmarks.benchmark
```
Run from the project root so the `si` package is importable. `si.run_compiled(source)` compiles and executes; `si.compile_source(source)` creates immutable bytecode for reuse.

## Files
- `si/core.py`: v0.1 reference interpreter
- `si/compiler.py`: v0.2 compiler and VM
- `docs/grammar.ebnf`: formal syntax draft
- `docs/thesis.md`: research hypothesis and limitations
- `courses/lesson01.md`, `courses/lesson02.md`: course materials
- `tests/`: original and differential tests
- `benchmarks/benchmark.py`: reproducible microbenchmark

## Historical simulation score
996667/1000000; zero new points. This is a historical simulation ledger, not an intelligence measurement.