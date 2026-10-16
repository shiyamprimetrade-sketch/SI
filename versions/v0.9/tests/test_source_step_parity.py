"""Source parser and step-budget parity across two independent SI engines."""
import random
import unittest
from si.core import run, SIError
from si.compiler import compile_source, execute

def both(source, **opts):
    return run(source, **opts), execute(compile_source(source), **opts)

class SourceStepParityTests(unittest.TestCase):
    def test_empty_program_zero_steps(self):
        self.assertEqual(both(''), ({'output': [], 'stack': [], 'steps': 0},) * 2)

    def test_comments_only_zero_steps(self):
        self.assertEqual(both('\n# comment\n  \n# another\n'), ({'output': [], 'stack': [], 'steps': 0},) * 2)

    def test_inline_comment_counts_only_instruction(self):
        a,b=both('PUSH 7 # first\n\nPRINT # second\n# trailing')
        self.assertEqual(a,b)
        self.assertEqual(a['steps'],2)
        self.assertEqual(a['output'],['7'])

    def test_comments_do_not_exhaust_step_budget(self):
        code='\n'.join(['# a']*40+['PUSH 1']+['']*40+['PRINT']+['# b']*40)
        a,b=both(code,max_steps=2)
        self.assertEqual(a,b)
        self.assertEqual(a['steps'],2)

    def test_budget_tightness_identical(self):
        source='# comment\nPUSH 7\n\nPRINT'
        for runner in (run,lambda s,**kw: execute(compile_source(s),**kw)):
            with self.assertRaisesRegex(SIError,'step budget exceeded'):
                runner(source,max_steps=1)

    def test_jump_targets_skip_comment_lines(self):
        code='\n# start\nJMP later\n# skipped\nPUSH 999\n\nLABEL later\nPUSH 2\nPRINT'
        a,b=both(code)
        self.assertEqual(a,b)
        self.assertEqual(a['output'],['2'])

    def test_comments_in_bounded_loop(self):
        source='# begin\nPUSH 3\nLABEL loop\n# loop comment\nDUP\nPRINT\nPUSH 1\nSUB\nDUP\nJZ end\nJMP loop\nLABEL end\nDROP\n# end'
        a,b=both(source)
        self.assertEqual(a,b)
        self.assertEqual(a['output'],['3','2','1'])

    def test_unreachable_unknown_opcode_rejected(self):
        for runner in (run,compile_source):
            with self.assertRaisesRegex(SIError,'unknown opcode'):
                runner('HALT\nREBOOT NOW')

    def test_unreachable_bad_arity_rejected(self):
        for runner in (run,compile_source):
            with self.assertRaisesRegex(SIError,'needs 0 args'):
                runner('HALT\nADD 100')

    def test_unreachable_bad_integer_rejected(self):
        for runner in (run,compile_source):
            with self.assertRaisesRegex(SIError,'integer required'):
                runner('HALT\nPUSH fake')

    def test_unreachable_missing_label_rejected(self):
        for runner in (run,compile_source):
            with self.assertRaisesRegex(SIError,'unknown label'):
                runner('HALT\nJMP nowhere')

    def test_unreachable_missing_conditional_target_rejected(self):
        for runner in (run,compile_source):
            with self.assertRaisesRegex(SIError,'unknown label'):
                runner('HALT\nJZ nowhere')

    def test_source_lineno_retained_with_comments(self):
        for runner in (run,compile_source):
            with self.assertRaisesRegex(SIError,'line 5: unknown opcode BAD'):
                runner('# one\n\n# three\nPUSH 3\nBAD')

    def test_dead_valid_code_after_halt(self):
        src='PUSH 8\nHALT\n# dead\nPUSH 99\nPRINT'
        a,b=both(src)
        self.assertEqual(a,b)
        self.assertEqual(a['stack'],[8])
        self.assertEqual(a['steps'],2)

    def test_zero_step_budget_with_comments_only(self):
        a,b=both('# only\n\n',max_steps=0)
        self.assertEqual(a,b)
        self.assertEqual(a['steps'],0)

    def test_seeded_metamorphic_comments_and_blanks_600(self):
        rng=random.Random(20261016)
        ops=('ADD','SUB','MUL','DIV','LT','EQ')
        for case in range(600):
            a=rng.randint(-9999,9999)
            b=rng.randint(-9999,9999) or 1
            op=rng.choice(ops)
            base=f'PUSH {a}\nPUSH {b}\n{op}\nPRINT\nHALT'
            decorated=[]
            for line in base.splitlines():
                decorated.extend(['','  # generated note','\t'] * rng.randint(0,3))
                decorated.append(line+'  # inline')
            decorated.extend(['',' # trailing comment'])
            source='\n'.join(decorated)
            reference,vm=both(source)
            self.assertEqual(reference,vm,f'case {case}')
            self.assertEqual(reference,run(base),f'metamorphic case {case}')

    def test_seeded_control_flow_comments_200(self):
        rng=random.Random(619)
        for case in range(200):
            x=rng.randrange(-100,101)
            base=f'PUSH {x}\nJZ yes\nPUSH 11\nJMP end\nLABEL yes\nPUSH 22\nLABEL end\nPRINT\nHALT'
            decorated='\n# inserted\n'.join(base.splitlines())
            reference,vm=both(decorated)
            self.assertEqual(reference,vm,f'case {case}')
            self.assertEqual(reference,run(base),f'metamorphic case {case}')

if __name__ == '__main__': unittest.main()
