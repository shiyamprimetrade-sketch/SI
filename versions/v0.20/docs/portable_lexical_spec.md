# SI v0.10 — Portable Source Profile 1 (SI-Portable-1)

**Status:** an optional, strict portable lexical subset of the existing SI educational language. This is a research specification for a new parser implementation; it does **not** replace the v0.9 `shlex`-based parser, does not define a host-independent numeric runtime, and is not a universal formal proof of language correctness.

## 1. Source representation

An input is a Python `str` representing a sequence of **ASCII characters only**. Permit printable ASCII U+0020 through U+007E, horizontal tab U+0009, LF U+000A, and CR U+000D **only when immediately followed by LF**. Prohibit NUL, other control characters, non-ASCII text (including inside comments), and lone CR. Count original source characters before newline normalization; the existing global maximum is 100,000. LF and CRLF represent the same logical line ending. An optional final line ending is allowed.

## 2. Tokens and comments

The scanner runs left-to-right independently of `shlex` and Python string-escape processing. On each line, spaces and tabs separate unquoted tokens. A literal `#` begins a comment anywhere outside prior structure (there is no quoting), to the next line ending. Thus:

- `PUSH 12#comment` lexes to `PUSH`, `12`.
- `LABEL end # note` lexes to `LABEL`, `end`.
- `# entire line`, empty lines and whitespace-only lines generate zero instructions and cost zero execution steps.
- Quotes `"`, apostrophes `'`, backslashes `\`, and other punctuation may appear in comments but cannot form special escapes in code. There is **no string literal syntax**.
- Multiple spaces/tabs are equivalent as token separators.

This is intentionally narrower than v0.9: the old parser accepts some quoted operands, Unicode comments, underscores within Python integer literals, and a wider range of label names. Such sources remain valid for the legacy parser but are rejected by SI-Portable-1.

## 3. Concrete grammar

Notation: `{X}` means zero or more repetitions; `[X]` optional. `WS` is one or more ASCII space/tab characters. A `comment` may follow an operand without an intervening space. End-of-line is LF or CRLF.

```ebnf
program          = { source_line } ;
source_line      = [ hspace ], [ statement ], [ hspace ], [ comment ], newline_or_eof ;
statement        = instruction0 | instruction1 ;
instruction0     = opcode0 ;
instruction1     = opcode1, WS, operand ;
opcode0          = "ADD" | "SUB" | "MUL" | "DIV" | "LT" | "EQ"
                 | "DUP" | "SWAP" | "DROP" | "PRINT" | "HALT" ;
opcode1          = "PUSH" | "LABEL" | "JMP" | "JZ" ;
operand          = signed_decimal | identifier ;
signed_decimal   = [ "+" | "-" ], decimal_digit, { decimal_digit } ;
identifier       = ( ascii_letter | "_" ), { ascii_letter | decimal_digit | "_" } ;
comment          = "#", { printable_ascii | tab } ;
hspace           = { " " | tab } ;
WS               = ( " " | tab ), hspace ;
decimal_digit    = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ;
ascii_letter     = "A".."Z" | "a".."z" ;
```

Opcode spelling is **ASCII case-insensitive** and normalized to uppercase. Operand syntax depends on the opcode: `PUSH` requires `signed_decimal`; `LABEL`, `JMP`, and `JZ` require `identifier`. Identifiers are **case-sensitive** and limited to **64 characters**. An integer literal token may contain at most **1,200 characters** and the resulting integer at most **4,096 bits**. Signed zero and leading zeroes are permitted and have ordinary integer value. `0x10`, `_` separators, scientific notation, Unicode digits, labels starting with digits, and quoted names are not portable.

The published grammar is schematic about comment placement: the normative scanner algorithm is **first cut at the initial `#`, then split the preceding line on spaces and tabs**. This correctly covers `PUSH 12#note` without requiring punctuation whitespace. Implementations must apply ASCII validation before comment stripping; disallowed bytes cannot hide in a comment.

## 4. Instruction and label resolution

After lexical processing, each nonempty row contains one opcode with the required number of operands. Resolve labels in two passes; reject duplicates and unknown jump labels, including in unreachable code. Label names are case-sensitive; opcode names are not. `LABEL` consumes an instruction slot (and runtime step), as does `HALT`. For a zero-indexed instruction sequence of length `n`, jumps carry a resolved target index in `0..n-1`. A legal named `LABEL` necessarily appears among the parsed instructions. Maximum 50,000 instructions. Runtime step/stack/output budgets and actual numeric execution semantics remain those defined by the v0.9 interpreter and VM.

## 5. Canonicalization and bounded executable obligations

`parse_portable(s)` returns an immutable sequence with source line numbers, integer values, case-preserving label names and resolved jump targets. `canonical_source` emits one instruction per line, uppercase opcodes, canonical decimal integer text and unchanged identifier spelling, omitting comments and padding. It is not a lossless formatting transform.

For every **accepted** SI-Portable-1 source tested, the following obligations are executable:

- **Round-trip structure:** `signature(parse(s)) == signature(parse(canonical_source(parse(s))))`, where signatures omit source-line locations.
- **Canonical idempotence:** `canonical_source(parse(canonical_source(parse(s)))) == canonical_source(parse(s))`.
- **Portable/legacy agreement:** for valid portable sources, their typed instruction tuples equal those from v0.9 `compile_source(s)`, and the compiled/interpreted/reference execution results match with identical resource settings.
- **Validation:** malformed syntax is rejected before execution even if unreachable.

The small exhaustive test enumerates all 4,681 strings of length 0–4 over `{P,U,0,+,#,space,tab,LF}`, with 945 accepted and 3,736 rejected in the original local run. This enumeration proves nothing about unenumerated strings. Seeded metamorphic and grammar-based test corpora provide additional finite evidence, **not mechanized universal theorems**.

## 6. Portability boundary

This specifies portable **lexing, parsing, and program shape**, not portable floating-point arithmetic, identical exception messages, OS resource isolation, deterministic host memory use, secure bytecode deserialization, or compiler equivalence for all inputs. The SI number system still inherits CPython floating arithmetic, signed-zero printing and resource semantics. Cross-runtime implementations (e.g. Rust/Go/Java) and a more complete formal semantics remain future research.