# AxiomFlow lesson 19 — Defining a typed table sublanguage

Objectives: write a small language grammar, parse a source program into immutable operations, validate field-level schemas *before execution*, execute persistent table transformations and test against a separate fixed-point reference model.

Lab: (1) declare USD/scalar columns and insert three rows; (2) apply `derive ... landed`; (3) perform stable sort, select and sum; (4) submit mismatched typed columns, missing table, duplicate fields and a row after derivation to observe static errors; (5) seed 400 cent/basis-point samples and compare all outputs to integer division plus round-half-even.

Assessment /10: grammar 2, type checking 3, deterministic evaluation 2, independent oracle 2, scientific limitations 1. Educational score is not an SI engineering project score.
