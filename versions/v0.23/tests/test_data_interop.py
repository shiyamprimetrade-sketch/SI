"""v0.21 data pipeline integration, exact model baseline and rejection tests."""
import csv
from decimal import Decimal
from hashlib import sha256
import io
import json
import random
import subprocess
import sys
from pathlib import Path
import unittest

from axiomflow.data import (HEADER, analyze, feature_axiomflow,
                             feature_decimal_reference,load_rows)
from axiomflow.language import AxiomError

ROOT=Path(__file__).resolve().parent.parent
FIXTURE=ROOT/"data"/"landed_cost.csv"


def to_data(rows):
    buf=io.StringIO(newline="")
    writer=csv.writer(buf,lineterminator="\n")
    writer.writerow(HEADER)
    writer.writerows(rows)
    return buf.getvalue().encode("ascii")


class DataInteroperabilityTests(unittest.TestCase):
    def test_fixture_reproducible(self):
        raw=FIXTURE.read_bytes()
        report=analyze(raw)
        self.assertEqual(report["dataset_sha256"],sha256(raw).hexdigest())
        self.assertEqual((report["rows"],report["train_rows"],report["test_rows"]),(9,6,3))
        self.assertEqual(Decimal(report["slope"]),Decimal("2"))
        self.assertEqual(Decimal(report["intercept"]),Decimal("5"))
        self.assertEqual(Decimal(report["test_mae"]),Decimal("0"))
        self.assertEqual(analyze(raw),report)

    def test_exact_independent_feature_oracle_400(self):
        rng=random.Random(21021)
        for i in range(400):
            cents=rng.randrange(0,100000000)
            basis_points=rng.randrange(0,10001)
            price=f"{Decimal(cents)/100:.2f}"
            rate=f"{Decimal(basis_points)/10000:.4f}"
            with self.subTest(case=i):
                self.assertEqual(feature_axiomflow(price,rate),
                                 feature_decimal_reference(price,rate))

    def test_invalid_headers(self):
        for raw in (b"",b"x,y,z\n1,2,3\n",b"price_usd,rate,observed_cost_usd,x\n"):
            with self.subTest(raw=raw),self.assertRaises(AxiomError):
                load_rows(raw)

    def test_malformed_rows_and_non_ascii(self):
        base=b"price_usd,rate,observed_cost_usd\n"
        for row in (b"1,0.5,2.00\n",b"1.00,0.0,not_a_number\n",
                    b"1.00,NaN,2.00\n",b"-1.00,0.1,2.00\n",
                    b"1.00,1.0001,2.00\n",b"1.00,0.1,2.00,4\n",
                    "1.00,0.1,é\n".encode(),b"1.00,0.1,\x00\n"):
            with self.subTest(row=row),self.assertRaises(AxiomError):
                load_rows(base+row+b"2.00,0.1,3.00\n3.00,0.1,4.00\n")

    def test_missing_rows_and_budget(self):
        with self.assertRaisesRegex(AxiomError,"three data rows"):
            load_rows(to_data([("1.00","0.1","2.00")]))
        with self.assertRaises(AxiomError):
            load_rows(to_data([("1.00","0.1","2.00")]*501))
        with self.assertRaises(AxiomError):
            load_rows(b"x"*100001)

    def test_constant_feature_rejected(self):
        raw=to_data([("1.00","0.0","1.00")]*9)
        with self.assertRaisesRegex(AxiomError,"constant feature"):
            analyze(raw)

    def test_train_test_split_is_ordered_no_leakage(self):
        rows=load_rows(FIXTURE.read_bytes())
        self.assertEqual(len(rows),9)
        self.assertEqual(analyze(FIXTURE.read_bytes())["split_policy"],
                         "ordered first floor(2n/3) train, remaining test")

    def test_cli_json_parity(self):
        result=subprocess.run([sys.executable,"-m","axiomflow.data",str(FIXTURE)],
                              cwd=ROOT,text=True,capture_output=True,timeout=15)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertEqual(json.loads(result.stdout),analyze(FIXTURE.read_bytes()))

    def test_cli_missing_file_is_error(self):
        result=subprocess.run([sys.executable,"-m","axiomflow.data",
                               "data/nonexistent.csv"],cwd=ROOT,text=True,
                              capture_output=True,timeout=15)
        self.assertEqual(result.returncode,2)
        self.assertIn("data error",result.stderr)

    def test_json_canonical_repeatability(self):
        result=analyze(FIXTURE.read_bytes())
        enc=json.dumps(result,sort_keys=True,separators=(",",":"))
        self.assertEqual(enc,json.dumps(analyze(FIXTURE.read_bytes()),
                                        sort_keys=True,separators=(",",":")))


if __name__=="__main__":
    unittest.main()
