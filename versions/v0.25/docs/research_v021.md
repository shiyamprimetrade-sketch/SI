# SI research notebook v0.21 — Data/ML interoperability, benchmark rigor and packaging

## Research question
Can a small typed AxiomFlow calculation be used as a deterministic feature generator in an ordinary data/ML workflow, and can its numeric results be checked independently?

## Protocol
- Strict CSV schema and ASCII decimal values, bounded size and row count, rejected control characters, extra fields and malformed monetary values.
- Typed function `landed(price:USD,rate:scalar)->USD` evaluated by AxiomFlow as a feature.
- Independent host-language `decimal.Decimal` oracle checks every accepted feature, including 400 reproducibly generated values in tests.
- Decimal ordinary-least-squares one-feature regression with intercept, ordered 2/3 training and 1/3 held-out test. Synthetic nine-row data encodes a perfect linear target solely to test integration; zero error is **not** a generalization claim.
- A three-repeat median microbenchmark checks equal output on four examples, then compares full parse/typecheck/evaluate and direct Decimal. This is **not cost-equivalent** and can only establish observed overhead on tested runners.
- Reproducible source ZIP builder fixes timestamps, member order and permissions and includes per-file SHA-256, with a repeated-byte-for-byte build test.

## Negative results and missing claims
AxiomFlow currently depends on the Python runtime for ML modeling, IO and HTTP. The language itself is not a general ML platform. No GPU training, model deployment, training on real customer data, native TensorFlow/PyTorch integration or correctness proof exists. The benchmark must not be reported as a fair win over Python or compared to C/C++/Java without equivalent functionality and environments. No actual visual browser automation or public secure deployment has been demonstrated.

## Next milestones
Extend typed arrays/tables, explicit JSON/CSV types, a practical packaging/distribution story, controlled same-feature comparisons against Python/JavaScript/C++ implementations and a thesis-style reproducibility appendix. Preserve synthetic data provenance and permission boundaries. Ten-day deadline remains ambitious and gates may remain incomplete.
