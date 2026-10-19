# SI doctoral research notebook — v0.10 portable lexical profile

**Document type:** incremental research notebook suitable for later doctoral-level elaboration, not a completed, defended, or peer-reviewed PhD thesis. **Focus:** reproducible semantics and portable source grammar as prerequisites for credible language invention.

## Research objective

The existing SI training language is built with Python's `shlex` tokenizer, which allows behavior specific to that library and its host runtime. Independently implementing a second parser enables a falsifiable portability claim for an explicitly restricted source profile, without altering the existing program behavior. This is conventional language-engineering research, not an assertion of original theoretical invention.

## Hypotheses

**H1 — deterministic profile parsing.** For a valid ASCII portable source under the resource caps, the independent scanner produces the same instruction sequence/label resolutions as the legacy compiler, up to source-line metadata and retained symbolic jump names.

**H2 — canonical structural preservation.** For accepted inputs, canonical rendering followed by parsing preserves typed instruction values and resolved targets, and applying canonicalization twice does not change the result.

**H3 — execution conformance.** On portable sources for which execution returns successfully within a bounded budget, the interpreter, compiler VM and independent v0.9 small-step model agree on observable `output`, `stack`, and `steps`.

**H4 — strict boundary.** Inputs with non-ASCII comments, shell-style quoting and nondecimal Python integer separators may remain valid for the legacy parser while being rejected by the portable profile. This narrowing is intentional; it is not a backward-compatible replacement.

## Experiments and methods

1. Enumerate all short strings over a fixed 8-character alphabet (length <= 4). Record total accepted/rejected, stable SHA256 digest and minimal failing counterexamples.
2. Generate 1,500 grammar-based seeded canonical round-trip examples, 1,200 arithmetic cases, 700 branches, and 400 whitespace/comment metamorphic examples with recorded deterministic seeds. Compare the portable parser against `compile_source` and source/VM/reference runtime results.
3. Exercise both positive and negative grammar boundaries: source caps, 1200-digit literals, 64-character identifier cap, zero and negative literals, CRLF normalization, bare CR, ASCII controls, non-ASCII comments, quote/escape sequences, missing labels and dead code.
4. Run complete inherited SI test suites and new v0.10 tests on Python 3.11, 3.12 and 3.13. Preserve logs, commit SHA, GitHub Actions run IDs and any failures.
5. In a later phase, implement a second independent non-Python parser and a host-independent numeric model to reduce common-mode errors.

## Preliminary counterexample to broad portability claims

`PUSH "17"` is accepted by the legacy `shlex` tokenizer; SI-Portable-1 rejects the quote characters. A comment containing non-ASCII text is likewise excluded by the new profile. Consequently we must **not** claim the second parser reproduces all behavior of v0.9: the claim concerns the documented portable subset only. The experiment motivates precise and testable language profiles.

## Threats to validity

- The new parser and old compiler execute on CPython, so runtime independence is limited; `shlex` and new scanner differ by design outside the portable profile.
- Corpus enumeration is exhaustive only over a tiny bounded input alphabet. It does not prove correctness of arbitrary programs, full Unicode processing, or all numeric values.
- Parser/compiler agreement can be misleading if both use the same host libraries for `int()` and execution. Further cross-language implementation and stronger arithmetic/semantics models are required.
- The grammar constrains source format, not secure execution. No claim of sandbox isolation, arbitrary-code prevention under hostile Python object injection, or bounded process CPU/RAM is justified.
- No performance superiority is established against other programming languages; speed/energy/portability tradeoffs will require realistic comparable workloads and independent measurement.

## Next staged work

- v0.11: independently implemented non-Python lexer or a generated lexer plus differential tokenization tests, with explicit Unicode design alternatives.
- Subsequent: representation-independent bytecode serialization and type-soundness obligations; realistic application benchmarks across language families; design and evaluation of a separately named purpose-built language; complete education curriculum, doctoral-level thesis manuscript, and eventually an independently engineered terminal.

## Scoring and evidence governance

Retain historic 996667/1000000 as an archival simulation metric. New SI mission starts at **0/1000000** and stays there until the user approves transparent point-award rules with independently reproducible evidence. Passing tests does not automatically award points or constitute a universal proof or graduation.