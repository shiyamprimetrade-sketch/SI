# SI v0.11 — Cross-runtime parser research note

**Research claim examined:** Can two independently implemented parsers (Python and JavaScript) accept the same strict ASCII profile and produce equivalent typed instruction programs?

### Baseline reviewed
v0.10 draft PR #6, head `6560820936627965170d62a3ca7d9b43a060f8a4`, completed Python 3.11/3.12/3.13 CI. Its finite bounded corpus contained 4681 candidates (945 accepted). v0.10 had no independent non-Python parser.

### Independent implementation
`js/portable.js` is handwritten, with independent character validation, whitespace/comment scanner, instruction table, label resolver, `BigInt` integer conversion and canonical emitter. Input is a JSON list and output a JSON list of classification/signatures. Python conformance tests spawn Node rather than importing JavaScript logic.

### Testable hypotheses
- H1: Valid accepted SI-Portable-1 programs yield identical opcode, operand, target and canonical normal form across runtimes.
- H2: Both reject hostile lexical variants (CR-only, Unicode in comments, source-length cap, malformed integers/labels).
- H3: Existing SI execution results and v0.10 parser proof-obligation digest remain unchanged.

### Reproducible protocol
From `versions/v0.11`:
`python -W error -m unittest discover -s tests -v`; `python -W error -m si.obligations`; `node --version`; `python -m si examples.si`. Node is required in GitHub's v0.11 matrix; when unavailable locally, cross-runtime tests skip visibly and cannot be counted as verified.

### Threats
- Both parsers use similar manually translated specification; conceptual misunderstandings can affect both.
- Python and Node may differ in Unicode code-point indexing, decimal parsing, error classification and exceptions.
- `BigInt` is independently implemented at language runtime level; this is not a formal proof of bignum conformance.
- IPC via JSON could introduce encoding issues. The tests are not an adversarial process sandbox or a JSON API security audit.
- This is finite conformance, not certified portability of arithmetic execution, compiler correctness or performance. No PhD thesis, original universal language or terminal invention is claimed.

### Roadmap
Next: formal parser-state transition invariants; richer mutation/fuzzing with independent corpus generator; machine-checkable CFG properties; second-runtime VM; realistic cross-language microbenchmarks with baselines; language invention proposal, curriculum and later thesis/terminal research.

**New SI score: 0 / 1,000,000; new points 0. Historical archive 996,667 / 1,000,000.**
