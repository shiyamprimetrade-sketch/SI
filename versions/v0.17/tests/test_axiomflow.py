"""AxiomFlow alpha regression and independent Decimal oracle."""
import random, subprocess, sys, unittest
from decimal import Decimal, ROUND_HALF_EVEN
from axiomflow import AxiomError,evaluate,parse_program

class AxiomFlowTests(unittest.TestCase):
    def test_arithmetic(self):
        self.assertEqual(evaluate("emit 2+3*4"),["14"])
        self.assertEqual(evaluate("emit (2+3)*4"),["20"])
        self.assertEqual(evaluate("emit 7/2"),["3.5"])
    def test_money(self):
        self.assertEqual(evaluate("emit 12.35 USD + 0.65 USD"),["13.00 USD"])
        self.assertEqual(evaluate("emit 1.00 USD * 0.125"),["0.12 USD"])
        self.assertEqual(evaluate("emit 1.00 USD * 0.135"),["0.14 USD"])
        self.assertEqual(evaluate("emit -(1.00 USD + 0.25 USD)"),["-1.25 USD"])
    def test_variables(self):
        self.assertEqual(evaluate("let base = 19.99 USD\nemit base * 2"),["39.98 USD"])
        self.assertEqual(len(parse_program("emit 1\nemit 2")),2)
    def test_currency_rejection(self):
        with self.assertRaisesRegex(AxiomError,"currency/type mismatch"):
            evaluate("emit 1.00 USD + 1.00 EUR")
    def test_money_multiply_rejected(self):
        with self.assertRaisesRegex(AxiomError,"money multiplied"):
            evaluate("emit 1.00 USD * 1.00 USD")
    def test_money_division_rejected(self):
        with self.assertRaisesRegex(AxiomError,"division by money"):
            evaluate("emit 1.00 USD / 1.00 USD")
    def test_invalid_programs(self):
        for s in ("import os","emit __import__(1)","emit 0xFF",
                  "let a =","emit [1]","emit 1.23.4"):
            with self.subTest(s=s),self.assertRaises(AxiomError):evaluate(s)
    def test_zero_division(self):
        with self.assertRaisesRegex(AxiomError,"division by zero"):evaluate("emit 1/0")
    def test_missing_variable(self):
        with self.assertRaisesRegex(AxiomError,"undefined name"):evaluate("emit abc")
    def test_duplicate_binding(self):
        with self.assertRaisesRegex(AxiomError,"duplicate binding"):
            evaluate("let x=1\nlet x=2")
    def test_ascii_and_source_caps(self):
        with self.assertRaisesRegex(AxiomError,"ASCII"):evaluate("emit 1 # café")
        with self.assertRaisesRegex(AxiomError,"source budget"):evaluate(" "*100001)
        with self.assertRaisesRegex(AxiomError,"line budget"):evaluate("\n"*2001)
    def test_numeric_cap(self):
        with self.assertRaisesRegex(AxiomError,"numeric bound"):
            evaluate("emit 9999999999999999999999999999999999999")
    def test_comments(self):
        self.assertEqual(evaluate("# demo\nemit 2 # hi"),["2"])
    def test_seeded_decimal_model_500(self):
        rng=random.Random(17001)
        for i in range(500):
            a,b=rng.randrange(0,200000),rng.randrange(0,200000)
            rate=rng.randrange(1,20000)
            x,y,z=Decimal(a)/100,Decimal(b)/100,Decimal(rate)/10000
            expected=((x+y)*z).quantize(Decimal(".01"),rounding=ROUND_HALF_EVEN)
            src=f"emit ({x:.2f} USD + {y:.2f} USD) * {z}"
            with self.subTest(i=i):
                self.assertEqual(evaluate(src),[f"{expected:.2f} USD"])
    def test_terminal_cli(self):
        cp=subprocess.run([sys.executable,"-m","axiomflow","--eval",
                            "emit 2.00 USD + 3.00 USD"],
                          capture_output=True,text=True)
        self.assertEqual(cp.returncode,0)
        self.assertEqual(cp.stdout.strip(),"5.00 USD")
if __name__=="__main__":unittest.main()
