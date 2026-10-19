# SI v0.12 — Independent JavaScript execution semantics

This engineering increment adds an independently implemented Node.js VM for **SI-Portable-1**. It executes bytecode constructed by the v0.11 handwritten JavaScript parser; it does not invoke Python, its VM, or its arithmetic helper.

## State
A machine state contains program counter, stack, output list, output character count and executed instruction count. Each reached opcode consumes exactly one step (including LABEL and HALT). Instructions after HALT are validated at parse time but never executed.

## Numbers
Integer values are represented by JavaScript `BigInt` (max 4096 bits), floating-point results by IEEE-754 JavaScript `Number` (binary64). PUSH and ADD/SUB/MUL for pairs of integer operands retain exact integer values. True division produces a float, with an SI error for zero divisor, overflow and non-finite output. Comparisons return integer 0 or 1. Stack values in test transport include `{kind,text}` so integer precision and `-0.0` are preserved in JSON.

## Resource budgets
SI defaults: 10,000 execution steps, 1,024 stack entries, 100,000 output characters. `PUSH` source operand max 1,200 ASCII decimal characters, max 4,096 integer bits; max 50,000 instruction slots and 100,000 source characters. A budget of zero is permitted, with errors when a resource is actually needed.

## Differential protocol
Python launches the independent Node VM with JSON-encoded source + budgets and compares `output`, `stack`, `steps` and coarse `error category` against the Python source interpreter, compiled VM and v0.9 reference evaluator. Tests cover signed zero, branches, loops, division, overflow and bounded fuzz corpora.

## Exact limitations
The JavaScript VM is a **second implementation**, not an independent specification. Cross-runtime binary64-to-string formatting and division rounding can diverge on large or carefully selected values; sample coverage does not prove all values equivalent. JavaScript `Number(BigInt)` is limited to finite binary64 input. Python's float conversion and shortest-representation algorithms may differ from JS. Outputs are standardized only where explicitly tested. No sandbox or secure process isolation.
