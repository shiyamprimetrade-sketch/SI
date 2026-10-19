# SI v0.15 — Bounded executable IEEE-754 obligations

For rational R=a/b, b≠0, and candidate finite binary64 f, let f↓=nextafter(f,−∞) and f↑=nextafter(f,+∞). The **nearest obligation** requires the exact rational distance |Fraction(f)−R| to be no greater than the distance to either finite neighbor. The **ties-to-even obligation** requires an even low significand bit when distances tie. These are local properties checked on tested finite candidates, not a universal mechanically proved result.

**Signed zero:** when the rounded result is zero, its sign must match the quotient sign, including a zero numerator. Fraction(0) alone cannot retain this sign.

**Domain limitations:** nonfinite overflow is handled by separate v0.14 tests. Candidate outputs are obtained from the Node VM, while Python independently checks using Fraction, struct and math.nextafter.

**Counterexample shrinking:** deterministic digit-removal and small candidates may be accepted only when the failure predicate stays true and a published rank strictly decreases; predicate calls are capped. Greedy results are locally smaller, not globally minimal.

**Negative control:** an intentionally wrong value f=1.0 for R=1+2^-51 must be rejected.

No host sandbox, universal language equivalence proof or intelligence measurement is claimed.
