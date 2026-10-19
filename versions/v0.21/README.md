# SI v0.21 — Reproducible AxiomFlow data + ML interoperability

This version connects AxiomFlow's **statically checked typed USD calculation** to a small CSV-to-machine-learning pipeline. It is not a native AxiomFlow machine-learning compiler or replacement for Python's established ML ecosystem.

## Run

From `versions/v0.21`:

```sh
python -m axiomflow.data data/landed_cost.csv
python -W error -m unittest discover -s tests -v
python benchmarks/compare_features.py --iterations 100 --repeats 3
python -m tools.package_source --output /tmp/axiomflow-v021.zip
```

The CSV has exact columns `price_usd,rate,observed_cost_usd`, decimal-string data, maximum 500 rows and 100 KB. The typed AxiomFlow function computes `price * (1 + rate)`; a separate Python Decimal implementation checks the values. Deterministic ordered first two-thirds training/remaining test split and exact-Decimal, one-feature ordinary-least-squares model produce slope/intercept/test mean absolute error. The nine-row synthetic example follows `observed_cost_usd = 2 * AxiomFlow_landed_cost + 5`, hence expected slope **2**, intercept **5**, test MAE **0**.

The data is **synthetic and intentionally perfectly linear**; this does not indicate real-world predictive accuracy. There is no scikit-learn or external library requirement and no deployed ML model endpoint.

The limited source package script creates reproducible timestamp-fixed ZIP bundles with a SHA-256 manifest. This is **not** a pip wheel, signed distribution, independent runtime, or full dependency installer.

The prior localhost web/API still works: `python -m axiomflow.api --port 8000`; never expose it publicly.

**Scoring:** initial new SI project score **3300/1000000**; award only incremental, CI-verified points. Historical archive **996667/1000000** remains separate.
