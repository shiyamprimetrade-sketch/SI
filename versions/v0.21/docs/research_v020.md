# SI v0.20 — Research notebook: End-to-end AxiomFlow API integration

## Hypothesis
An independently parsed, typed AxiomFlow monetary function can serve as the calculation engine of a reproducible local HTTP API and browser form. Demonstrating this would establish **vertical integration**, not performance supremacy over conventional backend frameworks.

## Methods
- Reuse `axiomflow.typed.evaluate_typed` from v0.19; avoid rewriting monetary semantics in the server handler.
- Implement a minimal Python standard-library HTTP API, fixed static frontend, same-origin form and precise decimal-string JSON validation.
- Test actual HTTP over a loopback ephemeral port with a background test-server thread; test page assets, successful JSON, errors, malformed/oversized payloads, duplicate fields, path rejection and consecutive requests.
- Independently compare 300 seeded positive price/rate pairs with Python Decimal half-even oracle output, and retain the original 319-test inherited regression baseline.
- CI: Python 3.11/3.12/3.13, Node.js 22 syntax and legacy cross-runtime checks. Versioned logs and reproducibility.

## Known limitations and threats
AxiomFlow is the monetary expression engine; the webserver, HTTP protocol, static frontend and JSON parsing are implemented in standard Python/JavaScript. This does **not** demonstrate AxiomFlow can independently author all application layers, compile JavaScript/C/C++/Java, or outperform those languages.

A localhost proof of concept requires additional safeguards and testing for public internet deployment. The API lacks TLS, authentication, persistent storage, rate limiting, user sessions, telemetry and accessibility evaluation with actual assistive technology.

No scientific benchmark of throughput, allocations, developer experience, or secure-isolation performance against other programming languages has been completed here. No production-ready shell/terminal replacement, general package manager, ML framework or final defended PhD thesis has been achieved.

The short sprint's next gates are data/ML interoperability, a controlled fair benchmark suite, packaging/release and thesis-style consolidation.
