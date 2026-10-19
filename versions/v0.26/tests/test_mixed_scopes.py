"""v0.26 bounded mixed scalar/table scope and independent Node conformance."""
import json
import random
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from axiomflow.language import AxiomError
from axiomflow.unified import compile_program,execute_program,run_program

ROOT=Path(__file__).resolve().parents[1]
DATA=(ROOT/"data"/"landed_cost.csv").read_bytes()
NODE=shutil.which("node")
JS=ROOT/"js"/"relational_runtime.js"


def source(threshold="100.00",factor="1.10"):
    return (f"let min_price = {threshold} USD\n"
            f"let multiplier = {factor}\n"
            "table t = input\n"
            "filter t where price_usd >= min_price\n"
            "derive t adjusted_usd = price_usd * multiplier\n"
            "sort t by price_usd\n"
            "sum t.adjusted_usd\n"
            "select t (price_usd,adjusted_usd)\n"
            "emit t")


def inlined(threshold="100.00",factor="1.10"):
    return ("table t = input\n"
            f"filter t where price_usd >= {threshold} USD\n"
            f"derive t adjusted_usd = price_usd * {factor}\n"
            "sort t by price_usd\n"
            "sum t.adjusted_usd\n"
            "select t (price_usd,adjusted_usd)\n"
            "emit t")


def csv_bytes(rows):
    return ("price_usd,rate,observed_cost_usd\n"+
            "".join(",".join(row)+"\n" for row in rows)).encode("ascii")


class MixedScopeTests(unittest.TestCase):
    def test_compiles_shared_ast_and_runs(self):
        compiled=compile_program(source())
        self.assertEqual(compiled.mode,"mixed")
        self.assertEqual(len(compiled.shared_ast),2+len(compiled.compiled.steps))
        self.assertIn("adjusted_usd",compiled.schema)
        self.assertEqual(execute_program(compiled,csv_bytes=DATA),
                         run_program(inlined(),csv_bytes=DATA))

    def test_multiple_reuse_without_mutation(self):
        compiled=compile_program(source("120.00","1.15"))
        reference=execute_program(compiled,csv_bytes=DATA)
        for _ in range(30):
            self.assertEqual(execute_program(compiled,csv_bytes=DATA),reference)

    def test_scalar_and_old_table_preserved(self):
        self.assertEqual(run_program("fn double(x:scalar)->scalar=x*2\nemit double(4)"),["8"])
        self.assertEqual(run_program(inlined(),csv_bytes=DATA),
                         run_program(source(),csv_bytes=DATA))

    def test_reject_currency_type_mismatch(self):
        bad=source().replace("let min_price = 100.00 USD","let min_price = 100.00 EUR")
        with self.assertRaisesRegex(AxiomError,"filter type mismatch"):
            compile_program(bad)

    def test_reject_scalar_where_money_needed(self):
        bad=source().replace("let min_price = 100.00 USD","let min_price = 100.00")
        with self.assertRaises(AxiomError):compile_program(bad)

    def test_reject_money_factor(self):
        bad=source().replace("let multiplier = 1.10","let multiplier = 1.10 USD")
        with self.assertRaises(AxiomError):compile_program(bad)

    def test_unsupported_effects_rejected(self):
        for x in ("let z = open(1)\n"+source(),
                  "use os\n"+source(),
                  "let min_price = __import__(2)\n"+source()):
            with self.subTest(code=x[:50]),self.assertRaises(AxiomError):
                compile_program(x)

    def test_shadow_and_duplicate_rejected(self):
        for x in ("let price_usd = 100.00 USD\n"+inlined(),
                  "let min_price = 1.00 USD\n"+source(),
                  "let adjusted_usd = 100.00 USD\n"+inlined()):
            with self.subTest(code=x[:60]),self.assertRaises(AxiomError):
                compile_program(x)

    def test_invalid_mixed_position(self):
        bad="table t = input\nlet min_price = 1.00 USD\nemit t"
        with self.assertRaises(AxiomError):compile_program(bad)

    def test_constant_budget(self):
        prefix="\n".join(f"let n{i} = {i}" for i in range(9))
        with self.assertRaisesRegex(AxiomError,"budget"):
            compile_program(prefix+"\n"+inlined())

    def test_csv_bounds(self):
        compiled=compile_program(source())
        for data in (None,b"x"*100001):
            with self.assertRaises(AxiomError):
                execute_program(compiled,csv_bytes=data)

    def test_seeded_inline_differential_220(self):
        rng=random.Random(26026)
        for i in range(220):
            threshold=rng.randrange(0,500000)
            factor=10000+rng.randrange(0,5000)
            a=f"{threshold//100}.{threshold%100:02d}"
            b=f"{factor//10000}.{factor%10000:04d}"
            with self.subTest(i=i):
                self.assertEqual(run_program(source(a,b),csv_bytes=DATA),
                                 run_program(inlined(a,b),csv_bytes=DATA))

    def test_cli_mixed_source(self):
        with tempfile.TemporaryDirectory() as d:
            file=Path(d)/"mixed.af"
            file.write_text(source(),encoding="ascii")
            p=subprocess.run([sys.executable,"-m","axiomflow.unified",
                  str(file),"--csv",str(ROOT/"data"/"landed_cost.csv")],
                  cwd=ROOT,capture_output=True,text=True,timeout=15)
            self.assertEqual(p.returncode,0,p.stderr)
            self.assertEqual(json.loads(p.stdout),run_program(source(),csv_bytes=DATA))


@unittest.skipUnless(NODE,"Node.js 22 required")
class IndependentNodeMixedTests(unittest.TestCase):
    def test_seeded_160_cross_runtime(self):
        rng=random.Random(26260)
        batch=[]
        for i in range(160):
            n=rng.randrange(3,15)
            rows=[]
            for _ in range(n):
                cents=rng.randrange(0,200000)
                r=rng.randrange(0,10001)
                rows.append([f"{cents//100}.{cents%100:02d}",
                             f"{r//10000}.{r%10000:04d}","0.00"])
            threshold=rng.randrange(0,150000)
            factor=10000+rng.randrange(0,5000)
            batch.append({"source":source(f"{threshold//100}.{threshold%100:02d}",
                                               f"{factor//10000}.{factor%10000:04d}"),
                          "rows":rows})
        p=subprocess.run([NODE,str(JS)],input=json.dumps(batch),
            capture_output=True,text=True,timeout=40)
        self.assertEqual(p.returncode,0,p.stderr)
        output=json.loads(p.stdout)
        self.assertEqual(len(output),len(batch))
        for i,(case,result) in enumerate(zip(batch,output)):
            with self.subTest(i=i):
                self.assertEqual(run_program(case["source"],csv_bytes=csv_bytes(case["rows"])),result)

    def test_node_rejects_unsafe_scope(self):
        x=[{"source":"let min_price = open(1)\ntable t = input\nemit t",
            "rows":[["1.00","0.0000","0.00"]]}]
        p=subprocess.run([NODE,str(JS)],input=json.dumps(x),
           capture_output=True,text=True,timeout=15)
        self.assertNotEqual(p.returncode,0)

    def test_rounding_ties_mixed(self):
        batch=[{"source":source("0.00","1.1250"),
                "rows":[["1.00","0.0000","0.00"],["1.01","0.0000","0.00"],["1.02","0.0000","0.00"]]}]
        p=subprocess.run([NODE,str(JS)],input=json.dumps(batch),
            capture_output=True,text=True,timeout=15)
        self.assertEqual(p.returncode,0,p.stderr)
        self.assertEqual(json.loads(p.stdout)[0],
                         run_program(batch[0]["source"],csv_bytes=csv_bytes(batch[0]["rows"])))


if __name__=="__main__":
    unittest.main()
