# SI v0.13 — Cross-runtime numeric conformance contract

**Scope:** the optional SI-Portable-1 stack language, not full Python language semantics.

## Numeric representation
- SI integers are arbitrary precision **within 4,096 bits**. Python uses `int`; Node.js uses `BigInt`.
- All true division results are IEEE-754 binary64 floats, including signed positive/negative zero; division by zero raises a dedicated SI language error.
- Arithmetic results that exceed the integer cap raise `integer bit budget exceeded`. Integer-to-float division whose correctly rounded quotient is outside the finite binary64 range raises `numeric overflow`. Operations on already floating operands that result in nonfinite values raise `non-finite numeric result`.

## Integer division independent of direct int→float conversion
v0.12 called `Number(bigint)` on each operand before true division. When both integers had 400 decimal digits, both conversions overflowed, even though the quotient (e.g. 10^400 / 10^400) was 1.0. Python's integer division can calculate a finite ratio without converting both integers separately.

v0.13 rounds the *exact BigInt rational quotient* directly to a binary64 representation. It uses bit-length comparison, integer quotient/remainder, round-to-nearest ties-to-even, and constructs IEEE-754 sign/exponent/fraction bits using DataView. This is an engineering implementation tested against CPython, **not** a machine-checked floating-point proof.

## Exact mixed integer / float comparisons
v0.12 cast both operands to `Number` for comparisons. That loses distinctions above 2^53. For example, integer 9007199254740993 must not compare equal to float 9007199254740992.0. v0.13 extracts the binary64 rational value from its bits and performs exact `BigInt` rational comparison to integer operands.

## Python-compatible decimal rendering
JS shortest `Number.toString()` and Python `repr(float)` have different formatting thresholds. Examples: 1e-7 vs 1e-07; 0.000001 vs 1e-06; 10000000000000000 vs 1e+16. SI v0.13 normalizes finite JS shortest-decimal text into the CPython-like fixed/scientific threshold: scientific if decimal exponent below -4 or at least 16; otherwise fixed notation, with `.0` for integral-valued float display and two-digit exponent minimum. The output remains explicitly **CPython-repr-compatible in tested cases**, not a universal external specification of float serialization.

## Proposed executable obligations
1. Every sampled finite ratio (including both operand magnitudes beyond binary64) agrees with CPython integer true-division display, tagged stack values and error category.
2. Samples near signed-zero and subnormal boundaries agree, with tie-to-even rounding behavior exercised.
3. Mixed int/float comparison distinguishes 2^53 from 2^53+1.
4. Previously passing v0.12 suites remain intact, and the v0.10 lexical corpus digest is invariant.

## Limitations
No mechanized proof or mathematical coverage of all binary64 bit patterns. Shortest-decimal algorithms can differ on rare boundary cases; CPython is used as a behavioral oracle, not as a language-independent formal standard. The VM is not a sandbox or production runtime.
