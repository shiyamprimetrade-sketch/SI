"""v0.18: distinguish repeatable parsed execution from reparsing."""
import random
import unittest
from unittest.mock import patch
from axiomflow import (AxiomError, compile_source, evaluate, evaluate_compiled)


class CompileOnceTests(unittest.TestCase):
    def test_equivalent_output(self):
        samples=[
            "emit 1 + 2 * 3",
            "emit 2.00 USD * 1.075",
            "let x = 10.00 USD\nemit x + 2.00 USD",
            "emit 0.125 + 0.375",
            "let x=2\nlet y=x*3\nemit y",
            "# comment\nemit (1+2)*4",
        ]
        for source in samples:
            with self.subTest(source=source):
                self.assertEqual(evaluate_compiled(compile_source(source)),evaluate(source))

    def test_no_parsing_during_compiled_execution(self):
        program=compile_source("emit 19.99 USD * 2")
        with patch("axiomflow.language.parse_program",side_effect=AssertionError("reparsed")):
            self.assertEqual(evaluate_compiled(program),["39.98 USD"])

    def test_repeat_execution_has_no_state_leak(self):
        program=compile_source("let amount=1.25 USD\nemit amount*3")
        for _ in range(25):
            self.assertEqual(evaluate_compiled(program),["3.75 USD"])

    def test_reject_bad_container(self):
        with self.assertRaisesRegex(AxiomError,"compiled program must be"):
            evaluate_compiled(["emit"])

    def test_bad_statement_rejected(self):
        with self.assertRaisesRegex(AxiomError,"invalid statement"):
            evaluate_compiled((("UNSUPPORTED",),))

    def test_independent_seeded_equivalence_800(self):
        rng=random.Random(18018)
        for index in range(800):
            a,b=rng.randrange(0,100000),rng.randrange(0,100000)
            scale=rng.randrange(1,10001)
            source=f"emit ({a//100}.{a%100:02d} USD + {b//100}.{b%100:02d} USD) * {scale/10000:.4f}"
            with self.subTest(case=index):
                self.assertEqual(evaluate(source),evaluate_compiled(compile_source(source)))

    def test_invalid_syntax_rejected_at_compile(self):
        with self.assertRaises(AxiomError):
            compile_source("emit 1 USD / 2")

    def test_compiled_program_has_immutable_top_level(self):
        self.assertIs(type(compile_source("emit 2")),tuple)


if __name__=="__main__":unittest.main()
