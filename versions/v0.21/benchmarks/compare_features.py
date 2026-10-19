"""Reproducible *experimental* timing of exactly equal AxiomFlow/Decimal features.

This is still NOT a matched cost benchmark: AxiomFlow reparses/checks source,
while the Python baseline directly evaluates Decimal arithmetic.
"""
import argparse
from decimal import Decimal
import json
import statistics
import sys
import time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from axiomflow.data import feature_axiomflow,feature_decimal_reference


def median_ns(fn,iterations,repeats):
    results=[]
    for _ in range(repeats):
        start=time.perf_counter_ns()
        for _ in range(iterations):
            fn()
        results.append((time.perf_counter_ns()-start)/iterations)
    return round(statistics.median(results),2)


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--iterations",type=int,default=100)
    p.add_argument("--repeats",type=int,default=3)
    args=p.parse_args()
    if not (1<=args.iterations<=10000 and 1<=args.repeats<=30):
        p.error("invalid benchmark limits")
    cases=[("125.50","0.0750"),("1.00","0.1250"),
           ("999999.99","0.0001"),("17.25","0.2500")]
    for price,rate in cases:
        assert feature_axiomflow(price,rate)==feature_decimal_reference(price,rate)
    idx=0
    def axiom():
        nonlocal idx
        price,rate=cases[idx%len(cases)]
        idx+=1
        return feature_axiomflow(price,rate)
    def decimal():
        nonlocal idx
        price,rate=cases[idx%len(cases)]
        idx+=1
        return feature_decimal_reference(price,rate)
    # Both use identical deterministic case sequence from a reset index.
    idx=0; a=median_ns(axiom,args.iterations,args.repeats)
    idx=0; d=median_ns(decimal,args.iterations,args.repeats)
    print(json.dumps({"iterations":args.iterations,"repeats":args.repeats,
        "axiomflow_ns_median":a,"python_decimal_ns_median":d,
        "results_parity":"verified_on_four_cases",
        "warning":"NOT cost-equivalent: AxiomFlow includes parsing, typechecking and execution; direct Decimal does not. No cross-language superiority claim."},
        sort_keys=True))


if __name__=="__main__":
    main()
