# SI Course — Lesson 10: Bit-Exact Numerical Testing and Minimal Counterexamples

**Goal:** progress from output comparison to raw IEEE-754 representation, reproducible boundary cases and counterexample reduction.

## Learning objectives
1. Decode IEEE-754 binary64 sign/exponent/significand and explain negative zero, denormals, normal numbers and infinities.
2. Specify exact rounding to nearest, ties-even for rational input.
3. Separate bitwise numeric accuracy from decimal shortest-roundtrip printing.
4. Design independent test oracles and document the limits of shared runtime assumptions.
5. Reproduce and shrink a failing test input without falsely claiming global optimality.

## Lab
- Construct the half-ULP tie (2^53+1)/2^53; predict and verify its binary64 hex representation.
- Predict whether 1/2^1075 rounds to zero and whether 3/2^1075 ties to an even subnormal.
- Compare the Python and Node rendering of 0x0000000000000001, 0x0010000000000000 and -0.0.
- Use `js/numeric_probe.js` and Python `struct` to compare result bits.
- Inject a synthetic predicate to validate `shrink_ratio`; distinguish a local minimum from a global minimum.

## Assessment (course points only, /10)
3 IEEE bit-pattern derivation; 2 correct ties-even explanation; 2 reproducing an independent oracle; 2 deterministic failure reduction; 1 explicit negative findings and scientific limits.

Course grades are **not** the SI project simulation score. New SI score is assigned only by the separate declared rubric and evidence.
