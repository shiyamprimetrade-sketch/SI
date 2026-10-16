"""Regression tests for SI reference interpreter parser parity."""
import unittest
from si.core import run, SIError
from si.compiler import compile_source, execute

class ParserParityTests(unittest.TestCase):
    def test_lowercase_label_and_jump(self):
        src = 'push 0\njz skip\npush 3\nlabel skip\npush 7\nprint\nhalt'
        self.assertEqual(run(src)['output'], ['7'])
        self.assertEqual(run(src)['output'], execute(compile_source(src))['output'])

    def test_mixed_case_label(self):
        src = 'PUSH 0\nJZ end\nPUSH 99\nLaBeL end\nPUSH 2\nPRINT'
        self.assertEqual(run(src)['output'], ['2'])
        self.assertEqual(run(src)['output'], execute(compile_source(src))['output'])

    def test_duplicate_labels(self):
        src='LABEL x\nPUSH 5\nlabel x\nHALT'
        for interpreter in (run, compile_source):
            with self.assertRaisesRegex(SIError, 'duplicate label'): interpreter(src)

    def test_unreachable_duplicate_labels(self):
        src='HALT\nLABEL x\nLABEL x'
        for interpreter in (run, compile_source):
            with self.assertRaisesRegex(SIError, 'duplicate label'): interpreter(src)

    def test_malformed_quote(self):
        src='PUSH 1\nPUSH "2'
        for interpreter in (run, compile_source):
            with self.assertRaisesRegex(SIError, 'line 2:'): interpreter(src)

    def test_unreachable_malformed_quote(self):
        src='HALT\nPUSH "2'
        for interpreter in (run, compile_source):
            with self.assertRaises(SIError): interpreter(src)

    def test_malformed_label_arity(self):
        src='LABEL x y'
        for interpreter in (run, compile_source):
            with self.assertRaisesRegex(SIError, 'LABEL needs 1 args'): interpreter(src)

    def test_step_budget(self):
        with self.assertRaisesRegex(SIError, 'step budget exceeded'):
            run('LABEL start\nJMP start',max_steps=12)

    def test_arithmetic_regression(self):
        src='PUSH 4\nPUSH 5\nADD\nPRINT'
        self.assertEqual(run(src)['output'], ['9'])
        self.assertEqual(run(src)['output'], execute(compile_source(src))['output'])

if __name__ == '__main__': unittest.main()
