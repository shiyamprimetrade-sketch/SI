import random
import unittest
from si import run, run_compiled, compile_source, SIError

class CompilerTests(unittest.TestCase):
    def test_example(self):
        s='PUSH 3\nLABEL loop\nDUP\nPRINT\nPUSH 1\nSUB\nDUP\nJZ end\nJMP loop\nLABEL end\nDROP'
        self.assertEqual(run(s)['output'],run_compiled(s)['output'])
    def test_arithmetic(self):
        for op in ('ADD','SUB','MUL','DIV','LT','EQ'):
            for a in (-9,-1,0,1,9):
                for b in (-7,-1,1,7):
                    s=f'PUSH {a}\nPUSH {b}\n{op}\nPRINT'
                    self.assertEqual(run(s)['output'],run_compiled(s)['output'])
    def test_random_programs(self):
        rng=random.Random(20261016)
        for _ in range(1000):
            s=f'PUSH {rng.randint(-100,100)}\n'
            for _ in range(12):
                s+=f'PUSH {rng.randint(-10,10)}\n{rng.choice(["ADD","SUB","MUL","LT","EQ"])}\n'
            self.assertEqual(run(s)['stack'],run_compiled(s)['stack'])
    def test_duplicate_label(self):
        with self.assertRaisesRegex(SIError,'duplicate label'): compile_source('LABEL a\nLABEL a')
    def test_unknown_jump(self):
        with self.assertRaisesRegex(SIError,'unknown label'): compile_source('JMP nowhere')
    def test_bad_arity(self):
        with self.assertRaisesRegex(SIError,'needs'): compile_source('ADD 5')
    def test_zero_division(self):
        with self.assertRaisesRegex(SIError,'division by zero'): run_compiled('PUSH 1\nPUSH 0\nDIV')
    def test_stack_budget(self):
        with self.assertRaisesRegex(SIError,'stack budget'): run_compiled('PUSH 1\nPUSH 2',max_stack=1)
    def test_step_budget(self):
        with self.assertRaisesRegex(SIError,'step budget'): run_compiled('LABEL loop\nJMP loop',max_steps=20)
    def test_underflow(self):
        with self.assertRaisesRegex(SIError,'underflow'): run_compiled('SWAP')
    def test_forward_jump(self):
        self.assertEqual(run_compiled('JMP end\nPUSH 9\nLABEL end\nPUSH 3')['stack'],[3])
    def test_compiler_determinism(self):
        s='PUSH 3\nPUSH 4\nADD'
        self.assertEqual(compile_source(s),compile_source(s))