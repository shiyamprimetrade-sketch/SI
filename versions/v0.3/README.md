# SI v0.3 — Verified bytecode control flow

SI is an experimental stack-based language implemented in Python. This release adds a conservative stack-height/type-domain verifier and reachable-code elimination. It does not establish superiority over Python.

Run tests: `python -m unittest discover -s tests -v`

Core APIs: `si.verify.verify(code)` and `si.verify.remove_unreachable(code)`.

Research: `docs/thesis_v03.md`; course: `courses/lesson03.md`.

Historical simulation ledger: 996667/1000000, zero new points. This is not an intelligence metric.