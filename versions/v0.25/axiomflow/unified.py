"""AxiomFlow v0.25 single entrypoint for typed scalar or table programs.

This is a conservative source dispatcher with one explicit mode per program,
not yet a fully merged grammar or runtime; unsupported cross-mode programs
are rejected instead of silently executing an arbitrary subset.
"""
from dataclasses import dataclass
from pathlib import Path
import argparse
import json
import re

from .language import AxiomError
from .typed import parse_script, static_check, evaluate_typed
from .table_language import compile_table, execute_table
from .data import load_rows, MAX_CSV_BYTES

MAX_SOURCE=10000
MAX_LINES=100


@dataclass(frozen=True)
class UnifiedProgram:
    mode: str
    source: str
    schema: tuple
    compiled: object


def compile_program(source):
    if type(source) is not str or len(source)>MAX_SOURCE or not source.isascii():
        raise AxiomError("invalid unified source")
    if len(source.splitlines())>MAX_LINES:
        raise AxiomError("unified statement budget exceeded")
    code=[x.split("#",1)[0].strip() for x in source.splitlines()]
    code=[x for x in code if x]
    if not code:
        raise AxiomError("empty unified program")
    table_decl=any(re.fullmatch(r"table\s+[a-z_][a-z_0-9]*\s*=\s*input",x) for x in code)
    table_keywords=("table ","filter ","derive ","select ","sort ","augment ","sum ")
    if table_decl:
        if any(x.startswith(("let ","use ")) for x in code):
            raise AxiomError("scalar bindings/modules unsupported in table program")
        plan=compile_table(source)
        return UnifiedProgram("table",source,plan.result_schema,plan)
    if any(x.startswith(table_keywords) for x in code):
        raise AxiomError("table operation requires a table declaration")
    statements,functions,uses=parse_script(source)
    if uses:
        raise AxiomError("unified module loading requires pinned project runner")
    static_check(statements,functions)
    return UnifiedProgram("scalar",source,(),(statements,tuple(sorted(functions.items()))))


def execute_program(program, *, csv_bytes=None):
    if type(program) is not UnifiedProgram:
        raise AxiomError("expected compiled unified program")
    if program.mode=="table":
        if type(csv_bytes) is not bytes or len(csv_bytes)>MAX_CSV_BYTES:
            raise AxiomError("table mode requires bounded CSV bytes")
        return execute_table(program.compiled,load_rows(csv_bytes))
    if program.mode=="scalar":
        if csv_bytes is not None:
            raise AxiomError("CSV input not allowed in scalar mode")
        # Existing independently tested typed evaluator. Re-parsing on execute
        # is documented; table mode uses the reusable compiled plan.
        return evaluate_typed(program.source)
    raise AxiomError("unknown unified mode")


def run_program(source, *, csv_bytes=None):
    return execute_program(compile_program(source),csv_bytes=csv_bytes)


def main(argv=None):
    parser=argparse.ArgumentParser(description="AxiomFlow v0.25 unified source runner")
    parser.add_argument("source",type=Path)
    parser.add_argument("--csv",type=Path)
    args=parser.parse_args(argv)
    try:
        if args.source.stat().st_size>MAX_SOURCE:
            raise AxiomError("source size budget exceeded")
        text=args.source.read_text(encoding="ascii")
        csv_bytes=None
        if args.csv is not None:
            if args.csv.stat().st_size>MAX_CSV_BYTES:
                raise AxiomError("CSV size budget exceeded")
            csv_bytes=args.csv.read_bytes()
        result=run_program(text,csv_bytes=csv_bytes)
    except (OSError,UnicodeError,AxiomError) as exc:
        parser.exit(2,f"AxiomFlow unified error: {exc}\n")
    print(json.dumps(result,sort_keys=True,separators=(",",":")))


if __name__=="__main__":
    main()
