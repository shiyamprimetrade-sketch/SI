# SI research notebook — v0.8 structural bytecode validation

**Status:** experimental technical note, not a peer-reviewed or completed PhD thesis.

## Questions and hypotheses
- H1: the v0.7 executor accepts malformed *unreachable* manually-constructed bytecode because it checks opcodes and operands only when reached.
- H2: whole-program preflight can make structural rejection consistent among execution, verification, and type analysis.
- H3: a separately implemented exact rational arithmetic oracle can detect common defects that cross-executor agreement cannot.

## v0.7 source counterexamples
`(Instruction('HALT'), Instruction('ADD', 5))` and `(Instruction('HALT'), Instruction('EXEC'))` are ignored after `HALT` in v0.7. They should now fail structural validation. Similarly, an arbitrary object after HALT is not a valid instruction. This is a format-consistency flaw; **no arbitrary code execution or escape from Python has been demonstrated**.

## Method
- Create `si.bytecode.validate_bytecode` with strict tuple, strict dataclass type, uppercase opcode vocabulary, strict integer operands, jump target bounds and old numeric limits.
- Apply the check to `execute`, `verify`, and `typecheck` before control-flow work.
- Retain runtime stack checks separately; structurally valid code can still underflow.
- Use deterministic, mutated invalid bytecode to seek raw host exceptions and control-flow bypasses.
- Write `fractions.Fraction` arithmetic tests without importing SI's shared numeric helper. Compare bounded integer-result operations exactly and integer DIV against `float(Fraction(a,b))`; record random seeds.

## Falsifiable acceptance criteria
- A1: every malformed bytecode candidate produces `SIError` consistently, including dead code.
- A2: existing SI regression tests continue to pass across Python 3.11, 3.12, 3.13.
- A3: new deterministic oracle tests agree over their specified ranges, without claiming exhaustive equivalence.
- A4: legitimate exits (`JMP` to exactly program length), empty programs, and verifier dead-code behavior remain valid.

## Explicit limits and threats to validity
- The validator does not prove termination, stack safety, constant-time execution, memory bounds, or correct floating-point semantics for all values.
- `Fraction` is independent from SI's numeric helper but uses the same CPython host runtime. Different platforms and independent implementations remain untested.
- A native Python tuple is not a wire format and does not make bytecode ingestion safe from arbitrary untrusted serialization.
- Random tests cover finite samples. There is no formal verification, coverage-guided fuzzing, production security audit, or proof of universal language superiority.

## SI long-term research sequence
1. Foundational computer science, theory of computation, mathematics and formal proofs.
2. Representative programming language families: imperative, functional, logic, system-level, concurrent, database/query, and hardware-description.
3. Hard language/compiler/OS evaluations and documented negative results.
4. Design a separately named, original-purpose programming language with grammar, typing, compiler/runtime and real application benchmarks.
5. Compare against appropriate language baselines with reproducible, statistically sound evaluation.
6. Develop courses and a doctoral-level dissertation manuscript with peer-review-ready evidence and reproducibility.
7. Invent and test a distinct terminal environment and accompanying developer tools.

A single finite test or benchmark cannot establish that a language is better than every other existing language.

**Ledger:** new SI mission 0/1,000,000; archival historical simulation 996667/1,000,000; new points 0.
