"""Independent rational-arithmetic checks against SI's shared numeric helpers.

This oracle uses Fraction directly and never calls si.limits.apply_binary.
"""
from fractions import Fraction
import random
import unittest

from si import SIError, run, run_compiled, compile_source
from si.verify import verify
from si.types import typecheck


def rational_oracle(op, a, b):
    x,y=Fraction(a),Fraction(b)
    if op=='ADD': return int(x+y)
    if op=='SUB': return int(x-y)
    if op=='MUL': return int(x*y)
    if op=='DIV':
        if y==0: raise ZeroDivisionError()
        return float(x/y)
    if op=='LT': return int(x<y)
    if op=='EQ': return int(x==y)
    raise AssertionError('unknown operation')


class IndependentOracleTests(unittest.TestCase):
    def test_known_literals(self):
        cases=[('ADD',-3,8),('SUB',-3,8),('MUL',-12,-9),
               ('DIV',1,3),('DIV',-7,2),('LT',-1,0),('EQ',9,9)]
        for op,a,b in cases:
            with self.subTest(op=op,a=a,b=b):
                src=f'PUSH {a}\nPUSH {b}\n{op}'
                wanted=rational_oracle(op,a,b)
                for engine in (run,run_compiled):
                    self.assertEqual(engine(src)['stack'],[wanted])

    def test_seeded_rational_model_2400(self):
        rng=random.Random(18102026)
        ops=('ADD','SUB','MUL','DIV','LT','EQ')
        for i in range(2400):
            op=rng.choice(ops)
            a=rng.randrange(-(1<<70),1<<70)
            b=rng.randrange(-(1<<70),1<<70)
            if op=='DIV' and b==0: b=1
            wanted=rational_oracle(op,a,b)
            src=f'PUSH {a}\nPUSH {b}\n{op}'
            reference,compiled=run(src),run_compiled(src)
            self.assertEqual(reference,compiled,f'engine case {i}')
            self.assertEqual(reference['stack'],[wanted],f'model case {i}')

    def test_seeded_conditional_oracle_400(self):
        rng=random.Random(808)
        for i in range(400):
            condition=rng.randrange(-2,3)
            a,b,c=(rng.randrange(-100000,100001) for _ in range(3))
            op=rng.choice(('ADD','SUB','MUL','LT','EQ'))
            src=(f'PUSH {condition}\nJZ yes\nPUSH {a}\nJMP end\n'
                 f'LABEL yes\nPUSH {b}\nLABEL end\nPUSH {c}\n{op}\nPRINT')
            chosen=b if condition==0 else a
            wanted=str(rational_oracle(op,chosen,c))
            reference,compiled=run(src),run_compiled(src)
            self.assertEqual(reference,compiled,f'engine case {i}')
            self.assertEqual(reference['output'],[wanted],f'oracle case {i}')
            code=compile_source(src)
            self.assertTrue(verify(code).reachable)
            self.assertTrue(typecheck(code).reachable)

    def test_zero_division_si_error(self):
        for engine in (run,run_compiled):
            with self.assertRaisesRegex(SIError,'division by zero'):
                engine('PUSH 0\nPUSH 0\nDIV')

    def test_overflow_si_error(self):
        src='PUSH 1'+'0'*400+'\nPUSH 1\nDIV'
        for engine in (run,run_compiled):
            with self.assertRaisesRegex(SIError,'numeric overflow'):
                engine(src)

    def test_division_rounding_against_fraction(self):
        for a,b in ((1,3),(7,-10),(2**53+1,7),(0,7),(-1,6)):
            src=f'PUSH {a}\nPUSH {b}\nDIV'
            self.assertEqual(run(src)['stack'],[float(Fraction(a,b))])


if __name__=='__main__':
    unittest.main()
