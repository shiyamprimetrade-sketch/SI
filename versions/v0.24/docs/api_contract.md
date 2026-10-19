# AxiomFlow HTTP API v0.20 — Request/response contract

## POST /api/v1/landed-cost
```json
{"price":"125.50","rate":"0.075"}
```
- Request header: `Content-Type: application/json`.
- Exactly two JSON fields `price` and `rate`; duplicate keys rejected.
- `price`: nonnegative decimal string with exactly two fractional digits, no exponent syntax, maximum 1,000,000.00 USD.
- `rate`: decimal string between 0 and 1 inclusive, one to four fractional digits. Maximum 1.0000.
- Successful HTTP 200: `{"currency":"USD","total":"134.91 USD"}`.
- Monetary operations use AxiomFlow's typed `fn tax(price: USD, rate: scalar) -> USD = price * (1 + rate)` with its existing Decimal, half-even rounding semantics.

## GET /health
HTTP 200 with `{"engine":"AxiomFlow","status":"ok"}`.

## GET /, /app.js, /style.css
Serves fixed, version-controlled local frontend files. All other paths give 404; no directory listing.

## HTTP validation
- 400: malformed/duplicate-field JSON, incorrect price/rate, unsupported field names.
- 411: missing or invalid Content-Length.
- 413: Content-Length exceeds 2,048 bytes.
- 415: non-JSON MIME type.
- 404: unsupported endpoint.
- Response includes `X-Content-Type-Options: nosniff`, a strict CSP, cache-disabling header and explicit response length.
- There is no CORS wildcard; requests originate from the served same-origin frontend.

This is a finite, testable local demo API, *not* a public-facing secure service. Public deployment would require an independently audited, maintained server and reverse proxy with TLS, authentication, request limits, observability and operational controls.
