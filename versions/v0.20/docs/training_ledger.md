# SI v0.20 — Evidence-based self-assessed SI score

| Ledger | Score |
|---|---:|
| Historical simulation archive | **996667 / 1000000**, unchanged |
| New SI project before v0.20 | 2400 / 1000000 |
| Incremental v0.20 award | **+900** |
| **New SI cumulative project score** | **3300 / 1000000** |
| Remaining to evidence-gated 100,000 milestone | **96,700** |

## Provisional 900-point award for **new v0.20 work only**
| Criterion | Points | Evidence |
|---|---:|---|
| Real localhost HTTP API executing existing statically typed AxiomFlow monetary function | 350 | `axiomflow/api.py`, live HTTP integration tests |
| Browser frontend using HTML/CSS/JavaScript and same-origin API | 200 | `web/index.html`, `web/app.js`, `web/style.css` and tested GET |
| New tests: 16 methods, 300 independently seeded Decimal cases, HTTP error classes and multi-request checks | 200 | `tests/test_http_api.py` and real CI |
| Explicit loopback, bounded JSON, duplicate input and content-type validation, CSP/nosniff headers | 100 | `axiomflow/api.py`, adversarial tests |
| Reproducible API contract/development launch guide, course lesson 16, threat-model research note | 50 | `README.md`, `docs/api_contract.md`, `docs/research_v020.md`, course |
| **Total** | **900** | [Verified CI 39241370185](https://github.com/shiyamprimetrade-sketch/SI/actions/runs/39241370185) |

CI: Python 3.11, 3.12, 3.13 + Node.js 22 each passed 335 tests. **1,005 successful unittest executions**, zero workflow warnings in inspected logs. Pinned-project demo printed `134.91 USD`; inherited lexical digest reproduced.

## Scoring boundaries
- No second award for existing AxiomFlow typing, functions, local pins, the inherited SI VM, or prior CLI.
- No points for independently compiling backend/frontend in AxiomFlow, deployed public service, real browser automation, TLS/auth, database, ML frameworks, universal language superiority or complete PhD thesis.
- v0.20 is progress toward the **backend/API/frontend** gate of the 100,000-point conditional rubric, **not completion of its full gate**.
- Score is subjective, auditable project-progress self-assessment; it does not represent new model training, an intelligence change or external scientific certification.
