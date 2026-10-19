# SI Course lesson 15 — Static monetary types, pure functions and pinned modules

**Learning objective:** trace and validate typed function calls, understand pure function state, and distinguish reproducible module file hashes from general security isolation.

### Lab
1. Write `fn tax(price: USD,rate: scalar)->USD=price*(1+rate)`; predict output for price 125.50 USD and rate 0.075.
2. Predict and check compiler rejection for USD+EUR, money×money, return type mismatch, invalid arity and recursion.
3. Construct a pinned JSON manifest with SHA-256 digests. Modify one byte in an imported file and explain the failure.
4. Show why rejection of `../` paths and symlinks does not prevent every possible hostile-host attack.
5. Compare AxiomFlow pure computation with Python Decimal on identical expected output; avoid turning this into a speed-superiority claim.

### Assessment /10
3 static typing, 2 language grammar, 2 pinned dependency integrity, 2 deterministic conformance evidence, 1 scientific threat model. Educational credits are **not** automatic SI project score.

### Follow-up
Implement modules with controlled versioning, explicit capabilities, a production-safe execution boundary, and a fully tested HTTP API/web example.
