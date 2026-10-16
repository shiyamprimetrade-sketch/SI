# SI v0.2: Testable thesis

**Hypothesis:** Compiling a restricted stack language into resolved bytecode can remove repeated source-token parsing during execution while preserving its observable behavior (stack and output). This is not a novel general-purpose language and does not establish superiority to Python.

## Semantics
The bytecode is a sequence of typed `(opcode, argument)` instructions. Jumps are resolved to instruction indices. Arithmetic follows the v0.1 operand order; division uses Python floating-point division. A step limit and stack limit remain mandatory. Source comments and blank lines do not become instructions, so `steps` may differ from the original interpreter; stack and output are the differential oracle.

## Evaluation
A seeded random-program test generates 1,000 arithmetic programs, plus exhaustive arithmetic pairs, control flow, malformed programs, and resource-budget tests. Benchmarking records wall-clock timing and runtime version; it is environment-specific and not a general performance claim.

## Known limitations
No static type system, memory isolation, verified optimizer, packages, concurrency, or formal proof of semantic equivalence. SI runs on CPython. The compiler checks duplicate labels, unlike v0.1; comparisons cover valid shared programs. No cross-language performance claims are supported.