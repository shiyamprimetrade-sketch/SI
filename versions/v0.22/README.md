# SI v0.22 — Typed immutable tables and compiled monetary feature execution

**Experimental AxiomFlow research** based on the v0.21 stacked draft, preserving previous snapshots. This version adds an immutable host-API typed table model and a compiled-once monetary feature executor; neither adds table syntax to the AxiomFlow language grammar yet.

From `versions/v0.22`:

```sh
python -W error -m unittest discover -s tests -v
python -m axiomflow.data data/landed_cost.csv
python benchmarks/compare_precompiled.py --iterations 200 --repeats 5
python -m tools.package_source --output /tmp/axiomflow-v022.zip
```

New modules: `axiomflow/table.py` immutable `Table` and `Record` with typed columns USD/scalar, selection, stable sorting, sum and landed-cost augmentation; `axiomflow/data.py` has `feature_precompiled` which parses/checks `landed` once. `js/fixed_cents.js` is an independently implemented BigInt cent-level arithmetic comparator, checked against Python Decimal and AxiomFlow on seeded inputs.

The source ZIP includes `table.py`, retains deterministic timestamps and SHA-256 manifest; previous archives remain unchanged. Performance is reported with full parse/typecheck, compiled AxiomFlow, and direct Decimal measured separately, not an assertion of speed superiority.

**Limits:** table operations are Python host APIs, not in-language AxiomFlow table expression syntax; no production sandbox, genuinely cost-equivalent benchmarks across C/C++/Java/JS/Python or general-purpose ML system. AxiomFlow uses Python to execute. Do not claim universal superiority.

New SI self-assessed score entering v0.22: **3950/1,000,000**; historical archive: **996667/1,000,000**. Incremental award only after actual GitHub CI verification.
