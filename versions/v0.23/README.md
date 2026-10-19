# SI v0.23 — Executable AxiomFlow table sublanguage

AxiomFlow now has executable **table statements** in `examples/table_summary.af`: `table costs = input`, `augment`, `select`, `sort`, `sum` and `emit`. The limited syntax is parsed and statically schema-checked by `axiomflow/table_language.py`. It is a separate table-program entrypoint, **not yet integrated into the legacy scalar/function grammar**. It operates on immutable typed host `Table` values built from bounded validated CSV rows.

## Reproduce
From `versions/v0.23`:
```sh
python -m axiomflow.table_language examples/table_summary.af --csv data/landed_cost.csv
python -W error -m unittest discover -s tests -v
python benchmarks/compare_precompiled.py --iterations 200 --repeats 3
python -m tools.package_source --output /tmp/axiomflow-v023.zip
```

Table statements operate on named input, not arbitrary source files. No dynamic imports, evaluation, IO or general expressions in table programs; file IO is exclusively the host CLI boundary. `sum` produces typed scalar/money output, `emit` generates a deterministic JSON-compatible row representation. The static checker rejects unbound tables, incorrect columns, projected-away columns and unknown operations before executing the program.

Includes 11 new test methods, seeded 250-case table evaluation with independent Decimal oracle, updated repeatable source ZIP and course lesson 19. The historical SI research snapshots remain present and unmerged. Existing numeric and JS fixed-point tests are preserved.

**Limits:** grammar is a specialized sublanguage; not a universal relational algebra, full SQL, general parser merger or secure execution sandbox. Fair performance comparison against Python/JS/C/C++/Java on fully equivalent table workloads remains future research.

New SI score starts at **4750/1,000,000** pending verified CI; historical archival score **996667/1,000,000** unchanged.
