"""Independent Node BigInt vs grammar-executed AxiomFlow table workloads."""
import json
import random
import shutil
import subprocess
import unittest
from pathlib import Path
from axiomflow.table_language import compile_table, execute_table

NODE=shutil.which("node")
SCRIPT=Path(__file__).resolve().parents[1]/"js"/"table_reference.js"

@unittest.skipUnless(NODE,"Node 22 required")
class TableJsReferenceTests(unittest.TestCase):
    def test_seeded_200(self):
        rng=random.Random(24025)
        batch=[]
        python=[]
        for i in range(200):
            minimum=rng.randrange(0,100000)
            threshold=f"{minimum//100}.{minimum%100:02d}"
            values=[]
            rows=[]
            for _ in range(rng.randrange(3,35)):
                v=rng.randrange(0,1000000)
                price=f"{v//100}.{v%100:02d}"
                values.append(price)
                rows.append((price,"0.1000","0.00"))
            batch.append({"minimum":threshold,"rows":values})
            program=(f"table t = input\nfilter t where price_usd >= {threshold} USD\n"
                     "derive t adjusted_usd = price_usd * 1.10\n"
                     "sum t.adjusted_usd\n"
                     "select t (price_usd,adjusted_usd)\nemit t")
            python.append(execute_table(compile_table(program),tuple(rows)))
        done=subprocess.run([NODE,str(SCRIPT)],input=json.dumps(batch),
                            text=True,capture_output=True,check=True,timeout=45)
        self.assertEqual(len(json.loads(done.stdout)),len(batch))
        for i,(left,right) in enumerate(zip(python,json.loads(done.stdout))):
            with self.subTest(i=i):
                self.assertEqual(left[0]["value"],right["sum"])
                self.assertEqual(left[1]["rows"],right["rows"])

    def test_node_reject_bad_input(self):
        done=subprocess.run([NODE,str(SCRIPT)],input=json.dumps(
            [{"minimum":"0.00","rows":["-5.00"]}]),capture_output=True,text=True,timeout=15)
        self.assertNotEqual(done.returncode,0)

if __name__=="__main__":
    unittest.main()
