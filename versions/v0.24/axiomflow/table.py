"""AxiomFlow v0.22: immutable bounded table/record operations.

Host-language representation and validation, not new AxiomFlow grammar syntax.
Decimal rows remain immutable; stable sort and grouping are explicitly specified.
"""
from dataclasses import dataclass
from decimal import Decimal
from .language import AxiomError
from .data import PRICE, RATE, TARGET, MAX_ROWS, feature_precompiled

COLS=("price_usd","rate","observed_cost_usd")
OUT_COLS=("price_usd","rate","observed_cost_usd","landed_cost_usd")
TYPES=("USD","scalar","USD")
MAX_COLUMNS=16


@dataclass(frozen=True)
class Record:
    fields: tuple

    def __getitem__(self, key):
        for k,v in self.fields:
            if k==key: return v
        raise KeyError(key)


@dataclass(frozen=True)
class Table:
    columns: tuple
    types: tuple
    records: tuple

    def __post_init__(self):
        if (type(self.columns) is not tuple or type(self.types) is not tuple or
                type(self.records) is not tuple or not 1<=len(self.columns)<=MAX_COLUMNS or
                len(self.columns)!=len(self.types) or len(set(self.columns))!=len(self.columns)):
            raise AxiomError("invalid typed table schema")
        if any(type(r) is not Record or len(r.fields)!=len(self.columns) or
               tuple(k for k,_ in r.fields)!=self.columns for r in self.records):
            raise AxiomError("invalid typed record layout")
        if len(self.records)>MAX_ROWS:
            raise AxiomError("table row budget exceeded")
        if any(type(v) is not Decimal or not v.is_finite()
               for rec in self.records for _,v in rec.fields):
            raise AxiomError("invalid typed table value")

    def select(self, names):
        names=tuple(names)
        if not names or len(set(names))!=len(names) or any(x not in self.columns for x in names):
            raise AxiomError("invalid table projection")
        positions=[self.columns.index(x) for x in names]
        return Table(names,tuple(self.types[i] for i in positions),
                     tuple(Record(tuple(record.fields[i] for i in positions))
                           for record in self.records))

    def sorted_by(self, name):
        if name not in self.columns:
            raise AxiomError("unknown sort column")
        return Table(self.columns,self.types,
                     tuple(sorted(self.records,key=lambda r:r[name])))

    def sum_column(self, name):
        if name not in self.columns:
            raise AxiomError("unknown aggregate column")
        return sum((r[name] for r in self.records),Decimal(0))

    def augment_landed_cost(self):
        if self.columns != COLS or self.types != TYPES:
            raise AxiomError("landed-cost transformation expects source schema")
        transformed=[]
        for record in self.records:
            price=record["price_usd"];rate=record["rate"]
            amount=feature_precompiled(f"{price:.2f}",f"{rate:.4f}")
            transformed.append(Record(record.fields+(("landed_cost_usd",amount),)))
        return Table(OUT_COLS,TYPES+("USD",),tuple(transformed))


def from_validated_csv_rows(rows):
    if type(rows) not in (tuple,list) or len(rows)>MAX_ROWS:
        raise AxiomError("invalid table row collection")
    records=[]
    for row in rows:
        if (type(row) is not tuple or len(row)!=3 or
                any(type(x) is not str for x in row)):
            raise AxiomError("invalid record shape")
        price,rate,target=row
        if not PRICE.fullmatch(price) or not RATE.fullmatch(rate) or not TARGET.fullmatch(target):
            raise AxiomError("invalid record decimal format")
        p,r,t=Decimal(price),Decimal(rate),Decimal(target)
        if p>1_000_000 or r>1:
            raise AxiomError("record out of bounds")
        records.append(Record(tuple(zip(COLS,(p,r,t)))))
    return Table(COLS,TYPES,tuple(records))
