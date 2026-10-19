# SI v0.15 doctoral-level research notebook — numeric verification

## Baseline and hypotheses
Review of SI v0.14 draft PR #10 confirmed 256/256 tests on Python 3.11, 3.12, 3.13 with Node.js 22, and self-assessed new SI score 500/1,000,000. Can the independent Node VM's binary64 outputs satisfy exact nearest-even inequalities for seeded and adversarial rational test cases, beyond just agreeing on output strings?

## Method
1. Build an exact-rational candidate checker using Python Fraction, math.nextafter and struct, independent of SI arithmetic internals.
2. Check ties near 1.0, zero/subnormal ties, subnormal-normal transitions and huge balanced quotient inputs, plus 250 reproducible rational neighborhoods (seed 151501).
3. Test a deliberately incorrect candidate to ensure the proof-obligation checker actually detects violations.
4. Implement a deterministic rank-decreasing, budget-limited counterexample reducer, tested on synthetic failures.

## Threats to validity
- Both programs share IEEE-754 hardware semantics. Python math/struct are independently used but are not a theorem prover.
- The invariant checker only covers the finite candidate subset tested, and it does not prove that the neighbor relation is implemented correctly for all float values.
- The reducer is greedy and does not establish a global minimum.
- No production discrepancy was discovered merely by writing these tests; any new failing CI must be reported rather than suppressed.
- Shortest-roundtrip decimal algorithms remain an independent ongoing challenge; the current version retains v0.14's numeric display rules and their existing tests.
- The broad SI plan—learn language families, invent a practical language, demonstrate scoped advantages, produce course and dissertation, and develop a terminal—has not yet been completed.

## Reproducibility
From versions/v0.15 run `python -W error -m unittest discover -s tests -v`, then `python -W error -m si.obligations`. Verify the three GitHub matrix job logs and record job IDs, failures and scores.

**Historic score 996667/1000000 preserved. New SI score starts v0.15 at 500/1000000; new points require a nonduplicative rubric and passing evidence.**
