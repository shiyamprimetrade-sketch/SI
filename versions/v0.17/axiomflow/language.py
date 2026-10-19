"""AxiomFlow v0.1: deterministic, intentionally limited money DSL.

Statements: let name = expr | emit expr.
Expressions: decimal numbers, XX.YY USD money, names, + - * /,
unary minus and parentheses. No imports, reflection or I/O.
"""
import re
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_EVEN, localcontext, InvalidOperation

class AxiomError(Exception): pass

@dataclass(frozen=True)
class Value:
    amount: Decimal
    currency: str | None = None
    def text(self):
        return f"{self.amount:.2f} {self.currency}" if self.currency else format(self.amount,"f")

TOK=re.compile(r"\s*(\d+\.\d{2} [A-Z]{3}|\d+(?:\.\d+)?|[a-z_][a-z0-9_]*|[()+*/-])")
MONEY=re.compile(r"(\d+\.\d{2}) ([A-Z]{3})\Z")
NUMBER=re.compile(r"\d+(?:\.\d+)?\Z")
NAME=re.compile(r"[a-z_][a-z0-9_]*\Z")
MAX_ABS=Decimal("1e30")

class Parser:
    def __init__(self, source):
        self.tokens=[];p=0
        while p<len(source):
            if not source[p:].strip():break
            m=TOK.match(source,p)
            if not m:raise AxiomError(f"invalid token at column {p+1}")
            self.tokens.append(m.group(1));p=m.end()
            if len(self.tokens)>10000:raise AxiomError("token budget exceeded")
        self.pos=0
    def peek(self):
        return self.tokens[self.pos] if self.pos<len(self.tokens) else None
    def take(self):
        t=self.peek()
        if t is None:raise AxiomError("unexpected end of expression")
        self.pos+=1;return t
    def factor(self):
        t=self.take()
        if t=="-":return ("neg",self.factor())
        if t=="(":
            n=self.expr()
            if self.take()!=")":raise AxiomError("missing closing parenthesis")
            return n
        m=MONEY.fullmatch(t)
        if m:return ("literal",Value(Decimal(m[1]),m[2]))
        if NUMBER.fullmatch(t):return ("literal",Value(Decimal(t)))
        if NAME.fullmatch(t):return ("name",t)
        raise AxiomError("invalid factor")
    def term(self):
        n=self.factor()
        while self.peek() in ("*","/"):
            op=self.take();n=("bin",op,n,self.factor())
        return n
    def expr(self):
        n=self.term()
        while self.peek() in ("+","-"):
            op=self.take();n=("bin",op,n,self.term())
        return n
    def complete(self):
        n=self.expr()
        if self.peek() is not None:raise AxiomError("trailing token")
        return n

def parse_program(source):
    if type(source) is not str:raise AxiomError("source must be a string")
    if len(source)>100000:raise AxiomError("source budget exceeded")
    if not source.isascii():raise AxiomError("only ASCII source supported")
    lines=source.splitlines()
    if len(lines)>2000:raise AxiomError("line budget exceeded")
    statements=[]
    for number,raw in enumerate(lines,1):
        line=raw.split("#",1)[0].strip()
        if not line:continue
        if line.startswith("let "):
            m=re.fullmatch(r"let\s+([a-z_][a-z0-9_]*)\s*=\s*(.+)",line)
            if not m:raise AxiomError(f"line {number}: invalid let")
            statements.append(("let",m[1],Parser(m[2]).complete()))
        elif line.startswith("emit "):
            statements.append(("emit",Parser(line[5:]).complete()))
        else:raise AxiomError(f"line {number}: unknown statement")
    return tuple(statements)

def checked(v):
    if not v.amount.is_finite() or abs(v.amount)>MAX_ABS:
        raise AxiomError("numeric bound exceeded")
    if v.currency:return Value(v.amount.quantize(Decimal(".01"),rounding=ROUND_HALF_EVEN),v.currency)
    return v

def binary(op,a,b):
    if op in ("+","-"):
        if a.currency!=b.currency:raise AxiomError("currency/type mismatch")
        return checked(Value(a.amount+b.amount if op=="+" else a.amount-b.amount,a.currency))
    if op=="*":
        if a.currency and b.currency:raise AxiomError("money multiplied by money")
        return checked(Value(a.amount*b.amount,a.currency or b.currency))
    if op=="/":
        if b.amount==0:raise AxiomError("division by zero")
        if b.currency:raise AxiomError("division by money")
        return checked(Value(a.amount/b.amount,a.currency))
    raise AxiomError("invalid operator")

def eval_expr(n,env):
    if n[0]=="literal":return checked(n[1])
    if n[0]=="name":
        if n[1] not in env:raise AxiomError("undefined name")
        return env[n[1]]
    if n[0]=="neg":
        v=eval_expr(n[1],env);return checked(Value(-v.amount,v.currency))
    if n[0]=="bin":return binary(n[1],eval_expr(n[2],env),eval_expr(n[3],env))
    raise AxiomError("invalid expression")

def evaluate(source):
    parsed=parse_program(source);env={};out=[]
    try:
        with localcontext() as ctx:
            ctx.prec=50;ctx.rounding=ROUND_HALF_EVEN
            for op,*args in parsed:
                if op=="let":
                    name,expr=args
                    if name in env:raise AxiomError("duplicate binding")
                    env[name]=eval_expr(expr,env)
                else:out.append(eval_expr(args[0],env).text())
    except (InvalidOperation,OverflowError,ZeroDivisionError):
        raise AxiomError("numeric operation failed") from None
    return out
