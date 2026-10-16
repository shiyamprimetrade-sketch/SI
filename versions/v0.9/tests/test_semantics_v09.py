"""SI v0.9 executable-semantics conformance tests.

No formal soundness/completeness proof is claimed. Uses a separate source parser
and Fraction-based small-step evaluator, then cross-checks two SI engines.
"""
import random
import unittest

from si.core import run, SIError
from si.compiler import compile_source, execute, run_compiled
from si.reference import Machine, assemble, evaluate, transition
from si.limits import MAX_LITERAL_CHARS, MAX_SOURCE_CHARS


class OperationalSemanticsTests(unittest.TestCase):
    def assert_three(self, source, **budgets):
        expected = evaluate(source, **budgets)
        interpreter = run(source, **budgets)
        vm = execute(compile_source(source), **budgets)
        self.assertEqual(expected, interpreter, 'reference/interpreter disagreement')
        self.assertEqual(expected, vm, 'reference/VM disagreement')
        return expected

    def assert_invalid_source(self, source, needle):
        for engine in (evaluate, run, run_compiled):
            with self.subTest(engine=engine.__name__):
                with self.assertRaisesRegex(SIError, needle):
                    engine(source)

    def test_empty_program(self):
        self.assertEqual(self.assert_three(''), {'output': [], 'stack': [], 'steps': 0})

    def test_comments_only_zero_steps(self):
        self.assertEqual(self.assert_three('# comment\n\n   # ignored', max_steps=0)['steps'], 0)

    def test_arithmetic_stack_order(self):
        self.assertEqual(self.assert_three('PUSH 10\nPUSH 3\nSUB')['stack'], [7])

    def test_integer_multiplication(self):
        self.assertEqual(self.assert_three('PUSH -7\nPUSH 6\nMUL')['stack'], [-42])

    def test_integer_division_produces_float(self):
        self.assertEqual(self.assert_three('PUSH 8\nPUSH 2\nDIV')['stack'], [4.0])
        self.assertIs(type(evaluate('PUSH 8\nPUSH 2\nDIV')['stack'][0]), float)

    def test_negative_zero_division_and_print(self):
        result=self.assert_three('PUSH 0\nPUSH -3\nDIV\nPRINT')
        self.assertEqual(result['output'], ['-0.0'])

    def test_negative_zero_float_multiplication(self):
        result=self.assert_three('PUSH 0\nPUSH -3\nDIV\nPUSH 2\nMUL\nPRINT')
        self.assertEqual(result['output'], ['-0.0'])

    def test_true_and_false_equality(self):
        self.assertEqual(self.assert_three('PUSH 2\nPUSH 2\nEQ')['stack'], [1])
        self.assertEqual(self.assert_three('PUSH 2\nPUSH 3\nEQ')['stack'], [0])

    def test_comparison_order(self):
        self.assertEqual(self.assert_three('PUSH -1\nPUSH 5\nLT')['stack'], [1])
        self.assertEqual(self.assert_three('PUSH 5\nPUSH -1\nLT')['stack'], [0])

    def test_dup_swap_drop(self):
        result=self.assert_three('PUSH 3\nDUP\nPUSH 7\nSWAP\nDROP\nPRINT')
        self.assertEqual(result['output'],['7'])

    def test_print_consumes_stack_top(self):
        self.assertEqual(self.assert_three('PUSH 2\nPUSH 3\nPRINT'),
                         {'output':['3'], 'stack':[2], 'steps':3})

    def test_label_counts_as_step(self):
        self.assertEqual(self.assert_three('LABEL here\nHALT')['steps'],2)

    def test_halt_skips_later_valid_instructions(self):
        self.assertEqual(self.assert_three('PUSH 7\nHALT\nPUSH 9')['stack'],[7])

    def test_jmp_executes_target_label(self):
        program='JMP skip\nPUSH 111\nLABEL skip\nPUSH 8\nPRINT'
        self.assertEqual(self.assert_three(program),
                         {'output':['8'], 'stack':[], 'steps':4})

    def test_jz_zero_branch(self):
        p='PUSH 0\nJZ yes\nPUSH 1\nJMP end\nLABEL yes\nPUSH 2\nLABEL end\nPRINT'
        self.assertEqual(self.assert_three(p)['output'],['2'])

    def test_jz_nonzero_fallthrough(self):
        p='PUSH -1\nJZ yes\nPUSH 1\nJMP end\nLABEL yes\nPUSH 2\nLABEL end\nPRINT'
        self.assertEqual(self.assert_three(p)['output'],['1'])

    def test_bounded_countdown_loop(self):
        p='PUSH 4\nLABEL loop\nDUP\nPRINT\nPUSH 1\nSUB\nDUP\nJZ end\nJMP loop\nLABEL end\nDROP'
        result=self.assert_three(p)
        self.assertEqual(result['output'],['4','3','2','1'])
        self.assertEqual(result['stack'],[])

    def test_max_steps_exact_boundary(self):
        self.assertEqual(self.assert_three('PUSH 1\nPRINT',max_steps=2)['steps'],2)

    def test_zero_budget_empty_program(self):
        self.assertEqual(self.assert_three('',max_steps=0)['steps'],0)

    def test_step_budget_exceeded(self):
        src='LABEL start\nJMP start'
        for f in (evaluate,run,run_compiled):
            with self.assertRaisesRegex(SIError,'step budget exceeded'):
                f(src,max_steps=5)

    def test_stack_budget_exceeded(self):
        for f in (evaluate,run,run_compiled):
            with self.assertRaisesRegex(SIError,'stack budget exceeded'):
                f('PUSH 1\nPUSH 2',max_stack=1)

    def test_output_budget_exact(self):
        self.assertEqual(self.assert_three('PUSH 23\nDUP\nPRINT\nPRINT',max_output_chars=4)['output'],['23','23'])

    def test_output_budget_exceeded(self):
        for f in (evaluate,run,run_compiled):
            with self.assertRaisesRegex(SIError,'output budget exceeded'):
                f('PUSH 23\nDUP\nPRINT\nPRINT',max_output_chars=3)

    def test_integer_overflow_multiplication(self):
        src='PUSH '+('9'*MAX_LITERAL_CHARS)+'\nPUSH '+('9'*MAX_LITERAL_CHARS)+'\nMUL'
        for f in (evaluate,run,run_compiled):
            with self.assertRaisesRegex(SIError,'integer bit budget exceeded'):
                f(src)

    def test_large_integer_division_overflow(self):
        src='PUSH 1'+('0'*400)+'\nPUSH 1\nDIV'
        for f in (evaluate,run,run_compiled):
            with self.assertRaisesRegex(SIError,'numeric overflow'):
                f(src)

    def test_division_by_zero(self):
        for f in (evaluate,run,run_compiled):
            with self.assertRaisesRegex(SIError,'division by zero'):
                f('PUSH 1\nPUSH 0\nDIV')

    def test_malformed_quoted_source(self):
        self.assert_invalid_source('PUSH "3', 'line 1:')

    def test_unreachable_invalid_push(self):
        self.assert_invalid_source('HALT\nPUSH x', 'integer required')

    def test_unreachable_unknown_opcode(self):
        self.assert_invalid_source('HALT\nHACK', 'unknown opcode')

    def test_duplicate_label(self):
        self.assert_invalid_source('LABEL end\nLABEL end', 'duplicate label')

    def test_missing_jump_label(self):
        self.assert_invalid_source('JMP missing', 'unknown label')

    def test_case_insensitive_opcodes(self):
        self.assertEqual(self.assert_three('push 2\nlabel L\nprint')['output'], ['2'])

    def test_literal_length_limit(self):
        self.assert_invalid_source('PUSH '+('9'*(MAX_LITERAL_CHARS+1)), 'literal budget exceeded')

    def test_source_length_limit(self):
        self.assert_invalid_source('HALT\n#'+('x'*MAX_SOURCE_CHARS), 'source budget exceeded')

    def test_smallstep_immutability(self):
        program=assemble('PUSH 5\nDUP\nPRINT\nHALT')
        state0=Machine()
        state1=transition(program,state0)
        state2=transition(program,state1)
        state3=transition(program,state2)
        state4=transition(program,state3)
        self.assertEqual(state0,Machine())
        self.assertEqual(state1.stack,(5,))
        self.assertEqual(state2.stack,(5,5))
        self.assertEqual(state3.stack,(5,))
        self.assertEqual(state3.output,('5',))
        self.assertTrue(state4.halted)
        self.assertEqual(state4.steps,4)
        self.assertEqual(transition(program,state4),state4)

    def test_smallstep_errors_without_partial_mutation(self):
        program=assemble('PUSH 1\nPUSH 0\nDIV')
        before=transition(program, transition(program,Machine()))
        with self.assertRaisesRegex(SIError,'division by zero'):
            transition(program,before)
        self.assertEqual(before.stack,(1,0))
        self.assertEqual(before.steps,2)

    def test_program_counter_normal_exit_is_terminal(self):
        program=assemble('PUSH 2')
        s=transition(program,Machine())
        self.assertEqual(s.pc,len(program))
        self.assertEqual(transition(program,s),s)

    def test_empty_machine_and_program_terminal(self):
        self.assertEqual(transition((),Machine(),max_steps=0),Machine())

    def test_exhaustive_small_integer_arithmetic_715(self):
        checked=0
        for a in range(-5,6):
            for b in range(-5,6):
                for op in ('ADD','SUB','MUL','DIV','EQ','LT'):
                    if op=='DIV' and b==0:
                        continue
                    p=f'PUSH {a}\nPUSH {b}\n{op}\nPRINT'
                    self.assert_three(p)
                    checked+=1
        self.assertEqual(checked,11*11*6-11)

    def test_seeded_mixed_arithmetic_2000(self):
        rng=random.Random(20261017)
        for i in range(2000):
            a=rng.randint(-(1<<70),(1<<70))
            b=rng.randint(-(1<<70),(1<<70)) or 1
            op=rng.choice(('ADD','SUB','MUL','DIV','EQ','LT'))
            p=f'PUSH {a}\nPUSH {b}\n{op}\nPRINT'
            with self.subTest(i=i,op=op):
                self.assert_three(p)

    def test_seeded_control_flow_700(self):
        rng=random.Random(72207)
        for i in range(700):
            n=rng.randint(-10,10)
            a,b=rng.randint(-999,999),rng.randint(-999,999)
            p=(f'PUSH {n}\nJZ left\nPUSH {a}\nJMP done\n'
               f'LABEL left\nPUSH {b}\nLABEL done\nPRINT\nHALT')
            with self.subTest(i=i):
                self.assert_three(p)

    def test_seeded_comment_insertion_250(self):
        rng=random.Random(406)
        for i in range(250):
            a,b=rng.randint(-1000,1000),rng.randint(-1000,1000)
            lines=[f'PUSH {a}',f'PUSH {b}','ADD','PRINT','HALT']
            baseline='\n'.join(lines)
            enriched='\n\n# injected\n'.join(x+' #note' for x in lines)
            with self.subTest(i=i):
                self.assertEqual(self.assert_three(baseline),self.assert_three(enriched))


if __name__ == '__main__':
    unittest.main()