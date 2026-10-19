# SI v0.19 — Executable typed functions and deterministic local builds

## Baseline review
SI v0.18 draft PR #14 passes Python 3.11/3.12/3.13 CI and uses parse-once AST execution for the previous expression interpreter. The 100,000-point gate rubric is cumulative and conditional.

## New hypotheses
H1. Adding declaration types and a pre-execution type pass rejects currency mistakes earlier and more predictably than runtime-only evaluation.
H2. Offline dependency content hashes enable a deterministic, auditable source resolution contract without network installation.
H3. A module-limited API is an observable, testable improvement in language expressivity without equating that to better performance or safety.

## Implemented experiment
A separately bounded `axiomflow.typed` parser/inference/evaluation path supports user functions and local namespace imports. A manifest loader verifies strict shape, file paths, SHA-256 digests and duplicate entries, then evaluates with sorted module names. Unit tests use seeded Python Decimal expected amounts, type-negative cases, symlink/path/traversal tampering, and CLI subprocesses.

## Limits and negative findings
There is no dependency installation, lockfile standard, transitive module import, general type polymorphism, bytecode emission, async I/O, HTTP service, web UI, ML compiler or system-terminal implementation yet. Module integrity is not process sandboxing. No large cross-language benchmark or developer productivity study establishes an advantage over Python, Java, C, C++, Rust or JavaScript. Negative CI outcomes must be kept in the evidence record.

## Ten-day accelerated project
Next implement a real HTTP API example and frontend, then ML/data interoperability; run fair controlled comparisons only after matching workloads and outputs. Prioritize a publishable small working language rather than claims of universally winning every workload. A completed doctoral thesis and independently reviewed findings remain separate future gates.
