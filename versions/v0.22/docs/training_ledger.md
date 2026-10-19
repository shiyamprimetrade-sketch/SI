# SI v0.22 — Audited self-assessed engineering points

| Ledger | Points |
|---|---:|
| Historical simulation archive, unchanged | **996667/1000000** |
| New SI project before v0.22 | **3950/1000000** |
| **Incremental v0.22 award** | **+800** |
| **New SI project cumulative** | **4750/1000000** |
| Remaining to evidence-gated 100000 project milestone | **95250** |

## New v0.22 work awarded once
| Distinct evidence | New points | Verification |
|---|---:|---|
| Bounded immutable typed tables/records host operations, validated schemas and deterministic transforms | 250 | `axiomflow/table.py`, passing table tests |
| Cached parsed and statically checked typed AxiomFlow money feature, parity against v0.21 | 200 | `axiomflow/data.py`, no-reparse test and measured medians |
| New adversarial and seeded tests (17 new unittest methods/version; 400 triple-path cases) | 150 | `tests/test_typed_tables.py`, CI 39244404827 |
| Independent Node.js BigInt cent-based half-even comparator and 250 reproducible pairs | 100 | `js/fixed_cents.js`, `tests/test_js_fixed_cents.py` |
| Updated reproducible release ZIP includes typed table module and archive checks | 50 | `tools/package_source.py`, `tests/test_package_source.py` |
| Course lesson 18 and reproducible, failure-inclusive research/performance documentation | 50 | `courses/lesson18_typed_tables.md`, research and CI report |
| **Total new, provisional self-assessed points** | **800** | [Successful GitHub CI run](https://github.com/shiyamprimetrade-sketch/SI/actions/runs/39244404827) |

**Zero new points** for inherited 348 test methods, prior typed functions, original Decimal semantics, earlier source release, backend/web/ML demos and repetition of older results. First specialized workflow failure 39244247653 is documented; success was verified only after fix in commit `03a02f9ef5a3eff8bf2084a0128ecbe9382f5877`. A successful run is not a proof of general-purpose superiority. Formal grammar-level tables, secure production release, cross-language cost-equivalent benchmarks and completed thesis remain unearned.

The score is a subjective user-authorized project progress ledger, **not** evidence that underlying AI model weights or intelligence changed.
