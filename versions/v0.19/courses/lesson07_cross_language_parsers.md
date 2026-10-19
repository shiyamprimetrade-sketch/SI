# SI Course — Lesson 07: Independent parser implementations

**Objective:** explain and demonstrate parser portability without conflating it with portable execution.

## Concepts
- Lexical categories, normative scanner, CRLF normalization and rejecting Unicode outside the ASCII source profile.
- Delimiting comments before whitespace tokenization.
- Grammar vs. semantics vs. runtime.
- Arbitrary-precision integers and JSON-safe decimal string serialization.
- Independent implementations, differential conformance and limitations of finite tests.

## Lab
1. Read the SI-Portable-1 grammar and predict tokenization of `PUSH 12#note`.
2. Compare output from `si.portable.parse_portable` and `node js/portable.js`.
3. Build a valid forward-jump program with mixed-case opcode and case-sensitive labels. Verify jump addresses agree.
4. Send a 1200-digit signed decimal operand; compare bit limits and normal form.
5. Generate invalid corpora (unmatched quote, bare CR, Unicode comment, invalid LABEL identifier), and record disagreement if any.

## Assessment (course /10, not training score)
- 3: correct lexical grammar and normalization.
- 3: typed parser conformance for two runtimes.
- 2: reproducible experiments and failure logs.
- 2: honest scope boundaries and unresolved cases.

**Research caution:** a language can have a portable parser without portable numeric semantics. The degree/course assessment is not a verified PhD-level thesis or evidence of a new language's superiority.
