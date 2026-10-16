"""Local, independent lexer checks; these do not depend on SI's compiler."""
import itertools
import random
import unittest

from si.errors import SIError
from si.portable import (
    parse_portable, canonical_source, structural_signature,
    roundtrip_obligation,
)


class PortableStandaloneTests(unittest.TestCase):
    def test_empty_and_comment(self):
        self.assertEqual(parse_portable('# hello\n'), ())
        self.assertEqual(canonical_source(()), '')

    def test_case_and_whitespace(self):
        src = '  push\t+0002#comment\r\nlabel\tEnd\n pRiNt\n HaLt'
        parsed = parse_portable(src)
        self.assertEqual(canonical_source(parsed), 'PUSH 2\nLABEL End\nPRINT\nHALT')
        self.assertTrue(roundtrip_obligation(src))

    def test_jumps(self):
        src = 'jmp _End\nPUSH 999\nLABEL _End\nHALT'
        ops = parse_portable(src)
        self.assertEqual(ops[0].target, 2)
        self.assertEqual(ops[2].operand, '_End')

    def test_labels_case_sensitive(self):
        ops = parse_portable('LABEL x\nLABEL X\nJMP x\nJMP X')
        self.assertEqual((ops[-2].target, ops[-1].target), (0,1))

    def test_bad_lexical(self):
        bad = ['PUSH "2"','PUSH 1_0','PUSH 0xA','PUSH ١','PUSH 1\x00',
               'PUSH 1\u2009','PUSH 2\rHALT','PUSH +','LABEL 8bad',
               'LABEL x.y','JMP missing','LABEL x\nLABEL x',
               'PUSH 2\\#x', 'PUSH 1\vHALT']
        for src in bad:
            with self.subTest(src=repr(src)):
                with self.assertRaises(SIError):
                    parse_portable(src)

    def test_nul_in_comment_rejected(self):
        with self.assertRaisesRegex(SIError,'nonportable character'):
            parse_portable('HALT # ignored\x00')

    def test_exhaustive_short_lexical_sequences(self):
        alphabet = 'P+0# \t\n'
        tested=0
        for n in range(4):
            for chars in itertools.product(alphabet, repeat=n):
                src=''.join(chars)
                try:
                    first=parse_portable(src)
                except SIError:
                    continue
                self.assertEqual(structural_signature(first),
                                 structural_signature(parse_portable(canonical_source(first))))
                tested += 1
        self.assertGreater(tested, 0)

    def test_seeded_roundtrip_1500(self):
        rng = random.Random(20261016)
        for i in range(1500):
            name = 'L_' + str(i)
            value = rng.randint(-100000,100000)
            source = f'\tpush +{abs(value):06d}\t# comment\nJMP {name}\nPUSH 999\nLABEL {name}\nPRINT'
            if value < 0:
                source=source.replace(f'+{abs(value):06d}',f'-{abs(value):06d}')
            self.assertTrue(roundtrip_obligation(source), f'case {i}')

    def test_canonical_stability(self):
        raw='pUsH +00008\nLABEL L\nJMP L\n# comment\nHALT'
        stable=canonical_source(parse_portable(raw))
        self.assertEqual(canonical_source(parse_portable(stable)),stable)

    def test_invalid_source_type(self):
        for source in (None, b'PUSH 1', 123):
            with self.assertRaisesRegex(SIError, 'source must be a string'):
                parse_portable(source)


if __name__ == '__main__': unittest.main()