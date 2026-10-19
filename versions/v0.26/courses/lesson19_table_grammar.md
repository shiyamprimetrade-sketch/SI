# SI Course lesson 19 — Typed table syntax and operational semantics

## Learning objectives
Implement a small real declarative language, not just a Python library; understand schema/type inference, immutable relational operations, bounded execution, and honest conformance experiments.

## Lab
1. Trace `table costs = input` then `augment costs landed_cost_usd` across nine CSV rows. Derive the exact typed output schema.
2. Apply `sum costs.landed_cost_usd`, project `(price_usd,landed_cost_usd)`, stably sort by `price_usd`, and `emit costs`. Independently recompute USD values using Decimal.
3. Remove the `landed_cost_usd` column with `select` and attempt to `sum` it. Explain the compile-time rejection and why the rejection precedes row execution.
4. Test malicious or unsupported expressions, incorrect table names, source-size limits and unknown columns; document error categories.
5. Compare the actual table sublanguage with existing AxiomFlow arithmetic statements. Propose a unified grammar and type preservation theorem, and identify still-unproved obligations.
6. Create a seed-controlled generated table corpus and verify deterministic output independently.

Assessment (/10): grammar 2; static validation 2; exact numeric results 2; testing 2; sound research limitations 2. Educational credit is separate from SI project self-assessment.
