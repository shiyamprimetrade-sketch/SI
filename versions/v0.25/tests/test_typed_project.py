"""AxiomFlow v0.19: typed functions, module graph, pinned local builds."""
import hashlib
import json
import random
import subprocess
import sys
import tempfile
import unittest
from decimal import Decimal, ROUND_HALF_EVEN
from pathlib import Path

from axiomflow.language import AxiomError
from axiomflow.typed import evaluate_typed, project_build, parse_script, static_check


MODULE = "fn tax(price: USD, rate: scalar) -> USD = price * (1 + rate)"
ENTRY = "use pricing\nemit pricing.tax(125.50 USD, 0.075)"
LOCAL = "fn double(value: USD) -> USD = value * 2\nemit double(19.99 USD)"


def make_project(root, entry=ENTRY, modules=None):
    modules = {"pricing": MODULE} if modules is None else modules
    (root / "main.af").write_text(entry, encoding="ascii")
    names = {"main.af": entry}
    paths = {}
    for key, text in modules.items():
        name = key + ".af"
        (root / name).write_text(text, encoding="ascii")
        names[name] = text
        paths[key] = name
    manifest = {
        "format": 1, "entry": "main.af", "modules": paths,
        "sha256": {path: hashlib.sha256(contents.encode("ascii")).hexdigest()
                   for path, contents in names.items()}
    }
    location = root / "axiomflow.json"
    location.write_text(json.dumps(manifest, sort_keys=True), encoding="ascii")
    return location


class TypedLanguageTests(unittest.TestCase):
    def test_local_function(self):
        self.assertEqual(evaluate_typed(LOCAL), ["39.98 USD"])

    def test_imported_function(self):
        self.assertEqual(evaluate_typed(ENTRY, {"pricing": MODULE}),
                         ["134.91 USD"])

    def test_nested_function_calls(self):
        source = ("fn twice(v: scalar) -> scalar = v * 2\n"
                  "fn four(v: scalar) -> scalar = twice(twice(v))\n"
                  "emit four(3)")
        self.assertEqual(evaluate_typed(source), ["12"])

    def test_scalar_and_multi_arg(self):
        program = ("fn weighted(a: scalar, b: scalar) -> scalar = "
                   "(a + b) / 2\nemit weighted(5, 7)")
        self.assertEqual(evaluate_typed(program), ["6"])

    def test_money_currency_type_rejected(self):
        for s in [
            "fn f(x: USD) -> USD = x\nemit f(2.00 EUR)",
            "fn f(x: USD) -> EUR = x\nemit f(2.00 USD)",
            "fn f(x: USD) -> USD = x + 1\nemit f(2.00 USD)",
            "fn f(x: USD) -> USD = x * x\nemit f(2.00 USD)",
            "fn f(x: USD) -> USD = x / x\nemit f(2.00 USD)",
        ]:
            with self.subTest(s=s), self.assertRaises(AxiomError):
                evaluate_typed(s)

    def test_argument_count(self):
        with self.assertRaisesRegex(AxiomError, "arity"):
            evaluate_typed("fn f(v:scalar)->scalar=v\nemit f(1,2)")

    def test_undefined_function_and_name(self):
        for s in ("emit mystery(1)",
                  "fn f(x:scalar)->scalar = y\nemit f(1)",
                  "emit pricing.tax(1.00 USD,1)"):
            with self.subTest(s=s),self.assertRaises(AxiomError):
                evaluate_typed(s)

    def test_recursive_rejection(self):
        src = ("fn f(x:scalar)->scalar = g(x)\n"
               "fn g(x:scalar)->scalar = f(x)\nemit f(1)")
        with self.assertRaisesRegex(AxiomError, "recursive"):
            evaluate_typed(src)

    def test_unsupported_constructs(self):
        for source in ("import os", "use ../evil", "emit __import__(1)",
                       "fn x(x:scalar)->scalar = open(x)\nemit x(1)",
                       "while 1", "fn x(x:scalar)->scalar=x;print(1)"):
            with self.subTest(source=source),self.assertRaises(AxiomError):
                evaluate_typed(source)

    def test_import_manifest_mismatch(self):
        with self.assertRaisesRegex(AxiomError, "mismatch"):
            evaluate_typed(ENTRY, {})
        with self.assertRaisesRegex(AxiomError, "mismatch"):
            evaluate_typed("emit 1", {"pricing": MODULE})

    def test_reject_duplicate_modules(self):
        with self.assertRaises(AxiomError):
            evaluate_typed("use pricing\nuse pricing\nemit 1",
                           {"pricing": MODULE})

    def test_static_binding_types(self):
        source = ("fn f(x:USD)->USD = x + 2.00 USD\n"
                  "let result=f(3.00 USD)\nemit result")
        self.assertEqual(evaluate_typed(source), ["5.00 USD"])

    def test_seeded_money_against_decimal_300(self):
        rng = random.Random(19019)
        for i in range(300):
            cents = rng.randrange(0, 300000)
            basis_points = rng.randrange(0, 5000)
            amount = Decimal(cents) / 100
            rate = Decimal(basis_points) / 10000
            src = f"use pricing\nemit pricing.tax({amount:.2f} USD,{rate})"
            expected = (amount * (1 + rate)).quantize(
                Decimal(".01"), rounding=ROUND_HALF_EVEN)
            with self.subTest(case=i):
                self.assertEqual(evaluate_typed(src, {"pricing": MODULE}),
                                 [f"{expected:.2f} USD"])

    def test_function_arity_and_dup_params(self):
        with self.assertRaisesRegex(AxiomError,"duplicate typed parameter"):
            evaluate_typed("fn bad(x:scalar,x:scalar)->scalar=x\nemit bad(1,2)")

    def test_empty_script(self):
        self.assertEqual(evaluate_typed(""), [])


class ProjectBuildTests(unittest.TestCase):
    def test_clean_pinned_project(self):
        with tempfile.TemporaryDirectory() as location:
            manifest = make_project(Path(location))
            result = project_build(manifest)
            self.assertEqual(result["output"], ["134.91 USD"])
            self.assertEqual(result["module_order"], ["pricing"])
            self.assertEqual(len(result["lock_digest"]), 64)
            self.assertEqual(result, project_build(manifest))

    def test_deterministic_manifest_insertion_order(self):
        with tempfile.TemporaryDirectory() as location:
            root = Path(location)
            manifest = make_project(root)
            first = project_build(manifest)["lock_digest"]
            doc = json.loads(manifest.read_text())
            doc = {key: doc[key] for key in reversed(list(doc))}
            manifest.write_text(json.dumps(doc))
            self.assertEqual(project_build(manifest)["lock_digest"], first)

    def test_tampered_dependency_rejected(self):
        with tempfile.TemporaryDirectory() as location:
            root = Path(location)
            manifest = make_project(root)
            (root / "pricing.af").write_text(MODULE + "\n# tampered")
            with self.assertRaisesRegex(AxiomError, "digest mismatch"):
                project_build(manifest)

    def test_traversal_rejected(self):
        with tempfile.TemporaryDirectory() as location:
            root = Path(location)
            manifest = make_project(root)
            obj = json.loads(manifest.read_text())
            obj["modules"]["pricing"] = "../danger.af"
            obj["sha256"]["../danger.af"] = obj["sha256"].pop("pricing.af")
            manifest.write_text(json.dumps(obj))
            with self.assertRaisesRegex(AxiomError, "unsafe module filename"):
                project_build(manifest)

    def test_unpinned_file_rejected(self):
        with tempfile.TemporaryDirectory() as location:
            root = Path(location)
            manifest = make_project(root)
            obj = json.loads(manifest.read_text())
            del obj["sha256"]["pricing.af"]
            manifest.write_text(json.dumps(obj))
            with self.assertRaisesRegex(AxiomError, "digest entries"):
                project_build(manifest)

    def test_symlink_rejected(self):
        with tempfile.TemporaryDirectory() as location:
            root = Path(location)
            manifest = make_project(root)
            (root / "pricing.af").unlink()
            (root / "pricing.af").symlink_to(root / "main.af")
            with self.assertRaisesRegex(AxiomError, "symlinked"):
                project_build(manifest)

    def test_invalid_manifest_shape(self):
        with tempfile.TemporaryDirectory() as location:
            path = Path(location) / "axiomflow.json"
            path.write_text('{"format":1}')
            with self.assertRaisesRegex(AxiomError,"invalid project manifest"):
                project_build(path)

    def test_cli_project(self):
        with tempfile.TemporaryDirectory() as location:
            manifest = make_project(Path(location))
            command = [sys.executable, "-m", "axiomflow", "--project", str(manifest)]
            run = subprocess.run(command, text=True, capture_output=True,
                                 timeout=15, check=False)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertEqual(run.stdout.strip(), "134.91 USD")

    def test_cli_rejects_tampered_project(self):
        with tempfile.TemporaryDirectory() as location:
            root = Path(location)
            manifest = make_project(root)
            (root / "main.af").write_text("emit 2", encoding="ascii")
            command = [sys.executable, "-m", "axiomflow", "--project", str(manifest)]
            run = subprocess.run(command, text=True, capture_output=True, timeout=15)
            self.assertEqual(run.returncode, 2)
            self.assertIn("digest mismatch", run.stderr)


if __name__ == "__main__":
    unittest.main()
