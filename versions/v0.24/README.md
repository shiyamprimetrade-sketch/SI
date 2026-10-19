# SI v0.24 — AxiomFlow relational table expressions and pure functions

New: executable schema-checked `filter` and `derive` statements in table source files, using the existing typed scalar/function expression parser and interpreter. This is a real language grammar integration but not an independent fully general SQL implementation.

```sh
cd versions/v0.24
python -m axiomflow.table_language examples/filtered_table.af --csv data/landed_cost.csv
python -W error -m unittest discover -s tests -v
python benchmarks/table_workload.py
python -m tools.package_source --output /tmp/axiomflow-v024.zip
```

Tests cover invalid statically typed expressions, pure-function calls, 250 independently expected Decimal cases and 200 separately implemented JavaScript fixed-point table comparisons. Benchmark outputs must match before timing; the Python/Node execution paths differ and include Node startup.

The source bundle now carries `js/table_reference.js` and `examples/filtered_table.af` alongside the previous AxiomFlow project and legacy research artifacts.

**Start-of-cycle new self-assessed SI project score:** 5450 / 1,000,000. **Historical archive:** 996667 / 1,000,000 (unchanged). Score updates require successfully verified real CI; 100,000 remains an evidence-gated long-term milestone.
