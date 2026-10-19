"""AxiomFlow terminal CLI prototype; not a system shell or security sandbox."""
import argparse
from pathlib import Path
import sys
from .language import AxiomError,evaluate
def main(argv=None):
    p=argparse.ArgumentParser(prog="axiomflow")
    p.add_argument("file",nargs="?")
    p.add_argument("--eval",dest="expression")
    a=p.parse_args(argv)
    try:
        if a.expression is not None:
            for x in evaluate(a.expression):print(x)
        elif a.file:
            path=Path(a.file)
            if path.stat().st_size>100000:raise AxiomError("source budget exceeded")
            for x in evaluate(path.read_text(encoding="utf-8")):print(x)
        else:
            print("AxiomFlow 0.1 terminal; :quit exits.")
            binds=[]
            while True:
                try:line=input("af> ")
                except EOFError:break
                if line.strip()==":quit":break
                try:
                    prior=sum(s.lstrip().startswith("emit ") for s in binds)
                    for x in evaluate("\n".join(binds+[line]))[prior:]:print(x)
                    if line.lstrip().startswith("let "):binds.append(line)
                except AxiomError as e:print("error:",e,file=sys.stderr)
    except (AxiomError,OSError,UnicodeError) as e:
        print("AxiomFlow error:",e,file=sys.stderr);return 2
    return 0
if __name__=="__main__":raise SystemExit(main())
