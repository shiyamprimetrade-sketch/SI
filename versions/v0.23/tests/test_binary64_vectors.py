"""v0.14: externally specified binary64 bit patterns and independent Fraction ratios.

Probe runs in a separate Node process. Python uses struct and Fraction to define
expected bits; this does not import the SI arithmetic interpreter or helper.
"""
from fractions import Fraction
import json
import random
import shutil
import struct
import subprocess
import unittest
from pathlib import Path

NODE=shutil.which('node')
PROBE=Path(__file__).resolve().parent.parent/'js'/'numeric_probe.js'


def bits(value):
    return struct.pack('>d',value).hex()


def frombits(hexvalue):
    return struct.unpack('>d',bytes.fromhex(hexvalue))[0]


def run_node(data):
    x=subprocess.run([NODE,str(PROBE)],input=json.dumps(data),
                     capture_output=True,text=True,check=True,timeout=45)
    return json.loads(x.stdout)


def expected_ratio(a,b):
    if b==0:
        return {'ok':False,'error':'division by zero'}
    try:
        value=float(Fraction(a,b))
    except OverflowError:
        return {'ok':False,'error':'numeric overflow'}
    # Preserve IEEE signed zero for an exactly zero numerator.
    if a==0 and b<0:
        value=-0.0
    return {'ok':True,'bits':bits(value),'text':str(value)}


def shrink_ratio(a,b,predicate):
    """Deterministic monotone digit-removal counterexample reducer.

    predicate(x,y) means failure still reproduces. Returns a smaller or equal
    counterexample, NOT a globally minimal one.
    """
    if not predicate(a,b):
        raise ValueError('input does not reproduce the failure')
    changed=True
    while changed:
        changed=False
        for side in (0,1):
            value=(a,b)[side]
            direction=-1 if value<0 else 1
            decimal=str(abs(value))
            candidates=[]
            if len(decimal)>1:
                candidates.extend([decimal[:len(decimal)//2],
                                   decimal[-len(decimal)//2:]])
                candidates.extend(decimal[:i]+decimal[i+1:]
                                  for i in range(len(decimal)))
            candidates.extend(('0','1','2'))
            for s in candidates:
                v=direction*int(s) if s else 0
                if len(str(abs(v)))>=len(decimal) and abs(v)>=abs(value):
                    continue
                new_a,new_b=(v,b) if side==0 else (a,v)
                if new_b==0:
                    continue
                if predicate(new_a,new_b):
                    a,b=new_a,new_b
                    changed=True
                    break
            if changed:break
    return a,b


@unittest.skipUnless(NODE,'Node.js needed for v0.14 independent numeric probe')
class Binary64Vectors(unittest.TestCase):
    def check_cases(self,cases):
        actual=run_node(cases)
        self.assertEqual(len(actual),len(cases))
        for i,(item,observed) in enumerate(zip(cases,actual)):
            if item['kind']=='ratio':
                expected=expected_ratio(int(item['a']),int(item['b']))
            elif item['kind']=='bits':
                v=frombits(item['hex'])
                expected=({'ok':True,'bits':bits(v),'text':str(v)}
                          if v==v and abs(v)!=float('inf')
                          else {'ok':False,'error':'non-finite numeric result'})
            else:
                integer=int(item['integer'])
                v=frombits(item['hex'])
                target=Fraction(v)
                expected={'ok':True,'comparison':(integer>target)-(integer<target)}
            with self.subTest(i=i,kind=item['kind'],sample=str(item)[:100]):
                self.assertEqual(observed,expected)

    def test_exact_binary64_bit_vectors_14(self):
        cases=[
            '0000000000000000','8000000000000000',
            '0000000000000001','8000000000000001',
            '0000000000000002','000fffffffffffff',
            '0010000000000000','0010000000000001',
            '3fefffffffffffff','3ff0000000000000',
            '3ff0000000000001','3fd5555555555555',
            '7fefffffffffffff','ffe0000000000000'
        ]
        self.check_cases([{'kind':'bits','hex':v} for v in cases])

    def test_ieee_nonfinite_patterns_4(self):
        self.check_cases([{'kind':'bits','hex':x} for x in
                          ('7ff0000000000000','fff0000000000000',
                           '7ff8000000000000','7ff0000000000001')])

    def test_signed_zero_rounding(self):
        cases=[(0,-1),(0,1),(1,10**400),(-1,10**400),
               (1,-10**400),(-1,-10**400)]
        self.check_cases([{'kind':'ratio','a':str(a),'b':str(b)}
                          for a,b in cases])

    def test_exact_half_min_subnormal(self):
        # Halfway between zero and minimum subnormal = 1/2**1075.
        cases=[(1,2**1075),(3,2**1075),(5,2**1075),
               (-1,2**1075),(-3,2**1075)]
        self.check_cases([{'kind':'ratio','a':str(a),'b':str(b)}
                          for a,b in cases])

    def test_subnormal_normal_boundary(self):
        cases=[(2**52-1,2**1074),(2**52,2**1074),
               (2**52+1,2**1074),(2**53-1,2**1075),
               (2**53+1,2**1075)]
        self.check_cases([{'kind':'ratio','a':str(a),'b':str(b)}
                          for a,b in cases])

    def test_nearest_even_halfway_to_one(self):
        # 1 + 2**-53 is halfway between 1.0 and its successor.
        cases=[(2**53,2**53),(2**53+1,2**53),
               (2**53+2,2**53),(2**53+3,2**53),
               (-2**53-1,2**53)]
        self.check_cases([{'kind':'ratio','a':str(a),'b':str(b)}
                          for a,b in cases])

    def test_binary64_big_integer_overflow(self):
        cases=[(10**400,1),(10**400,10**92),
               (10**400,10**93),(10**400,10**400)]
        self.check_cases([{'kind':'ratio','a':str(a),'b':str(b)}
                          for a,b in cases])

    def test_exact_mixed_integer_float(self):
        cases=[]
        for hexcode in ('3ff0000000000000','4340000000000000',
                        '0000000000000001','8000000000000000'):
            for number in (0,1,-1,2**53-1,2**53,2**53+1,2**100, -2**100):
                cases.append({'kind':'compare','integer':str(number),'hex':hexcode})
        self.check_cases(cases)

    def test_seeded_binary64_bit_patterns_300(self):
        rng=random.Random(14001)
        cases=[]
        while len(cases)<300:
            x=rng.getrandbits(64)
            if (x>>52)&2047==2047:continue
            cases.append({'kind':'bits','hex':f'{x:016x}'})
        self.check_cases(cases)

    def test_seeded_bounded_ratios_300(self):
        rng=random.Random(14002)
        cases=[]
        for _ in range(300):
            a=rng.randrange(-(1<<4090),(1<<4090))
            b=rng.randrange(-(1<<4090),(1<<4090)) or 1
            cases.append({'kind':'ratio','a':str(a),'b':str(b)})
        self.check_cases(cases)

    def test_seeded_near_subnormal_ratios_120(self):
        rng=random.Random(14003)
        cases=[]
        for _ in range(120):
            denom=1<<rng.randrange(1030,1080)
            num=rng.randrange(-64,65)
            cases.append({'kind':'ratio','a':str(num),'b':str(denom)})
        self.check_cases(cases)

    def test_minimizer_finds_smaller_synthetic_failure(self):
        # Deliberately injected predicate, not a production SI error.
        def fake_bug(a,b):return b!=0 and a>=13
        initial=(130045,77000)
        a,b=shrink_ratio(*initial,fake_bug)
        self.assertTrue(fake_bug(a,b))
        self.assertLess(len(str(a))+len(str(b)),
                        len(str(initial[0]))+len(str(initial[1])))

    def test_minimizer_requires_reproduction(self):
        with self.assertRaisesRegex(ValueError,'does not reproduce'):
            shrink_ratio(1,2,lambda a,b:a>10)


if __name__=='__main__':unittest.main()
