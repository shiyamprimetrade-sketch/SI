# SI research notebook v0.12 — Portable execution as a falsifiable hypothesis

## Research question
Can independent Python and JavaScript execution implementations agree on observable behavior of bounded, portable SI programs, beyond mere parsing parity?

## Hypotheses
- H1: bounded integer arithmetic, control-flow, output, state stack and step counts agree on an explicitly seeded domain.
- H2: signed-zero `0 / -3` survives both execution and string formatting, and resource-limit violations yield comparable SI error categories.
- H3: adversarial cases reveal deviations near floating-point conversion boundaries and source limits; all discovered divergences are recorded, rather than suppressed.

## Method
- Use handwritten JavaScript VM with BigInt integers and binary64 floats, and existing independently authored JavaScript scanner/parser.
- Compare to three Python execution models (source interpreter, bytecode VM, independent small-step evaluator).
- Execute on Node.js 22 and Python 3.11/3.12/3.13 in GitHub Actions.
- Preserve deterministic seeds and publish exact run IDs, failures, or warnings.
- Retain previous parser corpus digest and unit suites.

## Threats to validity
- Each runtime shares the host CPU's floating-point semantics; their numeral formatting algorithms differ and are not formally shown equivalent.
- Error-category comparison is intentionally coarser than exact error messages.
- Pure Python code runs in Linux CI; multi-OS/architecture parity is not established.
- The transport process is not a security sandbox; input string limits are language-level controls only.
- User's long-term challenge (learn language families, invent a new language, prove scoped advantages with fair benchmarks, teach it, publish doctoral-level technical thesis, build a terminal) remains future work and has not been completed by this experiment.

**New SI mission 0/1,000,000, points 0; historical archive 996,667/1,000,000.**
