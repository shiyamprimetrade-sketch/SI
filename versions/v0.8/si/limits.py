"""Conservative SI resource policy; not a process/memory security sandbox."""
import math
from .errors import SIError

MAX_SOURCE_CHARS = 100_000
MAX_LITERAL_CHARS = 1_200
MAX_INTEGER_BITS = 4_096
MAX_OUTPUT_CHARS = 100_000
MAX_BYTECODE_INSTRUCTIONS = 50_000


def check_source(source):
    if not isinstance(source, str):
        raise SIError('source must be a string')
    if len(source) > MAX_SOURCE_CHARS:
        raise SIError('source budget exceeded')


def check_budget(value, label):
    if type(value) is not int or value < 0:
        raise SIError(f'invalid {label} budget')


def check_runtime_budgets(max_steps, max_stack, max_output_chars):
    check_budget(max_steps, 'step')
    check_budget(max_stack, 'stack')
    check_budget(max_output_chars, 'output')


def check_numeric(value):
    if type(value) is int:
        if value.bit_length() > MAX_INTEGER_BITS:
            raise SIError('integer bit budget exceeded')
    elif type(value) is float:
        if not math.isfinite(value):
            raise SIError('non-finite numeric result')
    else:
        raise SIError('invalid numeric operand')
    return value


def parse_integer(token, lineno):
    if len(token) > MAX_LITERAL_CHARS:
        raise SIError(f'line {lineno}: integer literal budget exceeded')
    try:
        value = int(token)
    except ValueError:
        raise SIError(f'line {lineno}: integer required') from None
    return check_numeric(value)


def apply_binary(op, a, b):
    check_numeric(a)
    check_numeric(b)
    try:
        if op == 'ADD':
            result = a + b
        elif op == 'SUB':
            result = a - b
        elif op == 'MUL':
            result = a * b
        elif op == 'DIV':
            if b == 0:
                raise SIError('division by zero')
            result = a / b
        elif op == 'LT':
            result = int(a < b)
        elif op == 'EQ':
            result = int(a == b)
        else:
            raise SIError('unknown numeric operation')
    except (OverflowError, ZeroDivisionError):
        raise SIError('numeric overflow') from None
    return check_numeric(result)


def number_to_text(value):
    check_numeric(value)
    try:
        return str(value)
    except (OverflowError, ValueError):
        raise SIError('numeric rendering failed') from None
