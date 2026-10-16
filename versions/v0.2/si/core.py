"""SI v0.1: deterministic stack language; no eval, no filesystem/network primitives."""
import shlex

class SIError(Exception): pass

OPS = {'ADD': lambda a,b:a+b, 'SUB':lambda a,b:a-b, 'MUL':lambda a,b:a*b, 'DIV':lambda a,b:a/b if b else (_ for _ in ()).throw(SIError('division by zero')), 'LT':lambda a,b:int(a<b), 'EQ':lambda a,b:int(a==b)}

def run(source, *, max_steps=10000, max_stack=1024):
    stack=[]; output=[]; steps=0
    lines=[(i,shlex.split(s, comments=True)) for i,s in enumerate(source.splitlines(),1)]
    labels={tokens[1]:pc for pc,(_,tokens) in enumerate(lines) if len(tokens)==2 and tokens[0]=='LABEL'}
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