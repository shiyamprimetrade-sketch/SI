"""Deterministic source archive of the v0.22 AxiomFlow data interoperability demo.

Releases a limited source subset. Does not install dependencies or promise a
standalone binary; inherited SI research snapshots are outside this bundle.
"""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import zipfile

FILES=(
    "axiomflow/__init__.py",
    "axiomflow/__main__.py",
    "axiomflow/api.py",
    "axiomflow/data.py",
    "axiomflow/language.py",
    "axiomflow/typed.py",
    "axiomflow/table.py",
    "data/landed_cost.csv",
    "web/index.html",
    "web/app.js",
    "web/style.css",
    "project/main.af",
    "project/pricing.af",
    "project/axiomflow.json",
)
STAMP=(2020,1,1,0,0,0)


def build(root, output):
    root=Path(root).resolve()
    output=Path(output)
    manifest={}
    entries={}
    for filename in FILES:
        file=root/filename
        if file.is_symlink() or not file.is_file():
            raise ValueError("missing or symlinked release file: "+filename)
        data=file.read_bytes()
        entries[filename]=data
        manifest[filename]=sha256(data).hexdigest()
    entries["RELEASE-MANIFEST.json"]=(json.dumps(
        {"files":manifest,"format":"axiomflow-source-v1"},
        sort_keys=True,separators=(",",":"))+"\n").encode("utf-8")
    output.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(output,"w",compression=zipfile.ZIP_STORED) as bundle:
        for filename,contents in sorted(entries.items()):
            info=zipfile.ZipInfo("axiomflow-v0.22/"+filename,STAMP)
            info.compress_type=zipfile.ZIP_STORED
            info.external_attr=0o100644<<16
            info.create_system=3
            bundle.writestr(info,contents)
    return sha256(output.read_bytes()).hexdigest()


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    root=Path(__file__).resolve().parents[1]
    print(json.dumps({"bundle_sha256":build(root,args.output),
                      "files":len(FILES),"format":"axiomflow-source-v1"},
                     sort_keys=True))


if __name__=="__main__":
    main()
