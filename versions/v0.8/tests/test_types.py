import unittest
from si.compiler import compile_source, Instruction
from si.types import typecheck, INT, FLOAT, NUMBER
from si.core import SIError

class TypesTests(unittest.TestCase):
    def test_integer_add(self):
        r=typecheck(compile_source('PUSH 2\nPUSH 3\nADD\nHALT'))
        self.assertEqual(r.incoming[3],(INT,))
    def test_division_float(self):
        r=typecheck(compile_source('PUSH 2\nPUSH 3\nDIV\nHALT'))
        self.assertEqual(r.incoming[3],(FLOAT,))
    def test_comparison_int(self):
        r=typecheck(compile_source('PUSH 2\nPUSH 3\nLT\nHALT'))
        self.assertEqual(r.incoming[3],(INT,))
    def test_join_number(self):
        code=compile_source('PUSH 1\nJZ float\nPUSH 2\nPUSH 3\nDIV\nJMP join\nLABEL float\nPUSH 5\nLABEL join\nPRINT\nHALT')
        r=typecheck(code)
        self.assertEqual(r.incoming[9],(NUMBER,))
    def test_stack_join_error(self):
        with self.assertRaisesRegex(SIError,'inconsistent stack height'):
            typecheck(compile_source('PUSH 1\nJZ branch\nPUSH 3\nLABEL branch\nHALT'))
    def test_underflow(self):
        with self.assertRaisesRegex(SIError,'underflow'): typecheck(compile_source('ADD'))
    def test_bad_jump(self):
        with self.assertRaisesRegex(SIError,'jump target'): typecheck((Instruction('JMP',99),))
    def test_bad_push_bool(self):
        with self.assertRaisesRegex(SIError,'invalid PUSH'): typecheck((Instruction('PUSH',True),))
    def test_overflow(self):
        with self.assertRaisesRegex(SIError,'overflow'): typecheck(compile_source('PUSH 1\nPUSH 2'),max_stack=1)
    def test_loop_fixed_point(self):
        src='PUSH 3\nLABEL loop\nDUP\nJZ done\nPUSH 1\nSUB\nJMP loop\nLABEL done\nHALT'
        r=typecheck(compile_source(src));self.assertIn(1,r.reachable)
    def test_unknown_op(self):
        with self.assertRaisesRegex(SIError,'unknown opcode'): typecheck((Instruction('MYSTERY'),))
    def test_empty(self):
        self.assertEqual(typecheck(()).incoming,((),))