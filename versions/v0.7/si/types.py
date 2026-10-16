"""Forward dataflow stack type analysis. Types: INT, FLOAT, NUMBER (join)."""
from collections import deque
from dataclasses import dataclass
from .core import SIError
from .verify import successors

INT, FLOAT, NUMBER = 'INT', 'FLOAT', 'NUMBER'

@dataclass(frozen=True)
class TypeReport:
    incoming: tuple[tuple[str, ...] | None, ...]
    reachable: frozenset[int]
    max_stack_height: int

def join_type(a, b):
    return a if a == b else NUMBER

def arithmetic(a, b):
    if a == INT and b == INT: return INT
    if a == FLOAT or b == FLOAT: return FLOAT if NUMBER not in (a,b) else NUMBER
    return NUMBER

def typecheck(code, *, max_stack=1024):
    """Conservative verification: rejects stack-shape errors; propagates numeric types.

    NUMBER means INT or FLOAT. This is not a termination or division-by-zero proof.
    """
    n=len(code)
    states=[None]*(n+1)
    states[0]=()
    queue=deque([0]); pending={0}; peak=0
    while queue:
        pc=queue.popleft(); pending.remove(pc)
        if pc==n: continue
        inst=code[pc]; op=inst.op; arg=inst.arg
        if op not in {'PUSH','ADD','SUB','MUL','DIV','LT','EQ','DUP','SWAP','DROP','PRINT','LABEL','JMP','JZ','HALT'}:
            raise SIError(f'unknown opcode at {pc}')
        if op=='PUSH' and type(arg) is not int: raise SIError(f'invalid PUSH at {pc}')
        if op in ('JMP','JZ') and (type(arg) is not int or not 0<=arg<=n):
            raise SIError(f'invalid jump target at {pc}')
        s=list(states[pc]); needs={'ADD':2,'SUB':2,'MUL':2,'DIV':2,'LT':2,'EQ':2,'SWAP':2,'DUP':1,'DROP':1,'PRINT':1,'JZ':1}.get(op,0)
        if len(s)<needs: raise SIError(f'possible stack underflow at {pc}')
        if op=='PUSH': s.append(INT)
        elif op in ('ADD','SUB','MUL','DIV','LT','EQ'):
            b=s.pop(); a=s.pop()
            s.append(FLOAT if op=='DIV' else INT if op in ('LT','EQ') else arithmetic(a,b))
        elif op=='DUP': s.append(s[-1])
        elif op=='SWAP': s[-1],s[-2]=s[-2],s[-1]
        elif op in ('DROP','PRINT','JZ'): s.pop()
        if len(s)>max_stack: raise SIError(f'possible stack overflow at {pc}')
        peak=max(peak,len(s))
        nxt_state=tuple(s)
        for target in successors(code,pc):
            old=states[target]
            if old is None: merged=nxt_state
            else:
                if len(old)!=len(nxt_state): raise SIError(f'inconsistent stack height at {target}')
                merged=tuple(join_type(x,y) for x,y in zip(old,nxt_state))
            if merged!=old:
                states[target]=merged
                if target not in pending: queue.append(target);pending.add(target)
    return TypeReport(tuple(states),frozenset(i for i in range(n) if states[i] is not None),peak)