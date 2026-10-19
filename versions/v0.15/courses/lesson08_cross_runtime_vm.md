# SI Course — Lesson 08: Independent virtual machines

## Learning outcomes
1. Describe a stack VM program counter, instruction step budget, operand stack and output buffer.
2. Explain why `BigInt` is required for exact SI integers in JavaScript.
3. Differentiate Python's `float` and JavaScript's `Number` display semantics.
4. Design differential tests with three independently structured Python engines and a Node.js engine, with explicit sampling limitations.

## Lab
- Compile `PUSH 8; PUSH 3; SUB; PRINT`, predict output and step counts, then run both runtimes.
- Explain why the result of `PUSH 0; PUSH -3; DIV; PRINT` must display `-0.0`.
- Trigger stack, step and output budgets in both runtimes and classify the errors.
- Evaluate `PUSH 9007199254740993` to demonstrate why JS `Number` alone loses integer precision.
- Construct seeded control-flow tests including LABEL and JMP/JZ branches.
- **Advanced:** compare rounding modes, non-finite rejection, and shortest round-trip float printing on extreme magnitudes.

## Coursework rubric (/10, separate from training score)
3 = correct state-machine trace; 3 = cross-runtime number handling; 2 = reproducible adversarial evidence; 2 = limitations and negative results.

A passing course exercise is not a formal theorem, peer-reviewed dissertation, or earned point in the new SI challenge.
