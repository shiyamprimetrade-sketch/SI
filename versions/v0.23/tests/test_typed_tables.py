"""v0.22 immutable typed tables and preparsed-feature parity."""
from decimal import Decimal
import random
import unittest
from unittest.mock import patch

from axiomflow.language import AxiomError
from axiomflow.data import (load_rows, feature_axiomflow,feature_precompiled,
                             feature_decimal_reference,analyze)
from axiomflow.table import (Table,Record,from_validated_csv_rows,COLS,TYPES)
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent


class TableTests(unittest.TestCase):
    def fixture(self):
        return from_validated_csv_rows(load_rows((ROOT/"data"/"landed_cost.csv").read_bytes()))

    def test_schema_and_immutability(self):
        t=self.fixture()
        self.assertEqual(t.columns,COLS)
        self.assertEqual(t.types,TYPES)
        self.assertEqual(len(t.records),9)
        with self.assertRaises((AttributeError,TypeError)):
            t.records=()

    def test_select_projected_columns(self):
        t=self.fixture().select(("rate","price_usd"))
        self.assertEqual(t.columns,("rate","price_usd"))
        self.assertEqual(t.types,("scalar","USD"))
        self.assertEqual(t.records[0]["price_usd"],Decimal("100.00"))

    def test_sort_is_stable_and_input_unchanged(self):
        t=self.fixture()
        s=t.sorted_by("price_usd")
        self.assertEqual(s.records[0]["price_usd"],Decimal("50.00"))
        self.assertEqual(t.records[0]["price_usd"],Decimal("100.00"))
        self.assertEqual(t.sorted_by("price_usd"),s)

    def test_sum_column(self):
        t=self.fixture()
        expected=sum((r["price_usd"] for r in t.records),Decimal(0))
        self.assertEqual(t.sum_column("price_usd"),expected)

    def test_augment_feature_exact_oracle(self):
        t=self.fixture()
        transformed=t.augment_landed_cost()
        self.assertEqual(len(transformed.columns),4)
        for raw,record in zip(t.records,transformed.records):
            self.assertEqual(record["landed_cost_usd"],
                             feature_decimal_reference(
                                 f"{raw['price_usd']:.2f}",f"{raw['rate']:.4f}"))
        self.assertEqual(len(t.columns),3)

    def test_projection_errors(self):
        t=self.fixture()
        for cols in ((),("unknown",),("rate","rate")):
            with self.subTest(cols=cols),self.assertRaises(AxiomError):
                t.select(cols)

    def test_aggregate_and_sort_errors(self):
        t=self.fixture()
        with self.assertRaises(AxiomError):t.sum_column("nonesuch")
        with self.assertRaises(AxiomError):t.sorted_by("nonesuch")

    def test_malformed_schema_and_value_rejection(self):
        for schema in (
            lambda:Table(("a","a"),("USD","USD"),()),
            lambda:Table(("a",),("USD",), (Record((("other",Decimal(1)),)),)),
            lambda:Table(("a",),("USD",), (Record((("a",Decimal("NaN")),)),)),
        ):
            with self.assertRaises(AxiomError):schema()

    def test_invalid_row_shapes(self):
        for rows in ((("bad",),), (("1.00","0.1","oops"),),
                     (("1.00",1,"2.00"),)):
            with self.subTest(rows=rows),self.assertRaises(AxiomError):
                from_validated_csv_rows(rows)

    def test_seeded_feature_parity_400(self):
        rng=random.Random(22022)
        for index in range(400):
            p=Decimal(rng.randrange(0,100000000))/100
            r=Decimal(rng.randrange(0,10001))/10000
            price=f"{p:.2f}";rate=f"{r:.4f}"
            with self.subTest(i=index):
                self.assertEqual(feature_precompiled(price,rate),
                                 feature_axiomflow(price,rate))
                self.assertEqual(feature_precompiled(price,rate),
                                 feature_decimal_reference(price,rate))

    def test_reparsed_source_not_called(self):
        from axiomflow import data
        with patch.object(data,"evaluate_typed",side_effect=AssertionError("reparsed")):
            self.assertEqual(feature_precompiled("125.50","0.0750"),
                             Decimal("134.91"))

    def test_compiled_repeated_isolation(self):
        for _ in range(40):
            self.assertEqual(feature_precompiled("9.99","0.1250"),
                             Decimal("11.24"))

    def test_feature_invalid_input_rejected(self):
        for pair in ((1,"0.1"),("1.00",.1),("-1.00","0.1"),
                     ("1.005","0.1"),("1.00","NaN"),
                     ("1000000.01","0.1")):
            with self.subTest(pair=pair),self.assertRaises(AxiomError):
                feature_precompiled(*pair)

    def test_dataset_model_retains_result(self):
        d=(ROOT/"data"/"landed_cost.csv").read_bytes()
        self.assertEqual(Decimal(analyze(d)["test_mae"]),Decimal(0))


if __name__=="__main__":
    unittest.main()
