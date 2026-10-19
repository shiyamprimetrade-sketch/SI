# SI doctoral-research notebook — v0.13 numerical cross-runtime semantics

## Falsifiable findings and counterexamples
- **Large finite integer ratio:** `PUSH 10^400; PUSH 10^400; DIV` (written as 401-character decimal operands) is finite (1.0) in Python. v0.12 JS called `Number` on each integer, obtaining infinities and `numeric overflow`.
- **Shortest-decimal formatting:** `1 / 1000000` outputs `1e-06` in CPython while JS `String(0.000001)` yields `0.000001`. v0.12 formatter retained the JS fixed representation.
- **Precision-sensitive comparison:** the integer `9007199254740993` differs from float `9007199254740992.0`. Converting both to `Number` can make them appear equal.

These are testable deviations in v0.12's numeric representation approach, not evidence of security compromise, real-world superintelligence or novel language superiority.

## v0.13 experimental method
1. Round exact BigInt ratios to IEEE-754 binary64 by integer quotient/remainder and ties-to-even, including subnormal numbers and signed zero.
2. Compare mixed integers and floats by converting binary64 to exact rational numerator/denominator, instead of rounding integer operands.
3. Normalize JS shortest-decimal strings to Python's scientific notation thresholds for intended display equivalence.
4. Add directed edge tests and seeded balanced large-integer ratios; preserve older cross-runtime arithmetic/branching/budget tests.
5. Run full GitHub Actions Python 3.11, 3.12, 3.13 + Node.js 22, and record failed runs as well as success.

## Threats to validity
- Python `repr` and JS Number.toString each use runtime formatting algorithms that might choose different shortest representations in carefully constructed boundary cases. Tests are evidence of sampled agreement, not a universal theorem.
- No independent formally proved BigInt-to-binary64 implementation is currently used.
- Signed-zero and negative quotient underflow need particularly careful treatment.
- A single-source JS implementation can share defects with its test data or with the Python behavioral oracle.
- No multi-operating-system comparison, runtime hardening, language performance benchmark or external peer review.

## Next research trajectory
Obtain an externally specified binary64 conformance corpus, mechanically check rounding invariants where feasible, add Rust/Go reference runtime, then design the newly invented practical programming language with domain-specific goals, fair benchmarks and educational material. The broader thesis and terminal engineering goals remain future deliverables.

**New SI mission 0/1,000,000; awarded points 0. Historical archive 996,667/1,000,000.**
