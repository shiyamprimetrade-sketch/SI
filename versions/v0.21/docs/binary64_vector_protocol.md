# SI v0.14 — Numerical evidence protocol and machine-checkable obligations

## Protocol
The standalone Node numeric probe `js/numeric_probe.js` accepts a JSON array of bounded commands:

- `{"kind":"ratio","a":"<signed decimal>","b":"<nonzero signed decimal>"}`: calculate integer true division with exact BigInt rounding to binary64. Successful response gives 16-digit big-endian hexadecimal binary64 `bits` and CPython-style decimal `text`.
- `{"kind":"bits","hex":"<16 hex digits>"}`: decode an IEEE binary64 representation, rejecting NaN and infinities; return the same bit pattern and decimal display.
- `{"kind":"compare","integer":"<signed decimal>","hex":"<16 hex digits>"}`: compare exact BigInt integer to a finite IEEE binary64 value. Returns -1, 0 or +1.

Python's independent test oracle derives expected binary64 bits with `float(Fraction(a,b))` and `struct.pack('>d')`. It handles negative zero explicitly because `Fraction(0)` does not have a sign. Expected decimal text is `str(float)`.

## Boundary vectors
Explicitly exercise 0x0000000000000000, 0x8000000000000000, 0x0000000000000001, 0x000fffffffffffff, 0x0010000000000000, 0x3ff0000000000000, 0x7fefffffffffffff, NaNs/infinities. Check tie-to-even with (2^53+1)/2^53 and 1/2^1075. Check mixed int/float comparisons across 2^53.

## Executable obligations
- For every tested finite ratio, bit-precise expected and observed binary64 values are equal.
- For every tested finite raw bit vector, round-trip bits are conserved; decimal strings agree with tested Python reference printing.
- Every tested huge BigInt vs finite float comparison agrees with the exact `Fraction(float)` reference.
- `shrink_ratio` applied to a known reproducing predicate preserves reproduction while reducing decimal size; greedy local reduction is **not** global minimization.
- The inherited v0.13 full regression suite and SI-Portable-1 bounded lexical digest remain unchanged.

**No universal theorem is proved.** Tests must run under real Node.js and GitHub Python 3.11–3.13.
