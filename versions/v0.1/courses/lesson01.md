# SI Course — Lesson 1: Stack computation

**Objective:** predict the contents of a stack after every instruction.

```
PUSH 6
PUSH 7
MUL
PRINT
```

Output: `42`. `PUSH` adds an integer; `MUL` consumes two operands; `PRINT` consumes the result.

**Exercise:** write an SI program that computes `(9 - 4) * 3` and prints 15.

**Challenge:** create a countdown loop from 5 to 1 using `LABEL`, `DUP`, `JZ` and `JMP`. Run `python -m unittest discover -s tests -v` after each change.

**Research assignment:** compare the interpreter's semantics with Python's, identify differences in type behavior and performance, and propose tests. Do not assume SI is faster or safer than Python.