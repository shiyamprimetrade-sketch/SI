"""Conservative stack-height and numeric-type verifier for SI bytecode.

All numeric stack slots use the abstract type NUMBER (int or float).
The verifier proves consistent stack heights at reachable CFG joins, not termination.
"""
from collections import deque
from dataclasses import dataclass
from .core import SIError
from .compiler import Instruction

@dataclass(frozen=True)
class Verification:
    reachable: frozenset[int]
    stack_heights: tuple[int | None, ...]
    max_stack_height: int
    abstract_type: str = 'NUMBER'

EFFECT = {'PUSH':(0,1),'ADD':(2,1),'SUB':(2,1),'MUL':(2,1),
          'DIV':(2,1),'LT':(2,1),'EQ':(2,1),'DUP':(1,2),
          'SWAP':(2,2),'DROP':(1,0),'PRINT':(1,0),'LABEL':(0,0),
          'JMP':(0,0),'JZ':(1,0),'HALT':(0,0)}

def successors(code, pc):
    inst=code[pc]
    if inst.op=='HALT': return ()
    if inst.op=='JMP': return (inst.arg,)
    if inst.op=='JZ': return (inst.arg, pc+1)
    return (pc+1,)

def verify(code: tuple[Instruction,...], *, max_stack=1024):
    n=len(code)
    heights=[None]*(n+1)
    heights[0]=0
    q=deque([0]); max_seen=0
    while q:
        pc=q.popleft()
        if pc==n: continue
        inst=code[pc]
        if inst.op not in EFFECT: raise SIError(f'unknown opcode at {pc}')
        if inst.op=='PUSH' and type(inst.arg) is not int: raise SIError(f'invalid PUSH at {pc}')
        if inst.op in ('JMP','JZ') and (type(inst.arg) is not int or not 0<=inst.arg<=n):
            raise SIError(f'invalid jump target at {pc}')
        needed,produced=EFFECT[inst.op]
        h=heights[pc]
        if h<needed: raise SIError(f'possible stack underflow at {pc}')
        new=h-needed+produced
        if new>max_stack: raise SIError(f'possible stack overflow at {pc}')
        max_seen=max(max_seen,new)
        for nxt in successors(code,pc):
            if heights[nxt] is None:
                heights[nxt]=new;q.append(nxt)
            elif heights[nxt]!=new:
                raise SIError(f'inconsistent stack height at {nxt}: {heights[nxt]} vs {new}')
    return Verification(frozenset(i for i in range(n) if heights[i] is not None),tuple(heights),max_seen)

def remove_unreachable(code: tuple[Instruction,...]):
    """Preserve reachable instruction sequence and rebase all jump targets."""
    info=verify(code)
    indices=sorted(info.reachable)
    remap={old:new for new,old in enumerate(indices)}
    remap[len(code)]=len(indices)
    optimized=[]
    for old in indices:
        inst=code[old]
        if inst.op in ('JMP','JZ'):
            optimized.append(Instruction(inst.op,remap[inst.arg]))
        else: optimized.append(inst)
    return tuple(optimized)