"""SI 0.2 compiler and independent bytecode virtual machine."""
import shlex
from .bytecode import Instruction, validate_bytecode
from .core import SIError
from .limits import (
    MAX_BYTECODE_INSTRUCTIONS, MAX_OUTPUT_CHARS, apply_binary,
    check_numeric, check_runtime_budgets, check_source,
    number_to_text, parse_integer,
)

ARITY = {'PUSH':1,'ADD':0,'SUB':0,'MUL':0,'DIV':0,'LT':0,'EQ':0,'DUP':0,'SWAP':0,'DROP':0,'PRINT':0,'LABEL':1,'JMP':1,'JZ':1,'HALT':0}
def compile_source(source: str) -> tuple[Instruction,...]:
    check_source(source)
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
        if len(lines)>MAX_BYTECODE_INSTRUCTIONS: raise SIError('instruction budget exceeded')
    code=[]
    for lineno,op,arg in lines:
        if op=='PUSH':
            arg=parse_integer(arg,lineno)
        elif op in ('JMP','JZ'):
            if arg not in labels: raise SIError(f'line {lineno}: unknown label {arg}')
            arg=labels[arg]
        else: arg=None
        code.append(Instruction(op,arg))
    return tuple(code)

def execute(code: tuple[Instruction,...], *, max_steps=10000, max_stack=1024,
            max_output_chars=MAX_OUTPUT_CHARS):
    check_runtime_budgets(max_steps, max_stack, max_output_chars)
    validate_bytecode(code)
    stack=[]; output=[]; pc=0; steps=0; output_chars=0
    while pc<len(code):
        steps+=1
        if steps>max_steps: raise SIError('step budget exceeded')
        inst=code[pc]; pc+=1; op=inst.op
        if op=='PUSH':
            stack.append(inst.arg)
        elif op in ('ADD','SUB','MUL','DIV','LT','EQ'):
            if len(stack)<2: raise SIError('stack underflow')
            b=stack.pop(); a=stack.pop()
            stack.append(apply_binary(op, a, b))
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
            rendered=number_to_text(stack.pop())
            if output_chars + len(rendered) > max_output_chars:
                raise SIError('output budget exceeded')
            output.append(rendered)
            output_chars += len(rendered)
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