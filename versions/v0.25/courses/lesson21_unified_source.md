# SI course lesson 21 — One command, two checked modes, independent source interpreters

## Objectives
Distinguish a unified **CLI/dispatcher** from a genuinely unified grammar and type system. Describe static schema vs scalar typing, explain fixed-point cents and ties-even, and design defensible whole-process comparisons.

## Exercises
1. Run `python -m axiomflow.unified examples/filtered_table.af --csv data/landed_cost.csv`. Explain the table schema and result.
2. Run a typed scalar source with `fn twice(x: USD)->USD=x*2` and `emit twice(12.55 USD)` using the same CLI, **without** CSV.
3. Add a `let` inside a table script. Explain why rejecting unsupported mixed scope is safer than silently skipping the line.
4. Inspect the independent JS parser's supported source statements. Describe which Python AxiomFlow operations it *cannot* execute.
5. Compare Python and JS whole-process wall times only after checking all 40 source/data batch outputs. List four threats to inferring universal language speed.
6. Run the source packager twice, compare ZIP bytes and per-file SHA digests, and distinguish reproducibility from signed software supply chains.

## Assessment /10
3 parser/typing constraints; 2 independent conformance; 2 deterministic cents arithmetic; 2 benchmarking integrity; 1 science/safety limitations. Educational credit is separate from SI score.
