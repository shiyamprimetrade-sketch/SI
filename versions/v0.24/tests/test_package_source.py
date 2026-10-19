"""Repeatable AxiomFlow v0.21 limited-source package integrity tests."""
import json
from hashlib import sha256
from pathlib import Path
import tempfile
import unittest
import zipfile
from tools.package_source import FILES,build

ROOT=Path(__file__).resolve().parent.parent


class SourcePackagingTests(unittest.TestCase):
    def test_two_builds_identical(self):
        with tempfile.TemporaryDirectory() as d:
            first=Path(d)/"first.zip";second=Path(d)/"second.zip"
            digest1=build(ROOT,first);digest2=build(ROOT,second)
            self.assertEqual(digest1,digest2)
            self.assertEqual(first.read_bytes(),second.read_bytes())
            with zipfile.ZipFile(first) as z:
                names=z.namelist()
                self.assertEqual(len(names),len(FILES)+1)
                manifest=json.loads(z.read("axiomflow-v0.24/RELEASE-MANIFEST.json"))
                self.assertEqual(manifest["format"],"axiomflow-source-v1")
                for path in FILES:
                    self.assertEqual(manifest["files"][path],
                        sha256(z.read("axiomflow-v0.24/"+path)).hexdigest())

    def test_missing_or_symlink_file_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaisesRegex(ValueError,"missing or symlinked"):
                build(d,Path(d)/"x.zip")

    def test_archive_does_not_contain_external_path(self):
        with tempfile.TemporaryDirectory() as d:
            result=Path(d)/"release.zip"
            build(ROOT,result)
            with zipfile.ZipFile(result) as z:
                self.assertTrue(all(n.startswith("axiomflow-v0.24/") for n in z.namelist()))
                self.assertFalse(any(".." in n for n in z.namelist()))


if __name__=="__main__":
    unittest.main()
