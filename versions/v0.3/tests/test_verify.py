import random
import unittest
from si.core import SIError
from si.compiler import Instruction,compile_source,execute
from si.verify import verify,remove_unreachable

class VerifyTests(unittest.TestCase):
    def test_basic(self):
        code=compile_source('PUSH 3\nPUSH 4\nADD\nPRINT\nHALT')
        self.assertEqual(verify(code).max_stack_height,2)
    def test_underflow(self):
        with self.assertRaisesRegex(SIError,'underflow'):
            verify(compile_source('ADD'))
    def test_join_mismatch(self):
        with self.assertRaisesRegex(SIError,'inconsistent'):
            verify(compile_source('PUSH 0\nJZ done\nPUSH 2\nLABEL done\nHALT'))
    def test_unreachable_underflow_ignored(self):
        code=compile_source('JMP end\nADD\nLABEL end\nHALT')
        self.assertNotIn(1,verify(code).reachable)
    def test_bad_jump(self):
        with self.assertRaisesRegex(SIError,'jump'):
            verify((Instruction('JMP',99),))
    def test_max_stack(self):
        with self.assertRaisesRegex(SIError,'overflow'):
            verify(compile_source('PUSH 1\nPUSH 2'),max_stack=1)
    def test_dead_code_removed(self):
        code=compile_source('PUSH 7\nJMP end\nPUSH 999\nPRINT\nLABEL end\nPRINT\nHALT')
        opt=remove_unreachable(code)
        self.assertLess(len(opt),len(code))
        self.assertEqual(execute(code),execute(opt))
    def test_jump_to_exit(self):
        code=(Instruction('PUSH',4),Instruction('JMP',3),Instruction('PUSH',9))
        self.assertEqual(execute(code),execute(remove_unreachable(code)))
    def test_randomized_equivalence(self):
        rng=random.Random(31032026)
        for _ in range(1000):
            n=rng.randrange(1,35)
            lines=['PUSH 0']
            for i in range(n):
                lines.extend([f'PUSH {rng.randrange(-50,51)}',rng.choice(['ADD','SUB','MUL','EQ','LT'])])
                if rng.random()<0.15:
                    lines.extend(['JMP finish','PUSH 999','PRINT'])
                    break
            lines+=['LABEL finish','PRINT','HALT']
            code=compile_source('\n'.join(lines))
            optimized=remove_unreachable(code)
            self.assertEqual(execute(code),execute(optimized))
    def test_deterministic(self):
        code=compile_source('PUSH 1\nPRINT')
        self.assertEqual(remove_unreachable(code),remove_unreachable(code))

if __name__=='__main__': unittest.main()