# SI v0.17 — AxiomFlow research notebook

## Implementation contribution
First executable Python-hosted AxiomFlow **domain-specific language** core: immutable `let` bindings, `emit`, Decimal scalars, tagged money literals, arithmetic precedence, parentheses, two-decimal half-even rounding, currency mismatch errors, explicit source/numeric budgets, CLI file/one-shot/interactive modes.

## Reference testing
Targeted valid/invalid tests, independently computed Decimal formulas, 500 seeded cases (seed 17001). GitHub workflow executes inherited SI numerical test suite and new AxiomFlow tests across Python 3.11, 3.12, 3.13 with Node.js 22.

## Negative benchmark finding
The initial local *exploratory* benchmark (Python 3.13.5, 50 iterations, 2 repeats) showed approx. **13,637 ns/call** for AxiomFlow reparsing/evaluation versus **801 ns/call** for direct Python Decimal operations. This is NOT cost-equivalent because the DSL reparses source on every call, and the sample size is tiny. It indicates current overhead and provides no evidence that AxiomFlow is faster. Re-run normalized workloads before any relative performance claim.

## Known limitations
No compiled machine-code backend, self-hosted runtime, complete typed semantics, functions/imports, resolver, frontend/web/API/ML platform, security sandbox, separate runtime, or standalone OS terminal. The interactive CLI is *not* a replacement for Bash/PowerShell. The project is not independently measured superintelligence. Currency tags are syntactic; there is no verified external currency registry. No thesis defense or universal superiority is claimed.

## Next falsifiable research
Measure parsing once vs interpreted execution repeatedly, precise Decimal quantization properties, reject budget attacks, introduce typed module signatures, then compare against Python Decimal, Java BigDecimal and compiled-language decimal libraries using identical algorithms. Negative results must be published.
