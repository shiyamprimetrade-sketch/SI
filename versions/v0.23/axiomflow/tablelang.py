"""SI v0.23: executable, bounded AxiomFlow table-source sublanguage.

This is deliberately a separately parsed extension, NOT yet a unified scalar/
function/table grammar. No Python eval, file imports, side effects or loops.
"""
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
import json
import re

from .language import AxiomError
from .data import feature_precompiled
from .table import Table, Record

ID=r"[a-z][a-z0-9_]*"
TYPE=r"(?:USD|scalar)"
IDENT=re.compile(ID+r"\Z")
DECL=re.compile(rf"table\s+({ID})\s*\(\s*(.*?)\s*\)\Z")
ROW=re.compile(rf"row\s+({ID})\s*\(\s*(.*?)\s*\)\Z")
DERIVE=re.compile(rf"derive\s+({ID})\s+({ID})\s*:\s*(USD)\s*=\s*landed\(\s*({ID})\s*,\s*({ID})\s*\)\Z")
SELECT=re.compile(rf"select\s+({ID})\s+({ID}(?:\s*,\s*{ID})*)\Z")
SORT=re.compile(rf"sort\s+({ID})\s+by\s+({ID})\Z")
SUM=re.compile(rf"sum\s+({ID})\s+({ID})\Z")
LIT=re.compile(r"(0|[1-9][0-9]{0,6})\.[0-9]{2} USD\Z")
SCALAR=re.compile(r"(?:0|[1-9][0-9]{0,6})(?:\.[0-9]{1,4})?\Z")
MAX_ROWS=500
MAX_COMMANDS=2000
MAX_BYTES=100_000


@dataclass(frozen=True)
class TypedTableProgram:
    steps: tuple
    schema: tuple


def _columns(raw):
    columns=[]
    for field in raw.split(","):
        match=re.fullmatch(rf"\s*({ID})\s*:\s*({TYPE})\s*",field)
        if not match:raise AxiomError("invalid table field declaration")
        columns.append((match[1],match[2]))
    if not 1<=len(columns)<=16 or len(set(x[0] for x in columns))!=len(columns):
        raise AxiomError("invalid or duplicate table columns")
    return tuple(columns)


def _cells(raw, schema):
    rawcells=tuple(x.strip() for x in raw.split(","))
    if len(rawcells)!=len(schema):raise AxiomError("table row width mismatch")
    values=[]
    for text, (_,kind) in zip(rawcells,schema):
        if kind=="USD":
            if not LIT.fullmatch(text):raise AxiomError("expected USD cents literal")
            val=Decimal(text[:-4])
            if val>1_000_000:raise AxiomError("money value outside supported bounds")
        else:
            if not SCALAR.fullmatch(text):raise AxiomError("expected finite scalar")
            val=Decimal(text)
        values.append(val)
    return tuple(values)


def compile_table_source(source):
    """Parse and statically validate every instruction before any execution."""
    if type(source) is not str or len(source)>MAX_BYTES or not source.isascii():
        raise AxiomError("invalid table source")
    lines=source.splitlines()
    if len(lines)>MAX_COMMANDS:raise AxiomError("table command budget exceeded")
    schemas={}
    row_counts={}
    derived=set()
    steps=[]
    for n,raw in enumerate(lines,1):
        line=raw.split("#",1)[0].strip()
        if not line:continue
        try:
            if m:=DECL.fullmatch(line):
                name=m[1]
                if name in schemas:raise AxiomError("duplicate table declaration")
                schema=_columns(m[2])
                schemas[name]=schema
                row_counts[name]=0
                steps.append(("table",name,schema))
            elif m:=ROW.fullmatch(line):
                name=m[1]
                if name not in schemas:raise AxiomError("unknown table")
                if name in derived:raise AxiomError("rows after derived column rejected")
                row_counts[name]+=1
                if row_counts[name]>MAX_ROWS:raise AxiomError("table row budget exceeded")
                values=_cells(m[2],schemas[name])
                steps.append(("row",name,values))
            elif m:=DERIVE.fullmatch(line):
                name,column,currency,price,rate=m.groups()
                if name not in schemas:raise AxiomError("unknown table")
                schema=dict(schemas[name])
                if column in schema or len(schema)>=16:raise AxiomError("duplicate or excess derived column")
                if schema.get(price)!="USD" or schema.get(rate)!="scalar":
                    raise AxiomError("landed feature input type mismatch")
                schemas[name]=schemas[name]+((column,currency),)
                derived.add(name)
                steps.append(("derive",name,column,price,rate))
            elif m:=SELECT.fullmatch(line):
                name=m[1]
                if name not in schemas:raise AxiomError("unknown table")
                selected=tuple(x.strip() for x in m[2].split(","))
                if not selected or len(set(selected))!=len(selected) or any(x not in dict(schemas[name]) for x in selected):
                    raise AxiomError("invalid table projection")
                steps.append(("select",name,selected))
            elif m:=SORT.fullmatch(line):
                name,column=m.groups()
                if name not in schemas or column not in dict(schemas[name]):
                    raise AxiomError("invalid sort field")
                steps.append(("sort",name,column))
            elif m:=SUM.fullmatch(line):
                name,column=m.groups()
                if name not in schemas or column not in dict(schemas[name]):
                    raise AxiomError("invalid aggregate field")
                steps.append(("sum",name,column))
            else:
                raise AxiomError("unsupported table statement")
        except AxiomError as exc:
            raise AxiomError(f"table line {n}: {exc}") from None
    return TypedTableProgram(tuple(steps),tuple(sorted(schemas.items())))


def execute_table(program):
    """Run an already validated table program, with fresh per-call storage."""
    if type(program) is not TypedTableProgram:
        raise AxiomError("expected compiled table program")
    tables={}
    output=[]
    for step in program.steps:
        op,name,*args=step
        if op=="table":
            schema=args[0]
            tables[name]=Table(tuple(x[0] for x in schema),
                               tuple(x[1] for x in schema),())
        elif op=="row":
            tab=tables[name]
            if len(tab.records)>=MAX_ROWS:raise AxiomError("table row budget exceeded")
            values=args[0]
            tables[name]=Table(tab.columns,tab.types,tab.records+(Record(tuple(zip(tab.columns,values))),))
        elif op=="derive":
            column,price,rate=args
            tab=tables[name]
            records=[]
            for rec in tab.records:
                p=rec[price];r=rec[rate]
                result=feature_precompiled(f"{p:.2f}",f"{r:.4f}")
                records.append(Record(rec.fields+((column,result),)))
            tables[name]=Table(tab.columns+(column,),tab.types+("USD",),tuple(records))
        elif op=="sort":
            tables[name]=tables[name].sorted_by(args[0])
        elif op=="select":
            projection=tables[name].select(args[0])
            output.append({"kind":"table","name":name,"columns":list(projection.columns),
                           "types":list(projection.types),
                           "rows":[[str(value) for _,value in rec.fields] for rec in projection.records]})
        elif op=="sum":
            column=args[0]
            total=tables[name].sum_column(column)
            output.append({"kind":"sum","table":name,"column":column,
                           "type":tables[name].types[tables[name].columns.index(column)],
                           "value":str(total)})
        else:
            raise AxiomError("unrecognized compiled table operation")
    return output


def run_table_source(source):
    return execute_table(compile_table_source(source))


def main(argv=None):
    import argparse
    from pathlib import Path
    parser=argparse.ArgumentParser(description="AxiomFlow v0.23 bounded table source runner")
    parser.add_argument("file",type=Path)
    args=parser.parse_args(argv)
    try:
        source=args.file.read_text("ascii")
        result=run_table_source(source)
    except (OSError,UnicodeError,AxiomError,InvalidOperation) as exc:
        parser.exit(2,f"table error: {exc}\n")
    print(json.dumps(result,sort_keys=True,separators=(",",":")))


if __name__=="__main__":main()
