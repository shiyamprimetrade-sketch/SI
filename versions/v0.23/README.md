# SI v0.23 — Executable AxiomFlow table source

A narrowly scoped **executable language extension**, rather than only a Python Table API. Run the table CLI:
```sh
cd versions/v0.23
python -m axiomflow.tablelang examples/table.af
python -W error -m unittest discover -s tests -v
python -m tools.package_source --output /tmp/axiomflow-v023.zip
```

Table statements: `table name(column: USD, rate: scalar)`, `row name(1.00 USD,0.1250)`, `derive name cost: USD = landed(column, rate)`, `sort name by column`, `select name column,cost`, `sum name cost`. Results print deterministic JSON. Types and table fields are checked before execution. Up to 500 rows/table, 16 columns, 2000 lines, 100000 source characters; no file IO or Python eval in source programs.

This is a separate typed table grammar, **not yet a unified grammar** with scalar/function language. It uses Python host Table and Decimal execution. No general SQL, joins, dynamic user-defined table functions, full safety sandbox or demonstrated superiority over Python/C/Java is claimed.

All v0.22 source/tests are preserved in the prior directory. New package includes the table runner.
