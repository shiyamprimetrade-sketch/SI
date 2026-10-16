# SI v0.7 — Bounded numeric execution and resource accounting

SI remains a small experimental stack-language laboratory; its historical simulation ranking does **not** establish general or superhuman intelligence.

## Why this version
Reviewing [v0.6 PR #2](https://github.com/shiyamprimetrade-sketch/SI/pull/2) found numeric/resource gaps beyond the existing stack and step budgets. On CPython, dividing a sufficiently large integer by 1 raises `OverflowError`, and large integer-to-decimal rendering can raise `ValueError`. Both escaped the SI API rather than producing consistent `SIError`. Arithmetic could produce non-finite floating values; source, integer and cumulative output sizes had no explicit budgets.

## Implemented policy (fixed default caps)
- Source characters: **100,000**, rejected before splitting/tokenizing.
- Literal characters: **1,200** per integer `PUSH` token.
- Numeric integer bit length: **4,096** (checked at parse, stack pushes and after arithmetic).
- Bytecode instruction count: **50,000**.
- Total printed characters: **100,000** by default, configurable downward with `max_output_chars`; cumulative, not per `PRINT`.
- Existing `max_steps=10,000` and `max_stack=1,024` retained; nonsensical or negative budgets rejected.
- Division overflow and non-finite results raise `SIError`. A zero divisor remains `SIError('division by zero')`.
- Manually crafted bytecode cannot use non-integer `PUSH` args or invalid jump targets. This is **not** comprehensive bytecode validation.
- Shared numeric policy in `si/limits.py` ensures interpreter and VM enforce identical limits; parser implementations remain separate. Sharing code is a testing limitation, since differential equality is not independent proof of the numeric helper.

## Test
From `versions/v0.7`:

```sh
python -W error -m unittest discover -s tests -v
python -m si examples.si
```

New `tests/test_numeric_boundaries.py` covers exceptions, caps, dead code, malformed bytecode, 1,000 seeded numeric cases and 200 output-limit scenarios. GitHub Actions `.github/workflows/ci-v07.yml` runs on Python 3.11, 3.12 and 3.13.

## Important limits of this result
The caps are **engineering policy choices**, not proofs of bounded wall time, CPU, process memory, or secure isolation. The host process remains Python, and side-channel or environment limits are not modeled. Float behavior inherits CPython and platform semantics. Compile-time validation is still separate from execution-time budgets. No external formal verification, coverage-guided fuzzing, or hostile-input sandbox has been performed. No Python interpreter/runtime was upgraded on the user's desktop.

Stacked draft branch builds on v0.6, not on `main`. Do not merge without review.

**Simulation ledger:** historical **996667/1000000**, **new points 0**. The score is not an externally validated intelligence metric.
