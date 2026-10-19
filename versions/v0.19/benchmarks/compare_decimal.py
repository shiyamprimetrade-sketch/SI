"""Exploratory separate parse+execute, repeated execute and Decimal baseline.

These are not a fair across-language benchmark; direct Python arithmetic does
less work than even AxiomFlow precompiled expression-tree interpretation.
"""
import argparse,json,statistics,sys,time
from decimal import Decimal,ROUND_HALF_EVEN
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from axiomflow import evaluate,compile_source,evaluate_compiled
SCRIPT="emit (125.50 USD + 18.25 USD) * 1.075"
def direct():
    v=(Decimal("125.50")+Decimal("18.25"))*Decimal("1.075")
    return format(v.quantize(Decimal(".01"),rounding=ROUND_HALF_EVEN),".2f")+" USD"
def measure(fn,n,r):
    samples=[]
    for _ in range(r):
        start=time.perf_counter_ns()
        for __ in range(n):fn()
        samples.append((time.perf_counter_ns()-start)/n)
    return {"median_ns_per_call":round(statistics.median(samples),2),"samples_ns":[round(x,2) for x in samples]}
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--iterations",type=int,default=1000)
    p.add_argument("--repeats",type=int,default=5)
    args=p.parse_args()
    if not 1<=args.iterations<=100000 or not 1<=args.repeats<=50:
        p.error("invalid benchmark limits")
    program=compile_source(SCRIPT)
    if evaluate(SCRIPT)!=evaluate_compiled(program) or evaluate(SCRIPT)!=[direct()]:
        raise RuntimeError("output disagreement")
    result={"warning":"Not cost-equivalent: interpreted AST vs Python direct arithmetic. No speed superiority claim.",
            "python":sys.version.split()[0],"iterations":args.iterations,"repeats":args.repeats,
            "source_reparse_each_call":measure(lambda:evaluate(SCRIPT),args.iterations,args.repeats),
            "preparsed_ast_execute":measure(lambda:evaluate_compiled(program),args.iterations,args.repeats),
            "direct_python_decimal":measure(direct,args.iterations,args.repeats)}
    print(json.dumps(result,indent=2))
if __name__=="__main__":main()
