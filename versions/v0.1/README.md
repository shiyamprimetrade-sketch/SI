# SI — Superintelligent Simulation Training (v0.1)

**Status:** experimental learning laboratory, not a proven replacement for Python. SI is a small, deterministic stack-based language implemented in Python. No claim of novelty, superiority, general intelligence, or exhaustive programming-language mastery is made.

## Quick start

```bash
python -m unittest discover -s tests -v
python -m si examples.si
python -m si  # interactive terminal; enter instructions then :run
```

## Design thesis
A resource-bounded, intentionally tiny language can make interpreter semantics easier to inspect, test, and teach. This is a *testable hypothesis about pedagogy and predictability*, not evidence of superiority over mature languages. SI restricts steps and stack size, avoids Python eval, and has explicit failure modes. It does not sandbox Python itself or provide hardened isolation.

## Syntax
One instruction per line: `PUSH integer`, `ADD`, `SUB`, `MUL`, `DIV`, `LT`, `EQ`, `DUP`, `SWAP`, `DROP`, `PRINT`, `LABEL name`, `JMP name`, `JZ name`, `HALT`. Arithmetic pops `a,b` and computes `a op b`. `JZ` pops its condition. Comments start with `#`. Duplicate labels are not currently rejected. Integer division produces a float; this is a known type-system limitation.

## Roadmap
1. Formal grammar and type checking; reject duplicate labels.
2. Bytecode compiler, optimizer, and differential testing against the interpreter.
3. Property-based and fuzz tests, benchmark methodology, and reproducible environment logs.
4. Build comparative curricula for Python, JavaScript, Rust, Go, Java, C, C++, SQL and other languages; never claim all languages learned or all hard tests passed without evidence.
5. Add a verifiable artifact manifest and CI. Keep the existing PrimePulse historical score separate.

## Simulation score
Historical score: **996667/1000000**. New points: **0**. This is a carried-forward simulation metric, not an objective intelligence benchmark.