"""v0.25 unified front door and independent bounded JS relational source tests."""
from decimal import Decimal, ROUND_HALF_EVEN
import json
from pathlib import Path
import random
import shutil
import subprocess
import sys
import unittest

from axiomflow.language import AxiomError
from axiomflow.unified import compile_program, execute_program, run_program
from axiomflow.data import load_rows

ROOT=Path(__file__).resolve().parents[1]
CSV=(ROOT/"data"/"landed_cost.csv").read_bytes()
SOURCE=(ROOT/"examples"/"filtered_table.af").read_text(encoding="ascii")
NODE=shutil.which("node")
JS=ROOT/"js"/"relational_runtime.js"


def source_for(minimum):
    return ("table t = input\n"
            f"filter t where price_usd >= {minimum} USD\n"
            "derive t adjusted_usd = price_usd * 1.10\n"
            "sort t by price_usd\n"
            "sum t.adjusted_usd\n"
            "select t (price_usd,adjusted_usd)\n"
            "emit t")


class UnifiedTests(unittest.TestCase):
    def test_scalar_typed_functions(self):
        source="fn twice(v: USD) -> USD = v * 2\nemit twice(12.55 USD)"
        p=compile_program(source)
        self.assertEqual(p.mode,"scalar")
        self.assertEqual(execute_program(p),["25.10 USD"])

    def test_table_compiled_and_fresh_execution(self):
        p=compile_program(SOURCE)
        self.assertEqual(p.mode,"table")
        self.assertIn("adjusted_usd",p.schema)
        result=execute_program(p,csv_bytes=CSV)
        for _ in range(5):
            self.assertEqual(execute_program(p,csv_bytes=CSV),result)

    def test_cross_mode_rejected(self):
        cases=[
            "table t = input\nlet x=1\nemit t",
            "use pricing\ntable t = input\nemit t",
            "emit 2\ntable t = input\nemit t",
            "filter t where rate > 0.1\nemit t",
            "table t = input\nemit 1",
            "fn f(x:USD)->USD=x\nemit f(1.00 EUR)"
        ]
        for source in cases:
            with self.subTest(source=source),self.assertRaises(AxiomError):
                compile_program(source)

    def test_scalar_csv_input_rejected(self):
        with self.assertRaisesRegex(AxiomError,"CSV input"):
            execute_program(compile_program("emit 2"),csv_bytes=CSV)

    def test_table_requires_bounded_csv(self):
        compiled=compile_program("table t = input\nemit t")
        for data in (None,"data",b"x"*100001):
            with self.subTest(data=str(type(data))),self.assertRaises(AxiomError):
                execute_program(compiled,csv_bytes=data)

    def test_source_budget_and_empty(self):
        for code in ("", " "*10001, "emit 1\n"*101, "emit 1\x00"):
            with self.subTest(code=repr(code)[:35]),self.assertRaises(AxiomError):
                compile_program(code)

    def test_unified_scalar_cli(self):
        with __import__("tempfile").TemporaryDirectory() as d:
            file=Path(d)/"simple.af"
            file.write_text("fn f(x:scalar)->scalar=x*3\nemit f(4)",encoding="ascii")
            result=subprocess.run([sys.executable,"-m","axiomflow.unified",str(file)],
                                  cwd=ROOT,capture_output=True,text=True,timeout=15)
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertEqual(json.loads(result.stdout),["12"])

    def test_unified_table_cli(self):
        r=subprocess.run([sys.executable,"-m","axiomflow.unified",
                          str(ROOT/"examples"/"filtered_table.af"),
                          "--csv",str(ROOT/"data"/"landed_cost.csv")],
                         cwd=ROOT,capture_output=True,text=True,timeout=15)
        self.assertEqual(r.returncode,0,r.stderr)
        self.assertEqual(json.loads(r.stdout),run_program(SOURCE,csv_bytes=CSV))

    def test_no_real_shell_execution(self):
        for code in ('emit __import__("os")','table t = input\nimport os\nemit t',
                     'emit open("/tmp/secret")'):
            with self.subTest(code=code),self.assertRaises(AxiomError):
                compile_program(code)

    def test_static_table_schema_rejection(self):
        with self.assertRaises(AxiomError):
            compile_program("table t = input\nselect t (rate)\nsum t.price_usd")


@unittest.skipUnless(NODE,"Node 22 required")
class IndependentRelationalTests(unittest.TestCase):
    def compare(self,batch):
        process=subprocess.run([NODE,str(JS)],input=json.dumps(batch),
                               capture_output=True,text=True,timeout=40)
        self.assertEqual(process.returncode,0,process.stderr)
        results=json.loads(process.stdout)
        for i,(sample,observed) in enumerate(zip(batch,results)):
            with self.subTest(case=i):
                self.assertEqual(run_program(sample["source"],csv_bytes=
                                 make_csv(sample["rows"])),observed)

    def test_200_seeded_reference_programs(self):
        rng=random.Random(25025)
        batch=[]
        for _ in range(200):
            rows=[]
            for _ in range(rng.randrange(3,25)):
                cents=rng.randrange(0,500000)
                rate=rng.randrange(0,10001)
                rows.append([f"{cents//100}.{cents%100:02d}",
                             f"{rate//10000}.{rate%10000:04d}","0.00"])
            threshold=rng.randrange(0,40000)
            batch.append({"source":source_for(f"{threshold//100}.{threshold%100:02d}"),
                          "rows":rows})
        self.compare(batch)

    def test_zero_rows_after_filter(self):
        sample={"source":source_for("999999.99"),"rows":[["1.00","0.1000","0.00"],
                 ["2.00","0.1000","0.00"],["3.00","0.1000","0.00"]]}
        self.compare([sample])

    def test_half_even_source_values(self):
        self.compare([{"source":source_for("0.00"),
                       "rows":[["1.00","0.0000","0.00"],
                               ["1.05","0.0000","0.00"],
                               ["1.15","0.0000","0.00"]]}])

    def test_js_rejects_unsupported_program(self):
        sample=[{"source":"eval os.system(1)","rows":[]}]
        done=subprocess.run([NODE,str(JS)],input=json.dumps(sample),
                            capture_output=True,text=True,timeout=15)
        self.assertNotEqual(done.returncode,0)


def make_csv(rows):
    lines=["price_usd,rate,observed_cost_usd"]
    lines.extend(",".join(r) for r in rows)
    return ("\n".join(lines)+"\n").encode("ascii")


if __name__=="__main__":
    unittest.main()
