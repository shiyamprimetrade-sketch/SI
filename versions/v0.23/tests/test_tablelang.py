"""SI v0.23 AxiomFlow table syntax, static checking and seeded conformance."""
import json
import random
import subprocess
import sys
from decimal import Decimal, ROUND_HALF_EVEN
from pathlib import Path
import unittest
from axiomflow.language import AxiomError
from axiomflow.tablelang import compile_table_source,execute_table,run_table_source

EXAMPLE="""table costs(price_usd: USD, rate: scalar, observed_cost_usd: USD)
row costs(125.50 USD, 0.0750, 134.91 USD)
row costs(1.00 USD, 0.1250, 1.12 USD)
derive costs landed_cost_usd: USD = landed(price_usd, rate)
sort costs by price_usd
select costs price_usd,landed_cost_usd
sum costs landed_cost_usd
"""


def oracle(cents, bps):
    q,r=divmod(cents*(10000+bps),10000)
    if 2*r>10000 or (2*r==10000 and q%2):q+=1
    return f"{q//100}.{q%100:02d}"


class TableSourceTests(unittest.TestCase):
    def test_program_success_and_static_type(self):
        code=compile_table_source(EXAMPLE)
        result=execute_table(code)
        self.assertEqual(result[0]["columns"],["price_usd","landed_cost_usd"])
        self.assertEqual(result[0]["types"],["USD","USD"])
        self.assertEqual(result[0]["rows"],[["1.00","1.12"],["125.50","134.91"]])
        self.assertEqual(result[1]["value"],"136.03")

    def test_executable_source_equivalence(self):
        self.assertEqual(run_table_source(EXAMPLE),execute_table(compile_table_source(EXAMPLE)))

    def test_repeat_execution_immutable(self):
        code=compile_table_source(EXAMPLE)
        self.assertEqual(execute_table(code),execute_table(code))

    def test_type_mismatch_rejected(self):
        src="table t(price: scalar, rate: scalar)\nderive t cost: USD = landed(price, rate)"
        with self.assertRaisesRegex(AxiomError,"type mismatch"):compile_table_source(src)

    def test_duplicate_columns_rejected(self):
        with self.assertRaisesRegex(AxiomError,"duplicate"):compile_table_source("table t(price: USD, price: USD)")

    def test_missing_columns_rejected(self):
        with self.assertRaises(AxiomError):compile_table_source("table t(price: USD)\nselect t unknown")

    def test_missing_table_rejected(self):
        with self.assertRaises(AxiomError):compile_table_source("sum unknown value")

    def test_unknown_operation_rejected(self):
        for line in ("import os","python open('x')","drop t","while 1","row t(__import__)"):
            with self.subTest(line=line),self.assertRaises(AxiomError):
                compile_table_source(line)

    def test_money_decimal_syntax_rejected(self):
        for bad in ("1 USD","1.005 USD","-1.00 USD","NaN USD","1e9 USD"):
            s=f"table t(price: USD)\nrow t({bad})"
            with self.subTest(bad=bad),self.assertRaises(AxiomError):
                compile_table_source(s)

    def test_row_after_derive_rejected_pre_execution(self):
        s=("table t(price: USD,rate: scalar)\n"
           "derive t final: USD = landed(price,rate)\n"
           "row t(1.00 USD,0.1)")
        with self.assertRaisesRegex(AxiomError,"rows after derived"):
            compile_table_source(s)

    def test_resource_row_cap(self):
        source="table t(price: USD)\n"+"row t(1.00 USD)\n"*501
        with self.assertRaisesRegex(AxiomError,"row budget"):compile_table_source(source)

    def test_resource_source_cap(self):
        with self.assertRaises(AxiomError):compile_table_source("#"+"x"*100001)

    def test_non_ascii_rejected(self):
        with self.assertRaises(AxiomError):compile_table_source("#é")

    def test_seeded_independent_oracle_400(self):
        rng=random.Random(23023)
        rows=[]
        expected=[]
        for _ in range(400):
            cents=rng.randrange(0,100000000)
            bps=rng.randrange(0,10001)
            rows.append(f"row t({cents//100}.{cents%100:02d} USD,{bps//10000}.{bps%10000:04d})")
            expected.append(oracle(cents,bps))
        source=("table t(price: USD,rate: scalar)\n"+"\n".join(rows)+
                "\nderive t result: USD = landed(price,rate)\nselect t result")
        output=run_table_source(source)
        self.assertEqual([r[0] for r in output[0]["rows"]],expected)

    def test_serialize_deterministically(self):
        result=run_table_source(EXAMPLE)
        self.assertEqual(json.dumps(result,sort_keys=True),
                         json.dumps(run_table_source(EXAMPLE),sort_keys=True))

    def test_cli_actual_file(self):
        with __import__("tempfile").TemporaryDirectory() as d:
            path=Path(d)/"test.af"
            path.write_text(EXAMPLE,encoding="ascii")
            run=subprocess.run([sys.executable,"-m","axiomflow.tablelang",str(path)],
                               text=True,capture_output=True,timeout=15)
            self.assertEqual(run.returncode,0,run.stderr)
            self.assertEqual(json.loads(run.stdout),run_table_source(EXAMPLE))

    def test_cli_invalid_source_nonzero(self):
        with __import__("tempfile").TemporaryDirectory() as d:
            path=Path(d)/"test.af";path.write_text("import os")
            run=subprocess.run([sys.executable,"-m","axiomflow.tablelang",str(path)],
                               text=True,capture_output=True,timeout=15)
            self.assertEqual(run.returncode,2)
            self.assertIn("table error",run.stderr)


if __name__=="__main__":unittest.main()
