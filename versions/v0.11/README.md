# SI v0.11 — Grammar refinement and independent JavaScript parser

SI is an experimental educational stack-language and a stepping stone in the larger computer-science, programming-language invention, course, doctoral-research and terminal-design mission.

## Deliverables
- `docs/grammar_portability.md` refines the portable lexical grammar and machine-checkable conformance contract.
- `js/portable.js` independently implements SI-Portable-1 scanning, syntax checking, label resolution and canonicalization using JavaScript and `BigInt`. It does not execute programs or import SI's Python parser.
- `tests/test_cross_runtime_portable.py` runs Python↔Node differential cases, including randomized, adversarial and boundary samples.
- Retains the v0.10 bounded Python proof-obligation checker and older SI tests.
- `courses/lesson07_cross_language_parsers.md` and `docs/research_v011.md` extend coursework and the research notebook.
- `.github/workflows/ci-v011.yml` executes the full Python matrix and requires Node.js availability for the cross-runtime checks.

## Commands (from `versions/v0.11`)
```sh
node --version
python -W error -m unittest discover -s tests -v
python -W error -m si.obligations
python -m si examples.si
```

The JavaScript CLI expects JSON input representing an array of source strings and produces JSON results. Run: `printf '["PUSH 3"]' | node js/portable.js`.

### Limitations
Finite parser agreement is not a mathematical proof, nor is it evidence of full cross-language runtime compatibility. The Node program is a parser, not a production compiler/runtime, security sandbox, original new language or terminal. Do not infer superiority over every existing language.

**New SI project: 0 / 1,000,000; newly awarded 0. Archived historic simulation: 996,667 / 1,000,000.**
