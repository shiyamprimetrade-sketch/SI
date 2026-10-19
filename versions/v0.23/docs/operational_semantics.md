# SI v0.9 — Small-step Operational Semantics (working specification)

**Status:** versioned, executable *working specification* accompanying the independent `si/reference.py` model. It is not a mechanically checked proof and does not define a new general-purpose language. Scope: SI's existing bounded, deterministic, stack-based educational language as implemented in v0.8.

## 1. Lexical and source program model

A source program `s` is a Python Unicode string with `len(s) <= 100000` characters. `str.splitlines()` divides the source into numbered lines. Each line is tokenized using `shlex.split(line, comments=True)`; empty and comment-only lines are ignored. The first token is an opcode, normalized to uppercase. Operands are case-sensitive. A program is a finite sequence `P = [i_0, ..., i_(n-1)]` of instructions with `0 <= n <= 50000`.

Instruction arities:

| One operand | Operand meaning | Zero operands |
|---|---|---|
| `PUSH token` | `int(token)` parsed in Python's default decimal convention; <=1200 characters; value bit-length <=4096 | `ADD`, `SUB`, `MUL`, `DIV`, `LT`, `EQ`, `DUP`, `SWAP`, `DROP`, `PRINT`, `HALT` |
| `LABEL name` | Declare case-sensitive label; must be unique | |
| `JMP name` | Unconditional jump to declaration's **instruction index** | |
| `JZ name` | Pop condition; jump if numerically zero | |

**Validation precedes execution**, including instructions after `HALT` and unreachable instructions. Invalid quoting, opcode, arity, duplicate label, integer token, or unresolved target raises `SIError`. First pass validates all instruction names/arity and collects label indexes; second resolves integer literals and jumps. The reference evaluator deliberately implements its own parser; it is not a call to the production compiler. Python `shlex`, Unicode, and `int()` remain host-defined dependencies, so this document does *not* purport to provide a wholly language-neutral lexical grammar.

`LABEL` stays an executable no-op instruction and consumes one step; jumps land **on** the label instruction. Source labels map to indexes in the comment-free instruction array, not source-line numbers. A validated source jump can target an in-program label; separately constructed bytecode may jump to index `n` as a normal exit.

## 2. Values and configurations

The numeric domain is `V = Z_(<=4096 bits) ∪ finite IEEE-754 binary64`. `PUSH` yields a Python `int`; division yields a Python `float`. `LT` and `EQ` yield integer `0` or `1`. Host Python's signed zero is observable through `PRINT` (`-0.0` versus `0.0`). Non-finite numeric results and over-budget integers are rejected. This policy does not establish cross-platform floating-point determinism.

A machine configuration is

`C = <pc, S, O, k, c, h>`

with program counter `pc`, finite bottom-to-top stack `S`, tuple of printed strings `O`, number of executed instructions `k`, cumulative number of characters in `O` denoted `c`, and halt flag `h`. Initially `C_0 = <0, [], [], 0, 0, false>`. Let `N = len(P)`; `pc == N` or `h == true` is terminal.

Runtime budgets `B = <steps, stack, output_chars>` default to `<10000,1024,100000>`; each must be an exact nonnegative Python integer (booleans are invalid). No step is taken once a state is terminal. If nonterminal and `k >= max_steps`, execution raises `SIError('step budget exceeded')`. A successful step increments `k` by one (including `LABEL`, `PRINT`, `JMP`, `JZ`, and `HALT`). Stack length and total printed characters may not exceed their budgets; excess raises the corresponding `SIError`. Executing an instruction can raise `SIError` instead of yielding a successor state.

## 3. Successful small-step relation

Write `P ⊢_B C → C'`. Unless otherwise stated, the next `pc` is `pc+1`, and output, stack and counters not named below are unchanged. Every rule presumes the nonterminal budget precheck succeeds and increments `k` by one. The top of stack appears at the **right** (`S·a·b`).

| Instruction | Required stack | Stack/output effect | Next `pc` |
|---|---|---|---|
| `PUSH a` | any | `S → S·a` | `pc+1` |
| `ADD` | `S·a·b` | `S·(a+b)` | `pc+1` |
| `SUB` | `S·a·b` | `S·(a-b)` | `pc+1` |
| `MUL` | `S·a·b` | `S·(a*b)` | `pc+1` |
| `DIV` | `S·a·b`, `b≠0` | `S·(a/b)` as bounded finite float | `pc+1` |
| `LT` | `S·a·b` | `S·int(a<b)` | `pc+1` |
| `EQ` | `S·a·b` | `S·int(a==b)` | `pc+1` |
| `DUP` | `S·a` | `S·a·a` | `pc+1` |
| `SWAP` | `S·a·b` | `S·b·a` | `pc+1` |
| `DROP` | `S·a` | `S` | `pc+1` |
| `PRINT` | `S·a` | stack `S`; append `str(a)` to `O` and count its characters | `pc+1` |
| `LABEL` | any | no change | `pc+1` |
| `JMP t` | any | no change | `t` |
| `JZ t` | `S·a` | stack `S` | `t` if `a==0`, else `pc+1` |
| `HALT` | any | no change; set `h=true` | `pc+1` |

Arithmetic: integer-only `ADD`/`SUB`/`MUL` are mathematically exact, subject to the integer bit budget. `DIV` is rounded to binary64 and can raise numeric overflow. Operations involving float values inherit CPython binary64 operator behavior, including signed zero, finite-result policy and host-exception normalization. The reference model uses `fractions.Fraction` for integer-only arithmetic and integer division and explicitly preserves the negative-zero division case; float-involved operations use host operators to preserve their rounding/sign behavior. This makes the reference independently implemented but not entirely independent of CPython's floating-point runtime.

## 4. Errors, termination and observables

- **Stack underflow:** an instruction requiring more values than present raises `SIError('stack underflow')`.
- **Division by zero:** `b==0` raises `SIError('division by zero')`, including signed zero.
- **Finite and resource bounds:** overlarge integers, non-finite float results, invalid budgets, exhausted steps/stack/output, and host arithmetic overflow raise documented `SIError` categories.
- **Terminal:** `pc == N` (fallthrough or explicit exit) or `HALT` ends execution without extra step. A program with zero executable instructions terminates with zero steps.
- **Observables:** successful `evaluate(s, B)` produces `{'output': list[str], 'stack': list[V], 'steps': int}`; these three fields must match each production engine on the covered conformance domain. Error strings are tested where meaningful, but error priority between invalid budgets and invalid source is **not** promised identical for all frontends.

## 5. Limitations and falsifiable conformance claim

The executable model is **not** a mechanically verified semantics theorem, a memory/CPU sandbox, or a secure bytecode transport. It allocates immutable tuples on every step and is deliberately slower than the production VM; no performance superiority is asserted. Machine precision and host conversion still influence float behavior. The bounded test suites sample arithmetic, conditionals, loops, malformed programs, resource limits, and signed-zero regression; they cannot prove equivalence for all possible input programs. A future milestone should define an unambiguous lexer, prove selected invariants with a proof assistant or model checker, and add an independent implementation in another language.

**Scoring:** historical archival ledger 996667/1000000, new SI challenge ledger 0/1000000, newly awarded points 0.