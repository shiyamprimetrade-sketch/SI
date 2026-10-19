# SI v0.16 — Proposed language: AxiomFlow (research candidate)

**Working name:** AxiomFlow. This is a proposal, **not** an invented/implemented new general-purpose language at v0.16 and not a claim of superiority.

## Goal and intended niche
A small, deterministic, auditable workflow language for data transformations and reproducible business calculations, with explicit numeric effects, immutable records, bounded execution and versioned external-input declarations. Intended use cases: import-price calculations, customs-tariff scenarios, commodity data cleaning and educational compiler experiments. Nothing here asserts access to PrimePulse or any user data.

## Three scoped hypotheses to test later
H1. A typed fixed-decimal `Money<currency,scale>` type can prevent silent binary64 currency rounding compared to simple Python/JavaScript floating-point scripts.
H2. Declared capabilities (read data, emit result) can make effect review clearer than unrestricted scripts.
H3. Canonical input schemas and deterministic serialization improve cross-runtime replay fidelity.

These are **design hypotheses**, not measured facts.

## Candidate minimal language sketch (non-executable)
```
capability read tariff_table: Table<Tariff>;
type MoneyUSD = Decimal<USD, 2>;
fn landed_cost(invoice: MoneyUSD, shipping: MoneyUSD, duty: Percent)
   -> Result<MoneyUSD, CostError> pure {
  let subtotal = invoice + shipping;
  return round_half_even(subtotal * (1 + duty));
}
```
The grammar, typing, effect analysis and semantics are provisional. A compiler, runtime, package system, debugger and interoperable standard library must be developed and tested before this can be called a working language.

## Fair evaluation plan (preregister before implementation)
- **Correctness:** exact decimal oracle for invoices, FX conversion and tax scales, randomized valid/invalid values, rejected dimensional errors.
- **Reproducibility:** same source/input produces bytewise identical output across two runtimes and machines with different locales.
- **Performance:** compare against Python Decimal, JavaScript decimal libraries and one compiled baseline on identical operations; report warmup, throughput, CPU, memory, confidence intervals, toolchain versions and environment.
- **Usability:** blinded user tasks in each language with consistent documentation and measure completed tasks, time, error rate and subjective survey scores.
- **Security:** inventory of declared and actual IO privileges and sandbox limitations; no blanket "secure" claim.
- **Success criterion:** prove a *scoped advantage* in defined workloads only; publish negative results. Never claim universally better than every language.

## Research milestones
AxiomFlow 0: requirements and grammar; AxiomFlow 1: reference interpreter and executable typing rules; AxiomFlow 2: independent compiler; AxiomFlow 3: controlled benchmarks; AxiomFlow 4: complete course modules and replicable thesis experiments; AxiomFlow 5: prototype terminal/editor integration.

**Status:** idea and test plan only. User's SI project progress score is separate from objective language superiority.
