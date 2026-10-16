"""Cross-runtime conformance: Python SI-Portable-1 against independent Node.js.

Node is optional for local Python-only work; GitHub cross-runtime CI requires it.
Only source shape/canonicalization is checked, not JS numeric execution.
"""
import json
import random
import shutil
import subprocess
import unittest
from pathlib import Path

from si.errors import SIError
from si.portable import parse_portable, canonical_source, structural_signature

JS = Path(__file__).resolve().parent.parent / "js" / "portable.js"
NODE = shutil.which("node")


def node_batch(sources):
    completed = subprocess.run(
        [NODE, str(JS)], input=json.dumps(sources), capture_output=True,
        encoding="utf-8", timeout=40, check=True
    )
    return json.loads(completed.stdout)


def normalize_python(source):
    try:
        ops = parse_portable(source)
        signature = [[op.opcode,
                      str(op.operand) if op.opcode == "PUSH" else op.operand,
                      op.target] for op in ops]
        return {"ok": True, "signature": signature,
                "canonical": canonical_source(ops)}
    except SIError as exc:
        return {"ok": False, "error": str(exc)}


@unittest.skipUnless(NODE, "Node.js unavailable; GitHub cross-runtime job requires it")
class CrossRuntimePortableTests(unittest.TestCase):
    def compare(self, sources, exact_errors=False):
        for index, (src, js_result) in enumerate(zip(sources, node_batch(sources))):
            py_result = normalize_python(src)
            with self.subTest(index=index, source=repr(src)[:90]):
                self.assertEqual(py_result["ok"], js_result["ok"])
                if py_result["ok"]:
                    self.assertEqual(py_result["signature"], js_result["signature"])
                    self.assertEqual(py_result["canonical"], js_result["canonical"])
                elif exact_errors:
                    self.assertEqual(py_result["error"], js_result["error"])

    def test_empty_comments_and_newlines(self):
        self.compare(["", "# hi", " \t ", "\n", "\r\n", " \r\n\t# note\r\n",
                      "# test\nPUSH 1\nPRINT", "PUSH 12#inline\nPRINT",
                      "PUSH 12\r\nPRINT\r\n"], exact_errors=True)

    def test_valid_integer_boundaries(self):
        self.compare(["PUSH 0", "PUSH -0", "PUSH +00012", "PUSH -99",
                      "PUSH " + "9"*1200, "PUSH 0000123456789",
                      "PUSH 12\nPUSH -3\nDIV\nPRINT"])

    def test_all_operations(self):
        names = ["ADD", "SUB", "MUL", "DIV", "LT", "EQ", "DUP",
                 "SWAP", "DROP", "PRINT", "HALT"]
        self.compare(names + ["push 7", "LABEL z", "JMP done\nLABEL done",
                              "PUSH 1\nJZ _e\nLABEL _e"])

    def test_labels_case_sensitive(self):
        self.compare(["LABEL a\nLABEL A\nJMP a\nJMP A",
                      "LABEL _a9\nJZ _a9", "LABEL "+"z"*64,
                      "LABEL "+"z"*65])

    def test_invalid_profiles(self):
        self.compare(["PUSH 1_0", "PUSH 0x10", "PUSH ½", "PUSH ⁴",
                      "PUSH 17\n#é", "PUSH 1\rPRINT",
                      "PUSH \"1\"", "LABEL 123", "JMP never", "LABEL x\nLABEL x",
                      "HALT\nBROKEN", "PUSH 9\nDROP x",
                      "\x00", "PUSH 5\x01", "PUSH " + "9"*1201],
                     exact_errors=True)

    def test_canonical_equivalence(self):
        examples = [" pUsH\t+0004# comment\r\nprint\r\n",
                    "JMP _end\nPUSH 8\nLABEL _end\nHALT"]
        self.compare(examples)
        self.compare([normalize_python(x)["canonical"] for x in examples])

    def test_seeded_valid_corpus_300(self):
        rng = random.Random(20261016)
        ops = ["ADD", "SUB", "MUL", "DIV", "LT", "EQ"]
        src = []
        for _ in range(300):
            a, b = rng.randint(-10**30, 10**30), rng.randint(-10**30, 10**30) or 1
            src.append(f"\tPuSh {a:+d}\nPUSH {b}#note\n{rng.choice(ops)}\nPRINT")
        self.compare(src)

    def test_seeded_random_ascii_300(self):
        rng = random.Random(71011)
        alphabet = "PUSH012+-# \t\n\r_a"
        sources = ["".join(rng.choice(alphabet) for _ in range(rng.randrange(0,90)))
                   for _ in range(300)]
        self.compare(sources, exact_errors=True)

    def test_utf16_surrogate_and_unicode(self):
        # json.dumps escapes these, so subprocess transport remains valid UTF-8.
        self.compare(["\U0001F642", "#\U0001F642", "PUSH 1\n#\u00e9"], exact_errors=False)

    def test_max_length_source(self):
        self.compare(["#" + "x"*99999, "#" + "x"*100000], exact_errors=True)


if __name__ == "__main__":
    unittest.main()
