"""Independent Node.js VM vs three Python SI engines on portable programs.

Comparisons include stack numeric tags, output, steps and coarse error categories.
BigInt/Number semantics are tested on bounded common-domain numeric cases.
"""
import json
import random
import shutil
import subprocess
import unittest
from pathlib import Path

from si.core import run, SIError
from si.compiler import run_compiled
from si.reference import evaluate as reference_evaluate
from si.portable import parse_portable
from si.limits import MAX_INTEGER_BITS

NODE = shutil.which("node")
VM = Path(__file__).resolve().parent.parent / "js" / "vm.js"


def python_result(src, options=None):
    options = options or {}
    try:
        parse_portable(src)
        result = run(src, **options)
        def number(x):
            return {"kind": "float" if type(x) is float else "int", "text": str(x)}
        other = run_compiled(src, **options)
        independent = reference_evaluate(src, **options)
        if result != other or result != independent:
            raise AssertionError("Python engine mismatch")
        return {"ok": True, "output": result["output"],
                "stack": [number(x) for x in result["stack"]],
                "steps": result["steps"]}
    except SIError as e:
        text = str(e)
        if "budget exceeded" in text: category = text
        elif "underflow" in text: category = "stack underflow"
        elif "division by zero" in text: category = "division by zero"
        elif "numeric overflow" in text: category = "numeric overflow"
        elif "non-finite" in text: category = "non-finite numeric result"
        else: category = "parse error"
        return {"ok": False, "category": category}


def node_results(samples):
    raw = json.dumps([{"source": s, "options": o} for s, o in samples])
    cp = subprocess.run([NODE, str(VM)], input=raw, text=True,
                        capture_output=True, check=True, timeout=40)
    return json.loads(cp.stdout)


@unittest.skipUnless(NODE, "Node is required for GitHub cross-runtime CI")
class RuntimeParityTests(unittest.TestCase):
    def compare(self, samples):
        actual = node_results(samples)
        self.assertEqual(len(actual), len(samples))
        for idx, ((source, options), observed) in enumerate(zip(samples, actual)):
            expected = python_result(source, options)
            with self.subTest(case=idx, snippet=source[:90]):
                self.assertEqual(observed["ok"], expected["ok"])
                if expected["ok"]:
                    self.assertEqual(observed["output"], expected["output"])
                    self.assertEqual(observed["stack"], expected["stack"])
                    self.assertEqual(observed["steps"], expected["steps"])
                else:
                    self.assertEqual(observed["category"], expected["category"])

    def test_empty_and_comments(self):
        self.compare([("",{}),("#comment\n\n",{}),("   \nHALT\n#tail",{})])

    def test_basic_stack(self):
        self.compare([("PUSH 2\nPUSH 3\nADD",{}),
                      ("PUSH -9\nDUP\nSWAP\nPRINT\nDROP",{}),
                      ("PUSH 3\nPUSH 6\nEQ\nPRINT",{}),
                      ("PUSH -1\nPUSH 1\nLT\nPRINT",{})])

    def test_true_division_and_signed_zero(self):
        self.compare([("PUSH 0\nPUSH -3\nDIV\nPRINT",{}),
                      ("PUSH 0\nPUSH 3\nDIV\nPRINT",{}),
                      ("PUSH -7\nPUSH 2\nDIV\nPRINT",{}),
                      ("PUSH 1\nPUSH 2\nDIV\nPUSH 2\nMUL\nPRINT",{})])

    def test_branch_and_halt(self):
        self.compare([("PUSH 0\nJZ end\nPUSH 19\nLABEL end\nHALT",{}),
                      ("PUSH 1\nJZ end\nPUSH 19\nLABEL end\nHALT",{}),
                      ("JMP end\nPUSH 8\nLABEL end\nPUSH 3",{}),
                      ("PUSH 3\nHALT\nPUSH 10",{})])

    def test_countdown(self):
        self.compare([("PUSH 3\nLABEL loop\nDUP\nPRINT\nPUSH 1\nSUB\nDUP\nJZ end\nJMP loop\nLABEL end\nDROP",{})])

    def test_boundaries_step_stack_output(self):
        self.compare([("PUSH 1",{"max_steps":0}),
                      ("PUSH 1",{"max_stack":0}),
                      ("PUSH 1\nPRINT",{"max_output_chars":0}),
                      ("PUSH 1\nPRINT",{"max_output_chars":1}),
                      ("#comment",{"max_steps":0}),
                      ("HALT",{"max_steps":0})])

    def test_repeated_output(self):
        self.compare([("PUSH 44\nDUP\nPRINT\nPRINT",{"max_output_chars":3}),
                      ("PUSH 44\nDUP\nPRINT\nPRINT",{"max_output_chars":4})])

    def test_underflows(self):
        self.compare([(op,{}) for op in ("ADD","SUB","MUL","DIV","DUP",
                                          "SWAP","DROP","PRINT","JZ end\nLABEL end")])

    def test_division_by_zero(self):
        self.compare([("PUSH 5\nPUSH 0\nDIV",{}),
                      ("PUSH 0\nPUSH 0\nDIV",{})])

    def test_overflow_integer_bits(self):
        giant="9"*1200
        self.compare([("PUSH "+giant+"\nPUSH "+giant+"\nMUL",{}),
                      ("PUSH "+giant+"\nDROP",{})])

    def test_numeric_overflow(self):
        self.compare([("PUSH 1"+"0"*400+"\nPUSH 1\nDIV",{})])

    def test_nonfinite_float(self):
        src=("PUSH 1"+"0"*300+"\nPUSH 1\nDIV\nPUSH 1\nPUSH 1"+
             "0"*300+"\nDIV\nDIV")
        self.compare([(src,{})])

    def test_rejected_malformed_source(self):
        self.compare([("PUSH 1_0",{}),("LABEL x\nLABEL x",{}),
                      ("HALT\nJMP missing",{}),("LABEL 999",{}),
                      ("PUSH 1\rADD",{})])

    def test_seeded_small_integer_arithmetic_360(self):
        rng=random.Random(12026)
        samples=[]
        for _ in range(360):
            a,b=rng.randrange(-100000,100001),rng.randrange(-100000,100001)
            op=rng.choice(("ADD","SUB","MUL","DIV","LT","EQ"))
            if op=="DIV" and b==0:b=1
            samples.append((f"PUSH {a}\nPUSH {b}\n{op}\nPRINT",{}))
        self.compare(samples)

    def test_seeded_branches_240(self):
        rng=random.Random(12240)
        samples=[]
        for _ in range(240):
            flag=rng.randrange(-1,2)
            a,b=rng.randrange(-500,501),rng.randrange(-500,501)
            source=(f"PUSH {flag}\nJZ left\nPUSH {a}\nJMP end\n"
                    f"LABEL left\nPUSH {b}\nLABEL end\nPRINT")
            samples.append((source,{}))
        self.compare(samples)

    def test_seeded_budget_variations_150(self):
        rng=random.Random(12015)
        samples=[]
        for _ in range(150):
            steps=rng.randrange(0,5)
            limit=rng.randrange(0,3)
            a=rng.randrange(-100,101)
            samples.append((f"PUSH {a}\nDUP\nPRINT\nPRINT",
                            {"max_steps":steps,"max_stack":limit}))
        self.compare(samples)

    def test_float_exact_display_simple(self):
        self.compare([("PUSH 1\nPUSH 4\nDIV\nPRINT",{}),
                      ("PUSH 1\nPUSH 8\nDIV\nPRINT",{}),
                      ("PUSH -0\nPUSH -1\nDIV\nPRINT",{})])

    def test_precision_boundary_is_documented(self):
        # Exact integers: JS BigInt must preserve values beyond binary64 precision.
        src="PUSH 9007199254740993\nPUSH 2\nADD\nPRINT"
        self.compare([(src,{})])


if __name__ == "__main__":
    unittest.main()
