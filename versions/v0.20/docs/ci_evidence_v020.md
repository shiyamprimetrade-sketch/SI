# SI v0.20 — HTTP/Web integration GitHub CI evidence

**Tested code commit:** `36f0226092218ea2db10323ee985b1df826eb1e9`
**Workflow:** `.github/workflows/ci-v020.yml`
**Successful push run:** https://github.com/shiyamprimetrade-sketch/SI/actions/runs/39241370185

| Runtime | GitHub job | Tests | Conclusion |
|---|---:|---:|---|
| Python 3.11 + Node.js 22 | `118022739021` | 335/335 | SUCCESS |
| Python 3.12 + Node.js 22 | `118022738706` | 335/335 | SUCCESS |
| Python 3.13 + Node.js 22 | `118022738968` | 335/335 | SUCCESS |

**1,005 successful test executions**, no failed unittest methods and zero GitHub warning annotations in the three inspected jobs. v0.19 had 319 tests/version; v0.20 adds **16** test methods. Node.js runs JS syntax checks and inherited portable SI tests; it is not a new independent implementation of the typed AxiomFlow HTTP application.

### Validated functions
- Live loopback HTTP GET health and static HTML/JS/CSS tests.
- POST calculation of `{"price":"125.50","rate":"0.075"}` into typed AxiomFlow source, returning `{"currency":"USD","total":"134.91 USD"}`.
- 300 seeded price/rate cases independently compared with Python Decimal and half-even rounding.
- Invalid content type, malformed JSON, duplicate keys, unsupported routes, oversized input and changing successive request state tests.
- Hard-coded loopback bind restriction, restrictive same-origin CSP and no raw HTML injection from server results.
- Pinned module project CLI printed `134.91 USD` in CI.
- Previous bounded lexical obligation SHA256 `9997585eb832c9a59660a7ff3873c1e53a087a975b17a79198512aa36a30bd4d` reproduced on Python 3.11, 3.12 and 3.13.
- The prior exploratory Decimal benchmark continues to run, but **no fair new comparative language speed measurement** is claimed from it.

### Unverified and excluded
- No real visual browser automation, remote deployed domain, TLS, authentication, rate limiting, database, container, user accounts or production-grade security.
- No evidence that AxiomFlow independently implements the web server or frontend: both are hosted through Python stdlib and ordinary JavaScript.
- No end-to-end measurement showing superiority over C, C++, Java, JavaScript, Python, or existing web frameworks.
- No compiled production binary, ML integration, complete package manager, global formal proof or defended doctoral thesis.

The HTML/CSS/JS browser page and local HTTP API are development demonstrations. The tests validate HTTP and static responses, but do **not** constitute a publicly deployed or browser-automation-verified release.

**Score:** Starting user-authorized self-assessed SI project 2,400/1,000,000, v0.20 provisional incremental +900 points, new total **3,300/1,000,000**. Historical archival **996667/1,000,000** unchanged. Not an intelligence measurement.
