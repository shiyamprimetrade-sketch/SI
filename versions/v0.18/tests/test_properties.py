import random,unittest
from si.core import run, SIError
from si.compiler import compile_source,execute
from si.types import typecheck
from si.verify import remove_unreachable

class PropertyTests(unittest.TestCase):
    def test_seeded_arithmetic_differential_5000(self):
        rng=random.Random(20261016)
        for i in range(5000):
            a=rng.randrange(-10000,10001);b=rng.randrange(-10000,10001)
            op=rng.choice(('ADD','SUB','MUL','LT','EQ','DIV'))
            if op=='DIV' and b==0:b=1
            src=f'PUSH {a}\nPUSH {b}\n{op}\nPRINT\nHALT'
            code=compile_source(src);typecheck(code)
            self.assertEqual(run(src)['output'],execute(code)['output'],f'case {i}')
    def test_seeded_control_flow_1000(self):
        rng=random.Random(44)
        for i in range(1000):
            x=rng.randint(-1000,1000)
            src=f'PUSH {x}\nJZ zero\nPUSH 11\nJMP end\nLABEL zero\nPUSH 22\nLABEL end\nPRINT\nHALT'
            code=compile_source(src);typecheck(code)
            self.assertEqual(execute(code)['output'],execute(remove_unreachable(code))['output'])
            self.assertEqual(run(src)['output'],execute(code)['output'])
    def test_seeded_underflow_rejection_1000(self):
        rng=random.Random(77)
        for _ in range(1000):
            op=rng.choice(('ADD','SUB','DIV','DUP','DROP','PRINT','SWAP','JZ'))
            code=compile_source(f'{op} target\nLABEL target' if op=='JZ' else op)
            with self.assertRaises(SIError):typecheck(code)