# SI Course — Lesson 06: Portable Lexing, Independent Parsing and Bounded Proof Obligations

**Level:** basic programming → compiler construction → research methodology. **Version:** SI v0.10.

## Prerequisites

SI lessons 01–05 or equivalent knowledge of strings, tokens, stacks, finite automata, test cases and Python `unittest`.

## Objectives

By the end, a learner can distinguish lexical, syntactic, semantic and runtime portability; describe the ASCII tokenization rule without depending on Python `shlex`; implement and test a state-machine scanner; and state clearly the limits of a finite proof corpus.

## Module A — Basic foundation

1. A character is not a token. The SI profile recognizes ASCII `PUSH`, numbers, label identifiers, comments and whitespace.
2. Whitespace `SP` and `HTAB` separates tokens; `LF` and `CRLF` separate lines; a `#` begins a comment **even inside the current would-be token**.
3. An opcode is case-insensitive, but a label name is case-sensitive.
4. Explain why `PUSH "12"` remains valid in the **legacy** parser but is not accepted by the portable profile.

**Exercise A:** Hand-tokenize `PUSH +0012# comment\r\nPRINT` and predict the canonical rendering (`PUSH 12\nPRINT`).

## Module B — Parser engineering

Build a deterministic scanner that accepts only valid ASCII, detects lone carriage returns and other control characters, tokenizes per-line, requires 0/1 operands, validates strict decimal integers and identifiers, and records source-line positions. Implement a two-pass label resolver and reject duplicate or missing labels in dead code. Explain why rejecting disallowed Unicode *before* discarding comments matters.

**Exercise B:** Create a source with two labels `x` and `X` and jumps to both; show distinct target instruction indices. Explain why a 65-character identifier is rejected in this profile.

## Module C — Independent conformance

Compare the independent SI-Portable-1 parser against the existing v0.9 `shlex`-based compiler on sources accepted by the new profile. Then run the reference interpreter, bytecode VM and small-step evaluator to check output, remaining stack, and step count. **Do not assert agreement for source outside the documented portable subset.**

**Exercise C:** Test one thousand deterministically generated portable arithmetic programs with signed decimal literals and explicit seed. Include signed negative zero, a short conditional branch and a countdown loop.

## Module D — Machine-checkable bounded obligations

Study `si/obligations.py`: it enumerates every source up to length four over an explicit eight-symbol alphabet, checks canonical round-trip/idempotence for accepted examples, and writes a stable SHA-256 digest of results. The corpus contains exactly 4,681 strings, **not all programs**. A mathematical universal proof would require separate induction and a formal model covering all grammatically valid strings and interpreter states.

**Exercise D:** Expand the alphabet or maximal length to expose a new edge case, then report the precise bound, count, seed/digest, test environment and counterexamples.

## Assessment rubric (course / 20; NOT SI mission points)

- Lexical grammar and portability distinctions: 5
- Independent scanner, identifier/integer rules and error handling: 5
- Cross-engine conformance, deterministic seed and mutation evidence: 5
- Formal limitations, falsifiable claims and reproducibility: 5

## Research extension

Design a non-Python lexer in Rust or Go, compare accepted/rejected source corpora against SI-Portable-1, measure parsing performance on realistic workloads and investigate Unicode internationalization requirements. This is a proposal, **not a completed cross-language implementation**.

Historical training archive: 996,667/1,000,000. New SI challenge: **0/1,000,000**, with **zero newly awarded points**.