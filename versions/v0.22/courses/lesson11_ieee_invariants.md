# SI Course — Lesson 11: Nearest-even proof obligations and shrinking failures

**Objectives:** understand exact rational distances between binary64 numbers, ties-to-even significand parity, signed-zero preservation, and counterexample reduction.

## Exercises
1. Derive the neighbors of 1.0 and check why the halfway case 1+2^-53 rounds to even.
2. Explain why 1/2^1075 rounds to zero but 3/2^1075 rounds to the even neighboring subnormal.
3. Prove for a specific finite candidate that |f−R| is no larger than the distance from each adjacent float to R.
4. Construct a candidate that violates the nearest-neighbor property, and verify the executable checker rejects it.
5. Shrink a synthetic reproducible counterexample using decimal digit deletion. Explain the differences between a local improvement and a global minimum.
6. Document a case where binary64 bit equality and shortest decimal string equality answer different questions.

## Assessment /10 (course points, not SI project points)
3: correct rounding derivation; 2: negative control; 2: signed zero; 2: bounded minimizer; 1: threat model and reproducibility.

**Caution:** this lesson does not constitute a formalized universal proof, thesis defense or new language invention.
