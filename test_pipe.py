from pipe import _pipe
import unittest
from unittest import skip
from functools import partial


class test_pipe(unittest.TestCase):

    def test_no_args_single_pipe(self):
        fnc = lambda: 1
        proc = _pipe(fnc)
        gold = 1
        output = proc().run()
        self.assertEqual(gold, output)

    def test_one_arg_single_pipe(self):
        fnc = lambda x: x + 1
        proc = _pipe(fnc)
        gold = 2
        output = proc(1).run()
        self.assertEqual(gold, output)

    def test_mult_args_single_pipe(self):
        fnc = lambda x, y: x * y
        proc = _pipe(fnc)
        gold = 6
        output = proc(2, 3).run()
        self.assertEqual(gold, output)
    
    def test_bad_other_arity(self):
        fnc1 = lambda x: x + 1
        fnc2 = lambda: 1
        proc1 = _pipe(fnc1)
        proc2 = _pipe(fnc2)
        with self.assertRaises(ValueError):
            proc1(1) | proc2

    def test_two_pipes(self):
        fnc1 = lambda x: x + 1
        fnc2 = lambda y: y + 1
        proc1 = _pipe(fnc1)
        proc2 = _pipe(fnc2)
        gold = 3
        output = proc1(1) | proc2
        output = output.run()
        self.assertEqual(gold, output)

    def test_mult_pipes(self):
        fnc1 = lambda: 1
        fnc2 = lambda y: y + 1
        fnc3 = lambda z: z + 1
        proc1 = _pipe(fnc1)
        proc2 = _pipe(fnc2)
        proc3 = _pipe(fnc3)
        gold = 3
        output = proc1 | proc2 | proc3
        output = output.run()
        self.assertEqual(gold, output)

    def test_useless_args(self):
        fnc1 = lambda x: x + 1
        fnc2 = lambda y: y + 1
        proc1 = _pipe(fnc1)
        proc2 = _pipe(fnc2)
        gold = 3
        output = proc1(1) | proc2(4)  # proc2 arg does nothing but set self.args
        output = output.run()
        self.assertEqual(gold, output)

    def test_second_pipe_mult_inputs(self):
        fnc1 = lambda: (2, 3)
        fnc2 = lambda x, y: x * y
        proc1 = _pipe(fnc1)
        proc2 = _pipe(fnc2)
        gold = 6
        output = proc1() | proc2
        output = output.run()
        self.assertEqual(gold, output)

    def test_first_pipe_no_call(self):
        fnc1 = lambda: (2, 3)
        fnc2 = lambda x, y: x * y
        proc1 = _pipe(fnc1)
        proc2 = _pipe(fnc2)
        gold = 6
        output = proc1 | proc2
        output = output.run()
        self.assertEqual(gold, output)


if __name__ == "__main__":
    unittest.main()
