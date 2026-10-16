"""Bounded executable parsing obligations; NOT a formal universal theorem.

Run `python -m si.obligations` from the SI v0.10 project directory.
The enumerated input corpus and its digest make evaluations reproducible.
"""
import hashlib
import itertools
import json

from .errors import SIError
from .portable import parse_portable, canonical_source, structural_signature

ALPHABET = ('P', 'U', '0', '+', '#', ' ', '\t', '\n')


def check_bounded_lexical_obligations(max_length=4):
    """Exhaustive for a *finite* alphabet up to given length, no wider proof."""
    if type(max_length) is not int or not 0 <= max_length <= 5:
        raise SIError('invalid proof corpus length')
    digest = hashlib.sha256()
    examined = accepted = rejected = 0
    for length in range(max_length + 1):
        for items in itertools.product(ALPHABET, repeat=length):
            text = ''.join(items)
            examined += 1
            try:
                first = parse_portable(text)
            except SIError:
                rejected += 1
                digest.update(b'R\x00' + text.encode('ascii') + b'\x00')
                continue
            canonical = canonical_source(first)
            second = parse_portable(canonical)
            # Bounded executable obligations; a mismatch aborts the entire run.
            if structural_signature(first) != structural_signature(second):
                raise AssertionError('roundtrip structural violation')
            if canonical_source(second) != canonical:
                raise AssertionError('canonical idempotence violation')
            accepted += 1
            digest.update(b'A\x00' + text.encode('ascii') + b'\x00' + canonical.encode('ascii') + b'\x00')
    assert examined == accepted + rejected
    return {
        'language_profile': 'SI-Portable-1',
        'obligation': 'bounded-lexer-roundtrip-and-idempotence',
        'alphabet': list(ALPHABET),
        'max_length': max_length,
        'total_cases': examined,
        'accepted': accepted,
        'rejected': rejected,
        'sha256_corpus_results': digest.hexdigest(),
        'universal_proof': False,
    }


if __name__ == '__main__':
    print(json.dumps(check_bounded_lexical_obligations(), indent=2, sort_keys=True))