# SI v0.26 — Conservative mixed AxiomFlow scalar/table scopes

SI v0.26 introduces a **bounded shared front end** for scalar/monetary binding AST nodes and table instructions. It is a research milestone, **not a complete merged compiler or independent JS general interpreter**.

```sh
cd versions/v0.26
python -m axiomflow.unified examples/mixed_table.af --csv data/landed_cost.csv
python -W error -m unittest discover -s tests -v
python benchmarks/unified_relational.py
python -m tools.package_source --output /tmp/axiomflow-v026.zip
```

New capability: up to **eight immutable `let` bindings** before the table input declaration, each a pure scalar or money expression supported by existing AxiomFlow typed expression grammar. The shared AST references the existing typed expression nodes, not string-substitution or Python eval. Bound values participate in schema-checked `filter`/ `derive` expressions and are carried in a compiled immutable plan. Table columns cannot be shadowed. Bindings after `table ... = input`, module loading, arbitrary Python effects, recursion and unsupported grammar are rejected. Existing scalar-only and table-only programs still work.

The independent Node.js relational comparator adds direct support for **literal** scalar/money mixed bindings in its bounded source subset; it is not a complete Node.js implementation of all AxiomFlow functions. Tests exercise 220 deterministic inlined-vs-bound cases plus 160 seeded Python/Node comparisons, adversarial syntax and budget cases. The benchmark runs the identical JSON workloads on Python and Node as whole processes, including startup overhead; it cannot rank language execution speed universally.

GitHub CI workflow `.github/workflows/ci-v026.yml` runs Python 3.11/3.12/3.13 with Node 22. Release ZIP includes the new mixed example; course lesson 22 and thesis-style research documentation are included.

**Scores before v0.26:** new self-scored SI engineering 7100/1000000, historic archived 996667/1000000. Points only for new evidenced work, not prior implementations.
