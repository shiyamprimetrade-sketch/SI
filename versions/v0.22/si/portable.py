"""SI Portable Profile 1, independently lexed without shlex or SI's compiler.

ASCII-only, canonicalizable, deliberately narrower than the v0.9 legacy syntax.
This is an optional profile; the legacy parser retains its previous behavior.
"""
from dataclasses import dataclass
from .errors import SIError
from .limits import (
    MAX_SOURCE_CHARS, MAX_LITERAL_CHARS, MAX_INTEGER_BITS,
    MAX_BYTECODE_INSTRUCTIONS,
)

OP_ARITY = {
    'PUSH': 1, 'LABEL': 1, 'JMP': 1, 'JZ': 1,
    'ADD': 0, 'SUB': 0, 'MUL': 0, 'DIV': 0,
    'LT': 0, 'EQ': 0, 'DUP': 0, 'SWAP': 0,
    'DROP': 0, 'PRINT': 0, 'HALT': 0,
}
LABEL_LIMIT = 64


@dataclass(frozen=True)
class PortableOp:
    opcode: str
    operand: int | str | None
    target: int | None
    line: int


def _label(name):
    if not name or len(name) > LABEL_LIMIT:
        return False
    first = name[0]
    if not (('a' <= first <= 'z') or ('A' <= first <= 'Z') or first == '_'):
        return False
    for char in name[1:]:
        if not (('a' <= char <= 'z') or ('A' <= char <= 'Z') or
                ('0' <= char <= '9') or char == '_'):
            return False
    return True


def _integer(token, lineno):
    if len(token) > MAX_LITERAL_CHARS:
        raise SIError(f'line {lineno}: integer literal budget exceeded')
    digits = token[1:] if token[:1] in ('+', '-') else token
    if not digits or any(not ('0' <= x <= '9') for x in digits):
        raise SIError(f'line {lineno}: nonportable integer literal')
    # Length is capped before int() conversion; no implicit Unicode digits,
    # separators, hex notation or Python-specific escape sequences.
    value = int(token, 10)
    if value.bit_length() > MAX_INTEGER_BITS:
        raise SIError('integer bit budget exceeded')
    return value


def _words(line):
    """Scan tokens using only the portable SP/HTAB/# grammar."""
    tokens = []
    token = []
    for char in line:
        if char == '#':
            break
        if char == ' ' or char == '\t':
            if token:
                tokens.append(''.join(token))
                token = []
        else:
            token.append(char)
    if token:
        tokens.append(''.join(token))
    return tokens


def parse_portable(source):
    """Parse the ASCII portable subset into typed immutable operations.

    Validation includes unreachable instructions; jump operands resolve to
    instruction indices. No shared lexer, shlex, or compiler code is used.
    """
    if type(source) is not str:
        raise SIError('source must be a string')
    if len(source) > MAX_SOURCE_CHARS:
        raise SIError('source budget exceeded')
    for offset, ch in enumerate(source):
        code = ord(ch)
        if not (32 <= code <= 126 or ch in ('\t', '\n', '\r')):
            raise SIError(f'nonportable character at offset {offset}')
    if '\r' in source.replace('\r\n', ''):
        raise SIError('bare CR line ending is not portable')
    lines = source.replace('\r\n', '\n').split('\n')
    rows = []
    labels = {}
    for lineno, line in enumerate(lines, 1):
        words = _words(line)
        if not words:
            continue
        opcode = words[0].upper()
        if opcode not in OP_ARITY:
            raise SIError(f'line {lineno}: unknown opcode {opcode}')
        if len(words) != OP_ARITY[opcode] + 1:
            raise SIError(f'line {lineno}: {opcode} needs {OP_ARITY[opcode]} args')
        operand = words[1] if len(words) == 2 else None
        if opcode in ('LABEL', 'JMP', 'JZ') and not _label(operand):
            raise SIError(f'line {lineno}: nonportable label')
        if opcode == 'LABEL':
            if operand in labels:
                raise SIError(f'line {lineno}: duplicate label {operand}')
            labels[operand] = len(rows)
        rows.append((opcode, operand, lineno))
        if len(rows) > MAX_BYTECODE_INSTRUCTIONS:
            raise SIError('instruction budget exceeded')
    operations = []
    for opcode, token, lineno in rows:
        operand = _integer(token, lineno) if opcode == 'PUSH' else token
        if opcode in ('JMP', 'JZ') and token not in labels:
            raise SIError(f'line {lineno}: unknown label {token}')
        target = labels[token] if opcode in ('JMP', 'JZ') else None
        operations.append(PortableOp(opcode, operand, target, lineno))
    return tuple(operations)


def canonical_source(program):
    """Produce stable ASCII source from parse_portable() output.

    Canonical rendering intentionally discards comments, formatting, source
    line numbers, leading zeroes and case variations in opcode spelling.
    """
    if type(program) is not tuple or any(type(x) is not PortableOp for x in program):
        raise SIError('invalid portable program')
    lines = []
    for inst in program:
        if inst.opcode in ('LABEL', 'JMP', 'JZ'):
            lines.append(inst.opcode + ' ' + inst.operand)
        elif inst.opcode == 'PUSH':
            lines.append('PUSH ' + str(inst.operand))
        else:
            lines.append(inst.opcode)
    return '\n'.join(lines)


def structural_signature(program):
    """Semantic parse signature excluding line numbers, for proof obligations."""
    return tuple((op.opcode, op.operand, op.target) for op in program)


def roundtrip_obligation(source):
    """Executable assertion for a supplied source, NOT universal proof."""
    first = parse_portable(source)
    second = parse_portable(canonical_source(first))
    if structural_signature(first) != structural_signature(second):
        raise SIError('canonical roundtrip obligation failed')
    return True