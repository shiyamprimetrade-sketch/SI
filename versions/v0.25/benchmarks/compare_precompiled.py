"""Within-Python matched-output microbenchmark; separate Node correctness test.

Timing uses the same four decimal values; operations are *not* cost-equivalent
because the full AxiomFlow path reparses/rechecks source each call.
"""
from decimal import Decimal
import json
import statistics
import time
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from axiomflow.data import feature_axiomflow,feature_precompiled,feature_decimal_reference

SAMPLES=(("125.50","0.0750"),("1.00","0.1250"),
         ("17.25","0.2500"),("999999.99","0.0001"))

def measure(fn,iterations=200,repeats=5):
    samples=[]
    for _ in range(repeats):
        begin=time.perf_counter_ns()
        for i in range(iterations):
            a,b=SAMPLES[i%len(SAMPLES)]
            fn(a,b)
        samples.append((time.perf_counter_ns()-begin)/iterations)
    return {"median_ns":round(statistics.median(samples),2),
            "samples_ns":[round(x,2) for x in samples]}

def main():
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("--iterations",type=int,default=200)
    p.add_argument("--repeats",type=int,default=5)
    args=p.parse_args()
    if not 1<=args.iterations<=10000 or not 1<=args.repeats<=20:
        p.error("invalid limits")
    for a,b in SAMPLES:
        if not (feature_axiomflow(a,b)==feature_precompiled(a,b)==feature_decimal_reference(a,b)):
            raise RuntimeError("benchmark output parity failed")
    result={
        "same_output":True, "iterations":args.iterations,"repeats":args.repeats,
        "reparse_typecheck_execute":measure(feature_axiomflow,args.iterations,args.repeats),
        "preparsed_typed_execute":measure(feature_precompiled,args.iterations,args.repeats),
        "direct_python_decimal":measure(feature_decimal_reference,args.iterations,args.repeats),
        "warning":"Different work: full parse/typecheck vs cached AST execution vs direct Decimal. No general language superiority or equivalent execution-cost claim."
    }
    print(json.dumps(result,sort_keys=True,indent=2))

if __name__=="__main__":
    main()
