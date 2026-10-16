# SI v0.6 — bounded portable bytecode (candidate)

This version is based on SI v0.5 and adds `si.portable`: a canonical JSON bytecode format, SHA-256 accidental-corruption detection, strict opcode/argument validation, signed 64-bit PUSH operands, bounded input/instruction/stack limits, and static verification before executing decoded programs.

## Use

```python
from si.compiler import compile_source
from si.portable import dumps, loads, execute_checked
program = dumps(compile_source('PUSH 3\nPUSH 4\nADD\nPRINT'))
assert execute_checked(program)['output'] == ['7']
```

From `versions/v0.6`, run `python -W error -m unittest discover -s tests -v`. GitHub Actions CI tests Python 3.11, 3.12, 3.13.

## Security boundary

The digest is **not a signature or authentication**. Anyone able to replace the payload can recompute the digest. Do not treat bytecode or decoded output as independently verified evidence. This codec is not a Python sandbox. The interpreter has no network or filesystem primitives, but running the Python host is not a security boundary. Untrusted code must be isolated by a separate operating-system sandbox. Inputs larger than 1 MB and programs longer than 10,000 instructions are rejected. Runtime steps and stack height remain bounded by caller-configurable limits.

## Scope and score

No claim of general intelligence, superintelligence, formal proof, exhaustive security, or independent verification. Historical simulation score **996667/1000000**, **zero new points**. `main` is not modified by the candidate branch.