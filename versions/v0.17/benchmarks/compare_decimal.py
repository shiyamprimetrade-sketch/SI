"""Exploratory comparison, not an apples-to-apples language benchmark."""
import argparse,json,statistics,sys,time
from decimal import Decimal,ROUND_HALF_EVEN
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from axiomflow import evaluate
SCRIPT="emit (125.50 USD + 18.25 USD) * 1.075"
def python_direct():
    v=(Decimal("125.50")+Decimal("18.25"))*Decimal("1.075")
    return format(v.quantize(Decimal(".01"),rounding=ROUND_HALF_EVEN),".2f")+" USD"
def measure(fn,n,r):
    data=[]
    for _ in range(r):
        start=time.perf_counter_ns()
        for i in range(n):fn()
        data.append((time.perf_counter_ns()-start)/n)
    return {"median_ns_per_call":round(statistics.median(data),2),"samples_ns":[round(x,2) for x in data]}
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--iterations",type=int,default=1000)
    p.add_argument("--repeats",type=int,default=5)
    a=p.parse_args()
    if not (1<=a.iterations<=100000 and 1<=a.repeats<=50):p.error("invalid limits")
    if evaluate(SCRIPT)!=[python_direct()]:raise RuntimeError("output mismatch")
    print(json.dumps({"warning":"NOT cost-equivalent; interpreter reparses each call",
        "python":sys.version.split()[0],"iterations":a.iterations,"repeats":a.repeats,
        "axiomflow":measure(lambda:evaluate(SCRIPT),a.iterations,a.repeats),
        "python_decimal_direct":measure(python_direct,a.iterations,a.repeats)},indent=2))
if __name__=="__main__":main()
