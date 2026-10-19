import unittest
from si import run,SIError
class SITests(unittest.TestCase):
    def test_arithmetic(self):self.assertEqual(run('PUSH 7\nPUSH 6\nMUL\nPRINT')['output'],['42'])
    def test_order(self):self.assertEqual(run('PUSH 10\nPUSH 3\nSUB')['stack'],[7])
    def test_division(self):self.assertEqual(run('PUSH 9\nPUSH 3\nDIV')['stack'],[3.0])
    def test_zero(self):
        with self.assertRaises(SIError):run('PUSH 1\nPUSH 0\nDIV')
    def test_underflow(self):
        with self.assertRaises(SIError):run('ADD')
    def test_unknown(self):
        with self.assertRaises(SIError):run('SYSTEM rm')
    def test_loop(self):
        src='PUSH 3\nLABEL loop\nDUP\nPRINT\nPUSH 1\nSUB\nDUP\nJZ end\nJMP loop\nLABEL end\nDROP'
        self.assertEqual(run(src)['output'],['3','2','1'])
    def test_budget(self):
        with self.assertRaisesRegex(SIError,'budget'):run('LABEL loop\nJMP loop',max_steps=30)
    def test_stack_limit(self):
        with self.assertRaisesRegex(SIError,'stack budget'):run('PUSH 1\nPUSH 2',max_stack=1)
    def test_no_code_execution(self):
        with self.assertRaises(SIError):run('PUSH __import__("os")')
    def test_comments(self):self.assertEqual(run('PUSH 2 #comment\nPRINT')['output'],['2'])
    def test_bad_label(self):
        with self.assertRaises(SIError):run('JMP missing')
if __name__=='__main__':unittest.main()