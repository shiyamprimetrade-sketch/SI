# SI Course, Lesson 05 — Operational Semantics and Conformance Testing

**Track:** computer-science theory → programming-language engineering → doctoral-level research methods. **Prerequisites:** lessons 01–04; Python stacks, algebra, code paths, and unit tests.

## Competencies

1. Distinguish a programming language's **syntax**, **static constraints**, **dynamic small-step semantics**, and **host-runtime assumptions**.
2. Represent a machine using an explicit state and a deterministic transition relation.
3. Compute an execution trace with conditional branches, stack mutations, termination, and step budgets.
4. Build an independently implemented reference interpreter and compare it against two existing engines.
5. Explain why successful finite conformance tests do not constitute a soundness or universality proof.

## Lecture 1 — From source to an abstract machine

Read `docs/operational_semantics.md`. The SI source `PUSH 3; DUP; ADD; PRINT` maps to operations in which stack top is on the right. At the start, `<pc=0, S=[], O=[], steps=0>`. The four transitions are:

1. `PUSH 3` → `<1, [3], [], 1>`
2. `DUP` → `<2, [3,3], [], 2>`
3. `ADD` → `<3, [6], [], 3>`
4. `PRINT` → `<4, [], ['6'], 4>`, terminal by reaching program end.

Formalizing state makes resource accounting, errors and control flow testable. The reference module `si/reference.py` exposes `assemble`, immutable `Machine`, `transition`, and `evaluate`.

## Lecture 2 — Branches, loops, and reachability

`JZ target` *pops* the condition regardless of whether it branches. The jump lands at the target `LABEL`, and executing `LABEL` consumes one step. Try `PUSH 0; JZ yes; PUSH 9; LABEL yes; PUSH 7; PRINT`; trace program counter changes and verify output `7`. Include `HALT` and dead code; recognize the difference between **static validation** of all instructions and **dynamic execution** of reachable instructions.

## Lecture 3 — A genuinely independent oracle (within limits)

The production interpreter and VM share a numeric helper, so matching each other could conceal the same mistake. The reference model parses source independently and uses `fractions.Fraction` for integer arithmetic before converting division into binary64. Consider the counterexample `PUSH 0; PUSH -3; DIV; PRINT`: an exact fraction loses the sign of zero, so the model must explicitly preserve observable `-0.0`. Operations involving floats use host Python arithmetic to retain IEEE behavior; independence is therefore incomplete and disclosed.

## Laboratory

From `versions/v0.9`, run:

```bash
python -W error -m unittest discover -s tests -v
python -m si examples.si
```

In a Python session:

```python
from si.reference import assemble, Machine, transition, evaluate
program = assemble('PUSH 3\nDUP\nADD\nPRINT')
state = Machine()
while state.pc < len(program) and not state.halted:
    state = transition(program, state)
    print(state.pc, state.stack, state.output, state.steps)
assert evaluate('PUSH 3\nDUP\nADD\nPRINT')['output'] == ['6']
```

## Assignments

1. (Foundations) Trace a countdown loop including label steps and the condition popped by `JZ`.
2. (Compiler theory) Explain why a compiler's accepted grammar is not yet its operational semantics.
3. (Testing) Add one seeded conformance property and report the exact reproduction seed and search domain.
4. (Numeric) Test integer division rounding and signed zero; document any model mismatches instead of suppressing them.
5. (Research) Draft a falsifiable lemma about determinism under fixed host semantics and no resource errors. State every assumption and explain what evidence would count as a proof.

## Assessment (course rubric only; 20 points)

- Trace and machine state precision: 5
- Static versus dynamic semantics distinction: 4
- Independent evaluator reasoning and numerical limitations: 5
- Reproducibility and counterexample quality: 4
- Clarity of falsifiable claim: 2

**The course's 20 assessment points are not SI simulation points.** SI challenge score remains 0/1,000,000 until a scoring rubric is authorized and applied to independently verified evidence.