"""SI v0.8 strict, whole-program structural bytecode validation.

This validation is not a proof of stack safety or termination.
"""
from dataclasses import dataclass
from .errors import SIError
from .limits import MAX_BYTECODE_INSTRUCTIONS, check_numeric

VALID_OPS = frozenset({
    'PUSH', 'ADD', 'SUB', 'MUL', 'DIV', 'LT', 'EQ',
    'DUP', 'SWAP', 'DROP', 'PRINT', 'LABEL', 'JMP', 'JZ', 'HALT',
})
JUMPS = frozenset({'JMP', 'JZ'})


@dataclass(frozen=True)
class Instruction:
    op: str
    arg: int | None = None


def validate_bytecode(code: tuple[Instruction, ...]) -> tuple[Instruction, ...]:
    """Reject malformed instructions including unreachable entries.

    Jumps to exactly len(code) are valid and exit. No CFG shape proof.
    """
    if type(code) is not tuple:
        raise SIError('invalid bytecode container')
    n = len(code)
    if n > MAX_BYTECODE_INSTRUCTIONS:
        raise SIError('instruction budget exceeded')
    for pc, inst in enumerate(code):
        if type(inst) is not Instruction:
            raise SIError(f'invalid bytecode instruction at {pc}')
        op = inst.op
        if type(op) is not str or op not in VALID_OPS:
            raise SIError(f'invalid bytecode opcode (unknown opcode) at {pc}')
        if op == 'PUSH':
            if type(inst.arg) is not int:
                raise SIError(f'invalid PUSH bytecode at {pc}')
            check_numeric(inst.arg)
        elif op in JUMPS:
            if type(inst.arg) is not int or not 0 <= inst.arg <= n:
                raise SIError(f'invalid jump target at {pc}')
        elif inst.arg is not None:
            raise SIError(f'invalid bytecode argument at {pc}')
    return code
