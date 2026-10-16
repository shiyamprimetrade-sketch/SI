"""SI 0.2 compiler and independent bytecode virtual machine."""
import shlex
from dataclasses import dataclass
from .core import SIError

ARITY = {'PUSH':1,'ADD':0,'SUB':0,'MUL':0,'DIV':0,'LT':0,'EQ':0,'DUP':0,'SWAP':0,'DROP':0,'PRINT':0,'LABEL':1,'JMP':1,'JZ':1,'HALT':0}
@dataclass(frozen=True)
class Instruction:
    op: str
    arg: int | None = None

def compile_source(source: str) -> tuple[Instruction,...]:
    lines=[]; labels={}
    for lineno, raw in enumerate(source.splitlines(),1):
        try: tokens=shlex.split(raw,comments=True)
        except ValueError as e: raise SIError(f'line {lineno}: {e}') from None
        if not tokens: continue
        op=tokens[0].upper()
        if op not in ARITY: raise SIError(f'line {lineno}: unknown opcode {op}')
        if len(tokens)-1!=ARITY[op]: raise SIError(f'line {lineno}: {op} needs {ARITY[op]} args')
        arg=tokens[1] if len(tokens)>1 else None
        if op=='LABEL':
            if arg in labels: raise SIError(f'line {lineno}: duplicate label {arg}')
            labels[arg]=len(lines)
        lines.append((lineno,op,arg))
    code=[]
    for lineno,op,arg in lines:
        if op=='PUSH':
            try: arg=int(arg)
            except ValueError: raise SIError(f'line {lineno}: integer required') from None
        elif op in ('JMP','JZ'):
            if arg not in labels: raise SIError(f'line {lineno}: unknown label {arg}')
            arg=labels[arg]
        else: arg=None
        code.append(Instruction(op,arg))
    return tuple(code)

def execute(code: tuple[Instruction,...], *, max_steps=10000, max_stack=1024):
    stack=[]; output=[]; pc=0; steps=0
    while pc<len(code):
        steps+=1
        if steps>max_steps: raise SIError('step budget exceeded')
        inst=code[pc]; pc+=1; op=inst.op
        if op=='PUSH': stack.append(inst.arg)
        elif op in ('ADD','SUB','MUL','DIV','LT','EQ'):
            if len(stack)<2: raise SIError('stack underflow')
            b=stack.pop(); a=stack.pop()
            if op=='DIV' and b==0: raise SIError('division by zero')
            stack.append({'ADD':lambda:a+b,'SUB':lambda:a-b,'MUL':lambda:a*b,'DIV':lambda:a/b,'LT':lambda:int(a<b),'EQ':lambda:int(a==b)}[op]())
        elif op=='DUP':
            if not stack: raise SIError('stack underflow')
            stack.append(stack[-1])
        elif op=='SWAP':
            if len(stack)<2: raise SIError('stack underflow')
            stack[-1],stack[-2]=stack[-2],stack[-1]
        elif op=='DROP':
            if not stack: raise SIError('stack underflow')
            stack.pop()
        elif op=='PRINT':
            if not stack: raise SIError('stack underflow')
            output.append(str(stack.pop()))
        elif op=='JMP': pc=inst.arg
        elif op=='JZ':
            if not stack: raise SIError('stack underflow')
            if stack.pop()==0: pc=inst.arg
        elif op=='HALT': break
        elif op!='LABEL': raise SIError('invalid bytecode')
        if len(stack)>max_stack: raise SIError('stack budget exceeded')
    return {'output':output,'stack':stack,'steps':steps}

def run_compiled(source,**kwargs):
    return execute(compile_source(source),**kwargs)