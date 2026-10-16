"""SI v0.1: deterministic stack language; no eval, no filesystem/network primitives."""
import shlex

class SIError(Exception): pass

OPS = {'ADD': lambda a,b:a+b, 'SUB':lambda a,b:a-b, 'MUL':lambda a,b:a*b, 'DIV':lambda a,b:a/b if b else (_ for _ in ()).throw(SIError('division by zero')), 'LT':lambda a,b:int(a<b), 'EQ':lambda a,b:int(a==b)}

# Kept independent from compiler.ARITY so differential tests exercise both parsers.
SOURCE_ARITY = {
    **{op: 0 for op in OPS},
    **{op: 0 for op in ('DUP', 'SWAP', 'DROP', 'PRINT', 'HALT')},
    **{op: 1 for op in ('PUSH', 'LABEL', 'JMP', 'JZ')},
}

def run(source, *, max_steps=10000, max_stack=1024):
    stack=[]; output=[]; steps=0
    lines=[]; labels={}
    for lineno, raw in enumerate(source.splitlines(), 1):
        try: tokens=shlex.split(raw, comments=True)
        except ValueError as exc: raise SIError(f'line {lineno}: {exc}') from None
        # Empty and comment-only lines have no execution cost, like compiler.py.
        if not tokens: continue
        op=tokens[0].upper()
        if op not in SOURCE_ARITY: raise SIError(f'line {lineno}: unknown opcode {op}')
        if len(tokens)-1 != SOURCE_ARITY[op]:
            raise SIError(f'line {lineno}: {op} needs {SOURCE_ARITY[op]} args')
        if op == 'LABEL':
            name=tokens[1]
            if name in labels: raise SIError(f'line {lineno}: duplicate label {name}')
            labels[name]=len(lines)
        lines.append((lineno, tokens))

    # Validate reachable and unreachable syntax without invoking the compiler.
    # Mirrors compiler's second pass; runtime stack errors remain dynamic.
    for lineno,tokens in lines:
        op=tokens[0].upper()
        if op=='PUSH':
            try: int(tokens[1])
            except ValueError: raise SIError(f'line {lineno}: integer required') from None
        elif op in ('JMP','JZ') and tokens[1] not in labels:
            raise SIError('unknown label')
    pc=0
    while pc<len(lines):
        steps+=1
        if steps>max_steps: raise SIError('step budget exceeded')
        lineno,t=lines[pc]; pc+=1
        if not t: continue
        op=t[0].upper(); args=t[1:]
        def arity(n):
            if len(args)!=n: raise SIError(f'line {lineno}: {op} needs {n} args')
        if op=='PUSH':
            arity(1)
            try: v=int(args[0])
            except ValueError: raise SIError(f'line {lineno}: integer required') from None
            stack.append(v)
        elif op in OPS:
            arity(0)
            if len(stack)<2: raise SIError('stack underflow')
            b=stack.pop();a=stack.pop();stack.append(OPS[op](a,b))
        elif op=='DUP':
            arity(0)
            if not stack: raise SIError('stack underflow')
            stack.append(stack[-1])
        elif op=='SWAP':
            arity(0)
            if len(stack)<2: raise SIError('stack underflow')
            stack[-1],stack[-2]=stack[-2],stack[-1]
        elif op=='DROP':
            arity(0)
            if not stack: raise SIError('stack underflow')
            stack.pop()
        elif op=='PRINT':
            arity(0)
            if not stack: raise SIError('stack underflow')
            output.append(str(stack.pop()))
        elif op=='LABEL': arity(1)
        elif op in ('JMP','JZ'):
            arity(1)
            if args[0] not in labels: raise SIError('unknown label')
            if op=='JMP': pc=labels[args[0]]
            else:
                if not stack: raise SIError('stack underflow')
                if stack.pop()==0: pc=labels[args[0]]
        elif op=='HALT': arity(0);break
        else: raise SIError(f'line {lineno}: unknown opcode {op}')
        if len(stack)>max_stack: raise SIError('stack budget exceeded')
    return {'output':output,'stack':stack,'steps':steps}