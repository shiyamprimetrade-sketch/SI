"""SI v0.15 bounded, exact-rational IEEE-754 rounding invariants.

Independently assess the candidate binary64 value and its immediate finite
neighbors as exact fractions; the test does not call the SI number helper.
"""
import json
import math
import random
import shutil
import struct
import subprocess
import unittest
from fractions import Fraction
from pathlib import Path

NODE = shutil.which("node")
PROBE = Path(__file__).resolve().parent.parent / "js" / "numeric_probe.js"


def bits(v):
    return struct.pack(">d", v).hex()


def frombits(hexstring):
    return struct.unpack(">d", bytes.fromhex(hexstring))[0]


def node_batch(items):
    done = subprocess.run(
        [NODE, str(PROBE)], input=json.dumps(items),
        text=True, capture_output=True, check=True, timeout=45
    )
    return json.loads(done.stdout)


def even_significand(v):
    """Parity of the stored binary64 fraction LSB, valid for finite numbers."""
    raw = int.from_bytes(struct.pack(">d", v), "big")
    return (raw & 1) == 0


def exact_rounding_obligation(a, b, bits_hex):
    """Prove a *single* finite candidate is nearest among adjacent floats.

    Uses exact Fraction distances and even significand for halfway ties.
    Handles signed zero by checking the intended sign explicitly.
    This is a check on one candidate, not a universal theorem.
    """
    if b == 0:
        raise ValueError("nonzero denominator required")
    candidate = frombits(bits_hex)
    if not math.isfinite(candidate):
        raise AssertionError("candidate must be finite")
    target = Fraction(a, b)
    if candidate == 0:
        expected_sign = (a < 0) != (b < 0)
        if (math.copysign(1.0, candidate) < 0) != expected_sign:
            raise AssertionError("incorrect signed zero")
    center = Fraction(candidate)
    center_dist = abs(center - target)
    for neighbor in (math.nextafter(candidate, -math.inf),
                     math.nextafter(candidate, math.inf)):
        if not math.isfinite(neighbor):
            continue
        distance = abs(Fraction(neighbor) - target)
        if center_dist > distance:
            raise AssertionError("neighbor is strictly closer")
        if center_dist == distance and not even_significand(candidate):
            raise AssertionError("halfway tie did not choose even significand")
    return True


def deterministic_shrink(a, b, reproduces, limit=10000):
    """Stable greedy shrink on decimal-length then magnitude.

    Shrinks only when the predicate remains true; bounded attempts and a
    monotonic ranking guarantee termination. Not globally minimal.
    """
    if b == 0 or not reproduces(a, b):
        raise ValueError("counterexample must reproduce with nonzero denominator")
    if type(limit) is not int or limit < 1:
        raise ValueError("invalid attempt limit")
    attempts = 0

    def rank(x, y):
        return (len(str(abs(x))) + len(str(abs(y))), abs(x) + abs(y),
                abs(x), abs(y))

    while attempts < limit:
        changed = False
        for side in (0, 1):
            value = (a, b)[side]
            digits = str(abs(value))
            sign = -1 if value < 0 else 1
            options = [0, 1, 2, 3, 5, 10]
            if len(digits) > 1:
                options.extend(int(digits[:i] + digits[i+1:] or "0")
                               for i in range(len(digits)))
                options.extend([int(digits[:len(digits)//2]),
                                int(digits[len(digits)//2:])])
            candidates = sorted(set(sign * v for v in options), key=abs)
            for candidate in candidates:
                x, y = (candidate, b) if side == 0 else (a, candidate)
                if y == 0 or rank(x, y) >= rank(a, b):
                    continue
                attempts += 1
                if reproduces(x, y):
                    a, b = x, y
                    changed = True
                    break
                if attempts >= limit:
                    break
            if changed or attempts >= limit:
                break
        if not changed:
            break
    return (a, b), attempts


@unittest.skipUnless(NODE, "Node.js mandatory for cross-runtime proof obligations")
class RoundingInvariantTests(unittest.TestCase):
    def verify(self, pairs):
        requests = [{"kind": "ratio", "a": str(a), "b": str(b)}
                    for a, b in pairs]
        observed = node_batch(requests)
        self.assertEqual(len(observed), len(pairs))
        for i, ((a, b), item) in enumerate(zip(pairs, observed)):
            with self.subTest(i=i, a=str(a)[:45], b=str(b)[:45]):
                self.assertTrue(item["ok"], item)
                self.assertTrue(exact_rounding_obligation(a, b, item["bits"]))

    def test_nearest_even_ties_at_one(self):
        pairs = [(2**53 + x, 2**53) for x in range(-9, 10)]
        pairs += [(-a, b) for a, b in pairs]
        self.verify(pairs)

    def test_zero_and_subnormal_ties(self):
        pairs = [(n, 2**1075) for n in range(-19, 20)]
        self.verify(pairs)

    def test_normal_subnormal_transition(self):
        pairs = [(2**53 + n, 2**1075) for n in range(-16, 17)]
        self.verify(pairs)

    def test_seeded_rational_neighborhoods_250(self):
        r = random.Random(151501)
        pairs = []
        for _ in range(250):
            exp = r.randrange(1, 1025)
            a = r.randrange(-2**55, 2**55)
            b = (1 << exp) + r.randrange(-100, 101)
            pairs.append((a, b))
        self.verify(pairs)

    def test_very_large_finite_balanced_ratios(self):
        pairs = [(10**400 + delta, 10**400)
                 for delta in (0, 1, -1, 10**350, -10**350)]
        pairs += [(-a, b) for a, b in pairs]
        self.verify(pairs)

    def test_minimizer_reproduction_and_monotone_rank(self):
        fake_bug = lambda a, b: b != 0 and a >= 17 and abs(b) >= 3
        pair, attempts = deterministic_shrink(170024, 70031, fake_bug)
        self.assertTrue(fake_bug(*pair))
        self.assertGreater(attempts, 0)
        self.assertLess(len(str(abs(pair[0]))) + len(str(abs(pair[1]))),
                        len("170024") + len("70031"))
        self.assertEqual(pair, deterministic_shrink(170024, 70031, fake_bug)[0])

    def test_minimizer_rejects_nonfailing_input(self):
        with self.assertRaisesRegex(ValueError, "must reproduce"):
            deterministic_shrink(1, 2, lambda a,b:a>4)

    def test_minimizer_attempt_bound(self):
        fake_bug = lambda a,b: b != 0 and a>10
        result, attempts = deterministic_shrink(12345678, 99998, fake_bug, limit=1)
        self.assertLessEqual(attempts, 1)
        self.assertTrue(fake_bug(*result))

    def test_proof_checker_catches_wrong_neighbor(self):
        # 1.0 for 1+2^-51 is not nearest: the next representable value is.
        with self.assertRaisesRegex(AssertionError, "neighbor"):
            exact_rounding_obligation(2**51+1, 2**51, bits(1.0))


if __name__ == "__main__":
    unittest.main()
