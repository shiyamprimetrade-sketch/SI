"""SI v0.24: grammar-level typed filtering and derived columns."""
import json
import random
import subprocess
import sys
import unittest
from decimal import Decimal, ROUND_HALF_EVEN
from pathlib import Path
from axiomflow.language import AxiomError
from axiomflow.table_language import compile_table, execute_table, run_table
from axiomflow.data import load_rows

ROOT=Path(__file__).resolve().parents[1]
CSV=(ROOT/"data"/"landed_cost.csv").read_bytes()
SOURCE=(ROOT/"examples"/"filtered_table.af").read_text(encoding="ascii")
NODE=ROOT/"js"/"table_reference.js"


class ExtendedTableTests(unittest.TestCase):
    def test_filter_derived_function_complete(self):
        results=run_table(SOURCE,CSV)
        self.assertEqual(results[0]["operation"],"sum")
        self.assertEqual(results[0]["column"],"adjusted_usd")
        self.assertEqual(results[1]["operation"],"emit")
        self.assertEqual(results[1]["columns"],["price_usd","adjusted_usd"])
        self.assertEqual(results[1]["types"],["USD","USD"])
        self.assertEqual(len(results[1]["rows"]),5)
        expected=sum((Decimal(row[1].split()[0]) for row in results[1]["rows"]),
                     Decimal(0))
        self.assertEqual(results[0]["value"],f"{expected:.2f} USD")

    def test_compile_preserves_schema_types(self):
        plan=compile_table(SOURCE)
        self.assertEqual(plan.result_schema,("price_usd","adjusted_usd"))
        self.assertEqual(plan.result_types,("USD","USD"))
        self.assertEqual(len(plan.functions),1)

    def test_repeated_compiled_execution(self):
        plan=compile_table(SOURCE)
        rows=load_rows(CSV)
        first=execute_table(plan,rows)
        for _ in range(20):
            self.assertEqual(execute_table(plan,rows),first)

    def test_invalid_static_filter_types(self):
        cases=[
            "table t = input\nfilter t where price_usd >= 10\nemit t",
            "table t = input\nfilter t where rate == 1.00 USD\nemit t",
            "table t = input\nfilter t where nowhere == 1\nemit t",
            "table t = input\nfilter t where rate == invalid\nemit t",
        ]
        for source in cases:
            with self.subTest(source=source),self.assertRaises(AxiomError):
                compile_table(source)

    def test_invalid_derived_type_name(self):
        cases=[
            "table t = input\nderive t rate = rate+1\nemit t",
            "table t = input\nderive t extra = price_usd + rate\nemit t",
            "table t = input\nderive t extra = unknown(1)\nemit t",
            "table t = input\nderive t extra = price_usd * price_usd\nemit t",
        ]
        for source in cases:
            with self.subTest(source=source),self.assertRaises(AxiomError):
                compile_table(source)

    def test_function_order_and_recursion_rejected(self):
        with self.assertRaises(AxiomError):
            compile_table("table t = input\nfn f(x:scalar)->scalar=x\nemit t")
        with self.assertRaisesRegex(AxiomError,"recursive"):
            compile_table("fn f(x:scalar)->scalar=f(x)\ntable t = input\nemit t")

    def test_schema_changes_before_filter(self):
        with self.assertRaises(AxiomError):
            compile_table("table t = input\nselect t (rate)\nfilter t where price_usd > 1.00 USD\nemit t")

    def test_rejection_of_dynamic_io(self):
        for command in ("filter t where rate == os.system(1)",
                        "derive t dangerous = eval(rate)",
                        "derive t bad = __import__(rate)"):
            with self.subTest(command=command),self.assertRaises(AxiomError):
                compile_table("table t = input\n"+command+"\nemit t")

    def test_seeded_relational_reference_250(self):
        rng=random.Random(24024)
        for i in range(250):
            rows=[]
            for _ in range(rng.randrange(3,30)):
                cents=rng.randrange(0,1000000)
                rate=rng.randrange(0,10001)
                rows.append((f"{cents//100}.{cents%100:02d}",
                             f"{rate//10000}.{rate%10000:04d}","0.00"))
            minimum=rng.randrange(0,10000)
            minimum_text=f"{minimum//100}.{minimum%100:02d}"
            source=("fn uplift(x: USD) -> USD = x * 1.10\n"
                    "table t = input\n"
                    f"filter t where price_usd >= {minimum_text} USD\n"
                    "derive t adjusted_usd = uplift(price_usd)\n"
                    "sum t.adjusted_usd\n"
                    "select t (price_usd,adjusted_usd)\n"
                    "emit t")
            output=execute_table(compile_table(source),tuple(rows))
            kept=[Decimal(price) for price,_,_ in rows if Decimal(price)>=Decimal(minimum_text)]
            computed=[(x*Decimal("1.10")).quantize(Decimal(".01"),
                      rounding=ROUND_HALF_EVEN) for x in kept]
            with self.subTest(i=i):
                self.assertEqual(output[0]["value"],f"{sum(computed,Decimal(0)):.2f} USD")
                self.assertEqual([r[1] for r in output[1]["rows"]],
                                 [f"{x:.2f} USD" for x in computed])

    def test_cli_example(self):
        done=subprocess.run([sys.executable,"-m","axiomflow.table_language",
                             str(ROOT/"examples"/"filtered_table.af"),"--csv",
                             str(ROOT/"data"/"landed_cost.csv")],cwd=ROOT,
                            capture_output=True,text=True,timeout=20)
        self.assertEqual(done.returncode,0,done.stderr)
        self.assertEqual(json.loads(done.stdout),run_table(SOURCE,CSV))


if __name__=="__main__":
    unittest.main()
