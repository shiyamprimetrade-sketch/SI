"""AxiomFlow v0.21 reproducible CSV/ML interoperation.

A narrow, dependency-free data/ML pipeline, NOT a general ML framework.
The cost feature is computed by the existing typed AxiomFlow evaluator;
a deterministic Decimal OLS model is fitted on its output and compared to an
independently calculated Decimal feature baseline in the tests.
"""
import argparse
import csv
from decimal import Decimal, InvalidOperation, ROUND_HALF_EVEN, localcontext
from hashlib import sha256
import io
import json
from pathlib import Path
import re

from .language import AxiomError
from .typed import evaluate_typed, parse_function, static_check, execute_expression
from .language import Value

MAX_CSV_BYTES=100_000
MAX_ROWS=500
PRICE=re.compile(r"(?:0|[1-9][0-9]{0,6})\.[0-9]{2}\Z")
RATE=re.compile(r"(?:0|1)\.[0-9]{1,4}\Z")
TARGET=re.compile(r"-?(?:0|[1-9][0-9]{0,6})\.[0-9]{2}\Z")
MODULE_SOURCE="fn landed(price: USD, rate: scalar) -> USD = price * (1 + rate)\n"
HEADER=("price_usd","rate","observed_cost_usd")


def load_rows(data):
    if type(data) is not bytes or len(data)>MAX_CSV_BYTES:
        raise AxiomError("invalid CSV size")
    try:
        text=data.decode("ascii")
    except UnicodeDecodeError:
        raise AxiomError("non-ASCII CSV") from None
    if "\x00" in text or "\r" in text.replace("\r\n","\n"):
        raise AxiomError("invalid CSV control character")
    handle=io.StringIO(text, newline="")
    try:
        reader=csv.reader(handle, strict=True)
        headings=next(reader)
        if tuple(headings)!=HEADER:
            raise AxiomError("incorrect CSV header")
        out=[]
        for line in reader:
            if len(line)!=3 or len(out)>=MAX_ROWS:
                raise AxiomError("invalid CSV field count or row budget")
            price,rate,target=line
            if not PRICE.fullmatch(price) or not RATE.fullmatch(rate) or not TARGET.fullmatch(target):
                raise AxiomError("invalid dataset decimal")
            if Decimal(price)>1_000_000 or Decimal(rate)>1:
                raise AxiomError("dataset decimal out of bounds")
            out.append((price,rate,target))
        if len(out)<3:
            raise AxiomError("at least three data rows required")
        return tuple(out)
    except (csv.Error,StopIteration):
        raise AxiomError("invalid CSV structure") from None


def feature_axiomflow(price,rate):
    program=MODULE_SOURCE + f"emit landed({price} USD, {rate})"
    result=evaluate_typed(program)
    if len(result)!=1 or not result[0].endswith(" USD"):
        raise AxiomError("AxiomFlow feature shape mismatch")
    return Decimal(result[0][:-4])


# Function body is parsed and typechecked ONCE at module import, not for each row.
# The caller passes validated decimal strings; the per-call local map is fresh.
_LANDED = parse_function(MODULE_SOURCE.strip())
_LANDED_FUNCTIONS = {_LANDED.name: _LANDED}
static_check((), _LANDED_FUNCTIONS)


def feature_precompiled(price, rate):
    """Execute the already typechecked AxiomFlow function with new arguments."""
    if (type(price) is not str or type(rate) is not str or
            not PRICE.fullmatch(price) or not RATE.fullmatch(rate)):
        raise AxiomError("invalid typed feature input")
    if Decimal(price)>1_000_000 or Decimal(rate)>1:
        raise AxiomError("feature input outside supported bounds")
    with localcontext() as ctx:
        ctx.prec=50
        ctx.rounding=ROUND_HALF_EVEN
        args={"price": Value(Decimal(price),"USD"), "rate": Value(Decimal(rate))}
        result=execute_expression(_LANDED.body,args,_LANDED_FUNCTIONS)
        if result.currency!="USD":
            raise AxiomError("feature result type mismatch")
        return result.amount


def feature_decimal_reference(price,rate):
    """Separate host-language oracle: deliberately never calls AxiomFlow."""
    with localcontext() as ctx:
        ctx.prec=50
        ctx.rounding=ROUND_HALF_EVEN
        return (Decimal(price)*(Decimal(1)+Decimal(rate))).quantize(
            Decimal(".01"),rounding=ROUND_HALF_EVEN)


def _linear_fit(samples):
    """OLS with intercept using exact Decimal sums (no NumPy/sklearn)."""
    n=Decimal(len(samples))
    xs=[x for x,_ in samples]
    ys=[y for _,y in samples]
    sx=sum(xs,Decimal(0));sy=sum(ys,Decimal(0))
    sxx=sum((x*x for x in xs),Decimal(0))
    sxy=sum((x*y for x,y in samples),Decimal(0))
    denom=n*sxx-sx*sx
    if denom==0:
        raise AxiomError("constant feature prevents linear fit")
    slope=(n*sxy-sx*sy)/denom
    intercept=(sy-slope*sx)/n
    return slope,intercept


def analyze(data):
    rows=load_rows(data)
    with localcontext() as ctx:
        ctx.prec=50;ctx.rounding=ROUND_HALF_EVEN
        prepared=[]
        for price,rate,target in rows:
            computed=feature_precompiled(price,rate)
            direct=feature_decimal_reference(price,rate)
            if computed!=direct:
                raise AxiomError("interoperability reference mismatch")
            prepared.append((computed,Decimal(target)))
        # Stable order-preserving split: first floor(2n/3) train, rest test.
        cut=2*len(prepared)//3
        train,test=prepared[:cut],prepared[cut:]
        slope,intercept=_linear_fit(train)
        errors=[abs(y-(slope*x+intercept)) for x,y in test]
        mae=sum(errors,Decimal(0))/Decimal(len(errors))
        return {
            "dataset_sha256":sha256(data).hexdigest(),
            "rows":len(rows),"train_rows":len(train),"test_rows":len(test),
            "split_policy":"ordered first floor(2n/3) train, remaining test",
            "feature":"typed AxiomFlow landed-cost, USD rounded half-even",
            "model":"one-feature ordinary least squares with intercept (Decimal)",
            "slope":str(slope),"intercept":str(intercept),
            "test_mae":str(mae),
            "currency":"USD",
        }


def main(argv=None):
    parser=argparse.ArgumentParser(description="AxiomFlow reproducible local data/ML example")
    parser.add_argument("csv",type=Path)
    args=parser.parse_args(argv)
    try:
        if args.csv.stat().st_size>MAX_CSV_BYTES:
            raise AxiomError("invalid CSV size")
        report=analyze(args.csv.read_bytes())
    except (OSError,AxiomError,InvalidOperation,OverflowError) as exc:
        parser.exit(2,f"data error: {exc}\n")
    print(json.dumps(report,sort_keys=True,indent=2))


if __name__=="__main__":
    main()
