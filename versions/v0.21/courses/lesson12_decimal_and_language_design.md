# SI Course — Lesson 12: Floating-point roundtrip and language invention

**Prerequisites:** IEEE-754 representation, elementary type systems, interpreters.

## Goals
1. Distinguish exact binary64 bit roundtrip from shortest decimal spelling and CPython-specific canonical spelling.
2. Create seeded full-bit random tests, special encoding vectors and nextafter-neighbor tests.
3. Identify requirements that justify inventing a new language rather than adding a library to Python, JavaScript or Rust.
4. Design unbiased comparative benchmarks and publish negative results.

## Labs
- Roundtrip 0x8000000000000000 through decimal: why must the string contain a minus sign?
- Compare `1e-06`, `1e-6`, `0.000001` and discuss formatting policy and uniqueness.
- Write a deterministic 100-case bit corpus, preserve the seed, compare JavaScript rendering against Python, and collect failures.
- Review the provisional AxiomFlow `Money<currency,scale>` and explicit capability model. Identify an established-language library that may already meet each requirement.
- Preregister three benchmarks: correctness, runtime cost, and developer usability; include competing baselines and sample counts.

## Assessment (/10 educational credit, not SI scoring)
3 numeric representation and roundtrip; 3 falsifiable language hypotheses; 2 reproducible benchmark design; 2 limitations and critique. No claims of original implementation or universal superiority.
