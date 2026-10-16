# Lesson 2 — Compilation and differential testing

1. Read `docs/grammar.ebnf` and locate the `PUSH` and `JMP` productions.
2. Compile `PUSH 2\nPUSH 3\nADD` with `compile_source`; inspect the resulting immutable instruction tuple.
3. Compare `run(source)` with `run_compiled(source)` for stack and output. Why can the `steps` values differ?
4. Write a countdown loop and test it in both engines.
5. Challenge: design a generator for valid stack programs, then shrink any counterexample. Explain why random tests are evidence, not a mathematical proof.
6. Research exercise: compare stack machines with register machines and write down a falsifiable performance hypothesis.

Assessment: provide a test log, reproducible seed, expected behavior, and one documented limitation.