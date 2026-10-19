"""AxiomFlow v0.19: small typed-function/module interpreter and pinned local builds.

Offline, no network imports, no external code execution and no Python eval.
This is an educational restricted DSL, not a process security sandbox.
"""
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation, ROUND_HALF_EVEN, localcontext
from hashlib import sha256
import json
from pathlib import Path
import re

from .language import AxiomError, Value, checked, binary

IDENT = r"[a-z_][a-z0-9_]*"
IDENT_RE = re.compile(IDENT + r"\Z")
TYPE_RE = re.compile(r"(?:scalar|[A-Z]{3})\Z")
FUNCTION = re.compile(
    rf"fn\s+({IDENT})\s*\((.*?)\)\s*->\s*(scalar|[A-Z]{{3}})\s*=\s*(.+)\Z"
)
TOKEN = re.compile(
    rf"\s*(\d+\.\d{{2}} [A-Z]{{3}}|\d+(?:\.\d+)?|{IDENT}(?:\.{IDENT})?|[()+*/,-])"
)
MONEY = re.compile(r"(\d+\.\d{2}) ([A-Z]{3})\Z")
NUMBER = re.compile(r"\d+(?:\.\d+)?\Z")
MAX_CALL_DEPTH = 32
MAX_FUNCTIONS = 100
MAX_MODULES = 16
MAX_TOTAL_SOURCE = 100_000


@dataclass(frozen=True)
class Function:
    name: str
    params: tuple
    returns: str
    body: tuple


class Expression:
    def __init__(self, source):
        self.tokens = []
        position = 0
        while position < len(source):
            if not source[position:].strip():
                break
            match = TOKEN.match(source, position)
            if match is None:
                raise AxiomError(f"invalid typed expression token at column {position + 1}")
            self.tokens.append(match[1])
            position = match.end()
            if len(self.tokens) > 2000:
                raise AxiomError("typed token budget exceeded")
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def take(self):
        tok = self.peek()
        if tok is None:
            raise AxiomError("unexpected end of typed expression")
        self.pos += 1
        return tok

    def factor(self):
        token = self.take()
        if token == "-":
            return ("neg", self.factor())
        if token == "(":
            expr = self.expr()
            if self.take() != ")":
                raise AxiomError("missing closing parenthesis")
            return expr
        literal = MONEY.fullmatch(token)
        if literal:
            return ("literal", Value(Decimal(literal[1]), literal[2]))
        if NUMBER.fullmatch(token):
            return ("literal", Value(Decimal(token)))
        if re.fullmatch(rf"{IDENT}(?:\.{IDENT})?", token):
            if self.peek() == "(":
                self.take()
                arguments = []
                if self.peek() != ")":
                    while True:
                        arguments.append(self.expr())
                        if len(arguments) > 12:
                            raise AxiomError("too many call arguments")
                        if self.peek() != ",":
                            break
                        self.take()
                if self.take() != ")":
                    raise AxiomError("missing call parenthesis")
                return ("call", token, tuple(arguments))
            if "." in token:
                raise AxiomError("qualified variable not supported")
            return ("name", token)
        raise AxiomError("invalid typed expression factor")

    def term(self):
        node = self.factor()
        while self.peek() in ("*", "/"):
            op = self.take()
            node = ("bin", op, node, self.factor())
        return node

    def expr(self):
        node = self.term()
        while self.peek() in ("+", "-"):
            op = self.take()
            node = ("bin", op, node, self.term())
        return node

    def complete(self):
        node = self.expr()
        if self.peek() is not None:
            raise AxiomError("trailing typed expression token")
        return node


def parse_function(line, namespace=""):
    match = FUNCTION.fullmatch(line)
    if not match:
        raise AxiomError("invalid function declaration")
    name, arguments, result_type, expression = match.groups()
    params = []
    if arguments.strip():
        for arg in arguments.split(","):
            spec = re.fullmatch(rf"\s*({IDENT})\s*:\s*(scalar|[A-Z]{{3}})\s*", arg)
            if spec is None:
                raise AxiomError("invalid typed parameter")
            if spec[1] in [p[0] for p in params]:
                raise AxiomError("duplicate typed parameter")
            params.append((spec[1], spec[2]))
    if len(params) > 12:
        raise AxiomError("too many parameters")
    full_name = namespace + "." + name if namespace else name
    return Function(full_name, tuple(params), result_type, Expression(expression).complete())


def parse_script(source, *, module=False, namespace=""):
    if type(source) is not str or len(source) > MAX_TOTAL_SOURCE or not source.isascii():
        raise AxiomError("invalid typed source")
    instructions, functions, uses = [], {}, []
    for line_number, raw in enumerate(source.splitlines(), 1):
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        try:
            if line.startswith("fn "):
                function = parse_function(line, namespace)
                if function.name in functions:
                    raise AxiomError("duplicate function")
                functions[function.name] = function
            elif not module and line.startswith("use "):
                mod = line[4:].strip()
                if not IDENT_RE.fullmatch(mod) or mod in uses:
                    raise AxiomError("invalid or duplicate module import")
                uses.append(mod)
            elif not module and line.startswith("let "):
                match = re.fullmatch(rf"let\s+({IDENT})\s*=\s*(.+)", line)
                if match is None:
                    raise AxiomError("invalid typed binding")
                instructions.append(("let", match[1], Expression(match[2]).complete()))
            elif not module and line.startswith("emit "):
                instructions.append(("emit", Expression(line[5:]).complete()))
            else:
                raise AxiomError("unsupported typed statement")
        except AxiomError as error:
            raise AxiomError(f"line {line_number}: {error}") from None
        if len(instructions) + len(functions) > 2000:
            raise AxiomError("statement budget exceeded")
    return tuple(instructions), functions, tuple(uses)


def value_type(value):
    return value.currency or "scalar"


def infer(node, scope, functions):
    kind = node[0]
    if kind == "literal":
        return value_type(node[1])
    if kind == "name":
        if node[1] not in scope:
            raise AxiomError("undefined typed name: " + node[1])
        return scope[node[1]]
    if kind == "neg":
        return infer(node[1], scope, functions)
    if kind == "call":
        if node[1] not in functions:
            raise AxiomError("unknown function: " + node[1])
        fn = functions[node[1]]
        if len(node[2]) != len(fn.params):
            raise AxiomError("wrong function arity")
        for expression, (_, expected) in zip(node[2], fn.params):
            if infer(expression, scope, functions) != expected:
                raise AxiomError("function parameter type mismatch")
        return fn.returns
    if kind == "bin":
        operator = node[1]
        left = infer(node[2], scope, functions)
        right = infer(node[3], scope, functions)
        if operator in ("+", "-"):
            if left != right:
                raise AxiomError("static currency/type mismatch")
            return left
        if operator == "*":
            if left != "scalar" and right != "scalar":
                raise AxiomError("static money multiplication rejected")
            return right if left == "scalar" else left
        if operator == "/":
            if right != "scalar":
                raise AxiomError("static division by money rejected")
            return left
    raise AxiomError("invalid typed expression")


def callees(node):
    if node[0] == "call":
        return {node[1]}.union(*(callees(x) for x in node[2]))
    if node[0] == "bin":
        return callees(node[2]) | callees(node[3])
    if node[0] == "neg":
        return callees(node[1])
    return set()


def static_check(instructions, functions):
    if len(functions) > MAX_FUNCTIONS:
        raise AxiomError("function budget exceeded")
    for function in functions.values():
        scope = dict(function.params)
        if infer(function.body, scope, functions) != function.returns:
            raise AxiomError("function return type mismatch: " + function.name)

    graph = {name: callees(fn.body) for name, fn in functions.items()}
    visited, visiting = set(), set()
    def visit(name):
        if name in visiting:
            raise AxiomError("recursive function graph rejected")
        if name in visited:
            return
        visiting.add(name)
        for callee in sorted(graph[name]):
            visit(callee)
        visiting.remove(name)
        visited.add(name)
    for name in sorted(functions):
        visit(name)

    scope = {}
    for statement in instructions:
        if statement[0] == "let":
            if statement[1] in scope:
                raise AxiomError("duplicate binding")
            scope[statement[1]] = infer(statement[2], scope, functions)
        else:
            infer(statement[1], scope, functions)


def execute_expression(node, scope, functions, depth=0):
    if depth > MAX_CALL_DEPTH:
        raise AxiomError("function call depth exceeded")
    kind = node[0]
    if kind == "literal":
        return checked(node[1])
    if kind == "name":
        return scope[node[1]]
    if kind == "neg":
        result = execute_expression(node[1], scope, functions, depth)
        return checked(Value(-result.amount, result.currency))
    if kind == "bin":
        return binary(node[1],
                      execute_expression(node[2], scope, functions, depth),
                      execute_expression(node[3], scope, functions, depth))
    if kind == "call":
        function = functions[node[1]]
        args = [execute_expression(x, scope, functions, depth) for x in node[2]]
        local = {name: val for (name, _), val in zip(function.params, args)}
        return execute_expression(function.body, local, functions, depth + 1)
    raise AxiomError("invalid expression")


def evaluate_typed(source, modules=None):
    """Parse, statically typecheck and evaluate without Python eval or IO."""
    modules = {} if modules is None else modules
    if type(modules) is not dict or len(modules) > MAX_MODULES:
        raise AxiomError("invalid module mapping")
    instructions, functions, uses = parse_script(source)
    if set(uses) != set(modules):
        raise AxiomError("module import / manifest mismatch")
    for namespace in sorted(modules):
        if not IDENT_RE.fullmatch(namespace):
            raise AxiomError("invalid module name")
        _, exported, _ = parse_script(modules[namespace], module=True, namespace=namespace)
        for name, function in exported.items():
            if name in functions:
                raise AxiomError("duplicate function")
            functions[name] = function
    static_check(instructions, functions)
    outputs, scope = [], {}
    try:
        with localcontext() as ctx:
            ctx.prec = 50
            ctx.rounding = ROUND_HALF_EVEN
            for stmt in instructions:
                if stmt[0] == "let":
                    scope[stmt[1]] = execute_expression(stmt[2], scope, functions)
                else:
                    outputs.append(execute_expression(stmt[1], scope, functions).text())
    except (InvalidOperation, OverflowError, ZeroDivisionError):
        raise AxiomError("numeric operation failed") from None
    return outputs


def _read_pinned(root, name, digest):
    if not isinstance(name, str) or not re.fullmatch(r"[a-z][a-z0-9_]*\.af", name):
        raise AxiomError("unsafe module filename")
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise AxiomError("invalid SHA256 digest")
    path = root / name
    if path.is_symlink() or not path.is_file():
        raise AxiomError("missing or symlinked local dependency")
    data = path.read_bytes()
    if len(data) > MAX_TOTAL_SOURCE:
        raise AxiomError("module size budget exceeded")
    if sha256(data).hexdigest() != digest:
        raise AxiomError("dependency digest mismatch")
    try:
        return data.decode("ascii")
    except UnicodeDecodeError:
        raise AxiomError("non-ASCII module") from None


def project_build(manifest_path):
    """Offline content-addressed local-only build. Never installs dependencies."""
    manifest_path = Path(manifest_path)
    if manifest_path.is_symlink() or not manifest_path.is_file():
        raise AxiomError("invalid manifest path")
    data = manifest_path.read_bytes()
    if len(data) > 20000:
        raise AxiomError("manifest size budget exceeded")
    try:
        manifest = json.loads(data)
    except (ValueError, UnicodeError):
        raise AxiomError("invalid JSON manifest") from None
    if (type(manifest) is not dict or set(manifest) !=
            {"format", "entry", "modules", "sha256"} or
            type(manifest["format"]) is not int or manifest["format"] != 1 or
            type(manifest["modules"]) is not dict or
            type(manifest["sha256"]) is not dict):
        raise AxiomError("invalid project manifest")
    modules = manifest["modules"]
    if len(modules) > MAX_MODULES or any(not IDENT_RE.fullmatch(m) for m in modules):
        raise AxiomError("invalid module mapping")
    paths = [manifest["entry"]] + [modules[m] for m in sorted(modules)]
    if len(paths) != len(set(paths)) or set(paths) != set(manifest["sha256"]):
        raise AxiomError("missing or surplus digest entries")
    root = manifest_path.parent
    verified = {p: _read_pinned(root, p, manifest["sha256"][p]) for p in paths}
    sources = {name: verified[modules[name]] for name in sorted(modules)}
    outputs = evaluate_typed(verified[manifest["entry"]], sources)
    # Canonical digest is independent of JSON key insertion order and file read order.
    lock = sha256(json.dumps(
        {"format": 1, "entry": manifest["entry"],
         "modules": {k: modules[k] for k in sorted(modules)},
         "sha256": {k: manifest["sha256"][k] for k in sorted(paths)}},
        sort_keys=True, separators=(",", ":")).encode("ascii")).hexdigest()
    return {"output": outputs, "lock_digest": lock, "module_order": sorted(modules)}
