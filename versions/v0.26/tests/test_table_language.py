"""v0.23 parser/type checking and executable table source conformance."""
import json
import random
import subprocess
import sys
import tempfile
from pathlib import Path
import unittest
from decimal import Decimal

from axiomflow.language import AxiomError
from axiomflow.data import load_rows, feature_decimal_reference
from axiomflow.table_language import compile_table,execute_table,run_table

ROOT=Path(__file__).resolve().parents[1]
CSV=(ROOT/"data"/"landed_cost.csv").read_bytes()
SOURCE=(ROOT/"examples"/"table_summary.af").read_text(encoding="ascii")


class TableLanguageTests(unittest.TestCase):
    def test_parse_and_execute_real_source(self):
        result=run_table(SOURCE,CSV)
        self.assertEqual(len(result),2)
        self.assertEqual(result[0]["operation"],"sum")
        self.assertEqual(result[0]["column"],"landed_cost_usd")
        self.assertEqual(len(result[1]["rows"]),9)
        self.assertEqual(result[1]["columns"],
                         ["price_usd","landed_cost_usd"])

    def test_cli_execution_same_as_model(self):
        done=subprocess.run([sys.executable,"-m","axiomflow.table_language",
              str(ROOT/"examples"/"table_summary.af"),"--csv",
              str(ROOT/"data"/"landed_cost.csv")],cwd=ROOT,
              capture_output=True,text=True,timeout=20)
        self.assertEqual(done.returncode,0,done.stderr)
        self.assertEqual(json.loads(done.stdout),run_table(SOURCE,CSV))

    def test_static_error_before_execution(self):
        for src in (
            "sort t by rate",
            "table t = input\nselect t (unknown)\nemit t",
            "table t = input\nselect t (price_usd,price_usd)\nemit t",
            "table t = input\nselect t (rate)\naugment t landed_cost_usd\nemit t",
            "table t = input\nsum t.unknown",
            "table t = input\nemit other",
            "table t = input\nspawn shell",
            "table t = input\ntable b = input\nemit t",
            "table t = input\n__import__(os)\nemit t",
            "table t = input\nselect other (rate)\nemit t",
            "table t = input",
        ):
            with self.subTest(src=src),self.assertRaises(AxiomError):
                compile_table(src)

    def test_budget_and_encoding(self):
        for source in ("table t = input\n"+"emit t\n"*101,
                       "a"*10001, "table t = input\nemit t\n☃"):
            with self.subTest(source=source[:50]),self.assertRaises(AxiomError):
                compile_table(source)

    def test_repeatable_compiled_execution(self):
        program=compile_table(SOURCE)
        a=execute_table(program,load_rows(CSV))
        for _ in range(20):
            self.assertEqual(execute_table(program,load_rows(CSV)),a)

    def test_immutable_compiled_plan(self):
        plan=compile_table(SOURCE)
        with self.assertRaises((AttributeError,TypeError)):
            plan.steps=()

    def test_aggregate_independent_decimal(self):
        records=load_rows(CSV)
        expected=sum((feature_decimal_reference(a,b)
                      for a,b,_ in records),Decimal(0))
        result=run_table(SOURCE,CSV)
        self.assertEqual(result[0]["value"],f"{expected:.2f} USD")

    def test_projection_static_type_order(self):
        p=compile_table("table t = input\nselect t (rate,price_usd)\nemit t")
        self.assertEqual(p.result_schema,("rate","price_usd"))
        self.assertEqual(p.result_types,("scalar","USD"))
        data=execute_table(p,load_rows(CSV))[0]
        self.assertEqual(data["columns"],["rate","price_usd"])

    def test_seeded_table_data_250(self):
        rng=random.Random(23023)
        p=compile_table("table t = input\naugment t landed_cost_usd\nsum t.landed_cost_usd")
        for i in range(250):
            rows=[]
            for _ in range(rng.randrange(3,16)):
                cents=rng.randrange(0,10000000)
                rate=rng.randrange(0,10001)
                a=f"{cents//100}.{cents%100:02d}"
                b=f"{rate//10000}.{rate%10000:04d}"
                rows.append((a,b,"0.00"))
            expected=sum((feature_decimal_reference(a,b)
                          for a,b,_ in rows),Decimal(0))
            with self.subTest(case=i):
                output=execute_table(p,tuple(rows))
                self.assertEqual(output[0]["value"],f"{expected:.2f} USD")

    def test_no_dynamic_source_execution(self):
        with self.assertRaises(AxiomError):
            compile_table("table t = input\nemit eval('bad')")

    def test_no_input_filename_in_source(self):
        with self.assertRaises(AxiomError):
            compile_table('table t = "../secret.csv"\nemit t')


if __name__=="__main__":
    unittest.main()
