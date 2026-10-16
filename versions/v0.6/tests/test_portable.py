"""SI v0.6 bounded bytecode interchange regression tests."""
import hashlib
import json
import unittest
from si.compiler import Instruction, compile_source, execute
from si.core import SIError
from si.portable import dumps, loads, validate, execute_checked, MAX_BYTES


def envelope(rows):
    payload = {"format": "si-bytecode-v1", "instructions": rows}
    digest = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")).hexdigest()
    return json.dumps({"payload": payload, "sha256": digest}, sort_keys=True, separators=(",", ":"))


class PortableTests(unittest.TestCase):
    def test_round_trip(self):
        code = compile_source("PUSH 5\nPUSH 6\nMUL\nPRINT\nHALT")
        self.assertEqual(loads(dumps(code)), code)
        self.assertEqual(execute_checked(dumps(code))["output"], ["30"])

    def test_deterministic_bytes(self):
        code = compile_source("PUSH -7\nPUSH 2\nADD\nPRINT")
        self.assertEqual(dumps(code), dumps(code))

    def test_empty_program(self):
        self.assertEqual(loads(dumps(())), ())

    def test_tamper_detected(self):
        text = dumps(compile_source("PUSH 1\nHALT"))
        with self.assertRaisesRegex(SIError, "digest mismatch"):
            loads(text.replace('"PUSH",1', '"PUSH",2'))

    def test_invalid_opcode_even_with_matching_digest(self):
        with self.assertRaisesRegex(SIError, "invalid opcode"):
            loads(envelope([["SYSTEM", None]]))

    def test_negative_jump_even_with_matching_digest(self):
        with self.assertRaisesRegex(SIError, "invalid jump target"):
            loads(envelope([["JMP", -1]]))

    def test_out_of_bounds_jump(self):
        with self.assertRaisesRegex(SIError, "invalid jump target"):
            loads(envelope([["JMP", 2]]))

    def test_bool_is_not_integer(self):
        with self.assertRaisesRegex(SIError, "signed 64-bit"):
            loads(envelope([["PUSH", True]]))

    def test_large_integer_rejected(self):
        with self.assertRaisesRegex(SIError, "signed 64-bit"):
            dumps((Instruction("PUSH", 2**64),))

    def test_extra_arg_rejected(self):
        with self.assertRaisesRegex(SIError, "unexpected argument"):
            loads(envelope([["HALT", 9]]))

    def test_invalid_row_rejected(self):
        with self.assertRaisesRegex(SIError, "invalid instruction"):
            loads(envelope([["PUSH"]]))

    def test_duplicate_json_key_rejected(self):
        data = dumps(())
        with self.assertRaisesRegex(SIError, "duplicate JSON key"):
            loads(data[:-1] + ',"sha256":"' + '0'*64 + '"}')

    def test_underflow_rejected_statically(self):
        with self.assertRaisesRegex(SIError, "underflow"):
            loads(envelope([["ADD", None]]))

    def test_inconsistent_stack_height_rejected(self):
        code = compile_source("PUSH 0\nJZ x\nPUSH 1\nLABEL x\nHALT")
        with self.assertRaisesRegex(SIError, "inconsistent stack height"):
            dumps(code)

    def test_runtime_division_zero(self):
        code = compile_source("PUSH 1\nPUSH 0\nDIV")
        with self.assertRaisesRegex(SIError, "division by zero"):
            execute_checked(dumps(code))

    def test_step_budget_loop(self):
        code = compile_source("LABEL loop\nJMP loop")
        with self.assertRaisesRegex(SIError, "step budget exceeded"):
            execute_checked(dumps(code), max_steps=10)

    def test_max_instructions(self):
        with self.assertRaisesRegex(SIError, "instruction limit"):
            dumps(compile_source("PUSH 1\nPUSH 2\nHALT"), max_instructions=2)

    def test_max_stack(self):
        with self.assertRaisesRegex(SIError, "overflow"):
            dumps(compile_source("PUSH 1\nPUSH 2"), max_stack=1)

    def test_bytes_limit(self):
        with self.assertRaisesRegex(SIError, "size limit"):
            loads(" " * (MAX_BYTES + 1))

    def test_invalid_budget(self):
        with self.assertRaisesRegex(SIError, "max_steps"):
            execute_checked(dumps(()), max_steps=0)

    def test_invalid_payload(self):
        with self.assertRaisesRegex(SIError, "invalid bytecode envelope"):
            loads("{}")

    def test_invalid_nonfinite(self):
        with self.assertRaisesRegex(SIError, "invalid JSON"):
            loads("NaN")

    def test_rehash_not_authentication(self):
        # An attacker able to rewrite both payload and hash can forge a valid envelope.
        forged = envelope([["PUSH", 4], ["PRINT", None]])
        self.assertEqual(execute_checked(forged)["output"], ["4"])


if __name__ == "__main__":
    unittest.main()