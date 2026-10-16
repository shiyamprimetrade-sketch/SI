# SI v0.11 — Verified GitHub CI and cross-runtime evidence

## Source and review
- Parent: v0.10 stacked draft PR #6, head `6560820936627965170d62a3ca7d9b43a060f8a4`.
- Proposed stacked draft: PR #7, base `si-v0.10-portable-lexer-20261016`.
- Tested code commit: `1faa6ff03cf0d0e43a9e0e00fe8b4fbb6a865bea`.
- GitHub Actions run: https://github.com/shiyamprimetrade-sketch/SI/actions/runs/38904702299
- Workflow: `.github/workflows/ci-v011.yml`.
- Job command from `versions/v0.11`: `python -W error -m unittest discover -s tests -v`.

## Verified results (2026-10-16)

| Python | GitHub job ID | Result | Test count |
|---|---:|---|---:|
| 3.11 | `116985238178` | Success | 217/217 |
| 3.12 | `116985238073` | Success | 217/217 |
| 3.13 | `116985238204` | Success | 217/217 |

**651 successful test executions; no unittest failures.** The three inspected job logs contained **no GitHub warning annotations**. The workflow ran `actions/setup-node@v7` with Node.js 22 alongside the three Python versions. Python compileall, JavaScript syntax checking, full regression tests, the bounded SI portable source obligations, and SI CLI smoke test completed through the successful workflow.

## Bounded obligation replication
The old v0.10 checker retained exactly the same SHA256 signature in each matrix job:

`9997585eb832c9a59660a7ff3873c1e53a087a975b17a79198512aa36a30bd4d`.

It checks 4,681 input strings length ≤4 over a declared eight-symbol alphabet (945 accepted, 3,736 rejected), **not** all source strings.

## New cross-language properties exercised
- A handwritten JavaScript scanner/parser/canonicalizer uses no Python `shlex`, compiler or reference imports.
- The Python differential suite runs Node in a subprocess and compares typed opcode, integer-as-decimal-string, resolved jump targets, and canonical renderings for accepted SI-Portable-1 programs.
- Reject/accept parity is exercised on quoted and Unicode forms, CRLF and bare CR, invalid identifiers, integer limits, comments and seeded corpora.
- The Node runtime in this cycle implements **parsing only**. No independent JavaScript VM was developed or tested.

## Failures, changes and limitations
- Initial workflow `actions/setup-node@v4` passed all tests but produced a Node.js 20 deprecation warning. Migrated to `actions/setup-node@v7`; the revised complete matrix passed without warning annotations.
- Initial generated 'valid' test corpus incorrectly formatted some negative numbers as `+-123`. Revised it to use explicit sign formatting `{a:+d}` and reran the complete CI matrix successfully.
- Finite differential tests and a reproducible digest do not amount to a proof of lexer equivalence for arbitrary inputs; both implementations may share specification misunderstandings.
- No measured speed claim, language novelty claim, full independent runtime, complete doctoral thesis, security sandbox or terminal invention.

**New SI mission score: 0/1000000; points awarded: 0. Historical archival score: 996667/1000000 (unchanged).**
