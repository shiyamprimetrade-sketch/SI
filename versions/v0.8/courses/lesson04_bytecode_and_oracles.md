# SI Course — Lesson 04: Bytecode, Safety Checks, and Independent Oracles

**Level:** foundations to advanced programming-language testing. **Version:** SI v0.8.

## Learning outcomes
1. Distinguish *source syntax*, *bytecode structure*, *control-flow verification*, *runtime checks*, and *host isolation*.
2. Explain why dead/unreachable bytecode still requires strict format validation.
3. Build a separate mathematical reference using exact rational arithmetic.
4. Demonstrate how two engines can agree and still share the same arithmetic defect.

## Bytecode contract
The program is a `tuple` of immutable `Instruction(op,arg)` instances.
- `PUSH` takes exactly one Python `int` within 4096 bits, **not** a `bool`.
- `JMP` and `JZ` take strict integer targets in `[0, len(code)]`. `len(code)` is the normal exit position.
- Every other opcode takes `None` as its argument.
- Opcode names must match the uppercase SI instruction set exactly. Incorrect instruction objects, arguments, or extra fields are rejected even when unreachable.
- This is a *structural* check; `ADD` with an empty stack is structurally valid but fails if executed.

## Hands-on
Run these in `versions/v0.8`:

```python
from si.compiler import Instruction, execute
from si.bytecode import validate_bytecode
from si.core import SIError
valid = (Instruction('PUSH', 4), Instruction('PUSH', 5), Instruction('MUL'))
assert execute(valid)['stack'] == [20]
invalid = (Instruction('HALT'), Instruction('ADD', 9))
try:
    validate_bytecode(invalid)
except SIError as exc:
    print('Rejected as intended:', exc)
```

## Independent arithmetic oracle
The executor and reference interpreter both use `si.limits.apply_binary`. Their mutual agreement therefore does not certify arithmetic correctness. The new tests compute integer results with `fractions.Fraction`, an independently written specification. For division of bounded integers, convert the exact fraction to a Python float for comparison. The oracle still shares CPython as a host, which limits independence.

## Exercises
1. List three structurally invalid but unreachable instructions (and prove rejection).
2. Construct a valid program that still fails at runtime due to stack underflow.
3. Verify whether `JMP` to exactly `len(code)` is legal and explain why.
4. Design a reproducible randomized comparison between SI and an independent rational oracle; record random seed, sample domain and exclusions.
5. **Advanced:** Propose a typed serialized bytecode format and state how you would prevent decoding ambiguity, memory exhaustion, and host-level object injection.

## Assessment rubric /10 (course grading ONLY, not SI score)
3 points structural format; 2 points CFG/runtime distinction; 3 points independent oracle/reproducibility; 2 points honest threat model. Course assessment scores never automatically convert into SI mission points.

**Project scoring:** new SI mission **0/1,000,000**; historical archive **996667/1000000**.
