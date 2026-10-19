# SI v0.11 — Refined SI-Portable-1 grammar and cross-runtime test contract

## Scope
This refines v0.10's normative scanner algorithm; it does **not** alter the legacy Python parser, define a new runtime, or claim general language superiority. Grammar and operational semantics are separate.

## Input validation
- Source is at most 100,000 Unicode code points, but accepted characters are only ASCII U+0020–U+007E, TAB, LF, CR as part of CRLF.
- Reject disallowed characters even in comments. Reject lone CR. Normalize CRLF to LF after validation.
- A line is scanned from left to right: first `#` terminates code, then SP/HTAB split the preceding fragment into tokens. Blank/comment-only lines add no instructions.
- Keywords use ASCII case-insensitive matching; label identifiers are ASCII `[A-Za-z_][A-Za-z0-9_]*`, 1–64 chars, **case sensitive**.
- Zero-argument opcodes: ADD SUB MUL DIV LT EQ DUP SWAP DROP PRINT HALT.
- One-argument opcodes: PUSH LABEL JMP JZ.
- PUSH decimal is `[+-]?[0-9]+`, max 1200 chars and max 4096 bits, no hex, Unicode numerals, underscores or quoting.
- LABEL JMP JZ take identifiers, with duplicates and unknown targets rejected, even if unreachable.
- Maximum 50,000 instructions.
- Canonical serialization prints uppercase opcodes, canonical base-10 integer values, preserved label spelling and no comments; positions not retained.

## Cross-language representation
The Node.js parser in `js/portable.js` does **not** call the Python implementation or its dependencies. Python reference outputs `(opcode, operand, target)` tuples; Node emits JSON arrays. Because JSON numbers cannot safely encode arbitrary precision, PUSH integer values are transported as **decimal strings** in both comparison projections, jump indices as JSON numbers (at most 50,000) and null for absent fields.

This is a parser-conformance contract only. JavaScript does not execute the resulting bytecode in v0.11.

## Bounded obligations
1. All accepted corpus samples have equal typed opcode, operands, jump targets and canonical source in Python and Node.
2. Rejected samples must be rejected by both engines; selected error messages are compared where stable.
3. Input normalization is idempotent on accepted programs in both engines.
4. Existing Python operational semantics and legacy tests must continue passing.
5. Cross-runtime workflow runs Python 3.11–3.13 and a supported Node.js runtime with explicit version output.

**Proof status:** finite exhaustive subsets and seeded tests constitute machine-executable checks, **not universal theorems**. Formal proof of scanner equivalence and serialized bytecode semantics remains future work.
