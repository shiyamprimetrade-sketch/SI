"""JSON batch adapter for workload-equivalent process-level comparison."""
import json
import sys
from axiomflow.unified import run_program
from axiomflow.language import AxiomError

def run(batch):
    if type(batch) is not list or len(batch)>500:
        raise AxiomError("invalid bounded batch")
    results=[]
    for case in batch:
        if type(case) is not dict or set(case)!={"source","rows"}:
            raise AxiomError("invalid batch item")
        rows=case["rows"]
        if type(rows) is not list or len(rows)>500:
            raise AxiomError("invalid CSV rows")
        for row in rows:
            if type(row) is not list or len(row)!=3 or any(type(x) is not str for x in row):
                raise AxiomError("invalid row")
        data=("price_usd,rate,observed_cost_usd\n"+
              "".join(",".join(row)+"\n" for row in rows)).encode("ascii")
        results.append(run_program(case["source"],csv_bytes=data))
    return results

if __name__=="__main__":
    try:
        data=json.load(sys.stdin)
        print(json.dumps(run(data),separators=(",",":"),sort_keys=True))
    except (AxiomError,ValueError,UnicodeError,TypeError) as error:
        sys.exit("batch error: "+str(error))
