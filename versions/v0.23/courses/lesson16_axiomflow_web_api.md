# SI Course lesson 16 — Typed language execution behind HTTP and a browser

**Learning goals:** distinguish language semantics from host-runtime orchestration, define a precise HTTP contract, validate inputs at boundaries, and design real end-to-end reproducible tests.

## Practical steps
1. Trace request `{"price":"125.50","rate":"0.075"}` through the HTTP handler, strict parser, AxiomFlow type checker, Decimal runtime and JSON response. Derive result `134.91 USD`.
2. Run `python -m axiomflow.api --port 8000`, open the local browser app and verify same-origin `fetch` calls.
3. Submit invalid content-type, duplicate fields, malformed JSON, price exponent, negative amount and oversized body. Predict the appropriate HTTP status and test it.
4. Read the CSP and explain why `textContent` helps avoid DOM-based markup injection. Explain why these features do not alone make a secure server.
5. Design a cost-equivalent Python Decimal reference API with exactly the same parsing, typing and error behavior before making any comparative speed claim.

## Assessment (/10)
2 HTTP contract, 2 AxiomFlow integration, 2 negative validation, 2 end-to-end testing, 2 security and reproducibility limitations.

Course points are educational; no automatic award to SI project score.
