# SI v0.20 — AxiomFlow HTTP API and local web application

This milestone adds a working **local-only** HTTP application powered by AxiomFlow's v0.19 statically checked monetary function semantics. It is not a production internet-facing service or a claim to beat existing web frameworks.

## Start the backend and frontend

From `versions/v0.20`:

```sh
python -m axiomflow.api --port 8000
```

Then browse **http://127.0.0.1:8000/**. The standard-library Python HTTP server serves a static HTML/CSS/JS form. Form submissions call `POST /api/v1/landed-cost`, passing exactly `{"price":"125.50","rate":"0.075"}`. The API validates values as decimal strings, invokes the typed AxiomFlow `tax(price: USD, rate: scalar) -> USD` function and returns `{"currency":"USD","total":"134.91 USD"}`.

To test without a browser:
```sh
curl -sS http://127.0.0.1:8000/health
curl -sS -X POST http://127.0.0.1:8000/api/v1/landed-cost -H 'Content-Type: application/json' -d '{"price":"125.50","rate":"0.075"}'
```

## Scope, validation, limitations

- HTTP/1.1-level features are limited; uses Python standard-library `ThreadingHTTPServer` and binds **loopback only**.
- Accepts exact JSON fields, string decimal syntax, bounded price/rate values, and a maximum 2,048-byte request body.
- Rejects duplicate JSON fields, incorrect MIME type, unsupported routes, unsafe bind addresses and out-of-range amounts.
- Frontend uses `textContent` (not `innerHTML`) for server output and a strict same-origin CSP. No remote scripts/dependencies.
- No authentication, TLS, reverse-proxy trust model, request-rate limiting, process isolation, multi-user accounts, database, or production deployment is implemented. **Do not expose this server publicly.**
- Frontend static files are included directly in the repo; this is not a general JS/CSS app compiler.
- The original `python -m axiomflow --project project/axiomflow.json` still runs the SHA-256-pinned local project demo.

## Reproducibility
```sh
python -W error -m unittest discover -s tests -v
python -m si.obligations
```
CI `.github/workflows/ci-v020.yml` tests Python 3.11–3.13 with Node.js 22.

**Scoring:** start from new-project 2,400/1,000,000; v0.20 award only after evidenced CI, without re-crediting v0.19 typing/modules. Historical archive 996,667/1,000,000 stays unchanged.
