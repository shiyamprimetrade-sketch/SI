# SI v0.25 — Unified AxiomFlow entrypoint and independent relational source validation

This snapshot **adds a single strict entrypoint** for existing scalar/functions and table/relational programs. It is a *mode-dispatching interface*, **not yet** a mathematically unified syntax or a language able to mix scalar `let` and table statements in one scope. Mixed-mode programs are explicitly rejected.

Run from `versions/v0.25`:
```sh
python -m axiomflow.unified examples/filtered_table.af --csv data/landed_cost.csv
python -m axiomflow.unified example.af
python -W error -m unittest discover -s tests -v
python benchmarks/unified_relational.py
python -m tools.package_source --output /tmp/axiomflow-v025.zip
```
Scalar source supports existing statically checked typed functions; table mode supports v0.24 validated filtering, derived expressions, sorting, column selection, summaries and typed function declarations. A compiled table plan can run repeatedly without reparsing; the scalar mode currently reruns the existing typed parser and is documented as such.

New independent Node.js `js/relational_runtime.js` implements a deliberately **limited table source subset** using BigInt cents, and Python tests compare entire output objects on 200 seeded program+dataset samples, plus empty filter sets and rounding cases. Unsupported syntax is rejected.

`tools/table_batch.py` runs identical source/data JSON batches as the JavaScript counterpart, and `benchmarks/unified_relational.py` compares end-to-end process timings with output equivalence checked **before** timing. This is a comparative workload result, not proof of general language speed superiority. Source packaging incorporates the new unified module, JS runner and Python batch adapter.

The repository's branch `main` is not altered. Previous version directories and legacy score remain intact. New self-assessed SI score at entry is **6250/1000000**, historical archive **996667/1000000** unchanged.
