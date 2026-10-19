"""Independent Node.js BigInt fixed-point reference vs AxiomFlow and Decimal."""
from decimal import Decimal
import json
import random
import shutil
import subprocess
from pathlib import Path
import unittest
from axiomflow.data import feature_precompiled,feature_decimal_reference

NODE=shutil.which("node")
SCRIPT=Path(__file__).resolve().parent.parent/"js"/"fixed_cents.js"


@unittest.skipUnless(NODE,"Node.js required for independent comparison")
class FixedPointReferenceTests(unittest.TestCase):
    def test_seeded_250(self):
        rng=random.Random(22119)
        rows=[]
        for _ in range(250):
            cents=rng.randrange(0,100000001)
            bps=rng.randrange(0,10001)
            rows.append({"price":f"{cents//100}.{cents%100:02d}",
                         "rate":f"{bps//10000}.{bps%10000:04d}"})
        done=subprocess.run([NODE,str(SCRIPT)],input=json.dumps(rows),
                            text=True,capture_output=True,check=True,timeout=30)
        result=json.loads(done.stdout)
        self.assertEqual(len(result),len(rows))
        for i,(row,text) in enumerate(zip(rows,result)):
            with self.subTest(index=i):
                self.assertEqual(Decimal(text),
                                 feature_precompiled(row["price"],row["rate"]))
                self.assertEqual(Decimal(text),
                                 feature_decimal_reference(row["price"],row["rate"]))

    def test_exact_half_even_ties(self):
        rows=[{"price":"1.00","rate":"0.1250"},
              {"price":"1.00","rate":"0.1350"},
              {"price":"1.00","rate":"0.0050"}]
        done=subprocess.run([NODE,str(SCRIPT)],input=json.dumps(rows),
                            text=True,capture_output=True,check=True,timeout=30)
        self.assertEqual(json.loads(done.stdout),["1.12","1.14","1.00"])

    def test_reject_unsafe_big_inputs(self):
        done=subprocess.run([NODE,str(SCRIPT)],
                            input=json.dumps([{"price":"99999999.99","rate":"0.1"}]),
                            text=True,capture_output=True,timeout=30)
        self.assertNotEqual(done.returncode,0)


if __name__=="__main__":unittest.main()
