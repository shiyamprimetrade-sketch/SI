# SI v0.6 — Source validation and step-budget parity

Experimental, resource-bounded stack-language laboratory derived from SI v0.5. No claim of general intelligence, programming-language novelty, or exhaustive correctness.

## Review basis
[SI v0.5 draft PR #1](https://github.com/shiyamprimetrade-sketch/SI/pull/1) passed CI on Python 3.11, 3.12, 3.13. Source inspection identified a discrepancy: reference interpreter counted blank/comment-only lines as steps, while VM skipped them. A second discrepancy let the reference interpreter ignore malformed instructions after HALT, while the compiler rejects them.

## Focused changes
- Ignore blank/comment-only lines in the reference interpreter's program counter and execution step budget. Preserve original source line numbers in diagnostics.
- Prevalidate all instruction names and arities, PUSH integer operands, and JMP/JZ label names, including unreachable instructions, matching the compiler's two-pass approach independently.
- Add 17 regression tests including 800 seeded metamorphic programs. In tested cases, compare full state (output, stack, steps) across reference and bytecode VMs, and verify invariance to blank/comment insertion.

## Run
From `versions/v0.6`:
```sh
python -W error -m unittest discover -s tests -v
python -m si examples.si
```

CI workflow at repository root: `.github/workflows/ci-v06.yml`, Python 3.11/3.12/3.13. Do not claim CI success until verified in GitHub Actions. PR #2 is stacked on the SI v0.5 branch; merging must be done deliberately, with tests rechecked.

## Limitations
- The compiler and interpreter share Python numeric behavior; finite fuzz tests are not a proof of equivalence.
- Static source validation does not prove termination or safe stack behavior on all paths.
- Very large source/integer literals, non-finite floating-point outcomes, unusual Unicode, and hostile input need separate hardening.
- The interpreter is NOT a sandbox and must not execute untrusted Python (it contains no eval; that is not a host-level security guarantee).
- The prevalidation opcode list is duplicated intentionally to maintain independent implementations and should be guarded by parity regression tests.

**Historical simulation score:** 996667/1000000. **New points:** 0. This is a simulation ledger, not a measured intelligence score.
