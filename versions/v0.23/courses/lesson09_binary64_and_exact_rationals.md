# SI Course — Lesson 09: Exact Rational Arithmetic and IEEE-754 Binary64

## Objectives
Explain why JavaScript BigInt and Python int preserve integer precision; why integer-to-float conversion can overflow even when a ratio is finite; how rounding to nearest ties-to-even works; how IEEE sign/exponent/fraction fields encode positive and negative zero; and why Python and JavaScript display equal binary64 values differently.

## Concepts and exercises
1. Compute the exact fraction (10^400)/(10^400). Explain why Number(10n**400n) / Number(10n**400n) is not a valid replacement.
2. Derive the binary exponent of a positive rational a/b using bit lengths and an exact comparison.
3. To round a rational number, scale to a 53-bit significand; take integer quotient and remainder; increment on more than half or on half with odd least-significant bit.
4. Explain subnormal rounding when the exponent is below -1022; test numerator 1 and denominator 10^323.
5. Construct 9007199254740993 as BigInt and compare it with the binary64 value 9007199254740992.0 without converting the BigInt to Number.
6. Predict Python printing of 1e-4, 1e-5, 1e-6, 1e-7, 1e15, 1e16 and negative zero; compare with JS String().

## Practical lab
Read `js/vm.js` and `tests/test_cross_runtime_vm.py`. Run the full GitHub CI matrix and record a counterexample, expected result, and observed result. Explain which comparisons are exact and which are statistical/bounded checks.

## Course assessment (10 points, not SI mission score)
3 for mathematically correct rounding derivation; 2 for signed-zero reasoning; 2 for cross-runtime decimal comparison; 3 for reproducible failure/repair evidence and limitations.

Passing this lesson is not a PhD degree, universal proof, original language invention or general intelligence benchmark.
