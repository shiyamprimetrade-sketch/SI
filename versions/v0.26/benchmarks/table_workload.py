"""Output-equivalent batch-table workload telemetry, deliberately exploratory.

Node subprocess spawn is included; Python executes precompiled plans in-process.
These are NOT cost-equivalent language performance timings.
"""
import json
import random
import shutil
import statistics
import subprocess
import sys
import time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from axiomflow.table_language import compile_table,execute_table

NODE=shutil.which("node")
JS=Path(__file__).resolve().parents[1]/"js"/"table_reference.js"

def main():
 if not NODE:
  raise SystemExit("Node 22 required")
 rng=random.Random(24026)
 batch=[]
 rows=[]
 for i in range(100):
  n=rng.randrange(0,100000)
  th=f"{n//100}.{n%100:02d}"
  prices=[rng.randrange(0,1000000) for _ in range(15)]
  batch.append({"minimum":th,"rows":[f"{x//100}.{x%100:02d}" for x in prices]})
  rows.append(tuple((f"{x//100}.{x%100:02d}","0.1000","0.00") for x in prices))
 programs=[compile_table(f"table t = input\nfilter t where price_usd >= {item['minimum']} USD\n"
   "derive t adjusted_usd = price_usd * 1.10\nsum t.adjusted_usd\n"
   "select t (price_usd,adjusted_usd)\nemit t") for item in batch]
 def python_batch():
  return [{"sum":v[0]["value"],"rows":v[1]["rows"]}
          for v in [execute_table(plan,row) for plan,row in zip(programs,rows)]]
 def js_batch():
  done=subprocess.run([NODE,str(JS)],input=json.dumps(batch),
       capture_output=True,text=True,check=True,timeout=30)
  return json.loads(done.stdout)
 if python_batch()!=js_batch():raise RuntimeError("reference result mismatch")
 def timing(fn):
  samples=[]
  for _ in range(3):
   start=time.perf_counter_ns()
   fn()
   samples.append(round((time.perf_counter_ns()-start)/len(batch),2))
  return {"ns_per_dataset_median":statistics.median(samples),"samples_ns":samples}
 print(json.dumps({"datasets":100,"rows_each":15,
     "python_precompiled":timing(python_batch),
     "node_subprocess_included":timing(js_batch),
     "output_equivalent":True,
     "warning":"Not cost-equivalent: Node process startup and Python compiled AST vs custom JS comparator; no language supremacy claim."},
     sort_keys=True))

if __name__=="__main__":main()
