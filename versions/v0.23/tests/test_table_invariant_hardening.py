"""Additional v0.23 table grammar regression gates (no scoring award)."""
import unittest
from decimal import Decimal

from axiomflow.language import AxiomError
from axiomflow.table_language import compile_table, execute_table


ROWS = [("12.00", "0.1000", "13.20"), ("8.00", "0.2500", "10.00")]


class TableInvariantHardening(unittest.TestCase):
    def test_compile_rejects_projected_away_column(self):
        with self.assertRaises(AxiomError):
            compile_table("table costs = input\nselect costs (price_usd)\nsum costs.rate")

    def test_compile_rejects_duplicate_projection(self):
        with self.assertRaises(AxiomError):
            compile_table("table costs = input\nselect costs (rate,rate)\nemit costs")

    def test_compile_rejects_multiple_input_declarations(self):
        with self.assertRaises(AxiomError):
            compile_table("table costs = input\ntable other = input\nemit costs")

    def test_compile_rejects_missing_observable_output(self):
        with self.assertRaises(AxiomError):
            compile_table("table costs = input\nsort costs by price_usd")

    def test_compiled_program_reusable_and_input_unchanged(self):
        source = "table costs = input\nsort costs by price_usd\nsum costs.price_usd\nemit costs"
        compiled = compile_table(source)
        original = list(ROWS)
        first = execute_table(compiled, original)
        second = execute_table(compiled, original)
        self.assertEqual(first, second)
        self.assertEqual(original, ROWS)
        self.assertEqual(first[0]["value"], "20.00 USD")
        self.assertEqual(first[1]["columns"], ["price_usd", "rate", "observed_cost_usd"])
        self.assertEqual(first[1]["rows"][0][0], "8.00 USD")

    def test_source_line_limit(self):
        with self.assertRaises(AxiomError):
            compile_table("table costs = input\n" + "# comment\n" * 100 + "emit costs")


if __name__ == "__main__":
    unittest.main()
