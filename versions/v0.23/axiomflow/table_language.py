"""AxiomFlow v0.23 table sublanguage: actual parsed statements, bounded semantics.

This is a deliberately scoped *table program* grammar, separate from the
scalar/function parser. Input records come from validated CSV; no filesystem
access is permitted by the table program itself.
"""
import argparse
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
import json
import re
from .language import AxiomError
from .data import load_rows, MAX_CSV_BYTES
from .table import COLS, TYPES, OUT_COLS, Table, from_validated_csv_rows

IDENT=r"[a-z_][a-z0-9_]*"
NAME=re.compile(IDENT+r"\Z")
TABLE=re.compile(rf"table\s+({IDENT})\s*=\s*input\Z")
PROJECT=re.compile(rf"select\s+({IDENT})\s*\(\s*({IDENT}(?:\s*,\s*{IDENT})*)\s*\)\Z")
SORT=re.compile(rf"sort\s+({IDENT})\s+by\s+({IDENT})\Z")
AUGMENT=re.compile(rf"augment\s+({IDENT})\s+landed_cost_usd\Z")
SUM=re.compile(rf"sum\s+({IDENT})\.({IDENT})\Z")
EMIT=re.compile(rf"emit\s+({IDENT})\Z")
MAX_LINES=100
MAX_SOURCE_CHARS=10000
MAX_OUTPUT_ROWS=500


@dataclass(frozen=True)
class CompiledTable:
    steps: tuple
    result_schema: tuple
    result_types: tuple


def compile_table(source):
    """Check complete source and static table schema before executing any step."""
    if type(source) is not str or len(source)>MAX_SOURCE_CHARS or not source.isascii():
        raise AxiomError("invalid table source budget or encoding")
    if len(source.splitlines())>MAX_LINES:
        raise AxiomError("table line budget exceeded")
    steps=[]
    schema=None
    types=None
    var=None
    initialized=False
    for line_no,raw in enumerate(source.splitlines(),1):
        line=raw.split("#",1)[0].strip()
        if not line:
            continue
        if (match:=TABLE.fullmatch(line)):
            if initialized:
                raise AxiomError(f"line {line_no}: multiple table declarations")
            var=match[1]
            schema=COLS
            types=TYPES
            initialized=True
            steps.append(("input",))
            continue
        if not initialized:
            raise AxiomError(f"line {line_no}: table must be declared first")
        if (match:=PROJECT.fullmatch(line)):
            if match[1]!=var:raise AxiomError(f"line {line_no}: unknown table")
            columns=tuple(x.strip() for x in match[2].split(","))
            if len(set(columns))!=len(columns) or any(x not in schema for x in columns):
                raise AxiomError(f"line {line_no}: invalid projected column")
            types=tuple(types[schema.index(x)] for x in columns)
            schema=columns
            steps.append(("select",columns))
        elif (match:=SORT.fullmatch(line)):
            if match[1]!=var or match[2] not in schema:
                raise AxiomError(f"line {line_no}: unknown table/sort column")
            steps.append(("sort",match[2]))
        elif (match:=AUGMENT.fullmatch(line)):
            if match[1]!=var or schema!=COLS or types!=TYPES:
                raise AxiomError(f"line {line_no}: augmentation requires original schema")
            schema=OUT_COLS
            types=TYPES+("USD",)
            steps.append(("augment",))
        elif (match:=SUM.fullmatch(line)):
            if match[1]!=var or match[2] not in schema:
                raise AxiomError(f"line {line_no}: unknown table/aggregate column")
            steps.append(("sum",match[2],types[schema.index(match[2])]))
        elif (match:=EMIT.fullmatch(line)):
            if match[1]!=var:raise AxiomError(f"line {line_no}: unknown table")
            steps.append(("emit",))
        else:
            raise AxiomError(f"line {line_no}: unsupported table statement")
        if len(steps)>MAX_LINES:
            raise AxiomError("table statement budget exceeded")
    if not initialized or not any(op in ("sum","emit") for op,*_ in steps):
        raise AxiomError("table program must declare input and produce output")
    return CompiledTable(tuple(steps),schema,types)


def _display_amount(value, typ):
    if typ=="scalar":
        return format(value,"f")
    return f"{value:.2f} {typ}"


def execute_table(compiled, rows):
    """Execute a previously compiled table program with a fresh input table."""
    if type(compiled) is not CompiledTable:
        raise AxiomError("expected validated table program")
    table=from_validated_csv_rows(rows)
    output=[]
    for step in compiled.steps:
        op=step[0]
        if op=="input":
            continue
        if op=="select":
            table=table.select(step[1])
        elif op=="sort":
            table=table.sorted_by(step[1])
        elif op=="augment":
            table=table.augment_landed_cost()
        elif op=="sum":
            output.append({"operation":"sum","column":step[1],
                           "value":_display_amount(table.sum_column(step[1]),step[2])})
        elif op=="emit":
            if len(table.records)>MAX_OUTPUT_ROWS:
                raise AxiomError("output row budget exceeded")
            output.append({"operation":"emit","columns":list(table.columns),
                           "types":list(table.types),
                           "rows":[[_display_amount(value,typ)
                                     for (_,value),typ in zip(record.fields,table.types)]
                                   for record in table.records]})
        else:
            raise AxiomError("invalid compiled table operation")
    return output


def run_table(source, csv_bytes):
    compiled=compile_table(source)
    rows=load_rows(csv_bytes)
    return execute_table(compiled,rows)


def main(argv=None):
    parser=argparse.ArgumentParser(description="AxiomFlow table DSL experiment")
    parser.add_argument("source",type=Path)
    parser.add_argument("--csv",type=Path,required=True)
    args=parser.parse_args(argv)
    try:
        if args.source.stat().st_size>MAX_SOURCE_CHARS or args.csv.stat().st_size>MAX_CSV_BYTES:
            raise AxiomError("source/data size budget exceeded")
        result=run_table(args.source.read_text(encoding="ascii"),args.csv.read_bytes())
    except (OSError,UnicodeError,AxiomError) as exc:
        parser.exit(2,f"AxiomFlow table error: {exc}\n")
    print(json.dumps(result,sort_keys=True,separators=(",",":")))


if __name__=="__main__":
    main()
