# SI v0.4 — Abstract types and reproducible comparisons

Experimental stack language built on SI v0.3. Adds forward abstract interpretation (`INT`, `FLOAT`, `NUMBER`), seeded differential/property-style tests, structured Python microbenchmark, GitHub Actions CI, thesis and lesson. No claim of superiority over Python or independent language invention.

Run from this folder:

```sh
python -W error -m unittest discover -s tests -v
python -m benchmarks.compare_python
python -m si examples.si
```

CI workflow is located in `.github/workflows/ci.yml` and should be published at repository root (not under `versions/v0.4`) to run on GitHub. It tests Python 3.11, 3.12 and 3.13. No CI pass is claimed until GitHub reports it.

Historical simulation score: 996667/1000000. New points: 0. This ledger is not a measurement of intelligence.