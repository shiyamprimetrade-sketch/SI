"""Second lexer's equivalence to v0.9 engines on its documented subset.

V0.10 portable grammar is deliberately narrower than the legacy shlex grammar.
Only successfully parsed portable text is expected to have equivalent semantics.
"""
import random
import unittest

from si.bytecode import Instruction, validate_bytecode
from si.compiler import compile_source, execute
from si.core import run
from si.errors import SIError
from si.reference import assemble, evaluate
from si.portable import (
    parse_portable, canonical_source, structural_signature, roundtrip_obligation,
)
from si.limits import MAX_SOURCE_CHARS, MAX_LITERAL_CHARS


def portable_bytecode(source):
    operations = parse_portable(source)
    return tuple(Instruction(
        op.opcode,
        op.operand if op.opcode == 'PUSH' else op.target
        if op.opcode in ('JMP', 'JZ') else None,
    ) for op in operations)


class PortableConformanceTests(unittest.TestCase):
    def assert_four(self, source, **kw):
        """Run old source interpreter, compiled VM, small-step model and portable VM."""
        portable = portable_bytecode(source)
        canonical = canonical_source(parse_portable(source))
        self.assertEqual(portable, compile_source(source))
        self.assertEqual(portable, compile_source(canonical))
        self.assertIs(validate_bytecode(portable), portable)
        baseline = run(source, **kw)
        self.assertEqual(baseline, execute(portable, **kw))
        self.assertEqual(baseline, execute(compile_source(source), **kw))
        self.assertEqual(baseline, evaluate(source, **kw))
        self.assertEqual(baseline, run(canonical, **kw))
        self.assertTrue(roundtrip_obligation(source))
        return baseline

    def test_empty(self):
        self.assertEqual(self.assert_four('')['steps'], 0)

    def test_comments_and_crlf(self):
        src='# hi\r\n  pUsH\t+00012#inline\r\nPRINT\r\n#bye\r\n'
        self.assertEqual(self.assert_four(src)['output'], ['12'])

    def test_case_sensitive_label_names(self):
        src='JMP X\nLABEL x\nPUSH 9\nLABEL X\nPUSH 4\nPRINT'
        self.assertEqual(self.assert_four(src)['output'], ['4'])

    def test_all_arithmetic_ops(self):
        for op in ('ADD','SUB','MUL','DIV','EQ','LT'):
            for a,b in ((1,2),(-4,7),(0,-5),(20,5)):
                with self.subTest(op=op,a=a,b=b):
                    self.assert_four(f'PUSH {a}\nPUSH {b}\n{op}\nPRINT')

    def test_negative_zero(self):
        self.assertEqual(self.assert_four('PUSH 0\nPUSH -3\nDIV\nPRINT')['output'], ['-0.0'])

    def test_all_non_arithmetic_opcodes(self):
        src=('PUSH 3\nDUP\nSWAP\nDROP\nLABEL top\nPUSH 0\nJZ jump\n'
             'PUSH 99\nLABEL jump\nPUSH 2\nPRINT\nHALT\nPUSH 999')
        self.assertEqual(self.assert_four(src)['output'], ['2'])

    def test_bounded_countdown_loop(self):
        src='PUSH 3\nLABEL loop\nDUP\nPRINT\nPUSH 1\nSUB\nDUP\nJZ end\nJMP loop\nLABEL end\nDROP'
        self.assertEqual(self.assert_four(src)['output'], ['3','2','1'])

    def test_seeded_arithmetic_1200(self):
        rng=random.Random(20261016)
        for i in range(1200):
            a=rng.randint(-(10**35),10**35)
            b=rng.randint(-(10**35),10**35) or 1
            op=rng.choice(('ADD','SUB','MUL','DIV','LT','EQ'))
            src=f'PUSH {a}\nPUSH {b}\n{op}\nPRINT'
            with self.subTest(i=i):
                self.assert_four(src)

    def test_seeded_conditional_branches_700(self):
        rng=random.Random(55)
        for i in range(700):
            x=rng.randrange(-2,3)
            a,b=rng.randrange(-1000,1000),rng.randrange(-1000,1000)
            src=(f'PUSH {x}\nJZ _left\nPUSH {a}\nJMP _end\n'
                 f'LABEL _left\nPUSH {b}\nLABEL _end\nPRINT')
            with self.subTest(i=i): self.assert_four(src)

    def test_seeded_comment_whitespace_metamorphisms_400(self):
        rng=random.Random(419)
        for i in range(400):
            a,b=rng.randint(-5000,5000),rng.randint(-5000,5000)
            base=f'PUSH {a}\nPUSH {b}\nADD\nPRINT\nHALT'
            noisy='\r\n# note\r\n'.join(line+'\t# trailing' for line in base.splitlines())
            with self.subTest(i=i):
                self.assertEqual(self.assert_four(base),self.assert_four(noisy))

    def test_seeded_portable_parser_vs_reference_500(self):
        rng=random.Random(831)
        for i in range(500):
            name='Q'+str(i)
            literal=rng.randint(-500000,500000)
            src=f'JMP {name}\nPUSH 123\nLABEL {name}\nPUSH {literal}\nHALT'
            parsed=parse_portable(src)
            ref_ops=assemble(src)
            self.assertEqual(len(ref_ops),len(parsed))
            for p,ref in zip(parsed,ref_ops):
                self.assertEqual(p.opcode,ref.opcode)
                if p.opcode == 'PUSH': self.assertEqual(p.operand,ref.operand)
                if p.opcode in ('JMP','JZ'): self.assertEqual(p.target,ref.operand)
            self.assertEqual(self.assert_four(src)['stack'],[literal])

    def test_large_valid_literal_matches_baseline(self):
        src='PUSH '+'9'*MAX_LITERAL_CHARS+'\nDROP\nHALT'
        self.assert_four(src)

    def test_source_limit_rejection(self):
        src='#' + 'x'*MAX_SOURCE_CHARS
        with self.assertRaisesRegex(SIError,'source budget exceeded'):
            parse_portable(src)

    def test_legacy_quotation_is_explicitly_outside_profile(self):
        legacy='PUSH "17"\nPRINT'
        self.assertEqual(run(legacy)['output'],['17'])
        with self.assertRaises(SIError): parse_portable(legacy)

    def test_legacy_unicode_comment_is_explicitly_outside_profile(self):
        legacy='PUSH 2 # naïve\nPRINT'
        self.assertEqual(run(legacy)['output'],['2'])
        with self.assertRaises(SIError): parse_portable(legacy)

    def test_unreachable_nonportable_integer_rejected(self):
        with self.assertRaisesRegex(SIError,'nonportable integer literal'):
            parse_portable('HALT\nPUSH 1_0')

    def test_reserved_identifier_limits(self):
        self.assert_four('LABEL '+('a'*64)+'\nPUSH 0\nHALT')
        with self.assertRaisesRegex(SIError,'nonportable label'):
            parse_portable('LABEL '+('a'*65))

    def test_portable_parser_deterministic(self):
        p='PUSH 12\nLABEL a\nJMP a'
        self.assertEqual(parse_portable(p),parse_portable(p))
        self.assertEqual(structural_signature(parse_portable(p)),
                         structural_signature(parse_portable(canonical_source(parse_portable(p)))))


if __name__ == '__main__':unittest.main()