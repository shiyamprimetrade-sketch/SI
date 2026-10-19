# AxiomFlow v0.19 — Typed-function and local-module specification

This prototype is a deliberately restricted expression-oriented financial DSL, not a general-purpose language.

## Grammar
```
main      := (use | function | let | emit | comment | blank)*
module    := (function | comment | blank)*
use       := 'use' NAME
function  := 'fn' NAME '(' parameters? ')' '->' TYPE '=' expression
parameters:= NAME ':' TYPE (',' NAME ':' TYPE)*
TYPE      := 'scalar' | THREE_UPPERCASE_ASCII_CURRENCY
let       := 'let' NAME '=' expression
emit      := 'emit' expression
expression:= signed literals | local names | qualified/local function calls
             | parentheses | unary minus | + - * / with standard precedence
```
Function and module names are lowercase ASCII identifiers. Monetary literals have exactly two fractional digits followed by a 3-letter uppercase currency. Scalar literals are ASCII decimal numerals. Expressions are parsed independently of Python `eval`.

## Static checks
Parameters have explicitly declared scalar/currency types, and return expressions must infer the declared type. Addition/subtraction require equal types; money×money and division by money are rejected. Calls require exactly matching argument count and types. Unknown identifiers, unbound functions, duplicate declarations, and direct/mutual recursion are rejected before any program output is returned. Top-level bindings are immutable.

## Runtime
Functions are pure, with call-local environments and no I/O. Currency values are rounded half-even to 2 digits after operations under the existing AxiomFlow Decimal policy. Total function declarations max 100; max 12 parameters and per-call argument count, and a secondary call-depth bound. The top-level interpreter retains old features separately.

## Module and build policy
The manifest is a UTF-8 JSON document with exactly `format`, `entry`, `modules`, `sha256`. Only format 1 is supported. An entry source declares `use module_name`; module names map to ASCII `[a-z][a-z0-9_]*.af` files in the manifest directory. Each local file's SHA-256 hash must match its pinned digest. No remote imports, network download, arbitrary filesystem paths, or dependency installation. Any surplus/unpinned digest and symlinked source is rejected. Modules may only declare functions; the initial version has no nested dependency graph.

`project_build` validates and executes, returning printed output, deterministic module order and canonical manifest lock digest. It is **not** a bytecode compiler or secure container.

## Reproducibility
The demo has `project/axiomflow.json`, `project/main.af` and `project/pricing.af`. Run:
```sh
cd versions/v0.19
python -m axiomflow --project project/axiomflow.json
```
Expected: `134.91 USD`.

No domain-wide superiority claim is supported by these semantics. Future work requires module namespaces, lockfile revision semantics, resource hardening, user-defined composite types, and independent implementation.
