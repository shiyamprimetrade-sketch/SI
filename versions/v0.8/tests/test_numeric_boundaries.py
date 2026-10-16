"""Focused v0.7 regression cases: source, numeric, bytecode and output limits."""
import random
import unittest

from si import SIError, run, run_compiled, compile_source, execute
from si.compiler import Instruction
from si.limits import (
    MAX_SOURCE_CHARS, MAX_LITERAL_CHARS, MAX_INTEGER_BITS, MAX_OUTPUT_CHARS,
)

class NumericBoundaryTests(unittest.TestCase):
    def both(self, src, **opts):
        return run(src, **opts), run_compiled(src, **opts)

    def reject_both(self, src, expected, **opts):
        for engine in (run, run_compiled):
            with self.subTest(engine=engine.__name__, expected=expected):
                with self.assertRaisesRegex(SIError, expected):
                    engine(src, **opts)

    def test_huge_division_reports_si_error(self):
        self.reject_both('PUSH ' + '1' + '0'*400 + '\nPUSH 1\nDIV', 'numeric overflow')

    def test_huge_division_unreachable_is_not_executed(self):
        src = 'HALT\nPUSH ' + '1' + '0'*400 + '\nPUSH 1\nDIV'
        a,b=self.both(src)
        self.assertEqual(a,b)
        self.assertEqual(a['steps'],1)

    def test_non_finite_float_result_is_rejected(self):
        src = ('PUSH ' + '1' + '0'*300 +
               '\nPUSH 1\nDIV\nPUSH 1\nPUSH ' + '1' + '0'*300 +
               '\nDIV\nDIV')
        self.reject_both(src, 'non-finite numeric result')

    def test_large_literal_has_defined_limit(self):
        self.reject_both('PUSH ' + '9'*(MAX_LITERAL_CHARS+1),
                         'integer literal budget exceeded')

    def test_dead_large_literal_rejected_during_source_validation(self):
        self.reject_both('HALT\nPUSH ' + '9'*(MAX_LITERAL_CHARS+1),
                         'integer literal budget exceeded')

    def test_1200_digit_literal_is_accepted(self):
        src = 'PUSH ' + '9'*MAX_LITERAL_CHARS
        a,b=self.both(src)
        self.assertEqual(a,b)
        self.assertLessEqual(a['stack'][0].bit_length(), MAX_INTEGER_BITS)

    def test_arithmetic_bit_budget_exceeded(self):
        src='PUSH ' + '9'*MAX_LITERAL_CHARS + '\nPUSH ' + '9'*MAX_LITERAL_CHARS + '\nMUL'
        self.reject_both(src, 'integer bit budget exceeded')

    def test_arithmetic_small_numbers_regression(self):
        a,b=self.both('PUSH 9\nPUSH 3\nDIV\nPUSH 2\nMUL\nPRINT')
        self.assertEqual(a,b)
        self.assertEqual(a['output'], ['6.0'])

    def test_source_budget_enforced_before_parsing(self):
        long_src='#'+('x'*MAX_SOURCE_CHARS)
        self.reject_both(long_src, 'source budget exceeded')

    def test_source_budget_rejects_without_execution(self):
        long_src='HALT\n#'+('a'*MAX_SOURCE_CHARS)
        self.reject_both(long_src, 'source budget exceeded')

    def test_nontext_input_rejected(self):
        for engine in (run, run_compiled):
            with self.assertRaisesRegex(SIError,'source must be a string'):
                engine(b'PUSH 1')

    def test_output_budget_exact_boundary(self):
        src='PUSH 123\nDUP\nPRINT\nPRINT'
        a,b=self.both(src,max_output_chars=6)
        self.assertEqual(a,b)
        self.assertEqual(a['output'],['123','123'])

    def test_output_budget_exceeded(self):
        src='PUSH 123\nDUP\nPRINT\nPRINT'
        self.reject_both(src,'output budget exceeded',max_output_chars=5)

    def test_output_budget_zero_with_empty_output(self):
        a,b=self.both('PUSH 123\nHALT',max_output_chars=0)
        self.assertEqual(a,b)

    def test_invalid_negative_runtime_budgets(self):
        for opts, message in (({'max_steps':-1},'invalid step budget'),
                              ({'max_stack':-1},'invalid stack budget'),
                              ({'max_output_chars':-1},'invalid output budget')):
            self.reject_both('HALT',message,**opts)

    def test_invalid_boolean_runtime_budget(self):
        self.reject_both('HALT','invalid step budget',max_steps=True)

    def test_invalid_big_integer_in_manual_bytecode(self):
        with self.assertRaisesRegex(SIError,'integer bit budget exceeded'):
            execute((Instruction('PUSH',1 << (MAX_INTEGER_BITS+1)),))

    def test_invalid_float_in_manual_bytecode(self):
        for value in (float('inf'),float('nan')):
            with self.assertRaisesRegex(SIError,'invalid PUSH bytecode'):
                execute((Instruction('PUSH',value),))

    def test_invalid_negative_jump_target_rejected(self):
        with self.assertRaisesRegex(SIError,'invalid jump target'):
            execute((Instruction('JMP',-1),),max_steps=2)

    def test_invalid_nonint_jump_target_rejected(self):
        with self.assertRaisesRegex(SIError,'invalid jump target'):
            execute((Instruction('JMP',1.0),),max_steps=2)

    def test_jump_to_exact_exit_is_valid(self):
        self.assertEqual(execute((Instruction('JMP',1),))['steps'],1)

    def test_invalid_opcode_in_manual_bytecode(self):
        with self.assertRaisesRegex(SIError,'invalid bytecode opcode'):
            execute((Instruction('EXEC'),))

    def test_seeded_numeric_parity_1000(self):
        rng=random.Random(20261016)
        for case in range(1000):
            a=rng.randrange(-10**25,10**25)
            b=rng.randrange(-10**25,10**25) or 1
            op=rng.choice(['ADD','SUB','MUL','DIV','LT','EQ'])
            src=f'PUSH {a}\nPUSH {b}\n{op}\nPRINT'
            reference,compiled=self.both(src)
            self.assertEqual(reference,compiled,f'case {case}')

    def test_output_budget_seeded_repetitions_200(self):
        rng=random.Random(16)
        for case in range(200):
            digits=str(rng.randrange(0,10**40))
            repetitions=rng.randrange(1,15)
            src='PUSH '+digits+'\n'+('DUP\nPRINT\n'*(repetitions-1))+'PRINT'
            expected=repetitions*len(digits)
            reference,compiled=self.both(src,max_output_chars=expected)
            self.assertEqual(reference,compiled,f'case {case}')
            self.assertEqual(len(''.join(reference['output'])),expected)
            self.reject_both(src,'output budget exceeded',max_output_chars=expected-1)

    def test_compile_source_limit_without_vm(self):
        with self.assertRaisesRegex(SIError,'integer literal budget exceeded'):
            compile_source('PUSH '+'9'*(MAX_LITERAL_CHARS+1))

if __name__ == '__main__':
    unittest.main()
