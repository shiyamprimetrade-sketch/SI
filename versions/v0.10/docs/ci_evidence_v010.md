# SI v0.10 — Reproducible CI evidence and limitations

**Repository:** `shiyamprimetrade-sketch/SI`  
**Branch:** `si-v0.10-portable-lexer-20261016` (draft stacked on v0.9)  
**Code commit:** `ceaa49950da58beee20a695554fe3a4df9cc5e79`  
**Observed GitHub Actions push workflow:** https://github.com/shiyamprimetrade-sketch/SI/actions/runs/38903463749  
**Workflow file:** `.github/workflows/ci-v010.yml`  
**Execution location:** `versions/v0.10`  
**Test command:** `python -W error -m unittest discover -s tests -v`  
**Evidence observation date:** October 16, 2026 (UTC GitHub logs).

## Confirmed matrix results

| Python runtime | Job ID | Tests | Test time | Conclusion |
|---|---:|---:|---:|---|
| 3.11 | `116981126492` | 207/207 | 4.784 s | success |
| 3.12 | `116981126584` | 207/207 | 2.550 s | success |
| 3.13 | `116981126168` | 207/207 | 4.807 s | success |

**621 successful test executions**, consisting of 172 inherited v0.9 test methods and 35 new v0.10 test methods per Python version. No unittest failures or workflow warning annotations appeared in the inspected jobs. Each job also completed syntax compilation (`python -m compileall -q si tests`) and executed the existing SI CLI example, printing `3`, `2`, `1`.

## Executable bounded lexical obligations

All three Python jobs ran `python -W error -m si.obligations` and reproduced:

- Alphabet: `P`, `U`, `0`, `+`, `#`, space, tab, newline.
- Enumerated input lengths: zero through four inclusive.
- Total candidates: **4,681**.
- Accepted: **945**, each passed structural round-trip and canonicalization idempotence.
- Rejected: **3,736**.
- SHA256 of the enumerated source/outcome stream:

`9997585eb832c9a59660a7ff3873c1e53a087a975b17a79198512aa36a30bd4d`

**Important:** This is an *exhaustive result for that finite alphabet and length bound only*. The digest is evidence of reproducibility across the tested runners; it is not an independent formal proof of all-source parser correctness.

## Scientific conclusions supported

- Under the tested cases, the new hand-coded ASCII parser's accepted programs agree with the v0.9 compiler and execution models on typed code, output, final stack and step count.
- Canonical source rendering is structure-preserving and idempotent over the bounded and seeded exercised cases.
- The strict profile purposefully rejects quoted operands, Unicode comments and nonportable integer syntax that v0.9 may accept; the legacy parser has **not** been changed.

## Negative evidence, gaps and next work

- **No cross-language runtime** was tested: all engines ran on CPython on Linux runners. Claims of portability here refer to *defined source syntax* and repeatable parser semantics, not full host-independent execution.
- **No universal proof** was obtained. An inductive proof over the scanner states, a mechanized formalization (Coq/Lean/Isabelle/TLA+), or a genuinely independent non-Python lexer remains future work.
- The executable checker exhaustively covers a tiny eight-symbol corpus; it is deliberately weak on numbers, long identifiers and Unicode (other targeted and seeded tests cover some of those cases).
- These tests do not measure language speed against Python/Rust/Java, prove security sandboxing, create a new production language or terminal, or constitute a PhD thesis defense.
- Any later commit to this branch must be re-tested: results above apply to the named code commit. This evidence report itself can be introduced through a docs-only commit, with a separate CI run if made.

**Training ledger:** new SI score **0/1,000,000**, new points **0**; historical archive **996,667/1,000,000**, unchanged. No graduation or intelligence claim.