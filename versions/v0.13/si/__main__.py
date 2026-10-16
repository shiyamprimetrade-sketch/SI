import argparse
from pathlib import Path
from .core import run,SIError
p=argparse.ArgumentParser(description='SI v0.1 terminal');p.add_argument('file',nargs='?');a=p.parse_args()
try:
    if a.file:
        for line in run(Path(a.file).read_text(encoding='utf-8'))['output']: print(line)
    else:
        print('SI REPL: enter one instruction per line; :run executes, :quit exits')
        lines=[]
        while True:
            s=input('si> ')
            if s==':quit':break
            if s==':run':
                print(run('\n'.join(lines)));lines=[]
            else:lines.append(s)
except (SIError,OSError,ValueError) as e:
    p.exit(1,f'SI error: {e}\n')