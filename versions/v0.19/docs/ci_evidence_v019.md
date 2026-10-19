# SI v0.19 — Real GitHub CI and reproducibility report

**Code commit tested:** `5a7bb1582b4d8a09d26e212d60f4d7568342b44d`
**GitHub Actions:** https://github.com/shiyamprimetrade-sketch/SI/actions/runs/39239306041
**Workflow:** `.github/workflows/ci-v019.yml`, `versions/v0.19`

| Runtime | GitHub job | Unittest count | Status |
|---|---:|---:|---|
| Python 3.11 + Node.js 22 | `118015962524` | 319/319 | SUCCESS |
| Python 3.12 + Node.js 22 | `118015962629` | 319/319 | SUCCESS |
| Python 3.13 + Node.js 22 | `118015962280` | 319/319 | SUCCESS |

**957 passing unittest executions** (319 tests times three Python versions), no failures and zero GitHub warning annotations in inspected jobs. Earlier v0.18 had 295 tests/version; **24 new test methods** were added in v0.19. The Node.js 22 matrix ran syntax checks and previous cross-runtime tests, not a new independent AxiomFlow typed-language implementation.

The workflow also ran:
- `python -m axiomflow --project project/axiomflow.json`: **134.91 USD** in all three inspected job logs.
- Legacy SI CLI and previously specified bounded lexical obligations; SHA256 `9997585eb832c9a59660a7ff3873c1e53a087a975b17a79198512aa36a30bd4d` reproduced.
- The inherited exploratory `Decimal` benchmark harness. This version does **not** claim a speed advantage over Python, C, C++, Java or any other language.

## New tested features
- Function declaration parsing with explicit scalar/currency parameter and return types, qualified local module function calls, static type inference, forbidden recursion and duplicate/bad-arity rejection.
- 300 seeded Decimal-model outputs and deliberate type and malformed-source failure cases.
- Offline source-manifest format-1 strict schema, deterministic canonical lock digest, verified SHA-256 pins, path traversal/duplicate digest/symlink rejection, command-line project run and altered-dependency failure.
- Course lesson 15, versioned language specification and research notebook.

## Honest limitations and negative findings
- Modules are local-only and consist of pure functions; no transitive imports, package downloads, dynamic dependency resolution or general module system.
- Static checks are for restricted scalar/3-letter-money types; no global language soundness theorem and no typed VM on Node.
- File hashing protects against accidental/nonmalicious changes to pinned files; checking files then executing in the same process is not protection against hostile operating-system actors. **No security sandbox is claimed.**
- The v0.19 branch still lacks full web frontend, backend/API, ML interoperability, production terminal, comparative developer productivity trial, universal speed superiority and defended PhD thesis.
- All earlier PRs remain draft/unmerged, main unchanged.

**New SI score before v0.19:** 1700/1000000. Evidence-based provisional +700 award is recorded in `docs/training_ledger.md`; new cumulative 2400/1000000, leaving 97,600 to the conditional 100,000 milestone. Historical archived 996667/1000000 unchanged. Neither is a measurement of underlying model intelligence.
