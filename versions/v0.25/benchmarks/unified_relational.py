"""Output-equivalent whole-process Python vs Node relational source workload.

Both processes receive identical JSON batches and parse the same restricted
AxiomFlow table source. Measures launch/JSON/runtime together; not intrinsic
language speed. Runs small numbers of samples without statistical claims.
"""
import json
from pathlib import Path
import random
import shutil
import statistics
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[1]
NODE=shutil.which("node")

def make_batch():
    rng=random.Random(250250)
    batch=[]
    for _ in range(40):
        threshold=rng.randrange(0,120000)
        source=("table t = input\n"
                f"filter t where price_usd >= {threshold//100}.{threshold%100:02d} USD\n"
                "derive t adjusted_usd = price_usd * 1.10\n"
                "sort t by price_usd\n"
                "sum t.adjusted_usd\n"
                "select t (price_usd,adjusted_usd)\n"
                "emit t")
        rows=[]
        for _ in range(18):
            amount=rng.randrange(0,500000)
            rows.append([f"{amount//100}.{amount%100:02d}","0.1000","0.00"])
        batch.append({"source":source,"rows":rows})
    return batch

def once(command,payload):
    start=time.perf_counter_ns()
    completed=subprocess.run(command,input=payload,text=True,capture_output=True,
                             timeout=30,cwd=ROOT)
    elapsed=time.perf_counter_ns()-start
    if completed.returncode:
        raise RuntimeError(completed.stderr[:1200])
    return json.loads(completed.stdout),elapsed

def main():
    if NODE is None:
        raise SystemExit("Node.js 22 required")
    payload=json.dumps(make_batch(),sort_keys=True,separators=(",",":"))
    py=[sys.executable,"-m","tools.table_batch"]
    js=[NODE,str(ROOT/"js"/"relational_runtime.js")]
    pyval,_=once(py,payload)
    jsval,_=once(js,payload)
    if pyval!=jsval:
        raise RuntimeError("different outputs, benchmark aborted")
    samples={}
    for name,command in (("python_process",py),("node_process",js)):
        ns=[once(command,payload)[1] for _ in range(5)]
        samples[name]={"median_ms":round(statistics.median(ns)/1e6,3),
                       "samples_ms":[round(x/1e6,3) for x in ns]}
    print(json.dumps({"datasets":40,"rows_per_dataset":18,"output_equal":True,
        "units":"full-process wall time incl. startup, JSON and program parsing",
        "samples":samples,
        "limitation":"Implementations support identical constrained workload, not equivalent architecture or compiler maturity. Five samples, runner jitter; cannot claim language-wide superiority."},
        sort_keys=True))

if __name__=="__main__":
    main()
