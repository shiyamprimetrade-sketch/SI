# Lesson 3 — Verify before optimizing

Prerequisites: SI v0.1 stack semantics and v0.2 compilation.

1. Draw the control-flow graph of `PUSH 0; JZ end; PUSH 4; LABEL end; HALT`.
2. Explain why the verifier rejects it: the two paths join with different stack heights.
3. Run `verify(compile_source('PUSH 4\nPRINT\nHALT'))` and inspect `max_stack_height`.
4. Run `remove_unreachable(compile_source('JMP end\nPUSH 9\nLABEL end\nHALT'))` and compare instruction counts.
5. Challenge: construct a loop with a consistent stack height at its back-edge and show why the worklist terminates.
6. Advanced: identify the assumptions needed for the observational-equivalence proof sketch and design a counterexample if jump targets were not remapped.

Pass criteria: explain the join invariant, produce a passing verifier example, and demonstrate equivalent output and steps before and after optimization.