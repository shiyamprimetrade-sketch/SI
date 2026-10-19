# SI Course lesson 17 — Typed feature engineering and deterministic ML evaluation

## Outcomes
Explain decimal vs floating-point features, strict CSV validation, train/test leakage, linear least-squares with intercept, bounded artifacts and benchmark fairness.

## Lab
1. Inspect the nine synthetic dataset rows. Compute `price * (1 + rate)` in AxiomFlow and Python Decimal and verify equal cent-level results.
2. Prove that the illustrative target `2*feature+5` yields OLS slope 2, intercept 5, zero test MAE on this hand-built dataset. Explain why this says nothing about real production ML performance.
3. Alter the CSV header, append a malformed row or constant price/rate training rows, and identify which rejection occurs.
4. Package the source bundle twice, verify byte-identical ZIP digests and member SHA-256 manifest.
5. Compare AxiomFlow and direct Decimal measured medians while explicitly noting the paths have unequal parsing/typechecking costs.

## Assessment /10
3 validated feature semantics; 2 leakage/OLS logic; 2 source artifact integrity; 2 reproducibility; 1 negative claims. Course grades are distinct from the SI progress ledger.
