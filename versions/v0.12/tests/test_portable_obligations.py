"""Bounded machine-checkable obligations and regression examples."""
import unittest
from si.errors import SIError
from si.obligations import ALPHABET, check_bounded_lexical_obligations
from si.portable import parse_portable, canonical_source, structural_signature


class PortableObligationTests(unittest.TestCase):
    def test_complete_small_corpus_four_chars(self):
        result = check_bounded_lexical_obligations(max_length=4)
        expected=sum(len(ALPHABET)**n for n in range(5))
        self.assertEqual(result['total_cases'],expected)
        self.assertEqual(result['total_cases'],result['accepted']+result['rejected'])
        self.assertFalse(result['universal_proof'])
        self.assertEqual(len(result['sha256_corpus_results']),64)

    def test_deterministic_digest(self):
        self.assertEqual(check_bounded_lexical_obligations(3),
                         check_bounded_lexical_obligations(3))

    def test_bounded_not_unbounded(self):
        for value in (-1,6,'4',True):
            with self.subTest(value=value):
                with self.assertRaisesRegex(SIError,'invalid proof corpus length'):
                    check_bounded_lexical_obligations(value)

    def test_nontrivial_program_structural_invariance(self):
        src=' PUSH +0003# ignored\nLABEL Loop\nDUP\nJZ Exit\nPUSH 1\nSUB\nJMP Loop\nLABEL Exit\nHALT'
        p=parse_portable(src)
        q=parse_portable(canonical_source(p))
        self.assertEqual(structural_signature(p),structural_signature(q))
        self.assertEqual(q[6].target, 1)

    def test_comment_insertion_preserves_program_shape(self):
        base='PUSH 3\nLABEL L\nDUP\nJZ End\nPUSH 1\nSUB\nJMP L\nLABEL End\nHALT'
        enriched='\n# header\n'.join(x+' # trailing' for x in base.splitlines())
        self.assertEqual(structural_signature(parse_portable(base)),
                         structural_signature(parse_portable(enriched)))

    def test_canonical_rejection_of_invalid_object(self):
        with self.assertRaisesRegex(SIError,'invalid portable program'):
            canonical_source(['PUSH 5'])

    def test_literal_alphabet_strict_not_unicode(self):
        for bad in ('PUSH ９','PUSH १२','PUSH \u0665'):
            with self.subTest(value=bad):
                with self.assertRaises(SIError): parse_portable(bad)


if __name__=='__main__': unittest.main()