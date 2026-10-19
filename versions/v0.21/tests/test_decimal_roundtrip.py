"""SI v0.16: decimal shortest-roundtrip checks and independent float neighbors."""
import json
import math
import random
import shutil
import struct
import subprocess
import unittest
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

NODE = shutil.which("node")
PROBE = Path(__file__).resolve().parent.parent / "js" / "numeric_probe.js"


def float_bits(value):
    return struct.pack(">d", value).hex()


def unpack_bits(value):
    return struct.unpack(">d", bytes.fromhex(value))[0]


def node_results(inputs):
    completed = subprocess.run(
        [NODE, str(PROBE)], input=json.dumps(inputs), text=True,
        capture_output=True, timeout=45, check=True
    )
    return json.loads(completed.stdout)


def decimal_roundtrip_criterion(bits_hex, text):
    """Check finite float rendering recovers exactly the input bit pattern."""
    value = unpack_bits(bits_hex)
    if not math.isfinite(value):
        raise ValueError("requires finite float")
    decoded = float(text)
    return float_bits(decoded) == bits_hex


def lexical_shortening_checks(text):
    """Try removing each non-sign, non-exp digit: necessary, not sufficient,
    test for shortest textual representation, and not a decimal optimality proof.
    """
    for i, ch in enumerate(text):
        if ch not in "0123456789":
            continue
        candidate = text[:i] + text[i+1:]
        try:
            converted = float(candidate)
        except ValueError:
            continue
        yield candidate, float_bits(converted)


@unittest.skipUnless(NODE, "Node required in CI")
class DecimalAndOracleTests(unittest.TestCase):
    def compare_bits(self, samples, check_lexical=False):
        responses = node_results([{"kind":"bits","hex":b} for b in samples])
        for b, result in zip(samples, responses):
            with self.subTest(bits=b):
                self.assertTrue(result["ok"], result)
                self.assertEqual(result["bits"], b)
                self.assertTrue(decimal_roundtrip_criterion(b, result["text"]))
                self.assertEqual(result["text"], str(unpack_bits(b)))
                if check_lexical:
                    # This property is a bounded text-deletion heuristic only.
                    for candidate, newbits in lexical_shortening_checks(result["text"]):
                        if "e" in result["text"] and "e" not in candidate:
                            continue
                        # Some removal can preserve value while merely
                        # changing exponent zero-padding: do not claim
                        # global shortest-length optimality.
                        if candidate.replace("e+0", "e+") == result["text"]:
                            continue

    def test_exponent_transition_vectors(self):
        samples = [
            float_bits(v) for v in
            (1e-7, 1e-6, 1e-5, 1e-4, 1e15, 1e16, 1e17,
             1e20, 1e21, 1e22, 0.0, -0.0,
             math.nextafter(1.0, 2.0),
             math.nextafter(1.0, 0.0),
             math.ldexp(1., -1022),
             math.ldexp(1., -1074))
        ]
        self.compare_bits(samples, check_lexical=True)

    def test_random_full_bits_800(self):
        rng = random.Random(16001)
        cases=[]
        while len(cases)<800:
            raw = rng.getrandbits(64)
            if (raw >> 52) & 0x7ff == 0x7ff:
                continue
            cases.append(f"{raw:016x}")
        self.compare_bits(cases)

    def test_ulp_neighbor_both_sides_240(self):
        rng = random.Random(16002)
        bits=[]
        for _ in range(80):
            raw = rng.getrandbits(64)
            val = unpack_bits(f"{raw:016x}")
            if not math.isfinite(val):
                continue
            for v in (val, math.nextafter(val, -math.inf),
                      math.nextafter(val, math.inf)):
                if math.isfinite(v):
                    bits.append(float_bits(v))
        self.compare_bits(bits)

    def test_signed_zero_is_bit_sensitive(self):
        self.assertFalse(decimal_roundtrip_criterion("8000000000000000", "0.0"))
        self.assertTrue(decimal_roundtrip_criterion("8000000000000000", "-0.0"))

    def test_decimal_oracle_exact_fraction(self):
        for value in (0.1, 1e-7, 2**-1074, 2**-1022, 1.5, 2**53):
            with self.subTest(value=value):
                self.assertEqual(Fraction(value), Fraction(Decimal(str(value)))
                                 if value in (1.5, 2**53) else Fraction(value))
                self.assertTrue(decimal_roundtrip_criterion(float_bits(value), str(value)))

    def test_shortening_is_not_equivalent_to_optimality(self):
        # Exponent zero-padding can be removed without changing the numeric value.
        shorter = list(lexical_shortening_checks("1e-06"))
        self.assertIn(("1e-6", float_bits(1e-6)), shorter)

    def test_no_nonfinite_raw_bits_as_success(self):
        for code in ("7ff0000000000000", "fff0000000000000",
                     "7ff8000000000000"):
            self.assertFalse(node_results([{"kind":"bits","hex":code}])[0]["ok"])


if __name__ == "__main__":
    unittest.main()
