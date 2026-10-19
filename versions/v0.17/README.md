# SI v0.17 — Executable AxiomFlow alpha and terminal prototype

A real, intentionally narrow deterministic monetary DSL written in Python. It is **not a universal replacement** for Python, C, C++, Java, JavaScript, Rust, or any other language, and no broad speed or functionality superiority is claimed.

## Run from versions/v0.17
```sh
python -m axiomflow example.af
python -m axiomflow --eval 'emit 2.00 USD + 3.00 USD'
python -m axiomflow # interactive terminal, :quit to exit
python -W error -m unittest discover -s tests -v
python benchmarks/compare_decimal.py --iterations 1000 --repeats 5
```

**Supported:** `let`, `emit`, Decimal literals and `12.34 USD` monetary literals, + - * /, parentheses, unary -, deterministic half-even 2-place money rounding, immutable bindings, explicit mismatched currency rejection and bounded input.

**Unsupported:** functions, imports, dependency installation, a compiler, app/frontend/backend/API/ML platform, typed multidimensional money conversion, security sandbox, true standalone terminal or demonstrated universal superiority. CPython hosts execution.

See `docs/ten_day_sprint.md` for October 19–29 goals, `courses/lesson13_axiomflow_alpha.md` and `docs/thesis_outline_v017.md`. **New SI score before milestone:** 950/1,000,000. Historical archive: 996667/1,000,000.
