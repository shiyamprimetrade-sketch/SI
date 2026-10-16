"""Bounded, deterministic SI bytecode JSON interchange.

SHA-256 detects accidental changes, not adversarial forgery. This is not
an authentication mechanism or a sandbox for hostile Python code.
"""
import hashlib
import hmac
import json

from .compiler import Instruction, execute
from .core import SIError
from .types import typecheck
from .verify import verify

FORMAT = "si-bytecode-v1"
MAX_BYTES = 1_000_000
MAX_INSTRUCTIONS = 10_000
MIN_INT = -(2**63)
MAX_INT = 2**63 - 1
OPS = frozenset({"PUSH", "ADD", "SUB", "MUL", "DIV", "LT", "EQ", "DUP", "SWAP", "DROP", "PRINT", "LABEL", "JMP", "JZ", "HALT"})


def _positive(name, value):
    if type(value) is not int or value < 1:
        raise SIError(f"{name} must be a positive integer")


def validate(code, *, max_stack=1024, max_instructions=MAX_INSTRUCTIONS):
    """Validate structural shape and reachable stack safety before execution."""
    _positive("max_stack", max_stack)
    _positive("max_instructions", max_instructions)
    if type(code) not in (tuple, list):
        raise SIError("bytecode must be a tuple or list")
    if len(code) > max_instructions:
        raise SIError("instruction limit exceeded")
    for pc, ins in enumerate(code):
        if type(ins) is not Instruction or type(ins.op) is not str or ins.op not in OPS:
            raise SIError(f"invalid opcode at {pc}")
        if ins.op == "PUSH":
            if type(ins.arg) is not int or not MIN_INT <= ins.arg <= MAX_INT:
                raise SIError(f"invalid signed 64-bit PUSH at {pc}")
        elif ins.op in ("JMP", "JZ"):
            if type(ins.arg) is not int or not 0 <= ins.arg <= len(code):
                raise SIError(f"invalid jump target at {pc}")
        elif ins.arg is not None:
            raise SIError(f"unexpected argument at {pc}")
    result = tuple(code)
    verify(result, max_stack=max_stack)
    typecheck(result, max_stack=max_stack)
    return result


def _canonical(value):
    return json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("ascii")


def dumps(code, *, max_stack=1024, max_instructions=MAX_INSTRUCTIONS):
    code = validate(code, max_stack=max_stack, max_instructions=max_instructions)
    payload = {"format": FORMAT, "instructions": [[x.op, x.arg] for x in code]}
    digest = hashlib.sha256(_canonical(payload)).hexdigest()
    result = _canonical({"payload": payload, "sha256": digest})
    if len(result) > MAX_BYTES:
        raise SIError("bytecode size limit exceeded")
    return result.decode("ascii")


def _unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


def loads(serialized, *, max_stack=1024, max_instructions=MAX_INSTRUCTIONS):
    _positive("max_stack", max_stack)
    _positive("max_instructions", max_instructions)
    if type(serialized) is not str:
        raise SIError("bytecode must be JSON text")
    if len(serialized.encode("utf-8")) > MAX_BYTES:
        raise SIError("bytecode size limit exceeded")
    try:
        data = json.loads(serialized, object_pairs_hook=_unique_pairs,
                          parse_constant=lambda x: (_ for _ in ()).throw(ValueError("nonfinite JSON number")))
    except (ValueError, TypeError, RecursionError) as exc:
        raise SIError(f"invalid JSON: {exc}") from None
    if type(data) is not dict or set(data) != {"payload", "sha256"}:
        raise SIError("invalid bytecode envelope")
    payload, digest = data["payload"], data["sha256"]
    if type(payload) is not dict or set(payload) != {"format", "instructions"} or payload["format"] != FORMAT:
        raise SIError("unsupported bytecode format")
    if type(digest) is not str or len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
        raise SIError("invalid digest")
    if not hmac.compare_digest(hashlib.sha256(_canonical(payload)).hexdigest(), digest):
        raise SIError("bytecode digest mismatch")
    rows = payload["instructions"]
    if type(rows) is not list:
        raise SIError("instructions must be a list")
    if len(rows) > max_instructions:
        raise SIError("instruction limit exceeded")
    code = []
    for pc, row in enumerate(rows):
        if type(row) is not list or len(row) != 2:
            raise SIError(f"invalid instruction at {pc}")
        code.append(Instruction(row[0], row[1]))
    return validate(tuple(code), max_stack=max_stack, max_instructions=max_instructions)


def execute_checked(serialized, *, max_steps=10_000, max_stack=1024, max_instructions=MAX_INSTRUCTIONS):
    _positive("max_steps", max_steps)
    code = loads(serialized, max_stack=max_stack, max_instructions=max_instructions)
    return execute(code, max_steps=max_steps, max_stack=max_stack)