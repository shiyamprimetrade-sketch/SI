"""SI v0.8: whole-program bytecode validation and adversarial mutations."""
import random
import unittest

from si import SIError, compile_source, execute
from si.bytecode import Instruction, validate_bytecode
from si.limits import MAX_BYTECODE_INSTRUCTIONS, MAX_INTEGER_BITS
from si.types import typecheck
from si.verify import verify, remove_unreachable


class BytecodePreflightTests(unittest.TestCase):
    def reject_all(self, code, expected):
        for fn in (validate_bytecode, execute, verify, typecheck):
            with self.subTest(fn=fn.__name__):
                with self.assertRaisesRegex(SIError, expected):
                    fn(code)

    def test_container_list(self):
        self.reject_all([Instruction('HALT')], 'invalid bytecode container')

    def test_container_generator(self):
        self.reject_all((i for i in (Instruction('HALT'),)),
                        'invalid bytecode container')

    def test_noninstruction(self):
        self.reject_all((Instruction('HALT'), object()),
                        'invalid bytecode instruction')

    def test_fake_string_instruction(self):
        self.reject_all(('HALT',), 'invalid bytecode instruction')

    def test_dead_opcode(self):
        self.reject_all((Instruction('HALT'), Instruction('EXEC')),
                        'unknown opcode')

    def test_jump_skips_bad_instruction(self):
        self.reject_all((Instruction('JMP',2),Instruction('ADD',5),
                         Instruction('HALT')), 'invalid bytecode argument')

    def test_lowercase_opcode(self):
        self.reject_all((Instruction('push',3),), 'unknown opcode')

    def test_nonstring_opcode(self):
        self.reject_all((Instruction(True),), 'unknown opcode')

    def test_bool_push(self):
        self.reject_all((Instruction('PUSH', True),), 'invalid PUSH')

    def test_float_push(self):
        self.reject_all((Instruction('PUSH',1.0),), 'invalid PUSH')

    def test_giant_integer_in_dead_code(self):
        self.reject_all((Instruction('HALT'),
                         Instruction('PUSH', 1 << (MAX_INTEGER_BITS+1))),
                        'integer bit budget exceeded')

    def test_bool_jump(self):
        self.reject_all((Instruction('JMP',True),), 'invalid jump target')

    def test_negative_jump(self):
        self.reject_all((Instruction('JMP',-1),), 'invalid jump target')

    def test_jump_over_end(self):
        self.reject_all((Instruction('HALT'),Instruction('JMP',22)),
                        'invalid jump target')

    def test_nonint_jump(self):
        self.reject_all((Instruction('JZ',1.0),), 'invalid jump target')

    def test_noop_argument(self):
        self.reject_all((Instruction('HALT', False),),
                        'invalid bytecode argument')

    def test_label_argument(self):
        self.reject_all((Instruction('LABEL','name'),),
                        'invalid bytecode argument')

    def test_big_instruction_tuple(self):
        code=(Instruction('HALT'),)*(MAX_BYTECODE_INSTRUCTIONS+1)
        self.reject_all(code,'instruction budget exceeded')

    def test_empty_program(self):
        self.assertEqual(validate_bytecode(()),())
        self.assertEqual(execute(()),{'output':[],'stack':[],'steps':0})
        self.assertEqual(typecheck(()).incoming,((),))
        self.assertEqual(verify(()).reachable,frozenset())

    def test_exit_jump_is_valid(self):
        code=(Instruction('JMP',2),Instruction('PUSH',2))
        self.assertIs(validate_bytecode(code),code)
        self.assertEqual(execute(code)['steps'],1)

    def test_unreachable_underflow_is_legal_shape(self):
        code=(Instruction('JMP',2),Instruction('ADD'),Instruction('HALT'))
        self.assertIs(validate_bytecode(code),code)
        self.assertEqual(execute(code)['steps'],2)
        self.assertNotIn(1,verify(code).reachable)

    def test_invalid_analysis_budget(self):
        code=(Instruction('HALT'),)
        for fn in (verify,typecheck):
            with self.assertRaisesRegex(SIError,'invalid stack budget'):
                fn(code,max_stack=-1)

    def test_compiler_and_optimizer_outputs_valid(self):
        code=compile_source('PUSH 8\nJMP done\nPUSH 7\nLABEL done\nPRINT')
        opt=remove_unreachable(code)
        self.assertIs(validate_bytecode(code),code)
        self.assertIs(validate_bytecode(opt),opt)
        self.assertEqual(execute(code)['output'],execute(opt)['output'])

    def test_seeded_invalid_bytecode_mutations_600(self):
        rng=random.Random(20261016)
        malformed=[
            Instruction('PUSH',True),Instruction('PUSH',1.0),
            Instruction('PUSH',object()),Instruction('PUSH',[]),
            Instruction('PUSH',1<<(MAX_INTEGER_BITS+2)),
            Instruction('JMP',False),Instruction('JZ',-9),
            Instruction('JZ',1.25),Instruction('ADD',0),
            Instruction('HALT',1),Instruction('LABEL','x'),
            Instruction('PRINT',[]),Instruction('NOP'),
            Instruction('push',0),object(),None,False
        ]
        for i in range(600):
            bad=rng.choice(malformed)
            code=(Instruction('HALT'),bad)
            with self.subTest(i=i):
                with self.assertRaises(SIError):
                    validate_bytecode(code)


if __name__ == '__main__':
    unittest.main()
