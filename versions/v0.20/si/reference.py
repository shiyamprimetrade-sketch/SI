"""Independent executable small-step semantics for the SI source language.

This module intentionally does not import the SI compiler, VM, reference
interpreter, or their numeric helper. It uses Fraction as a mathematical
oracle and the common public SIError and fixed policy constants.

It is an executable model for bounded programs, NOT a machine-checked proof.
"""
from dataclasses import dataclass
from fractions import Fraction
import math
import shlex

from .errors import SIError
from .limits import (
    MAX_SOURCE_CHARS, MAX_LITERAL_CHARS, MAX_INTEGER_BITS,
    MAX_BYTECODE_INSTRUCTIONS, MAX_OUTPUT_CHARS,
)

# An independent vocabulary (no reference to compiler.ARITY).
_ARITIES = {
    'PUSH': 1, 'ADD': 0, 'SUB': 0, 'MUL': 0, 'DIV': 0,
    'LT': 0, 'EQ': 0, 'DUP': 0, 'SWAP': 0, 'DROP': 0,
    'PRINT': 0, 'LABEL': 1, 'JMP': 1, 'JZ': 1, 'HALT': 0,
}
_BINARY = frozenset(('ADD', 'SUB', 'MUL', 'DIV', 'LT', 'EQ'))


@dataclass(frozen=True)
class Operation:
    opcode: str
    operand: int | None = None
    source_line: int = 0


@dataclass(frozen=True)
class Machine:
    pc: int = 0
    stack: tuple = ()
    output: tuple[str, ...] = ()
    steps: int = 0
    output_chars: int = 0
    halted: bool = False


def _budget(value, label):
    if type(value) is not int or value < 0:
        raise SIError(f'invalid {label} budget')


def _number(value):
    if type(value) is int:
        if value.bit_length() > MAX_INTEGER_BITS:
            raise SIError('integer bit budget exceeded')
    elif type(value) is float:
        if not math.isfinite(value):
            raise SIError('non-finite numeric result')
    else:
        raise SIError('invalid numeric operand')
    return value


def _literal(token, lineno):
    if len(token) > MAX_LITERAL_CHARS:
        raise SIError(f'line {lineno}: integer literal budget exceeded')
    try:
        value = int(token)
    except ValueError:
        raise SIError(f'line {lineno}: integer required') from None
    return _number(value)


def assemble(source):
    """Independently parse SI source into operations; validate unreachable text."""
    if not isinstance(source, str):
        raise SIError('source must be a string')
    if len(source) > MAX_SOURCE_CHARS:
        raise SIError('source budget exceeded')

    rows = []
    labels = {}
    for lineno, line in enumerate(source.splitlines(), 1):
        try:
            words = shlex.split(line, comments=True)
        except ValueError as error:
            raise SIError(f'line {lineno}: {error}') from None
        if not words:
            continue
        opcode = words[0].upper()
        if opcode not in _ARITIES:
            raise SIError(f'line {lineno}: unknown opcode {opcode}')
        if len(words) - 1 != _ARITIES[opcode]:
            raise SIError(f'line {lineno}: {opcode} needs {_ARITIES[opcode]} args')
        if opcode == 'LABEL':
            name = words[1]
            if name in labels:
                raise SIError(f'line {lineno}: duplicate label {name}')
            labels[name] = len(rows)
        rows.append((lineno, opcode, words[1] if len(words) == 2 else None))
        if len(rows) > MAX_BYTECODE_INSTRUCTIONS:
            raise SIError('instruction budget exceeded')

    operations = []
    for lineno, opcode, operand in rows:
        if opcode == 'PUSH':
            operand = _literal(operand, lineno)
        elif opcode in ('JMP', 'JZ'):
            if operand not in labels:
                raise SIError(f'line {lineno}: unknown label {operand}')
            operand = labels[operand]
        else:
            operand = None
        operations.append(Operation(opcode, operand, lineno))
    return tuple(operations)


def _binary(op, left, right):
    """Exact-rational oracle for integer arithmetic, IEEE host ops for float.

    Fraction supplies an independently implemented integer-only model. For
    mixed/float operations the host's binary64 operators preserve signed zero
    and rounding; those cases are not independent host-level verification.
    """
    _number(left)
    _number(right)
    a, b = Fraction(left), Fraction(right)
    if op == 'DIV' and not b:
        raise SIError('division by zero')
    if op == 'EQ':
        return int(a == b)
    if op == 'LT':
        return int(a < b)
    try:
        if type(left) is float or type(right) is float:
            # Exact-rational conversion would lose IEEE-754 negative zero.
            if op == 'ADD':
                value = left + right
            elif op == 'SUB':
                value = left - right
            elif op == 'MUL':
                value = left * right
            elif op == 'DIV':
                value = left / right
            else:
                raise SIError('unknown numeric operation')
        else:
            if op == 'ADD':
                result = a + b
            elif op == 'SUB':
                result = a - b
            elif op == 'MUL':
                result = a * b
            elif op == 'DIV':
                result = a / b
            else:
                raise SIError('unknown numeric operation')
            if op != 'DIV':
                value = int(result)
            else:
                value = float(result)
                # Python's int/int true division preserves a negative zero
                # when the mathematical numerator is exactly zero.
                if left == 0 and right < 0:
                    value = -0.0
    except (OverflowError, ZeroDivisionError):
        raise SIError('numeric overflow') from None
    return _number(value)


def transition(program, state, *, max_steps=10000, max_stack=1024,
               max_output_chars=MAX_OUTPUT_CHARS):
    """One state transition, without mutating the prior state or parsed program.

    End-of-program/halted states are terminal and cannot consume steps.
    A step budget is charged for *each executed opcode*, including LABEL/HALT.
    """
    _budget(max_steps, 'step')
    _budget(max_stack, 'stack')
    _budget(max_output_chars, 'output')
    if not isinstance(state, Machine):
        raise SIError('invalid machine state')
    if not 0 <= state.pc <= len(program):
        raise SIError('invalid machine pc')
    if state.halted or state.pc == len(program):
        return state
    if state.steps >= max_steps:
        raise SIError('step budget exceeded')

    instruction = program[state.pc]
    op = instruction.opcode
    pc, stack, output = state.pc + 1, state.stack, state.output
    chars = state.output_chars
    halted = False

    if op == 'PUSH':
        stack = stack + (_number(instruction.operand),)
    elif op in _BINARY:
        if len(stack) < 2:
            raise SIError('stack underflow')
        stack = stack[:-2] + (_binary(op, stack[-2], stack[-1]),)
    elif op == 'DUP':
        if not stack:
            raise SIError('stack underflow')
        stack = stack + (stack[-1],)
    elif op == 'SWAP':
        if len(stack) < 2:
            raise SIError('stack underflow')
        stack = stack[:-2] + (stack[-1], stack[-2])
    elif op == 'DROP':
        if not stack:
            raise SIError('stack underflow')
        stack = stack[:-1]
    elif op == 'PRINT':
        if not stack:
            raise SIError('stack underflow')
        value = _number(stack[-1])
        try:
            rendered = str(value)
        except (OverflowError, ValueError):
            raise SIError('numeric rendering failed') from None
        if chars + len(rendered) > max_output_chars:
            raise SIError('output budget exceeded')
        stack = stack[:-1]
        output = output + (rendered,)
        chars += len(rendered)
    elif op == 'LABEL':
        pass
    elif op == 'JMP':
        pc = instruction.operand
    elif op == 'JZ':
        if not stack:
            raise SIError('stack underflow')
        condition = stack[-1]
        stack = stack[:-1]
        if condition == 0:
            pc = instruction.operand
    elif op == 'HALT':
        halted = True
    else:
        raise SIError('invalid semantic opcode')

    if len(stack) > max_stack:
        raise SIError('stack budget exceeded')
    return Machine(pc, stack, output, state.steps + 1, chars, halted)


def evaluate(source, *, max_steps=10000, max_stack=1024,
             max_output_chars=MAX_OUTPUT_CHARS):
    """Run source using independent parser and small-step rules; match SI dict API."""
    _budget(max_steps, 'step')
    _budget(max_stack, 'stack')
    _budget(max_output_chars, 'output')
    program = assemble(source)
    state = Machine()
    while not state.halted and state.pc < len(program):
        state = transition(program, state, max_steps=max_steps,
                           max_stack=max_stack, max_output_chars=max_output_chars)
    return {'output': list(state.output), 'stack': list(state.stack), 'steps': state.steps}