# SI v0.19 — Typed AxiomFlow functions and pinned local module projects

Introduces an **opt-in** typed function/module interpreter (`axiomflow/typed.py`) without breaking v0.18 AxiomFlow programs. Typed functions declare scalar or uppercase three-letter currency types, prohibit recursion, enforce call arity and return types, and evaluate with immutable local parameters. Local-only project manifests pin source SHA-256 digests and reject unsafe filenames, missing/surplus pins and symlinks.

## Run
```sh
cd versions/v0.19
python -m axiomflow --project project/axiomflow.json
python -W error -m unittest discover -s tests -v
python -W error -m si.obligations
```

The project CLI prints `134.91 USD`. A working language and CLI **do not** imply a secure execution sandbox, universal language performance superiority, complete package manager, full system terminal or finished thesis.

New course lesson 15, research notebook and 100,000-point milestone gate status accompany the release. Historical archive 996667/1000000 stays separate from the new user-authorized self-scored SI progress ledger.
